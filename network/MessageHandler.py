messages_history = {}


def add_message_to_history(message_id, peer_id, message_text):
    # Check if the message_id is already in the history to avoid duplicates
    if message_id not in messages_history:
        messages_history[message_id] = {"peer_id": peer_id, "message": message_text}


# Function to retrieve the entire messages history
def get_messages_history():
    return messages_history
