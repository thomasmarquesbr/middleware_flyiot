import docker
import socket


def get_address_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


ADDRESS = get_address_ip()
client = docker.from_env()

print('Iniciando container')
container_db = client.containers.run("mvertes/alpine-mongo:latest", detach=True, ports={"27017": "27017"})
container_service = client.containers.run("thomasmarquesbr/flyiot_datamanagement", ADDRESS, detach=True, ports={"5001": "5001"})
print('Container inicializado')
