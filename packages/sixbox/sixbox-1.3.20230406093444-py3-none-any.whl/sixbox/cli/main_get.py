
import yaml
import json
# from ruamel import yaml
from .commands import (getCases, getApps, getJobs, getDatasets, 
                    Pretty_printer, jsonstr2yamlstr, yamlstr2jsonstr, is_yaml, is_json, log)

from .commands.dataset_command import extract
'''
This file contains the code to get the overall information related to the CWL and case in cwldb and casedb
'''

def app_table(args, version):
    """
    Show the cwl App you have already had
    """

    # 初始化table
    table = Pretty_printer(template=[ "tag", "provider", "name","resource_id", "version"])

    if args.tag_or_id:
        for tag_or_id in args.tag_or_id:
            case = getApps(tag_or_id) 
            if case:
                
                name = case["name"]
                provider = case["provider"]
                resource_id = case["resource_id"]
                version = case["version"]
                if args.output == "all":
                    print(case)
                if args.output == "json":
                    print(yamlstr2jsonstr(case['content']))
                if args.output == "yaml":
                    print(eval(repr(case['content'])))
                elif args.output == "doc":
                    print(case["instruction"])
                elif args.output == "demo":
                    print(case["profile"])
                else:
                    table.add_row(["{}/{}:{}".format(provider, name, version), provider, name,  resource_id, version])
            else:
                # 没查到
                log.warning('unable to find App  {} !'.format(tag_or_id))
        if not args.output:
            print(table)
    else:
        # 默认打印所有
        for case in getApps():    
            name = case["name"]
            provider = case["provider"]
            resource_id = case["resource_id"]
            version = case["version"]
            table.add_row(["{}/{}:{}".format(provider, name, version), provider, name,  resource_id, version])
        print(table)


def case_table(args, version):
    """
    Case 详情
    """

    # 初始化cwl table
    cwl_table = Pretty_printer(template= [ "tag", "provider", "name","resource_id"])
   
    if args.tag_or_id:
        for tag_or_id in args.tag_or_id:
            case = getCases(tag_or_id)
            if case:
                name = case["name"]
                provider = case["provider"]
                resource_id = case["resource_id"]
                if args.output == "all":
                    print(case)
                if args.output == "json":
                    print(case["content"])
                if args.output == "yaml":
                    print(jsonstr2yamlstr(case["content"]))
                elif args.output == "doc":
                    print(case["instruction"])
                else:
                     cwl_table.add_row(["{}/{}".format(provider, name), provider, name,  resource_id])
            else:
                # 没查到
                log.warning('unable to find case  {} !'.format(tag_or_id))
        if not args.output:
            print(cwl_table)

    else:
        # 默认打印所有
        for case in getCases():    
            name = case["name"]
            provider = case["provider"]
            resource_id = case["resource_id"]
            cwl_table.add_row(["{}/{}".format(provider, name), provider, name,  resource_id])
        print(cwl_table)


def job_table(args, version):
    """
    Job 详情
    """

    # 初始化cwl table
    cwl_table = Pretty_printer(template= [  "name", "status", "created", "lastUpdated"])
   
    if args.job_name:
        for job_name in args.job_name:
            case = getJobs(job_name)
            if case:
                name = case["jobName"]
                status = case["status"]
                created = case["created"]
                lastUpdated = case["lastUpdated"]
                
                if args.output == "all":
                    print(case)
                if args.output == "yaml":
                    print(yaml.dump(case["request"], allow_unicode=True))
                elif args.output == "json":
                   print(json.dumps(case["request"]))
                elif args.output == "outcome":
                    print(case["output"])
                else:
                    cwl_table.add_row([ name, status, created, lastUpdated])
            else:
                # 没查到
                log.warning('Unable to find job  {} !'.format(job_name))
                           
        if not args.output:
            print(cwl_table)

    else:
        # 默认打印所有
        for case in getJobs():    
            name = case["jobName"]
            status = case["status"]
            created = case["created"]
            lastUpdated = case["lastUpdated"]
            cwl_table.add_row([ name, status, created, lastUpdated])

        print(cwl_table)


def dataset_table(args, version):
    """
    Show the dataset you have already had
    """

    # 初始化table
    table = Pretty_printer(template=[ "tag", "provider", "name","resource_id", "version"])

    if args.tag_or_id:
        for tag_or_id in args.tag_or_id:
            case = getDatasets(tag_or_id) 
            if case:
                name = case["name"]
                provider = case["provider"]
                resource_id = case["resource_id"]
                version = case["version"]
                if args.output:
                    dataset = json.loads(case["content"])
                    extract(dataset, dst=args.output)
      
                else:
                    table.add_row(["{}/{}:{}".format(provider, name, version), provider, name,  resource_id, version])
            else:
                # 没查到
                log.warning('unable to find Dataset  {} !'.format(tag_or_id))
        if not args.output:
            print(table)
    else:
        # 默认打印所有
        for case in getDatasets():    
            name = case["name"]
            provider = case["provider"]
            resource_id = case["resource_id"]
            version = case["version"]
            table.add_row(["{}/{}:{}".format(provider, name, version), provider, name,  resource_id, version])
        print(table)

