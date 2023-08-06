import os
import sys

sys.path.append(os.path.dirname(os.path.abspath((os.path.dirname(__file__)))))



# print('utils test start!!!')
# from krutils import utils

# print(utils.is_empty(""))
# print(utils.is_empty("input"))




print('logger test start!!!')
from krutils import logger

str = 'my string is str'
logger.dblog("[%%]", str)

# file_path = u.find_first_file_to_root('logger.json')
# logger.debug("file_path[%%]", file_path)


