import json as js
import numpy as np
import Config as cfg
import Crossover
import Initialice
import Selection
import Analyze  as an
from Fitness import closeness_score
from Fitness import schdl_value
def gen_report(population,dic_notas,dic_horarios):
    dones=[]
    for individual in population:
        if individual not in dones:
            if int(closeness_score(individual)[1])==0:
                gen_report_individual(individual,dic_notas,dic_horarios)
            print("#"*50)
            dones.append(individual)

def gen_report_individual(individual,dic_notas,dic_horarios):
    dataframe=an.create_dataframe(individual)
    print(dataframe)
    score=schdl_value(individual,dic_notas,dic_horarios)
    print("VALOR: "+str(score))
    genotype=Crossover.create_genotype(individual)
    materias=[]
    for gen in genotype:
        info=gen.split("-")
        materia=info[0]
        if materia not in materias:
            paralelo=info[2]
            profesor=dic_horarios[materia][str(paralelo)]["Profesor"]
            rank=get_rank(profesor,materia,dic_notas)
            nota=np.mean(np.array(dic_notas[materia][profesor]))
            print("MATERIA: "+materia)
            print("PROFESOR: "+profesor)
            print("RANGO: "+str(rank))
            print("NOTA: "+str(nota))
            print("▀"*30)    
            materias.append(materia)           





def get_rank(profesor,materia,dic_notas):
    promedios=[]  
    promedio_profesor=np.mean(np.array(dic_notas[str(materia)][profesor]))
    for notas in dic_notas[str(materia)].values():
        notas=np.array(notas)
        promedio=np.mean(notas)
        promedios.append(promedio)
    pos =1
    for prom in promedios:
        if promedio_profesor < prom:
            pos+=1
    return pos 













info_dir = r"D:\optimice_info.csv" #Cambier directorio del csv de info (no es un archivo necesario)
ar = open(info_dir, "w")
ar.write("")
ar.close()

#######################################################################################
horarios_path = (
    r'D:\horarios.json')          #Cambiar directorio del json de horaios
notas_path = r'D:\notas.json'      #Cambiar directorio del json de notas
#################################
alltime_best_inidvidual = ""
alltime_best_score = -100
#################################

with open(horarios_path) as hr:
    dic_horarios = js.load(hr)

with open(notas_path) as nt:
    dic_notas = js.load(nt)
################################################################################
population_1 = Initialice.gen_random_population(
    dic_horarios, cfg.population_size)
prev_pop = population_1
cant_mat = len(dic_horarios.keys())

for i in range(cfg.amount_of_generations):

    print("generacion "+str(i))
    partners = Selection.selec_partners(prev_pop, dic_notas, dic_horarios)
    new_pop = Crossover.mating(partners, dic_horarios, cant_mat)
    prev_pop = new_pop
##############################################################################

    fitness_in = Selection.fitness_info(prev_pop, dic_notas, dic_horarios)
#############################################################################
    best_fit, mean_fit, max_tv, mean_tv, max_gap, mean_gap, max_conflicts, mean_conflicts, max_dis, mean_dis, best_indv = fitness_in
    strng = ""
    for element in fitness_in[:-1]:
        strng = strng+str(element)+","
    fina_strng = str(i)+","+strng[:-1]+"\n"
    ar = open(info_dir, "a+")  
    ar.write(fina_strng)
    ar.close()
    if best_fit > alltime_best_score:
        alltime_best_inidvidual = best_indv
        alltime_best_score = best_fit

    print("Best fitness= "+str(best_fit))
    print("Mean fitness= "+str(mean_fit))
gen_report(prev_pop,dic_notas,dic_horarios)

print("\n")
print("Best"+"▀"*30)
gen_report_individual(alltime_best_inidvidual,dic_notas,dic_horarios)


