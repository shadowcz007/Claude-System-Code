from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware  

from src.prompt.prompt_code import PromptEngine
from src.parser.semantic_parser import SemanticParser
from src.graph.context_graph import ContextGraph
from src.db.models import Database
from src.db.operations import DatabaseOperations
from src.tools import process_text, query,get_database_fields

@dataclass
class AppContext:
    prompt_engine: PromptEngine
    parser: SemanticParser
    graph: ContextGraph
    db: Database
    db_ops: DatabaseOperations

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """管理应用程序生命周期"""
    # 初始化组件
    prompt_engine = PromptEngine()
    parser = SemanticParser()
    graph = ContextGraph()
    db = Database()
    db.connect()
    db_ops = DatabaseOperations(db)
    
    try:
        yield AppContext(
            prompt_engine=prompt_engine,
            parser=parser,
            graph=graph,
            db=db,
            db_ops=db_ops
        )
    finally:
        db.close()

# 创建MCP服务器实例
mcp = FastMCP("Prompt Code Server", 
    dependencies=[
        "beautifulsoup4",
        "networkx",
        "sqlite3"
    ],
    lifespan=app_lifespan,
    port=8080,
    host="0.0.0.0",
    debug=True,  # 开启调试模式
)

# 注册工具函数
mcp.tool()(process_text)
mcp.tool()(query)
mcp.tool()(get_database_fields)

if __name__ == "__main__":
    import uvicorn,asyncio

    starlette_app = mcp.sse_app()
    
    # 添加 CORS 中间件
    starlette_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
        expose_headers=["*"],
        max_age=3600
    )

    config = uvicorn.Config(
            starlette_app,
            host=mcp.settings.host,
            port=mcp.settings.port,
            log_level=mcp.settings.log_level.lower(),
        )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())