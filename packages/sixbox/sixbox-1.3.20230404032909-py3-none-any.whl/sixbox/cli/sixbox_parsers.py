# encoding: utf-8
import argparse
import sys
from textwrap import dedent



from sixbox.cli import __version__


# 把所有模块都导入，以免do_call 动态导入导致的pyinstaller编译之后找不到包
# from .install_packages import install_packages
from .main_install import install
from .main_uninstall import remove
from .main_update import update
from .main_config import *

from .main_run import run
from .main_commit import commit_app, commit_case, commit_dataset
from .main_pull import pull_app, pull_case
from .main_push import push_app, push_case
from .main_tag import tag_app, tag_case, tag_dataset

from .main_rm import rm_app, rm_case, rm_job, rm_dataset
from .main_stop import stop_job
from .main_log import log_job

from .main_cwls import cwls_table
from .main_get import case_table, app_table, job_table, dataset_table
from .main_search import search_app, search_case

"""
This file contains information about sixbox related parameters and instructions for use
"""





def generate_parser():
    """
    定义参数解析器
    """

    parser = argparse.ArgumentParser(
        prog='sixbox',
        # formatter_class=argparse.RawDescriptionHelpFormatter, 
        # formatter_class=argparse.RawTextHelpFormatter, 
        description='sixbox is a tool for managing and running CWL workflow local and from www.sixoclock.net.'
    )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version='sixbox %s' % __version__,
        help='Show the sixbox version number.'  
    )
    sub_parsers = parser.add_subparsers(
            help='sub-command help'
    )

    sub_parsers.required = True


    ## 此处添加子命令
    # sixbox 全局设置和插件相关
    configure_parser_config(sub_parsers)
    configure_parser_update(sub_parsers)
    configure_parser_install(sub_parsers)
    configure_parser_uninstall(sub_parsers)

    # sixbox CWL 相关
    configure_parser_run(sub_parsers)
    configure_parser_pull(sub_parsers)
    configure_parser_push(sub_parsers)
    configure_parser_cwls(sub_parsers)
    configure_parser_commit(sub_parsers)
    configure_parser_tag(sub_parsers)
    configure_parser_rm(sub_parsers)

    # 查询
    configure_parser_get(sub_parsers)
    configure_parser_search(sub_parsers)
    # job
    configure_parser_stop(sub_parsers)
    configure_parser_log(sub_parsers)
    return parser



def do_call(args, parser):
    """
    动态导入包和函数，替换argpaser func指定的函数
    """

    try:
  
        relative_mod, func_name = args.func.rsplit('.', 1)
    except: # 命令没有绑定func时，打印命令帮助信息
        return 0

    # func_name should always be 'execute'
    from importlib import import_module
    module = import_module(relative_mod, __name__.rsplit('.', 1)[0])

    return getattr(module, func_name)(args, parser)


# #############################################################################################
#
# sub-parsers
#
# #############################################################################################

