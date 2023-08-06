import subprocess
import socket

class Network:
    def __init__(
        self,
        network
        )-> None:

        cmd = f'fping -g -r 1 {network}'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.wait()

        self.hosts_list = [(x.strip().decode().split(' ')[0], x.strip().decode().split(' ')[2]) for x in process.stdout]


    @property
    def free(self):
        ip = []
        for host, status in self.hosts_list:
            if status == 'unreachable': ip.append(host)
        return ip
    
    @property
    def busy(self):
        ip = []
        for host, status in self.hosts_list:
            if status == 'alive': ip.append(host)
        return ip


    def check_open_port(self, host, port=22, timeout=2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)                                      #2 Second Timeout
        result = sock.connect_ex((host, port))
        if result == 0:
            return True
        else:
            return False