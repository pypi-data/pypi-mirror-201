import os
import yaml
from .commands import Config, setConfig
import sys
"""
this file contain code for read or write Configuration file
e.g., write token into config.yaml, write channel into config.yaml, customize lib path
"""


def set_token(args, version):
    """
    write token into config file
    """
    token = args.token 

    Config['token'] = token
    setConfig(Config)

def add_channel(args, version):
    """
    write channel into config file
    """
    channel = args.channel_url

    Config['channel'] = channel # 写入channel
    setConfig(Config)



def print_info(args, version):
    """
    print config file content
    """
    config_path = os.environ['HOME'] + '/.sixbox/config.yaml'
    with open(config_path, encoding='utf-8') as f:
        print(yaml.dump(yaml.load(f, Loader=yaml.FullLoader)))
        # for line in f.readlines():
        #     print(line)


def set_lib(args, version):
    """
    Custom lib path
    """
    libpath = args.libpath

    Config['libPath'] = libpath # 自定义lib path

    if not os.path.exists(libpath):
        print("WARN: The path you specified does not exist ! ")
        sys.exit()
    setConfig(Config)
