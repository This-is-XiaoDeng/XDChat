import xdchat
import threading
import rich.console
import json
import sys
import time

console = rich.console.Console()

def get_message_thread(client: xdchat.XDChat, sleep: float = 0.1):
    while True:
        messages = client.get_msg()
        for msg in messages:
            console.print(f"[{time.strftime('%H:%M:%S', time.localtime(msg['time']))}] [yellow]{msg['username']}[/]: {msg['text']}")
        time.sleep(sleep)

if __name__ == "__main__":
    config = json.load(open("config.json", encoding="utf-8"))

    # Connect
    with console.status(f"[red] Connect to {config['server']['IP']}:{config['server']['port']} . . ."):
        client = xdchat.XDChat((config["server"]["IP"], config["server"]["port"]))
    console.print(f"[green]Connected to {config['server']['IP']}:{config['server']['port']}")

    # Login
    if "user" not in config.keys():
        config["user"] = []
    if config["user"] == []:
        config["user"] = [console.input("Name: ")]
    try:
        welcome_message = client.login(config["user"])
    except ValueError:
        while True:
            try:
                welcome_message = client.login(config["user"], console.input("Password: "))
            except:
                console.print("[red]Wrong Password!")
            else:
                break
    except NameError:
        console.print("[red]Username not available!")
        sys.exit(1)
    console.print(welcome_message)

    # Start Thread
    threading.Thread(target=lambda: get_message_thread(client)).start()

    # Send Message
    while True:
        client.send_chat_message(console.input())
