import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

function columnLetters(number) {
  let result = "";
  while (number > 0) {
    const remainder = (number - 1) % 26;
    result = String.fromCharCode(65 + remainder) + result;
    number = Math.floor((number - 1) / 26);
  }
  return result;
}

function safeTableName(name, index) {
  return `T${index}_${name.replace(/[^A-Za-z0-9_]/g, "_")}`.slice(0, 200);
}

const payloadPath = process.argv[2];
const outputPath = process.argv[3];
const previewDir = process.argv[4];
if (!payloadPath || !outputPath || !previewDir) {
  throw new Error("Usage: node build_workbook.mjs payload.json output.xlsx preview_dir");
}

const payload = JSON.parse(await fs.readFile(payloadPath, "utf8"));
const workbook = Workbook.create();
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

for (let i = 0; i < payload.sheets.length; i += 1) {
  const spec = payload.sheets[i];
  const sheet = workbook.worksheets.add(spec.name);
  sheet.showGridLines = false;
  const matrix = [spec.headers, ...spec.rows];
  const rowCount = matrix.length;
  const colCount = spec.headers.length;
  const finalColumn = columnLetters(colCount);
  const fullRange = sheet.getRange(`A1:${finalColumn}${rowCount}`);
  fullRange.values = matrix;
  fullRange.format.font = { name: "Arial", size: 9, color: "#1F2937" };
  fullRange.format.verticalAlignment = "center";
  const header = sheet.getRange(`A1:${finalColumn}1`);
  header.format = {
    fill: "#17365D",
    font: { name: "Arial", size: 9, bold: true, color: "#FFFFFF" },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    wrapText: true,
    borders: { preset: "outside", style: "thin", color: "#17365D" },
  };
  header.format.rowHeight = 48;
  if (rowCount > 1) {
    const table = sheet.tables.add(`A1:${finalColumn}${rowCount}`, true, safeTableName(spec.name, i + 1));
    table.style = "TableStyleMedium2";
    table.showFilterButton = true;
    table.showBandedRows = true;
  }
  sheet.freezePanes.freezeRows(1);

  for (let c = 0; c < colCount; c += 1) {
    const headerName = String(spec.headers[c]).toLowerCase();
    const letter = columnLetters(c + 1);
    const column = sheet.getRange(`${letter}1:${letter}${rowCount}`);
    let width = headerName.length > 14 ? 155 : 110;
    if (headerName.includes("path") || headerName.includes("description") || headerName.includes("evidence") || headerName.includes("language") || headerName.includes("definition") || headerName === "check") width = 420;
    else if (headerName.includes("sha256")) width = 470;
    else if (headerName.includes("sample_id")) width = 220;
    else if (headerName.includes("status")) width = 500;
    else if (headerName.includes("variable")) width = 220;
    else if (headerName.includes("timestamp") || headerName.includes("date")) width = 150;
    else if (headerName === "model" || headerName === "node_id" || headerName === "bin") width = 95;
    column.format.columnWidthPx = width;
    if (/^(n|rows|columns|fold|horizon|node_order|node_order_verified|top_quartile_fold_count|folds_with_data)$/.test(headerName) || headerName.includes("count") || headerName.includes("size_bytes")) {
      if (rowCount > 1) sheet.getRange(`${letter}2:${letter}${rowCount}`).format.numberFormat = "#,##0";
    } else if (headerName.includes("rate") || headerName.includes("pct") || headerName.includes("ratio")) {
      if (rowCount > 1) sheet.getRange(`${letter}2:${letter}${rowCount}`).format.numberFormat = "0.0000";
    } else if (headerName.includes("mae") || headerName.includes("rmse") || headerName.includes("bias") || headerName.includes("error") || headerName.includes("mismatch") || headerName.includes("cutpoint") || headerName.includes("corridor_km")) {
      if (rowCount > 1) sheet.getRange(`${letter}2:${letter}${rowCount}`).format.numberFormat = "0.000000";
    }
  }
  if (spec.name === "README" || spec.name === "Claim_Boundaries") {
    fullRange.format.wrapText = true;
    fullRange.format.rowHeight = 44;
  }
}

const check = await workbook.inspect({
  kind: "table",
  sheetId: "README",
  range: "A1:B12",
  include: "values,formulas",
  tableMaxRows: 12,
  tableMaxCols: 4,
  maxChars: 6000,
});
await fs.writeFile(path.join(previewDir, "inspect_readme.ndjson"), check.ndjson ?? "", "utf8");

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
await fs.writeFile(path.join(previewDir, "formula_error_scan.ndjson"), errors.ndjson ?? "", "utf8");

for (const spec of payload.sheets) {
  const maxRow = Math.min(spec.rows.length + 1, 30);
  const maxCol = Math.min(spec.headers.length, 12);
  const renderRange = `A1:${columnLetters(maxCol)}${maxRow}`;
  const preview = await workbook.render({ sheetName: spec.name, range: renderRange, scale: 1, format: "png" });
  await fs.writeFile(path.join(previewDir, `${spec.name}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
