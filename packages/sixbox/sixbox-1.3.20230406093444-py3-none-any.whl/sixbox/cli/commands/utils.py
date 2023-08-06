
import os,io,sys
import re
import yaml
import json
import uuid
import random, string
import hashlib
import oss2
import filetype
import base64
from tqdm import tqdm
import time
import math

"""

一些小的辅助函数

"""


def rand_string(lens = 6):
    """
    生成指定位数的随机字符串
    """

    return ''.join(random.sample(string.ascii_letters+ string.digits, lens))


def check_uuid4(test_uuid, version=4):
    """
    检查给定字符串是否为uuid格式
    返回 True or False
    """
    try:
        return uuid.UUID(test_uuid).version == version
    except ValueError:
        return False


def tree(root, filters=['__pycache__', 'pyc','build','dist'], depth=0, prefix='|  '):
    """
    递归打印目录，类似linux tree命令
    用法：tree(path, 递归深度)
    """
    print(prefix*depth + '|-- ' + os.path.basename(root))
    depth+=1
    dirFiles = os.listdir(root)
    for df in dirFiles:
        if not df.split('.')[-1] in filters:
            path = os.path.join(root, df)
            if os.path.isdir(path):
                tree(path, filters, depth, prefix)
            else:
                print(prefix*depth + '|-- ' + df)


def askToUser(notes='Do you want to overwrite the file? Please input Y/N: ', ask_times=0, tolerances=2):
    """
    定义向用户询问内容，通过输入Y/N来确认用户意向
    tolerances设置允许用户输错的次数
    """

    user_ans = input(notes)
    if user_ans.upper() == "Y":
        return True

    elif user_ans.upper() == "N":
        return False
    else:
        if ask_times >= tolerances: # 达到设置的询问次数，退出询问
            print("INFO: Your input is wrong, exit. ")
            return False
        print("INFO: Your input is wrong, please try again.\n ")
        ask_times += 1
        askToUser(notes=notes, ask_times=ask_times)

        
                      
def _get_version_from_version_file(path):
    """
     读取version.py中记录的sixbox版本号
    """
    file_path = os.path.join(path, 'version.py')

    if os.path.isfile(file_path):
        with open(file_path, 'r') as fh:
            return fh.read().strip().split('=')[1].strip('\'')


def get_version(dunder_file): 
    """
    获取dunder_file路径
    """
    path = os.path.abspath(os.path.expanduser(os.path.dirname(dunder_file)))
    return _get_version_from_version_file(path)

def json2file(f_path, payload):
    """
    字典写入josn文件
    """
    with open(f_path, "w") as  f:
        json.dump(payload,f)   

def file2json(f_path):
    """
    json文件读取为字典
    """
    with open(f_path, "r") as  f:
        return json.load(f)  


def ValidateTag(tag):
    """
    判断tag是否符合规定格式
    """

    tag_pattern = re.compile(r'[0-9a-zA-Z\_\.\-]+/[0-9a-zA-Z\_\.\-]+:[0-9a-zA-Z\_\.\-]+') # provider/cwlname/version
    filed_start_pattern =  re.compile(r'^[^\_\.\-]') # 不能开头
    filed_end_pattern = re.compile(r'[^\_\.\-]$') # 不能结尾

    if tag_pattern.search(tag):
        patterns = []
        for filed in re.split('/|:', tag):
            patterns.extend([bool(filed_start_pattern.search(filed)),
                                bool(filed_end_pattern.search(filed))
                                ])
        return all(patterns)
    else:
        return False

def ValidateCaseTag(tag):
    """
    判断case tag是否符合规定格式
    """

    tag_pattern = re.compile(r'[0-9a-zA-Z\_\.\-]+/[0-9a-zA-Z\_\.\-]+') # provider/cwlname
    filed_start_pattern =  re.compile(r'^[^\_\.\-]') # 不能开头
    filed_end_pattern = re.compile(r'[^\_\.\-]$') # 不能结尾

    if tag_pattern.search(tag):
        patterns = []
        for filed in re.split('/|:', tag):
            patterns.extend([bool(filed_start_pattern.search(filed)),
                                bool(filed_end_pattern.search(filed))
                                ])
        return all(patterns)
    else:
        return False




