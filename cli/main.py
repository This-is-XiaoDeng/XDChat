import socket
from rich.console import Console
import threading
import json
import time

console = Console()
sock = None
sockThread = None
# inUse = False


def send(data):
    global sock, console
    # print(inUse)
    # while inUse:
    # time.sleep(0.1)
    # inUse = True
    sock.send(json.dumps(data).encode("utf-8"))
    recv = sock.recv(10240).decode("utf-8")
    # inUse = False

    try:
        return json.loads(recv)
    except json.JSONDecodeError:
        console.print("Error to decode json:", recv)


def getMsg():
    global sock, console
    while True:
        msg = send({"mode": "get_message", "data": {}})
        try:
            for m in msg["data"]["message"]:
                t = time.strftime("%H:%M:%S", time.localtime(m["time"]))

                console.print(f'[{t}]<[yellow]{m["username"]}[/]> {m["text"]}')
        except KeyError:
            pass
            # console.print_exception(show_locals= True)


def login(user, passwd=""):

    loginRecv = send({
        "mode": "login",
        "data": {
            "username": user,
            "version": "xchat-v3 cli",
            "password": passwd
        }
    })

    # 密码
    if loginRecv["code"] == 403:
        if passwd:
            console.print("[red]Wrong Password!")
        return login(user, console.input("[yellow]Password: "))
    else:
        return loginRecv


if __name__ == "__main__":
    console.print("[green]XChat CLI V2")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    console.print(
        '[blue]Connecting to the server means that you have read and agreed to the "xchat and related components use statement and Disclaimer"（ https://www.thisisxd.tk/index.php/archives/262/ ）'
    )

    sock.connect(
        (console.input("[yellow]IP: "), int(console.input("[yellow]Port: "))))

    loginRecv = login(console.input("[yellow]User: "))

    if loginRecv["code"] == 200:
        console.print("[green]Server connected!")

        sockThread = threading.Thread(None, getMsg)
        sockThread.start()

        while True:
            sendMsg = console.input("")
            mode = "send"
            if sendMsg == "/exit":
                mode = "exit"
            elif sendMsg == "/list":
                mode = "getlist"
            a = send({"mode": mode, "data": {"message": sendMsg}})

            if mode == "getlist":
                try:
                    console.print(a["data"]["list"])
                except KeyError:
                    console.print(
                        "[red]Failed to get online list, please try again.")
    else:
        console.log(loginRecv)
