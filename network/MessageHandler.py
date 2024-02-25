import time
import heapq
messages_history = {}
message_times = []


# Function to retrieve the entire messages history
def get_messages_history():
    return messages_history


def new_message(peer_id, message_text):
    try:
        message_id = str(int(time.time() * 1_000_000))
        add_message(message_id, peer_id, message_text)
    except Exception as e:
        print("MESSAGE_HANDLER: |ERROR|: Error adding new message:", e)


def add_message(message_id, peer_id, message_text):
    try:
        global message_times
        if len(message_times) >= 100 and message_times[0] < message_id:
            oldest_message_id = heapq.heappop(message_times)
            del messages_history[oldest_message_id]
        messages_history[message_id] = {"peer_id": peer_id, "message": message_text}
        heapq.heappush(message_times, message_id)
    except Exception as e:
        print("MESSAGE_HANDLER: |ERROR|: Error adding message:", e)


def number_of_messages():
    return len(messages_history)


def get_sorted_messages(local_messages_history, message_times_heap):
    try:
        heap_copy = message_times_heap[:]
        sorted_message_ids = [heapq.heappop(heap_copy) for _ in range(len(heap_copy))]
        sorted_messages = [local_messages_history[message_id] for message_id in sorted_message_ids]
    except Exception as e:
        print("MESSAGE_HANDLER: |ERROR|: Error getting sorted messages:", e)
        return []
    return sorted_messages


def update_local_history(messages):
    try:
        for message_id, info in messages.items():
            add_message(message_id, info["peer_id"], info["message"])
    except Exception as e:
        print("MESSAGE_HANDLER: |ERROR|: Error updating local history:", e)
