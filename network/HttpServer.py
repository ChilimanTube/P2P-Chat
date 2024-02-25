import requests
import json
import threading
from network import MessageHandler

# TODO: Make BASE_URL configurable in a config file
# URL of the backend server
BASE_URL = 'http://127.0.0.1:8000'


def fetch_messages():
    response = requests.get(f'{BASE_URL}/messages')
    if response.status_code == 200:
        messages = response.json()
        print("HTTP: |SERVER|: Fetched messages:", json.dumps(messages, indent=2))
        MessageHandler.update_local_history(messages)
        # Save messages to JSON file or in-memory structure
        # For example, saving to a file:
        # with open('messages_history.json', 'w') as file:
        #    json.dump(messages, file)
    else:
        print("HTTP: |SERVER|: Failed to fetch messages")


def send_message(message_text):
    # Note: Ideally, for sending data, POST should be used, but following the task's instructions
    response = requests.get(f'{BASE_URL}/send', params={"message": message_text})
    if response.status_code == 200:
        print("HTTP: |SERVER|: Message sent successfully:", message_text)
    else:
        print("HTTP: |SERVER|: Failed to send message")


def schedule_fetch(interval):
    fetch_messages()
    # Schedule the next call
    threading.Timer(interval, schedule_fetch, [interval]).start()


# TODO: Configurable interval in the config file
# Example usage
schedule_fetch(60)  # Fetch messages every 60 seconds

# Example of sending a message
send_message("Klickova is in my walls!")