def configure_parser_run(sub_parsers):
    """
    定义CWL run命令

    动态参数部分参考：
        1. https://stackoverflow.com/questions/20165843/argparse-how-to-handle-variable-number-of-arguments-nargs
        2. https://stackoverflow.com/questions/45614229/argparse-when-using-a-remainder
    """

    run_descr = dedent("""
    Run CWL tools and Workflow locally.
    """)
    run_example = dedent("""
    Examples:

        sixbox run [CWL file] [YAML file]

        1. Run by specify a local CWL path:
        sixbox run ./test.cwl

        2. Run CWL sotre in CWLdb:
        sixbox run 6oclock/bwa:v0.1

        3. Run by CWL and YML:
        sixbox run ./test.cwl ./test.yml

        4. Run CWL in command line mode instead of specifying run parameters within yml:
        sixbox run 6oclock/bwa:v0.1 -mem test.fastq

        5. Builds the YML parameter template for the specified CWL:
        sixbox run --make-template 6oclock/bwa:v0.1
        
    """)
    parser_run = sub_parsers.add_parser(
        'run',
        formatter_class=argparse.RawTextHelpFormatter,
        description=run_descr,
        help=run_descr,
        epilog=run_example,
    )

    # run_target_options = p.add_argument_group("run CWL Workflow")
    parser_run.add_argument(
        'cwl',
        type=str,
        metavar='CWL-FILE',
        nargs='*',
        help="path or URL to a CWL Workflow, CommandLineTool, or ExpressionTool"
    )
    parser_run.add_argument(
        '--outdir',
        type=str,
        required=False,
        metavar='OUTDIR',
        help="Output directory"
    )
    parser_run.add_argument(
        '--make-template',
        action='store_true',
        dest='template',
        required=False,
        help="Generate a template input object"
    )
    parser_run.add_argument(
        '--udocker',
        action='store_true',
        dest='udocker',
        required=False,
        help="(Linux/OS X only) Use the udocker runtime for running containers "
    )
    parser_run.add_argument(
        '--singularity',
        action='store_true',
        dest='singularity',
        required=False,
        help="[experimental] Use Singularity runtime for running containers. Requires Singularity v2.6.1+ and Linux with kernel version v3.18+ or with overlayfs support backported."
    )
    parser_run.add_argument(
        '--yml', 
        type=str,
        metavar='YML-FILE',
        nargs="?",
        required=False,
        default=None,
        help='path or URL to a YAML or JSON formatted description of the required input values for the given cwl'
    )


    # 支持动态参数
    parser_run.add_argument( 
        'cwl_args', 

        nargs=argparse.REMAINDER,
    )
 
    parser_run.set_defaults(func='.main_run.run')


def configure_parser_update(sub_parsers):
    """
    定义sixbox或sixbox插件更新函数
    
    """
 
    update_descr = dedent("""
    Updates sixbox package to the latest compatible version.
    """)
    update_example = dedent("""

    Examples:

    update sixbox,

        sixbox update sixbox

    """)

    parser_update = sub_parsers.add_parser(
        'update',
        formatter_class=argparse.RawTextHelpFormatter,
        description=update_descr,
        help=update_descr,
        epilog=update_example,
    )
    parser_update.add_argument(
        'packages', 
        type=str,
        nargs='?',
        default = 'sixbox',
        metavar='packages',
        help='Packages to install or update, if not specified, default to sixbox'
    )
    parser_update.add_argument(
        '--url', 
        type=str, 
        metavar='URL',
        required=False, 
        help='Specify the sixbox update source, which must be a valid http link'
    )
    parser_update.add_argument(
        '--prefix', 
        type=str, 
        required=False,  
        metavar='sixbox-PATH',
        help='Full path to sixbox location'
    )
    parser_update.add_argument(
        '--beta', 
        action='store_true',
        dest='beta',
        required=False,
        help='Allows checking of the beta version'
    )
    # modules_update = import_module('main_update')
    parser_update.set_defaults(func='.main_update.update')


def configure_parser_install(sub_parsers):
    """
    定义sixbox插件安装函数
    """

    install_descr = dedent("""
    Install sixbox package.
    """)
    install_example = dedent("""

    Examples:

        1. Install sixbox with latest version:
        sixbox install sixbox

        2. Install the specified version of sixbox:
        sixbox install sixbox=1.2.20211102095206

    """)

    parser_install = sub_parsers.add_parser(
        'install',
        formatter_class=argparse.RawTextHelpFormatter,
        description=install_descr,
        help=install_descr,
        epilog=install_example,
    )
    parser_install.add_argument(
        'packages', 
        type=str, 
        metavar='package_name',
        help='Packages to install or update'
    )
    parser_install.add_argument(
        '--url', 
        type=str, 
        metavar='URL',
        required=False, 
        help='the url of sixbox repositorie'
    )
    parser_install.add_argument(
        '--prefix', 
        type=str, 
        required=False,  
        metavar='sixbox-PATH',
        help='Full path to sixbox location'
    )

    parser_install.add_argument(
        '--beta', 
        action='store_true',
        dest='beta',
        required=False,
        help='Allows checking of the beta version'
    )

    parser_install.add_argument(
        '--force', 
        action='store_true',
        dest='force',
        required=False,
        help='Force to install'
    )
    # modules_install = import_module('main_install')
    parser_install.set_defaults(func='.main_install.install')


