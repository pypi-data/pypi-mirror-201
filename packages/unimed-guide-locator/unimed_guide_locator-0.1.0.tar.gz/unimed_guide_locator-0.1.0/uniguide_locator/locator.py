from datetime import datetime, timedelta
from turtle import delay
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class GuideLocator:
    """Locator for Guias Unimed and Intermed"""
    
    def __init__(self):
        pass
        
    def status(num_guias, username, password):
        
        data_guias = []

        # hoje = datetime.now()

        # dias_30 = timedelta(days=29)
        # data_menos_30_dias = hoje - dias_30
        # init_date = data_menos_30_dias.strftime('%d/%m/%Y')
        # finish_date = hoje.strftime('%d/%m/%Y')


        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        service = Service(ChromeDriverManager().install())
        spider = webdriver.Chrome(service=service, options=options)

        spider.get("https://saw.trixti.com.br/saw/Logar.do?method=abrirSAW")

        login = spider.find_element('xpath', "/html/body/form/table/tbody/tr[1]/td/div/div/input[1]")
        senha = spider.find_element('xpath', "/html/body/form/table/tbody/tr[1]/td/div/div/input[2]")
        logar = spider.find_element('xpath', "/html/body/form/table/tbody/tr[1]/td/div/div/input[3]")
        login.send_keys(username)
        senha.send_keys(password)

        logar.click()


        tiss = spider.find_element('xpath', "/html/body/table[2]/tbody/tr/td[1]/div/div/ul/li[3]/a")
        tiss.click()
        exec_panel = spider.find_element('xpath', "/html/body/table[2]/tbody/tr/td[1]/div/div/ul/li[3]/ul/li[1]/a/label")
        exec_panel.click()
        
        
        for num_guia in num_guias:
            searchField = spider.find_element('xpath', "/html/body/table[2]/tbody/tr/td[2]/form/table[2]/tbody/tr[1]/td[4]/input[3]")
            searchField.clear()
            searchField.send_keys(num_guia)
            
            search = spider.find_element('xpath', "/html/body/table[2]/tbody/tr/td[2]/form/table[3]/tbody/tr/td/input")
            search.click()
            
            try:
                guia = spider.find_element('xpath', f"/html/body/table[2]/tbody/tr/td[2]/form/table[4]/tbody/tr")

                num_guia = guia.find_element('xpath', "./td[2]/a").text
                guia_status = guia.find_element('xpath', "./td[10]").text

                guia_status = guia_status.title()
                
                data_guias.append({"guia":num_guia, "status":guia_status})
                print(data_guias)      

            except:
                continue  
        
        return data_guias

        