
import os, sys
import json
from multiprocessing import Process, Lock


from .utils import check_uuid4, ValidateTag, file_read, json2file, file2json, jsonstr2yamlstr, yamlstr2jsonstr
from .db_command import libMaps
from .config_command import Config


################################
## dataset 读写相关
#########################################

def queryDatasets(URI):
    """
    查询并返回Dataset id
    """
    with open(libMaps["dataset_repositories"], 'r') as f:
        Datasets = json.load(f)

    # 指定查找
    if URI:
        querys = None
        # URI 为uuid4格式的dataset id
        if check_uuid4(URI):
            for case in Datasets.values():
                if case["resource_id"] == URI:
                    querys = case

        # URI 为tag
        if ValidateTag(URI):
            try:
                querys = Datasets[URI]
            except:
                querys = None
    return querys


def getDatasets(URI=None):
    """
    从repositories.json中读取dataset Dataset信息
    """
    if URI:
        querys = queryDatasets(URI)
        if querys:
            with open(os.path.join(libMaps["dataset_metadata"], querys["resource_id"]), "r") as json_file: # 根据tag获取
                Dataset= json.load(json_file)
            Dataset['content'] = file_read(os.path.join(libMaps["dataset_content"], querys["resource_id"]))
            return Dataset
        else:
            return None
    else:
        # 默认返回所有Dataset
        with open(libMaps["dataset_repositories"], 'r') as f:
            Datasets = json.load(f)
        return Datasets.values()


def removeDatasets(URI=None):
    """
    删除
    """
    with open(libMaps["dataset_repositories"], 'r') as f:
        Datasets = json.load(f)
 
    querys = queryDatasets(URI) # 先查后删除
    if querys:
        os.remove(os.path.join(libMaps["dataset_metadata"], querys["resource_id"]))
        os.remove(os.path.join(libMaps["dataset_content"], querys["resource_id"]))
        # 更新dataset_repositories
        Dataset_uri = '{}/{}:{}'.format(
                            querys["provider"],  
                            querys["name"],  
                            querys["version"])
        Datasets = file2json(libMaps["dataset_repositories"])
        Datasets.pop(Dataset_uri)
        json2file(libMaps["dataset_repositories"], Datasets)
        try:
            hub_dir =  os.path.join(Config["libPath"],'datahub', querys['resource_id'])
            os.removedirs(hub_dir)
        except:
            pass
        return True
    else:
        return False
 
def modifyDatasets(URI, payload):
    """
    修改标签
    """
 
    querys = queryDatasets(URI) # 先查后修改
    if querys:
        r_Dataset_uri = '{}/{}:{}'.format(
                    querys["provider"],  
                    querys["name"],  
                    querys["version"])
        q_Dataset_uri ='{}/{}:{}'.format(
                    payload["provider"],  
                    payload["name"],  
                    payload["version"])
        # 先读取内容
        with open(os.path.join(libMaps["dataset_metadata"], querys["resource_id"]), "r") as json_file: # 根据tag获取
                Dataset= json.load(json_file)
        Dataset.update(payload)

        # 更新仓库
        if q_Dataset_uri != r_Dataset_uri:
            # 当标签修改后，同步修改更新repositories
            DatasetManifestWriter(Dataset, old_uri=r_Dataset_uri)
        else:
            DatasetManifestWriter(Dataset)

        
        # 修改 content
        isContent = True
        try:
            Dataset['content']
        except:
            isContent = False
        DatasetsWriter(Dataset, isMeta=True, isContent=isContent, isRepositories=False)

        return True
    else:
        return False


def DatasetsWriter(payload, isMeta=True, isContent=True, isRepositories=True):
    """
    dataset 写入db
    """
    if isContent:
        with open(os.path.join(libMaps["dataset_content"], payload["resource_id"]), 'w', encoding='utf-8') as f:
            f.write(payload["content"])
    if isMeta:
        with open(os.path.join(libMaps["dataset_metadata"], payload["resource_id"]), 'w', encoding='utf-8') as f:
            f.write(json.dumps(payload))

    if isRepositories:
        DatasetManifestWriter(payload)


def DatasetManifestWriter(payload, old_uri=None):
    """
    修改Dataset 仓库文件
    """
    colFileds = ["provider", "name",  "resource_id", "version", "type", "updated_at", "description"]
    Dataset_uri = '{}/{}:{}'.format(
                                    payload["provider"],  
                                    payload["name"],  
                                    payload["version"])

    # 更新dataset_repositories
    Datasets = file2json(libMaps["dataset_repositories"])
    if old_uri:
        Datasets.pop(old_uri) # 删除旧数据

    Datasets[Dataset_uri] = {k:payload[k] for k in payload.keys() if k in colFileds}
    json2file(libMaps["dataset_repositories"], Datasets)


