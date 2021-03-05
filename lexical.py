import sys
import os
import re

palavraReservadaRegex = re.compile("^(var|const|typedef|struct|extends|procedure|function|start|return|if|else|then|while|read|print|int|real|boolean|string|true|false|global|local)( |\n)")
comentario_de_linha_regex = re.compile("^//.*")
start_comentario_de_bloco_regex = re.compile("^/\*")
end_comentario_de_bloco_regex = re.compile(".*\*/")
itentificador_regex = re.compile("^([A-Za-z][\w|\d]*)")
start_cadeia_de_caracter_regex = re.compile("^(\")")
# TODO: Precisa ver a questão de caracter duplo usando \"
inside_cadeia_de_caracter_regex = re.compile("([A-Za-z|\w|\x20-\x21|\x23-\x7E]*)")
end_cadeia_de_caracter_regex = re.compile("^(\")")

# variaveis de controle
is_block_comment = False
is_block_catacteres = False
caracteres_acumulated = ""

# variaveis globais
erros = []


def main():
    inputs_diretory = "./input"
    output_diretory = "./output"

    # for input_file in os.listdir(inputs_diretory):
    for input_file in ['entrada1.txt']: 
        count_line = 0
        p = re.compile('entrada(\d+).txt')
        file_number = p.findall(input_file)[0]

        if not os.path.isdir('./output'):
            os.mkdir('./output')

        with open((inputs_diretory+"/"+input_file), "r") as input_file_stream, open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
            for line in input_file_stream:
                count_line+=1
                acumulated_tokens = []
                identify_token(line, count_line, acumulated_tokens)
                for token in acumulated_tokens:
                    output_file_stream.write(token)

def identify_token(word, line_number, acumulated):
    global is_block_comment
    global is_block_catacteres
    global caracteres_acumulated

    # checar comentarios
    if is_block_comment or start_comentario_de_bloco_regex.search(word) != None:
        is_block_comment = True
        if end_comentario_de_bloco_regex.search(word) != None:
            is_block_comment = False
            regexMatch = list(filter(lambda x: x != "" and x != " ", end_comentario_de_bloco_regex.split(word)))
            if len(regexMatch) >= 1:
                return identify_token("".join(regexMatch), line_number, acumulated)
        return
    if comentario_de_linha_regex.search(word) != None:
        return
    # final de checar comentarios

    # checar caracteres
    if is_block_catacteres:
        if end_cadeia_de_caracter_regex.search(word[0]):
            acumulated.append(formatter_token(line_number, "CDC", caracteres_acumulated))
            is_block_catacteres = False
            return identify_token(word[1:], line_number, acumulated)
        if inside_cadeia_de_caracter_regex.search(word):
            regexMatch = list(filter(lambda x: x != "", inside_cadeia_de_caracter_regex.split(word)))
            caracteres_acumulated += regexMatch[0]
            if len(regexMatch) > 1:
                return identify_token("".join(regexMatch[1:]), line_number, acumulated)
            else:
                return

    if word[0] == " ":
        return identify_token(word[1:], line_number, acumulated)
    if palavraReservadaRegex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", palavraReservadaRegex.split(word)))
        if len(regexMatch) > 1:
            acumulated.append(formatter_token(line_number, "PRE", regexMatch[0]))
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
    elif itentificador_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", itentificador_regex.split(word)))
        if len(regexMatch) > 1:
            acumulated.append(formatter_token(line_number, "IDE", regexMatch[0]))
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
    elif start_cadeia_de_caracter_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", start_cadeia_de_caracter_regex.split(word)))
        is_block_catacteres = True
        caracteres_acumulated = ""
        return identify_token("".join(regexMatch[1:]), line_number, acumulated)

def formatter_token(line, token_type, token):
    return str(line) + " " + token_type + " " + token + "\n"

if __name__ == "__main__":
    main()