
import os, sys
from ruamel import yaml
import json
from .logger import log


###################################
# config相关
##################################
# 默认的config配置信息
default_config = {
    'libPath': os.path.join(os.environ['HOME'], '.sixbox', 'lib'),
    'channel': 'https://www.sixoclock.net/api',
    'channels': {
        'main': 'https://www.sixoclock.net/api',
        'clients': 'https://bucket.sixoclock.net/resources/dist/history/linux'
    },

    'token': 'Fill in your token here'
}


def read_channel():
    """
    获取config.yaml中的channel
    """
    config_path = os.environ['HOME'] + '/.sixbox/config.yaml'
    initialize_config()
    try:
        with open(config_path, encoding='utf-8') as f: # 读取config文件中的libPath
            content = yaml.load(f, Loader= yaml.RoundTripLoader)
            return content['channels']
    except:
        log.error("Your configuration is incorrect, run folowing command to the configuration:\n\tsixbox config info \n\t and set it up with command:\n\t sixbox config set ")
        sys.exit()


def getConfig():
    """
    读取config文件
    """
    config_path = os.environ['HOME'] + '/.sixbox/config.yaml'
    initialize_config()

    try:
        with open(config_path, encoding='utf-8') as f:
            content = yaml.load(f, Loader= yaml.RoundTripLoader)
            default_config.update(json.loads(json.dumps(content)))
            return default_config
    except:
        log.error(
            """config ~/sixbox/config.yaml is not correct!!!
View with command:
    sixbox config info
Or set it up with command:
    sixbox config set
See more in: https://docs.sixoclock.net/clients/sixbox-linux.html#%E8%AF%BB%E5%86%99%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6
    """
        )
        sys.exit()

def setConfig(config):
    """
    配置config文件
    """
    config_path = os.environ['HOME'] + '/.sixbox/config.yaml'

    try:
        with open(config_path, 'w', encoding="utf-8") as nf:
            yaml.dump(config, nf, Dumper= yaml.RoundTripDumper)
    except:
        log.error("Your configuration is incorrect, run folowing command to the configuration:\n\tsixbox config info \n\t and set it up with command:\n\t sixbox config set ")
        sys.exit()


        


def initialize_config():
    """
    初始化config.yaml
    
    """
    # TODO:  config 添加一个配置，用于指定其它路径的配置（比如当前用户支持使用其他用户安装的sixbox并调用CWLdb内的应用）
    config_path = os.environ['HOME'] + '/.sixbox/config.yaml'

    if os.path.exists(config_path):
        pass
        
    else:
        log.warning("Config.yaml for sixbox  could not be found, we are trying to initialize ... ")

        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        os.makedirs(default_config['libPath'], exist_ok=True)
        with open(config_path, 'w', encoding="utf-8") as nf:
            yaml.dump(default_config, nf, Dumper= yaml.RoundTripDumper)


# 默认导入配置
Config = getConfig()