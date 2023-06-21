import pyautogui
import time
import easygui
import argparse
import requests
import datetime
from logger import log_start, log_end, log_info, log_error
from custom_exceptions import LibreOfficeOpenError

def main():
    # Obter o nome do usuário como um argumento de linha de comando
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', help='Nome do usuário')
    args = parser.parse_args()

    # Verificar se o nome do usuário foi fornecido
    if not args.user:
        easygui.msgbox('Por favor, forneça o nome do usuário através do parâmetro --user')
        exit()

    # Linha de início da execução
    log_start(args.user)

    try:
        # Exibir uma caixa de diálogo para o usuário inserir o número de usuários a serem obtidos
        num_users = int(easygui.integerbox(msg='Quantos usuários (de 1 a 10)?',
                                        title='Número de usuários',
                                        default=1,
                                        lowerbound=1))
        log_info(f"Número de usuários a serem inseridos: {num_users}")

        # Verificar se o número fornecido está dentro do intervalo válido (1 a 10)
        if num_users < 1 or num_users > 10:
            log_info(f"Número {num_users} inválido. O número de usuários deve estar entre 1 e 10.")
            easygui.msgbox("Número inválido. O número de usuários deve estar entre 1 e 10.")
            exit()

        # Restante do código relacionado à execução do PyAutoGUI

        # URL base da API que fornece os dados dos usuários
        url_base = "https://jsonplaceholder.typicode.com/users/"

        # Abrir o LibreOffice Calc
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write('libreoffice calc')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(10)

        if not check_libreoffice_open():
            raise LibreOfficeOpenError("Erro ao abrir o LibreOffice Calc.")

        # Cabeçalho das colunas
        header = ["id", "name", "username", "email"]

        # Inserir cabeçalho na primeira linha do LibreOffice Calc
        for col, value in enumerate(header):
            pyautogui.typewrite(value)
            pyautogui.press('tab')

        # Loop para obter os dados dos usuários e colar nas células do LibreOffice Calc
        for i in range(1, num_users + 1):
            # URL completa para obter os dados do usuário
            url = url_base + str(i)
            log_info(f"url to get user: {url}")

            # Obter os dados do usuário através da API
            response = requests.get(url)
            user = response.json()

            # Extrair as informações do usuário
            log_info(f"response: {user}")
            user_info = [str(user["id"]), user["name"], user["username"], user["email"]]

            # Ir para a próxima linha no LibreOffice Calc
            pyautogui.press('down')
            pyautogui.press('home')

            # Inserir as informações nas células do LibreOffice Calc
            for col, value in enumerate(user_info):
                pyautogui.typewrite(value)
                pyautogui.press('tab')

        timestamp = datetime.datetime.now().timestamp()

        pyautogui.hotkey('ctrl', 'q')
        time.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.write(f"C:\\Users\\Dinaerte\\Documents\\code\\farme\\poc2\\files\ {timestamp}")
        time.sleep(2)
        pyautogui.press('enter')

    except LibreOfficeOpenError as e:
        # Registrar a exceção no arquivo de log
        easygui.msgbox(msg=e, title="Erro")
        log_error(str(e))

    except Exception as e:
        easygui.msgbox(msg=e, title="Erro")
        log_error(str(e))

        # fecha o libre office sem salvar o arquivo
        pyautogui.hotkey('ctrl', 'q')
        time.sleep(0.5)
        pyautogui.press('tab')
        pyautogui.press('enter')

    finally:
        # Linha de fim da execução
        log_end()

    # Fechar o LibreOffice Calc
    # pyautogui.hotkey('alt', 'f4')

def check_libreoffice_open():
    window_title = "LibreOffice Calc"  # Título da janela do LibreOffice Calc
    windows = pyautogui.getWindowsWithTitle(window_title)
    return len(windows) > 0

main()