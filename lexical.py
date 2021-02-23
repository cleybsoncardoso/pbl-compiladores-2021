import sys
import os
import re

palavraReservadaRegex = re.compile("^(var|const|typedef|struct|extends|procedure|function|start|return|if|else|then|while|read|print|int|real|boolean|string|true|false|global|local) ")

def main():
    inputs_diretory = "./input"
    output_diretory = "./output"

    for input_file in os.listdir(inputs_diretory):
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
    if word[0] == " ":
        return identify_token(word[1:], line_number, acumulated)
    if palavraReservadaRegex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", palavraReservadaRegex.split(word)))
        if len(regexMatch) > 1:
            acumulated.append(formatter_token(line_number, "PRE", regexMatch[0]))
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)

def formatter_token(line, token_type, token):
    return str(line) + " " + token_type + " " + token + "\n"

if __name__ == "__main__":
    main()