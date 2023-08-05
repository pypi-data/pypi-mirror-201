
import os, sys
import json
from cwltool import main
from multiprocessing import Process, Lock


from .utils import check_uuid4, ValidateTag, file_read, json2file, file2json, jsonstr2yamlstr, yamlstr2jsonstr
from .db_command import libMaps
from .config_command import Config


################################
## CWL 读写相关
#########################################

def queryApp(URI):
    """
    查询并返回APP id
    """
    with open(libMaps["cwl_repositories"], 'r') as f:
        apps = json.load(f)

    # 指定查找
    if URI:
        querys = None
        # URI 为uuid4格式的CWL id
        if check_uuid4(URI):
            for case in apps.values():
                if case["resource_id"] == URI:
                    querys = case

        # URI 为tag
        if ValidateTag(URI):
            try:
                querys = apps[URI]
            except:
                querys = None
    return querys


def getApps(URI=None):
    """
    从repositories.json中读取CWL App信息
    """
    if URI:
        querys = queryApp(URI)
        if querys:
            with open(os.path.join(libMaps["cwl_metadata"], querys["resource_id"]), "r") as json_file: # 根据tag获取
                app= json.load(json_file)
            app['content'] = file_read(os.path.join(libMaps["cwl_content"], querys["resource_id"]))
            return app
        else:
            return None
    else:
        # 默认返回所有app
        with open(libMaps["cwl_repositories"], 'r') as f:
            apps = json.load(f)
        return apps.values()


def removeApps(URI=None):
    """
    删除
    """
    with open(libMaps["cwl_repositories"], 'r') as f:
        apps = json.load(f)
 
    querys = queryApp(URI) # 先查后删除
    if querys:
        os.remove(os.path.join(libMaps["cwl_metadata"], querys["resource_id"]))
        os.remove(os.path.join(libMaps["cwl_content"], querys["resource_id"]))
        # 更新cwl_repositories
        app_uri = '{}/{}:{}'.format(
                            querys["provider"],  
                            querys["name"],  
                            querys["version"])
        apps = file2json(libMaps["cwl_repositories"])
        apps.pop(app_uri)
        json2file(libMaps["cwl_repositories"], apps)
        return True
    else:
        return False
 
def modifyApps(URI, payload):
    """
    修改标签
    """
 
    querys = queryApp(URI) # 先查后修改
    if querys:
        r_app_uri = '{}/{}:{}'.format(
                    querys["provider"],  
                    querys["name"],  
                    querys["version"])
        q_app_uri ='{}/{}:{}'.format(
                    payload["provider"],  
                    payload["name"],  
                    payload["version"])
        # 先读取内容
        with open(os.path.join(libMaps["cwl_metadata"], querys["resource_id"]), "r") as json_file: # 根据tag获取
                app= json.load(json_file)
        app.update(payload)

        # 更新仓库
        if q_app_uri != r_app_uri:
            # 当标签修改后，同步修改更新repositories
            AppManifestWriter(app, old_uri=r_app_uri)
        else:
            AppManifestWriter(app)

        
        # 修改 content
        isContent = True
        try:
            app['content']
        except:
            isContent = False
        AppWriter(app, isMeta=True, isContent=isContent, isRepositories=False)

        return True
    else:
        return False




def AppWriter(payload, isMeta=True, isContent=True, isRepositories=True):
    """
    CWL 写入db
    """
    if isContent:
        with open(os.path.join(libMaps["cwl_content"], payload["resource_id"]), 'w', encoding='utf-8') as f:
            f.write(payload["content"])
    if isMeta:
        with open(os.path.join(libMaps["cwl_metadata"], payload["resource_id"]), 'w', encoding='utf-8') as f:
            f.write(json.dumps(payload))

    if isRepositories:
        AppManifestWriter(payload)


def AppManifestWriter(payload, old_uri=None):
    """
    修改app 仓库文件
    """
    colFileds = ["provider", "name",  "resource_id", "version", "type", "updated_at", "description"]
    app_uri = '{}/{}:{}'.format(
                                    payload["provider"],  
                                    payload["name"],  
                                    payload["version"])

    # 更新cwl_repositories
    apps = file2json(libMaps["cwl_repositories"])
    if old_uri:
        apps.pop(old_uri) # 删除旧数据

    apps[app_uri] = {k:payload[k] for k in payload.keys() if k in colFileds}
    json2file(libMaps["cwl_repositories"], apps)


def run_val(lock, cmd):
    """
    cwltool main函数子进程函数
    """
    lock.acquire()
    main.run(cmd)
    lock.release()


def ValidateCWL(cwl_path):
    """
    校验给定的CWL文件是否存在以及语法是否正确
    返回：ture，false
    """
    if cwl_path and os.path.exists(cwl_path): # 验证CWL文件是否有效
        cmd = ['--validate', cwl_path]
        lock = Lock()
        proc = Process(target=run_val, args=(lock, cmd,))
        proc.start()
        proc.join()
        if proc.exitcode == 0:
            is_valid = True
        else:
            print('ERRO: The specified CWL contains error syntax, please check your CWL file ...')
            sys.exit()
    else:
        print('ERRO: The CWL you specified does not exist, please specify a valid CWL address. ')
        sys.exit()

    return is_valid


# def app2json(payload: dict):

