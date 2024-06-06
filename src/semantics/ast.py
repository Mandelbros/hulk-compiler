from common.utils import Scope

class Node:
    def __init__(self):
        self.scope: Scope

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations