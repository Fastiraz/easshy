import sys
import os
import tty
import termios
import time
import json

# ANSI color codes
KNRM = "\x1B[0m"
KRED = "\x1B[31m"
KGRN = "\x1B[32m"
KYEL = "\x1B[33m"
KBLU = "\x1B[34m"
KMAG = "\x1B[35m"
KCYN = "\x1B[36m"
KWHT = "\x1B[37m"

# Arrow key codes
UP_ARROW = 65
DOWN_ARROW = 66
ENTER = 13 #10

#CREDS_FILE = "~/.easshy/creds.json"
CREDS_FILE = os.path.expanduser("~/.easshy/creds.json")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def getch():
    # Get a single character from stdin without waiting for Enter
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def display_menu(choice, options):
    clear_screen()
    print(f"{KYEL}EASShY{KNRM}\n\n")
    for i, option in enumerate(options):
        if i == choice:
            print(f"➜ {KMAG}{option['name']}{KNRM}")
        else:
            print(f"   {option['name']}")

def load_options_from_json(CREDS_FILE):
    try:
        with open(CREDS_FILE, "r") as file:
            options = json.load(file)
            return options
    except FileNotFoundError:
        print(f"Error: JSON file '{CREDS_FILE}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{CREDS_FILE}'.")
        sys.exit(1)

################################################################################
# Load the JSON data from a file
def load_servers(filename):
    try:
        with open(filename, 'r') as file:
            servers = json.load(file)
    except FileNotFoundError:
        servers = {}
        with open(filename, 'w') as file:
            json.dump(servers, file)
    return servers

# Save the JSON data to a file
def save_servers(filename, servers):
    with open(filename, 'w') as file:
        json.dump(servers, file, indent=4)

# Add a new server entry
def add_server(filename, name, username, ip, port, password, sshkey):
    servers = load_servers(filename)
    new_id = str(len(servers))
    servers[new_id] = {
        "name": name,
        "username": username,
        "ip": ip,
        "port": port,
        "password": password,
        "sshkey": sshkey
    }
    save_servers(filename, servers)

# Edit an existing server entry
def edit_server(filename, server_id, name, username, ip, port, password, sshkey):
    servers = load_servers(filename)
    if server_id in servers:
        servers[server_id] = {
            "name": name,
            "username": username,
            "ip": ip,
            "port": port,
            "password": password,
            "sshkey": sshkey
        }
        save_servers(filename, servers)
    else:
        print(f"Server '{server_id}' not found.")

# Remove an existing server entry
def remove_server(filename, server_id):
    servers = load_servers(filename)
    if server_id in servers:
        del servers[server_id]
        save_servers(filename, servers)
    else:
        print(f"Server '{server_id}' not found.")
