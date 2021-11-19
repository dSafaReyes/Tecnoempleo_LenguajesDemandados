import requests
from bs4 import BeautifulSoup

def get_tag_content(url, tag, class_name):
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.content, "html.parser")
        return soup.find_all(f"{tag}", class_=f"{class_name}")
    else:
        return "No se ha podido obtener respuesta de la página. Excel creado en blanco."

def lista_palabras(txt):
    ''' Elimina todos los espacios de un string. Devuelve una lista con cada palabra '''
    lista_palabras = txt.split()
    lista_sin_espacios = list(filter(None, lista_palabras))
    return lista_sin_espacios

def redondear_arriba(num):
    ''' Deuelve el número redondeado
        a la siguiente unidad '''
    return round(num+0.5)

def get_ciudad_ofertas_paginas(string):
    ''' Recibe el contenido en h1, separa cada palabra en un elemento de la lista y devuelve de ella la ciudad,
        el número de ofertas y las páginas que tiene asociada dicha ciudad (en cada página caben 30 ofertas) '''
    lista_palabras_title = lista_palabras(string.text)
    n_ofertas = int(lista_palabras_title[0])
    ciudad = lista_palabras_title[-1]
    n_paginas = redondear_arriba(n_ofertas/30)
    return ciudad, n_ofertas, n_paginas

def contador(lista):
    ''' A partir de una lista creamos un diccionario doned se recuente la cantidad de veces que se repitan los elementos
        de dicha lista '''
    set_lista = set(lista)
    dic = {i:lista.count(i) for i in set_lista}
    return dic

def txt_url(string):
    ''' Transforma el input del usuario texto para introducir en la url'''
    return string.lower().replace(" ", "+")

def dict_to_excel(sheet, wb, dic, r=1, c=1):
    ''' Almacenamos un diccionario en una hoja de excel. La primera columna será la clave y la segunda el valor.
        Podemos introducir también a partir de qué columna o fila queremos escribir dicho diccionario. '''
    ws = wb.create_sheet(sheet)
    for i, (k, v) in enumerate(dic.items()):
        ws.cell(row=i+r, column=c, value=k)
        ws.cell(row=i+r, column=c+1, value=v)
    return ws