import paramiko
import json
import uuid
import io


def add_user_ssh(host, port, username, password, config_path, user_id):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, password=password)

    sftp = client.open_sftp()

    # Загрузить config.json
    with sftp.file(config_path, "r") as remote_file:
        config = json.load(remote_file)

    # Добавить клиента
    new_uuid = str(uuid.uuid4())
    config["inbounds"][0]["settings"]["clients"].append({
        "id": new_uuid,
        "level": 0,
        "email": f"{user_id}@vpn"
    })

    # Сохранить обратно config.json
    new_data = json.dumps(config, indent=2)
    with sftp.file(config_path, "w") as remote_file:
        remote_file.write(new_data)

    sftp.close()

    # Перезапуск Xray
    stdin, stdout, stderr = client.exec_command("systemctl restart xray")
    restart_output = stdout.read().decode()
    restart_error = stderr.read().decode()
    client.close()

    return new_uuid, restart_output, restart_error