def configure_parser_uninstall(sub_parsers):
    """
    
    定义sixbox插件卸载
    """
    parser_uninstall = sub_parsers.add_parser(
        'uninstall',
        help='uninstall a package'
    )
    # modules_remove = import_module('main_remove')
    parser_uninstall.set_defaults(func='.main_uninstall.remove')


def configure_parser_pull(sub_parsers):
    """
    定义pull CWL函数
    """

    pull_descr = dedent("""
    get CWL app or case from sixoclock.net.
    """)
    pull_example = dedent("""
    before you pull CWL Workflow from sixoclock.net, you should use 'CONFIG' command to set your sixbox config first.
    You can find pipe_id in https://www.sixoclock.net/application/pipes

    Examples:
    sixbox pull app $(app_id)
    sixbox pull case $(case_id)
    """)
    parser_pull = sub_parsers.add_parser(
        'pull',
        formatter_class=argparse.RawTextHelpFormatter,
        description=pull_descr,
        help=pull_descr,
        epilog=pull_example,
    )
    
    action_pull = parser_pull.add_subparsers(
        help='get resources from sixoclock.net ...'
    )

    # app
    parser_app = action_pull.add_parser(
        'app', 
        help='get CWL apps in CWLdb.'
    )
    parser_app.add_argument(
        'app', 
        type=str, 
        metavar='tag_or_id', 
        help='the CWL workflow tag or id from www.sixoclock.net'
    )

    parser_app.add_argument(
        '--force', 
        action='store_true',
        dest='force', 
        required=False,
        help='force pull'
    )
    parser_app.set_defaults(func='.main_pull.pull_app')

    # case
    parser_case = action_pull.add_parser(
        'case', 
        help='get case from sixoclock.net.'
    )
    parser_case.add_argument(
        'case', 
        type=str, 
        metavar='tag_or_id', 
        help='the case tag or id from www.sixoclock.net'
    )

    parser_case.add_argument(
        '--force', 
        action='store_true',
        dest='force', 
        required=False,
        help='force pull'
    )
    parser_case.set_defaults(func='.main_pull.pull_case')


def configure_parser_push(sub_parsers):
    """
    定义push CWL函数
    """

    push_descr = dedent("""
    push CWL app or case to sixoclock.net.
    """)
    push_example = dedent("""
    before you push CWL Workflow from sixoclock.net, you should use 'CONFIG' command to set your sixbox config first.
    You can find id or tag by commond `sixbox get app/case`

    Examples:
    sixbox push app $(CWL_tag)

    sixbox push case $(case_tag)
    """)
    parser_push = sub_parsers.add_parser(
        'push',
        formatter_class=argparse.RawTextHelpFormatter,
        description=push_descr,
        help=push_descr,
        epilog=push_example,
    )
    
    action_push = parser_push.add_subparsers(
        help='get resources for the local db..'
    )

    # app
    parser_app = action_push.add_parser(
        'app', 
        help='push CWL apps to sixoclock.net.'
    )
    parser_app.add_argument(
        'pipes', 
        type=str, 
        metavar='pipes', 
        help='the CWL workflow tag or id from local CWLdb'
    )

    parser_app.set_defaults(func='.main_push.push_app')

    # case
    parser_app = action_push.add_parser(
        'case', 
        help='push case to sixoclock.net.'
    )
    parser_app.add_argument(
        'cases', 
        type=str, 
        metavar='cases', 
        help='the case tag or id from local CWLdb'
    )

    parser_app.set_defaults(func='.main_push.push_case')

