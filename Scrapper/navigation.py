import time


from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains

from basic_func import en


def ingreso(usuario,contrasenia,browser):
    url=r"https://www.academico.espol.edu.ec/login.aspx?ReturnUrl=%2fUI%2fInformacionAcademica%2finformaciongeneral.aspx"

    browser.get(url)
    usuario_in= browser.find_element_by_name("ctl00$contenido$txtuser")
    siguiente=browser.find_element_by_name("ctl00$contenido$btnSigte")
    usuario_in.send_keys(usuario)
    siguiente.click()
    contrasenia_in=browser.find_element_by_name("ctl00$contenido$txtpsw")
    contrasenia_in.send_keys(contrasenia)
    a=0
    while not en("REGISTROS",browser ) :
        if a/1000 - a//1000 == float(0):
            print(5*"-"+"INGRESE CAPTCHA"+"-"*5)
        a+=1
    print(5*"-"+"CAPTCHA INGRESADO"+5*"-")
        
    cerrar_imagen(browser)

    return browser

    
def cerrar_imagen(browser):
    
    try:
        x=browser.find_element_by_xpath('//*[@id="myModal"]/div/div/div[1]/button')
        time.sleep(1)
        ac = ActionChains(browser)
        
        ac.move_to_element(x).click().perform()
        time.sleep(1)
        time.sleep(1)
    except:
        time.sleep(0.5)

def busc_profesor(browser,profesor):
    busqueda=browser.find_element_by_xpath('//*[@id="right"]/div[2]/table/tbody/tr[3]/td/form/table/tbody/tr/td/table/tbody/tr/td/p/input[1]')
    busqueda.send_keys(profesor)
    enter=browser.find_element_by_xpath('//*[@id="right"]/div[2]/table/tbody/tr[3]/td/form/table/tbody/tr/td/table/tbody/tr/td/p/input[2]')
    enter.click()
    return browser
