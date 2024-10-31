import requests
import time

# Your bot token and API base URL
BOT_TOKEN = "Token"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    """Send a message to the specified chat_id."""
    url = f"{BASE_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None

def get_updates(offset=None):
    """Get updates from the bot API with an optional offset."""
    url = f"{BASE_URL}/getUpdates"
    params = {'offset': offset, 'timeout': 10}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting updates: {e}")
        return None

# Main bot logic
def process_check():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates and 'result' in updates and updates['result']:
            for update in updates['result']:
                message = update.get('message', {})

                if not message or 'chat' not in message or 'from' not in message:
                    continue

                chat_id = message['chat']['id']
                message_id = message.get('message_id')

                # Check if the message is forwarded
                if 'forward_from_chat' in message:
                    forward_from_chat = message['forward_from_chat']['id']
                    forward_from_message_id = message.get('forward_from_message_id')

                    # Respond with the forwarding details
                    response_text = (
                        f"Forwarded from chat ID: {forward_from_chat}\n"
                        f"Original Message ID: {forward_from_message_id if forward_from_message_id else 'Not available'}\n"
                        f"New Message ID: {message_id}"
                    )
                    send_message(chat_id, response_text)
                    print(f"Responded to forwarded message in chat ID {chat_id}")

                # Update last_update_id to avoid processing the same update again
                last_update_id = update['update_id'] + 1

        # Sleep to prevent excessive API calls
        time.sleep(1)

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    process_check()