def configure_parser_config(sub_parsers):
    """
    定义config配置文件存取子命令处理函数
    """

    config_descr = dedent("""
    Modify configuration values in config.yaml.
    """)
    config_example = dedent("""
    You can get the token in the user center.

    Examples:

    add or change the token in config.yaml

        sixbox config set token $(token)

    custom lib path

        sixbox config set libpath $(lib_path)

    add or change the channel in config.yaml
        sixbox config add $(channel)

    show the config.yaml content
        sixbox config info
    """)

    parser_config = sub_parsers.add_parser(
        'config',
        formatter_class=argparse.RawTextHelpFormatter,
        description=config_descr,
        help=config_descr,
        epilog=config_example,
    )
    action_config = parser_config.add_subparsers(
        help='Modify configuration values in config.yaml.'
    )

    ## 添加子命令 set， set用于配置config.yaml文件
    parser_set = action_config.add_parser(
        'set', 
        help='Set parameters for the configuration file'
    )
    action_set = parser_set.add_subparsers(
        help='set value in config'
    )
    # 设置token
    parser_TOKEN = action_set.add_parser(
        'token', 
        help='Set up sixoclock.net personal access token, which you can get in the sixoclock site user center'
    )
    parser_TOKEN.add_argument(
        'token', 
        type=str, 
        metavar='token_string', 
        help='Set up sixoclock.net personal access token, which you can get in the sixoclock site user center, The token in the configuration file is related to the user\'s permissions.'
    )
    
    parser_TOKEN.set_defaults(func='.main_config.set_token')


    # 设置libPath, 默认CWLdb等从libPath读取
    parser_lib = action_set.add_parser(
        'libpath', 
        help='set path of local CWLdb, the default path is ~/.sixbox/lib .'
    )
    parser_lib.add_argument(
        'libpath', 
        type=str, 
        metavar='libpath_adress', 
        help='Specify a directory that sixbox uses for the CWLdb storage CWL Workflow.'
    )
    parser_lib.set_defaults(func='.main_config.set_lib')

    # 设置channel，channel约定了sixbox的开放api地址
    parser_add = action_config.add_parser(
        'add', 
        help='add values into config file'
    )


    action_add = parser_add.add_subparsers(
        help='add value in config'
    )
    parser_channel = action_add.add_parser(
        'channel', 
        help='add channel into config file'
    )

    parser_channel.add_argument(
        'channel_url', 
        type=str, 
        metavar='channel_url', 
        help='add channel for pull or push CWL to  www.sixoclock.net into config file'
    )
    
    parser_channel.set_defaults(func='.main_config.add_channel')


    # 打印当前用户配置文件信息
    parser_info = action_config.add_parser(
        'info', 
        help='Show the user configuration information for sixbox'
    )
    parser_info.set_defaults(func='.main_config.print_info')


def configure_parser_cwls(sub_parsers):
    """
    显示CWLdb内的CWL流程列表
    """
    cwls_help='Show the existing CWL Workflow in cwldb.'
    parser_cwls = sub_parsers.add_parser(
        'cwls',
        formatter_class=argparse.RawTextHelpFormatter,
        description=cwls_help,
        help=cwls_help,
    )

    parser_cwls.set_defaults(func='.main_cwls.cwls_table')

 
