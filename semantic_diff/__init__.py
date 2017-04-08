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

class Comparator(object):
    @type_dispatch(fatal=True)
    def compare(self, a, ctx_a, b, ctx_b):
        if type(a) != type(b):
            return [(a, b)]
        return type_dispatch.NEXT

    def compare_Print(self, a, ctx_a, b, ctx_b):
        # XXX make sure that print with trailing comma doesn't compare positive

        # XXX you'll need to LCS this...
        for a_value, b_value in zip(a.values, b.values):
            if ctx_a[a_value.id] != ctx_b[b_value.id]:
                return False
        return True # XXX return something that indicates what changed

    def compare_Assign(self, a, ctx_a, b, ctx_b):
        if ctx_a.resolve(a.value) != ctx_b.resolve(b.value):
            return False # XXX better return value
        return True

        # XXX LCS/reorderings?
        #for a_target, b_target in zip(a.targets, b.targets):

    def compare_Module(self, a, ctx_a, b, ctx_b):
        ctx_a = ctx_a.push_scope()
        ctx_b = ctx_b.push_scope()

        # XXX LCS and canoncial reorderings
        for a_stmt, b_stmt in zip(a.body, b.body):
            # XXX what to do with the result?
            result = self.compare(a_stmt, ctx_a, b_stmt, ctx_b)
            if not result:
                return False # XXX LTA
            ctx_a.apply(a_stmt)
            ctx_b.apply(b_stmt)
        return True

def diff(before, after):
    before_ast = ast.parse(before)
    after_ast = ast.parse(after)

    return Comparator().compare(
        before_ast,
        ASTContext(),
        after_ast,
        ASTContext())
