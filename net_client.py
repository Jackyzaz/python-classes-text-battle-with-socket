import socket
import json
import threading
import sys
import inquirer


def send_json(s, obj):
    data = json.dumps(obj) + "\n"
    s.sendall(data.encode())


def recv_json(s):
    buf = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            return None
        buf += chunk
        if b"\n" in buf:
            line, _, rest = buf.partition(b"\n")
            try:
                return json.loads(line.decode())
            except Exception:
                return None


def interactive_mode(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"Connected to server {host}:{port}")

    # choose class using inquirer
    choices = [
        "0) \u2694\ufe0f Warrior (balance)",
        "1) \ud83d\udee1\ufe0f Paladin (high HP, low dmg)",
        "2) \ud83c\udff9 Archer (low HP, high dmg)",
    ]

    questions = [
        inquirer.Text("name", message="Your name", default="Player"),
        inquirer.List("class_choice", message="Select your class", choices=choices),
    ]

    answers = inquirer.prompt(questions)
    name = answers.get("name") or "Player"
    choice = answers.get("class_choice")
    # extract leading digit
    choice = choice.split(")", 1)[0]

    send_json(s, {"type": "select_class", "choice": int(choice), "name": name})

    while True:
        msg = recv_json(s)
        if msg is None:
            print("Server closed connection")
            break

        t = msg.get("type")
        if t == "info":
            print("Server:", msg.get("msg"))
        elif t == "start":
            print("Game started")
            for p in msg.get("players", []):
                print(f"{p['name']} - {p['class']} - {p['health']}/{p['health_max']}")
        elif t == "request_choice":
            # prompt with inquirer choices
            questions = [
                inquirer.List(
                    "action",
                    message="Round: choose action",
                    choices=["A) \ud83d\udde1\ufe0f Attack", "C) \ud83d\udca5 Counter", "D) \ud83d\udee1\ufe0f Defense"],
                )
            ]
            ans = inquirer.prompt(questions)
            sel = ans.get("action")
            c = sel.split(")", 1)[0]
            send_json(s, {"type": "round_choice", "choice": c})
        elif t == "state_update":
            print("--- Round Result ---")
            print(msg.get("last_action"))
            for p in msg.get("players", []):
                print(f"{p['name']}: {p['health']}/{p['health_max']}")
        elif t == "game_over":
            print("Game over! Winner:", msg.get("winner"))
            break
        elif t == "error":
            print("Error from server:", msg.get("msg"))
            break
        else:
            print("Unknown message:", msg)

    s.close()


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
    interactive_mode(host, port)
