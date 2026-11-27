import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# =========================
# 1. 基本配置
# =========================
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
TIMEZONE = "Asia/Kuala_Lumpur"

START_DATE = "2025-12-01"
END_DATE   = "2026-02-28"

# 输出目录
OUTPUT_DIR = "daily_weather_xlsx"

# 7 个监测点
POINTS = [
    {"point_id": "P1", "latitude": 1.513, "longitude": 110.312},
    {"point_id": "P2", "latitude": 1.450, "longitude": 110.144},
    {"point_id": "P3", "latitude": 1.482, "longitude": 110.025},
    {"point_id": "P4", "latitude": 1.618, "longitude": 109.877},
    {"point_id": "P5", "latitude": 1.751, "longitude": 109.760},
    {"point_id": "P6", "latitude": 1.885, "longitude": 109.667},
    {"point_id": "P7", "latitude": 2.000, "longitude": 109.638},
]

# 需要下载的变量
HOURLY_VARS = [
    "temperature_2m",
    "precipitation",
    "rain",
    "weather_code",
    "wind_speed_10m"
]


# =========================
# 2. 日期工具
# =========================
def daterange(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    current = start
    while current <= end:
        yield current.strftime("%Y-%m-%d")
        current += timedelta(days=1)


# =========================
# 3. 请求单天数据（7个点一起）
# =========================
def fetch_one_day_all_points(date_str: str):
    latitudes = ",".join(str(p["latitude"]) for p in POINTS)
    longitudes = ",".join(str(p["longitude"]) for p in POINTS)

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "start_date": date_str,
        "end_date": date_str,
        "hourly": ",".join(HOURLY_VARS),
        "timezone": TIMEZONE
    }

    resp = requests.get(BASE_URL, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


# =========================
# 4. 解析返回结果
# =========================
def parse_response_to_hourly_df(json_data, date_str: str) -> pd.DataFrame:
    rows = []

    # 多点时通常返回 list；做兼容处理
    if isinstance(json_data, list):
        data_list = json_data
    else:
        data_list = [json_data]

    if len(data_list) != len(POINTS):
        print(f"[WARN] {date_str}: 预期 {len(POINTS)} 个点，实际返回 {len(data_list)} 个")

    for idx, item in enumerate(data_list):
        point_info = POINTS[idx] if idx < len(POINTS) else {
            "point_id": f"P{idx+1}",
            "latitude": None,
            "longitude": None
        }

        hourly = item.get("hourly", {})
        times = hourly.get("time", [])

        if not times:
            print(f"[WARN] {date_str} - {point_info['point_id']} 无 hourly 数据")
            continue

        temperature_vals   = hourly.get("temperature_2m", [None] * len(times))
        precipitation_vals = hourly.get("precipitation", [None] * len(times))
        rain_vals          = hourly.get("rain", [None] * len(times))
        weather_code_vals  = hourly.get("weather_code", [None] * len(times))
        wind_vals          = hourly.get("wind_speed_10m", [None] * len(times))

        for i, t in enumerate(times):
            rows.append({
                "point_id": point_info["point_id"],
                "latitude": point_info["latitude"],
                "longitude": point_info["longitude"],
                "datetime_hourly": t,
                "temperature_2m": temperature_vals[i],
                "precipitation": precipitation_vals[i],
                "rain": rain_vals[i],
                "weather_code": weather_code_vals[i],
                "wind_speed_10m": wind_vals[i],
            })

    df = pd.DataFrame(rows)

    if not df.empty:
        df["datetime_hourly"] = pd.to_datetime(df["datetime_hourly"])
        df["date"] = df["datetime_hourly"].dt.date.astype(str)

    return df


# =========================
# 5. 小时数据扩展为30分钟
# =========================
def hourly_to_30min(df_hourly: pd.DataFrame) -> pd.DataFrame:
    if df_hourly.empty:
        return df_hourly.copy()

    all_parts = []

    for point_id, group in df_hourly.groupby("point_id"):
        group = group.sort_values("datetime_hourly").copy()

        part_00 = group.copy()
        part_00["datetime_30min"] = part_00["datetime_hourly"]

        part_30 = group.copy()
        part_30["datetime_30min"] = part_30["datetime_hourly"] + pd.Timedelta(minutes=30)

        merged = pd.concat([part_00, part_30], ignore_index=True)
        merged = merged.sort_values("datetime_30min").reset_index(drop=True)
        all_parts.append(merged)

    df_30 = pd.concat(all_parts, ignore_index=True)
    df_30["date"] = df_30["datetime_30min"].dt.date.astype(str)
    df_30["time"] = df_30["datetime_30min"].dt.strftime("%H:%M:%S")
    df_30["year"] = df_30["datetime_30min"].dt.year
    df_30["month"] = df_30["datetime_30min"].dt.month
    df_30["day"] = df_30["datetime_30min"].dt.day

    df_30 = df_30[
        [
            "point_id", "latitude", "longitude",
            "datetime_30min", "date", "time", "year", "month", "day",
            "temperature_2m", "precipitation", "rain", "weather_code", "wind_speed_10m",
            "datetime_hourly"
        ]
    ].sort_values(["point_id", "datetime_30min"]).reset_index(drop=True)

    return df_30


# =========================
# 6. 每天单独导出一个 Excel
# =========================
def export_one_day_excel(df_day_30min: pd.DataFrame, date_str: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{date_str}_weather.xlsx")

    # 每天每个点位应有 48 条
    check_df = (
        df_day_30min.groupby(["point_id", "date"])
        .size()
        .reset_index(name="records_30min")
        .sort_values(["point_id", "date"])
    )

    summary_df = (
        df_day_30min.groupby("point_id")[["temperature_2m", "precipitation", "rain", "wind_speed_10m"]]
        .agg(["count", "mean", "min", "max"])
    )

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_day_30min.to_excel(writer, sheet_name="weather_30min", index=False)
        check_df.to_excel(writer, sheet_name="record_check", index=False)
        summary_df.to_excel(writer, sheet_name="summary")

    print(f"[OK] 导出完成: {output_path}")


# =========================
# 7. 主程序
# =========================
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    dates = list(daterange(START_DATE, END_DATE))
    print(f"共 {len(dates)} 天，输出目录: {OUTPUT_DIR}")

    for idx, date_str in enumerate(dates, start=1):
        try:
            print(f"[{idx}/{len(dates)}] 下载并导出 {date_str} ...")

            # 下载该日 7 点小时数据
            json_data = fetch_one_day_all_points(date_str)
            df_hourly = parse_response_to_hourly_df(json_data, date_str)

            if df_hourly.empty:
                print(f"[WARN] {date_str} 没有有效数据，跳过")
                continue

            # 扩展为 30 分钟
            df_30min = hourly_to_30min(df_hourly)

            # 只保留当天文件
            df_30min = df_30min[df_30min["date"] == date_str].copy()

            # 导出 Excel
            export_one_day_excel(df_30min, date_str, OUTPUT_DIR)

            # 轻微延时，避免请求过快
            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"[ERROR] {date_str} 请求失败: {e}")
        except Exception as e:
            print(f"[ERROR] {date_str} 处理失败: {e}")

    print("[DONE] 全部日期处理完成")


if __name__ == "__main__":
    main()