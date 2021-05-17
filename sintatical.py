# Cleybson Cardoso Leite e José Ricardo Nogueira Magalhães
import sys
import os
import re

separeteTokens = re.compile("(\d*) (\w*) (.*)")
declarationsType = ["real", "boolean", "int", "string"]

tokens = []
errors = []
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

    if len(errors) > 0:
      with open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
        for error in errors:
          output_file_stream.write(error)
    else:
      with open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
        output_file_stream.write("Sucesso")


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


def global_declarations():
  if currentToken != None:
    if currentToken["type"] == "PRE":
      if currentToken["value"] == "const":
        declaration_const()
      elif currentToken["value"] == "var":
        prox_token()
        declaration_var()
      elif currentToken["value"] == "struct":
        declaration_struct()
      else:
        prox_token()
    else:
      prox_token()
    global_declarations()



################# const ##############################

def declaration_const():
  if prox_token()["value"] == "{":
    prox_token()
    if currentToken["value"] != "}":
      if atribuition_const():
        print("declarou Constante")
      else:
        print("erro: Declarar Constante")
  if currentToken["value"] == "}":
    prox_token()

def atribuition_const():
  if currentToken["value"] == "}":
    return True
  if currentToken["value"] in declarationsType:
    prox_token()
    if atribuition_value():
      atribuition_const()
    if currentToken["value"] == ";":
      prox_token()
      atribuition_const()
      return True
  return False


def atribuition_value():
  if currentToken["type"] == "IDE":
      prox_token()
      if currentToken["value"] == "=":
        prox_token()
        if checkValues():
          prox_token()
          if currentToken["value"] == ",":
            prox_token()
            atribuition_value()
          elif currentToken["value"] == ";":
            return True
          return False
      if currentToken["value"] == ",":
        prox_token()
        atribuition_value()
  startErrorState("erro ao declarar constante na linha " + currentToken["line"] +"\n")
  return False


################# var ##############################

def declaration_var():
  if currentToken["value"] == "{":
    prox_token()
    if currentToken["value"] != "}":
      if atribuition_var():
        print("declarou Variavel")
      else:
        print("erro: Declarar Variavel " + currentToken["value"] + " linha:" + currentToken["line"])
  if currentToken["value"] == "}":
    prox_token()

def atribuition_var():
  if currentToken["value"] == "}":
    return True
  if currentToken["value"] in declarationsType:
    prox_token()
    if atribuition_value_optional():
      atribuition_var()
      return True
  return False

def atribuition_value_optional():
  if currentToken["type"] == "IDE":
      prox_token()
      if currentToken["value"] == "=":
        prox_token()
        if checkValues():
          prox_token()
          if currentToken["value"] == ",":
            prox_token()
            if atribuition_value_optional():
              return True
          elif currentToken["value"] == ";":
            prox_token()
            return True
      elif currentToken["value"] == ",":
        prox_token()
        if atribuition_value_optional():
          return True
      elif currentToken["value"] == ";":
        prox_token()
        return True
  elif currentToken["value"] == ";":
    prox_token()
    return True
  startErrorState("erro ao declarar variavel na linha " + currentToken["line"] +"\n")
  return False



#################### struct detection ################################################

def declaration_struct():
  if prox_token()["type"] == "IDE":
    prox_token()
    if currentToken["value"] == "extends":
      prox_token()
      if currentToken["type"] == "IDE":
        prox_token()
      else:
        startErrorState("erro ao declarar struct na linha " + currentToken["line"] +"\n")
    declaration_var()


#################### General Functions ###################################################

def errorState():
  finalDelimitate = [";", "}"]
  if currentToken["value"] not in finalDelimitate:
    prox_token()

def startErrorState(messageError):
  global errors
  errors.append(messageError)
  errorState()

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
