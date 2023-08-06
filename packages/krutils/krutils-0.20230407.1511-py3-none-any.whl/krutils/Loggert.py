'''
LOG처리

	내가 필요한것은 로그 문자열 포멧팅 밖에 없다.
	나중에 logging을 래핑하자




'''

import os
import inspect
from datetime import datetime

######################
# 전역변수 설정
######################
# 문자열 치환자
__LOG_SUBSTITUTOR      = "%%";

# 호출자 인덱스
__CALLER_IDX           = 4;

# 로그에 필요한 설정 파일 (Optional)
__LOGGER_CONFIG_FILE_NAME = 'logger.json'
#    SAMPLE : logger.json
#    {
#        "LOG_LEVEL" : "DB",
#        "LOG_CONSOLE_YN" : "Y",
#        "LOG_FILE_YN" : "N",
#        "LOG_DIR_PATH" : "./logs",
#        "LOG_FILE_NAME" : "mylog.log"
#    }





######################
# 로깅 레벨 설정
######################
def get_log_level_index(level: str) -> int:
    if level == None:
        return 4
    elif level == "ERR":
        return 4
    elif level == "INFO":
        return 3
    elif level == "APP":
        return 2
    elif level == "DB":
        return 1
    elif level == "ALL":
        return 0

    return 4


# 시스템 로그를 포함하여 출력
DEBUG_LEVEL_ALL        = get_log_level_index("ALL");
# DB접근 로그를 포함하여 출력
DEBUG_LEVEL_DB         = get_log_level_index("DB");
# 프로그램 로그를 포함하여 출력
DEBUG_LEVEL_APP        = get_log_level_index("APP");
# 중요 정보 발생시 출력
DEBUG_LEVEL_INFO       = get_log_level_index("INFO");
# 오류 발생시 출력
DEBUG_LEVEL_ERR        = get_log_level_index("ERR");

######################
# 로거 동작 설정
######################
# 현재 로그레벨 (최초 생성시 기본로그레벨로 세팅)
CURR_DEBUG_LEVEL       = get_log_level_index("ERR");

# 디버깅 출력 방법 : 콘솔 출력 여부
DEBUG_CONSOLE_PRINT_YN = "Y";

# 디버깅 출력 방법 : 파일 출력 여부
DEBUG_FILE_PRINT_YN    = "N";

# 디버깅 출력 방법 : 파일 출력 경로
DEBUG_FILE_DIR_PATH  = "./logs";
DEBUG_FILE_FILE_NAME  = datetime.now().strftime("%H%M%S") + '.log';








#######################################
# CLASS 초기화
#   - CALLER 정보를 입력하는 경우 설정 파일을 탐색하여 발견되면 적용한다
class init:
    caller_file_name = ''

    def __init__(self, caller_file_name):
        self.caller_file_name = caller_file_name;
        print(__name__ + ' is initiating... by ' + caller_file_name)


# try:
#     from krutils import utils
#     config_file_path = utils.find_first_file_to_root(__LOGGER_CONFIG_FILE_NAME)

#     if utils.is_empty(config_file_path) != True:

#         import json
#         with open(config_file_path) as cf:
#             logger_config = json.load(cf)

#         # print (logger_config)

#         cfv = logger_config['LOG_LEVEL']
#         if (utils.is_empty(cfv) != True):
#             CURR_DEBUG_LEVEL = get_log_level_index(cfv)

#         cfv = logger_config['LOG_CONSOLE_YN']
#         if (utils.is_empty(cfv) != True):
#             DEBUG_CONSOLE_PRINT_YN = cfv

#         cfv = logger_config['LOG_FILE_YN']
#         if (utils.is_empty(cfv) != True):
#             DEBUG_FILE_PRINT_YN = cfv

#         cfv = logger_config['LOG_DIR_PATH']
#         if (utils.is_empty(cfv) != True):
#             DEBUG_FILE_DIR_PATH = cfv

#         cfv = logger_config['LOG_FILE_NAME']
#         if (utils.is_empty(cfv) != True):
#             DEBUG_FILE_FILE_NAME = cfv

