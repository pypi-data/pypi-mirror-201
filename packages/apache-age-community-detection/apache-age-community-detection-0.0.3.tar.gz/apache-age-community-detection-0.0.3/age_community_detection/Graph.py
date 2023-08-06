from . import Check
from . import Lib

class Graph:
    def __init__(self):
        self.nodes = None
        self.edges = None
    
    def createGraph(self, nodes, edges):
        Check.Py1dList(nodes)
        Check.Py2dList(edges)
        Check.EdgeArray(edges)
        Check.EdgeExistInNodes(nodes,edges)
        self.nodes = nodes
        self.edges = edges

    def __str__(self):
        return f"Graph with nodes : {self.nodes} edges : ({self.edges})"
    
    def get_community(self):
        Check.isGraphCreated(self.nodes, self.edges)
        return Lib.get_community(self.nodes,self.edges)

