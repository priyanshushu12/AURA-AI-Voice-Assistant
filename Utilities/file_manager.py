import os
import speech_recognition as sr
import shutil  # For moving files/folders
import subprocess  # For opening files/folders

def get_desktop_path():
    """Returns the desktop path for the current user."""
    return os.path.join(os.path.expanduser("~"), "Desktop")

def create_file(file_name):
    """Creates a file on the desktop."""
    desktop_path = get_desktop_path()
    file_path = os.path.join(desktop_path, file_name)
    try:
        with open(file_path, 'w') as file:
            file.write("")  # Creates an empty file
        print(f"File '{file_name}' created on the desktop.")
    except Exception as e:
        print(f"Error creating file: {e}")

def create_folder(folder_name):
    """Creates a folder on the desktop."""
    desktop_path = get_desktop_path()
    folder_path = os.path.join(desktop_path, folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder '{folder_name}' created on the desktop.")
    except Exception as e:
        print(f"Error creating folder: {e}")

def delete_item(item_name):
    """Deletes a file or folder from the desktop."""
    desktop_path = get_desktop_path()
    item_path = os.path.join(desktop_path, item_name)
    try:
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"File '{item_name}' deleted.")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Folder '{item_name}' deleted.")
        else:
            print(f"No such file or folder: '{item_name}'.")
    except Exception as e:
        print(f"Error deleting item: {e}")

def rename_item(old_name, new_name):
    """Renames a file or folder on the desktop."""
    desktop_path = get_desktop_path()
    old_path = os.path.join(desktop_path, old_name)
    new_path = os.path.join(desktop_path, new_name)
    try:
        os.rename(old_path, new_path)
        print(f"Renamed '{old_name}' to '{new_name}'.")
    except Exception as e:
        print(f"Error renaming item: {e}")

def list_desktop_items():
    """Lists all files and folders on the desktop."""
    desktop_path = get_desktop_path()
    items = os.listdir(desktop_path)
    if items:
        print("Items on the desktop:")
        for item in items:
            print(f"- {item}")
    else:
        print("The desktop is empty.")

def open_item(item_name):
    """Opens a file or folder from the desktop."""
    desktop_path = get_desktop_path()
    item_path = os.path.join(desktop_path, item_name)
    try:
        if os.path.exists(item_path):
            subprocess.run(["open" if os.name == "posix" else "start", item_path], shell=True)
            print(f"Opened '{item_name}'.")
        else:
            print(f"No such file or folder: '{item_name}'.")
    except Exception as e:
        print(f"Error opening item: {e}")

def move_item(item_name, destination_path):
    """Moves a file or folder to a new location."""
    desktop_path = get_desktop_path()
    item_path = os.path.join(desktop_path, item_name)
    try:
        if os.path.exists(item_path):
            shutil.move(item_path, destination_path)
            print(f"Moved '{item_name}' to '{destination_path}'.")
        else:
            print(f"No such file or folder: '{item_name}'.")
    except Exception as e:
        print(f"Error moving item: {e}")

def listen_and_execute():
    """Captures and processes voice commands for desktop operations."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")

            # Handle folder creation
            if "create a folder" in command:
                folder_name = command.replace("create a folder", "").strip()
                if folder_name:  # Ensure there's a folder name after the command
                    create_folder(folder_name)
                else:
                    print("Please specify a folder name after 'create a folder'.")
            
            # Handle file creation
            elif "create a file" in command:
                file_name = command.replace("create a file named", "").strip()
                if file_name:
                    create_file(file_name)
                else:
                    print("Please specify a file name after 'create a file named'.")
            
            # Handle delete operation
            elif "delete" in command:
                item_name = command.replace("delete", "").strip()
                delete_item(item_name)
            
            # Handle rename operation
            elif "rename" in command:
                if "to" in command:
                    old_name, new_name = command.replace("rename", "").split("to")
                    rename_item(old_name.strip(), new_name.strip())
                else:
                    print("Please specify both the old and new names for renaming.")
            
            # List desktop items
            elif "list desktop items" in command or "show desktop items" in command:
                list_desktop_items()
            
            # Open file/folder
            elif "open" in command:
                item_name = command.replace("open", "").strip()
                open_item(item_name)
            
            # Move item operation
            elif "move" in command:
                parts = command.replace("move", "").strip().split("to")
                if len(parts) == 2:
                    item_name = parts[0].strip()
                    destination_path = parts[1].strip()
                    move_item(item_name, destination_path)
                else:
                    print("Please specify both the item and destination for moving.")
            
            else:
                print("Command not recognized.")
        except Exception as e:
            print(f"Error processing command: {e}")