def file_read(file):
    """
    文件读取
    """
    with open(file, "r", encoding='UTF-8') as f:
        return f.read()


def file_write(filename, data):
    """
    文件写入
    """
    with open(filename, "w", encoding='UTF-8') as f:
        f.write(data)





def is_json(strs):

    try:
        json.loads(eval(repr(strs)))
        return True
    except json.decoder.JSONDecodeError as err:
        # print(f"Invalid JSON: {err}") # in case json is invalid
        return False
    except:
        return False

def is_yaml(strs):
    """
    校验是否是yaml字符串，接收文件流
    """
    yaml_str = eval(repr(strs))
    try:
        yaml.load(yaml_str, Loader=yaml.FullLoader)
        return True
    except json.decoder.JSONDecodeError as err:
        # print(f"Invalid YAML: {err}") # in case json is invalid
        return False
    except Exception as err:
        # print(f"Invalid YAML: {err}")
        return False

def jsonstr2yamlstr(strs):
    """
    转换json 字符串为yaml字符串
    """
    
    json_str = is_json(strs)
    if json_str:
        payload = json.loads(eval(repr(strs)))
        return yaml.dump(payload, allow_unicode=True)
    else:
        return None

def yamlstr2jsonstr(strs):
    """
    转换yaml字符串为json 字符串
    """
    yaml_str = is_yaml(strs)
    if yaml_str:
        payload = yaml.load(eval(repr(strs)), Loader=yaml.FullLoader)
        json_str = json.dumps(payload)
        return json_str
    else:
        return yaml_str    

        
def json_validate(filename):
    
    with open(filename) as file:
        try:
            return json.load(file) # put JSON-data to a variable
        except json.decoder.JSONDecodeError as err:
            print(f"Invalid JSON: {err}") # in case json is invalid
        else:
            print("Valid JSON") # in case json is valid



def data_flatten(key, val, con_s='/', basic_types=(str,int,float,bool,complex,bytes)):
    """
    数据展开生成器,以键值对为最基础的数据
    param key: 键，默认为基础类型数据，不做进一步分析
    param val: 值，判断值的数据类型，如果为复杂类型就做进一步分析
    param con_s: 拼接符，当前级的键与父级键拼接的连接符，默认为_
    param basic_types: 基础数据类型元组，如果值的类型在元组之内，则可以输出
    return: 键值对元组
    """

    if isinstance(val, dict):
        for ck,cv in val.items():
            yield from data_flatten(con_s.join([key,ck]).lstrip('_'), cv)
    elif isinstance(val, (list,tuple,set)):
        for item in val:
            yield from data_flatten(key,item)
    elif isinstance(val, basic_types) or val is None:
        yield str(key).lower(),val





class TeeTextIO(io.TextIOBase):
    def __init__(self, target):
        self.target = target
        self.stringio = io.StringIO()
    def write(self, s):
        writecount = self.target.write(s)
        self.stringio.write(s[:writecount])
        return writecount


def calculate_file_md5(file_name, block_size=64 * 1024):
    '''计算文件的MD5
    :param file_name: 文件名
    :param block_size: 计算MD5的数据块大小，默认64KB
    :return 文件内容的MD5值
    '''
    with open(file_name, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    #return base64.b64encode(md5.digest())
    return hashlib.md5(data).hexdigest()

def percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前完成的百分比
    :param consumed_bytes: 已经上传/下载的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate))
        sys.stdout.flush()


# 定义回调参数Base64编码函数。
def encode_callback(callback_params):
    cb_str = json.dumps(callback_params).strip()
    return oss2.compat.to_string(base64.b64encode(oss2.compat.to_bytes(cb_str)))


