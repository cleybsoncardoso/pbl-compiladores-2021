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
operadores_logicos_regex = re.compile("^(&&|\|\||!(?!=))")
demilitadores_regex = re.compile("^([;|,|(|)|{|}|\[|\]|\.])")
cadeia_de_caracter_regex = re.compile("^(\"[A-Za-z|\w|\x20-\x21|\x23-\x7E]*\")")

# variaveis de controle
is_block_comment = False
comentario_error = False
hasError = False

# variaveis globais
errosLexicos = []

simbolo_erro_regex = re.compile("^([\x20-\x21|\x23-\x7E]{1})")
cadeira_de_caracter_erro_regex = re.compile("^(\"[A-Za-z|\w|\x20-\x21|\x23-\x7E]*)")


separeteTokens = re.compile("(\d*) (\w*) (.*)")

tokens = []
errors = []
currentToken = None
calledStart = False


# variable to semantical
indexabel_table = {
  "global": {},
  "start": {}
}
current_scope = "global"
semantical_errors = []
desconsidere_scope = False
is_global = False



####################################################################################################
####################################################################################################
#################################start lexical######################################################
####################################################################################################
####################################################################################################

def lexical(input_file):
  global errosLexicos
  global comentario_error
  global is_block_comment
  global hasError
  output_diretory = "./output_lexical"
  count_line = 0
  inputs_diretory = "./input"
  p = re.compile('entrada(\d+).txt')
  file_number = p.findall(input_file)[0]

  if not os.path.isdir('./output_lexical'):
      os.mkdir('./output_lexical')

  with open((inputs_diretory+"/"+input_file), "r") as input_file_stream, open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
      for line in input_file_stream:
        count_line+=1
        acumulated_tokens = []
        errosLexicos = []
        identify_token(line, count_line, acumulated_tokens)
        for token in acumulated_tokens:
            output_file_stream.write(token)
        # for token in errosLexicos:
        #     output_file_stream.write(token)

      if is_block_comment:
        is_block_comment = False
        hasError = True
        output_file_stream.write(comentario_error)
      if not hasError:
        print("arquivo " + input_file + " Sucesso!")
  return "saida"+file_number+".txt"

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
    elif operadores_logicos_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", operadores_logicos_regex.split(word)))
        acumulated.append(formatter_token(line_number, "LOG", regexMatch[0]))
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
    elif demilitadores_regex.search(word) != None:
        regexMatch = list(filter(lambda x: x != "" and x != " ", demilitadores_regex.split(word)))
        acumulated.append(formatter_token(line_number, "DEL", regexMatch[0]))
        if len(regexMatch) > 1:
            return identify_token("".join(regexMatch[1:]), line_number, acumulated)
        else:
            return
    checkErrors(word, line_number, acumulated)

def checkErrors(word, line_number, acumulated):
    global errosLexicos
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

#############################################################################################
#############################################################################################
##############################end lexical####################################################
#############################################################################################
#############################################################################################

#############################################################################################
#############################################################################################
##############################Start sintatical###############################################
#############################################################################################
#############################################################################################

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

def analise_sintatical():
  # start analise_sintatical
  prox_token()
  if(currentToken != None):
    global_declarations()


def global_declarations():
  global current_scope
  global desconsidere_scope
  current_scope = "global"
  desconsidere_scope = False

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
      elif currentToken["value"] == "function":
        prox_token()
        declaration_function()
      elif currentToken["value"] == "start":
        prox_token()
        declaration_start()
      else:
        prox_token()
    else:
      prox_token()
    global_declarations()


################ start ##############################
def declaration_start():
  global calledStart
  global current_scope

  current_scope = "start"

  if calledStart:
    startErrorState("exist 2 start function, line: " + currentToken["line"] +"\n")
  else:
    calledStart = True
    if currentToken["value"] == "(":
      prox_token()
      if currentToken["value"] == ")":
        prox_token()
        if currentToken["value"] == "{":
          prox_token()
          declaration_bodyFunction(False)
        else:
          startErrorState("error on start function, line: " + currentToken["line"] +"\n")
      else:
        startErrorState("error on start function, line: " + currentToken["line"] +"\n")
    else:
      startErrorState("error on start function, line: " + currentToken["line"] +"\n")

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
    type = currentToken["value"]
    prox_token()
    if atribuition_value(type):
      atribuition_const()
    if currentToken["value"] == ";":
      prox_token()
      atribuition_const()
      return True
  return False


