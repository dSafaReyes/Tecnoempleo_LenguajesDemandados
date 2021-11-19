import Tecnoempleo_Metodos as metodos
from openpyxl import Workbook

if __name__ == '__main__':

    # En próximas versiones el usuario podrá introducir por consola el nombre del puesto a buscar
    # empleo = metodos.txt_url(input("Introduzca el empleo sobre el que desea realizar el análisis: "))

    # Tecno empleo almacena información sobre las 50 provincias españolas (+2 ciudades autónomas):
    n_ciudades = range(231, 231+52)
    empleo = "desarrollador+web"
    # Crearemos un diccionario con la cantidad de ofertas por ciudad y otro donde aparezca la demanda de cada lenguaje
    # en x ciudad. Cabe destacar que este segundo diccionario tendrá una clave ciudad y otro diccionario como valor
    dic_ofertas = {}
    dic_lenguajes = {}

    for n in n_ciudades:

        # Adaptamos la url para cadad ciudad
        url_ciudad = f"https://www.tecnoempleo.com/busqueda-empleo.php?te={empleo}&pr=,{n},&pagina=1"
        # En la etiqueta h1 se encuentra almacenada información acerca de la ciudad y número de ofertas
        title = metodos.get_tag_content(url_ciudad, "h1", "h4 h5-xs py-4 text-center")[0]

        # En caso de obtener error el bucle finaliza
        if title == "N": break

        # Almacenamos como variables la ciudad, el número de ofertas y el números de páginas asociadas a cada ciudad
        ciudad, n_ofertas, n_paginas = metodos.get_ciudad_ofertas_paginas(title)
        dic_ofertas[ciudad] = n_ofertas
        # Creamos una lista de urls (páginas) para cada ciudad
        lista_paginas = [url_ciudad[:-1] + str(pag) for pag in range(1, n_paginas+1)]

        # Creamos una lista donde almacenaremos todos los lenguajes demandados
        lista_lenguajes = []
        for url_pg in lista_paginas:

            # Obtenemos la lista de de lenguajes de cada página
            lista = metodos.get_tag_content(url_pg, "a", "badge-pill badge-soft badge-primary text-primary text-warning-hover py-1 px-2 fs--13 mr-1")
            # Añadimos la lista obtenida a la lista acumulada
            lista_lenguajes += [element.text.upper() for element in lista]

        # Transformamos la lista de todos los lenguajes en un diccionario que recuente la cantidad de veces que se solicita
        dic_lenguajes[ciudad] = metodos.contador(lista_lenguajes)

    # Instanciamos un objeto Workbook
    wb = Workbook()
    ws = wb.active

    # Guardamos el primer diccionario en una hoja de excel
    ws = metodos.dict_to_excel("N_Ofertas", wb, dic_ofertas)
    # Guardamos los diccionario dentro del segundo diccionario en distintas hojas de excel
    for ciudad in dic_lenguajes:
        ws = metodos.dict_to_excel(f"{ciudad}", wb, dic_lenguajes[ciudad])

    wb.save(f'LenguajesMasDemandados_{empleo}.xlsx')
