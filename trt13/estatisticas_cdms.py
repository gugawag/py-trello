from trello import trelloclient
import plotly.graph_objs as go
import sys
import plotly
import datetime
import os

'''
TRELLO_API_KEY=152afd0574f3735b3925155d04b67223
TRELLO_API_SECRET=b738051312e8b8d79cf7d8f8635e6882c6f42c2e6fab08fb23154d9bfa209e84
TRELLO_TEST_BOARD_COUNT=10
TRELLO_TEST_BOARD_NAME=maratonapje
TRELLO_TOKEN=cc24b6e72362006df2d75a3465f53317f48ea760914e5958173ca389f4b8a346'''

trello = trelloclient.TrelloClient('152afd0574f3735b3925155d04b67223', None, 'cc24b6e72362006df2d75a3465f53317f48ea760914e5958173ca389f4b8a346', None)

"""
brd_maratona = trello.get_board('C13fMWkd')
quant_fechados = len(brd_maratona.get_cards(card_filter='closed'))
quant_abertos = len(brd_maratona.get_cards(card_filter='open'))
lista_quant = [quant_abertos, quant_fechados]

lista_estados = ['Abertos', 'Fechados']
data = [go.Bar(
            x=lista_estados,
            y=lista_quant
    )]


map_listas = dict()

for lista in brd_maratona.all_lists():
    print(lista.name)
    map_listas[lista.name] = len(lista.list_cards())

print("Chaves:", list(map_listas.keys()))
print("Valores:", list(map_listas.values()))
data2 = [go.Bar(
            x=list(map_listas.keys()),
            y=list(map_listas.values())
    )]

# plotly.offline.plot(data, filename='basic-bar.html')
# plotly.offline.plot(data2, filename='basic-bar2.html')


#api_key, api_secret=None, token=None, token_secret=None):

print(len(brd_maratona.get_cards()))
print(brd_maratona.get_cards(card_filter='closed'))
print(len(brd_maratona.all_lists()[1].list_cards()))
"""

#média de tempo em homologação
#"datetime saída de homologação" - "datetime chegada homologação"
brd_manutencao = trello.get_board('ImvgfhEa')
data_entrada = None
data_saida = None
tempos = list()
padrao_entrada = {'entrada':None,'saida':None,'total':0,'quant':0}
tempo_medio_dic = {'Homologando':padrao_entrada,'Fazendo':padrao_entrada, 'Aguardando':padrao_entrada, 'Testando':padrao_entrada, 'Implantando':padrao_entrada}

#porcentagem que passou em cada lista
quant_fechados_manutencao = len(brd_manutencao.get_cards(card_filter='closed'))
lista_cartoes_fechados_manutencao = brd_manutencao.get_cards(card_filter='closed')
print('Quantidade cartões:',quant_fechados_manutencao)

nomes_listas_ordem_cronologica = ['Feito', 'Revisado', 'Testado', 'Homologado', 'Implantado', 'Arquivado']
dict_listas_passadas = {'Feito':0, 'Revisado':0, 'Testado':0, 'Homologado':0, 'Implantado':0}
ano_inicial = 2016

quant_cards = 0
quants_cards_total = 0
"""
for cartao in lista_cartoes_fechados_manutencao:
    quants_cards_total += 1
    if cartao.card_created_date.year < 2016:
        continue
    quant_cards += 1
    for movimento in cartao.list_movements():
        fonte = movimento['destination']
        if fonte['name'] not in dict_listas_passadas.keys():
            continue
        dict_listas_passadas[fonte['name']] += 1
        print(dict_listas_passadas)"""

quants_cards_total_homologando = 0
quant_cards_retornados_homologacao = 0
#taxa de retorno da homologação
"""
for cartao in lista_cartoes_fechados_manutencao:
    if cartao.card_created_date.year < 2016:
        continue
    for movimento in cartao.list_movements():
        fonte = movimento['source']
        destino = movimento['destination']
        if fonte['name']=='Homologando':
            quants_cards_total_homologando += 1
            print('Homologando:',quants_cards_total_homologando)
        else:
            continue
        if fonte['name']=='Homologando' and destino['name'] not in ('Homologado', 'Implantando', 'Implantado'):
            quant_cards_retornados_homologacao += 1
            print('Retornados:',quant_cards_retornados_homologacao)

taxa_retorno_homologacao = quant_cards_retornados_homologacao/quants_cards_total_homologando"""
taxa_retorno_homologacao = 0.28
print('Taxa retorno: ', taxa_retorno_homologacao)