def CheckType(file_name):
    '''检查文件类型是否符合预期'''
    ALLOWED_EXTENSIONS = set(['gz','zip','bz2','7z','rar', 'tar'])
    if filetype.guess(file_name) is None:
        print('Cannot guess file type!')
        return None
    elif filetype.guess(file_name).extension in ALLOWED_EXTENSIONS:
        # print('压缩文件！！')
        return True 
    else: 
        print('非法文件格式，必须为目录或者打包文件!')
        return False
 

 
def pybyte(size, dot=2):
    """
    转换文件大小
    """
    size = float(size)
    # 位 比特 bit
    if 0 <= size < 1:
        human_size = str(round(size / 0.125, dot)) + 'b'
    # 字节 字节 Byte
    elif 1 <= size < 1024:
        human_size = str(round(size, dot)) + 'B'
    # 千字节 千字节 Kilo Byte
    elif math.pow(1024, 1) <= size < math.pow(1024, 2):
        human_size = str(round(size / math.pow(1024, 1), dot)) + 'KB'
    # 兆字节 兆 Mega Byte
    elif math.pow(1024, 2) <= size < math.pow(1024, 3):
        human_size = str(round(size / math.pow(1024, 2), dot)) + 'MB'
    # 吉字节 吉 Giga Byte
    elif math.pow(1024, 3) <= size < math.pow(1024, 4):
        human_size = str(round(size / math.pow(1024, 3), dot)) + 'GB'
    # 太字节 太 Tera Byte
    elif math.pow(1024, 4) <= size < math.pow(1024, 5):
        human_size = str(round(size / math.pow(1024, 4), dot)) + 'TB'
    # 拍字节 拍 Peta Byte
    elif math.pow(1024, 5) <= size < math.pow(1024, 6):
        human_size = str(round(size / math.pow(1024, 5), dot)) + 'PB'
    # 艾字节 艾 Exa Byte
    elif math.pow(1024, 6) <= size < math.pow(1024, 7):
        human_size = str(round(size / math.pow(1024, 6), dot)) + 'EB'
    # 泽它字节 泽 Zetta Byte
    elif math.pow(1024, 7) <= size < math.pow(1024, 8):
        human_size = str(round(size / math.pow(1024, 7), dot)) + 'ZB'
    # 尧它字节 尧 Yotta Byte
    elif math.pow(1024, 8) <= size < math.pow(1024, 9):
        human_size = str(round(size / math.pow(1024, 8), dot)) + 'YB'
    # 千亿亿亿字节 Bront Byte
    elif math.pow(1024, 9) <= size < math.pow(1024, 10):
        human_size = str(round(size / math.pow(1024, 9), dot)) + 'BB'
    # 百万亿亿亿字节 Dogga Byte
    elif math.pow(1024, 10) <= size < math.pow(1024, 11):
        human_size = str(round(size / math.pow(1024, 10), dot)) + 'NB'
    # 十亿亿亿亿字节 Dogga Byte
    elif math.pow(1024, 11) <= size < math.pow(1024, 12):
        human_size = str(round(size / math.pow(1024, 11), dot)) + 'DB'
    # 万亿亿亿亿字节 Corydon Byte
    elif math.pow(1024, 12) <= size:
        human_size = str(round(size / math.pow(1024, 12), dot)) + 'CB'
    # 负数
    else:
        raise ValueError('{}() takes number than or equal to 0, but less than 0 given.'.format(pybyte.__name__))
    return human_size


# 发呆0.5s
def action():
    time.sleep(0.5)

def percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前完成的百分比
    :param consumed_bytes: 已经上传/下载的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print("\r\t"+"▇"*int(rate/2)+" "+'{0}% {1}/{2}'.format(rate, pybyte(consumed_bytes), pybyte(total_bytes)), end="")
        # sys.stdout.flush()
