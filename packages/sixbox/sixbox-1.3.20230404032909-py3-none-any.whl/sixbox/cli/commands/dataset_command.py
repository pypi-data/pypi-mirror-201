

import json
import re
import uuid
import tarfile
from jsonpath_ng.ext import parse
import os, sys
import yaml
from .logger import log
from .check_update import downloadFile
import shutil
import hashlib
import jsonschema
from jsonschema import validate

from .oss_command import OssUploadfile
from .datasets_command import *
from .utils import CheckType, check_uuid4, is_json, askToUser

# TODO:
# refs: 
#   1. json schema 校验功能实现，http://donofden.com/blog/2020/03/15/How-to-Validate-JSON-Schema-using-Python
#                               https://python-jsonschema.readthedocs.io/en/stable/
#   2. json 增删查改功能： https://github.com/h2non/jsonpath-ng/issues/44
        # https://blog.csdn.net/lemonbit/article/details/119880803

# 本文件包含file yaml解析类datasetPaser()以及一些其它辅助函数。



def rm_file(id_full_path, data_resource):
    """
    删除指定id的文件记录

    id_full_path: 绝对索引路径
    """

    # parse('$..id.`parent`').filter(lambda x: x == file_id, data_resource)
    try:
        parse(id_full_path).filter(lambda _: True, data_resource)
    except:
        pass



def list_files(data_resource, id_based=True, path_only=False, location_only=False):
    """
    列出文件对象的所有文件记录，包含辅助文件
    """
    if id_based:
        expr = '$..id.`parent`'
    else:
        expr = '$..name.`parent`'

    objs = parse(expr).find(data_resource)
    if path_only == True:
        return [str(match.full_path) for match in parse(expr).find(data_resource)]
    if location_only == True:
        return [match.value['location'] for match in parse(expr).find(data_resource)]
  
    # return dict(zip([str(match.full_path) for match in objs], [match.value for match in objs]))
    return objs



def add_files(id_full_path='$', data_resource={}, file_obj=None, type="directory"):
    """
    向指定的文件对象添加文件，默认向当前 文件对象根目录添加
    full_path: 表征待添加文件的对象索引路径（父文件对象）
    file_obj: 添加的文件对象（子文件对象）
    type: 指示所添加的文件类型，可选项为"secondaryFiles", "directory"
    """

    # # 新增元素

    # id_expr = id_full_path + '.`parent`' + '.resources'
    id_expr = id_full_path  + '.' + type

    id_len = [match.value for match in parse(id_expr + '.`len`').find(data_resource)]
    print(id_len)

    # 判断原有文件夹是非空
    if id_len:
        id_add_expr = id_expr + '.[{}]'.format(id_len[0])
    else:
        id_add_expr = id_expr + '.[0]'

    matches = parse(id_add_expr ).find_or_create(data_resource)
    for match in matches:
        match.full_path.update(data_resource, file_obj)
    
    print('after add: ', [match.value for match in parse(id_expr + '.`len`').find(data_resource)])
    print('查找辅助文件：',  [match.value for match in parse(id_expr + '.[0]').find(data_resource)] )


def update_file(id_full_path='$', data_resource={}, file_obj=None):
    """
    更新指定path的内容，若不存在，则创建
    """

    matches = parse(id_full_path).find_or_create(data_resource)
    for match in matches:
        match.full_path.update(data_resource, file_obj)


def get_file(file_id, data_resource):
    """
    获得指定id下的文件记录
    
    return: full_path, file object
    """

    objs = list_files(data_resource)

    for match in objs:
        if file_id == match.value["id"]:
            return str(match.full_path), match.value
    return None, None




def extract(data_resource, file_id=None, dst="./data"):
    """
    提取数据集到指定目录
    file_id: 要提取的文件记录，可以是单个文件记录或者整个dataset
    dst: 提取到目标目录下，默认为当前工作目录
    """
    if not os.path.exists(dst):
        os.makedirs(dst)

    if file_id is not None:
        _, data_resource = get_file(file_id, data_resource)
        
    locations = path_extract(data_resource, dst)

        

