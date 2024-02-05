import re
import networkx as nx
import matplotlib.pyplot as plt

#parent Node
class Node:
    pass

class Assignment(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

#Extending class Binary operation from Node class
class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

#Extended class Num: to hold constant values
class Num(Node):
    def __init__(self, value):
        self.value = value

#Extended class Var: to hold variables
class Var(Node):
    def __init__(self, name):
        self.name = name

def parse_expression(tokens):
    return parse_addition(tokens)

#function to parse addition/subtraction operation and variables/constants involved
def parse_addition(tokens):
    left = parse_multiplication(tokens)
    while tokens and tokens[0] in ('+', '-'):
        op = tokens.pop(0)
        right = parse_multiplication(tokens)
        left = BinOp(left, op, right)
    return left

#function to parse mult/division operation and variables/constants involved
def parse_multiplication(tokens):
    left = parse_atom(tokens)
    while tokens and tokens[0] in ('*', '/'):
        op = tokens.pop(0) #popping operation from statement
        right = parse_atom(tokens) # assigning constant/variable to right
        left = BinOp(left, op, right)
    return left

#parsing constants or variables
def parse_atom(tokens):
    if tokens and tokens[0].isdigit():
        return Num(int(tokens.pop(0)))
    elif tokens and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tokens[0]):
        return Var(tokens.pop(0))
    else:
        raise SyntaxError("Invalid expression")

# tokenizes the expression based on assignment operator (=) and sends the remaining expression to 
#be parsed.
def expression_to_ast(expression):
    l,r=expression.split('=')
    tokens = tokenize(r)
    expr=Assignment(Var(l),'=',parse_expression(tokens))
    return expr

def check_if_Variable_alreadyInGraph(graph,node):
    for visit in list(graph.nodes()):
        if isinstance(visit,Var):
            if node.name==visit.name:
                node=visit
                return True
            
    return False
            

#adding nodes and edges to graph, for operator, number, variable
def ast_to_graph(ast_node, graph,label,label_counter=None):
    if label_counter is None:
        label_counter = {'=': 1, '+': 1, '-': 1, '*': 1, '/': 1}  # Initialize label counter

    def get_unique_label(op):
        unique_label = f"{op}_{label_counter[op]}"
        label_counter[op] += 1
        return unique_label
    #Adding nodes, edges to DFG
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

#reading input expression file 
def read_txt_getExpr(fileName):
    with open(fileName,"r",encoding='utf-8') as f:
        s=f.readlines()
    return s

#Removing space and nexrline from expression
def clean_expr(expr_list):
    for i,expr in zip(range(len(expr_list)),expr_list):
        expr=expr.replace(' ','')
        expr=expr.replace('\n','')
        expr_list[i]=expr

#tokenize the expression using regex
def tokenize(expression):
    return [token.strip() for token in re.findall(r'\b(?:\d+|[a-zA-Z_][a-zA-Z0-9_]*)\b|\S', expression)]

#creating a dictionary for every variable in expr, for Write/Read and how many times
#key:value = variable:[W/R, <expression_line>]
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
    expr_List=read_txt_getExpr(fileName)
    clean_expr(expr_List)
    label_counter = {'=': 1, '+': 1, '-': 1, '*': 1, '/': 1}
    for expr in expr_List:
        ast_eq=expression_to_ast(expr)
        
        ast_to_graph(ast_node=ast_eq,graph=graph,label=label,label_counter=label_counter)
    graph=nx.relabel_nodes(graph,label)
    return graph

#Function to display the graph using matplotlib
def display_Graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=400, node_color='lightblue', font_size=8)
    plt.show()


G=create_DFG('Assignment1/Expr_NoDep.txt')
display_Graph(G)
print(variableDependency_Dict(read_txt_getExpr('Assignment1/Expr_NoDep.txt')))
