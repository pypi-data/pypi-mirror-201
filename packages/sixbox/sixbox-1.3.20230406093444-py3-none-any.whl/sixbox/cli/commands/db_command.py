import os
from .config_command import Config
from .utils import data_flatten,  file_read
# from .check_update import get_updates

# 定义lib目录树，DirType表征目录，FileType表征文件。
lib_schemas = {
    "version": "v1.0",
    "resource": {
        "pipe": {
            "cwldb": {
                "repositories.json": "{}",
                "content": "DirType", 
                "metadata": "DirType",
            }
        },

        "case": {
            "casedb": {
                "repositories.json": "{}",
                "content": "DirType", 
                "metadata": "DirType",
            }
        },

        "dataset": {
            "datasetdb": {
                "repositories.json": "{}",
                "content": "DirType", 
                "metadata": "DirType",
            }
        },
    },

    "runtimes": {
        "cwl.runtime": "DirType", 
        "repositories.json": "{}",
        "tmp": "DirType"
        }

}

def initialize_lib():
    """
    初始化sixbox lib目录
    
    """

    # 批量依据目录树创建文件
    lib_path = Config["libPath"]
    for dir in set(data_flatten('', lib_schemas)):
        path = os.path.join(lib_path.rstrip('/'), dir[0].lstrip('/'))
        # 创建目录
        if not os.path.exists(path) and dir[1] == "DirType":
            os.makedirs(path)

        if not os.path.exists(path) and dir[1] != "FileType":
            # 先创建目录
            root_path = os.path.dirname(path)
            if not os.path.exists(root_path):
                os.makedirs(root_path)
            with open(path, 'w') as f:
                f.write(dir[1])

def getLib():
    """
    获取sixbox lib目录结构
    """

    initialize_lib() # 初始化
    # get_updates() # 检查更新

    libPath= Config["libPath"]
    libMaps = {
        "version": os.path.join(libPath, "version"),
        "cwldb": "",
        "cwl_repositories": os.path.join(libPath,'resource/pipe/cwldb/repositories.json'),
        "cwl_content": os.path.join(libPath, "resource/pipe/cwldb/content"),
        "cwl_metadata": os.path.join(libPath,"resource/pipe/cwldb/metadata"),

        "casedb": "",
        "case_repositories": os.path.join(libPath,'resource/case/casedb/repositories.json'),
        "case_content": os.path.join(libPath,"resource/case/casedb/content"),
        "case_metadata": os.path.join(libPath,"resource/case/casedb/metadata"),

        "datasetdb": "",
        "dataset_repositories": os.path.join(libPath,'resource/dataset/datasetdb/repositories.json'),
        "dataset_content": os.path.join(libPath,"resource/dataset/datasetdb/content"),
        "dataset_metadata": os.path.join(libPath,"resource/dataset/datasetdb/metadata"),

        "runtimes_home" : os.path.join(libPath,"runtimes/cwl.runtime"),
        "job_repositories" : os.path.join(libPath,"runtimes/repositories.json"),
        "runtimes_tmp": os.path.join(libPath,"runtimes/tmp")

    }

    return libMaps
    

## 加载lib目录结构
libMaps = getLib()


