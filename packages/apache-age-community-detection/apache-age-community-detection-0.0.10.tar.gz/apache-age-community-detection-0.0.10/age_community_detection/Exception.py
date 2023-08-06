class NotListException(Exception):
    def __repr__(self, data) :
        return f"{data} is not a valid list"

class Not2DListException(Exception):
    def __repr__(self, data) :
        return f"{data} is not a valid 2d list"

class NotAnEdgeException(Exception):
    def __repr__(self, data) :
        return f"{data} is not a valid edge"

class NodeNotExistException(Exception):
    def __repr__(self, data) :
        return f"Node {data} is not Exist in node List"

class GraphNotCreatedException(Exception):
    def __repr__(self, data) :
        return f"Graph is not created."