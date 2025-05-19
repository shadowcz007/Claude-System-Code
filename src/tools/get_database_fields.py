from typing import Dict, Any
from mcp.server.fastmcp import Context

def get_database_fields(ctx: Context) -> Dict[str, Any]:
    """用于了解prompt_code有哪些语义标签,获取prompt_code里所有唯一的 prompt_key 值
    Args:
        ctx: Context对象，包含应用程序上下文
    Returns:
        Dict包含以下信息:
        - prompt_keys: 所有唯一的 prompt_key 列表
    """
    try:
        app = ctx.request_context.lifespan_context
        db = app.db_ops
        # 查询所有唯一的 prompt_key
        db.db.cursor.execute('SELECT DISTINCT prompt_key FROM extracted_data')
        prompt_keys = [row[0] for row in db.db.cursor.fetchall()]
        db.db.cursor.execute('SELECT DISTINCT prompt_value FROM extracted_data')
        prompt_values = [row[0] for row in db.db.cursor.fetchall()]
        return {"prompt_keys": prompt_keys,
                "prompt_values": prompt_values,
                "table_name":"extracted_data"
                }
    except Exception as e:
        return {
            "error": str(e),
            "prompt_keys": [],
            "prompt_values": []
        }

if __name__ == "__main__":
    # 测试代码
    # 注意：此处需要传入 ctx
    print("请在实际环境中传入 ctx 进行测试")
