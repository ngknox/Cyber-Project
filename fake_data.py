import json, random, datetime

PLACES = [("China", 35.8, 104.1), ("Russia", 61.5, 105.3), ("USA", 37.1, -95.7),
          ("Brazil", -14.2, -51.9), ("India", 20.6, 78.9), ("Vietnam", 14.1, 108.3),
          ("Germany", 51.1, 10.4), ("Nigeria", 9.1, 8.7), ("Indonesia", -0.8, 113.9),
          ("Iran", 32.4, 53.7)]
USERS = ["root", "admin", "user", "test", "support", "ubnt", "pi", "guest", "oracle"]
PASSWORDS = ["123456", "admin", "password", "root", "12345",
             "1234", "default", "raspberry", "toor", "qwerty"]

attackers = []
for _ in range(25):
    country, lat, lon = random.choice(PLACES)
    ip = f"{random.randint(11,126)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    attackers.append((ip, country, lat + random.uniform(-4, 4), lon + random.uniform(-4, 4)))

now = datetime.datetime.now(datetime.timezone.utc)
with open("demo_attempts.jsonl", "w") as f:
    for _ in range(100):
        ip, country, lat, lon = random.choice(attackers)
        t = now - datetime.timedelta(minutes=random.randint(0, 1440))
        f.write(json.dumps({
            "time": t.isoformat(), "ip": ip,
            "user": random.choice(USERS), "password": random.choice(PASSWORDS),
            "country": country, "lat": lat, "lon": lon,
        }) + "\n")

print("demo_attempts.jsonl ban gayi")
