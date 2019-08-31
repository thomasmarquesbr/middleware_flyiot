import docker
import socket


def get_address_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


ADDRESS = get_address_ip()
client = docker.from_env()

print('Iniciando container')
container = client.containers.run("thomasmarquesbr/flyiot_management:0.2", ADDRESS, detach=True, ports={"5002": "5002"})
print('Container inicializado')
