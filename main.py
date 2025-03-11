import time
import requests
import os
from dotenv import load_dotenv
import telebot


LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'


def send_telegram_message(bot, message, tg_chat_id):
    bot.send_message(tg_chat_id, message)
    return True


def notify_user_about_success(success):
    if success:
        print('Сообщение отправлено')
    else:
        print('Сообщение не удалось отправить')


def check_reviews(bot, devman_token, tg_chat_id):
    timestamp = None
    while True:
        try:
            params = {}
            if timestamp:
                params['timestamp'] = timestamp

            headers = {
                "Authorization": f"Token {devman_token}"
            }

            response_long_polling = requests.get(
                LONG_POLLING_URL,
                headers=headers,
                params=params,
                timeout=10
            )
            response_long_polling.raise_for_status()

            response_data = response_long_polling.json()

            if response_data['status'] == 'timeout':
                timestamp = response_data.get('timestamp_to_request')
            elif response_data['status'] == 'found':
                timestamp = response_data.get('last_attempt_timestamp')
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

                    send_telegram_message(bot, message, tg_chat_id)

        except requests.exceptions.ReadTimeout:
            error_message = "Таймаут ожидания..."
            print(error_message)
            send_telegram_message(bot, error_message, tg_chat_id)
            time.sleep(5)
        except requests.exceptions.ConnectionError as ce:
            error_message = f"Ошибка соединения: {ce}"
            print(error_message)
            send_telegram_message(bot, error_message, tg_chat_id)
            time.sleep(5)
        except requests.exceptions.Timeout:
            error_message = "Превышено время ожидания ответа. Повторная попытка через 5 секунд..."
            print(error_message)
            send_telegram_message(bot, error_message,tg_chat_id)
            time.sleep(5)
        except Exception as e:
            error_message = f"Неизвестная ошибка: {e}. Скрипт будет перезапущен через 5 секунд..."
            print(error_message)
            send_telegram_message(bot, error_message, tg_chat_id)
            time.sleep(5)


def main():
    load_dotenv('.env')

    devman_token = os.environ['DEVMAN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    tg_chat_id = os.environ['CHAT_ID']

    bot = telebot.TeleBot(telegram_token)

    if not tg_chat_id.isdigit():
        raise ValueError('tg_chat_id должен быть целым числом')

    print("Скрипт запущен. Жду проверки работ...")

    try:
        success = check_reviews(bot, devman_token, tg_chat_id)
        notify_user_about_success(success)
    except Exception as e:
        print(f'Ошибка: {e}')


if __name__ == '__main__':
    main()