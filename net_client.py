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


# modify render_health_bar to accept a hp_width parameter for consistent padding
def render_health_bar(cur, maxv, length=20, hp_width=None):
    """Return a string like '██████░░░░  95% ( 95/100)' with padded numbers if hp_width provided"""
    try:
        cur = max(0, int(cur))
        maxv = max(1, int(maxv))
    except Exception:
        return f"{cur}/{maxv}"
    pct = cur / maxv
    filled = int(round(length * pct))
    empty = length - filled
    bar = "█" * filled + "░" * empty
    percent_text = f"{int(round(pct * 100)):3d}%"
    if hp_width is None:
        return f"{bar} {percent_text} ({cur}/{maxv})"
    else:
        # right-align numbers to hp_width so columns line up
        return f"{bar} {percent_text} ({str(cur).rjust(hp_width)}/{str(maxv).rjust(hp_width)})"


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

    # round counter
    round_count = 0

    while True:
        msg = recv_json(s)
        if msg is None:
            print("Server closed connection")
            break

        t = msg.get("type")
        if t == "info":
            print("Server:", msg.get("msg"))
        elif t == "start":
            round_count = 0
            print("Game started")
            players = msg.get("players", [])
            # compute padding widths
            name_width = max((len(p.get("name", "")) for p in players), default=0)
            hp_width = max((len(str(p.get("health_max", 0))) for p in players), default=1)
            for p in players:
                hb = render_health_bar(p.get("health", 0), p.get("health_max", 1), hp_width=hp_width)
                # pad name to name_width so bars align
                print(f"{p.get('name',''): <{name_width}} : {p.get('class','')} - {hb}")
            print()
        elif t == "request_choice":
            # new round begins when server asks for choice
            round_count += 1
            options = ["A - Attack", "C - Counter", "D - Defense"]
            selection = choose_from_list(f"Round {round_count}: choose action:", options)
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
            print(f"--- Round {round_count} Result ---")
            print(msg.get("last_action"))
            print()
            players = msg.get("players", [])
            name_width = max((len(p.get("name", "")) for p in players), default=0)
            hp_width = max((len(str(p.get("health_max", 0))) for p in players), default=1)
            for p in players:
                hb = render_health_bar(p.get("health", 0), p.get("health_max", 1), hp_width=hp_width)
                print(f"{p.get('name',''): <{name_width}} : {hb}")
        elif t == "game_over":
            print("Game over! Winner:", msg.get("winner"))
            print(f"Total rounds: {round_count}")
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
