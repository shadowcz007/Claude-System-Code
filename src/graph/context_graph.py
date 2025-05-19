import networkx as nx
import json
from typing import Dict, List, Any

class ContextGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_node(self, node_id: str, **attributes):
        """添加节点"""
        self.graph.add_node(node_id, **attributes)
        
    def add_edge(self, from_node: str, to_node: str, **attributes):
        """添加边"""
        self.graph.add_edge(from_node, to_node, **attributes)
        
    def build_from_fields(self, fields: Dict[str, Any]):
        """从字段数据构建图结构"""
        # 添加所有节点
        for prompt_key, field_data in fields.items():
            self.add_node(field_data['value'], type=prompt_key, **field_data['attributes'])
            
    def get_all_nodes(self) -> List[Dict[str, Any]]:
        """获取所有节点及其属性
        
        Returns:
            节点列表，每个节点包含id和属性
        """
        return [{"id": n, **d} for n, d in self.graph.nodes(data=True)]
    
    def get_all_edges(self) -> List[Dict[str, Any]]:
        """获取所有边及其属性
        
        Returns:
            边列表，每个边包含起点、终点和属性
        """
        return [{"from": u, "to": v, **d} for u, v, d in self.graph.edges(data=True)]
            
    def to_json(self) -> str:
        """将图结构转换为JSON格式"""
        data = {
            "nodes": self.get_all_nodes(),
            "edges": self.get_all_edges()
        }
        return json.dumps(data)
    
    def from_json(self, json_str: str):
        """从JSON格式恢复图结构"""
        data = json.loads(json_str)
        
        # 清空当前图
        self.graph.clear()
        
        # 添加节点
        for node in data["nodes"]:
            node_id = node.pop("id")
            self.add_node(node_id, **node)
            
        # 添加边
        for edge in data["edges"]:
            from_node = edge.pop("from")
            to_node = edge.pop("to")
            self.add_edge(from_node, to_node, **edge) 