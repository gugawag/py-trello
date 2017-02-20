from trello import trelloclient
from trt13.leitor_configuracao import configuracao
import plotly.graph_objs as go
import sys
import plotly
import datetime

trello = trelloclient.TrelloClient(configuracao['TRELLO_API_KEY'], None, configuracao['OAUTH_TOKEN'], None)

#média de tempo em homologação
#"datetime saída de homologação" - "datetime chegada homologação"
brd_manutencao = trello.get_board(configuracao['ID_BOARD'])
data_entrada = None
data_saida = None
tempos = list()
padrao_entrada = {'entrada':None,'saida':None,'total':0,'quant':0}
tempo_medio_dic = {'Homologando':padrao_entrada,'Fazendo':padrao_entrada, 'Aguardando':padrao_entrada,
                   'Testando':padrao_entrada, 'Implantando':padrao_entrada}

#porcentagem que passou em cada lista
quant_fechados_manutencao = len(brd_manutencao.get_cards(card_filter='closed'))
lista_cartoes_fechados_manutencao = brd_manutencao.get_cards(card_filter='closed')
print('Quantidade cartões:',quant_fechados_manutencao)

nomes_listas_ordem_cronologica = ['Feito', 'Revisado', 'Testado', 'Homologado', 'Implantado', 'Arquivado']
dict_listas_passadas = {'Feito':0, 'Revisado':0, 'Testado':0, 'Homologado':0, 'Implantado':0}
ano_inicial = int(configuracao['ANO_INICIAL'])

quant_cards = 0
quants_cards_total = 0
for cartao in lista_cartoes_fechados_manutencao:
    quants_cards_total += 1
    if cartao.card_created_date.year < ano_inicial:
        continue
    quant_cards += 1
    for movimento in cartao.list_movements():
        fonte = movimento['destination']
        if fonte['name'] not in dict_listas_passadas.keys():
            continue
        dict_listas_passadas[fonte['name']] += 1
        print(dict_listas_passadas)

#taxa de retorno da homologação
quants_cards_total_homologando = 0
quant_cards_retornados_homologacao = 0
for cartao in lista_cartoes_fechados_manutencao:
    if cartao.card_created_date.year < ano_inicial:
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

taxa_retorno_homologacao = quant_cards_retornados_homologacao/quants_cards_total_homologando
print('Taxa retorno: ', taxa_retorno_homologacao)


#taxa de retorno dos testes
quants_cards_total_testando = 0
quant_cards_retornados_testes = 0
for cartao in lista_cartoes_fechados_manutencao:
    if cartao.card_created_date.year < ano_inicial:
        continue
    for movimento in cartao.list_movements():
        fonte = movimento['source']
        destino = movimento['destination']
        if fonte['name']=='Testando':
            quants_cards_total_testando += 1
            print('Testando:',quants_cards_total_testando)
        else:
            continue
        if fonte['name']=='Testando' and destino['name'] not in ('Testado', 'Homologando',
                                                                 'Homologado', 'Implantando', 'Implantado'):
            quant_cards_retornados_testes += 1
            print('Retornados testes:',quant_cards_retornados_testes)

taxa_retorno_testes = quant_cards_retornados_testes/quants_cards_total_testando
print('Taxa retorno testes: ', taxa_retorno_testes)

#taxa de retorno da revisão
quants_cards_total_revisando = 0
quant_cards_retornados_revisao = 0
for cartao in lista_cartoes_fechados_manutencao:
    if cartao.card_created_date.year < ano_inicial:
        continue
    for movimento in cartao.list_movements():
        fonte = movimento['source']
        destino = movimento['destination']
        if fonte['name']=='Revisando':
            quants_cards_total_revisando += 1
            print('Revisando:',quants_cards_total_revisando)
        else:
            continue
        if fonte['name']=='Revisando' and destino['name'] not in ('Revisado', 'Testando', 'Testado',
                                                        'Homologando', 'Homologado', 'Implantando', 'Implantado'):
            quant_cards_retornados_revisao += 1
            print('Retornados revisão:',quant_cards_retornados_revisao)

taxa_retorno_revisao = quant_cards_retornados_revisao/quants_cards_total_revisando
print('Taxa retorno revisão: ', taxa_retorno_revisao)

