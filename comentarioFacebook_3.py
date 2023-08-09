from pathlib import Path
import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

# Digita letra por letra e substitui ENTER por SHIFT + ENTER
def slow_type(element, text: str):
    for text_part in text.split('\n'):
        for character in text_part:
            element.send_keys(character)
            # time.sleep(delay)
            time.sleep(random.randint(25, 35)/1000)
        element.send_keys(Keys.SHIFT+Keys.ENTER)
    element.send_keys(Keys.ENTER)

path_user_data = str(Path('User Data').absolute())

options = uc.ChromeOptions()
options.add_argument("--user-data-dir={}".format(path_user_data))
# options.add_argument("--profile-directory=Profile 9")
driver = uc.Chrome(version_main=114, options=options)

driver.get("https://chat.openai.com/")
sleep(1)
driver.switch_to.new_window('tab')
driver.get("https://www.facebook.com/permalink.php?story_fbid=pfbid03662FSLyXDyEnWGGdA3KAwA53s1WSqo9XCGakAMoXBJrC8QEaLCQxP5QvMCeqKVtil&id=100092642123333&")

chat_window = driver.window_handles[0]
facebook_window = driver.window_handles[1]

sleep(1)

respondidos = []  # Lista para armazenar comentários já respondidos

comentarios = WebDriverWait(driver, 15).until(
    EC.visibility_of_all_elements_located((By.XPATH, '//div[h3]/ul/li[.//li/div[text()="Responder"] and not(.//li//li)]'))
)
print('Número de botões de comentarios:', len(comentarios))

# # Lista de botões de resposta correspondentes aos comentários
# botoes_resposta = WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xi81zsa.x1xlr1w8[role="button"][tabindex="0"]'))
# )

for i, comentario  in enumerate(comentarios):
    # comentario = comentarios[i]
    comentario_texto_element = comentario.find_element(By.XPATH, './/span[@lang]')
    comentario_texto = comentario_texto_element.text
    
    if comentario_texto not in respondidos:
        respondidos.append(comentario_texto)
      
        nome_usuario_elementos = WebDriverWait(driver, 15).until(
        EC.visibility_of_all_elements_located((By.XPATH, './/a[contains(@href, "comment_id") and @tabindex="0" and .//span/span]'))
        )
        if nome_usuario_elementos:
            nome_usuario = nome_usuario_elementos[0].text
        else:
            nome_usuario = ""

        botao_responder = comentario.find_element(By.XPATH, './/li/div[text()="Responder"]')
        botao_responder.click()
        sleep(2)

        driver.switch_to.window(chat_window)
        textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'prompt-textarea')))
        textarea.click()
        textarea.send_keys(comentario_texto)
        espera = WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element_value((By.ID, 'prompt-textarea'), comentario_texto)
        )
        textarea.send_keys(Keys.ENTER)
        sleep(5)

        #Espera a resposta ser concluida
        _ = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="Regenerate response"]'))
        )
        resposta_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.markdown.prose.w-full.break-words.dark\:prose-invert.light"))
        )
        resposta_texto = resposta_element.text

        botao_new_chat = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mb-1.flex.flex-row.gap-2 > a'))
        )
    # Simular um clique com o mouse no botão "New chat"
        ActionChains(driver).move_to_element(botao_new_chat).click().perform()
        
        driver.switch_to.window(facebook_window)
        # campo_resposta = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//div[@aria-label="Responder a {nome_usuario}"]')))
        campo_resposta = comentario.find_element(By.XPATH, './/div[@aria-label="Responder a {}"]'.format(nome_usuario))
        campo_resposta.clear()  # Limpa o campo de resposta
        # campo_resposta.send_keys(resposta_texto)
        # campo_resposta.send_keys(Keys.RETURN)
        slow_type(campo_resposta, resposta_texto)

        sleep(5)

        # Volta ao Facebook, aperta o botão de notificação

driver.quit()
