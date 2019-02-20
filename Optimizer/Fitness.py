import numpy as np
import Config as cfg


def teacher_value(prof,subject,dic):
    prof_grades=np.array(dic[subject][prof])
    if len(prof_grades)!=0:
        prof_grades = prof_grades[np.logical_not(np.isnan(prof_grades))]
        prom=np.mean(prof_grades)

    avrgs=[]
    for professor in dic[subject].keys():
        notas=np.array(dic[subject][professor])
        notas=notas[np.logical_not(np.isnan(notas))]
        avrg=np.mean(notas)
        avrgs.append(avrg)
    avrgs=np.array(avrgs)
    avrgs = avrgs[np.logical_not(np.isnan(avrgs))]
    mean=np.mean(avrgs)
    if len(prof_grades)==0:
        prom=mean
    std=np.std(np.array([mean,prom]))

    value=(prom-mean)*std
    return value


def schedule_teacher_score(horario,dic_notas,dic_horarios):
    values=[]
    for day in horario.keys():
        for subject in horario[day].keys():
            inform=cfg.inf_from_key(subject)########function to get keys from subject
            materia=inform[0]
            paralelo=str(inform[1])
            profesor=dic_horarios[materia][paralelo]["Profesor"]
            value=teacher_value(profesor,materia,dic_notas)
            values.append(value)
    values=np.array(values)
    values = values[np.logical_not(np.isnan(values))]
    mean_value=np.mean(values)
    var=np.std(values)#
    val2=""
    if mean_value <0:
        val2=-mean_value
    else:
        val2=mean_value
    return (mean_value/var)*val2 
    #return mean_value



def dis_homogen_score(horario):
    cant_materias_pd=[]
    for day in horario.keys():
        cant_materias_pd.append(len(horario[day].keys()))
    cant_materias_pd=np.array(cant_materias_pd)
    std=np.std(cant_materias_pd)
    return -std

def takeFirst(elem):
    return elem[0]

def sort_horario(horario_dia):
    nt=list(horario_dia.values())
    nt.sort(key=takeFirst)
    return nt





def closeness_score(horario):###editar
    scores=[]
    daily_conflicts=[]
    for day in horario.keys():
        schdle_sorted=sort_horario((horario[day]))
        gaps=[]
        conflicts=[]
        for horas_ind in range(len(schdle_sorted)-1):
            hora_fin=schdle_sorted[horas_ind][1]
            hora_in=schdle_sorted[horas_ind+1][0]
            gap=hora_in-hora_fin
            if gap>=0:
                gaps.append(gap)
            else:
                conflicts.append(-gap)
        if len(gaps)==0:
            gaps.append(0)
        if len(conflicts)==0:
            conflicts.append(0)
        gaps=np.array(gaps)
        gaps=gaps[np.logical_not(np.isnan(gaps))]
        mean_gap=np.mean(gaps)
        total_conflict=np.sum(np.array(conflicts))
        scores.append(-mean_gap)
        daily_conflicts.append(total_conflict)
    scores=np.array(scores)
    total_conflicts=np.sum(np.array(daily_conflicts))
    mean_score=np.mean(scores)
    return -mean_score,total_conflicts



def schdl_value(horario,dic_notas,dic_horarios):#editar

    professors=schedule_teacher_score(horario,dic_notas,dic_horarios)*cfg.Teacher_importance
    dis_hom=dis_homogen_score(horario)*cfg.Dishomogen_importance
    closeness_sc=closeness_score(horario)
    gap=cfg.gap_multiplier*closeness_sc[0]
    conflic=cfg.conflict_multiplier*closeness_sc[1]
    grade=professors+dis_hom
    if professors<0 and grade <0:
        professors=-professors
    value= (professors)*(grade)/((gap+1)*((conflic)+1))#(professors)*(grade)/((gap+1)*(conflic+1))

    return value






