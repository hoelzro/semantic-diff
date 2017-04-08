# vim: encoding=utf-8

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
            return [(a.lineno, a.col_offset, b.lineno, b.col_offset)]
        return type_dispatch.NEXT

    def compare_Print(self, a, ctx_a, b, ctx_b):
        differences = []
        # XXX make sure that print with trailing comma doesn't compare positive

        # XXX you'll need to LCS this...
        for a_value, b_value in zip(a.values, b.values):
            if ctx_a[a_value.id] != ctx_b[b_value.id]:
                differences.append( (a_value.lineno, a_value.col_offset, b_value.lineno, b_value.col_offset) )
        return differences

    def compare_Assign(self, a, ctx_a, b, ctx_b):
        if ctx_a.resolve(a.value) != ctx_b.resolve(b.value):
            return [(a.lineno, a.col_offset, b.lineno, b.col_offset)]
        return []

        # XXX LCS/reorderings?
        #for a_target, b_target in zip(a.targets, b.targets):

    def compare_Module(self, a, ctx_a, b, ctx_b):
        ctx_a = ctx_a.push_scope()
        ctx_b = ctx_b.push_scope()
        differences = []

        # XXX LCS and canoncial reorderings
        for a_stmt, b_stmt in zip(a.body, b.body):
            result = self.compare(a_stmt, ctx_a, b_stmt, ctx_b)
            differences.extend(result)
            ctx_a.apply(a_stmt)
            ctx_b.apply(b_stmt)
        return differences

def diff(before, after):
    before_ast = ast.parse(before)
    after_ast = ast.parse(after)

    return Comparator().compare(
        before_ast,
        ASTContext(),
        after_ast,
        ASTContext())

def display_diff(differences, before, after):
    before_lines = before.rstrip('\n').split('\n')
    after_lines = after.rstrip('\n').split('\n')
    differences.sort(key=lambda d: d[2:])
    differences.reverse()

    line_no = 1
    for line in after_lines:
        annotation = [' '] * len(line)
        while differences and differences[-1][2] == line_no:
            annotation[differences.pop()[3]] = '↑'
        annotation = ''.join(annotation)
        print line
        if annotation.strip() != '':
            print annotation
        line_no += 1
