from .utils import *
from .jobs_command import *
from .cases_command import *
from .config_command import *
from .apps_command import *
from .datasets_command import *
from .check_update import *

from .db_command import *
from .logger import *


# 初始化
# TODO: 
# fix: 不要每次运行都检查更新，改为间隔一定时间段检查更新
try:
    # get_updates() # 检查更新
    pass
except:
    pass

initialize_lib() # 初始化lib 目录