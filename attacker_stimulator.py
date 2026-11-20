import socket, random, time, sys

HOST, PORT = "127.0.0.1", 2323   # honeypot.py ke same hona chahiye

USERS = ["root", "admin", "user", "test", "support", "ubnt", "pi", "guest", "oracle"]
PASSWORDS = ["123456", "admin", "password", "root", "12345",
             "1234", "default", "raspberry", "toor", "qwerty"]


def read_until(s, marker):
    """Jab tak marker (jaise b'login: ') na aaye, tab tak padhte raho."""
    data = b""
    while marker not in data:
        chunk = s.recv(1024)
        if not chunk:
            raise ConnectionError("Server ne connection band kar diya")
        data += chunk
    return data


def one_attack(user, pwd):
    s = socket.create_connection((HOST, PORT), timeout=5)
    try:
        read_until(s, b"login: ")
        s.sendall((user + "\r\n").encode())
        read_until(s, b"Password: ")
        s.sendall((pwd + "\r\n").encode())
        read_until(s, b"Login incorrect")   # honeypot ne log kar liya, tabhi yeh aata hai
    finally:
        s.close()


# Number command se do (python attacker_simulator.py 25) ya yahan likho
if len(sys.argv) > 1:
    total = int(sys.argv[1])
else:
    try:
        total = int(input("Kitne attacks bhejne hain? "))
    except ValueError:
        print("Number likho, jaise 25")
        sys.exit()

ok = 0
for i in range(1, total + 1):
    user, pwd = random.choice(USERS), random.choice(PASSWORDS)
    try:
        one_attack(user, pwd)
        ok += 1
        print(f"Try {i}: {user} / {pwd}  OK")
    except Exception as e:
        print(f"Try {i}: FAIL ({e}). Kya honeypot.py chal raha hai?")
        break
    time.sleep(0.3)

print(f"\nKul {ok} attacks bheje.")
print(f"Dashboard (Real data) mein bhi {ok} dikhne chahiye.")