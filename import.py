#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
import socks
import socket
from cookielib import CookieJar
import csv


socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, "127.0.0.1", 9050)
socket.socket = socks.socksocket

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

domain = "http://201.175.44.214/SNRSPD/Basica"

url = "%s/SNRSPDresultadosbasica/ConsultaPublica.aspx" % domain

r1 = opener.open(url)
rs1 = BeautifulSoup(r1.read(), 'html.parser')


def getValues(variable):

    input = rs1.find(
        'input', {'id': variable}
    )

    return input['value']


def generateParams():

    values = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '%s' % getValues('__VIEWSTATE'),
        '__VIEWSTATEGENERATOR': 'BF31ECFA',
        '__EVENTVALIDATION': '%s' % getValues('__EVENTVALIDATION'),
        'btnconsultar': 'Consultar'
    }

    return values


def getTiposEvaluacion():

    tipos = []

    for tipo in rs1.find(
            'select', {'id': 'ddlExamen'}
                ).find_all('option'):
        if tipo['value'].isdigit():
                tipos.append([tipo['value'], tipo['text']])

    return tipos


def getResult():

    tipos_evaluacion = getTiposEvaluacion()

    filename = "resultados.csv"
    resultados = open('%s' % filename, 'wb')
    writer = csv.writer(resultados,
                        delimiter=',',
                        quotechar='"',
                        quoting=csv.QUOTE_ALL)

    #Escribimos las cabeceras de nuestro documento
    writer.writerow([
        'idEntidad', 'idConvocatoria', 'idTipoEvaluacion',
        'Evaluacion', 'Posición en lista de prelación',
        'Folio del sustentante', 'Grupo de desempeño',
        'Nivel de desempeño',
        'Puntuación total del instrumento de evaluación',
        'Puntuación en el área Intervención didáctica',
        'Puntuación en el área Aspectos curriculares',
        'Nivel de desempeño',
        'Puntuación total del instrumento de evaluación',
        'Puntuación en el área Compromiso ético',
        'Puntuación en el área Mejora profesional',
        'Puntuación en el área Gestión escolar y vinculación con la comunidad'
    ]
    )

    #Iterando entre entidades
    for entidad in range(1, 33):
        #Iterando entre tipos de convocatoria
        # 1: Pública y Abierta
        # 2: Egresados de Normales
        mensaje = "Descargado: Entidad: %s" % entidad
        for convocatoria in range(1, 3):
            mensaje = mensaje + " Convocatoria: %s " % convocatoria
            #Iterando en tipos de evaluación
            for (idtipo,tipo) in tipos_evaluacion:

                #Completamos los parametros para consultar la página
                values = generateParams()
                values['ddlEntidad'] = entidad
                values['ddlConvocatoria'] = convocatoria
                values['ddlExamen'] = idtipo

                #Enviando los parametros para la consulta, vía POST
                data = urllib.urlencode(values)
                html = opener.open(url, data).read()
                parser = BeautifulSoup(html, 'html.parser')
                table = parser.find('table', {'id': 'gvResultadosEvaluacion2'})

                if table is not None:
                    for rows in table.findAll('tr'):
                        registro = []
                        registro.append(entidad)
                        registro.append(convocatoria)
                        registro.append(idtipo)
                        registro.append(tipo)
                        for cell in rows.findAll('td'):
                            registro.append(cell.getText().encode('utf-8'))
                        writer.writerow(registro)
                    mensaje + " Evaluacion: %s" % tipo


if __name__ == '__main__':

    #Ejecutamos para ver los resultados
    #Los resultados se guardaran en el archivo resultados.csv
    getResult()
