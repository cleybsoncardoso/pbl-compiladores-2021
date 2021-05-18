# Cleybson Cardoso Leite e José Ricardo Nogueira Magalhães
import sys
import os
import re

separeteTokens = re.compile("(\d*) (\w*) (.*)")

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
      elif currentToken["value"] == "procedure":
        prox_token()
        declaration_procedure()
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
  if check_declaration_type():
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
      if declaration_vector():
        if declaration_vector():
          matrix_assign()
        else:
          vector_assign()
        if currentToken["value"] == ",":
          prox_token()
          atribuition_value()
        elif currentToken["value"] == ";":
          return True
      elif currentToken["value"] == "=":
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
      atribuition_var()
    # if currentToken["value"] != "}":
    #   if atribuition_var():
    #     print("declarou Variavel")
    #   else:
    #     print("erro: Declarar Variavel " + currentToken["value"] + " linha:" + currentToken["line"])
  if currentToken["value"] == "}":
    prox_token()

def atribuition_var():
  if currentToken["value"] == "}":
    return True
  if check_declaration_type():
    prox_token()
    if atribuition_value_optional():
      atribuition_var()
      return True
  return False

def atribuition_value_optional():
  if currentToken["type"] == "IDE":
      prox_token()
      if declaration_vector():
        if declaration_vector():
          matrix_assign()
        else:
          vector_assign()
        if currentToken["value"] == ",":
          prox_token()
          atribuition_value_optional()
        elif currentToken["value"] == ";":
          return True
      elif currentToken["value"] == "=":
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


#################### procedure #######################################################

def declaration_procedure():
  if currentToken["type"] == "IDE":
    prox_token()
    if currentToken["value"] == "(":
      prox_token()
      if declaration_params():
        prox_token()
        if currentToken["value"] == "{":
          prox_token()
          declaration_bodyFunction(False)


def declaration_bodyFunction(can_return):
  if currentToken["value"] == "var":
    prox_token()
    declaration_var()
  else:
    assign()
  if not can_return:
    if currentToken["value"] != "}":
      declaration_bodyFunction(can_return)
  else:
    if currentToken["value"] != "}" or currentToken["value"] != "return":
      declaration_bodyFunction(can_return)
    print(currentToken)

def global_local():
  if currentToken["type"] == "PRE":
    if currentToken["value"] == "global" or currentToken["value"] == "local":
      prox_token()
      if currentToken["value"] == ".":
        prox_token()
      else:
        return False
  return True

def expression():
  if global_local():
    term()
    add_expression()

def term():
  expression_value()
  multi_expression()

def expression_value():
  if currentToken["value"] == "-":
    prox_token()
    return expression_value()
  elif currentToken["type"] in ["IDE", "NRO", "CAD"] or currentToken["value"] in ["false", "true"]:
    prox_token()
    return True
  elif currentToken["value"] == "(":
    prox_token()
    if expression():
      if currentToken["value"] == ")":
        prox_token()
        return True
      else:
        startErrorState("erro ao declarar expressao na linha " + currentToken["line"] +"\n")
        return False
    else:
      startErrorState("erro ao declarar expressao na linha " + currentToken["line"] +"\n")
      return False
  elif function_call():
    return True
  else:
    return False

def function_call():
  if currentToken["type"] == "IDE":
    prox_token()
    if currentToken["value"] == "(":
      argument_list()
      if(currentToken["value"] == ")"):
        prox_token()
        return True
      else:
        startErrorState("erro ao declarar chamada de função na linha " + currentToken["line"] +"\n")
        return False
    else:
      startErrorState("erro ao declarar chamada de função na linha " + currentToken["line"] +"\n")
      return False
  else:
    startErrorState("erro ao declarar chamada de função na linha " + currentToken["line"] +"\n")
    return False

def argument_list():
  if currentToken["type"] == "IDE":
    if(expression()):
      if currentToken["value"] == ",":
        prox_token()
        return argument_list()
  prox_token()
  return True