def pack(file_name, files, dst):
    """
    提取指定目录/文件/文件列表为一个数据集
    file_name: 新的数据集名字，可以是单个文件记录或者整个dataset
    files: dict, {file:"/data/a.bam", secondaryFiles:["/data/a.bam.bai", "/data/a.bam.fai"]}
    dst: 待提取的目标目录，如果为文件或目录

    usage: -i(include) /data/a.txt -s(secondaryFiles,list) '/data/a.txtx, /opt/b.csv'
    """

    pass

def pack_from_file(path):
    """
    从文件读入
    """

    all_datasets = []
    try:
        with open(path, encoding='utf-8') as f: # 读取config文件中的libPath
            datasets = yaml.safe_load_all(f)
            
            num = 0
            for dataset in datasets:
                num+=1
                if num >1:
                    log.warning("Warning: Contains multiple descriptions,and the others are ignored")
                    break
                # 校验
                is_valid, msg = validate_json(dataset)
                if not is_valid:
                    print(msg)
                    sys.exit()

                # 规范化
                dataset =  path_update(dataset, clean=False, upload=False, resources=set())
                all_datasets.append(dataset)
    except Exception as err:
        print(err)
        log.error("Not a valid dataset description yaml/json file.")
        sys.exit()

    return all_datasets
    # except:
    #     # log.error("path specified is not found, check it!!! ")
    #     print("cannot parser file: {}".format(path))
    #     sys.exit()



class string(str):
    def replace(self,regex,cls):
        self = re.sub(regex,cls,self)
        this = string(self)
        return this
 
# a = '{ name : abc}'
# b = string(a)
# b.replace('{\s*','{"').replace('\s*:\s*','":"').replace('\s*}','"}')


# print("dataset_exp:" , dataset_exp)
# files = list_files(dataset_exp, id_based=False, path_only=False, location_only=False)

# print("files: ", files.keys())
# for file in files.keys():

#     char_li = {'\$':'./', 'secondaryFiles':'', '\[\d+\]':''}
#     print("\nfile: ", file)
#     file = string(file)
#     for char in char_li.keys():
#         print("file replaceing: ", file.replace(char, char_li[char]))
#         file = file.replace(char, char_li[char])
#     print("file replaced: ", file)
# print(parse('$..name.`parent`').find(dataset_exp))


def get_filelist(dir, Filelist):
 
    newDir = dir
    if os.path.isfile(dir):
        Filelist.append(dir)
        # # 若只是要返回文件文，使用这个
        # Filelist.append(os.path.basename(dir))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            get_filelist(newDir, Filelist)
 
    return Filelist



def push():
    """
    1. 解析yaml，并初始化yaml然后上传至云端
    2. 逐个上传yaml中指定的文件，最后上传修改后的yaml或者间隔几个文件后同步修改后的yaml？
    4. 传输中断的处理
    """
    pass


