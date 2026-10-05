arquivo = open('dados.txt', 'a', encoding='utf-8')
arquivo.write("Novo arquivo de conteúdo\n")
arquivo.close()

arquivo = open("dados.txt", 'r', encoding='utf-8')
conteudo = arquivo.read()
arquivo.close()

print(conteudo)


arquivo = open('dados.txt', 'r', encoding='utf-8')
for linha in arquivo: print(linha.strip())
arquivo.close()

#se garantir que o arquivo fechou
with open('dados.txt', 'r', encoding='utf-8') as arquivo:
    linhas = arquivo.readlines()

print(f'Total de linhas {len(linhas)}')

try:
    with open('dados.txt', 'r', encoding='utf-8') as arq:
        linhas = arq.readlines()
except FileNotFoundError:
    print("Arquivo não encontrado!")
except Exception as e:
    print("Erro inesperado: " + e)
print(f'Total de linhas {len(linhas)}')