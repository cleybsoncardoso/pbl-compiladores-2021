# Cleybson Cardoso Leite e José Ricardo Nogueira Magalhães
import sys
import os
import re

separeteTokens = re.compile("(\d*) (\w*) (.*)")
declarationsType = ["real", "boolean", "int", "string"]

tokens = []
currentToken = None

def main():
  inputs_diretory = "./output_lexical"
  output_diretory = "./output"

  for input_file in os.listdir(inputs_diretory):
  # for input_file in ['entrada2.txt']:
    count_line = 0
    p = re.compile('saida(\d+).txt')
    file_number = p.findall(input_file)[0]

    if not os.path.isdir('./output'):
      os.mkdir('./output')

    with open((inputs_diretory+"/"+input_file), "r") as input_file_stream:
      convert_tokens(input_file_stream)
    analise()

def convert_tokens(fileTokens):
  global tokens

  for line in fileTokens:
    token = separeteTokens.split(line[:-1])
    tokens.append({ "line": token[1], "type": token[2], "value": token[3] })

def prox_token():
  global tokens
  global currentToken
  if len(tokens) > 0:
    currentToken = tokens.pop(0)
  else:
    currentToken = None
  return currentToken

def analise():
  # start analise
  prox_token()
  if(currentToken != None):
    global_declarations()
    analise()


def global_declarations():
  if currentToken["type"] == "PRE":
    if currentToken["value"] == "const":
      declaration_const()



def declaration_const():
    if prox_token()["value"] == "{":
      prox_token()
      if currentToken["value"] != "}":
          if atribuition_const():
            print(currentToken)

def atribuition_const():
  if currentToken["value"] == "}":
    return True
  if currentToken["value"] in declarationsType:
    prox_token()
    if currentToken["type"] == "IDE":
      prox_token()
      if currentToken["value"] == "=":
        prox_token()
      if checkValues():
        prox_token()
      if currentToken["value"] == ",":
        prox_token()
        atribuition_const()
      if currentToken["value"] == ";":
        prox_token()
        atribuition_const()
  print(currentToken)
  return False


def checkValues():
  possibleValue = ["false", "true"]
  possibleType = ["NRO", "CAD"]
  if currentToken["value"] in possibleValue or currentToken["type"] in possibleType:
    return True
  return False

def declaration_variable():
  if currentToken["value"] != "}":
    if currentToken["value"] in declarationsType:
      prox_token()
      if currentToken["type"] == "IDE":
        prox_token()








if __name__ == "__main__":
  main()
