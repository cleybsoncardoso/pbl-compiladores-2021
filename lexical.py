import sys
import os
import re

def main():
    inputs_diretory = "./input"
    output_diretory = "./output"
    for input_file in os.listdir(inputs_diretory):
        print(input_file)
        p = re.compile('entrada(\d+).txt')
        file_number = p.findall(input_file)[0]

        if not os.path.isdir('./output'):
            os.mkdir('./output')

        with open((inputs_diretory+"/"+input_file), "r") as input_file_stream, open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
            for line in input_file_stream:
                output_file_stream.write(formatter_token(1, "PRE", line))

def formatter_token(line, token_type, token):
    return str(line) + " " + token_type + " " + token + "\n"

if __name__ == "__main__":
    main()