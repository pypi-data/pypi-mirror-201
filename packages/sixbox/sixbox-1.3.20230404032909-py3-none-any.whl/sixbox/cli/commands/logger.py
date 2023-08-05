import os

import logging
import logging.handlers
from prettytable import PrettyTable
import sys
import colorlog

"""

一些小的辅助函数

"""


def cli_logs(log_f, skip_serve_logs: bool = False):
    """Starts cli_logs """

    logs = logging.getLogger('Sixbox')
    logs.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(
        log_f,maxBytes=10000000,backupCount=5)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(u'%(asctime)s [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    logs.addHandler(fh) 
    return logs, fh

# log = cli_logs(log_f= os.path.join(os.getenv('TEMP'), '.sixbox.log'))

# logging.basicConfig(level = logging.INFO,stream=sys.stderr, format = '%(levelname)s  %(message)s')
log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'white',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

log = logging.getLogger(__name__)
log.setLevel(level = logging.INFO)
console_handler = logging.StreamHandler()
console_formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s%(message)s',
    log_colors=log_colors_config
)
console_handler.setFormatter(console_formatter)
log.addHandler(console_handler)
# handler = logging.FileHandler(sys.stderr)
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log.setFormatter(formatter)

def Unauthorized_log():
    log.warning("Error response from www.sixoclock.net:  access denied, may require login !!!\
        \ncheck token in ~/.sixbox/config.yaml, make sure it is not expired.\
        \n\tsee https://docs.sixoclock.net/clients/sixbox-linux.html for more info about login and sixbox usage!")

def Pretty_printer(template=[ "name", "provider", "resource_id", "description"]):
    """
    格式化打印 表格
    """

    # 初始化table
    table = PrettyTable()
    table.field_names = template
    table.add_row([" "*8]*len(template))
    table.border = 0 # 不设边界
    table.align = 'l' #行对其
    table.right_padding_width =4

    return table