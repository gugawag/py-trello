separador = '='
configuracao = {}

with open('config.properties') as arquivo_config:
    for linha in arquivo_config:
        chave, valor = linha.split(separador)
        configuracao[chave.strip()] = valor.strip()

