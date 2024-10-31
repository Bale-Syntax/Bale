import requests
import time

# Your bot token and API base URL
BOT_TOKEN = "Token"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# Custom variables for demonstrating forwarding
custom_forward_from_id = ?  # Replace with your custom forward_from_id
custom_message_id = ? # Replace with your custom message_id

def send_message(chat_id, text):
    """Send a message to the specifiesd chat_id."""
    url = f"{BASE_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()

def forward_message(from_chat_id, to_chat_id, message_id):
    """Forward a message from one chat to another."""
    url = f"{BASE_URL}/forwardMessage"
    payload = {
        'chat_id': to_chat_id,
        'from_chat_id': from_chat_id,
        'message_id': message_id
    }
    response = requests.post(url, json=payload)
    return response.json()

def get_updates(offset=None):
    """Get updates from the bot API with an optional offset."""
    url = f"{BASE_URL}/getUpdates"
    params = {'offset': offset, 'timeout': 10}
    response = requests.get(url, params=params)
    return response.json()

# Main bot logic
def process_check():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if 'result' in updates and updates['result']:
            for update in updates['result']:
                message = update.get('message', {})

                if 'from' not in message:
                    continue

                chat_id = message['chat']['id']
                user_id = message['from'].get('id', None)
                first_name = message['from'].get('first_name', 'کاربر')
                text = message.get('text', '')

                if not user_id:
                    continue

                # Check for /start command
                if text == "/start":
                    send_message(chat_id, f"Hi {first_name}, welcome to the bot!")

                    # Forward the custom message with specified IDs
                    forward_message(custom_forward_from_id, chat_id, custom_message_id)

                # Update last_update_id to avoid processing the same update again
                last_update_id = update['update_id'] + 1

        # Sleep to prevent excessive API calls
        time.sleep(1)

# Run the bot
if __name__ == "__main__":
    process_check()
