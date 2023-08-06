import multiprocessing
import pathlib
import os.path
from src.simtwin.broker import Broker


def __mock_remote_server__(port, api_key):
    ssl_path = pathlib.Path(__file__).resolve().parent
    broker = Broker(port, lambda x: x == api_key, os.path.join(ssl_path, 'selfsigned.crt'),
                    os.path.join(ssl_path, 'private.key'))
    broker.await_client()
    while True:
        if not broker.listen():
            break
    broker.socket.close()


def run_remote_server(port, key):
    process = multiprocessing.Process(target=__mock_remote_server__, args=(port, key))
    process.start()
    return process
