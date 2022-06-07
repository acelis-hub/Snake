class Nodo():
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        
class PathFinder():
    def __init__(self):
        self.path = []

    def add(self, node):
        self.path.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.path)

    def empty(self):
        return len(self.path) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.path[0]
            self.path = self.path[1:]
            return node

