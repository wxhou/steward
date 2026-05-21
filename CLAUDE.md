# Steward Project

Airtest + Poco 自动化测试框架项目

## 开发环境

### Conda 环境

```bash
# 创建环境
conda create -n airtest python=3.9 -y

# 激活环境
conda activate airtest

# 安装依赖 (需要先降级 setuptools 以兼容老包)
pip install setuptools==69.0.0
pip install -r requirements.txt
```

### 环境信息

- **Python**: 3.9
- **Conda 环境名**: `airtest`
- **依赖文件**: `requirements.txt`
- **注意**: `pocoui==1.0.94` 依赖 `setuptools<80`，需要先安装 `setuptools==69.0.0`

## 依赖版本 (2026年5月)

| 包 | 版本 | 说明 |
|---|---|---|
| airtest | 1.4.3 | UI 自动化框架 |
| pocoui | 1.0.94 | Poco Android UI 自动化 (注意不是 `poco`) |
| pytest | 8.4.2 | 测试框架 |
| pytest-html | 4.2.0 | HTML 报告 |
| allure-pytest | 2.16.0 | Allure 报告 |
| pytesseract | 0.3.13 | OCR 识别 |
| pyyaml | 6.0.1 | YAML 解析 |

## 项目结构

```
steward/
├── common/           # 公共工具类
├── core/             # 核心模块 (aircore, airdevice)
├── utils/            # 工具函数
├── zhixue/           # 智学网业务模块
│   ├── images/       # 图片资源
│   ├── element/      # 页面数据 YAML
│   ├── pages/        # 页面对象
│   └── tests/        # 测试用例
└── requirements.txt
```

## 运行测试

```bash
conda activate airtest
pytest
```