def path_update(dataset, clean=False, upload=False, resources=set()):
    """
    1. 规范化所给dataset的yaml，添加必须字段 
    2. 更新yaml, 上传本地文件到云端，并同步替换location为云端路径

    dataset 的 path字段为必须项目
    clean: 脱敏，清除本地路径记录
    upload: True or False, 是否同时上传至云端
    sync: 是否同步数据到datahub
    resources: 同目录所有文件/目录记录

    TODO: 判断 同一目录下辅助文件与列表内其它文件/目录名字不能重复（实际都存在于同一个文件夹下）
    """
    # 本地修改yaml，直接上传至服务端
    # 逐个调用服务端api上传文件，由服务端完成yaml的生成与整合

    # resources = resources
    if isinstance( dataset, dict):

        if "id" not in dataset or not check_uuid4(dataset["id"]):  # id 为必须项
            dataset["id"] = str(uuid.uuid4())
        if "location" not in dataset:  # location 为必须项
            dataset["location"] = dataset["path"]
        if dataset["name"] not in resources:
            resources.add(dataset["name"])
        else:
            log.warning("Warning: Duplicate files or directories {} with id: {} already exist at the same level. It is not allowed that a file with the same name both in a Directory  or secondaryFiles field at the same level).".format(dataset["name"], dataset["id"]))
            sys.exit()


        if "secondaryFiles" in dataset: # 处理辅助文件
             path_update(dataset["secondaryFiles"], clean, upload, resources=resources)
             
        if dataset["class"] == 'Directory': # 条目为目录
            if "listing" in dataset.keys() and dataset["listing"]:
                resources = set()
                for fn in dataset["listing"]:
                    path_update(fn, clean, upload, resources=resources)
                dataset['location'] = "six://"
            else:
                if 'path'in dataset and os.path.exists(dataset['path']): # 从本地提取 
                    if os.path.isdir(dataset['path']):
                        
                        if clean:
                            dataset['path'] = ""
                        if upload:
                            # 打包压缩目录为单个文件后再上传
                            location = os.path.join(Config["libPath"],'datahub', hashlib.md5(dataset['path'].encode("utf8")).hexdigest()+ '.tar.gz') 
                            if not os.path.exists(os.path.dirname(location)):
                                os.makedirs(os.path.dirname(location))

                            make_targz(location, dataset['path']) # 压缩
                            with open(location, 'rb') as fr: # md5校验码
                                m = hashlib.md5(fr.read()).hexdigest()
                            dataset["path"] = location
                            dataset["hash"] = m
                            dataset['location'] = upload_file(dataset) # 上传，以path字段所指文件为准

                    else:
                        try: # 目录以打包形式给出，直接上传
                            if os.path.exists(dataset['path']) and CheckType(dataset['path']):
                                # dataset['location'] = "six://" + dataset['path']
                                if clean:
                                    dataset['path'] = ""
                                if upload:
                                    dataset['location'] = upload_file(dataset)
                                
                        except:
                            print("wrong format for directory, must be a directory or a tar file!!!")
                            sys.exit()
                else: # 从远程目录拉取后再上传
                    # 远程不支持指定目录
                    print("Skip, cannot find and parse path: ", dataset['location'])
                    pass
                    # file_sync(dataset['location'], dir_path+ ".tar.gz")

        if dataset["class"] == 'File': # 条目为文件
            if 'path'in dataset and os.path.exists(dataset['path']):
                if 'hash' not in  dataset or not  dataset['hash']:
                    with open(dataset['path'], 'rb') as fr: # md5校验码
                        dataset['hash'] = hashlib.md5(fr.read()).hexdigest()
                if clean:
                    dataset['path'] = ""
                if upload:
                    dataset['location'] = upload_file(dataset)

            else:
                #TODO: 报警告，文件不存在于本地
                pass
                # 本身是远程目录，暂不支持先拉取再上传
                # dataset['location'] = "six://" + dataset['location']
    
        return dataset

    elif isinstance( dataset, list): # 一组文件
        for fn in dataset:
             path_update(fn, clean, upload, resources=resources)
    else:
        print("wrong format")

    return dataset



def path_extract(dataset, dir, locations={}):
    """
    提取数据集为本地目录的组织形式
    返回：字典
    """
    if isinstance( dataset, dict):
        if "secondaryFiles" in dataset: # 处理辅助文件
             path_extract(dataset["secondaryFiles"], dir, locations)
             
        if dataset["class"] == 'Directory': # 条目为目录
            dir_path = os.path.join(dir, dataset["name"])
            if "listing" in dataset.keys() and dataset["listing"]:
                for fn in dataset["listing"]:
                    path_extract(fn, dir_path, locations)
            else:
                if 'path'in dataset and os.path.exists(dataset['path']): # 从本地提取 
                    if os.path.isdir(dataset['path']):
                        locations.update({os.path.basename(f):f for f in get_filelist(dataset['path'], [])})
                        file_sync(dataset['path'], dir_path)
                    else:
                        try: # 目录以打包形式给出，优先从本地检索与提取
                            print("untar: ", dir_path)
                            untar(dataset['path'], dir_path) # 尝试解压
                        except:
                            log.error("wrong format for directory, must be a directory !!!")
               
                else: # 从远程目录拉取
                    # 远程不支持指定目录
                    file_sync(dataset['location'], dir_path+ ".tar.gz")
                    untar(dir_path+ ".tar.gz", dir_path) # 尝试解压

        if dataset["class"] == 'File': # 条目为文件
            local_path = os.path.join(dir, dataset['name'])   
            if 'path'in dataset and os.path.exists(dataset['path']):
                file_sync(dataset['path'], local_path)
                locations.update({local_path:dataset['path']})
            else:
                file_sync(dataset['location'], local_path)
                locations.update({local_path:dataset['location']})
    
        return locations

    elif isinstance( dataset, list): # 一组文件
        for fn in dataset:
             path_extract(fn, dir, locations)
    else:
        print(type(dataset))
        log.error("wrong format")

    return locations


