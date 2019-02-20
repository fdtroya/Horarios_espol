import random as rd
def gen_random_population(dic,number):
    population=[]
    for individual in range(number):
        horario={}
        horario[0]={}
        horario[1] = {}
        horario[2] = {}
        horario[3] = {}
        horario[4] = {}

        for materia in dic.keys():
            paralelos=list(dic[materia].keys())
            paralelo_t=rd.choice(paralelos)
            horario_t=dic[materia][paralelo_t]["Horario"]["-T-"]

            horarios_p = dic[materia][paralelo_t]["Horario"]["-P-"]

            if len(horarios_p)>0:

                paralelo_p=rd.randint(0,len(horarios_p)-1)
                horario_p=horarios_p[paralelo_p]
            else:
                paralelo_p="n"
                horario_p=[]
            key_t = materia + "-" + "T"+"-"+ str(paralelo_t) +"-"+str(paralelo_p)
            key_p=materia + "-" + "P"+"-"+ str(paralelo_t) +"-"+str(paralelo_p)



            for clase_t in horario_t:
                dia=clase_t[0]

                horario[dia][key_t]=clase_t[1]

            if paralelo_p !="n":
                dia=horario_p[0]
                horario[dia][key_p] = horario_p[1]
        population.append(horario)
    return population
