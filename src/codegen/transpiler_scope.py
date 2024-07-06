from typing import Dict, List

class TranspilerScope:
    def __init__(self, parent: 'TranspilerScope | None' = None):
        self.parent: 'TranspilerScope | None' = parent
        self.root: 'TranspilerScope' = self if parent is None else parent.root
        self.curr_v: int = 0
        self.indent: int = 0
        self.c_code: List[str] = []
        self.stack_v: List[str] = []
        self.base: str = ''

        self.dict_v: Dict[str, str] = {}

    def get_code(self):                          # glob
        if self.parent is not None:             
            return self.root.get_code()

        return '\n'.join(l for l in self.c_code)
    
    def new_line(self, line: str):               # glob
        if self.parent is not None:                
            self.root.new_line(line)
            return
        
        if line == '}':
            self.indent -= 1

        tabs = '\t'*self.indent

        self.c_code.append(tabs+line)

        if line == '{':
            self.indent += 1

    def new_var(self) -> str:                     # glob
        if self.parent is not None: 
            return self.root.new_var()              

        v = 'v'+str(self.curr_v)
        self.curr_v += 1
        return v


    def push_var(self, v: str):                    # glob
        if self.parent is not None:              
            self.root.push_var(v)
            return

        self.stack_v.append(v)

    def pop_var(self) -> str:                     # glob
        if self.parent is not None:               
            return self.root.pop_var()

        v = self.stack_v[-1]
        self.stack_v.pop()

        return v

    def define_var(self, v) -> str:
        self.dict_v[v] = self.new_var()
        
        return self.dict_v[v]

    def get_var(self, v: str) -> str | None:
        if v in self.dict_v:
            return self.dict_v[v]

        if self.parent is not None:
            return self.parent.get_var(v)

        return None
 
    def child(self) -> 'TranspilerScope':
        return TranspilerScope(self)

    def define_base(self, name: str):
        self.base = name