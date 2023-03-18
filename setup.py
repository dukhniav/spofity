import os
import sys

env_file_path = './.env'
fields = {
    'SPOTIPY_CLIENT_ID': {'param': 'client_id', 'prompt': 'Spotify Client ID: '},
    'SPOTIPY_CLIENT_SECRET': {'param': 'client_secret', 'prompt': 'Spotify Client Secret: '},
    'SPOTIPY_CLIENT_USERNAME': {'param': 'client_username', 'prompt': 'Spotify Client Username: '}
}


def create_env_file():
    with open(env_file_path, 'w') as env_file:
        for field, config in fields.items():
            env_file.write(f"{field}=''\n")


def update_env_file(field_name, field_value):
    with open(env_file_path, 'r') as env_file:
        env_lines = env_file.readlines()
    with open(env_file_path, 'w') as env_file:
        for line in env_lines:
            if line.startswith(f"{field_name}="):
                env_file.write(f"{field_name}='{field_value}'\n")
            else:
                env_file.write(line)


def get_field_name(param):
    for field, config in fields.items():
        if config['param'] == param:
            return field
    return None


def main():
    if not os.path.isfile(env_file_path):
        create_env_file()

    if len(sys.argv) == 2:
        field_arg = sys.argv[1]
        field_name = get_field_name(field_arg)
        if field_name is not None:
            field_value = input(fields[field_name]['prompt'])
            update_env_file(field_name, field_value)
        else:
            print(f"Field param '{field_arg}' not found in fields.")
    else:
        with open(env_file_path, 'w') as env_file:
            for field, config in fields.items():
                field_value = input(config['prompt'])
                env_file.write(f"{field}='{field_value}'\n")


if __name__ == '__main__':
    main()