def file_sync(source, target):
    """
    source: 远程
    target: 本地
    """
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))
    if source.startswith(('http://', 'https://', "ftp://")): # 在线资源
        downloadFile(target, source)
    else: # 本地资源
        if os.path.isdir(source):
            shutil.copytree(source, target)
        else:
            shutil.copy(source, target)


def make_targz(output_filename, source_dir):
    """
        一次性打包整个根目录。空子目录会被打包。
        如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
    """
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def make_targz_one_by_one(output_filename, source_dir):
    """
        逐个添加文件打包，未打包空子目录。可过滤文件。
        如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
    """
    tar = tarfile.open(output_filename,"w:gz")
    for root,dir,files in os.walk(source_dir):
        for file in files:
            pathfile = os.path.join(root, file)
            tar.add(pathfile)
    tar.close()

def untar(fname, dirs):
    """
    解压打包文件
    """
    t = tarfile.open(fname)
    t.extractall(path=dirs)


def path_pack(path, max_depth=9999, depth=0, sync=False, tmp_dir="/tmp", hub_dir='./datahub', quiet=False, dataset=None):
    """
    打包目录为数据集
    path： 指定目录
    max_depth: 指定最深的目录，深度超过该值的目录将被打包
    sync: 是否同步到datahub

    md5校验码对于文件，对齐绝对路径字符串进行校验
    """
    
    dataset = [] if not dataset else dataset
    location=None
    depth += 1
    
    if os.path.isfile(path): # 添加单个文件
        files = [os.path.basename(path)]
        path = os.path.dirname(path)
    else:
        files = os.listdir(os.path.abspath(path))

    # 遍历目录
    for f in files:
        fn = os.path.abspath(os.path.join(path, f))
        log.info("parsing target {} ...".format(fn))
        # 是文件
        if os.path.isfile(fn): 
            with open(fn, 'rb') as fr:
                m = hashlib.md5(fr.read()).hexdigest()
            if sync: # 同步到本地数据仓库
                location = os.path.join(hub_dir, m)
                file_sync(fn, location)

            # path = fn if not sync else os.path.join(hub_dir, m)
            dataset.append( {
                "id": str(uuid.uuid4()),
                "name": f, 
                "class": "File", 
                "path": fn,
                "location": location,
                "bytes": os.path.getsize(fn),
                "hash": m,
                "schema": "",
                "sources": "",
                "licenses": "",
                "secondaryFiles":[]
            })
        

        # 目录
        if os.path.isdir(fn):
            m = None
            if depth >= max_depth: # 达到最大目录深度，打包压缩，只有在sync为True时有效
                if sync: # 同步到hub
                    location = os.path.join(hub_dir, hashlib.md5(fn.encode("utf8")).hexdigest()+ '.tar.gz') 
                    if not os.path.exists(os.path.dirname(location)):
                        os.makedirs(os.path.dirname(location))

                    make_targz(location, fn) # 压缩
                    with open(location, 'rb') as fr: # md5校验码
                        m = hashlib.md5(fr.read()).hexdigest()
        
            else: 
                if sync:
                    location = hub_dir

            # path = fn if not location else location
            dataset.append({
                    "id": str(uuid.uuid4()),
                    "name": f, 
                    "class": "Directory", 
                    "path": fn,
                    "location": location,
                    "bytes": None if not location else os.path.getsize(location),
                    "hash":  None if not location else m,
                    "schema": "",
                    "sources": "",
                    "licenses": "",
                    "listing": path_pack(os.path.abspath(os.path.join(path, f)), 
                                        max_depth=max_depth, depth=depth, sync=sync, 
                                        tmp_dir=tmp_dir, hub_dir=hub_dir) if depth < max_depth else []
                })

    return dataset