def configure_parser_get(sub_parsers):
    """
    显示cwldb和casedb中cwl和cwlc列表
    """
    get_descr = 'Show the messages of existing CWL app/case/job in local db.'
    get_example = dedent("""
    See Sixoclock Help document for for details on all the command.

    Examples:

    1. Show CWL App in db:

        sixbox get app

        sixbox get app 6oclock/bwa_mem

        sixbox get app 6oclock/bwa_mem -o demo

    2. Show CWL case in db:

        sixbox get case

        sixbox get case 6oclock/bwa_mem

        sixbox get case 6oclock/bwa_mem -o doc
    
    3. Show CWL job in db:

        sixbox get job

        sixbox get job bwa_mem

        sixbox get job bwa_mem -o yaml
    4. Show Dataset in db:

        sixbox get dataset

        sixbox get dataset bwa_mem

        sixbox get job bwa_mem -o ./data
    """)
    parser_get = sub_parsers.add_parser(
        'get',
        formatter_class=argparse.RawTextHelpFormatter,
        description=get_descr,
        help=get_descr,
        epilog=get_example,
    )
    
    # parser_get.add_argument(
    #     'cwl', 
    #     type=str, 
    #     metavar='CWL',
    #     default=None,
    #     help='show CWL Workflow in your cwldb'
    # )
    # parser_get.add_argument(
    #     'case', 
    #     type=str, 
    #     metavar='case',
    #     help='show CWLc in your casedb'
    # )

 
    parser_get.set_defaults(func='.main_get.app_table')
    
    action_get = parser_get.add_subparsers(
        help='get resources for the local db..'
    )

    # 设置token
    parser_app = action_get.add_parser(
        'app', 
        help='get CWL apps in CWLdb.'
    )
    parser_app.add_argument(
        'tag_or_id', 
        type=str, 
        nargs="*",
        metavar='app_tag', 
        # required=False,
        default=None,
        help='get CWL app.'
    )
    parser_app.add_argument(
        '-o', 
        '--output',
        type=str, 
        choices=['all', 'json', 'yaml', 'doc', 'demo'],
        metavar='output', 
        # required=False,
        default=None,
        help='get CWL app content with format and filter.'
    )

    parser_app.set_defaults(func='.main_get.app_table')

    # case
    parser_case = action_get.add_parser(
        'case', 
        help='get cases in Casedb.'
    )
    parser_case.add_argument(
        'tag_or_id', 
        type=str, 
        nargs="*",
        metavar='case_tag', 
        default=None,
        help='get CWL case.'
    )
    parser_case.add_argument(
        '-o', 
        '--output',
        type=str, 
        choices=['all', 'json', 'yaml', 'doc'],
        metavar='output', 
        default=None,
        help='get CWL case content with format and filter.'
    )
    parser_case.set_defaults(func='.main_get.case_table')

    # job
    parser_job = action_get.add_parser(
        'job', 
        help='get jobs in local db.'
    )
    parser_job.add_argument(
        'job_name', 
        type=str, 
        nargs="*",
        metavar='job_name', 
        # required=False,
        default=None,
        help='get CWL job messages.'
    )
    parser_job.add_argument(
        '-o', 
        '--output',
        type=str, 
        choices=['all', 'json', 'yaml', 'outcome'],
        metavar='output', 
        default=None,
        help='get CWL job content with format and filter.'
    )

    parser_job.set_defaults(func='.main_get.job_table')

    # Dataset
    parser_dataset = action_get.add_parser(
        'dataset', 
        help='get dataset in datasetdb.'
    )
    parser_dataset.add_argument(
        'tag_or_id', 
        type=str, 
        nargs="*",
        metavar='dataset_tag', 
        default=None,
        help='get dataset.'
    )
    parser_dataset.add_argument(
        '-o', 
        '--output',
        type=str, 
        # choices=['all', 'json', 'yaml', 'doc'],
        metavar='output', 
        default=None,
        required=False,
        help='extract dataset fo local path.'
    )
    parser_dataset.set_defaults(func='.main_get.dataset_table')

