import socket
import json
import threading
import sys

# add: try to prefer a module named "query" (as requested), then fall back to other common choice libs
try:
    import query as _questionary  # user asked for "query"
    _CHOICE_LIB = "questionary"
except Exception:
    try:
        import questionary as _questionary  # pip install questionary
        _CHOICE_LIB = "questionary"
    except Exception:
        try:
            import inquirer  # pip install inquirer
            _CHOICE_LIB = "inquirer"
        except Exception:
            try:
                from pick import pick  # pip install pick
                _CHOICE_LIB = "pick"
            except Exception:
                _CHOICE_LIB = None


def choose_from_list(prompt, options):
    """Return selected option string. Uses available interactive library or falls back to input."""
    if _CHOICE_LIB == "questionary":
        return _questionary.select(prompt, choices=options).ask()
    if _CHOICE_LIB == "inquirer":
        q = [inquirer.List("choice", message=prompt, choices=options)]
        ans = inquirer.prompt(q)
        return ans["choice"] if ans else None
    if _CHOICE_LIB == "pick":
        option, _ = pick(options, prompt)
        return option

    # fallback: numbered menu using input()
    print(prompt)
    for i, o in enumerate(options):
        print(f"{i}) {o}")
    while True:
        v = input("Choice: ")
        if v.isdigit() and 0 <= int(v) < len(options):
            return options[int(v)]
        print("Invalid input")


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
    classes = [
        "Warrior (balance)",
        "Paladin (high HP, low dmg)",
        "Archer (low HP, high dmg)",
    ]

    name = input("Your name: ") or "Player"

    # use choose_from_list (will use "query" if installed, then fallbacks)
    opts = [f"{i}) {c}" for i, c in enumerate(classes)]
    sel = choose_from_list("Select your class:", opts)
    try:
        choice = int(str(sel).split(")")[0])
    except Exception:
        # fallback to match by text
        choice = next((i for i, c in enumerate(classes) if c in (sel or "")), 0)

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
            options = ["A - Attack", "C - Counter", "D - Defense"]
            selection = choose_from_list("Round: choose action:", options)
            # normalize to single letter
            if selection:
                c = str(selection).strip()[0].upper()
                if c not in ("A", "C", "D"):
                    # fallback to input loop if unexpected
                    while True:
                        c = input("Your action (A/C/D): ").upper()
                        if c in ("A", "C", "D"):
                            break
                        print("Invalid")
            else:
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
