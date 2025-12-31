import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Initialize bot with your token
bot = telebot.TeleBot("Your-Bot-Token")

# Create keyboard with buttons
def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    visit_site = KeyboardButton('🌐 Visit Site')
    get_key = KeyboardButton('🔑 GetAuth Key')
    keyboard.add(visit_site, get_key)
    return keyboard

# Create inline keyboard for instant URL access
def create_url_keyboard():
    keyboard = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton("🌐 Open Website Now", url="https://nullnmods-key-auth.netlify.app")
    keyboard.add(url_button)
    return keyboard

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🔐 Secure Auth Key Bot

Choose an option below:
• 🌐 Visit Site - Open our website
• 🔑 Get Secure Auth Key - Fetch your authentication key from the server

What would you like to do?
    """
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=create_main_keyboard()
    )

# Handle button clicks
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == '🌐 Visit Site':
        handle_visit_site(message)
    elif message.text == '🔑 GetAuth Key':
        handle_get_key(message)
    else:
        bot.send_message(
            message.chat.id,
            "Please use the buttons below to interact with the bot!",
            reply_markup=create_main_keyboard()
        )

def handle_visit_site(message):
    site_url = "https://nullnmods-key-auth.netlify.app"
    
    # Send message with clickable button that opens the URL directly
    bot.send_message(
        message.chat.id,
        "Click the button below to open the website instantly:",
        reply_markup=create_url_keyboard()
    )
    

def handle_get_key(message):
    url = "https://nullnmods-key-auth.netlify.app/.netlify/functions/generate-key"
    
    # Send typing action to show bot is working
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # Send request to fetch key from API
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Format the response message
        key_info = f"""
🔑 **Secure Auth Key Retrieved**

**Key:** `{data['key']}`
**Generated At:** {data['generatedAt']}
**Expires At:** {data['expiresAt']}

*This key was fetched from the secure server*
        """
        
        bot.send_message(
            message.chat.id,
            key_info,
            parse_mode='Markdown'
        )
        
    except requests.exceptions.Timeout:
        bot.send_message(message.chat.id, "❌ Request timeout: Server took too long to respond")
    except requests.exceptions.ConnectionError:
        bot.send_message(message.chat.id, "❌ Connection error: Could not reach the server")
    except requests.exceptions.HTTPError as e:
        bot.send_message(message.chat.id, f"❌ Server error: {e.response.status_code}")
    except json.JSONDecodeError:
        bot.send_message(message.chat.id, "❌ Error: Invalid response format from server")
    except KeyError as e:
        bot.send_message(message.chat.id, f"❌ Error: Missing expected data in response")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Unexpected error: {str(e)}")

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
