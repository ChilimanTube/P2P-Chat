import time
import heapq
import threading

messages_history = dict()
message_times = []
message_lock = threading.Lock()


# Function to retrieve the entire messages history
def get_messages_history():
    return messages_history


def new_message(peer_id, message_text):
    try:
        message_id = str(int(time.time() * 1_000_000))
        add_message(message_id, peer_id, message_text)
    except Exception as e:
        print("MEH: |ERROR|: Error adding new message:", e)


def add_message(message_id, peer_id, message_text):
    try:
        global message_times
        message_id_int = int(message_id)
        if len(message_times) >= 100:
            # Remove the oldest message ID from the heap and also from messages_history
            oldest_message_id = heapq.heappop(message_times)
            oldest_message_id_str = str(oldest_message_id)
            if oldest_message_id_str in messages_history:
                del messages_history[oldest_message_id_str]
        heapq.heappush(message_times, message_id_int)
        messages_history[message_id] = {"peer_id": peer_id, "message": message_text}
    except Exception as e:
        print(f"MEH: |ERROR|: Error adding message: {message_id}, {str(e)}")


def number_of_messages():
    return len(messages_history)


def get_sorted_messages(local_messages_history, message_times_heap):
    try:
        heap_copy = message_times_heap[:]
        sorted_message_ids = [heapq.heappop(heap_copy) for _ in range(len(heap_copy))]
        sorted_messages = [local_messages_history[message_id] for message_id in sorted_message_ids]
    except Exception as e:
        print("MEH: |ERROR|: Error getting sorted messages:", e)
        return []
    return sorted_messages


def update_local_history(messages):
    try:
        for message_id, info in messages.items():
            add_message(message_id, info["peer_id"], info["message"])
        print("MEH: |INFO|: Local history updated.")
        print("MEH: |INFO|: Number of messages stored:", number_of_messages())
    except Exception as e:
        print("MEH: |ERROR|: Error updating local history:", e)