def atribuition_value(type):
  global indexabel_table
  global semantical_errors

  if currentToken["type"] == "IDE":
    hasError = False
    if not desconsidere_scope:
      if currentToken["value"] in indexabel_table[current_scope]:
        semantical_errors.append("Erro na linha " + currentToken["line"] + ", constante '" + currentToken["value"] + "' ja foi declarada\n")
        hasError = True
      else:
        indexabel_table[current_scope][currentToken["value"]] = {
          "type": type
        }
    else:
      hasError = True
    prox_token()
    if declaration_vector():
      if declaration_vector():
        matrix_assign()
      else:
        vector_assign()
      if currentToken["value"] == ",":
        prox_token()
        atribuition_value(type)
      elif currentToken["value"] == ";":
        return True
    elif currentToken["value"] == "=":
      prox_token()
      if checkValues(type, hasError):
        prox_token()
        if currentToken["value"] == ",":
          prox_token()
          atribuition_value(type)
        elif currentToken["value"] == ";":
          return True
        return False
    if currentToken["value"] == ",":
      prox_token()
      atribuition_value(type)
  startErrorState("erro ao declarar constante na linha " + currentToken["line"] +"\n")
  return False


################# var ##############################

def declaration_var():
  if currentToken["value"] == "{":
    prox_token()
    if currentToken["value"] != "}":
      atribuition_var()
  if currentToken["value"] == "}":
    prox_token()

def atribuition_var():

  if currentToken["value"] == "}":
    return True
  if check_declaration_type():
    type = currentToken["value"]
    prox_token()
    if atribuition_value_optional(type):
      atribuition_var()
      return True
  return False

def atribuition_value_optional(type):
  global indexabel_table
  global semantical_errors

  if currentToken["type"] == "IDE":
    hasError = False
    if not desconsidere_scope:
      if currentToken["value"] in indexabel_table[current_scope]:
        semantical_errors.append("Erro na linha " + currentToken["line"] + ", variavel '" + currentToken["value"] + "' ja foi declarada\n")
        hasError = True
      else:
        indexabel_table[current_scope][currentToken["value"]] = {
          "type": type
        }
    else:
      hasError = True
    prox_token()
    if declaration_vector():
      if declaration_vector():
        matrix_assign()
      else:
        vector_assign()
      if currentToken["value"] == ",":
        prox_token()
        atribuition_value_optional(type)
      elif currentToken["value"] == ";":
        return True
    elif currentToken["value"] == "=":
      prox_token()
      if checkValues(type, hasError):
        prox_token()
        if currentToken["value"] == ",":
          prox_token()
          if atribuition_value_optional(type):
            return True
        elif currentToken["value"] == ";":
          prox_token()
          return True
    elif currentToken["value"] == ",":
      prox_token()
      if atribuition_value_optional(type):
        return True
    elif currentToken["value"] == ";":
      prox_token()
      return True
  elif currentToken["value"] == ";":
    prox_token()
    return True
  startErrorState("erro ao declarar variavel na linha " + currentToken["line"] +"\n")
  return False


#################### functions #######################################################
def declaration_function():
  global indexabel_table
  global semantical_errors
  global desconsidere_scope

  return_type = currentToken["value"]

  if check_declaration_type():
    prox_token()
  elif currentToken["value"] == "void":
    prox_token()

  if currentToken["type"] == "IDE":
    function_name = currentToken["value"]
    prox_token()
    if currentToken["value"] == "(":
      prox_token()
      if declaration_params(function_name, return_type, [], {}):
        prox_token()
        if currentToken["value"] == "{":
          prox_token()
          declaration_bodyFunction(True)

#################### procedure #######################################################

def declaration_procedure():
  global indexabel_table
  global semantical_errors
  global desconsidere_scope

  if currentToken["type"] == "IDE":
    function_name = currentToken["value"]

    prox_token()
    if currentToken["value"] == "(":
      prox_token()
      if declaration_params(function_name, None, [], {}):
        prox_token()
        if currentToken["value"] == "{":
          prox_token()
          declaration_bodyFunction(False)


