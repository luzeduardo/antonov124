#!/usr/local/bin/python
# coding: utf-8

from datetime import datetime, date, timedelta
from collections import deque
from itertools import combinations
import time
import json
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re

reload(sys)
sys.setdefaultencoding('utf8')

def perdelta_start_to_end(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def perdelta_end_to_start(start, end, delta):
    curr = start
    while end > curr:
        yield end
        end -= delta

def days_between(s_year,s_month, s_day, e_year,e_month, e_day):
    d1 = datetime(s_year,s_month, s_day)
    d2 = datetime(e_year,e_month, e_day)
    return abs((d1 - d2).days)

def is_valid_min_days_in_place(start, end, min_days_in_place, exact=True):
    '''
    o parametro exact determina se podemos ficar no minimo x dias ou mais
    ou se podemos ficar exatamente x dias no local True equivale a um numero X dias apenas
    '''
    date_format = "%Y-%m-%d"
    a = datetime.strptime(start, date_format)
    b = datetime.strptime(end, date_format)
    delta = b - a
    num_days = int(delta.total_seconds()) / (3600 * 24) + 1
    if exact==True:
        if num_days == min_days_in_place:
            return True
    else:
        if num_days >= min_days_in_place:
            return True
    return False

def is_friday(date):
    date_format = "%Y-%m-%d"
    day_number = datetime.strptime(date, date_format).weekday()
    if day_number == 4:
        return True
    else:
        return False

def is_weekend_day(date):
    date_format = "%Y-%m-%d"
    day_number = datetime.strptime(date, date_format).weekday()
    if day_number == 5 or day_number == 6:
        return True
    else:
        return False

def date_interval(s_year,s_month, s_day, e_year,e_month, e_day):
    '''
    pega a diferenca entre as datas e gera o range baseado no numero de dias
    '''
    days = days_between(s_year,s_month, s_day, e_year,e_month, e_day)
    counter_days = days
    datas_list = list()

    #menor maior
    while counter_days > 0:
        for result in perdelta_start_to_end(date(s_year,s_month, s_day), date(e_year,e_month, e_day), timedelta(days=1)):
            if counter_days > 0:
                datas_list.append(str(result))
            counter_days = counter_days - 1

    #maior menor
    counter_days = days
    itr = 0
    while counter_days > 0:
        try:
            datetime(s_year,s_month, s_day + itr)
            for result in perdelta_end_to_start(date(s_year, s_month, s_day + itr), date(e_year, e_month, e_day), timedelta(days=1)):
                if itr == 0:
                    continue
                if counter_days > 0:
                    datas_list.append(str(result))
        except Exception, e:
            counter_days = counter_days - 1
            itr += 1
            continue
        counter_days = counter_days - 1
        itr += 1
        datas_list = setlist(datas_list)
    return combinations(datas_list, 2)

def setlist(lst=[]):
   return list(set(lst))

def search(origem, config_destinos, config_datas, ida_durante_semana, volta_durante_semana,
           exactly_days_check, min_days_in_place, timersleep, google_cheap_price_class, ida_sexta_feira, save_db):
    google_processing_price_class = ''
    # iii = 0
    for datas in config_datas:
        for config_origem in origem:
            for destino in config_destinos.items():
                try:
                    if is_friday(datas[0]) and not ida_sexta_feira:
                        continue
                    if not is_friday(datas[0]) and not is_weekend_day(datas[0]) and not ida_durante_semana:
                        continue
                    if not is_weekend_day(datas[1]) and not volta_durante_semana:
                        continue
                    if exactly_days_check and not is_valid_min_days_in_place(datas[0], datas[1], min_days_in_place):
                        continue
                    if datetime.strptime(datas[0], "%Y-%m-%d") >= datetime.strptime(datas[1], "%Y-%m-%d"):
                        continue

                    # print config_origem + ' - ' + str(destino[0])  + ' - ' + datas[0] + ' - ' + datas[1] + ' - ' + str(iii)
                    # iii += 1
                    # continue

                    config_dia_inicio = datas[0]
                    config_dia_fim = datas[1]
                    try:
                        driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any', '--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
                        driver.set_window_size(2048, 2048)  # set browser size.
                    except Exception, e:
                        print "Erro com driver"
                    url = 'https://www.google.com.br/flights/#search;f=' + config_origem + ';t='+ str(destino[0]) +';d='+ config_dia_inicio + ';r=' + config_dia_fim
                    driver.get(url)
                    time.sleep(timersleep)
                    driver.implicitly_wait(timersleep)

                    core = driver.find_element_by_css_selector('#root')
                    class_name = core.get_attribute("class")
                    class_splited = class_name.split('-',1)
                    final_class = '.' + class_splited[0] + google_cheap_price_class

                    try:
                        resultado = driver.find_element_by_css_selector(final_class)
                        valor_exibicao = resultado.text
                        valor_processado = valor_exibicao.split("R$")
                        valor_processado = valor_processado[1]
                        valor_processado = re.sub('[^0-9]+', '', valor_processado)

                        data =  valor_processado + "\t" + url  + "\t" + str(config_origem) + "\t" + str(destino[1])  + "-" + str(destino[0]) + "\t" + datetime.now().strftime("%d/%m/%Y %H:%M") + "\n"
                        datafile =  valor_processado + "\t" + config_dia_inicio + "\t" + config_dia_fim + "\t" + str(config_origem) + "\t" + str(destino[1])  + "-" + str(destino[0]) + "\t" + url  + "\t" + datetime.now().strftime("%d/%m/%Y %H:%M") + "\n"
                        print data
                        file = open('passagem_' + datetime.now().strftime("%d%m%Y") + '.csv', 'a')
                        file.write(datafile)
                        driver.quit()

                    except NoSuchElementException, e:
                        print "\n"
                        notfound_class = '.' + class_splited[0] + '-Pb-e'
                        resultado = driver.find_element_by_css_selector(notfound_class)
                        for ne in nao_existe:
                            if str(ne) == str(destino[1]):
                                problemas.append('Ignorar destino: ' + str(destino[1]))
                        nao_existe.append(str(destino[1]))
                        driver.quit()
                    except Exception, e:
                        problemas.append('Problema ao retornar valor de: ' + str(destino[1]) +"\t" + url)
                        driver.quit()
                except Exception, e:
                    print e
                    problemas.append('Problema ao retornar elemento principal: ' + str(destino[1]) +"\t")
                    driver.quit()

    print 'Hora Fim: ' + datetime.now().strftime("%d/%m/%Y %H:%M")

try:
    with open('config_origem.json', 'r') as f:
        config_origem = json.load(f)
except Exception,e:
    print "Json de origem inválido"

try:
    with open('config_destino.json', 'r') as f:
        config_destino = json.load(f)
except Exception,e:
    print "Json de destino inválido"

try:
    with open('config_params.json', 'r') as f:
        config_params = json.load(f)
except Exception,e:
    print "Json de parâmetros inválido"

try:
    min_days_in_place = config_params['minimo_dias_no_lugar']
    exactly_days_check = config_params['periodo_de_dias_exatos']
    ida_sexta_feira = config_params['ida_sexta_feira']
    ida_durante_semana = config_params['ida_seg_qui']
    volta_durante_semana = config_params['volta_seg_qui']
except Exception, e:
    print "Json de parâmetros inválido"

try:
    datas = ""
    s_year = config_params['start_year']
    s_month = config_params['start_month']
    s_day = config_params['start_day']

    e_year = config_params['end_year']
    e_month = config_params['end_month']
    e_day = config_params['end_day']
    timersleep = config_params['sleep']
    save_db = config_params['save_db']
    google_cheap_price_class = config_params['classe_google_menor_preco_sufixo']

    datas = date_interval(s_year,s_month, s_day, e_year,e_month, e_day)
except Exception, e:
    print "Período de datas inválido"
# ou setando na mao
# datas = [
#     ['2017-04-28','2017-04-30']
# ]

config_datas = datas
problemas = deque()
nao_existe = deque()
search(config_origem, config_destino, config_datas, ida_durante_semana, volta_durante_semana, exactly_days_check,
       min_days_in_place, timersleep, google_cheap_price_class, ida_sexta_feira, save_db)
