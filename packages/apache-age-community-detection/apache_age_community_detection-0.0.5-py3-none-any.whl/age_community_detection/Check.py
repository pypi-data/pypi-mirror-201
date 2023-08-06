from . import Exception

def Py1dList(data):
    """Check if its an 1d array List"""
    if not isinstance(data, list):
        raise Exception.NotListException(data)

def Py2dList(data):
    """Check if its an 2d array List"""
    if not isinstance(data, list) or any(not isinstance(sublist, list) for sublist in data):
        raise Exception.Not2DListException(data)

def EdgeArray(edges):
    """check if its an array of 2 columns"""
    for e in edges:
        if (len(e)!=2):
            raise Exception.NotAnEdgeException(e)

def EdgeExistInNodes(nodes, edges):
    """Check if Edge exist in node list"""
    for u,v in edges:
        if u not in nodes:
            raise Exception.NodeNotExistException(u)
        if v not in nodes:
            raise Exception.NodeNotExistException(v)

def isGraphCreated(nodes,edges):
    """Check if Graph created of not"""
    if(nodes == None):
        raise Exception.GraphNotCreatedException()
    if(edges== None):
        raise Exception.GraphNotCreatedException()