def commit(tag, tg_dir=None, from_file=False,  secondaryFiles=None, listFiles=None, sync=False):
    """
    提交到数据集仓库
    tg_dir: 目标数据集
    tag: 数据集名字
    from_file: 是否直接从yaml描述文件中解析 参数中用-f指代
    sync: 是否同步数据集中所指定的文件到本地datahub 仓库

    usage:
        1. commit dataset /data/a.txt 6oclock/dataset:v0.1
        2. commit dataset -f /data/a.txt 6oclock/dataset:v0.1
        3. commit dataset /data/a.txt 6oclock/dataset:v0.1 -s /data/a.txtx /opt/b.csv -l /data/a.txtx /opt/b.csv
    """
    if not ValidateTag(tag):
        log.error('Dataset tag is illegal, format must like `author/name:version` ...')
        sys.exit()

    tag = re.split("/|:", tag)
    payload = {
        'name': tag[1],
        'provider': tag[0],
        'version': tag[2],
        'resource_id': str(uuid.uuid4())
    }
    
    uri = '{}/{}:{}'.format(
                        payload["provider"],  
                        payload["name"],  
                        payload["version"])

    dataset = [] # 初始化
    hub_dir =  os.path.join(Config["libPath"],'datahub', payload['resource_id']) 

    if not tg_dir or not os.path.exists(tg_dir):
        log.error("Path {} not exist ...".format(tg_dir))
    

    if from_file: 
        dataset = pack_from_file(tg_dir)
    else:
        dat = path_pack(tg_dir, max_depth=2, hub_dir=hub_dir, sync=True, dataset=dataset) # 提取本地文件到datahub
        dataset.extend(dat)

    if secondaryFiles: # 辅助文件
        secondaryFiles_ = [] 
        for sf in secondaryFiles:
            if os.path.exists(sf): 
                dat = path_pack(sf, max_depth=2, hub_dir=hub_dir, sync=True) # 提取本地文件到datahub
                secondaryFiles_.extend(dat)
        dataset[0]["secondaryFiles"] = secondaryFiles_

    if listFiles: # 一组文件
        for sf in listFiles:
            if os.path.exists(sf): 
                dat = path_pack(sf, max_depth=2, hub_dir=hub_dir, sync=True, dataset=dataset) # 提取本地文件到datahub
                dataset.extend(dat)

    dataset = path_update(dataset)# 规范化与校验

    if not is_json(dataset):
        try:
            dataset = json.dumps(dataset, sort_keys=False, indent=4, separators=(',',': '))
        except:
            log.error("Invalid format, must be a json or yaml file")


    payload["content"] = dataset
   
    # 先查后改
    query = queryDatasets(uri)
    if query: # 如果存在，则替换
        log.warning('A Dataset  with the same name already exists. PLEASE confirm whether to replace it.')
        if askToUser(notes='Do you want to overwrite? Please input y/N: '):
            removeDatasets(uri)
            DatasetsWriter(payload) 
    else:
        DatasetsWriter(payload)
        
    log.info("Successfully submit to local Datasetsdb under the tag {}".format(uri))
    sys.exit()


    
def push(tag):
    """
    推送数据集到服务器
    """

def remove(tag):
    """
    删除数据集
    一般同步删除本地hub中的数据
    """
    

    removeDatasets(tag)


