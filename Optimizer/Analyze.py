import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import sys

from Selection import get_inf_ind

def create_barchart(schedule,dic_notas,dic_horarios):

    value, teacher_value, gap_value, conflict, dishom=get_inf_ind(schedule,dic_notas,dic_horarios)

    dic={"Label":["Valor de profesores","Espacio entre materias","Varianza de Materias"],"Value":[teacher_value,gap_value,dishom]}
    dataframe=pd.DataFrame(dic)
    graf=sns.barplot(x="Label",y="Value",data=dataframe,hue="Label")
    graf.set_title("Analisis")
    graf.set_xlabel("Caracteristicas")
    graf.set_ylabel("Valor")
    plt.show()

def create_dataframe(schedule):
    dias={0:"Lunes",1:"Martes",2:"Miercoles",3:"Jueves",4:"Viernes"}
    new_dic={"Lunes":[],"Martes":[],"Miercoles":[],"Jueves":[],"Viernes":[]}
    for dia in schedule.keys():
        horario=["-"]*22
        materias=schedule[dia]
        for materia in materias.keys():
            horas=materias[materia]
            hora_in=horas[0]
            hora_fin=horas[1]
            pos_ini=int((hora_in-7.5)*2)
            pos_fin=int((hora_fin-7.5)*2)
            for i in range(pos_ini,pos_fin):
                horario[i]=materia
        dia_letras=dias[dia]
        new_dic[dia_letras]=horario
    horas=[]
    for hora in range(15,37):
        numero=hora/2
        numero=round(numero,1)
        horas.append(numero)
    dataframe=pd.DataFrame(data=new_dic,index=horas,columns=list(new_dic.keys()))
    return dataframe



    
    





