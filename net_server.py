import socket
import threading
import json
from character_subclass import HeroWarrior, HeroPaladin, HeroArcher


def send_json(conn, obj):
    data = json.dumps(obj) + "\n"
    conn.sendall(data.encode())


def recv_json(conn):
    # read until newline
    buffer = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            return None
        buffer += chunk
        if b"\n" in buffer:
            line, _, rest = buffer.partition(b"\n")
            # leave rest unread for simplicity (messages are simple)
            try:
                return json.loads(line.decode())
            except Exception:
                return None


def class_from_index(idx, name):
    if idx == 0:
        return HeroWarrior(name=name)
    elif idx == 1:
        return HeroPaladin(name=name)
    elif idx == 2:
        return HeroArcher(name=name)
    else:
        return HeroWarrior(name=name)


def resolve_round(p1_choice, p2_choice, p1, p2):
    # A beats C, C beats D, D beats A
    if p1_choice == p2_choice:
        return "tie", "Tie! No damage."

    p1_wins = (
        (p1_choice == "A" and p2_choice == "C")
        or (p1_choice == "C" and p2_choice == "D")
        or (p1_choice == "D" and p2_choice == "A")
    )

    if p1_wins:
        damage = p1.weapon.damage
        p2.health = max(p2.health - damage, 0)
        p2.health_bar.update()
        return "p1", f"{p1.name} dealt {damage} damage to {p2.name} with {p1.weapon.name}"
    else:
        damage = p2.weapon.damage
        p1.health = max(p1.health - damage, 0)
        p1.health_bar.update()
        return "p2", f"{p2.name} dealt {damage} damage to {p1.name} with {p2.weapon.name}"


def player_summary(p):
    return {
        "name": p.name,
        "class": p.classname,
        "health": p.health,
        "health_max": p.health_max,
        "weapon": {"name": p.weapon.name, "damage": p.weapon.damage},
    }


def run_server(host="0.0.0.0", port=9999):
    print(f"Starting server on {host}:{port} ...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(2)

    clients = []

    while len(clients) < 2:
        conn, addr = s.accept()
        print(f"Client connected from {addr}")
        clients.append((conn, addr))
        send_json(conn, {"type": "info", "msg": "Connected to game server. Please send your class selection: {\"type\":\"select_class\", \"choice\":0|1|2, \"name\":\"You name\"}"})

    conn1, addr1 = clients[0]
    conn2, addr2 = clients[1]

    # receive class choices
    msg1 = recv_json(conn1)
    msg2 = recv_json(conn2)

    if not msg1 or msg1.get("type") != "select_class":
        send_json(conn1, {"type": "error", "msg": "Invalid class selection"})
        conn1.close()
        conn2.close()
        return

    if not msg2 or msg2.get("type") != "select_class":
        send_json(conn2, {"type": "error", "msg": "Invalid class selection"})
        conn1.close()
        conn2.close()
        return

    p1 = class_from_index(int(msg1.get("choice", 0)), msg1.get("name") or "Player1")
    p2 = class_from_index(int(msg2.get("choice", 0)), msg2.get("name") or "Player2")

    # notify clients game starting
    start_payload = {"type": "start", "players": [player_summary(p1), player_summary(p2)]}
    send_json(conn1, start_payload)
    send_json(conn2, start_payload)

    print("Game start: ", p1.classname, "vs", p2.classname)

    # main game loop
    while True:
        # request choices
        send_json(conn1, {"type": "request_choice"})
        send_json(conn2, {"type": "request_choice"})

        r1 = recv_json(conn1)
        r2 = recv_json(conn2)

        if not r1 or r1.get("type") != "round_choice":
            send_json(conn1, {"type": "error", "msg": "Invalid round choice"})
            break
        if not r2 or r2.get("type") != "round_choice":
            send_json(conn2, {"type": "error", "msg": "Invalid round choice"})
            break

        choice1 = r1.get("choice")
        choice2 = r2.get("choice")

        winner, action_msg = resolve_round(choice1, choice2, p1, p2)

        payload = {
            "type": "state_update",
            "players": [player_summary(p1), player_summary(p2)],
            "last_action": action_msg,
        }

        send_json(conn1, payload)
        send_json(conn2, payload)

        print(action_msg)

        if p1.health == 0 or p2.health == 0:
            if p1.health == 0 and p2.health == 0:
                result = "draw"
            elif p1.health == 0:
                result = p2.name
            else:
                result = p1.name

            send_json(conn1, {"type": "game_over", "winner": result})
            send_json(conn2, {"type": "game_over", "winner": result})
            break

    print("Shutting down server")
    conn1.close()
    conn2.close()
    s.close()


if __name__ == "__main__":
    run_server()
