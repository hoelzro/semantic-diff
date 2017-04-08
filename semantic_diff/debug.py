from __future__ import print_function
import ast

class DumpVisitor(ast.NodeVisitor):
    def __init__(self):
        self.depth = 0
        self.indent = '  '

    def visit_children(self, node):
        self.depth += 1
        try:
            super(DumpVisitor, self).generic_visit(node)
        finally:
            self.depth -= 1

    def print(self, *values):
        print(self.indent * self.depth, ' '.join(str(v) for v in values), sep='')

    def visit_Module(self, node):
        self.print('Module')
        self.visit_children(node)

    def visit_Assign(self, node):
        self.print('Assign')
        self.visit_children(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.print('Name (store)', node.id)
        elif isinstance(node.ctx, ast.Load):
            self.print('Name (load)', node.id)
        else:
            raise Exception('Unable to handle name context: ' + str(node.ctx))

    def visit_Store(self, node):
        self.print('Store')
        self.visit_children(node)

    def visit_Num(self, node):
        self.print('Num', node.n)
        self.visit_children(node)

    def visit_Print(self, node):
        self.print('Print')
        self.visit_children(node)

    def visit_Load(self, node):
        self.print('Load')
        self.visit_children(node)

    def generic_visit(self, node):
        raise Exception("Can't handle node: " + str(node))

def dump_ast(node):
    DumpVisitor().visit(node)