#taxa de retorno do feito
quants_cards_total_fazendo = 0
quant_cards_retornados_feito = 0
for cartao in lista_cartoes_fechados_manutencao:
    if cartao.card_created_date.year < ano_inicial:
        continue
    for movimento in cartao.list_movements():
        fonte = movimento['source']
        destino = movimento['destination']
        if fonte['name']=='Fazendo':
            quants_cards_total_fazendo += 1
            print('Fazendo:',quants_cards_total_fazendo)
        else:
            continue
        if fonte['name']=='Fazendo' and destino['name'] not in ('Feito', 'Revisando', 'Revisado', 'Testando',
                                                'Testado', 'Homologando', 'Homologado', 'Implantando', 'Implantado'):
            quant_cards_retornados_feito += 1
            print('Retornados feito:',quant_cards_retornados_feito)

taxa_retorno_feito = quant_cards_retornados_feito/quants_cards_total_fazendo
print('Taxa retorno fazendo: ', taxa_retorno_feito)


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
valores_absolutos = list()
for lista in nomes_listas_ordem_cronologica:
    valores_percentuais.append(round(dict_listas_passadas[lista]/quant_cards, 2))
    valores_absolutos.append(dict_listas_passadas[lista])

agora = datetime.datetime.now()
ano_atual = agora.year
mes_atual = agora.month
dia_atual= agora.day

layout = go.Layout(
    title='Aderência ao processo | Índice geral: '+str(percent_aderencia)[2:4]+'% | Período: 01/2016 a ' +
          str(dia_atual)+'/'+str(mes_atual)+'/'+str(ano_atual),
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

lista_quant_absoluta = [('#'+str(valor)) for valor in valores_absolutos]
print('Absoluta: ', lista_quant_absoluta)

data_aderencia = go.Bar(
            x=list(nomes_listas_ordem_cronologica),
            y=list(valores_percentuais),
            text=lista_quant_absoluta,
            marker=dict(
            color=['rgb(30,144,255)', 'rgb(0,0,128)',
                   'rgb(60,179,113)', 'rgb(123,104,238)',
                   'rgb(221,160,221)', 'rgb(250,128,114)']),
            name='Taxa de Aderência'
    )

valores_reais_percentuais_retorno = [0.15, 0.06, 0.08, 0.28, 0, 0]
valores_percentuais_retorno = [round(0.15*0.53, 2), round(0.06*0.55, 2), round(0.08*0.54, 2),
                               round((0.28*0.26), 2), 0, 0]

lista_quant_absoluta_retorno = [(str(valor)+'%') for valor in valores_reais_percentuais_retorno]
data_retorno = go.Bar(
            x=list(nomes_listas_ordem_cronologica),
            y=list(valores_percentuais_retorno),
            text=lista_quant_absoluta_retorno,
            marker=dict(color='rgb(255,0,0)'),
            name='Taxa de Retorno'
    )


data_geral = [data_aderencia, data_retorno]
fig = go.Figure(data=data_geral, layout=layout)

data_hoje = str(ano_atual) + '-' + str(mes_atual) + '-' + str(dia_atual) + '-' + str(agora.hour) + \
            str(agora.minute) + str(agora.second)

plotly.offline.plot(fig, filename=str(configuracao['PASTA_ARQUIVOS_ESTATISTICAS'])+'/aderencia-' + data_hoje)

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
            if tempo_medio_dic[destino['name']]['entrada'] is not None and \
                            tempo_medio_dic[fonte['name']]['saida'] is not None:
                tempo_medio_dic[destino['name']]['total'] += (tempo_medio_dic[fonte['name']]['saida'] -
                                                              tempo_medio_dic[destino['name']]['entrada']).days
                print(tempo_medio_dic[destino['name']]['total'])
                tempo_medio_dic[destino['name']]['entrada'] = None
                tempo_medio_dic[fonte['name']]['saida'] = None
                tempo_medio_dic[fonte['name']]['quant'] += 1
                print(tempo_medio_dic[fonte['name']]['quant'])

for nome_lista in tempo_medio_dic.keys():
    print('tempo médio em ', nome_lista, tempo_medio_dic[nome_lista]['total']/tempo_medio_dic[nome_lista]['quant'])

