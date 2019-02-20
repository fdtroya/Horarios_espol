import random as rd
import Config as cfg

def find_index(materia,genes):
    for gen_in in range(len(genes)):
        gen=genes[gen_in]
        mat=gen.split("-")[0]
        if mat == materia:
            return gen_in



def create_genotype(individual):
    ls=[]
    dias=list(individual.keys())
    for dia in dias :
        materias=list(individual[dia].keys())
        for materia in materias:
            if materia not in ls:
                ls.append(materia)       
    return ls

def mutation(genotype,dic,rate=cfg.mutation_rate):
    number_rand=rd.uniform(0,1)
    if rate>=number_rand:
        tipo="P"
        while tipo =="P":
            materia_ind=rd.randint(0,len(genotype)-1)
            materia_data=genotype[materia_ind]
            info=materia_data.split("-")
            tipo=info[1]
            if tipo =="T":
                materia=info[0]
                paralelos=list(dic[materia].keys())
                paralelo_t=rd.choice(paralelos)
                
            
                paralelos_p=dic[materia][paralelo_t]["Horario"]["-P-"]
                if len(paralelos_p) >0:
                    paralelo_p=rd.randint(0,len(paralelos_p)-1)
                else:
                    paralelo_p="n"
                key_p=materia + "-" + "P"+"-"+ str(paralelo_t) +"-"+str(paralelo_p)
                key_t = materia + "-" + "T"+"-"+ str(paralelo_t) +"-"+str(paralelo_p)
        to_change=get_indexes_to_change(genotype,materia)
        genotype[to_change[0]]=key_t
        if paralelo_p !="n":
            genotype[to_change[1]]=key_p    

       
    return genotype

def phenotype(genotype,dic):
    genotype=mutation(genotype,dic)
    horario = {}
    horario[0] = {}
    horario[1] = {}
    horario[2] = {}
    horario[3] = {}
    horario[4] = {}
    for char in genotype:
        data=char.split("-")
        materia=data[0]
        tipo=data[1]
        
        if tipo =="T":
            paralelo_t=data[2]
            for clase in dic[materia][paralelo_t]["Horario"]["-T-"]:
                dia=int(clase[0])
                horas=clase[1]
                horario[dia][char]=horas
        elif tipo=="P":
            paralelo_p=data[3]
            paralelo_t=data[2]
            if paralelo_p !="n":
                dia=dic[materia][paralelo_t]["Horario"]["-P-"][int(paralelo_p)][0]
                horas_pract=dic[materia][paralelo_t]["Horario"]["-P-"][int(paralelo_p)][1]
                horario[dia][char]=horas_pract
    return horario

def crossover(genotype1,genotype2):
    materias=get_materias(genotype1)
    cant=len(materias)//2
    a_cambiar=[]
    tom=0
    while cant>tom:
        n_materia=rd.choice(materias)
        if n_materia not in a_cambiar:
            a_cambiar.append(n_materia)
            tom+=1
    for materia in a_cambiar:
        ind_t_gntp1,ind_p_gntp1=get_indexes_to_change(genotype1,materia)
        ind_t_gntp2,ind_p_gntp2=get_indexes_to_change(genotype2,materia)
        genotype1[ind_t_gntp1]=genotype2[ind_t_gntp2]
        if ind_p_gntp1 !="n":
            genotype1[ind_p_gntp1]=genotype2[ind_p_gntp2]
        
    return genotype1
def crossover2(genotype1,genotype2,dic_horarios):#experimental no funciona muy bien :c
    dias=range(0,5)
    dia_a_cambiar=rd.choice(dias)
    materias=get_materias_dia(dia_a_cambiar,genotype1,dic_horarios)
    for materia in materias:
        ind_t_gntp1,ind_p_gntp1=get_indexes_to_change(genotype1,materia)
        ind_t_gntp2,ind_p_gntp2=get_indexes_to_change(genotype2,materia)
        genotype1[ind_t_gntp1]=genotype2[ind_t_gntp2]
        if ind_p_gntp1 !="n":
            genotype1[ind_p_gntp1]=genotype2[ind_p_gntp2]
        
    return genotype1
    

def mating(partners_list,dic_horaios,cant):
    new_pool=[]
    for partners in partners_list:
        partner1=partners[0]
        partner2=partners[1]
        genotype1=create_genotype(partner1)
        genotype2=create_genotype(partner2)

        offspring=crossover(genotype1,genotype2)
        result=phenotype(offspring,dic_horaios)
        new_pool.append(result)
    return new_pool

def get_indexes_to_change(genotype,materia):
    t=""
    p="n"
    for i in range(len(genotype)):
        mat=genotype[i].split("-")[0]
        tipo=genotype[i].split("-")[1]
        if mat == materia:
            if tipo=="T":
                t=i
            else:
                p=i
    return t,p


def get_materias(genotype):
    mat=[]
    for gen in genotype:
        materia=gen.split("-")[0]
        if materia not in mat:
            mat.append(materia)
    return mat

def get_materias_dia(dia,genotype,dic_horarios):
    materias=[]
    for gen in genotype:
        info=gen.split("-")
        materia=info[0]
        paralelo=info[2]
        tipo=info[1]
        if tipo =="T":
            dias_info=dic_horarios[materia][paralelo]["Horario"]["-T-"]
            dias=[]
            for horario in dias_info:
                dias.append(horario[0])
            if dia in dias:
                if materia not in materias:
                    materias.append(materia)
    return materias

