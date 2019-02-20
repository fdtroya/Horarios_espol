import jellyfish


def time_convert(time):
    horas,minutos,segundos=time.split(":")
    tiempo=int(horas)+(int(minutos)/60)+(int(segundos)/3600)
    return tiempo


def en_espacios(inicial,posicion,saltos):
    return(posicion-inicial)/saltos - (posicion-inicial)//saltos == float(0)

def en_2(browser):
    try:
        numb=browser.find_element_by_xpath('//*[@id="ctl00_contenido_ValidateCaptchaButton"]')
        return True
    except:
        return False



def en(name,browser):


    try:
        numb=browser.find_element_by_link_text(name)
        return True
    except:
        return False


def similitud(nombre1,profesor,threshold):
    nombre1=nombre1.upper().replace(" ","")
    profesor=profesor.upper().replace(" ","")
    sim=jellyfish.jaro_distance(nombre1,profesor)
    threshold=threshold/100
    if sim>=threshold:
        return True
    else:
        return False

def get_teachers_list(dictionary_courses):
    lista=[]
    for paralelo in dictionary_courses.keys():
        profesor=dictionary_courses[paralelo]["Profesor"]
        if profesor not in lista:
            lista.append(profesor)
    return lista