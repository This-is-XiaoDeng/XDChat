import socket
import time
import json

class XDChat():
    def __init__(self, server_addr: tuple) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server_addr)
        self.wait = False

    def send_message(self, message: dict, recv_size: int = 4096, encoding: str = "utf-8") -> dict:
        while self.wait:
            time.sleep(0.1)
        self.wait = True
        msg = json.dumps(message)
        self.socket.send(msg.encode(encoding))
        recv = self.socket.recv(recv_size)
        self.wait = False
        return json.loads(recv)
    
    def login(self, usernames: list, password: str = "") -> str:
        msg = {
            "mode": "login",
            "data": {
                "username": usernames[0],
                "password": password
            }
        }
        recv_data = self.send_message(msg)
        # print(recv_data)
        # Check
        if recv_data["code"] == 402:
            raise ValueError()

        elif recv_data["code"] == 404:
            if usernames.__len__() > 1:
                self.login(usernames[1:], password)
            else:
                raise NameError
        
        elif recv_data["code"] == 405:
            raise UserWarning

        elif recv_data["code"] == 200:
            return recv_data["data"]["message"]
        
        else:
            raise SystemError(recv_data)

    def send_chat_message(self, message: str) -> None:
        msg = {
            "mode": "send",
            "data": {
                "message": message
            }
        }
        recv_data = self.send_message(msg)
        
        if recv_data["code"] != 200:
            raise SystemError(recv_data)
        
    def get_msg(self) -> list:
        msg = {"mode": "get_message"}
        try:
            return self.send_message(msg)["data"]["message"]
        except KeyError:
            raise SystemError("You are offline! Please login again.")

    def send_to_server(self, mode: str, data: dict = {}) -> dict:
        return self.send_message(
            {
                "mode": mode,
                "data": data
            }
        )
        