def configure_parser_commit(sub_parsers):
    """
    提交CWL到CWLdb
    """
    commit_descr = dedent("""
    Commit your resources (CWL app, case, dataset) into local db.
    """)
    commit_example = dedent("""
    See Sixoclock Help document for for details on all the command.

    Examples:

    Commit CWL app. `[CWL_INFO[:TAG]]` format like `provider/testcwlname:version3` 

        sixbox commit app ./bwa.cwl 6oclock/bwa:v0.1
    
    Commit Dataset. `[Dataset_INFO[:TAG]]` format like `provider/testdataset:version3` 

        1. commit file as a dataset.

            sixbox commit dataset ./singleCell.fpkm 6oclock/singleCell:v0.1

        2. commit file with secondaryFiles and/or array of files as a dataset.

            sixbox commit dataset /data/a.txt 6oclock/dataset:v0.1 -s /data/a.txtx /opt/b.csv -l /data/a.txtx /opt/b.csv

        3. commit directory as a dataset.
        
            sixbox commit dataset ./singleCell_dir 6oclock/singleCell:v0.2

    """)
    parser_commit = sub_parsers.add_parser(
        'commit',
        formatter_class=argparse.RawTextHelpFormatter,
        description=commit_descr,
        help=commit_descr,
        epilog=commit_example,
    )

    action_commit = parser_commit.add_subparsers(
        help='commit resources to the local db..'
    )

    # 提交app
    parser_app = action_commit.add_parser(
        'app', 
        help='commit CWL apps to CWLdb.'
    )
    parser_app.add_argument(
        'cwl_path', 
        type=str, 
        metavar='CWL-FILE',
        help='path to a CWL Workflow.'
    )
    parser_app.add_argument(
        'cwl_info', 
        type=str, 
        metavar='CWL_INFO',
        help='cwl information included provider, name, version'
    )
    # parser_app.add_argument(
    #     '--demo', 
    #     type=str, 
    #     metavar='demo',
    #     help='demo input for CWL app'
    # )
    # parser_app.add_argument(
    #     '--doc', 
    #     type=str, 
    #     metavar='doc',
    #     help='tutorials or document about the CWL app'
    # )
    # parser_app.add_argument(
    #     '-m',
    #     '--message', 
    #     type=str, 
    #     metavar='description',
    #     help='Commit description of the CWL app'
    # )

    # parser_app.add_argument(
    #     '-c',
    #     '--category', 
    #     type=str, 
    #     metavar='description',
    #     help='description of the CWL app'
    # )
    parser_app.set_defaults(func='.main_commit.commit_app')

    # 提交case
    parser_case = action_commit.add_parser(
        'case', 
        help='commit CWL case to db.'
    )
    parser_case.add_argument(
        'case_path', 
        type=str, 
        metavar='case_path',
        help='path to a CWL case.'
    )
    parser_case.add_argument(
        'case_info', 
        type=str, 
        metavar='case_info',
        help='case information included provider, name'
    )
    parser_case.set_defaults(func='.main_commit.commit_case')

    # 提交datasets
    dataset_commit_descr = dedent("""
    Commit file(s)/directory as a dataset.
    """)
    dataset_commit_example = dedent("""
    See Sixoclock Help document for for details on all the command.

    Examples:
    
    Commit Dataset. `[Dataset_INFO[:TAG]]` format like `provider/testdataset:version3` 
        1. commit file as a dataset.
            sixbox commit dataset ./singleCell.fpkm 6oclock/singleCell:v0.1
        2. commit file with secondaryFiles and/or array of files as a dataset.
            sixbox commit dataset /data/a.txt 6oclock/dataset:v0.1 -s /data/a.txtx /opt/b.csv -l /data/a.txtx /opt/b.csv
        3. commit directory as a dataset.
            sixbox commit dataset ./singleCell_dir 6oclock/singleCell:v0.2

    """)
    parser_dataset = action_commit.add_parser(
        'dataset', 
        help='commit dataset to db.',
        # epilog=dataset_commit_example,
    )
    parser_dataset.add_argument(
        'dir_path', 
        type=str,
        metavar='dataset_path',
        help='path to a dataset dir.'
    )
    parser_dataset.add_argument(
        'dataset_info', 
        type=str, 
        metavar='dataset_info',
        help='dataset information included provider, name'
    )
    parser_dataset.add_argument(
        '-f'
        '--from_file', 
        dest='from_file',
        action='store_true',
        default=None,
        required=False,
        help='path to a dataset describes file.'
    )

    parser_dataset.add_argument(
        '-l'
        '--listFiles',
        dest='listFiles',
        type=str, 
        required=False,
        default=None,
        nargs='+',
        metavar='listFiles',
        help=' paths to dataset files.'
    ) 
 
    parser_dataset.add_argument(
        '-s'
        '--secondaryFiles', 
        dest='secondaryFiles',
        type=str, 
        nargs='+',
        metavar='secondaryFiles',
        help='secondaryFiles paths to a dataset file.'
    )

    parser_dataset.set_defaults(func='.main_commit.commit_dataset')


