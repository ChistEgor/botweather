import requests
import json
from time import sleep

telegram_token = '1146634987:AAHhhmXXUCWbnF3RPNM-rUBEaQV_s4tV2Xs'
telegram_link = 'https://api.telegram.org/bot' + telegram_token + '/'

open_weather_api = 'db71095002de213ae977f3d6cd10ed4f'
open_weather_link = 'https://api.openweathermap.org/data/2.5/weather'


def get_updates():
    """
    Getting json object
    """
    url = telegram_link + 'getUpdates'
    response = requests.get(url)
    return response.json()


def get_json_file():
    """
    Creating a file in text format Jason which
    helps to select the necessary dictionary keys for future use.
    """
    dict_updates = get_updates()
    with open('updates.json', 'w') as file:
        json.dump(dict_updates, file, indent=2, ensure_ascii=False)


def get_message():
    """
    Getting a dictionary consisting of chat_id and text
    which were originally taken from the file updates.json.
    """
    data: dict = get_updates()

    chat_id = data['result'][-1]['message']['chat']['id']
    message_text = data['result'][-1]['message']['text']

    message = {'chat_id': chat_id, 'text': message_text}
    return message


def get_update_id(): # Зачем я его получил если не с чем сравнить и обновить
    """
    Here we get update_id, which will be constantly refreshed.
    """
    data: dict = get_updates()
    current_update_id = data['result'][-1]['update_id']
    return current_update_id


def get_temp(city):
    """
    City is a parameter('text': message_text)
    that contains the last text entered in telegram chat by the user.
    """
    response = requests.get(url=open_weather_link,
                            params={'q': city, 'appid': open_weather_api, 'units': 'metric'})
    if response.status_code == 200:
        response = json.loads(response.content)
        temperature: int = response['main']['temp']
        result = round(temperature)
        return f'Текущая температура {result} °С'  # Here you can change the language :)
    return 'Введите корректное название города'


def send_message_from_bot(chat_id, text):
    url = telegram_link + f'sendMessage?chat_id={chat_id}&text={text}'
    requests.get(url)


def main():
    # current_update_id = get_update_id()
    while True:
        answer = get_message()
        chat_id = answer['chat_id']
        text = answer['text']
        send_message_from_bot(chat_id, get_temp(text))
        # sleep(3)


if __name__ == '__main__':
    main()
