from mcp.server.fastmcp import Context
from src.graph.context_graph import ContextGraph

def query(ctx: Context, sql: str) -> dict:
    """构造由prompt_key组成的sql，查询extracted_data表,返回结果prompt_value
    
    Args:
        sql: SQL查询语句
        
    Returns:
        包含查询结果和关联图结构的字典:
        - results: 查询结果列表，每个结果包含结果数据和关联的图结构数据
        - count: 结果总数
    """
    app = ctx.request_context.lifespan_context
    
    # 1. 执行SQL查询
    results = app.db_ops.execute_query(sql)
    
    # 2. 获取每条记录关联的图结构
    enriched_results = []
    for result in results:
        # 从结果中获取图结构JSON
        graph_json = result.get('context_graph')
        if graph_json:
            # 构建图结构对象
            graph = ContextGraph()
            graph.from_json(graph_json)
            
            # 获取关联数据
            related_data = {
                'nodes': graph.get_all_nodes(),
                'edges': graph.get_all_edges()
            }
            
            # 合并原始数据和关联数据
            enriched_result = {
                **result,
                'related_data': related_data
            }
            enriched_results.append(enriched_result)
            del result['context_graph']
        else:
            enriched_results.append(result)
    
    return {
        'results': enriched_results,
        'count': len(enriched_results)
    } 