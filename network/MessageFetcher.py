import requests
import json
import threading
from network import MessageHandler

# TODO: Make BASE_URL configurable in a config file
BASE_URL = 'http://127.0.0.1:8000'


def fetch_messages():
    response = requests.get(f'{BASE_URL}/messages')
    if response.status_code == 200:
        messages = response.json()
        print("HTTP: |SERVER|: Fetched messages:", json.dumps(messages, indent=2))
        MessageHandler.update_local_history(messages)
    else:
        print("HTTP: |SERVER|: Failed to fetch messages")


def send_message(message_text):
    response = requests.get(f'{BASE_URL}/send', params={"message": message_text})
    if response.status_code == 200:
        print("HTTP: |SERVER|: Message sent successfully:", message_text)
    else:
        print("HTTP: |SERVER|: Failed to send message")


def schedule_fetch(interval):
    fetch_messages()
    threading.Timer(interval, schedule_fetch, [interval]).start()


# TODO: Configurable interval in the config file
schedule_fetch(60)
