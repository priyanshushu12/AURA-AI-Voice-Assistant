import datetime
import time
from playsound import playsound  # For playing the ringtone
import os  # For handling file paths

# Alarm Functionality
def set_alarm(alarm_date, alarm_time, ringtone_path):
    # Combine date and time into a single datetime object
    alarm_datetime_str = f"{alarm_date} {alarm_time}"
    alarm_datetime = datetime.datetime.strptime(alarm_datetime_str, "%d-%m-%Y %H:%M:%S")
    
    print(f"Alarm is set for {alarm_datetime}.")
    while True:
        current_datetime = datetime.datetime.now()
        if current_datetime >= alarm_datetime:
            print("Wake up! Alarm ringing!")
            if os.path.exists(ringtone_path):
                try:
                    while True:
                        playsound(ringtone_path)
                        time.sleep(30) 
                       
                except Exception as e:
                    print(f"Error playing sound: {e}")
            else:
                print("Ringtone file not found. Please check the path.")
            break
        time.sleep(1)

# Timer Functionality
def start_timer(duration):
    print(f"Timer started for {duration} seconds.")
    while duration:
        mins, secs = divmod(duration, 60)
        timer = f'{mins:02}:{secs:02}'
        print(timer, end="\r")
        time.sleep(1)
        duration -= 1
    print("Time's up!")

# Stopwatch Functionality
def stopwatch():
    print("Press 'Enter' to start the stopwatch, 'Ctrl+C' to stop.")
    try:
        input("Press 'Enter' to start...")
        print("Stopwatch started.")
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            mins, secs = divmod(int(elapsed_time), 60)
            timer = f'{mins:02}:{secs:02}'
            print(timer, end="\r")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopwatch stopped.")

# Main Handler for Commands
def process_command():
    print("\nWhat would you like to do?")
    print("1. Set Alarm")
    print("2. Start Timer")
    print("3. Start Stopwatch")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        alarm_date = input("Enter date for alarm (DD-MM-YYYY): ")
        alarm_time = input("Enter time for alarm (HH:MM:SS): ")
        ringtone_path = r"C:\Users\shukla\Desktop\test\new feature\c486-c91f-4044-96ad-19597721794b.mp3"  # Hardcoded path for testing
        set_alarm(alarm_date, alarm_time, ringtone_path)
    elif choice == "2":
        duration = int(input("Enter duration for timer in seconds: "))
        start_timer(duration)
    elif choice == "3":
        stopwatch()
    elif choice == "4":
        print("Exiting. Have a great day!")
    else:
        print("Invalid choice. Exiting the program.")

# Start the Program
if __name__ == "__main__":
    process_command()