def declaration_bodyFunction(can_return):
  if currentToken["value"] == "var":
    prox_token()
    declaration_var()
  elif currentToken["value"] == "if":
    declaration_if(can_return)
  elif currentToken["value"] == "while":
    declaration_while(can_return)
  elif currentToken["value"] == "print":
    declaration_print()
  elif currentToken["value"] == "read":
    declaration_read()
  else:
    assign()
  if not can_return:
    if currentToken["value"] != "}":
      declaration_bodyFunction(can_return)
  else:
    if currentToken["value"] != "}" and currentToken["value"] != "return":
      declaration_bodyFunction(can_return)
    elif currentToken["value"] == "return":
      prox_token()
      return_state()

def return_state():
  if currentToken["value"] == ";":
    prox_token()
    return True
  expression()
  if declaration_vector():
    if declaration_vector():
      matrix_assign()
    else:
      vector_assign()

  if currentToken["value"] == "(":
    prox_token()
    argument_list()
    if(currentToken["value"] == ")"):
      prox_token()
      return True
    else:
      startErrorState("erro ao declarar chamada de função na linha " + currentToken["line"] +"\n")
      return False

def global_local():
  global is_global

  if currentToken["type"] == "PRE":
    if currentToken["value"] == "global" or currentToken["value"] == "local":
      is_global = currentToken["value"] == "global"
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
  elif currentToken["type"] == "IDE":
    prox_token()
    if currentToken["value"] == ".":
      prox_token()
      if currentToken["type"] == "IDE":
        prox_token()
      else:
        startErrorState("erro ao acessar struct na expressao da linha " + currentToken["line"] +"\n")
        return False
    elif currentToken["value"] == "(":
      prox_token()
      argument_list()
      if(currentToken["value"] == ")"):
        prox_token()
        return True
      else:
        startErrorState("erro ao declarar chamada de função na linha " + currentToken["line"] +"\n")
        return False
    return True
  elif currentToken["type"] in ["NRO", "CAD"] or currentToken["value"] in ["false", "true"]:
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
      prox_token()
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
  expression()
  if currentToken["value"] == ",":
    prox_token()
    return argument_list()
  return True

def multi_expression():
  if currentToken["value"] == "*" or currentToken["value"] == "/":
    prox_token()
    return term()
  else:
    return True

def add_expression():
  if currentToken["value"] == "+" or currentToken["value"] == "-":
    prox_token()
    return expression()
  else:
    return True

def assign():
  global is_global
  global semantical_errors

  is_global = False
  if not global_local():
    return False

  if currentToken["type"] == "IDE":
    old_token = currentToken["value"]
    prox_token()
    variable_type = None
    if currentToken["value"] != "(":
      if old_token in indexabel_table["global" if is_global == True else current_scope]:
        variable_type = indexabel_table["global" if is_global == True else current_scope][old_token]["type"]
      else:
        semantical_errors.append("Erro na linha " + currentToken["line"] + ", a variavel '" + old_token + "' nao foi declarada\n")

    if currentToken["value"] == ".":
      prox_token()
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

    if currentToken["value"] == "(":
      prox_token()
      argument_list()
      if(currentToken["value"] == ")"):
        prox_token()
        return True
      else:
        startErrorState("erro ao declarar chamada de função na linha " + currentToken["line"] +"\n")
        return False

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
  global indexabel_table
  global semantical_errors
  global current_scope
  global desconsidere_scope

  if prox_token()["type"] == "IDE":
    if currentToken["value"] in indexabel_table:
      semantical_errors.append("Erro na linha " + currentToken["line"] + ", struct '" + currentToken["value"] + "' ja foi declarada\n")
      desconsidere_scope = True
    else:
      indexabel_table[currentToken["value"]] = {}
      current_scope = currentToken["value"]
    prox_token()
    if currentToken["value"] == "extends":
      prox_token()
      if currentToken["type"] == "IDE":
        prox_token()
      else:
        startErrorState("erro ao declarar struct na linha " + currentToken["line"] +"\n")
    declaration_var()



