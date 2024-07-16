import os
from time import sleep
from utils import cria_buffer, decodifica_leitura, menu, conecta, get_crc


def main():

    uarto_filestream = conecta()
    matricula = [2, 2, 3, 8]

    codigo, valor = menu()
    buffer=cria_buffer(0x01,codigo,matricula,valor)


    valor_crc = get_crc(buffer)
    buffer += valor_crc.to_bytes(2, 'little')

    os.write(uarto_filestream, buffer)
    sleep(1)
    leitura = os.read(uarto_filestream, 255)
    
    decodifica_leitura(codigo, leitura)

    os.close(uarto_filestream)


if (__name__ == "__main__"):
    main()
