import re
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    pass

class Assignment(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(Node):
    def __init__(self, value):
        self.value = value

class Var(Node):
    def __init__(self, name):
        self.name = name

def parse_expression(tokens):
    return parse_addition(tokens)

def parse_addition(tokens):
    left = parse_multiplication(tokens)
    while tokens and tokens[0] in ('+', '-'):
        op = tokens.pop(0)
        right = parse_multiplication(tokens)
        left = BinOp(left, op, right)
    return left

def parse_multiplication(tokens):
    left = parse_atom(tokens)
    while tokens and tokens[0] in ('*', '/'):
        op = tokens.pop(0)
        right = parse_atom(tokens)
        left = BinOp(left, op, right)
    return left

def parse_atom(tokens):
    if tokens and tokens[0].isdigit():
        return Num(int(tokens.pop(0)))
    elif tokens and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tokens[0]):
        return Var(tokens.pop(0))
    else:
        raise SyntaxError("Invalid expression")

def tokenize(expression):
    # Split the expression into tokens (numbers, variables, and operators)
    return [token.strip() for token in re.findall(r'\b(?:\d+|[a-zA-Z_][a-zA-Z0-9_]*)\b|\S', expression)]

def expression_to_ast(expression):
    l,r=expression.split('=')
    tokens = tokenize(r)
    expr=Assignment(Var(l),'=',parse_expression(tokens))
    return expr

def ast_to_graph(ast_node, graph,label,label_counter=None):
    if label_counter is None:
        label_counter = {'=': 1, '+': 1, '-': 1, '*': 1, '/': 1}  # Initialize label counter

    def get_unique_label(op):
        unique_label = f"{op}_{label_counter[op]}"
        label_counter[op] += 1
        return unique_label
    if isinstance(ast_node, BinOp):
        label[ast_node]=get_unique_label(ast_node.op)
        graph.add_node(ast_node, label=label)
        ast_to_graph(ast_node.left, graph,label,label_counter)
        ast_to_graph(ast_node.right, graph,label,label_counter)
        graph.add_edge(ast_node.left, ast_node)
        graph.add_edge(ast_node.right, ast_node)
    elif isinstance(ast_node, Num):
        label[ast_node]=ast_node.value
        graph.add_node(ast_node, label=label)
    elif isinstance(ast_node, Var):
        label[ast_node]=ast_node.name
        graph.add_node(ast_node, label=label)
    elif isinstance(ast_node,Assignment):
        label[ast_node]=get_unique_label(ast_node.op)
        graph.add_node(ast_node, label=label)
        ast_to_graph(ast_node.left, graph,label,label_counter)
        ast_to_graph(ast_node.right, graph,label,label_counter)
        graph.add_edge( ast_node,ast_node.left)
        graph.add_edge(ast_node.right, ast_node)

def read_txt_getExpr(fileName):
    with open(fileName,"r",encoding='utf-8') as f:
        s=f.readlines()
    return s

def clean_expr(expr_list):
    for i,expr in zip(range(len(expr_list)),expr_list):
        expr=expr.replace(' ','')
        expr=expr.replace('\n','')
        expr_list[i]=expr

def tokenize(expression):
    return [token.strip() for token in re.findall(r'\b(?:\d+|[a-zA-Z_][a-zA-Z0-9_]*)\b|\S', expression)]


def variableDependency_Dict(expr_list):
    dep={}
    for i,expr in  zip(range(len(expr_list)),expr_list):
        left,right =expr.split('=')
        if left in dep:
            dep[left][0]+='W'
            dep[left][1]+=str(i)
        elif left not in dep:
            dep[left]=[None,None]
            dep[left][0]='W'
            dep[left][1]=str(i)
        for c in tokenize(right):
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', c):
                if c in dep:
                    dep[c][0]+='R'
                    dep[c][1]+=str(i)
                elif c not in dep:
                    dep[c]=[None,None]
                    dep[c][0]='R'
                    dep[c][1]=str(i)
        
    return dep
#This does not take care or the dependencies
def create_DFG(fileName):
    graph = nx.DiGraph()
    label={}
    expr_List=read_txt_getExpr('Expr.txt')
    clean_expr(expr_List)
    label_counter = {'=': 1, '+': 1, '-': 1, '*': 1, '/': 1}
    for expr in expr_List:
        ast_eq=expression_to_ast(expr)
        
        ast_to_graph(ast_node=ast_eq,graph=graph,label=label,label_counter=label_counter)
    graph=nx.relabel_nodes(graph,label)
    return graph

def display_Graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=400, node_color='lightblue', font_size=8)
    plt.show()


G=create_DFG('Expr.txt')
display_Graph(G)
print(variableDependency_Dict(read_txt_getExpr('Expr.txt')))