#################### conditional #########################################################
def declaration_if(can_return):
  if currentToken["value"] == "if":
    prox_token()
    if currentToken["value"] == "(":
      prox_token()
      declaration_conditional_expression()
      if(currentToken["value"] == ")"):
        prox_token()
        if declaration_then(can_return):
          if currentToken["value"] == "else":
            prox_token()
            declaration_then_body(can_return)
          return True
        else:
          return False
      else:
        startErrorState("erro ao declarar 'if' na linha " + currentToken["line"] +"\n")
        return False
    else:
      startErrorState("erro ao declarar 'if' na linha " + currentToken["line"] +"\n")
      return False

def declaration_conditional_expression():
  if currentToken["value"] == "!":
    if not global_local():
      return False
    prox_token()
    if currentToken["type"] == "IDE":
      prox_token()
      if declaration_vector():
        declaration_vector()
  elif isAtribuivel():
    expression()
    if currentToken["type"] == "REL":
      prox_token()
      expression()
  if currentToken["type"] == "LOG":
    prox_token()
    return declaration_conditional_expression()
  elif currentToken["value"] == ")":
    return True
  else:
    startErrorState("erro na condicional da linha " + currentToken["line"] +"\n")
    return False

def declaration_then(can_return):
  if currentToken["value"] == "then":
    prox_token()
    return declaration_then_body(can_return)
  else:
    startErrorState("erro na condicional da linha " + currentToken["line"] +"\n")
    return False

def declaration_then_body(can_return):
  if currentToken["value"] == "{":
    prox_token()
    declaration_bodyFunction(can_return)
    if currentToken["value"] == "}":
      prox_token()
      return True
    else:
      startErrorState("erro na condicional da linha " + currentToken["line"] +"\n")
      return False
  else:
    startErrorState("erro na condicional da linha " + currentToken["line"] +"\n")
    return False


#################### while function ##################################################
def declaration_while(can_return):
  if currentToken["value"] == "while":
    prox_token()
    if currentToken["value"] == "(":
      prox_token()
      declaration_conditional_expression()
      if(currentToken["value"] == ")"):
        prox_token()
        if declaration_then_body(can_return):
          return True
        else:
          return False
      else:
        startErrorState("erro ao declarar 'if' na linha " + currentToken["line"] +"\n")
        return False
    else:
      startErrorState("erro ao declarar 'if' na linha " + currentToken["line"] +"\n")
      return False


#################### print function #################################
def declaration_print():
  if currentToken["value"] == "print":
    prox_token()
    if currentToken["value"] == "(":
      prox_token()
      argument_list()
      if currentToken["value"] == ")":
        prox_token()
        if currentToken["value"] == ";":
          prox_token()
          return True
        else:
          startErrorState("erro ao declarar print na linha " + currentToken["line"] +"\n")
          return False
      else:
        startErrorState("erro ao declarar print na linha " + currentToken["line"] +"\n")
        return False
    else:
      startErrorState("erro ao declarar print na linha " + currentToken["line"] +"\n")
      return False

#################### read function ####################################

def declaration_read_body():
  if isAtribuivel():
    prox_token()
    if currentToken["value"] == ",":
      prox_token()
      return declaration_read_body()
    elif currentToken["value"] == ")":
      return True
  return False

def declaration_read():
  if currentToken["value"] == "read":
    prox_token()
    if currentToken["value"] == "(":
      prox_token()
      if not declaration_read_body():
        startErrorState("erro ao declarar read na linha " + currentToken["line"] +"\n")
        return False
      if currentToken["value"] == ")":
        prox_token()
        if currentToken["value"] == ";":
          prox_token()
          return True
        else:
          startErrorState("erro ao declarar read na linha " + currentToken["line"] +"\n")
          return False
      else:
        startErrorState("erro ao declarar read na linha " + currentToken["line"] +"\n")
        return False
    else:
      startErrorState("erro ao declarar read na linha " + currentToken["line"] +"\n")
      return False
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