def multi_expression():
  if currentToken["value"] == "*" or currentToken["value"] == "/":
    return term()
  else:
    return True

def add_expression():
  if currentToken["value"] == "+" or currentToken["value"] == "-":
    return expression()
  else:
    return True

def assign():
  if not global_local():
    return False

  if currentToken["type"] == "IDE":
    prox_token()
    if currentToken["value"] == "=":
      prox_token()
      expression()
    if declaration_vector():
      if declaration_vector():
        matrix_assign()
      else:
        vector_assign()

  if currentToken["value"] == ";":
    prox_token()
  else:
    startErrorState("erro em atribuicao na linha " + currentToken["line"] +"\n")
    return False

#################### vector matrix ###################################################

def matrix_assign():
  if currentToken["value"] == "=":
    prox_token()
    if currentToken["type"] in ["IDE", "NRO", "CAD"] or currentToken["value"] in ["false", "true"]:
      prox_token()
      return True
    else:
      startErrorState("erro em atribuicao de matrix na linha " + currentToken["line"] +"\n")
      return False
  elif currentToken["value"] == ";":
    return True
  else:
    startErrorState("erro em atribuicao de matrix na linha " + currentToken["line"] +"\n")
    return False


def vector_assign():
  if currentToken["value"] == "=":
    prox_token()
    if currentToken["type"] in ["IDE", "NRO", "CAD"] or currentToken["value"] in ["false", "true"]:
      prox_token()
      return True
    elif currentToken["value"] == "{":
      prox_token()
      if vector_assign_aux():
        if currentToken["value"] == "}":
          prox_token()
        else:
          startErrorState("erro em atribuicao de vetor na linha " + currentToken["line"] +"\n")
          return False
      else:
        startErrorState("erro em atribuicao de vetor na linha " + currentToken["line"] +"\n")
        return False
    else:
      startErrorState("erro em atribuicao de vetor na linha " + currentToken["line"] +"\n")
      return False
  elif currentToken["value"] == ";":
    return True
  else:
    startErrorState("erro em atribuicao de vetor na linha " + currentToken["line"] +"\n")
    return False

def vector_assign_aux():
  if currentToken["type"] in ["IDE", "NRO", "CAD"] or currentToken["value"] in ["false", "true"]:
    prox_token()
    if currentToken["value"] == ",":
      prox_token()
      return vector_assign_aux()
    else:
      return True
  return False

def declaration_vector():
  if currentToken["value"] == "[":
    prox_token()
    if currentToken["type"] in ["IDE", "NRO"]:
      prox_token()
      if currentToken["value"] == "]":
        prox_token()
        return True
      else:
        startErrorState("erro ao declarar vector na linha " + currentToken["line"] +"\n")
        return False
    else:
      startErrorState("erro ao acessar vector na linha " + currentToken["line"] +"\n")
      return False
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

def check_declaration_type():
  declarationsType = ["real", "boolean", "int", "string"]
  if currentToken["value"] in declarationsType or currentToken["type"] == "IDE":
    return True
  elif currentToken["value"] == "struct":
    prox_token()
    if currentToken["type"] == "IDE":
      prox_token()
      return True
  return False

def declaration_params():
  if currentToken["value"] == ")":
    return True
  if currentToken["value"] == "const":
    prox_token()
  if check_declaration_type():
    prox_token()
    if currentToken["type"] == "IDE":
      prox_token()
      if currentToken["value"] == ",":
        prox_token()
      return declaration_params()
    startErrorState("erro ao declarar paramentos em função/procedure na linha " + currentToken["line"] +"\n")
    return False
  startErrorState("erro ao declarar paramentos em função/procedure na linha " + currentToken["line"] +"\n")
  return False

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
    if check_declaration_type():
      prox_token()
      if currentToken["type"] == "IDE":
        prox_token()








if __name__ == "__main__":
  main()
