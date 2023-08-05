# coding:utf-8

import os,json
from uuid import uuid4
import sys
import oss2
import urllib.request,urllib.parse
from .utils import   calculate_file_md5, percentage, encode_callback, pybyte

class bcolors:
    """
    配色
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def OssUploadfile( request, resource_id=None):
    '''
        文件上传：
        1. 校验文件类型和大小  2.  md5校验  3. oss callback
    '''

    bucket_name = os.getenv('OSS_BUCKET', 'sixoclock')
    endpoint = os.getenv('OSS_ENDPOINT', 'oss-cn-zhangjiakou.aliyuncs.com')
    args = request

    # 变量
    access_key_id=args["access_key_id"]
    access_key_secret=args["access_key_secret"]
    security_token=args["security_token"]

    file_name=args["path"]
    callbackUrl = args['callbackUrl'] 

    # # 检查文件类型和大小
    # if not CheckSize(file_name) :
    #     return response.SizeNo()
    # if not CheckType(file_name) :
    #     return response.TypeNo()
    
    # 检查md5
    if "MD5" not in args:
        md5 = calculate_file_md5(file_name)
    else:
        md5= args["MD5"]

    # TODO: 使用md5校验码+格式后缀为文件的oss上传哈名字
    # oss_filename= os.path.join(args["ossdir"].rstrip("*").lstrip(bucket_name+'/'), os.path.basename(file_name))  # 此处可以对文件进行重命名
    oss_filename= os.path.join(args["ossdir"].rstrip("*").lstrip(bucket_name+'/'), md5)

    # 生成文件id，uuid4
    id = args["id"] if "id" in  args  else str(uuid4())
    # 生成bucket
    # 使用临时访问凭证中的认证信息初始化StsAuth实例
    auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
    # 使用StsAuth实例初始化存储空间。
    bucket = oss2.Bucket(auth,endpoint, bucket_name)

    # 定义callback
    callback_dict = {
        'callbackUrl': callbackUrl,
        'callbackHost': 'oss-cn-zhangjiakou.aliyuncs.com',
        'callbackBody': "{\"bucket\":${bucket}, \"object\":${object},\"etag\":${etag},\"size\":${size},\"mimeType\":${mimeType}, \
                                        \"user\":${x:user},\"resourceid\":${x:resourceid}, \
                                        \"name\":${x:name},\"md5\":${x:md5},\"id\":${x:id}}",

        'callbackBodyType': 'application/json', # 设置发起回调请求的Content-Type, 'application/x-www-form-urlencoded'

    }

    encoded_callback = encode_callback(callback_dict)

    # 设置发起回调请求的自定义参数，由Key和Value组成，Key必须以x:开始.
    callback_var_params = {
        'x:user': args["username"],
        'x:resourceid': resource_id or id, # 用户名，data 所对应的资源id， 指定返回user 名字，同时对应callbackBody的指定user
        'x:md5': md5, 
        'x:name':args["name"], 
        'x:id': id
        }   
    # print(callback_var_params)
    encoded_callback_var = encode_callback(callback_var_params)

    # 上传并回调。
    params = {'x-oss-callback': encoded_callback, 'x-oss-callback-var': encoded_callback_var}

    print("push {}: ".format(id))
    try:
        result = bucket.get_object_meta(oss_filename) # 先查后计算
        # print(result.headers['Last-Modified']) 
        # print(result.headers['Content-Length']) 
        # print(result.headers['ETag']) 
        # print('Size: ', result.headers['Size']) 

        if result.status == 200:
            rate = 100
            print("\r\t"+"▇"*int(rate/2)+" "+'{0}% {1}/{2}'.format(rate, pybyte(result.headers['Content-Length']), pybyte(result.headers['Content-Length'])), end="")
            print(bcolors.OKGREEN  + " Pushed"+ bcolors.ENDC)
            return "six://" + oss_filename
    except:
        pass
    # print("oss_filename: ", oss_filename)
    # print("file_name: ", file_name)
    
    result = bucket.put_object_from_file(oss_filename, file_name, progress_callback=percentage)
    
    # # 日志记录信息
    # print('http status: {0}'.format(result.status))
    # # 请求ID。请求ID是请求的唯一标识，强烈建议在程序日志中添加此参数。
    # print('request_id: {0}'.format(result.request_id))      
    # # ETag是put_object方法返回值特有的属性。
    # print('ETag: {0}'.format(result.etag))
    # # HTTP响应头部。
    # print('date: {0}'.format(result.headers['date']))

    # 确认返回码
    if result.status == 200:
        # body = result.resp.read()
        print(bcolors.OKGREEN  + " Pushed"+ bcolors.ENDC)
        # print("body: ", body)
        # resbody = json.loads(body.decode('utf-8'));del resbody["msg"];del resbody["code"]
        # return response.callbackSuccess(data=resbody['data'])
        return "six://" + oss_filename
    elif result.status == 203:
        print(bcolors.FAIL  + " fail"+ bcolors.ENDC)
        return None
    elif result.status == 403:
        print(bcolors.FAIL  + "permission denied"+ bcolors.ENDC)
        return None
    else:
        print(bcolors.FAIL  + " fail"+ bcolors.ENDC)
        return None


def OssDeletefile( request, resource_id=None):
    '''
        文件删除：
        1. 校验文件类型和大小  2.  md5校验  3. oss callback
    '''

    bucket_name = os.getenv('OSS_BUCKET', 'sixoclock')
    endpoint = os.getenv('OSS_ENDPOINT', 'oss-cn-zhangjiakou.aliyuncs.com')
    args = request

    # 变量
    access_key_id = args["access_key_id"]
    access_key_secret = args["access_key_secret"]
    security_token = args["security_token"]
    file_name = args["path"]
    callbackUrl = args['callbackUrl'] 

    

    # TODO: 使用md5校验码+格式后缀为文件的oss上传哈名字
    oss_filename= os.path.join(args["ossdir"].rstrip("*").lstrip(bucket_name+'/'), md5)

    # 生成bucket
    # 使用临时访问凭证中的认证信息初始化StsAuth实例
    auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
    # 使用StsAuth实例初始化存储空间。
    bucket = oss2.Bucket(auth,endpoint, bucket_name)

    # 定义callback
    callback_dict = {
        'callbackUrl': callbackUrl,
        'callbackHost': 'oss-cn-zhangjiakou.aliyuncs.com',
        'callbackBody': "{\"bucket\":${bucket}, \"object\":${object},\"etag\":${etag},\"size\":${size},\"mimeType\":${mimeType}, \
                                        \"user\":${x:user},\"resourceid\":${x:resourceid}, \
                                        \"name\":${x:name},\"md5\":${x:md5},\"id\":${x:id}}",

        'callbackBodyType': 'application/json', # 设置发起回调请求的Content-Type, 'application/x-www-form-urlencoded'

    }

    encoded_callback = encode_callback(callback_dict)

    # 设置发起回调请求的自定义参数，由Key和Value组成，Key必须以x:开始.
    callback_var_params = {
        'x:user': args["username"],
        'x:resourceid': resource_id or id, # 用户名，data 所对应的资源id， 指定返回user 名字，同时对应callbackBody的指定user
        'x:md5': md5, 
        'x:name':args["name"], 
        'x:id': id
        }   
    encoded_callback_var = encode_callback(callback_var_params)

    # 上传并回调。
    params = {'x-oss-callback': encoded_callback, 'x-oss-callback-var': encoded_callback_var}

    print("push {}: ".format(id))
    try:
        result = bucket.get_object_meta(oss_filename) # 先查后计算

        if result.status == 200:
            rate = 100
            print("\r\t"+"▇"*int(rate/2)+" "+'{0}% {1}/{2}'.format(rate, pybyte(result.headers['Content-Length']), pybyte(result.headers['Content-Length'])), end="")
            print(bcolors.OKGREEN  + " Pushed"+ bcolors.ENDC)
            return "six://" + oss_filename
    except:
        pass
    
    result = bucket.put_object_from_file(oss_filename, file_name, progress_callback=percentage)


    # 确认返回码
    if result.status == 200:
        # body = result.resp.read()
        print(bcolors.OKGREEN  + " Pushed"+ bcolors.ENDC)
        # print("body: ", body)
        # resbody = json.loads(body.decode('utf-8'));del resbody["msg"];del resbody["code"]
        # return response.callbackSuccess(data=resbody['data'])
        return "six://" + oss_filename
    elif result.status == 203:
        print(bcolors.FAIL  + " fail"+ bcolors.ENDC)
        return None
    elif result.status == 403:
        print(bcolors.FAIL  + "permission denied"+ bcolors.ENDC)
        return None
    else:
        print(bcolors.FAIL  + " fail"+ bcolors.ENDC)
        return None
