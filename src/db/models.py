import sqlite3
from pathlib import Path
from typing import Optional

class Database:
    def __init__(self, db_path: str = "data/database.sqlite"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        
    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
        
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            
    def _create_tables(self):
        """创建数据表"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS extracted_data (
            id INTEGER PRIMARY KEY,
            prompt_key TEXT NOT NULL,
            prompt_value TEXT,
            context_graph TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建索引
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_prompt_key 
        ON extracted_data (prompt_key)
        ''')
        
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_prompt_value 
        ON extracted_data (prompt_value)
        ''')
        
        self.conn.commit() 