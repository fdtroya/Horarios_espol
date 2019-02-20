from selenium import webdriver
from navigation import busc_profesor
import scrapper as sc 


path=r"D:\OneDrive - Escuela Superior Politécnica del Litoral\ESPOL\Programacion\Python\Proyectos\Horarios\Scrapper\chromedriver.exe"#editar path del chromedriver selenium
browser = webdriver.Chrome(path)

cenacad = r"https://cenacad.espol.edu.ec/index.php/module/Report/action/Profesores"
browser.get(cenacad)
profesor="ESCALA BENITES FRANCESCA ELIZABETH"
materia="QUIG1001"
browser=busc_profesor(browser,profesor)
page = browser.page_source
link=sc.find_name(page,profesor)
notas=sc.get_data(link,materia)
print(notas)
