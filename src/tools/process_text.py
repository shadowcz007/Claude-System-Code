from mcp.server.fastmcp import Context

def process_text(ctx: Context, text: str) -> dict:
    """prompt_code的核心功能，用于处理输入文本，结构化存储
    Args:
        text: 待处理的输入文本
        
    Returns:
        包含处理结果的字典，包括:
        - tagged_text: 添加语义标签后的文本
        - fields: 提取的字段信息
    """
    app = ctx.request_context.lifespan_context
    
    # 1. 使用LLM生成语义标签
    tagged_text = app.prompt_engine.semantic_tagging(text)
    
    # 2. 解析标签
    fields = app.parser.extract_fields(tagged_text)
    
    # 3. 构建图结构
    app.graph.build_from_fields(fields)
    graph_json = app.graph.to_json()
    
    # 4. 存储到数据库
    for prompt_key, field_data in fields.items():
        app.db_ops.create(
            prompt_key=prompt_key,
            prompt_value=field_data['value'],
            context_graph=graph_json
        )
    
    return {
        "tagged_text": tagged_text,
        "fields": fields
    } 