from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool
import csv
from datetime import datetime
MULTPROC = 10
FILE = 3
def divid_lista(lista,numb_process):
    size = len(lista)
    size_partes = size // numb_process
    partes = [lista[i* size_partes:(i+1)*size_partes]for i in range(numb_process)]
    return partes

def _waitForAlert(driver):
    return WebDriverWait(driver, 5).until(EC.alert_is_present())

def load_data():
    try:
        with open(f'./{str(FILE)}.csv','r', encoding='utf-8') as f:
            reader = csv.reader(f)
            dados = list(reader)
        return dados
    except Exception as err:
        print(f'ERRO:{err}')
        return False
    
def run_bot(dados):
    
    def fill_element(id_input:str,dado:str):
        driver.find_element(By.ID,id_input).send_keys(dado)
        return
    
    def forms_fill(dados_entrada:list):
        try:
            #MUDAR DADOS ENTRADA PARA O ID DO BOT
            now = datetime.now()
            dados_entrada.insert(0,f'python_mp_{MULTPROC}_{FILE}_{now.strftime("%Y%m%d")}')
            id_correspondente = ['fbot_id','fnome','fid_num','fdata_nasc','fid2_num_char','fgen']
            #print(dados_entrada)
            for index,dado in enumerate(dados_entrada):
                if index != 5:
                    fill_element(id_correspondente[index],dado)
                else:
                    match dado:
                        case 'f':
                            driver.find_element(By.XPATH,'/html/body/div/div[1]/div/div[1]/span/form/input[5]').click()
                        case 'm':
                            driver.find_element(By.XPATH,'/html/body/div/div[1]/div/div[1]/span/form/input[4]').click()
                        case 'nd':
                            driver.find_element(By.XPATH,'/html/body/div/div[1]/div/div[1]/span/form/input[6]').click()
            return True
        except Exception as err:
            print(f'ERROR IN forms_fill:{err}')
            return False
        
    def abertura_cadastramento():
        element = driver.find_element(By.CLASS_NAME,"buttonCadastro")
        element.click()
        return
    
    # options.add_argument('--headless') 
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage') 
    driver = webdriver.Edge()
    url = 'file:///C:/Users/jperi/OneDrive/Documentos/UVA 2024.1/TCC/CODE/SITE/index.html'
    driver.get(url)
    
    #inicio bot
    
    if dados:
        for line in dados:
            abertura_cadastramento()
            #print(line)
            if forms_fill(line):
                
                driver.find_element(By.CLASS_NAME,'buttonSalvar').click()
                alert = _waitForAlert(driver)
                alert.accept()
            else:
                driver.find_element(By.CLASS_NAME,'buttonCancelar').click()

if __name__=='__main__':
    #setup
    
    dados = divid_lista(load_data(),MULTPROC)
    pool = Pool(processes=MULTPROC)
    pool.map(run_bot,dados)
    pool.close()
    pool.join()
    
