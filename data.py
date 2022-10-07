import configparser

config = configparser.ConfigParser()
config.read('config/main.ini')


def put_file_by_id(file_id, data):
    local_path = f'{config["DATA"]["file_path"]}/{file_id}.jpg'  # TODO: handle extension
    file = open(local_path, 'wb')
    file.write(data)
    file.close()


def get_file_by_id(file_id):
    local_path = f'{config["DATA"]["file_path"]}/{file_id}.jpg'  # TODO: handle extension
    file = open(local_path, 'rb')
    print(f'opening file {local_path}')
    data = file.read()
    file.close()
    return data
