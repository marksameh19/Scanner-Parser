import re

# read file
f = open("test.txt",'r')
lines = f.read().split('\n')
comment = 0
objects = []
tokens = []
for line in lines:
    objects.extend(line.split(' '))
for object in objects:
    start_comment = re.search('^{',object)
    end_comment = re.search('}$',object)
    if(start_comment):
        comment = 1
    if(end_comment):
        comment = 0
    if(comment==0):
        if(object.find('{')!=-1 and object.find('{')!=0):
            object = object[0:object.find('{')]
            comment = 1
        if(object=='if' or object=='then' or object=='else' or object=='end' or object=='repeat' or object=='until' or object=='read' or object=='write'):
            tokens.append(['Reserved Word',object])
            continue
        elif(object=='+' or object=='-' or object=='*' or object=='/' or object=='=' or object=='<' or object=='>' or object=='(' or object==')' or object==';' or object==':='):
            tokens.append(['Special Symbol',object])
            continue
        identifier = re.search('[a-zA-z]+;?',object)
        number = re.search('[0-9]+;?',object)
        if(identifier):
            if (object[len(object) - 1] == ';'):
                tokens.append(['identifier', object[0:len(object)-1]])
                tokens.append(['Special Symbol', ';'])
            else:
                tokens.append(['identifier',object])
        elif(number):
            if (object[len(object) - 1] == ';'):
                tokens.append(['number', object[0:len(object)-1]])
                tokens.append(['Special Symbol', ';'])
            else:
                tokens.append(['number', object])
print(tokens)