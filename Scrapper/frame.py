
from bs4 import BeautifulSoup
import scrapper as sc
from navigation import busc_profesor
from basic_func import  get_teachers_list
from basic_func import en_2
def consulta_materia(browser,materia):
    registros = browser.find_element_by_link_text("REGISTROS")
    registros.click()

    consultar = browser.find_element_by_xpath('//*[@id="ctl00_contenido_btnConsultar"]')
    consultar.click()

    browser.find_element_by_xpath('//*[@id="ctl00_contenido_RBList_1"]').click()

    entrada_mat=browser.find_element_by_xpath('//*[@id="ctl00_contenido_codigoMateria"]')
    
    entrada_mat.send_keys(materia)
    browser.find_element_by_xpath('//*[@id="ctl00_contenido_Button2"]').click()
    soup=BeautifulSoup(browser.page_source,'lxml')
    links_object=soup.find_all('a',{"class":"myLink"})
    par_link={}
    url_base="https://www.academico.espol.edu.ec/UI/Registros/"
    for href in links_object:
        ref=str(href.get("href"))
        paralelo=int(ref.split("&")[1].split("=")[-1])
        par_link[paralelo]=(url_base+ref)
    par_horario={}
    for paralelo in par_link.keys():
        link=par_link[paralelo]
        browser.get(link)
        a = 0
        while en_2(browser):

            if a / 1000 - a // 1000 == float(0):
                print(5 * "-" + "INGRESE CAPTCHA" + "-" * 5)
            a += 1
        page=browser.page_source
        scrap_prac=sc.scrap_horario(page,'table',{"class": "display", "style": "width:100%;border-collapse:collapse;background-color:#FFFFFF;border-style:solid; border-width:1px;border-color:#D9d9d9"})
        scrap_teo=sc.scrap_horario(page,'table',{"class":"display","id":"ctl00_contenido_TableHorarios"})
        profesor=scrap_teo[1]
        horario_prac=sc.pros_horario(scrap_prac[0])
        horario_teo=sc.pros_horario(scrap_teo[0])
        par_horario[paralelo]={}
        par_horario[paralelo]["Horario"]={}
        par_horario[paralelo]["Horario"]["-T-"]=horario_teo
        par_horario[paralelo]["Horario"]["-P-"]=horario_prac
        par_horario[paralelo]["Profesor"]=profesor

    return(par_horario)


def consulta_nota(browser,diccionario):
    dic={}
    cenacad = r"https://cenacad.espol.edu.ec/index.php/module/Report/action/Profesores"
    for materia in list(diccionario.keys()):
        dic[materia]={}
        for profesor in get_teachers_list(diccionario[materia]):
            browser.get(cenacad)

            browser=busc_profesor(browser,profesor)
            page = browser.page_source
            link=sc.find_name(page,profesor)
            notas=sc.get_data(link,materia)
            dic[materia][profesor]=notas
    return dic








