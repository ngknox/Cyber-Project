import socket, threading, json, datetime

HOST, PORT = "127.0.0.1", 2323   # cloud VM par "0.0.0.0" karna
LOG_FILE = "attempts.jsonl"
lock = threading.Lock()


def log_attempt(ip, user, pwd):
    entry = {
        "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ip": ip,
        "user": user,
        "password": pwd,
    }
    with lock:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    print(entry)


def read_line(conn):
    data = conn.recv(256)
    if not data:
        return None
    return data.decode(errors="ignore").strip()[:100]


def handle(conn, addr):
    try:
        conn.settimeout(15)
        conn.sendall(b"Ubuntu 22.04 LTS\r\n")
        for _ in range(3):
            conn.sendall(b"login: ")
            user = read_line(conn)
            if user is None:
                break
            conn.sendall(b"Password: ")
            pwd = read_line(conn)
            if pwd is None:
                break
            log_attempt(addr[0], user, pwd)
            conn.sendall(b"\r\nLogin incorrect\r\n")
    except Exception:
        pass
    finally:
        conn.close()


server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(50)
print(f"Honeypot chalu hai port {PORT} par...")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()