[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ваш-юзер/ваш-репозиторий?style=flat-square)](https://github.com/ваш-юзер/ваш-репозиторий)
[![GitHub stars](https://img.shields.io/github/stars/ваш-юзер/ваш-репозиторий?style=flat-square)](https://github.com/ваш-юзер/ваш-репозиторий)
[![GitHub release](https://img.shields.io/github/v/release/ваш-юзер/ваш-репозиторий?style=flat-square)](https://github.com/ваш-юзер/ваш-репозиторий/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/Documentation-ReadTheDocs-blue?style=flat-square)](https://ваш-документация.рф)

# Уведомления о проверке работ на DevMan

## Содержание
1. [Требования](#требования)
2. [Настройка .env-файла](#настройка-env-файла)
3. [Установка зависимостей](#установка-зависимостей)
4. [Запуск скрипта](#запуск-скрипта)
5. [Пример сообщения в Telegram](#пример-сообщения-в-telegram)

---

## Требования
- **Python 3.7+**
- Учетная запись на [DevMan](https://dvmn.org/)
- Telegram-бот с токеном
- **Chat ID** вашего Telegram-аккаунта

---

## Настройка .env-файла
1. Создайте файл `.env` в корне проекта.
2. Укажите следующие переменные окружения:
```bash
  DEVMAN_TOKEN=ваш_токен_девмана
  TELEGRAM_TOKEN=ваш_токен_телеграм_бота
  CHAT_ID=ваш_chat_id
```
---

## Как получить данные:

### DEVMAN_TOKEN:
1. Перейдите в настройки своего аккаунта на [DevMan](https://dvmn.org/).
2. Найдите раздел **"API-токен"** и скопируйте его.

### TELEGRAM_TOKEN:
1. Создайте бота через [@BotFather](https://t.me/BotFather) в Telegram.
2. Получите токен в формате `123456789:ABCdefGHIJKLMNOPQRSTUVWxyz`.

### CHAT_ID:
1. Используйте бота **@userinfobot** для получения своего `chat_id`.

---

## Установка зависимостей

Установите зависимости из файла `requirements.txt`:
```bash
pip install -r requirements.txt
```
*Примечание*: Рекомендуется использовать виртуальное окружение (например, `venv`).

---

## Запуск скрипта

Активация виртуального окружения (если используется):
```bash
# Для Windows
  .\venv\Scripts\activate

# Для macOS/Linux
  source venv/bin/activate
```
Запуск скрипта:
```bash
  python main.py
```
*Пример вывода консоли:*
```bash
  Скрипт запущен. Жду проверки работ...
```
---

## Пример сообщения в Telegram

Успех проверки:
```bash
  Работа "Введение в Python" проверена!
  Ссылка на урок: https://dvmn.org/modules/1/
  Преподавателю все понравилось! Можно приступать к следующему уроку.
```
Ошибка в работе:
```bash
  Работа "Основы SQL" проверена!
  Ссылка на урок: https://dvmn.org/modules/2/
  К сожалению, в работе нашлись ошибки.
```
---
## Проверка работы

1. Отправьте любой урок на проверку через [DevMan](https://dvmn.org/).
2. Снимите урок с проверки (через опцию **"Вернуть работу с проверки"**).
3. Убедитесь, что уведомление появилось в вашем Telegram.
