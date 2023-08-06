import os
import json
from prettytable import PrettyTable
from .commands import  libMaps, AppWriter, file_read

"""
This file contains the code to get the overall information related to the CWL Workflow in cwldb
"""


def cwls_table(args, version):
    """
    Show the cwl file you have already had
    """

    # 初始化table
    table = PrettyTable()
    table.field_names = [ "tag", "provider", "name","resource_id", "version"]
    table.add_row([" "*8]*5)
    table.border = 0
    table.align = 'l'
    table.right_padding_width =4


    metapath = libMaps["cwl_metadata"] # 读取config文件中的libpath
    if os.path.isdir(metapath):
        for pipe in os.listdir(metapath):
            with open(os.path.join(metapath, pipe), 'r', encoding='utf-8') as pipe_f:
                pipes=json.load(pipe_f)
                pipes["content"] = file_read(os.path.join(libMaps["cwl_content"], pipes["resource_id"]))
                AppWriter(pipes)

                name = pipes["name"]
                provider = pipes["provider"]
                resource_id = pipes["resource_id"]
                version_file = pipes["version"]
                table.add_row(["{}/{}:{}".format(provider, name, version_file), provider, name,  resource_id, version_file])


    print(table)
