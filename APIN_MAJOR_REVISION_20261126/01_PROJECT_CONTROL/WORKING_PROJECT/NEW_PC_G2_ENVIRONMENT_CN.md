# G2 新电脑运行环境记录

- OS：Windows 10 专业工作站版 10.0.19045；CPU：Intel Xeon W-11855M，6 核/12 线程；内存约 64 GB；GPU：NVIDIA RTX A3000 Laptop，6 GiB；驱动 596.72。E 盘检查时空闲约 410.9 GiB。
- 主训练环境：`00_PROJECT_CONTROL\g2_venv`，Python 3.14.3，`--system-site-packages` 复用本机预装 NumPy 2.5.0、pandas 2.3.3、scikit-learn 1.9.1、PyArrow 25.0.0；工程内安装 XGBoost 3.4.1 和 PyTorch 2.15.0+cpu。安装来源：清华 PyPI 镜像 `https://pypi.tuna.tsinghua.edu.cn/simple`；`TEMP`、`TMP`、`PIP_CACHE_DIR` 指向工程 `00_PROJECT_CONTROL`。主训练实现按冻结协议使用 CPU；PyTorch 2 线程、XGBoost 10 线程。所有实际训练记录必须注明 CPU。
- CUDA 验证环境：`00_PROJECT_CONTROL\g2_cuda_probe_venv`，同一 Python 3.14.3，安装 PyTorch 2.14.1+cu126，来源为南京大学 PyTorch wheel 镜像 `https://mirrors.nju.edu.cn/pytorch/whl/cu126/`（对应 PyTorch 官方 CUDA 12.6 wheel）。实际检查：`torch.cuda.is_available() == True`，识别 `NVIDIA RTX A3000 Laptop GPU`；在 CUDA 张量上完成 1000×1000 的加法并得到总和 2,000,000。该验证不代表正式模型已经使用 GPU，也不改变 CPU 训练结果。
- 旧迁移包内的 CPU 版 Python 依赖目录与新电脑 Python 二进制不兼容，G2 操作代码不再把它们加入 `sys.path`。原始 G0/G1 证据保持只读。
