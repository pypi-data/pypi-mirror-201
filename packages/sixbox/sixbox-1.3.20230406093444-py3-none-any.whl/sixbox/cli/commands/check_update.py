
import time, re
import requests
from tqdm import tqdm
import sys

from sixbox.cli.version import __version__
from .config_command import Config
from .db_command import getLib
from .logger import log

class Args():

    def __init__(self, args) -> None:
        self.packages = args["packages"]
        # self.prefix = args["prefix"] or None


def get_updates():
    """ 检查软件跟新"""

    latest_version = get_latest_ver()

    # TODO:  改为定时更新而不是实时更新以降低访问sixoclock.net 的频次
    if __version__ < latest_version:
        print('NOTE: The lates version of sixbox is {}, you can update with the command `sixbox update`.\n'.format(latest_version))
        # if askToUser(notes='Do you want to update? Please input y/N: '):
        #     args = Args(args = {"packages": "sixbox"})
        #     install_packages(args, command='update')
    else:
        pass


def get_latest_ver(url=None):
    """
    获取sixbox最新版本
    """

    # TODO:  改为定时更新而不是实时更新以降低访问sixoclock.net 的频次
    if not url:
        url = Config["channels"]["clients"].rstrip("/")
    # 请求sixoclock服务器
    try:
        r = requests.get(url)
        raw_list = re.compile(r'<a.*?>(.*?)</a>').finditer(r.text.strip())
        
    except:
        log.warning("something wrong, cannot check for updates ...")
        return 0.0001

    # 解析软件列表
    ver_list=[]
    for v in raw_list:
        ver = v.group(1).replace('/', '')
        if re.match("^\D", ver) : continue
        ver_list.append(tuple(int(val) for val in ver.split('.')))
    latest_ver = ".".join(map(str,max(ver_list)))

    return latest_ver


def downloadFile( name, url):
    """
    下载文件
    """

    headers = {'Proxy-Connection':'keep-alive'}
    r = requests.get(url, stream=True, headers=headers)
    length = float(r.headers['content-length'])
    data_size = length/1024/1024

    if r.status_code != 200:
        log.error("Something wrong in downloading, check the url: %s" % url)
        sys.exit()
    count = 0
    count_tmp = 0
    time1 = time.time()
    # print('download：{}, size {:.2f}MB'.format(url, length/1024/1024))
    with open(name, 'wb') as f:
        for data in tqdm(iterable=r.iter_content(1024*1024), total=data_size, desc='downloading {}'.format(name), unit='MB'):
            f.write(data)
        # for chunk in r.iter_content(chunk_size = 512):
        #     if chunk:
        #         f.write(chunk)
        #         count += len(chunk)
        #         if time.time() - time1 > 2:
        #             p = count / length * 100
        #             speed = (count - count_tmp) / 1024 / 1024 / 2
        #             count_tmp = count
                    
        #             print( 'download: {} {:.2f}%  Speed: {:.2f}M/S'.format(url, p, speed))
        #             time1 = time.time()

        # print( name + ': downloaded\n')

def post_updates():
    """
    sixbox 更新后处理
    """

    # 创建lib目录
    getLib()
    # 初始化config.yaml如果config.yaml不存在