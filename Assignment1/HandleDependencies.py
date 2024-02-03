import re

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
    # Split the expression into tokens (numbers, variables, and operators)
    return [token.strip() for token in re.findall(r'\b(?:\d+|[a-zA-Z_][a-zA-Z0-9_]*)\b|\S', expression)]

def variableDependency_Dict(expr_list):
    dep={}
    for i,expr in  zip(range(len(expr_list)),expr_list):
        left,right =expr.split('=')
        for c in tokenize(right):
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', c):
                if c in dep:
                    dep[c][0]+='R'
                    dep[c][1]+=str(i)
                elif c not in dep:
                    dep[c]=[None,None]
                    dep[c][0]='R'
                    dep[c][1]=str(i)
        if left in dep:
            dep[left][0]+='W'
            dep[left][1]+=str(i)
        elif left not in dep:
            dep[left]=[None,None]
            dep[left][0]='W'
            dep[left][1]=str(i)
        
        
    return dep


def handle_dependicies(fileName):
    lines=read_txt_getExpr(fileName)
    clean_expr(lines)
    depend=variableDependency_Dict(lines)
    for var in depend:
        curVer=0
        new_var=""
        RW_Str=depend[var][0]
        li_str=depend[var][1]
        for l,rw in zip(li_str,RW_Str):
            if rw=='W':
                old_line=lines[int(l)]
                le,r=old_line.split('=')
                new_var=var+"_"+str(curVer)
                curVer+=1
                new_line=new_var+"="+r
                lines[int(l)]=new_line
            elif rw=='R':
                if new_var=="":
                    continue
                old_line=lines[int(l)]
                le,r=old_line.split('=')
                new_line=le+"="+r.replace(var,new_var)
                lines[int(l)]=new_line
    with open(fileName.split('.txt')[0]+"_NoDep.txt", 'w') as output_file:
        output_file.write('\n'.join(lines))

handle_dependicies('Assignment1/Expr.txt')