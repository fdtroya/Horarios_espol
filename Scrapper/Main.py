from navigation import ingreso
import frame as fr
from selenium import webdriver
import getpass
import json


horarios_path=r'D:\OneDrive - Escuela Superior Politécnica del Litoral\ESPOL\Programacion\Python\Proyectos\Horarios\Results\horarios.json' #editar Directorio del json de horarios
################################

usuario=input("Ingrese su Usuario...        -")
contrasenia=getpass.getpass("Ingrese su Contraseña...     -")
materias=input("Ingrese los Codigos de las Materias separados por (,)       -").upper().split(",")
#################################
path=r"D:\OneDrive - Escuela Superior Politécnica del Litoral\ESPOL\Programacion\Python\Proyectos\Horarios\Scrapper\chromedriver.exe"#editar path del chromedriver selenium
browser = webdriver.Chrome(path)

#######################################################################################


browser=ingreso(usuario,contrasenia,browser)

horarios={}

for materia in materias:


    horarios[materia]=fr.consulta_materia(browser,materia)

with open(horarios_path,"w+") as hr:#editar path del json
    json.dump(horarios, hr)



if len(horarios)==0:
    with open(horarios_path) as hr:
        horarios = json.load(hr)

notas=fr.consulta_nota(browser,horarios)
with open(r'D:\OneDrive - Escuela Superior Politécnica del Litoral\ESPOL\Programacion\Python\Proyectos\Horarios\Results\notas.json',"w+") as nt:#editar path del json de notas
    json.dump(notas, nt)




exit()