def declaration_params(function_name, return_type, params_list, obj_params):
  global desconsidere_scope
  global semantical_errors
  global current_scope

  if currentToken["value"] == ")":
    index_value = function_name + ("" if len(params_list) == 0 else "_" + "_".join(params_list))
    current_scope = index_value
    if index_value in indexabel_table:
      semantical_errors.append("Erro na linha " + currentToken["line"] + ", função/procedure '" + function_name + "' ja foi declarada\n")
      desconsidere_scope = True
    else:
      indexabel_table[index_value] = {
        "return": return_type,
        **obj_params
      }
    return True
  if currentToken["value"] == "const":
    prox_token()
  if check_declaration_type():
    params_list.append(currentToken["value"])
    obj_type = currentToken["value"]
    prox_token()
    if currentToken["type"] == "IDE":
      if not desconsidere_scope:
        if currentToken["value"] in obj_params:
          semantical_errors.append("Erro na linha " + currentToken["line"] + ", parametro da função/procedure '" + function_name + "' ja foi declarada\n")
          desconsidere_scope = True
        else:
          obj_params[currentToken["value"]] = {
            "type": obj_type
          }
      prox_token()
      if currentToken["value"] == ",":
        prox_token()
      return declaration_params(function_name, return_type, params_list, obj_params)
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

def checkValues(type, hasError):
  global semantical_errors

  possibleValue = ["false", "true"]
  possibleType = ["NRO", "CAD"]
  if currentToken["value"] in possibleValue or currentToken["type"] in possibleType:
    if not hasError:
      if type == "string" and currentToken["type"] != "CAD":
        semantical_errors.append("Erro na linha " + currentToken["line"] + ", esperava string e encontrou: " + currentToken["value"] + "\n")
      elif type == "boolean" and currentToken["value"] not in possibleValue:
        semantical_errors.append("Erro na linha " + currentToken["line"] + ", esperava boolean e encontrou: " + currentToken["value"] + "\n")
      elif type == "real" and currentToken["type"] != "NRO":
        semantical_errors.append("Erro na linha " + currentToken["line"] + ", esperava real e encontrou: " + currentToken["value"] + "\n")
      elif type == "int" and currentToken["type"] != "NRO" or type == "int" and currentToken["type"] == "NRO" and "." in currentToken["value"]:
        semantical_errors.append("Erro na linha " + currentToken["line"] + ", esperava int e encontrou: " + currentToken["value"] + "\n")

    return True
  return False

def isAtribuivel():
  possibleValue = ["false", "true"]
  possibleType = ["NRO", "CAD", "IDE"]
  if currentToken["value"] in possibleValue or currentToken["type"] in possibleType:
    return True
  return False

def declaration_variable():
  if currentToken["value"] != "}":
    if check_declaration_type():
      prox_token()
      if currentToken["type"] == "IDE":
        prox_token()

#############################################################################################
#############################################################################################
##############################end sintatical#################################################
#############################################################################################
#############################################################################################

def main():
  global hasError
  global tokens
  global errors
  global currentToken
  global calledStart

  inputs_diretory = "./input"
  output_diretory = "./output_lexical"

  for input_file in ["entrada1.txt"]:
    tokens = []
    errors = []
    currentToken = None
    calledStart = False


    lexical_tokens_file = lexical(input_file)
    inputs_diretory = "./output_lexical"
    output_diretory = "./output"
    p = re.compile('saida(\d+).txt')
    file_number = p.findall(lexical_tokens_file)[0]

    if not os.path.isdir('./output'):
      os.mkdir('./output')

    if hasError:
      with open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
        output_file_stream.write("Error on lexical")
        hasError = False
      break
    with open((inputs_diretory+"/"+lexical_tokens_file), "r") as input_file_stream:
      convert_tokens(input_file_stream)
    analise_sintatical()
    analise_semantical(file_number)

    if len(errors) > 0 or not calledStart:
      with open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
        for error in errors:
          output_file_stream.write(error)
        if not calledStart:
          output_file_stream.write("start não foi criado")
    else:
      with open((output_diretory+"/saida"+file_number+".txt"), "w") as output_file_stream:
        output_file_stream.write("Sucesso")

def analise_semantical(file_number):
  output_diretory = "output"
  print(indexabel_table)
  print("---------------------------------------------")
  print(semantical_errors)
  if len(semantical_errors) > 0:
    with open((output_diretory+"/saidasemantical"+file_number+".txt"), "w") as output_file_stream:
      for error in semantical_errors:
        output_file_stream.write(error)
      if not calledStart:
        output_file_stream.write("start não foi criado")
  else:
    with open((output_diretory+"/saidasemantical"+file_number+".txt"), "w") as output_file_stream:
      output_file_stream.write("Sucesso")

#############################################################################################


if __name__ == "__main__":
  main()
