#FITNESS VALUES
###################
Teacher_importance=1
Dishomogen_importance=4


conflict_multiplier=1
gap_multiplier=0.8
base=1000
##################
#CROSSOVER VALUES
#######################
mutation_rate=0.1
population_size=45
amount_of_generations=45

def inf_from_key(key):
    inf=key.split("-")
    materia=inf[0]
    par=inf[2]
    prac=inf[3]
    if prac !="n":
        prac=int(prac)
    return materia,par,prac