def configure_parser_tag(sub_parsers):
    """
    重命名CWLdb内的CWL tag信息。
    """

    tag_descr = dedent("""
    Modify CWL app or case tag
    """)
    tag_example = dedent("""
    See Sixoclock Help document for for details on all the command.
    
    Examples:

    Modify CWL Workflow tag. `[CWL_INFO_TAG]` format like `provider/testcwlname:version3`
        sixbox tag [$(CWL resouece_id) or SOURCE_CWL_TAG] [TARGET_CWL_TAG]

        By ID:
        sixbox tag app 30479859-c02d-4a40-8e7d-92f9011ac9b8 6oclock/bwa:v0.1
        By Tag:
        sixbox tag app 6oclock/bwa:v0.1 sixoclock/bwa:v0.2

    Modify Dataset tag. `[CWL_INFO_TAG]` format like `provider/dataset:version3`
        sixbox tag dataset [$(dataset resouece_id) or SOURCE_CWL_TAG] [TARGET_CWL_TAG]

        By ID:
        sixbox tag dataset 30479859-c02d-4a40-8e7d-92f9011ac9b8 6oclock/bwa:v0.1
        By Tag:
        sixbox tag dataset 6oclock/dataset:v0.1 sixoclock/dataset:v0.2

    """)
    parser_tag = sub_parsers.add_parser(
        'tag',
        formatter_class=argparse.RawTextHelpFormatter,
        description=tag_descr,
        help=tag_descr,
        epilog=tag_example,
    )
    
    action_tag = parser_tag.add_subparsers(
        help='rename resource in local db..'
    )

    # app
    parser_app = action_tag.add_parser(
        'app', 
        help='rename CWL apps in CWLdb.'
    )
    parser_app.add_argument(
        'raw_tag_ID', 
        type=str, 
        metavar='SOURCE_CWL_TAG',
        help='CWL raw tag or id.'
    )
    parser_app.add_argument(
        'new_tag', 
        type=str, 
        metavar='TARGET_CWL_TAG',
        help='CWL new tag'
    )
    parser_app.set_defaults(func='.main_tag.tag_app')

    # case
    parser_case = action_tag.add_parser(
        'case', 
        help='rename case in db.'
    )
    parser_case.add_argument(
        'raw_tag_ID', 
        type=str, 
        metavar='SOURCE_CWL_TAG',
        help='CWL raw tag or id.'
    )
    parser_case.add_argument(
        'new_tag', 
        type=str, 
        metavar='TARGET_CWL_TAG',
        help='CWL new tag'
    )
    parser_case.set_defaults(func='.main_tag.tag_case')

    # dataset
    parser_dataset = action_tag.add_parser(
        'dataset', 
        help='rename dataset in db.'
    )
    parser_dataset.add_argument(
        'raw_tag_ID', 
        type=str, 
        metavar='SOURCE_CWL_TAG',
        help='dataset raw tag or id.'
    )
    parser_dataset.add_argument(
        'new_tag', 
        type=str, 
        metavar='TARGET_CWL_TAG',
        help='dataset new tag'
    )
    parser_dataset.set_defaults(func='.main_tag.tag_dataset')


def configure_parser_rm(sub_parsers):
    """
    删除CWLdb内的CWL信息。
    """

    rm_descr = dedent("""
    Remove CWL app/case/job/dataset from local db
    """)
    rm_example = dedent("""
    See Sixoclock Help document for for details on all the command.
    
    Examples:

    Delete CWL app. `[CWL_INFO_TAG]` format like `provider/testcwlname:version3` 

        sixbox rm app [$(CWL resouece_id) or CWL_INFO_TAG]

        By ID:
        sixbox rm app 30479859-c02d-4a40-8e7d-92f9011ac9b8
        By Tag:
        sixbox rm app 6oclock/bwa:v0.1

    Delete case:
        sixbox rm case 6oclock/projectcase1

    Delete Job
        sixbox rm job projectjob1
    
    Delete Dataset
        sixbox rm dataset dataset1
    """)

    parser_rm = sub_parsers.add_parser(
        'rm',
        formatter_class=argparse.RawTextHelpFormatter,
        description=rm_descr,
        help=rm_descr,
        epilog=rm_example,
    )
    
    action_rm = parser_rm.add_subparsers(
        help='delete resource in local db..'
    )

    # app
    parser_app = action_rm.add_parser(
        'app', 
        help='delete CWL apps in CWLdb.'
    )
    parser_app.add_argument(
        'tag_ID', 
        type=str, 
        nargs="*",
        metavar='CWL_INFO_TAG',
        help='CWL tag or id.'
    )

    parser_app.set_defaults(func='.main_rm.rm_app')

    # case
    parser_app = action_rm.add_parser(
        'case', 
        help='delete vase in db.'
    )
    parser_app.add_argument(
        'tag_ID', 
        type=str, 
        nargs="*",
        metavar='INFO_TAG',
        help='tag or id.'
    )

    parser_app.set_defaults(func='.main_rm.rm_case')

  # job
    parser_job = action_rm.add_parser(
        'job', 
        help='delete job in db.'
    )
    parser_job.add_argument(
        'jobName', 
        type=str, 
        nargs="*",
        metavar='jobName',
        help='job name.'
    )

    parser_job.set_defaults(func='.main_rm.rm_job')

  # dataset
    parser_dataset = action_rm.add_parser(
        'dataset', 
        help='delete dataset in db.'
    )
    parser_dataset.add_argument(
        'tag_ID', 
        type=str, 
        nargs="*",
        metavar='INFO_TAG',
        help='tag or id of dataset.'
    )

    parser_dataset.set_defaults(func='.main_rm.rm_dataset')

