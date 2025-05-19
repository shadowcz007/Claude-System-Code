from typing import List, Dict, Any
from .models import Database

class DatabaseOperations:
    def __init__(self, db: Database):
        self.db = db
        
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """执行通用SQL查询
        
        Args:
            sql: SQL查询语句
            
        Returns:
            查询结果列表，每个结果是一个字典
        """
        self.db.cursor.execute(sql)
        
        # 获取列名
        columns = [description[0] for description in self.db.cursor.description]
        
        # 将结果转换为字典列表
        return [dict(zip(columns, row)) for row in self.db.cursor.fetchall()]
        
    def create(self, prompt_key: str, prompt_value: str, context_graph: str):
        """创建新记录"""
        self.db.cursor.execute('''
        INSERT INTO extracted_data (prompt_key, prompt_value, context_graph)
        VALUES (?, ?, ?)
        ''', (prompt_key, prompt_value, context_graph))
        self.db.conn.commit()
        
    def update(self, id: int, prompt_key: str, prompt_value: str, context_graph: str):
        """更新记录"""
        self.db.cursor.execute('''
        UPDATE extracted_data 
        SET prompt_key = ?, prompt_value = ?, context_graph = ?
        WHERE id = ?
        ''', (prompt_key, prompt_value, context_graph, id))
        self.db.conn.commit()
        
    def delete(self, id: int):
        """删除记录"""
        self.db.cursor.execute('DELETE FROM extracted_data WHERE id = ?', (id,))
        self.db.conn.commit()
        
    def get_by_prompt_key(self, prompt_key: str) -> List[Dict[str, Any]]:
        """按字段名称查询"""
        self.db.cursor.execute('''
        SELECT id, prompt_key, prompt_value, context_graph, timestamp
        FROM extracted_data
        WHERE prompt_key = ?
        ''', (prompt_key,))
        
        columns = ['id', 'prompt_key', 'prompt_value', 'context_graph', 'timestamp']
        return [dict(zip(columns, row)) for row in self.db.cursor.fetchall()]
    
    def get_by_prompt_value(self, prompt_value: str) -> List[Dict[str, Any]]:
        """按字段值查询"""
        self.db.cursor.execute('''
        SELECT id, prompt_key, prompt_value, context_graph, timestamp
        FROM extracted_data
        WHERE prompt_value LIKE ?
        ''', (f'%{prompt_value}%',))
        
        columns = ['id', 'prompt_key', 'prompt_value', 'context_graph', 'timestamp']
        return [dict(zip(columns, row)) for row in self.db.cursor.fetchall()]

    def get_tables(self):
        """获取所有表名"""
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in self.db.cursor.fetchall()]

    def get_table_info(self, table_name: str):
        """获取指定表的字段信息"""
        self.db.cursor.execute(f"PRAGMA table_info({table_name});")
        return [
            {"name": row[1], "type": row[2]}
            for row in self.db.cursor.fetchall()
        ]

    def get_foreign_keys(self, table_name: str):
        """获取指定表的外键信息"""
        self.db.cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        return [
            {
                "from_field": row[3],
                "to_table": row[2],
                "to_field": row[4]
            }
            for row in self.db.cursor.fetchall()
        ] 