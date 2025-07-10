import uuid
import json
from datetime import datetime, timedelta

def generate_uuid():
    return str(uuid.uuid4())

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def add_user(user_id, region, config_path, domain):
    users = load_users()
    user_uuid = generate_uuid()
    exp_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    client = {
        "id": user_uuid,
        "level": 0,
        "email": f"{user_id}@vpn"
    }

    with open(config_path, "r+") as f:
        data = json.load(f)
        data["inbounds"][0]["settings"]["clients"].append(client)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

    users[str(user_id)] = {
        "uuid": user_uuid,
        "region": region,
        "expires": exp_date
    }

    save_users(users)
    return user_uuid, domain