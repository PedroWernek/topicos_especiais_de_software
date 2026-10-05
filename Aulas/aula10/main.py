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

from pathlib import Path

a = Path('dados.txt')
if a.exists():
    print("Existe")
else:
    print("Não existe")

import csv
with open('dados.csv', 'r', encoding='utf-8') as arq:
    leitor = csv.reader(arq, delimiter=',')
    cabecalho = next(leitor)
    print(cabecalho)
    for linha in leitor:
        nome, cargo, salario = linha[1], linha[2], float(linha[4])

        print(f'{nome} atua como {cargo} e tem salario {salario}')

print()
with open('dados.csv', 'r', encoding='utf-8') as arq:
    leitor_dict = csv.DictReader(arq, delimiter=',')
    for registro in leitor_dict:

        print(f"{registro['nome']} atua como {registro['cargo']} e tem salario {registro['salario']}")

print()

f= [[10, 'José da Silva', 'Advogado','Teste', 1000.00]]
with open('dados.csv', 'a', newline='', encoding='utf-8') as arq:
    escritor = csv.writer(arq, delimiter=',')
    escritor.writerows(f)

d = [{'id': 11, 'name': 'João', 'cargo': 'Analista', 'salario': 5000.00}]
cabecalho = list(d[0].keys())
with open('dados.csv', 'a', newline='', encoding='utf-8') as arq:
    escritor = csv.DictWriter(arq,fieldnames=cabecalho, delimiter=',')
    escritor.writerows(d)

import xml.etree.ElementTree as ET

tree = ET.parse('dados_xml.xml')
root = tree.getroot()
print(f'Tag Raiz: {root.tag}')

for elem in root.findall('empresa'):
    id_prod = elem.get('cargo').text
    nome = elem.find('nome').text
    preco = elem.find('salario').text
    print(f'ID:{id_prod}, nome: {nome}, preço:{preco}')

import json
config = {'servidor': 'localhost', 'porta': 8080, 'debug': True}

with open('config.json', 'r', encoding='utf-8') as arq:
    json.dump('config.json', indent=4, ensure_ascii=False)
    dados_carregados = json.load(arq)

    print(dados_carregados['servidor'])

    d = json.