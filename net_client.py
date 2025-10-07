import socket
import json
import threading
import sys


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

    # choose class
    print("Select your class:")
    print("0) Warrior (balance)")
    print("1) Paladin (high HP, low dmg)")
    print("2) Archer (low HP, high dmg)")

    name = input("Your name: ") or "Player"
    while True:
        choice = input("Choice (0/1/2): ")
        if choice in ("0", "1", "2"):
            break
        print("Invalid input")

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
            print("Round: choose action: A=Attack, C=Counter, D=Defense")
            while True:
                c = input("Your action (A/C/D): ").upper()
                if c in ("A", "C", "D"):
                    break
                print("Invalid")
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
