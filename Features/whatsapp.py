# send_message.py
import pywhatkit as kit
import pyautogui
import time

# Function to get valid integer input
def get_valid_input(prompt, min_value, max_value):
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                raise ValueError("Input cannot be empty.")
            value = int(value)
            if value < min_value or value > max_value:
                raise ValueError(f"Value must be between {min_value} and {max_value}.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")

# Function to send a WhatsApp message
def send_whatsapp_message():
    # Get inputs from the user
    phone_number = input("Enter the recipient's phone number (with country code, e.g., +918XXXXXXXXX): ").strip()
    message = input("Enter the message to send: ").strip()

    # Ensure the user enters valid time values
    send_time_hour = get_valid_input("Enter the hour (24-hour format) to send the message: ", 0, 23)
    send_time_minute = get_valid_input("Enter the minute to send the message: ", 0, 59)

    # Send the message via WhatsApp
    try:
        print(f"Scheduling message to {phone_number} at {send_time_hour}:{send_time_minute:02d}")
        kit.sendwhatmsg(phone_number, message, send_time_hour, send_time_minute)

        # Wait for WhatsApp to open and type the message (pywhatkit's default delay is 20 seconds)
        time.sleep(20)

        # Press Enter programmatically to ensure the message is sent
        pyautogui.press('enter')

        print(f"Message sent to {phone_number}!")
    except Exception as e:
        print(f"An error occurred: {e}")
