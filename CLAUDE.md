# Steward Project

Airtest + Poco 自动化测试框架项目

## 开发环境

### Conda 环境

```bash
# 创建环境
conda create -n airtest python=3.9 -y

# 激活环境
conda activate airtest

# 安装依赖
pip install -r requirements.txt
```

### 环境信息

- **Python**: 3.9
- **Conda 环境名**: `airtest`
- **依赖文件**: `requirements.txt`

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