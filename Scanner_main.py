import re

special_symbols = {
    ';':"SEMICOLON",
    ":=":"ASSIGN",
    "<":"LESSTHAN",
    "=":"EQUAL",
    "+":"PLUS",
    "-":"MINUS",
    "*":"MULT",
    "/":"DIV",
    "(":"OPENBRACKET",
    ")":"CLOSEDBRACKET"
}

def match_array(iterator, type):
    matches = []
    for x in iterator:
        matches.append([x, type])
    return matches


def sortFunc(x):
    return x[0].span()[0]+x[0].span()[1]*0.01

def format_tokens(tokens):
    final_tokens = []
    for token in tokens:
        if token[1]=='reserved word':
            token[1] = token[0].group(2).upper()
            final_tokens.append([token[0].group(2),token[1]])
        elif token[1] == 'special symbol' :
            token[1] = special_symbols[token[0].group(1)]
            final_tokens.append([token[0].group(1), token[1]])
        else:
            final_tokens.append([token[0].group(1),token[1]])
    return final_tokens

f = open("test.txt", 'r')
comment = re.sub("[{][^{}]*[}]", " ", f.read())
lines = comment.split('\n')
tokens = []
for line in lines:
    reserved_words_iterator = re.finditer(r"(\W|^)(read|if|then|else|end|repeat|until|write)(\W|$)", line)
    #line = re.sub(r'(\W|^)(read|if|then|else|end|repeat|until|write)\W', "      ", line)
    list_of_reserved_words_matches = match_array(reserved_words_iterator, 'reserved word')

    #identifiers_iterator = re.finditer('([a-zA-Z]+)', line)
    identifiers_iterator = re.finditer(r"(\b(?!(?:read|if|then|else|end|repeat|until|write)\b)[a-zA-Z]+)", line)
    list_of_identifiers_matches = match_array(identifiers_iterator, 'identifier'.upper())

    numbers_iterator = re.finditer('([0-9]+)', line)
    list_of_numbers_matches = match_array(numbers_iterator, 'number'.upper())

    symbols_iterator = re.finditer('(:=|-|=|;|[+*/<>()])', line)
    list_of_symbols_matches = match_array(symbols_iterator, 'special symbol')

    list_of_reserved_words_matches.extend(list_of_identifiers_matches)
    list_of_reserved_words_matches.extend(list_of_numbers_matches)
    list_of_reserved_words_matches.extend(list_of_symbols_matches)
    list_of_reserved_words_matches.sort(key=sortFunc)
    tokens.extend(list_of_reserved_words_matches)

final_tokens = format_tokens(tokens)
with open('outputFile.txt', 'w') as filehandle:
    for token in final_tokens:
        print(token)
        filehandle.write('%s\n' % token)
