from switch import Switch
from threading import Thread
from getpass import getpass


def vlan_thread(info, xls_file):
    with Switch(**info) as sw:
        sw.add_vlan(xls_file)


if __name__ == "__main__":
    threads = list()
    switches = [
        "192.168.1.215",
        "192.168.1.224",
        "192.168.1.234"
    ]
    username = "cyruslab"
    password = getpass()
    secret = getpass("Enable secret: ")
    for switch in switches:
        sw_info = dict(
            ip=switch,
            username=username,
            password=password,
            secret=secret
        )
        t = Thread(target=vlan_thread, args=(sw_info, "vlans.xlsx"))
        t.name = switch
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()
