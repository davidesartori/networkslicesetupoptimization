"""
Author: Gruppo 22 Networking II
Description: Module for importing configurations into scripts
"""


def get_conf(path):
    file_conf = open(path)
    conf_dict = {}

    lines = file_conf.readlines()

    for line in lines:
        key = line.split("=")[0].strip()
        value = line.split("=")[1].strip()

        conf_dict[key] = value

    file_conf.close()

    return conf_dict
