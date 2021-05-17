# Cleybson Cardoso Leite e José Ricardo Nogueira Magalhães
import sys
import os
import re

palavraReservadaRegex = re.compile("^(var|const|typedef|struct|extends|procedure|function|start|return|if|else|then|while|read|print|int|real|boolean|string|true|false|global|local)")
comentario_de_linha_regex = re.compile("^//.*")
start_comentario_de_bloco_regex = re.compile("^/\*")
end_comentario_de_bloco_regex = re.compile(".*\*/")
itentificador_regex = re.compile("^([A-Za-z][\w|\d]*)")
numero_regex = re.compile("^(\d+\.?\d+|\d)")
operadores_aritmeticos_regex = re.compile("^([\+\+]{2}|[\-\-]{2}|[\+|\-|\-|\*|\/|\+]{1})")
operadores_relacionais_regex = re.compile("^([==|!=|>=|<=]{2}|[>|<|=])")
operadores_logicos_regex = re.compile("^(&&|\|\||!)")
demilitadores_regex = re.compile("^([;|,|(|)|{|}|\[|\]|\.])")
cadeia_de_caracter_regex = re.compile("^(\"[A-Za-z|\w|\x20-\x21|\x23-\x7E]*\")")

# variaveis de controle
is_block_comment = False
comentario_error = False
hasError = False

# variaveis globais
erros = []

simbolo_erro_regex = re.compile("^([\x20-\x21|\x23-\x7E]{1})")
cadeira_de_caracter_erro_regex = re.compile("^(\"[A-Za-z|\w|\x20-\x21|\x23-\x7E]*)")

def main():
    global erros
    global comentario_error
    global is_block_comment
    global hasError
    inputs_diretory = "./input"
    output_diretory = "./output_lexical"

    for input_file in os.listdir(inputs_diretory):
    # for input_file in ['entrada2.txt']:
        count_line = 0
        p = re.compile('entrada(\d+).txt')
        file_number = p.findall(input_file)[0]

        if not os.path.isdir('./output_lexical'):
            os.mkdir('./output_lexical')

        with open((inputs_diretory+"/"+input_file), "r") as input_file_stream, open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
            for line in input_file_stream:
                count_line+=1
                acumulated_tokens = []
                erros = []
                identify_token(line, count_line, acumulated_tokens)
                for token in acumulated_tokens:
                    output_file_stream.write(token)
                # for token in erros:
                #     output_file_stream.write(token)

            if is_block_comment:
                is_block_comment = False
                hasError = True
                output_file_stream.write(comentario_error)
            if not hasError:
                print("arquivo " + input_file + " Sucesso!")
            hasError = False


def identify_token(word, line_number, acumulated):
    global is_block_comment
    global comentario_error
    # checar comentarios
    if is_block_comment or start_comentario_de_bloco_regex.search(word) != None:
        is_block_comment = True
        if start_comentario_de_bloco_regex.search(word) != None:
            regexMatch = list(filter(lambda x: x != "" and x != " ", start_comentario_de_bloco_regex.split(word)))
            comentario_error = formatter_token(line_number, "CONF", regexMatch[0])
        if end_comentario_de_bloco_regex.search(word) != None:
            is_block_comment = False
            regexMatch = list(filter(lambda x: x != "" and x != " ", end_comentario_de_bloco_regex.split(word)))
            if len(regexMatch) >= 1:
                return identify_token("".join(regexMatch), line_number, acumulated)
        return
    if comentario_de_linha_regex.search(word) != None:
        return
    # final de checar comentarios
    if word[0] == " " or word[0] == "\n" or word[0] == "\t":
        if len(word) > 1:
            return identify_token(word[1:], line_number, acumulated)
        else:
            return
    if palavraReservadaRegex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", palavraReservadaRegex.split(word)))
        acumulated.append(formatter_token(line_number, "PRE", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
    elif itentificador_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", itentificador_regex.split(word)))
        acumulated.append(formatter_token(line_number, "IDE", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
    elif cadeia_de_caracter_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", cadeia_de_caracter_regex.split(word)))
        acumulated.append(formatter_token(line_number, "CAD", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
        return identify_token("".join(regexMatch[1:]), line_number, acumulated)
    elif numero_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", numero_regex.split(word)))
        acumulated.append(formatter_token(line_number, "NRO", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
    elif operadores_aritmeticos_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", operadores_aritmeticos_regex.split(word)))
        acumulated.append(formatter_token(line_number, "ART", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
    elif operadores_relacionais_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", operadores_relacionais_regex.split(word)))
        acumulated.append(formatter_token(line_number, "REL", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
    elif operadores_logicos_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", operadores_logicos_regex.split(word)))
        acumulated.append(formatter_token(line_number, "LOG", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
    elif demilitadores_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", demilitadores_regex.split(word)))
        acumulated.append(formatter_token(line_number, "DEL", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
    checkErrors(word, line_number, acumulated)

def checkErrors(word, line_number, acumulated):
    global erros
    global hasError
    hasError = True

    if cadeira_de_caracter_erro_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", cadeira_de_caracter_erro_regex.split(word)))
        acumulated.append(formatter_token(line_number, "CMF", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
    elif simbolo_erro_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", simbolo_erro_regex.split(word)))
        acumulated.append(formatter_token(line_number, "SIB", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)

def formatter_token(line, token_type, token):
    return str(line) + " " + token_type + " " + token + "\n"

if __name__ == "__main__":
    main()