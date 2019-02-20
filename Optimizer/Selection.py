import Fitness
import random as rd
import numpy as np

def pick_one(probs,pool):
    index=0
    r=rd.uniform(0,1)
    while r>0:
        r=r-probs[index]
        index+=1
    index-=1
    return  pool[index]



def selection(pool,dic_notas,dic_horarios):
    values=[]
    probs=[]
    for horario in pool:
        value=Fitness.schdl_value(horario,dic_notas,dic_horarios)
        values.append(value)
    values=(np.array(displace_values(values))+0.001).tolist()
    tot_val=sum(values)
    for value in values:
        prob=value/tot_val
        probs.append(prob)
    rd_indv=pick_one(probs,pool)
    return rd_indv
def fitness_info(pool,dic_notas,dic_horarios):
    values=[]
    teacher_values=[]
    gap_values=[]
    conflicts=[]
    dishomogen_values=[]
    for horario in pool:
        value,teacher_value,gap_value,conflict,dishom=get_inf_ind(horario,dic_notas,dic_horarios)
        values.append(value)
        teacher_values.append(teacher_value)
        gap_values.append(gap_value)
        conflicts.append(conflict)
        dishomogen_values.append(dishom)
    values=np.array(values)
    max_fit=np.max(values)
    best_indv=pool[np.argmax(values)]
    mean_fitness=np.mean(values)
    max_tv,mean_tv=get_stats(teacher_values)
    max_gap,mean_gap=get_stats(gap_values)
    max_conflicts,mean_conflicts=get_stats(conflicts)
    max_dis,mean_dis=get_stats(dishomogen_values)
    data=(max_fit,mean_fitness,max_tv,mean_tv,max_gap,mean_gap,max_conflicts,mean_conflicts,max_dis,mean_dis,best_indv)
    return data
def selec_partners(pool,dic_notas,dic_horaios):
    cant=len(pool)
    partners=[]
    while len(partners)<cant:
        individual1=selection(pool,dic_notas,dic_horaios)
        pool.remove(individual1)

        individual2=selection(pool,dic_notas,dic_horaios)
        pool.append(individual1)
        partners.append((individual1,individual2))
    return partners


def displace_values(values_old):
    val=np.array(values_old)
    min=np.min(val)
    new_val=val-min
    return new_val.tolist()

def get_inf_ind(horario,dic_notas,dic_horarios):
    value = Fitness.schdl_value(horario, dic_notas, dic_horarios)
    teacher_value = Fitness.schedule_teacher_score(horario, dic_notas, dic_horarios)
    closeness = Fitness.closeness_score(horario)
    gap_value = closeness[0]
    conflict = closeness[1]
    dishom = -Fitness.dis_homogen_score(horario)
    return value,teacher_value,gap_value,conflict,dishom

def get_stats(list):
    list=np.array(list)
    mean=np.mean(list)
    max=np.max(list)
    return mean,max