quant_cards = 178
dict_listas_passadas = {'Feito': 95, 'Testado': 97, 'Homologado': 47, 'Implantado': 162, 'Revisado': 98}

print('Quantidade cartões:',quant_fechados_manutencao)
print('Quantidade cartões computados:',quant_cards)
print('Quantidade cartões total:',quants_cards_total)

print(dict_listas_passadas)

aderencia_total = 0
for lista in dict_listas_passadas:
    percentual_lista = dict_listas_passadas[lista]/quant_cards
    aderencia_total += percentual_lista
    print('% passados pela lista', lista, ':', percentual_lista)

percent_aderencia = (aderencia_total/len(dict_listas_passadas.keys()))
print('Aderência total:', percent_aderencia)

dict_listas_passadas['Arquivado'] = quant_cards

valores_percentuais = list()
for lista in nomes_listas_ordem_cronologica:
    valores_percentuais.append(round(dict_listas_passadas[lista]/quant_cards, 2))

agora = datetime.datetime.now()
ano_atual = agora.year
mes_atual = agora.month

layout = go.Layout(
    title='Aderência ao processo | Índice geral: '+str(percent_aderencia)[2:4]+'% | Período: 01/2016 a '+str(mes_atual)+'/'+str(ano_atual),
    xaxis=dict(
        title='Listas CDMS - Manutenção',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='% cartões passaram pela lista',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    barmode='overlay'
)

data_aderencia = go.Bar(
            x=list(nomes_listas_ordem_cronologica),
            y=list(valores_percentuais),
            marker=dict(
            color=['rgb(30,144,255)', 'rgb(0,0,128)',
                   'rgb(60,179,113)', 'rgb(123,104,238)',
                   'rgb(221,160,221)', 'rgb(250,128,114)']),
            name='Taxa de Aderência'
    )

valores_percentuais_retorno = [0, 0, 0, round((0.28/0.26)-1, 2), 0, 0]

data_retorno = go.Bar(
            x=list(nomes_listas_ordem_cronologica),
            y=list(valores_percentuais_retorno),
            marker=dict(color='rgb(255,0,0)'),
            name='Taxa de Retorno'
    )

caminho_arquivo = '/tmp/estatcdms'
caminho_arquivos_passados = '/tmp/estatcdms/arquivos'
data_geral = [data_aderencia, data_retorno]
fig = go.Figure(data=data_geral, layout=layout)
plotly.offline.plot(fig, filename='/tmp/aderencia')
#plotly.offline.plot(data_aderencia, filename='aderencia.html')

sys.exit()

#tempo médio pos lista
for lista in brd_manutencao.all_lists():
    for cartao in lista.list_cards():
        for movimento in cartao.list_movements():
            data_movimento = movimento['datetime']
            fonte = movimento['source']
            print(fonte['name'])
            if fonte['name'] not in tempo_medio_dic.keys():
                tempo_medio_dic[fonte['name']] = padrao_entrada
            destino = movimento['destination']
            if destino['name'] not in tempo_medio_dic.keys():
                tempo_medio_dic[destino['name']] = padrao_entrada
            tempo_medio_dic[destino['name']]['entrada'] = data_movimento
            tempo_medio_dic[fonte['name']]['saida'] = data_movimento
            if tempo_medio_dic[destino['name']]['entrada'] is not None and tempo_medio_dic[fonte['name']]['saida'] is not None:
                tempo_medio_dic[destino['name']]['total'] += (tempo_medio_dic[fonte['name']]['saida'] - tempo_medio_dic[destino['name']]['entrada']).days
                print(tempo_medio_dic[destino['name']]['total'])
                tempo_medio_dic[destino['name']]['entrada'] = None
                tempo_medio_dic[fonte['name']]['saida'] = None
                tempo_medio_dic[fonte['name']]['quant'] += 1
                print(tempo_medio_dic[fonte['name']]['quant'])

for nome_lista in tempo_medio_dic.keys():
    print('tempo médio em ', nome_lista, tempo_medio_dic[nome_lista]['total']/tempo_medio_dic[nome_lista]['quant'])

