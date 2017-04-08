import ast

from semantic_diff.dispatch import type_dispatch

class ApplicationBehavior(object):
    @type_dispatch
    def apply(self, node):
        return type_dispatch.NEXT

    # XXX what about chained assignment?
    #     what about a <= b <= c?
    def apply_Assign(self, node):
        for target in node.targets:
            self.symbols[target.id] = self.resolve(node.value)

class ResolutionBehavior(object):
    @type_dispatch(fatal=True)
    def resolve(self, node):
        return type_dispatch.NEXT

    def resolve_Num(self, node):
        return node.n

    def resolve_Name(self, node):
        return self[node.id]

class ASTContext(ApplicationBehavior, ResolutionBehavior):
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent  = None

    def push_scope(self):
        return ASTContext(self)

    def __getitem__(self, key):
        if key in self.symbols:
            return self.symbols[key]
        if self.parent is not None:
            return self.parent[key]
        # XXX better exception
        raise Exception("Symbol '{}' not found in scope".format(key))
