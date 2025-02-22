import sys
import os
import tty
import termios
import time
import json
import keyboard
import subprocess
from cryptography.fernet import Fernet
import base64

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
ENTER = 13

CREDS_FILE = os.path.expanduser("~/.easshy/creds.json")

class Encrypt:
  def __init__(self) -> None:
    self.KEY_FILE = os.path.expanduser("~/.easshy/4.key")
    self.KEY = None
    self.load_or_generate_key()
    self.fernet = Fernet(self.KEY)

  def write_key(self):
    self.KEY = Fernet.generate_key()
    with open(self.KEY_FILE, "wb") as key_file:
      key_file.write(self.KEY)

  def load_key(self):
    return open(self.KEY_FILE, "rb").read()

  def load_or_generate_key(self):
    if os.path.exists(self.KEY_FILE):
      self.KEY = self.load_key()
    else:
      self.write_key()

  def encrypt(self, passwd):
    if not self.KEY:
      self.load_or_generate_key()
    encoded_passwd = passwd.encode()
    encrypted_passwd = self.fernet.encrypt(encoded_passwd)
    return encrypted_passwd

  def decrypt(self, passwd):
    decrypted_passwd = self.fernet.decrypt(passwd)
    return decrypted_passwd.decode()

def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

def getch():
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
      print(f"\033[36m➜\033[0m {KMAG}{option['name']}{KNRM}")
    else:
      print(f"   {option['name']}")

def load_options_from_json(CREDS_FILE):
  try:
    with open(CREDS_FILE, "r") as file:
      options = json.load(file)
      return options
  except FileNotFoundError:
    os.makedirs(os.path.dirname(CREDS_FILE), exist_ok=True)
    with open(CREDS_FILE, "w") as file:
      file.write("{}")
    return {}
  except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{CREDS_FILE}'.")
    sys.exit(1)

def load_servers(filename):
  try:
    with open(filename, 'r') as file:
      servers = json.load(file)
  except FileNotFoundError:
    servers = {}
    with open(filename, 'w') as file:
      json.dump(servers, file)
  return servers

def save_servers(filename, servers):
  with open(filename, 'w') as file:
    json.dump(servers, file, indent=4)

def add_server(filename, name, username, ip, port, password, sshkey):
  servers = load_servers(filename)
  new_id = str(len(servers))
  if password:
    e = Encrypt()
    encrypted_password = e.encrypt(password)
    password = base64.b64encode(encrypted_password).decode()
  servers[new_id] = {
    "name": name,
    "username": username,
    "ip": ip,
    "port": port,
    "password": password,
    "sshkey": sshkey
  }
  save_servers(filename, servers)

def edit_server(filename, server_id, name, username, ip, port, password, sshkey):
  servers = load_servers(filename)
  if server_id in servers:
    if password:
      e = Encrypt()
      encrypted_password = e.encrypt(password)
      password = base64.b64encode(encrypted_password).decode()
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

def remove_server(filename, server_id):
  servers = load_servers(filename)
  if server_id in servers:
    del servers[server_id]
    save_servers(filename, servers)
  else:
    print(f"Server '{server_id}' not found.")

def renew_ids(CREDS_FILE):
  try:
    with open(CREDS_FILE, 'r') as file:
      data = json.load(file)
    renewed_data = {}
    new_id = 0
    for old_id, server_data in data.items():
      renewed_data[str(new_id)] = server_data
      new_id += 1
    with open(CREDS_FILE, 'w') as file:
      json.dump(renewed_data, file, indent=4)
    print(f"Renewed IDs and saved to '{CREDS_FILE}'")
  except FileNotFoundError:
    print(f"Error: JSON file '{CREDS_FILE}' not found.")
  except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{CREDS_FILE}'.")

def autofill_password(password):
  print('Press [SHIFT] to autofill password.')
  if keyboard.wait("SHIFT"):
    keyboard.write(password)
    time.sleep(1)
    keyboard.press_and_release("enter")
  elif keyboard.wait("enter"):
    pass

def autofill_fingerprint():
  keyboard.write("yes")
  time.sleep(1)
  keyboard.press_and_release("enter")

def main():
  options = load_options_from_json(CREDS_FILE)
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
        sys.exit(0)
      elif selected_option["name"] == "Add server":
        clear_screen()
        name = input('Enter server name: ')
        username = input('Enter server username: ')
        ip = input('Enter server IP: ')
        port = input('Enter server port: ')
        password = input('Enter server password [IF NOT PRESS ENTER]: ')
        sshkey = input('Enter server sshkey path [IF NOT PRESS ENTER]: ')
        if not password:
          password = None
        if not sshkey:
          sshkey = None
        add_server(CREDS_FILE, name, username, ip, port, password, sshkey)
        main()
      else:
        server_id = option_keys[choice]
        clear_screen()
        print(f"Selected Server ID: {server_id}\n")
        server_options = {
          "connect": {"name": "Connect to this server"},
          "edit": {"name": "Edit this server"},
          "delete": {"name": "Delete this server"},
          "back": {"name": "Back to main menu"}
        }
        server_choice = 0
        server_option_keys = list(server_options.keys())

        while True:
          display_menu(server_choice, [server_options[key] for key in server_option_keys])
          key = ord(getch())
          if key == UP_ARROW and server_choice > 0:
            server_choice -= 1
          elif key == DOWN_ARROW and server_choice < len(server_options) - 1:
            server_choice += 1
          elif key == ENTER:
            selected_server_option = server_options[server_option_keys[server_choice]]
            if selected_server_option["name"] == "Back to main menu":
                break
            elif selected_server_option["name"] == "Connect to this server":
              servers = load_servers(CREDS_FILE)
              current_server = servers.get(server_id, {})
              if not current_server.get("password"):
                os.system(f'ssh {current_server.get("username")}@{current_server.get("ip")} -p {current_server.get("port")} -i {current_server.get("sshkey")}')
              else:
                e = Encrypt()
                encrypted_passwd = current_server.get("password")
                password = base64.b64decode(encrypted_passwd).decode()
                password = e.decrypt(password)
                os.system(f'ssh {current_server.get("username")}@{current_server.get("ip")} -p {current_server.get("port")}')
            elif selected_server_option["name"] == "Edit this server":
              servers = load_servers(CREDS_FILE)
              current_server = servers.get(server_id, {})
              clear_screen()
              print("If you don't want to edit, just press [ENTER]")
              name = input(f'Enter server name [{current_server.get("name")}]: ') or current_server.get("name")
              username = input(f'Enter server username [{current_server.get("username")}]: ') or current_server.get("username")
              ip = input(f'Enter server IP [{current_server.get("ip")}]: ') or current_server.get("ip")
              port = input(f'Enter server port [{current_server.get("port")}]: ') or current_server.get("port")
              password = input('Enter server password [**********]: ')
              sshkey = input(f'Enter server sshkey path [{current_server.get("sshkey")}]: ')
              if not password:
                password = current_server.get("password")
              if not sshkey:
                sshkey = current_server.get("sshkey")
              edit_server(CREDS_FILE, server_id, name, username, ip, port, password, sshkey)
              main()
            elif selected_server_option["name"] == "Delete this server":
              remove_server(CREDS_FILE, server_id)
              renew_ids(CREDS_FILE)
              main()

if __name__ == "__main__":
  main()
