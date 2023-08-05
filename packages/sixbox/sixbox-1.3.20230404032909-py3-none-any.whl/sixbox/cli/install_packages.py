
import os, sys
import re
import requests
from subprocess import Popen
from .commands import downloadFile, post_updates, log, Config
from sixbox.cli import __version__

"""
this file contains code for install or update sixbox-linux
"""


# TODO: 显示下载进度和速度
def install_packages(args, command='install'):

    
    if args.prefix: # 指定位置安装
        if os.path.isdir(args.prefix):
             prefix=args.prefix
        else:
            log.error(" %s does not exists!!! " % args.prefix)
            sys.exit()
    else:

        prefix=os.path.dirname(sys.executable)

    isupdate = bool(command == 'update')
    isinstall = bool(command == 'install')
    
    if isupdate :
        if not args.packages or args.packages != "sixbox" :
            log.warning( "No package names supplied\n If you want to update to a newer version of sixbox, type:\n#\n# $ sixbox update --prefix %s sixbox\n" % prefix)
            sys.exit()

    if isinstall :
        if not (args.packages == "sixbox" or  re.match("^sixbox=\d+\.\d+\.\d+", args.packages)) :
            log.warning( "No package names supplied\nIf you want to install to a newer version of sixbox, type:\n#\n# $ sixbox install sixbox(sixbox=%s)\n" % ( __version__))
            sys.exit()
        
        
    
    if re.match("^sixbox=", args.packages) :     
        (pkg, req_ver)=args.packages.split("=", 2)
    else:
        pkg=args.packages
        
    # Current version
    current_ver = __version__
 
    # List of the latest versions
    if args.url:
        url = args.url +"/"+ pkg
        
    elif args.beta:
        url = "http://www.sixoclock.net/resources/dist/beta/linux/" + pkg
    else:
        url = Config["channels"]["clients"].rstrip("/") + '/'+ pkg
    
    if url.startswith("https://www.sixoclock.net"): # 旧的api

        # 请求sixoclock服务器
        try:
            log.info("update from channel: %s" %url)
            r = requests.get(url)
            raw_list = re.compile(r'<a.*?>(.*?)</a>').finditer(r.text.strip())
            
        except:
            log.error("Something wrong when download ..., please check the channel: %s" % url)
            sys.exit()
        
        print("raw_list: ", raw_list)
        
        # 解析软件列表
        ver_list=[]
        for v in raw_list:
            ver = v.group(1).replace('/', '')
            if re.match("^\D", ver) : continue
            ver_list.append(tuple(int(val) for val in ver.split('.')))

        latest_ver=".".join(map(str,max(ver_list)))

    else: # 新的api
        # 请求sixoclock服务器
        try:
            log.info("update from channel: %s" %url)
            r = requests.get(url+'/stable.txt')
            latest_ver = r.text.strip()
            
        except:
            log.error("Something wrong when download ..., please check the channel: %s" % url)
            sys.exit()

    if isupdate:
        if current_ver == latest_ver:
            log.info("{} is already the latest version. if you want to reinstall, use command:\n\tsixbox install {}={}".format(latest_ver, args.packages, current_ver))
            sys.exit()
        else:
            log.info("\nThe following packages will be UPDATED:\n")
            log.info("\n\tsixbox\tsixbox=%s\t-->\tsixbox=%s\n" %(current_ver, latest_ver))
            install_ver = latest_ver

    if isinstall:
        if re.match("^sixbox=", args.packages) :
            (pkg, req_ver)=args.packages.split("=", 2)
            # if tuple(int(va) for va in req_ver.split('.')) not in ver_list :
            #     log.error("The specified version for %s was not found : %s \n" %(pkg,req_ver))
            #     sys.exit()
        else:
            (pkg, req_ver)=(args.packages, latest_ver)

        if current_ver == req_ver and not args.force:
            log.info("package {}={} is already installed, if you want to reinstall, use the command:\nsixbox install {}={} --force ".format(pkg, req_ver, pkg, req_ver))
            sys.exit()
        else:
            log.info("\nThe following packages will be INSTALL:\n")
            log.info("\n\tsixbox\tsixbox=%s\n" %(req_ver))
            install_ver=req_ver
    
    # update/install
    log.info("Downloading %s/%s/sixbox ..." %(url, install_ver))
    url_f = url+"/"+install_ver+"/sixbox"
    filename = prefix+"/sixbox-latest"
    downloadFile(filename, url_f)
    try:
        downloadFile(filename, url_f)
    except:
        log.error("Something wrong in downloading, check the channel: %s" % url)
        sys.exit()
    
    # 替换旧版本
    Popen("mv -f " + filename + " " + prefix+"/sixbox && chmod 754 " + prefix+"/sixbox", shell=True)
    # 安装后处理
    post_updates()
    sys.exit("{} was successfully installed. ".format(pkg))
