# LLM系统提示语义处理方案

基于LLM的系统提示语义处理解决方案，用于将自然语言转换为结构化的语义标签数据。

## 功能特点

- 使用LLM进行语义标签转换
- 支持字段和值提取
- 构建上下文关系图结构
- SQLite数据持久化存储

## 安装

1. 创建并激活Python虚拟环境:

Windows:
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.\.venv\Scripts\activate

# 确认Python解释器位置
where python
```

Linux/Mac:
```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 确认Python解释器位置
which python
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

## 使用方法

1. 确保虚拟环境已激活，终端提示符前应显示(venv)

2. 配置OpenAI API密钥:
修改.env文件

3. 运行主程序:
```bash
python main.py
```

## 项目结构

```
project_root/
├── src/              # 源代码
├── tests/            # 测试用例
├── config/           # 配置文件
├── data/             # 数据文件
├── .venv/             # Python虚拟环境
└── main.py          # 主入口
```

## 开发指南

1. 激活虚拟环境后安装开发依赖:
```bash
pip install -r requirements.txt
```

2. 运行测试:
```bash
pytest tests/
```

## 许可证

MIT License 