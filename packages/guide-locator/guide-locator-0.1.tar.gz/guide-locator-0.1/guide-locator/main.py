from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class SAWLocator:
    """Guias Unimed ou Intermed"""
    
    def __init__(self):
        pass
        
    def guider(guide_number, username, password):
        """Retorna uma lista de guias e seus respectivos status """
        # Verifica se as datas fornecidas estão no formato correto
        # try:
        #     start_date = datetime.strptime(start_date, '%d/%m/%Y')
        #     end_date = datetime.strptime(end_date, '%d/%m/%Y')
        # except ValueError:
        #     print("Formato de data inválido. Utilize o formato DD/MM/YYYY.")
        #     return []

        # # Verifica se as datas fornecidas estão em uma ordem correta
        # if start_date > end_date:
        #     print("A data de início deve ser anterior à data de término.")
        #     return []

        # # Verifica se o número da guia é um valor inteiro
        # try:
        #     guide_number = int(guide_number)
        # except ValueError:
        #     print("O número da guia deve ser um valor inteiro.")
        #     return []

        data_guias = []

        # init_date = start_date.strftime('%d/%m/%Y')
        # finish_date = end_date.strftime('%d/%m/%Y')

        

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Instala o ChromeDriver automaticamente com o ChromeDriverManager
        service = Service(ChromeDriverManager().install())

        # Cria uma instância do Chrome WebDriver com as opções configuradas
        spider = webdriver.Chrome(service=service, options=chrome_options)

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
        
        
        for num_guia in guide_number:
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

        