def upload_file(dataset, path="", name=""):
    """
    上传文件到服务端
    path: 文件本地路径
    name: 文件名
    """
    from sixbox.backend import Api
    import sixbox.backend.errors
    from . import  Config, libMaps, log, Unauthorized_log


    api = Api(Config["channel"], oauth_token=Config["token"])
    token = api.datasets.oss_token()
    request = {
        "username": token.username or "6oclcok",
        "access_key_id": token.access_key_id,
        "access_key_secret": token.access_key_secret,
        "security_token": token.security_token,
        "Bucket" : token.Bucket,
        "Region": token.Region,
        "ossdir": token.ossdir,
        "callbackUrl" : 'https://www.sixoclock.net' + token.callbackUrl,
        "MD5": dataset["hash"],
        "name": dataset["name"],
        "path": dataset["path"]
    }

    location = OssUploadfile(request)

    return location


def remove_file(files):
    """
    批量删除oss文件
    """
    pass


def get_schema():
    """This function loads the given schema available"""
    with open('sixbox/cli/commands/dataset_schema.json', 'r') as file:
        schema = json.load(file)
    return schema

def validate_json(json_data):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema()

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print("err:", err)
        err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message

def run_test():

    datasets = []
    with open("/home/yul/project/sixbox-linux/sixbox/cli/commands/dataset_example.yaml", encoding='utf-8') as f: # 读取config文件中的libPath
        docs = yaml.safe_load_all(f)
        for doc in docs:
            datasets.append(doc)
    dataset =  datasets[-1]

    tg_dir = './data'
    # extract(dataset, dst="./data1") # 提取到本地

    #     # TODO: 利用json_ng 模块动态添加文件到yaml描述中
    #     #       树结构：https://blog.csdn.net/usshe/article/details/111285247

    tmp_dir = "./tmp"
    data_hub =  "./"


    # is_valid, msg = validate_json(dataset)
    # print(msg)
    import sys
    from sixbox.backend import Api
    import sixbox.backend.errors

    from . import  Config, libMaps, log, Unauthorized_log

    # dataset = path_update(dataset)
    # path, value = get_file('453a3e85-b8a9-428c-8e00-b797eba12c26', dataset)
    # print("path: ", path)

    # rm_file(path, dataset)

    # objs = list_files(dataset)

    # print("objs: ", objs)
    # print("Config['token']: ", Config["token"])
    # api = Api(Config["channel"], oauth_token=Config["token"])
    # token = api.datasets.oss_token()
    # request = {
    #     "username": token.username or "6oclcok",
    #     "access_key_id":token.access_key_id,
    #     "access_key_secret": token.access_key_secret,
    #     "security_token": token.security_token,
    #     "Bucket" : token.Bucket,
    #     "Region": token.Region,
    #     "ossdir": token.ossdir,
    #     "callbackUrl" : 'https://www.sixoclock.net' + token.callbackUrl,

    #     "name": "e91a1f7f5eb4f639b9b443f02e8d35e9.tar.gz",
    #     "path": "./datahub/e91a1f7f5eb4f639b9b443f02e8d35e9.tar.gz"
    # }
    
    # location = OssUploadfile(request)
    # print("location: ", location)

    # location = upload_file(path="./datahub/e91a1f7f5eb4f639b9b443f02e8d35e9.tar.gz", name="e91a1f7f5eb4f639b9b443f02e8d35e9.tar.gz")
    # print("location: ", location)
    # dataset = path_pack( path="./data", max_depth=8, sync=True) # 提取本地文件到datahub

    # dataset = path_update(dataset, False, upload=True) # 上传dataset到远程
    # print("\ndataset:\n\n", yaml.dump(dataset, allow_unicode=True))

    # with open("pack.yaml", 'w') as fn:
    #     yaml.safe_dump(dataset, fn, allow_unicode=True)

    # 提交
    tag = '6oclock/test:v0.1'
    # commit(tag, tg_dir="./data", from_file=None,  sync=False)
    commit(tag, secondaryFiles=['pyproject.toml', 'LICENSE'], from_file=None,  sync=False)

    # downloadFile("hg19.chrM.fasta.sa" ,"http://bucket.sixoclock.net/resources/data/NGS/Homo_sapiens/Reference/hg19.chrM.fasta_BwaMem_index/hg19.chrM.fasta.sa")