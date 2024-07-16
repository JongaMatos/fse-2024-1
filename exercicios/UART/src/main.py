import os
from time import sleep
from utils import cria_buffer, decodifica_leitura, code_options ,operation_codes, menu,conecta

def main():
    
    uarto_filestream=conecta()
    
    codigo,valor = menu()
    
    
    # codigo = operation_codes[code_options[5]]
    # print(f"codigo: {codigo}")
    # valor = '31'
    matricula = [ 2, 2, 3, 8]
    
    buffer = cria_buffer(codigo, matricula, valor)

    os.write(uarto_filestream, buffer)
        
    sleep(1)

    leitura = os.read(uarto_filestream, 255)
    
    decodifica_leitura(codigo,leitura)


    os.close(uarto_filestream)


if(__name__=="__main__"):
    main()