################################################################################
################################################################################
def menu2(server_id, CREDS_FILE):
    clear_screen()
    print(f"Selected Server ID: {server_id}\n")
    options = {
        "connect": {"name": "Connect to this server"},
        "edit": {"name": "Edit this server"},
        "delete": {"name": "Delete this server"},
        "back": {"name": "Back to main menu"}
    }

    choice = 0
    option_keys = sorted(options.keys())

    while True:
        display_menu(choice, [options[key] for key in option_keys])
        key = ord(getch())
        if key == UP_ARROW and choice > 0:
            choice -= 1
        elif key == DOWN_ARROW and choice < len(options) - 1:
            choice += 1
        elif key == ENTER:
            selected_option = options[option_keys[choice]]
            if selected_option["name"] == "Back to main menu":
                return
            elif selected_option["name"] == "Connect to this server":
                # Implement your code to connect to the server here
                # You may want to call a separate function to handle the connection.
                # Load the current server details
                servers = load_servers(CREDS_FILE)
                current_server = servers.get(server_id, {})
                if not current_server.get("password"):
                    print(f'ssh {current_server.get("username")}@{current_server.get("ip")} -p {current_server.get("port")} -i {current_server.get("sshkey")}')
                    try:
                        os.system(f'ssh {current_server.get("username")}@{current_server.get("ip")} -p {current_server.get("port")} -i {current_server.get("sshkey")}')
                    except:
                        print('Error while connecting...')
                if not current_server.get("sshkey"):
                    print(f'ssh {current_server.get("username")}@{current_server.get("ip")} -p {current_server.get("port")}')
                    try:
                        os.system(f'ssh {current_server.get("username")}@{current_server.get("ip")} -p {current_server.get("port")}')
                    except:
                        print('Error while connecting...')

                print("Connecting to the server...")
                time.sleep(2)  # Simulate a connection
            elif selected_option["name"] == "Edit this server":
                # Load the current server details
                servers = load_servers(CREDS_FILE)
                current_server = servers.get(server_id, {})

                clear_screen()
                print("If you don't want to edit, just press [ENTER]")

                # Prompt for new values, using current values as defaults
                name = input(f'Enter servers name [{current_server.get("name")}]: ') or current_server.get("name")
                username = input(f'Enter servers username [{current_server.get("username")}]')
                ip = input(f'Enter servers IP [{current_server.get("ip")}]: ') or current_server.get("ip")
                port = input(f'Enter servers port [{current_server.get("port")}]: ') or current_server.get("port")
                password = input('Enter servers password [**********]: ')
                sshkey = input(f'Enter servers sshkey path [{current_server.get("sshkey")}]: ')

                # If the user didn't provide a new password or sshkey, use the current ones
                if not name:
                    name = current_server.get("name")
                if not username:
                    username = current_server.get("username")
                if not ip:
                    ip = current_server.get("ip")
                if not port:
                    port = current_server.get("port")
                if not password:
                    password = current_server.get("password")
                if not sshkey:
                    sshkey = current_server.get("sshkey")

                print("Editing server details...")
                edit_server(CREDS_FILE, server_id, name, username, ip, port, password, sshkey)
                time.sleep(2)  # Simulate editing
                main()
            elif selected_option["name"] == "Delete this server":
                # Implement your code to delete the server here
                print("Deleting server...")
                remove_server(CREDS_FILE, server_id)
                renew_ids(CREDS_FILE)
                time.sleep(2)  # Simulate deletion
                main()
################################################################################
def renew_ids(CREDS_FILE):
    try:
        with open(CREDS_FILE, 'r') as file:
            data = json.load(file)
        
        # Create a new dictionary with consecutive IDs starting from 0
        renewed_data = {}
        new_id = 0
        for old_id, server_data in data.items():
            renewed_data[str(new_id)] = server_data
            new_id += 1
        
        # Save the renewed data back to the JSON file
        with open(CREDS_FILE, 'w') as file:
            json.dump(renewed_data, file, indent=4)
        
        print(f"Renewed IDs and saved to '{CREDS_FILE}'")
    except FileNotFoundError:
        print(f"Error: JSON file '{CREDS_FILE}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{CREDS_FILE}'.")
################################################################################

def main():
    options = load_options_from_json(CREDS_FILE)

    # Add "Add server" and "Quit" options
    options["add_server"] = {"name": "Add server"}
    options["quit"] = {"name": "Quit"}

    choice = 0
    option_keys = sorted(options.keys())

    while True:
        display_menu(choice, [options[key] for key in option_keys])
        key = ord(getch())
        if key == UP_ARROW and choice > 0:
            choice -= 1
        elif key == DOWN_ARROW and choice < len(options) - 1:
            choice += 1
        elif key == ENTER:
            selected_option = options[option_keys[choice]]
            if selected_option["name"] == "Quit":
                sys.exit(0)  # Exit the program
            elif selected_option["name"] == "Add server":
                clear_screen()
                name = input('Enter servers name: ')
                username = input('Enter servers username: ')
                ip = input('Enter servers IP: ')
                port = input('Enter servers port: ')
                password = input('Enter servers password [IF NOT PRESS ENTER]: ')
                sshkey = input('Enter servers sshkey path [IF NOT PRESS ENTER]: ')
                if not password:
                    password = None
                if not sshkey:
                    sshkey = None
                add_server(CREDS_FILE, name, username, ip, port, password, sshkey)
                main()
            else:
                print("\nSelected Option:")
                for key, value in selected_option.items():
                    print(f"{key}: {value}")
                print()
                menu2(str(choice), CREDS_FILE)
                time.sleep(1)

if __name__ == "__main__":
    main()