#         # print ('CURR_DEBUG_LEVEL : ' + str(CURR_DEBUG_LEVEL))
#         # print ('DEBUG_CONSOLE_PRINT_YN : ' + DEBUG_CONSOLE_PRINT_YN)
#         # print ('DEBUG_FILE_PRINT_YN : ' + DEBUG_FILE_PRINT_YN)
#         # print ('DEBUG_FILE_PATH : ' + os.path.abspath(os.path.join(DEBUG_FILE_DIR_PATH, DEBUG_FILE_FILE_NAME)))

# except Exception as e:
#     print('Failed to read config file. e[' + str(e) + ']')



##########################################
##      시스템 정보
##########################################
# 호출자 파일 명
def __caller_file_name() -> str:
    return os.path.basename(inspect.stack()[__CALLER_IDX][1])

# 호출자 라인번호
def __caller_file_line() -> int:
    return inspect.stack()[__CALLER_IDX][2]


##########################################
##      log
##########################################
def __gen_substitutor_dummy_string(cnt: int) -> str:
    '''Dummy 치환자 문자열 생성'''
    ret = ""

    for ii in range(cnt):
        ret = ret + __LOG_SUBSTITUTOR

    return ret


def __gen_log_header(debug_level) -> str:
    '''[HH24MISS.FFF][CALLER_NAME:LINE5byte]'''

    HEADER_LENGTH = 40

    header = ""
    if (debug_level == DEBUG_LEVEL_ALL):
        header = header + "[SYSTEM]"
    elif (debug_level == DEBUG_LEVEL_DB):
        header = header + "[  DB  ]"
    elif (debug_level == DEBUG_LEVEL_APP):
        header = header + "[DEBUG ]"
    elif (debug_level == DEBUG_LEVEL_INFO):
        header = header + "[ INFO ]"
    elif (debug_level == DEBUG_LEVEL_ERR):
        header = header + "[ERROR ]"

    header = header + "[" + datetime.now().strftime("%H%M%S.%f")[:-3] + "]"                             # 일시
    header = header + "[" + __caller_file_name() + ":" + str(__caller_file_line()).zfill(5) + "]"       # 호출자
    header = header.ljust(HEADER_LENGTH, " ")                                                           # 길이 맞추기


    return header



def __substitute_string(input: str, *args) -> str:

    if input == None:
        return None

    # print ("len", str(len(args)))
    # print (args)
    for ii, arg in enumerate(args):

        idx = 0
        try:
            idx = input.index(__LOG_SUBSTITUTOR)
        except Exception as e:
            break;

        # print (idx)
        if (idx < 0):
            break;

        # print (__LOG_SUBSTITUTOR)
        # print (input, input.replace(__LOG_SUBSTITUTOR, str(arg), 1))
        input = input.replace(__LOG_SUBSTITUTOR, str(arg), 1)

    return input






def __print_log(debug_level, template="", *args):
    '''
    로그처리
    header + debug_strings...
    '''

    # 정합성 체크 : 시스템에 정의된 디버그레벨과 비교하여 로깅처리를 할지 정한다
    if (debug_level == None):
        return

    if (debug_level < CURR_DEBUG_LEVEL):
        return

    # object를 입력한 경우(예 : Exception) 문자로 변환하여 처리
    template_str = str(template)


    ######################
    # 처리

    # 문자열 치환
    log_body = __substitute_string(template_str, *args)

    # 남은 치환자 제거
    log_body = log_body.replace(__LOG_SUBSTITUTOR, "")


    #################
    # CONSOLE PRINT
    if DEBUG_CONSOLE_PRINT_YN == "Y":
        print (__gen_log_header(debug_level) + " " + log_body)


    #################
    # FILE PRINT
    if DEBUG_FILE_PRINT_YN == "Y":
        print("파일프린트 시작한다[{}]".format(DEBUG_FILE_PRINT_PATH))
        # writelog (__gen_log_header(debug_level) + " " + log_body)
        pass


def syslog(template="", *args):
    __print_log(DEBUG_LEVEL_ALL, template, *args)



def dblog(template="", *args):
    __print_log(DEBUG_LEVEL_DB, template, *args)



def debug(template="", *args):
    __print_log(DEBUG_LEVEL_APP, template, *args)



def info(template="", *args):
    __print_log(DEBUG_LEVEL_INFO, template, *args)



def error(template="", *args):
    __print_log(DEBUG_LEVEL_ERR, template, *args)




























