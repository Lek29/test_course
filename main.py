import time

import requests
import os
from pprint import pprint
from dotenv import load_dotenv
import telebot

load_dotenv()

devman_token = os.environ['DEVMAN_TOKEN']
telegram_token = os.environ['TELEGRAM_TOKEN']
tg_chat_id = os.environ['CHAT_ID']

url = 'https://dvmn.org/api/user_reviews/'
long_polling_url = 'https://dvmn.org/api/long_polling/'


bot = telebot.TeleBot(telegram_token)

if not tg_chat_id.isdigit():
    raise ValueError('tg_chat_id должен быть целым числом')

def send_telegram_message(message):
    try:
        bot.send_message(tg_chat_id, message)
        print(f"Сообщение отправлено: {message}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")



def check_reviews():
    timestump = None
    while True:
        try:
            params = {}
            if timestump:
                params['timestump'] = timestump

            headers = {
                "Authorization": f"Token {devman_token}"
            }

            response_long_polling = requests.get(
                long_polling_url,
                headers=headers,
                params=params,
                timeout=90
            )
            response_long_polling.raise_for_status()

            response_data = response_long_polling.json()


            if response_data['status'] == 'timeout':
                timestump = response_data.get('timestamp_to_request')
            elif response_data['status'] == 'found':
                timestump = response_data.get('last_attempt_timestamp')
                for attempt in response_data.get('new_attempts', []):
                    lesson_title = attempt.get('lesson_title')
                    is_negative = attempt.get('is_negative')
                    lesson_url = attempt.get('lesson_url')

                    message = f'Работа "{lesson_title}" проверена!\n'
                    message += f'Ссылка на урок: {lesson_url}\n'

                    if is_negative:
                        message += "К сожалению, в работе нашлись ошибки."
                    else:
                        message += "Преподавателю все понравилось! Можно приступать к следующему уроку."

                    send_telegram_message(message)

        except requests.exceptions.ReadTimeout:
            error_message = "Таймаут ожидания..."
            print(error_message)
            send_telegram_message(error_message)
            time.sleep(5)  # Ждем перед повторной попыткой
        except requests.exceptions.ConnectionError as ce:
            error_message = f"Ошибка соединения: {ce}"
            print(error_message)
            send_telegram_message(error_message)
            time.sleep(5)
        except requests.exceptions.Timeout:
            error_message = "Превышено время ожидания ответа. Повторная попытка через 5 секунд..."
            print(error_message)
            send_telegram_message(error_message)
            time.sleep(5)
        except Exception as e:
            error_message = f"Неизвестная ошибка: {e}. Скрипт будет перезапущен через 5 секунд..."
            print(error_message)
            send_telegram_message(error_message)
            time.sleep(5)

if __name__ == '__main__':
    print("Скрипт запущен. Жду проверки работ...")
    check_reviews()