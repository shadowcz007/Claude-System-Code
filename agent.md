# 基于 LLM 的System Prompt语义处理方案

## 1. 基本流程

### 1.1 字符串处理为语义标签

使用 `prompt_code` 工具（基于 LLM 的提示工程）将输入字符串转换为带语义标签的字符串。

**示例：**
- 输入：`John Doe works at ABC Corp`
- 提示：`将以下文本转换为类似 HTML 的语义标签结构：{输入文本}`
- 输出：`<person>John Doe</person> works at <company>ABC Corp</company>`

### 1.2 prompt_code 工具设计

- **输入**：原始字符串
- **输出**：带语义标签的字符串
- **方法**：零样本提示或少样本提示，结合上下文（如领域知识）提高准确性

### 1.3 字段和值提取

使用 BeautifulSoup 解析语义标签字符串，提取字段名称（标签名）和值（innerText）。

**示例：**
```json
输入：<person>John Doe</person> works at <company>ABC Corp</company>
输出：{
  "person": "John Doe",
  "company": "ABC Corp"
}
```

### 1.4 上下文关系提取（图结构）

使用 NetworkX 构建图数据结构，记录语义标签之间的关系。

**示例：**
```json
{
  "nodes": [
    {"id": "John Doe", "type": "person"},
    {"id": "ABC Corp", "type": "company"}
  ],
  "edges": [
    {"from": "John Doe", "to": "ABC Corp", "relation": "works_at"}
  ]
}
```

### 1.5 数据库存储

使用 SQLite 存储提取的字段、值和上下文关系。

**表结构：**
```sql
CREATE TABLE extracted_data (
    id INTEGER PRIMARY KEY,
    prompt_key TEXT NOT NULL,
    prompt_value TEXT,
    context_graph TEXT,  -- 存储 JSON 格式的图结构
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_prompt_key (prompt_key),
    INDEX idx_prompt_value (prompt_value(255))
);
```

**索引设计：**
- `idx_prompt_key`：加速按字段名称查询
- `idx_prompt_value`：加速按字段值查询（部分索引）

## 2. 技术选型

### 2.1 核心组件

1. **BeautifulSoup**
   - 用途：解析带语义标签的字符串
   - 优势：轻量、易用，支持 HTML/XML 解析

2. **SQLite**
   - 用途：存储字段名、值和上下文图结构
   - 优势：轻量、无服务器、易集成

3. **NetworkX**
   - 用途：构建和序列化图数据结构
   - 优势：Python 原生库，易实现

### 2.2 MCP 工具设计

1. **prompt_code**
```python
# 示例提示
"""
将以下文本转换为类似 HTML 的语义标签结构：
输入：{文本}
输出：带语义标签的字符串
"""
```

2. **数据库操作工具**
```sql
-- create
CREATE TABLE extracted_data (...);
INSERT INTO extracted_data (...) VALUES (...);

-- update
UPDATE extracted_data 
SET prompt_value = ?, context_graph = ? 
WHERE prompt_key = ? AND id = ?;

-- load
SELECT * FROM extracted_data WHERE prompt_key = ?;
```

## 3. 注意事项

### 3.1 数据完整性
- 字段名称唯一性处理
- 使用复合键或值列表存储

### 3.2 性能优化
- 合理使用索引
- 避免全文索引
- 分片处理大规模数据

### 3.3 安全性
- 使用参数化查询
- 限制 LLM SQL 生成范围
- 实现错误处理机制

### 3.4 可扩展性
- 考虑数据规模增长
- 提供回退机制
- 维护查询日志

## 4. 示例实现

```python
from bs4 import BeautifulSoup
import sqlite3
import networkx as nx
import json
import openai

# 初始化 LLM 和 prompt_code
llm = openai(model="mistral-7b")
prompt_code = lambda text: llm(f"将以下文本转换为语义标签结构：{text}")

# 1. 处理字符串
input_text = "John Doe works at ABC Corp"
tagged_text = prompt_code(input_text)

# 2. 提取字段和值
soup = BeautifulSoup(tagged_text, "html.parser")
fields = {tag.name: tag.text for tag in soup.find_all()}

# 3. 构建图结构
G = nx.DiGraph()
G.add_node("John Doe", type="person")
G.add_node("ABC Corp", type="company")
G.add_edge("John Doe", "ABC Corp", relation="works_at")
graph_json = json.dumps({
    "nodes": [{"id": n, **d} for n, d in G.nodes(data=True)],
    "edges": [{"from": u, "to": v, **d} for u, v, d in G.edges(data=True)]
})

# 4. 数据库操作
def create(table_name, data):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (...);")
    cursor.execute(f"INSERT INTO {table_name} (...) VALUES (...);")
    conn.commit()

def update(table_name, prompt_key  , prompt_value, graph_json, id):
    cursor.execute(
        f"UPDATE {table_name} SET prompt_value = ?, context_graph = ? WHERE prompt_key = ? AND id = ?;",
        (prompt_value, graph_json, prompt_key  , id)
    )
    conn.commit()

def load(query):
    cursor.execute(query)
    return cursor.fetchall()


# 6. 用户意图处理
user_query = "查找所有 person 字段"
sql_query = llm(f"将以下查询转换为 SQL：{user_query}\n表结构：extracted_data(prompt_key, prompt_value, context_graph)")
results = load(sql_query)
prompt = llm(f"基于以下数据生成提示：{results}")
print(prompt)

conn.close()
```
## 5. MCP 的参考代码

```python
# Add lifespan support for startup/shutdown with strong typing
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from fake_database import Database  # Replace with your actual DB type

from mcp.server.fastmcp import Context, FastMCP

# Create a named server
mcp = FastMCP("My App")

# Specify dependencies for deployment and development
mcp = FastMCP("My App", dependencies=["pandas", "numpy"])


@dataclass
class AppContext:
    db: Database


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        # Cleanup on shutdown
        await db.disconnect()


# Pass lifespan to server
mcp = FastMCP("My App", lifespan=app_lifespan)


# Access type-safe lifespan context in tools
@mcp.tool()
def query_db(ctx: Context) -> str:
    """Tool that uses initialized resources"""
    db = ctx.request_context.lifespan_context.db
    return db.query()

```