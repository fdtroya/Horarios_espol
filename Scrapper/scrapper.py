from bs4 import BeautifulSoup
import basic_func as bf
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrap_horario(page,name,atributes):
    soup_ob = BeautifulSoup(page, 'lxml')
    profesor = soup_ob.find('span', attrs={"id": "ctl00_contenido_LabelProfesor"}).text
    tables = soup_ob.findAll(name, atributes)
    horario = []
    for table in tables:
        for i in range(len(table.findAll('td'))):
            tabla_el = table.findAll('td')[i].text.strip()
            if tabla_el != '\n':
                horario.append(tabla_el)
    return horario,profesor


def pros_horario(horario):
    dias=["Lunes","Martes","Miércoles","Jueves","Viernes"]
    horarios_proc=[]
    for i in range(len(horario)):
        if bf.en_espacios(0,i,5):
            dia=dias.index(horario[i])
        elif bf.en_espacios(1,i,5):
            hora_in=bf.time_convert(horario[i])
        elif bf.en_espacios(2,i,5):
            hora_fin=bf.time_convert(horario[i])
        elif  bf.en_espacios(3,i,5):
            horarios_proc.append((dia,(hora_in,hora_fin)))
    return horarios_proc

def find_name(page,name):
    url_base="https://www.cenacad.espol.edu.ec"
    link=""

    while len(link)==0:
        soup_obj=BeautifulSoup(page,'lxml')


        table=soup_obj.find('table',attrs={'style':"width:100%;", 'cellpadding':"1", 'cellspacing':"1" ,'class':'tbl'})

        table_rows=table.findAll('tr')
        data_rows=table_rows[1:]
        for row in data_rows:
            elements=row.findAll('td')
            apellidos=elements[1].text.strip()
            nombres=elements[2].text.strip()
            profesor=apellidos+nombres
            if bf.similitud(profesor,name,80):
                link_obj=elements[3].find('a')
                ref = str(link_obj.get("href"))
                link=url_base+ref
                return link
        sig=siguiente(soup_obj)[1]
        page=requests.get(sig,verify=False).text

def get_data(link,materia):
    notas=[]
    sig=True
    while sig:
        
        page=requests.get(link,verify=False)
        soup_obj=BeautifulSoup(page.text,'lxml')
        table = soup_obj.find('table', attrs={"style":"width:100%;", "cellpadding":"1", "cellspacing":"1", "class":"tbl"})
        table_rows=table.findAll('tr')
        data_rows=table_rows[1:]
        for row in data_rows:
            data=row.findAll('td')
            materia_cod=data[3].text
            if materia==materia_cod:
                nota=float(data[6].text)
                notas.append(nota)
        next=siguiente(soup_obj)
        sig=next[0]
        link=next[1]


    return notas

def siguiente(soup):
    links=soup.findAll('a')
    for link in links:
        if link.text == 'Siguiente':
            url_base = "https://www.cenacad.espol.edu.ec"
            ref=str(link.get('href'))
            url=url_base+ref
            return True,url
    return False,"----"
