import paramiko
import re
import os
import json


def hostname_to_ip(hostname):
    ip = hostname

    m = re.match("gl([a-d])(\d)[a-z]+(\d{1,3})$", hostname)
    if m is not None:
        p1, p2, p3 = m.group(1,2,3)
        p1 = ('a', 'b', 'c', 'd').index(p1) + 2
        ip = "10.19{}.{}.{}".format(p1, p2, p3)

    return ip


def copy_files():
    client.exec_command('[[ -d bin ]] || mkdir -p bin')
    rsync = 'rsync -avrp -e "ssh -o StrictHostKeyChecking=no -i {}"'.format(private_key)

    for source, dest in config['files'].items():
        cmd = "{} {} {}:{}".format(rsync, source, ip_address ,dest)
        os.system(cmd)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    config = None
    with open("config.json", 'r') as f:
        config = json.load(f)

    private_key = config['private-key-file']

    host_list = None
    if ',' not in config['hosts'] and os.path.isfile(config['hosts']):
        with open(config['hosts'], 'r') as f:
            host_list = [h.strip() for h in f.readlines()]
    else:
        host_list = config['hosts'].split(',')

    for host in host_list:
        ip_address = hostname_to_ip(host)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = paramiko.RSAKey.from_private_key_file(private_key)
        try:
            client.connect(hostname=ip_address, pkey=k)
            stdin, stdout, stderr = client.exec_command('ls -l')
            error = stderr.read().strip()
            if len(error) != 0:
                print(error)
                raise paramiko.ssh_exception.AuthenticationException
        except Exception as e:
            print("Skipping host {} with ip {}, reason: {}".format(host, ip_address, e))
            continue
        
        copy_files()
