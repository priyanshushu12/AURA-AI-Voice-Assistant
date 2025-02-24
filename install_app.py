import subprocess
import webbrowser
import os

def search_app_in_microsoft_store(app_name):
    try:
        # Run the winget search command
        search_command = f"winget search {app_name}"
        search_result = subprocess.run(search_command, check=True, shell=True, capture_output=True, text=True)
        
        # If winget returns results, print them
        print(f"Search Results for {app_name}:")
        print(search_result.stdout)
        
        return search_result.stdout  # Return the search result to check later

    except subprocess.CalledProcessError as e:
        print(f"Error searching for {app_name}: {e}")
        return None

def install_app_from_microsoft_store(app_name):
    # Search for the app
    search_result = search_app_in_microsoft_store(app_name)
    
    # If no results are returned (i.e., the app is not found in winget)
    if search_result is None or "No results found" in search_result:
        print(f"{app_name} not found in winget. Redirecting to Microsoft Store...")
        
        # Redirect to the Microsoft Store page (you can add specific URLs if you have the Product ID)
        # For example, you can manually search for the app URL:
        store_url = f"ms-windows-store://search/?query={app_name}"

        # Use 'start' command to directly invoke Microsoft Store if it's not opening via web browser
        try:
            subprocess.run(["start", store_url], shell=True, check=True)
            print("Opening Microsoft Store...")
        except Exception as e:
            print(f"Error opening Microsoft Store: {e}")
    else:
        # Ask the user for the exact name/ID to install
        exact_app_name = input("\nEnter the exact app name/ID to install from the search results: ")
        
        try:
            # Run the winget install command with the exact name or ID
            install_command = f"winget install {exact_app_name}"
            subprocess.run(install_command, check=True, shell=True)
            print(f"Successfully installed {exact_app_name} from Microsoft Store.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {exact_app_name}: {e}")

