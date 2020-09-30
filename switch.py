from netmiko import ConnectHandler
from functools import wraps
from utility import config_template, xls_to_dict, check_nan


def config(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        self.session.enable()
        result = fn(self, *args, **kwargs)
        self.session.save_config()
        return result

    return wrapper


class Switch:
    def __init__(self, username="cisco", password="cisco", secret="", ip="192.168.1.1"):
        self.username = username
        self.password = password
        self.secret = secret
        self.ip = ip
        self.session = ConnectHandler(username=self.username,
                                      password=self.password,
                                      secret=self.secret,
                                      ip=self.ip,
                                      device_type="cisco_ios")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.disconnect()

    @config
    def add_vlan(self, xls_filename):
        vlans_config = config_template(template_file="vlans.j2")
        config_dict = xls_to_dict(xls_filename)
        for row in range(len(config_dict["vlan"])):
            if check_nan(config_dict["vlan"][row]) is None:
                raise ValueError("vlan column is compulsory and cannot be left blank.")
            vlan = config_dict["vlan"][row]
            name = check_nan(config_dict["name"][row])
            config = vlans_config.render(vlan=vlan, name=name)
            output = self.session.send_config_set(cmd for cmd in config.splitlines())
            print(output)
