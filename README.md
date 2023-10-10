<div align="center">
  <h1><code>EASShY</code></h1>
  <p>EASShY is a simple Python script that allows you to manage your SSH server connections with ease. You can add, edit, delete, and connect to SSH servers using this script. It provides a text-based menu interface for quick and convenient server management.</p>
</div>

![easshy](./img/easshy.png)

## Features

- Add new SSH server entries.
- Edit existing server details.
- Delete server entries.
- Connect to SSH servers with optional password or SSH key.

## Requirements

- Python 3.x

## Installation

1. Clone or download this repository to your local machine.
2. Make sure you have Python 3.x installed.
3. Run the the following commands:

For Linux and macOS:
```bash
mkdir ~/.easshy
cd ~/.easshy
wget https://github.com/Fastiraz/easshy/easshy.py
echo 'alias easshy="python3 ~/.easshy/easshy.py"'
```

## Usage

- Use the arrow keys to navigate the menu.
- Press Enter to select an option.
- You can add new servers, edit existing server details, or delete servers as needed.
- To connect to a server, select the "Connect to this server" option and follow the prompts.
