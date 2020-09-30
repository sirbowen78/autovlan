import os
from numpy import nan
from pandas import ExcelFile
from jinja2 import Environment, FileSystemLoader


def find_file(base_path="C:\\", filename=None):
    for root, subdirs, files in os.walk(base_path):
        if filename in files:
            return os.path.join(root, filename)


def check_nan(test_obj):
    """
    if there is nan object change to None object, otherwise
    return the original value.
    :param test_obj:
    :return:
    """
    return test_obj if test_obj is not nan else None


def config_template(template_path="templates", template_file=None):
    env = Environment(loader=FileSystemLoader(template_path))
    return env.get_template(template_file)


def xls_to_dict(xls_filename):
    template_file_path = find_file(filename=xls_filename)
    xls = ExcelFile(template_file_path)
    return xls.parse("vlans").to_dict()