import struct
import termios
import os

code_options=[
    "get_int",
    "get_float",
    "get_string",
    "send_int",
    "send_float", 
    "send_string"
  ]

operation_codes={
    "get_int":0xA1,
    "get_float":0xA2,
    "get_string":0xA3,
    "send_int":0xB1,
    "send_float":0xB2,
    "send_string":0xB3
  }


def cria_buffer(codigo, matricula, data):
  
  def argumento_por_codigo(codigo):
    if(codigo==operation_codes["send_int"]):
      return '<i'
    if(codigo==operation_codes["send_float"]):
      return '<f'
    return ''
  
  tx_buffer = bytearray()
  tx_buffer += bytes([codigo])
  
  if(codigo>=operation_codes["send_int"]):
    if(codigo==operation_codes["send_string"]):
      tx_buffer+= bytes([len(data)]) 
      tx_buffer+= data.encode("utf-8")
    else:
      tx_buffer+= struct.pack(argumento_por_codigo(codigo), data) 
    


  tx_buffer+=bytes(matricula)
    
  return tx_buffer

def decodifica_leitura(codigo, valor_bytes):
  
  if(codigo==operation_codes["get_int"] or codigo==operation_codes["send_int"]):
    
    valor_int = int.from_bytes(valor_bytes, byteorder='little')
    print(f"Valor inteiro recebido: {valor_int}")
    return valor_int
  
  if(codigo==operation_codes["get_float"] or codigo==operation_codes["send_float"]):
    valor_float = struct.unpack('f', valor_bytes)[0]
    print(f"Valor decimal recebido: {valor_float}")
    return valor_float
  
  if(codigo==operation_codes["get_string"] or codigo==operation_codes["send_string"]):
    valor_string=valor_bytes[1:].decode('utf-8')
    print(f"String recebida [{len(valor_string)}]: {valor_string}")
    return valor_string
    

# Menu e leitura de valores de envio

def menu():
  print("Escolha uma das operações abaixo")
  print("  1: Solicitar dado\x1B[3m integer\x1B[0m")
  print("  2: Solicitar dado\x1B[3m float \x1B[0m")
  print("  3: Solicitar dado\x1B[3m string \x1B[0m")
  print("  4: Enviar dado\x1B[3m integer\x1B[0m")
  print("  5: Enviar dado\x1B[3m float \x1B[0m")
  print("  6: Enviar dado\x1B[3m string \x1B[0m")
  
  selecionado = le_opcao()
  opcao=operation_codes[code_options[selecionado]]

  if(selecionado<3):
    return opcao, None
  
  if (opcao==operation_codes['send_int']):
    valor=le_inteiro()
    return opcao, valor
  
  if (opcao==operation_codes['send_float']):
    valor=le_float()
    print(valor)
    return opcao, valor
  
  return opcao, le_string()


def le_opcao():
  try:
      numero = int(input("Escolha uma opção: "))
      if(1<=numero<=6):
        return numero - 1
      print("   Opção invalida")
      return le_opcao() - 1
  except ValueError:
      print("   Opção invalida")
      return le_opcao() - 1
  
def le_inteiro():
  try:
      valor = int(input("Digite uma valor inteiro: ").strip())
      return valor
  except ValueError:
      print("   Valor invalido")
      return le_inteiro()
    
def le_float():
  try:
      valor = float(input("Digite uma valor numerico decimal: ").strip().replace(',', '.'))
      return valor
  except ValueError:
      print("   Valor invalido")
      return le_float()
    
def le_string():
  try:
      valor = input("Digite uma mensagem de texto: ").strip()
      return valor
  except ValueError:
      print("   Valor invalido")
      return le_string()
    
def conecta():
    uarto_filestream = os.open(
        "/dev/ttyS0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)

    [iflag, oflag, cflag, lflag] = [0, 1, 2, 3]

    attrs: termios._Attr = termios.tcgetattr(uarto_filestream)

    attrs[cflag] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD
    attrs[iflag] = termios.IGNPAR
    attrs[oflag] = 0
    attrs[lflag] = 0

    termios.tcflush(uarto_filestream, termios.TCIFLUSH)
    termios.tcsetattr(uarto_filestream, termios.TCSANOW, attrs)
    
    return uarto_filestream