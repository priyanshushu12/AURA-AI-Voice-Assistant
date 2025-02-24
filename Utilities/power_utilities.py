import os

power_commands = ["reboot", "restart", "shutdown", "sleep", "hibernate", "log off", "lock", "shutdown with delay"]

def execute_power_command(user_query):
    if user_query == "shutdown with delay":
        delay = input("Enter the delay time in seconds (e.g., 60): ")
        if delay.isdigit():
            delay = int(delay)
            print(f"Shutting down the PC in {delay} seconds...")
            os.system(f"shutdown /s /f /t {delay}")
        else:
            print("Invalid input. Please enter a valid number for the delay time.\n")
        return

    if user_query in ["reboot", "restart"]:
        print("Restarting the PC...")
        os.system("shutdown /r /f /t 1")
    elif user_query == "shutdown":
        print("Shutting down the PC...")
        os.system("shutdown /s /f /t 1")
    elif user_query == "sleep":
        print("Putting the PC to sleep...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
    elif user_query == "hibernate":
        print("Hibernating the PC...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState Hibernate")
    elif user_query == "log off":
        print("Logging off the user...")
        os.system("shutdown /l")
    elif user_query == "lock":
        print("Locking the PC...")
        os.system("rundll32.exe user32.dll,LockWorkStation")