def configure_parser_stop(sub_parsers):
    """
    停止CWL 任务。
    """

    stop_descr = dedent("""
    Stop CWL job running.
    """)
    stop_example = dedent("""
    See Sixoclock Help document for for details on all the command.
    
    Examples:

    Stop CWL job.  

        sixbox stop 30479859-c02d-4a40-8e7d-92f9011ac9b8

    """)

    parser_stop = sub_parsers.add_parser(
        'stop',
        formatter_class=argparse.RawTextHelpFormatter,
        description=stop_descr,
        help=stop_descr,
        epilog=stop_example,
    )
    

    parser_stop.add_argument(
        'jobName', 
        type=str, 
        nargs="*",
        metavar='jobName',
        help='job name.'
    )

    parser_stop.set_defaults(func='.main_stop.stop_job')


def configure_parser_log(sub_parsers):
    """
    实时打印CWL 任务日志。
    """

    stop_descr = dedent("""
    print log for CWL job.
    """)
    stop_example = dedent("""
    See Sixoclock Help document for for details on all the command.
    
    Examples:

    print log for CWL job.  

        sixbox log myjob
    """)

    parser_stop = sub_parsers.add_parser(
        'log',
        formatter_class=argparse.RawTextHelpFormatter,
        description=stop_descr,
        help=stop_descr,
        epilog=stop_example,
    )
    

    parser_stop.add_argument(
        'jobName', 
        type=str, 
        metavar='jobName',
        help='job name.'
    )
    parser_stop.add_argument(
        '-f', 
        '--follow',
        default = False,
        action='store_true',
        dest='follow', 
        required=False,
        help='Specify if the logs should be streamed.'
    )

    parser_stop.set_defaults(func='.main_log.log_job')


def configure_parser_search(sub_parsers):
    """
    搜索app或者case。
    """

    rm_descr = dedent("""
    search CWL app/case from sixoclock.net
    """)
    rm_example = dedent("""
    See Sixoclock Help document for for details on all the command.
    
    Examples:

    Search CWL app. `[term]` format like `app name or description` 

        sixbox search app bwa

    search case
        sixbox case projectcase

    """)

    parser_search = sub_parsers.add_parser(
        'search',
        formatter_class=argparse.RawTextHelpFormatter,
        description=rm_descr,
        help=rm_descr,
        epilog=rm_example,
    )
    
    action_search = parser_search.add_subparsers(
        help='search resource in local db..'
    )

    # app
    parser_app = action_search.add_parser(
        'app', 
        help='search CWL apps in sixoclock.net.'
    )
    parser_app.add_argument(
        'term', 
        type=str, 
        metavar='term',
        help='serach keywords.'
    )

    parser_app.set_defaults(func='.main_search.search_app')

    # app
    parser_case = action_search.add_parser(
        'case', 
        help='search CWL cases in sixoclock.net.'
    )
    parser_case.add_argument(
        'term', 
        type=str, 
        metavar='term',
        help='serach keywords.'
    )

    parser_case.set_defaults(func='.main_search.search_case')

