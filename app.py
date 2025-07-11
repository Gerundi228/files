import paramiko
import json
import uuid
import traceback


def add_user_ssh(host, port, username, password, config_path, user_id):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10,
            banner_timeout=10,
            auth_timeout=10
        )

        sftp = client.open_sftp()

        with sftp.file(config_path, "r") as remote_file:
            raw_data = remote_file.read().decode()
            config = json.loads(raw_data)

        new_uuid = str(uuid.uuid4())
        config["inbounds"][0]["settings"]["clients"].append({
            "id": new_uuid,
            "level": 0,
            "email": f"{user_id}@vpn"
        })

        new_data = json.dumps(config, indent=2)
        with sftp.file(config_path, "w") as remote_file:
            remote_file.write(new_data)

        sftp.close()

        stdin, stdout, stderr = client.exec_command("systemctl restart xray")
        restart_output = stdout.read().decode()
        restart_error = stderr.read().decode()
        client.close()

        return new_uuid, restart_output, restart_error

    except Exception as e:
        print("❌ Ошибка SSH:")
        print(traceback.format_exc())
        return None, None, f"SSH Error: {str(e)}"
