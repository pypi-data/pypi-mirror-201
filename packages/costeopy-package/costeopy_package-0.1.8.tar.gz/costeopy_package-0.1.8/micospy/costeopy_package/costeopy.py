import math

# Librerías para importar padrón de ESCALE

import pandas as pd
import httplib2
from bs4 import BeautifulSoup
import wget
import zipfile
import os
from dbfread import DBF

# Datos para agregar documentación

from pandas import DataFrame

# Ejemplos

def mancha(num1,num2):
    return num1+num2

def leo(num1,num2):
    return num1-num2

def vaca(num1,num2):
    return num1*num2

def mila(num1,num2):
    return num1/num2

# Lista de meses

mes_13=['ene','feb','mar','abr','may','jun','jul','ago','set','oct','nov','dic','anual']
mes_12=['ene','feb','mar','abr','may','jun','jul','ago','set','oct','nov','dic']
mes_10=['mar','abr','may','jun','jul','ago','set','oct','nov','dic']
mes_inactivo_2=['ene','feb']
mes_agui_2=['jul','dic']
mes_noagui_2=['ene','feb','mar','abr','may','jun','ago','set','oct','nov']

'''
        ETAPA 2: Definir funciones

'''

def cas(base,nombre_perfil,meses_perfil,monto_perfil):

    base['cas_'+nombre_perfil+'_anual'] = base[nombre_perfil]*meses_perfil*monto_perfil

    if meses_perfil == 12:

        for mes in mes_12:
            base['cas_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*monto_perfil

    else:

        for mes in mes_10:
            base['cas_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*monto_perfil

        for mes in mes_inactivo_2:
            base['cas_'+nombre_perfil+'_'+mes] = 0

#cas('psi_10',m_10,monto_psi)

# Aguinaldo

# nombre_perfil: nombre del perfil, entre comillas
# veces_agui: número de veces que recibe aguinaldo
# monto_agui: monto del aguinaldo

def aguinaldo(base,nombre_perfil,veces_agui,monto_agui):

    base['agui_'+nombre_perfil+'_anual'] = base[nombre_perfil]*veces_agui*monto_agui

    for mes in mes_agui_2:
        base['agui_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*monto_agui

    for mes in mes_noagui_2:
        base['agui_'+nombre_perfil+'_'+mes] = 0

#aguinaldo('vig',agui_2,monto_agui)

# Tope de Essalud

# UIT_porc: Porcentaje de UIT
# UIT: UIT del año

def tope(UIT_porc,UIT):
    x=math.ceil(0.09*UIT_porc*UIT)
    return x

#monto_tope=tope(0.55,4600)

# Aporte individual a EsSalud

# nombre_perfil: nombre del perfil, entre comillas
# monto_perfil: monto del perfil
# monto_tope: monto de tope de EsSalud, hallada con la función tope

def aporte_essalud(base,nombre_perfil,monto_perfil,monto_tope):

    base['ess_'+nombre_perfil] = min(math.ceil(0.09*monto_perfil),monto_tope)

#aporte_essalud('mant', monto_vig, monto_tope)

# EsSalud

# nombre_perfil: nombre del perfil, entre comillas
# meses_perfil: número de meses activos del perfil

def essalud(base,nombre_perfil,meses_perfil):

    base['essalud_'+nombre_perfil+'_anual'] = base[nombre_perfil]*meses_perfil*base['ess_'+nombre_perfil]

    if meses_perfil == 12:

        for mes in mes_12:
            base['essalud_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*base['ess_'+nombre_perfil]

    else:

        for mes in mes_10:
            base['essalud_'+nombre_perfil+'_'+mes] = base[nombre_perfil]*base['ess_'+nombre_perfil]

        for mes in mes_inactivo_2:
            base['essalud_'+nombre_perfil+'_'+mes] = 0

# Total por perfil

# nombre: puede tomar los valores = cas, essalud, agui
# nombre_perfil: nombre del perfil, entre comillas
# continuidad: si el perfil cuenta con continuidad, puede tomar valores = 1, 2
# 1: perfil con solo contrato de 12 meses o solo 10 meses
# 2: perfil con contrato de 12 meses y 10 meses
# 3: perfil con contrato de solo 12 meses
# 4: perfil con contrato de solo 10 meses

def total_perfil(base,nombre,nombre_perfil,continuidad):

    if continuidad == 1:
        base[nombre+'_'+nombre_perfil+'_total'] = base[nombre+'_'+nombre_perfil+'_anual']

    if continuidad == 2:
        base[nombre+'_'+nombre_perfil+'_total'] = base[nombre+'_'+nombre_perfil+'_anual']+base[nombre+'_'+nombre_perfil+'_10_anual']

    if continuidad == 3:
        base[nombre+'_'+nombre_perfil+'_total'] = base[nombre+'_'+nombre_perfil+'_anual']

    if continuidad == 4:
        base[nombre+'_'+nombre_perfil+'_total'] = base[nombre+'_'+nombre_perfil+'_10_anual']

# Total por perfil por meses

# nombre: puede tomar los valores = cas, essalud, agui
# nombre_perfil: nombre del perfil, entre comillas
# continuidad: si el perfil cuenta con continuidad, puede tomar valores = 1, 2
# 1: perfil con solo contrato de 12 meses o solo 10 meses
# 2: perfil con contrato de 12 meses y 10 meses
# 3: perfil con contrato de solo 12 meses
# 4: perfil con contrato de solo 10 meses

def total_perfil_mes(base,nombre,nombre_perfil,continuidad):

    if continuidad == 1:

        for mes in mes_12:
            base[nombre+'_'+nombre_perfil+'_total_'+mes] = base[nombre+'_'+nombre_perfil+'_'+mes]

    if continuidad == 2:

        for mes in mes_12:
            base[nombre+'_'+nombre_perfil+'_total_'+mes] = base[nombre+'_'+nombre_perfil+'_'+mes]+base[nombre+'_'+nombre_perfil+'_10_'+mes]

    if continuidad == 3:

        for mes in mes_12:
            base[nombre+'_'+nombre_perfil+'_total_'+mes] = base[nombre+'_'+nombre_perfil+'_'+mes]

    if continuidad == 4:

        for mes in mes_12:
            base[nombre+'_'+nombre_perfil+'_total_'+mes] = base[nombre+'_'+nombre_perfil+'_10_'+mes]

# Totales

# nombre: puede tomar los valores = cas, essalud, agui, costo
# cas: costo total de CAS de todos los perfiles
# ess: costo total de EsSalud de todos los perfiles
# agui: costo total de aguinaldo de todos los perfiles
# costo: suma de CAS, EsSalud y aguinaldo

def total(base,nombre):

    if nombre == 'cas':
        base['total_'+nombre+'_admin'] = base[base.columns[[x.startswith('cas_') for x in base.columns]].tolist()].sum(axis=1)
    elif nombre == 'essalud':
        base['total_'+nombre+'_admin'] = base[base.columns[[x.startswith('essalud_') for x in base.columns]].tolist()].sum(axis=1)
    elif nombre == 'agui':
        base['total_'+nombre+'_admin'] = base[base.columns[[x.startswith('agui_') for x in base.columns]].tolist()].sum(axis=1)
    else:
        base[nombre+'_cas_admin'] = base[base.columns[[x.startswith('total_') for x in base.columns]].tolist()].sum(axis=1)

# Total por mes

# nombre: puede tomar los valores = cas, essalud, agui
# cas: costo total de CAS de todos los perfiles por mes
# ess: costo total de EsSalud de todos los perfiles por mes
# agui: costo total de aguinaldo de todos los perfiles por mes

def total_mes(base,nombre):

    if nombre == 'cas':
        bcas = base[base.columns[[x.startswith('cas_') for x in base.columns]].tolist()]
        base['cas_admin_ene'] = bcas[bcas.columns[[x.endswith('_ene') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_feb'] = bcas[bcas.columns[[x.endswith('_feb') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_mar'] = bcas[bcas.columns[[x.endswith('_mar') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_abr'] = bcas[bcas.columns[[x.endswith('_abr') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_may'] = bcas[bcas.columns[[x.endswith('_may') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_jun'] = bcas[bcas.columns[[x.endswith('_jun') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_jul'] = bcas[bcas.columns[[x.endswith('_jul') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_ago'] = bcas[bcas.columns[[x.endswith('_ago') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_set'] = bcas[bcas.columns[[x.endswith('_set') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_oct'] = bcas[bcas.columns[[x.endswith('_oct') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_nov'] = bcas[bcas.columns[[x.endswith('_nov') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_dic'] = bcas[bcas.columns[[x.endswith('_dic') for x in bcas.columns]].tolist()].sum(axis=1)
        base['cas_admin_anual'] = bcas[bcas.columns[[x.endswith('_anual') for x in bcas.columns]].tolist()].sum(axis=1)

    elif nombre == 'essalud':
        bcas = base[base.columns[[x.startswith('essalud_') for x in base.columns]].tolist()]
        base['essalud_admin_ene'] = bcas[bcas.columns[[x.endswith('_ene') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_feb'] = bcas[bcas.columns[[x.endswith('_feb') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_mar'] = bcas[bcas.columns[[x.endswith('_mar') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_abr'] = bcas[bcas.columns[[x.endswith('_abr') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_may'] = bcas[bcas.columns[[x.endswith('_may') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_jun'] = bcas[bcas.columns[[x.endswith('_jun') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_jul'] = bcas[bcas.columns[[x.endswith('_jul') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_ago'] = bcas[bcas.columns[[x.endswith('_ago') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_set'] = bcas[bcas.columns[[x.endswith('_set') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_oct'] = bcas[bcas.columns[[x.endswith('_oct') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_nov'] = bcas[bcas.columns[[x.endswith('_nov') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_dic'] = bcas[bcas.columns[[x.endswith('_dic') for x in bcas.columns]].tolist()].sum(axis=1)
        base['essalud_admin_anual'] = bcas[bcas.columns[[x.endswith('_anual') for x in bcas.columns]].tolist()].sum(axis=1)

    else:
        bcas = base[base.columns[[x.startswith('agui_') for x in base.columns]].tolist()]
        base['agui_admin_ene'] = bcas[bcas.columns[[x.endswith('_ene') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_feb'] = bcas[bcas.columns[[x.endswith('_feb') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_mar'] = bcas[bcas.columns[[x.endswith('_mar') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_abr'] = bcas[bcas.columns[[x.endswith('_abr') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_may'] = bcas[bcas.columns[[x.endswith('_may') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_jun'] = bcas[bcas.columns[[x.endswith('_jun') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_jul'] = bcas[bcas.columns[[x.endswith('_jul') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_ago'] = bcas[bcas.columns[[x.endswith('_ago') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_set'] = bcas[bcas.columns[[x.endswith('_set') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_oct'] = bcas[bcas.columns[[x.endswith('_oct') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_nov'] = bcas[bcas.columns[[x.endswith('_nov') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_dic'] = bcas[bcas.columns[[x.endswith('_dic') for x in bcas.columns]].tolist()].sum(axis=1)
        base['agui_admin_anual'] = bcas[bcas.columns[[x.endswith('_anual') for x in bcas.columns]].tolist()].sum(axis=1)

def padron_web(ruta: str, almacenar: bool = True) -> DataFrame:

    '''
    Proporciona la versión más reciente del Padrón web

    ruta: str
        Directorio de descarga

    almacenar: bool, por defecto True
        Ingresar True si se quiere conservar las versiones anteriores del Padrón web, ingresar False si solo se quiere conservar la última versión del Padrón web

    Nota: El output se debe almacenar en un DataFrame

    Ejm:
    -----

    >>> padron = ct.padron_web('D:\eder', True)

    '''

    if almacenar == True:

        # Definir ruta

        #ruta='D:\eder'

        # Creación de carpeta

        dir = os.path.join(ruta, 'padron_web')

        if not os.path.exists(dir):
            os.mkdir(dir)

        else:
            print('Ya existe la carpeta')

        # Extración de enlaces del portal de ESCALE

        url = 'http://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/958881'

        http = httplib2.Http()

        response, content = http.request(url)

        links=[]

        for link in BeautifulSoup(content).find_all('a', href=True):
            links.append(link['href'])

        for link in links:
            print(link)

        enlace_1 = links [26:30]

        # Establecer enlace con fecha más actual

        l1=enlace_1[0]
        l2=enlace_1[1]
        l3=enlace_1[2]
        l4=enlace_1[3]

        n1=l1[76:81]
        n2=l2[76:81]
        n3=l3[76:81]
        n4=l4[76:81]

        mayor=max(n1,n2,n3,n4)

        enlace_2='http://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/958881/'+mayor+';jsessionid=28cf9ab9d37f6fed3dfe4cea19d6?_110_INSTANCE_GMv7_redirect=http%3A%2F%2Fescale.minedu.gob.pe%2Fuee%2F-%2Fdocument_library_display%2FGMv7%2Fview%2F958881%3Bjsessionid%3D28cf9ab9d37f6fed3dfe4cea19d6'

        # Extraer zip del enlace con fecha más actual

        url = enlace_2

        http = httplib2.Http()

        response, content = http.request(url)

        links=[]

        for link in BeautifulSoup(content).find_all('a', href=True):
            links.append(link['href'])

        for link in links:
            print(link)

        enlace_3 = links [32:33]

        # Enlace zip con fecha más actual

        e1=enlace_3[0]
        e2=e1[62:70]

        file = 'padron_web\Padron_web_'+e2+'.zip'

        # Extracción del padrón web en formato dbf

        path = os.path.join(ruta, file)

        if not os.path.exists(path):
            wget.download(enlace_3[0], ruta+'\padron_web')
            path2=os.path.join(ruta, '\padron_web\Padron_web.dbf')

            if not os.path.exists(path2):
                fantasy_zip = zipfile.ZipFile(ruta+'\padron_web\Padron_web_'+e2+'.zip')
                fantasy_zip.extract('Padron_web.dbf', ruta+'\padron_web')
                path3 = ruta+'/padron_web/'
                os.rename(path3+'Padron_web.dbf', path3+'Padron_web_'+e2+'.dbf')

            else:
                print('Ya existe el Padron_web.dbf')

        else:
            print('Ya existe el Padron_web_'+e2+'.zip')

        # Importar Padrón web con fecha más actual a Python

        # Generar DBF

        b_dbf=DBF(ruta+'\padron_web\Padron_web_'+e2+'.dbf')

        # Generar dataframe

        padweb = pd.DataFrame(iter(b_dbf))

        return padweb

    elif almacenar == False:

        # Creación de carpeta

        dir = os.path.join(ruta, 'padron_web')

        if not os.path.exists(dir):
            os.mkdir(dir)

        else:
            print('Ya existe la carpeta')

        # Eliminar todos los padrones

        dir = ruta+'\padron_web'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        # Extración de enlaces del portal de ESCALE

        url = 'http://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/958881'

        http = httplib2.Http()

        response, content = http.request(url)

        links=[]

        for link in BeautifulSoup(content).find_all('a', href=True):
            links.append(link['href'])

        for link in links:
            print(link)

        enlace_1 = links [26:30]

        # Establecer enlace con fecha más actual

        l1=enlace_1[0]
        l2=enlace_1[1]
        l3=enlace_1[2]
        l4=enlace_1[3]

        n1=l1[76:81]
        n2=l2[76:81]
        n3=l3[76:81]
        n4=l4[76:81]

        mayor=max(n1,n2,n3,n4)

        enlace_2='http://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/958881/'+mayor+';jsessionid=28cf9ab9d37f6fed3dfe4cea19d6?_110_INSTANCE_GMv7_redirect=http%3A%2F%2Fescale.minedu.gob.pe%2Fuee%2F-%2Fdocument_library_display%2FGMv7%2Fview%2F958881%3Bjsessionid%3D28cf9ab9d37f6fed3dfe4cea19d6'

        # Extraer zip del enlace con fecha más actual

        url = enlace_2

        http = httplib2.Http()

        response, content = http.request(url)

        links=[]

        for link in BeautifulSoup(content).find_all('a', href=True):
            links.append(link['href'])

        for link in links:
            print(link)

        enlace_3 = links [32:33]

        # Enlace zip con fecha más actual

        e1=enlace_3[0]
        e2=e1[62:70]

        file = 'padron_web\Padron_web_'+e2+'.zip'

        # Extracción del padrón web en formato dbf

        path = os.path.join(ruta, file)

        if not os.path.exists(path):
            wget.download(enlace_3[0], ruta+'\padron_web')
            path2=os.path.join(ruta, '\padron_web\Padron_web.dbf')

            if not os.path.exists(path2):
                fantasy_zip = zipfile.ZipFile(ruta+'\padron_web\Padron_web_'+e2+'.zip')
                fantasy_zip.extract('Padron_web.dbf', ruta+'\padron_web')
                path3 = ruta+'/padron_web/'
                os.rename(path3+'Padron_web.dbf', path3+'Padron_web_'+e2+'.dbf')

            else:
                print('Ya existe el Padron_web.dbf')

        else:
            print('Ya existe el Padron_web_'+e2+'.zip')

        # Importar Padrón web con fecha más actual a Python

        # Generar DBF

        b_dbf=DBF(ruta+'\padron_web\Padron_web_'+e2+'.dbf')

        # Generar dataframe

        padweb = pd.DataFrame(iter(b_dbf))

        return padweb

def siga_obj(base: DataFrame, objeto: str) -> DataFrame:

    '''
    Proporciona la base SIGA filtrada para un objeto

    base: DataFrame
        Base del SIGA

    objeto: str
        Nombre del objeto de búsqueda, debe estar en mayúscula

    Nota: El resultado se debe almacenar en un DataFrame

    Ejm:

        siga_tablet=ct.siga_obj(base_siga,'TABLET')
    '''

    base['GRUPO_BIEN'] = base['GRUPO_BIEN'].str.zfill(2)
    base['CLASE_BIEN'] = base['CLASE_BIEN'].str.zfill(2)
    base['FAMILIA_BIEN'] = base['FAMILIA_BIEN'].str.zfill(4)
    base['ITEM_BIEN'] = base['ITEM_BIEN'].str.zfill(4)

    sigaf=base.loc[(base['SECTOR'] != '01')]

    sigaf['verificar']=sigaf['NOMBRE_ITEM'].str.contains(objeto)

    sigaobj=sigaf.loc[(sigaf['verificar'] == True)]

    sigaobj['cod_siga'] = sigaobj['GRUPO_BIEN']+'.'+sigaobj['CLASE_BIEN']+'.'+sigaobj['FAMILIA_BIEN']+'.'+sigaobj['ITEM_BIEN']

    del sigaobj['verificar']

    return sigaobj

def precio_obj(siga_objeto: DataFrame) -> DataFrame:

    '''
    Proporciona una base de precios de un objeto de la base SIGA

    siga_objeto: DataFrame
        Resultado de la función siga_obj

    Nota: El resultado se debe almacenar en un DataFrame

    Ejm:

        precio_tablet=ct.precio_obj(siga_tablet)
    '''

    siga_objeto['n'] = 1
    objetoa=siga_objeto[['NOMBRE_ITEM','cod_siga','n','PRECIO_UNIT']]

    cant=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['n']].sum().reset_index()
    cant.rename(columns={'n':'cantidad'},inplace=True)

    media=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].mean().reset_index()
    media.rename(columns={'PRECIO_UNIT':'media'},inplace=True)

    p20=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.20).reset_index()
    p20.rename(columns={'PRECIO_UNIT':'p20'},inplace=True)

    p50=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.50).reset_index()
    p50.rename(columns={'PRECIO_UNIT':'mediana'},inplace=True)

    p80=objetoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.80).reset_index()
    p80.rename(columns={'PRECIO_UNIT':'p80'},inplace=True)

    media_cant=pd.merge(cant, media, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50=pd.merge(media_cant, p50, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50_20=pd.merge(media_cant_p50, p20, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50_20_80=pd.merge(media_cant_p50_20, p80, on =['NOMBRE_ITEM','cod_siga'], how ='inner')

    return media_cant_p50_20_80

def siga_cod(base: DataFrame, codigo: str) -> DataFrame:

    '''
    Proporciona la base SIGA filtrada para un código

    base: DataFrame
        Base del SIGA

    codigo: str
        Código de búsqueda

    El resultado se debe almacenar en un DataFrame

    Ejm:

        siga_7408=ct.siga_cod(base_siga,'74.08.9493.0001')
    '''

    base['GRUPO_BIEN'] = base['GRUPO_BIEN'].str.zfill(2)
    base['CLASE_BIEN'] = base['CLASE_BIEN'].str.zfill(2)
    base['FAMILIA_BIEN'] = base['FAMILIA_BIEN'].str.zfill(4)
    base['ITEM_BIEN'] = base['ITEM_BIEN'].str.zfill(4)

    sigaf=base.loc[(base['SECTOR'] != '01')]

    sigaf['cod_siga'] = sigaf['GRUPO_BIEN']+'.'+sigaf['CLASE_BIEN']+'.'+sigaf['FAMILIA_BIEN']+'.'+sigaf['ITEM_BIEN']

    sigaf['verificar']=sigaf['cod_siga'].str.contains(codigo)

    sigaobj=sigaf.loc[(sigaf['verificar'] == True)]

    del sigaobj['verificar']

    return sigaobj

def precio_cod(siga_codigo: DataFrame) -> DataFrame:

    '''
    Proporciona una base de precios de un código de la base SIGA

    siga_codigo: DataFrame
        Resultado de la función siga_cod

    Nota: El resultado se debe almacenar en un DataFrame

    Ejm:

        precio_7408=ct.precio_cod(siga_7408)
    '''

    siga_codigo['n'] = 1
    codigoa=siga_codigo[['NOMBRE_ITEM','cod_siga','n','PRECIO_UNIT']]

    cant=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['n']].sum().reset_index()
    cant.rename(columns={'n':'cantidad'},inplace=True)

    media=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].mean().reset_index()
    media.rename(columns={'PRECIO_UNIT':'media'},inplace=True)

    p20=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.20).reset_index()
    p20.rename(columns={'PRECIO_UNIT':'p20'},inplace=True)

    p50=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.50).reset_index()
    p50.rename(columns={'PRECIO_UNIT':'mediana'},inplace=True)

    p80=codigoa.groupby(['NOMBRE_ITEM','cod_siga'])[['PRECIO_UNIT']].quantile(0.80).reset_index()
    p80.rename(columns={'PRECIO_UNIT':'p80'},inplace=True)

    media_cant=pd.merge(cant, media, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50=pd.merge(media_cant, p50, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50_20=pd.merge(media_cant_p50, p20, on =['NOMBRE_ITEM','cod_siga'], how ='inner')
    media_cant_p50_20_80=pd.merge(media_cant_p50_20, p80, on =['NOMBRE_ITEM','cod_siga'], how ='inner')

    return media_cant_p50_20_80

# Importar base de traslados

def traslados(ruta,base):

    if base == 'movccpp':

        t = pd.read_stata(ruta+'/MovCCPP.dta')

    elif base == 'moviiee':

        t = pd.read_stata(ruta+'/MovIIEE.dta')

    elif base == 'movugel':

        t = pd.read_stata(ruta+'/MovUGEL.dta')

    return t

# Renombrar meses

def remes(base):

    base.rename(columns={'13':'costo_anual'},inplace=True)
    base.rename(columns={'1':'enero'},inplace=True)
    base.rename(columns={'2':'febrero'},inplace=True)
    base.rename(columns={'3':'marzo'},inplace=True)
    base.rename(columns={'4':'abril'},inplace=True)
    base.rename(columns={'5':'mayo'},inplace=True)
    base.rename(columns={'6':'junio'},inplace=True)
    base.rename(columns={'7':'julio'},inplace=True)
    base.rename(columns={'8':'agosto'},inplace=True)
    base.rename(columns={'9':'septiembre'},inplace=True)
    base.rename(columns={'10':'octubre'},inplace=True)
    base.rename(columns={'11':'noviembre'},inplace=True)
    base.rename(columns={'12':'diciembre'},inplace=True)

def validar_padron(dire: DataFrame, padweb: DataFrame, ue: DataFrame, nivel: str) -> DataFrame:

    '''
    Validaciones del padrón y metas físicas de la intervención donde se verifican: el código local, el nombre del pliego, nombre de la unidad ejecutora, nombre de la ugel y nombre de la institución educativa considerando como dato de validación a los códigos modulares. Se usan como insumos de validación al Padrón web de Escale y a la Base UE UGEL del Equipo Analítica de Datos

    dire: DataFrame
        Base de la dirección

    padweb: DataFrame
        Base del Padrón web

    ue: DataFrame
        Base UE UGEL

    nivel: str
        Nivel de en la cual se encuentra el padrón de la intervención, en esta parte se debe indicar si los colegios militares forman parte del padrón

    Ejm:
    ----

    >>> metas = ct.validar_padron(dire, padweb, ue, 'militar_ugel')

    '''

    if nivel == 'cod_mod':

        # Cambio de formato para validación

        dire.cod_mod=dire.cod_mod.astype(int)
        dire.cod_local_dire=dire.cod_local_dire.astype(int)
        dire.anexo=dire.anexo.astype(int)

        # Filtrar para estado igual a activa IE

        padweb_a = padweb[padweb.D_ESTADO == 'Activa']

        # Establecer df con variables de interés

        padweb_i=padweb_a[['COD_MOD','CODOOII','CODLOCAL','ANEXO','CEN_EDU','D_NIV_MOD']]

        # Verificar tipo de variables

        print(padweb_i.dtypes)

        # Pasar a integer

        padweb_i.COD_MOD=padweb_i.COD_MOD.astype(int)
        padweb_i.CODOOII=padweb_i.CODOOII.astype(int)
        padweb_i.ANEXO=padweb_i.ANEXO.astype(int)

        padweb_i.loc[(padweb_i['CODLOCAL'] == ''),'CODLOCAL'] = '0'

        padweb_i.CODLOCAL=padweb_i.CODLOCAL.astype(int)

        # Renombrar variables

        padweb_i.rename(columns={'COD_MOD':'cod_mod'},inplace=True)
        padweb_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        padweb_i.rename(columns={'CODLOCAL':'cod_local'},inplace=True)
        padweb_i.rename(columns={'ANEXO':'anexo'},inplace=True)
        padweb_i.rename(columns={'CEN_EDU':'nombre_iiee'},inplace=True)
        padweb_i.rename(columns={'COD_CAR':'cod_car'},inplace=True)
        padweb_i.rename(columns={'DAREACENSO':'dareacenso'},inplace=True)
        padweb_i.rename(columns={'D_NIV_MOD':'nivel'},inplace=True)

        # Combinar bases

        dire_padweb=pd.merge(dire, padweb_i, on =['cod_mod','anexo'], how ='left',indicator=True)

        # variables de interés

        ue_i=ue[['PLIEGO','EJECUTORA','CODOOII','NOM_PLIEGO','NOM_UE','UGEL']]

        # Renombrar variables

        ue_i.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
        ue_i.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
        ue_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        ue_i.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
        ue_i.rename(columns={'NOM_UE':'nom_ue'},inplace=True)
        ue_i.rename(columns={'UGEL':'ugel'},inplace=True)

        # Eliminar NA

        ue_i = ue_i.dropna()

        # Eliminar colegios militares

        ue_i.drop(ue_i[ue_i['nom_ue'].str.contains('301. COLEGIO MILITAR')].index, inplace=True)

        # Combinar bases usando inner

        dire_padweb_ue=pd.merge(dire_padweb, ue_i, on =['cod_ugel'], how ='left',indicator='merge_2')

        # Variables de interés

        bint=dire_padweb_ue[['cod_mod','cod_ugel','cod_local_dire','cod_local','nom_pliego_dire','nom_pliego','nom_ue_dire','nom_ue','ugel_dire','ugel','nombre_iiee_dire','nombre_iiee','nivel']]

        # Comparar suma con el total; out: True

        bint['cod_local_ver'] = bint['cod_local_dire'].eq(bint['cod_local'])
        bint['nom_pliego_ver'] = bint['nom_pliego_dire'].eq(bint['nom_pliego'])
        bint['nom_ue_ver'] = bint['nom_ue_dire'].eq(bint['nom_ue'])
        bint['ugel_ver'] = bint['ugel_dire'].eq(bint['ugel'])
        bint['nombre_iiee_ver'] = bint['nombre_iiee_dire'].eq(bint['nombre_iiee'])

        return bint

    elif nivel == 'ugel':

        # Variables de interés

        ue_i=ue[['PLIEGO','EJECUTORA','CODOOII','NOM_PLIEGO','NOM_UE','UGEL']]

        # Renombrar variables

        ue_i.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
        ue_i.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
        ue_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        ue_i.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
        ue_i.rename(columns={'NOM_UE':'nom_ue'},inplace=True)
        ue_i.rename(columns={'UGEL':'ugel'},inplace=True)

        # Eliminar NA

        ue_i = ue_i.dropna()

        # Eliminar colegios militares

        ue_i.drop(ue_i[ue_i['nom_ue'].str.contains('301. COLEGIO MILITAR')].index, inplace=True)

        # Combinar bases usando inner

        dire_padweb_ue=pd.merge(dire, ue_i, on =['cod_ugel'], how ='left',indicator='merge_2')

        # Variables de interés

        bint=dire_padweb_ue[['cod_ugel','nom_pliego_dire','nom_pliego','nom_ue_dire','nom_ue','ugel_dire','ugel']]

        # Comparar; out: True

        bint['nom_pliego_ver'] = bint['nom_pliego_dire'].eq(bint['nom_pliego'])
        bint['nom_ue_ver'] = bint['nom_ue_dire'].eq(bint['nom_ue'])
        bint['ugel_ver'] = bint['ugel_dire'].eq(bint['ugel'])

        return bint

    elif nivel == 'militar_cod_mod':

        # Cambio de formato para validación

        dire.cod_mod=dire.cod_mod.astype(int)
        dire.cod_local_dire=dire.cod_local_dire.astype(int)
        dire.anexo=dire.anexo.astype(int)

        # Filtrar para estado igual a activa IE

        padweb_a = padweb[padweb.D_ESTADO == 'Activa']

        # Establecer df con variables de interés

        padweb_i=padweb_a[['COD_MOD','CODOOII','CODLOCAL','ANEXO','CEN_EDU','D_NIV_MOD']]

        # Verificar tipo de variables

        print(padweb_i.dtypes)

        # Pasar a integer

        padweb_i.COD_MOD=padweb_i.COD_MOD.astype(int)
        padweb_i.CODOOII=padweb_i.CODOOII.astype(int)
        padweb_i.ANEXO=padweb_i.ANEXO.astype(int)

        padweb_i.loc[(padweb_i['CODLOCAL'] == ''),'CODLOCAL'] = '0'

        padweb_i.CODLOCAL=padweb_i.CODLOCAL.astype(int)

        # Renombrar variables

        padweb_i.rename(columns={'COD_MOD':'cod_mod'},inplace=True)
        padweb_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        padweb_i.rename(columns={'CODLOCAL':'cod_local'},inplace=True)
        padweb_i.rename(columns={'ANEXO':'anexo'},inplace=True)
        padweb_i.rename(columns={'CEN_EDU':'nombre_iiee'},inplace=True)
        padweb_i.rename(columns={'COD_CAR':'cod_car'},inplace=True)
        padweb_i.rename(columns={'DAREACENSO':'dareacenso'},inplace=True)
        padweb_i.rename(columns={'D_NIV_MOD':'nivel'},inplace=True)

        # Combinar bases

        dire_padweb=pd.merge(dire, padweb_i, on =['cod_mod','anexo'], how ='left',indicator=True)

        # variables de interés

        ue_i=ue[['PLIEGO','EJECUTORA','CODOOII','NOM_PLIEGO','NOM_UE','UGEL']]

        # Renombrar variables

        ue_i.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
        ue_i.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
        ue_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        ue_i.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
        ue_i.rename(columns={'NOM_UE':'nom_ue'},inplace=True)
        ue_i.rename(columns={'UGEL':'ugel'},inplace=True)

        # Eliminar NA

        ue_i = ue_i.dropna()

        # Eliminar colegios militares

        ue_i.drop(ue_i[ue_i['nom_ue'].str.contains('301. COLEGIO MILITAR')].index, inplace=True)

        # Combinar bases usando inner

        dire_padweb_ue=pd.merge(dire_padweb, ue_i, on =['cod_ugel'], how ='left',indicator='merge_2')

        # Arreglo para colegios militares

        dire_padweb_ue.loc[(dire_padweb_ue['nombre_iiee']=='MILITAR PEDRO RUIZ GALLO') & (dire_padweb_ue['cod_ugel']==200001),'nom_ue'] = '301. COLEGIO MILITAR PEDRO RUIZ GALLO'
        dire_padweb_ue.loc[(dire_padweb_ue['nombre_iiee']=='MILITAR LEONCIO PRADO') & (dire_padweb_ue['cod_ugel']==70101),'nom_ue'] = '301. COLEGIO MILITAR LEONCIO PRADO'

        # Variables de interés

        bint=dire_padweb_ue[['cod_mod','cod_ugel','cod_local_dire','cod_local','nom_pliego_dire','nom_pliego','nom_ue_dire','nom_ue','ugel_dire','ugel','nombre_iiee_dire','nombre_iiee','nivel']]

        # Comparar suma con el total; out: True

        bint['cod_local_ver'] = bint['cod_local_dire'].eq(bint['cod_local'])
        bint['nom_pliego_ver'] = bint['nom_pliego_dire'].eq(bint['nom_pliego'])
        bint['nom_ue_ver'] = bint['nom_ue_dire'].eq(bint['nom_ue'])
        bint['ugel_ver'] = bint['ugel_dire'].eq(bint['ugel'])
        bint['nombre_iiee_ver'] = bint['nombre_iiee_dire'].eq(bint['nombre_iiee'])

        return bint

    elif nivel == 'militar_ugel':

        # Variables de interés

        ue_i=ue[['PLIEGO','EJECUTORA','CODOOII','NOM_PLIEGO','NOM_UE','UGEL']]

        # Renombrar variables

        ue_i.rename(columns={'PLIEGO':'cod_pliego'},inplace=True)
        ue_i.rename(columns={'EJECUTORA':'cod_ue'},inplace=True)
        ue_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
        ue_i.rename(columns={'NOM_PLIEGO':'nom_pliego'},inplace=True)
        ue_i.rename(columns={'NOM_UE':'nom_ue'},inplace=True)
        ue_i.rename(columns={'UGEL':'ugel'},inplace=True)

        # Eliminar NA

        ue_i = ue_i.dropna()

        # Eliminar colegios militares

        ue_i.drop(ue_i[ue_i['nom_ue'].str.contains('301. COLEGIO MILITAR')].index, inplace=True)

        # Combinar bases usando inner

        dire_padweb_ue=pd.merge(dire, ue_i, on =['cod_ugel'], how ='left',indicator='merge_2')

        # Arreglo para colegios militares

        dire_padweb_ue.loc[(dire_padweb_ue['nom_ue_dire']=='301. COLEGIO MILITAR PEDRO RUIZ GALLO'),'nom_ue'] = '301. COLEGIO MILITAR PEDRO RUIZ GALLO'
        dire_padweb_ue.loc[(dire_padweb_ue['nom_ue_dire']=='301. COLEGIO MILITAR LEONCIO PRADO'),'nom_ue'] = '301. COLEGIO MILITAR LEONCIO PRADO'

        # Variables de interés

        bint=dire_padweb_ue[['cod_ugel','nom_pliego_dire','nom_pliego','nom_ue_dire','nom_ue','ugel_dire','ugel']]

        # Comparar; out: True

        bint['nom_pliego_ver'] = bint['nom_pliego_dire'].eq(bint['nom_pliego'])
        bint['nom_ue_ver'] = bint['nom_ue_dire'].eq(bint['nom_ue'])
        bint['ugel_ver'] = bint['ugel_dire'].eq(bint['ugel'])

        return bint

def validar_activo(dire: DataFrame, padweb: DataFrame) -> DataFrame:

    '''
    Validaciones del padrón de la intervención donde se verifica si el código modular esta activo y es de gestión pública usando el Padrón web de Escale

    dire: DataFrame
        Base de la dirección

    padweb: DataFrame
        Base del Padrón web

    Ejm:
    ----

    >>> iiee_activas = ct.validar_activo(dire, padweb)

    '''

    # Filtrar para estado igual a activa

    padweb_a = padweb[padweb.D_ESTADO == 'Activa']

    # Filtrar para instituciones educativas públicas

    padweb_a_p=padweb_a.loc[(padweb_a['GESTION']=='1')|(padweb_a['GESTION']=='2')]

    # Establecer df con variables de interés

    padweb_i=padweb_a_p[['COD_MOD','CODOOII','CODLOCAL','ANEXO','CEN_EDU','D_NIV_MOD','TALUMNO','TDOCENTE']]

    # Verificar tipo de variables

    print(padweb_i.dtypes)

    # Pasar a integer

    padweb_i.COD_MOD=padweb_i.COD_MOD.astype(int)
    padweb_i.CODOOII=padweb_i.CODOOII.astype(int)
    padweb_i.ANEXO=padweb_i.ANEXO.astype(int)

    padweb_i.loc[(padweb_i['CODLOCAL'] == ''),'CODLOCAL'] = '0'

    padweb_i.CODLOCAL=padweb_i.CODLOCAL.astype(int)

    # Renombrar variables

    padweb_i.rename(columns={'COD_MOD':'cod_mod'},inplace=True)
    padweb_i.rename(columns={'CODOOII':'cod_ugel'},inplace=True)
    padweb_i.rename(columns={'CODLOCAL':'cod_local'},inplace=True)
    padweb_i.rename(columns={'ANEXO':'anexo'},inplace=True)
    padweb_i.rename(columns={'CEN_EDU':'nombre_iiee'},inplace=True)
    padweb_i.rename(columns={'D_NIV_MOD':'nivel'},inplace=True)
    padweb_i.rename(columns={'TALUMNO':'total_alumnos'},inplace=True)
    padweb_i.rename(columns={'TDOCENTE':'total_docentes'},inplace=True)

    # Combinar bases

    dire_padweb=pd.merge(dire, padweb_i, on =['cod_mod','anexo'], how ='left',indicator=True)

    # Variables de interés

    bint=dire_padweb[['cod_mod','anexo','cod_local','cod_ugel','nombre_iiee','nivel','total_alumnos','total_docentes','_merge']]

    return bint
