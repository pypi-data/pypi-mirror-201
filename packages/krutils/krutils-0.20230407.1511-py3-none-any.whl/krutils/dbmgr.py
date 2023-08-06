import re
import os
import pymysql
from pymysql import Connection
from common import logger
from common import utils


# SQL PARAM 형식
SQL_PARAM_PATTERN = "#\\{\\D[\\w]*\\}";

# SELECT 기본 MAX 건수 : 500 (DBIO 조회 기본값)
MAX_CNT = 10000;







def excuteSQL():
    '''
    SQL을 실행, 결과를 반환한다.
    '''

    '''
    예를 들어 입력 SQL이 아래와 같다고 하면...

    SELECT * 
    FROM TBTMP
    where k1 = #{k1}
    ;
    '''

    # CONNECTION
    juso_db = pymysql.connect(
        user='root', 
        passwd='{설정한 비밀번호}', 
        host='127.0.0.1', 
        db='juso-db', 
        charset='utf8'
    )


    # CURSOR
    cursor = juso_db.cursor(pymysql.cursors.DictCursor)


    ##########################
    # SELECT
    sql = "SELECT * FROM `busan-jibun`;"
    cursor.execute(sql)
    result = cursor.fetchall()

    # PANDAS DF 로 변환
    import pandas as pd

    result = pd.DataFrame(result)
    result



    ##########################
    # INSERT
    sql = '''INSERT INTO `busan-jibun` (관리번호, 일련번호, 시도명, 시군구명) 
    VALUES ('1234567891234567891234567', '1', '서울특별시', '강남구');'''

    cursor.execute(sql)
    juso_db.commit()











def _get_connection() -> pymysql.Connection:
    '''
    DB Connection
    '''
    
    # katis 메인 환경설정 읽기
    katis_env = utils.get_katis_env()
    logger.debug("katis_env[%%]", katis_env)

    # DB 설정 파일 읽기
    curr_dir = os.path.dirname(__file__)
    base_name = os.path.basename(__file__)
    file_name = os.path.splitext(base_name)

    katis_db_env_file_path = os.path.join(curr_dir, file_name[0]) + ".json"
    logger.debug("katis_db_env_file_path[%%]", katis_db_env_file_path)

    import json
    with open(katis_db_env_file_path) as fp:
        katis_db_env = json.load(fp)



    # 메인 설정 파일의 system 구분에 해당하는 접속정보를 가져온다
    curr_db_env = katis_db_env[katis_env["SYSTEM"]]
    logger.debug("curr_db_env[%%]", curr_db_env)

    # DB Connect 실행
    try:
        myConn = pymysql.connect(
                                    host=curr_db_env["host"],
                                    port=curr_db_env["port"],
                                    database=curr_db_env["database"],
                                    user=curr_db_env["user"],
                                    passwd=curr_db_env["passwd"]
                                )
    except Exception as e:
        logger.error("e[%%]", e)
        raise e



    return myConn



def _parse_sql(sql: str, *args, **kwargs):
    '''
    sql의 변수를 %s로 변환하면서 kwargs를 sql입력으로 사용할 list로 변환한다.

    sql : SELECT * FROM TABLE WHERE COL1=#{COL1} and COL1=#{col2}
    kwargs : {'col1': '1'}

    KEY값은 대소문자 구분하지 않는다.

        - SQL은 변수가 %S 로 대체되어야 한다.
        - 값에 대응하는 변수는 LIST형태로 변경되어야 한다.

    @return : new_sql, new_arg_list
    '''
    ###############
    # 전처리

    # 변수 key를 대분자로 치환
    new_kwargs={}
    for kwargs_key in list(kwargs.keys()):
        new_kwargs[str(kwargs_key).upper()] = kwargs.pop(kwargs_key)
    # logger.dblog("new_kwargs[%%]", new_kwargs)

    ###############
    # 처리

    # sql에 포함된 변수 목록을 구한다.
    p = re.findall(SQL_PARAM_PATTERN, sql, re.I)
    # logger.dblog("p[%%]", p)


    # list형태로 변환하자
    new_args = []
    for ii, f in enumerate(p):
        new_key = str(f[2:-1]).upper()
        # logger.debug("new_key[%%]", new_key)

        try:
            new_val = new_kwargs[new_key]
        except Exception as e:
            new_val = None
        
        new_args.append(new_val)
    # logger.dblog("new_args[%%]", new_args)


    # sql에서 변수 할당 치환
    new_sql = re.sub(SQL_PARAM_PATTERN, "%s", sql)
    # logger.dblog("new_sql[%%] new_args[%%]", new_sql, new_args)

    logger.dblog("new_sql[%%], new_args[%%]", new_sql, new_args)
    return new_sql, new_args


def excuteSQL(sql: str, *args, **kwargs):
    '''
    [SQL 실행]

    사용예>
        sql = """SELECT * FROM TBTMP
        WHERE 1=1
        AND K1=#{K1}
        AND v1=#{v1}
        AND V2=#{V2}"""

        kwarg_list = {}
        kwarg_list["K1"]="1"
        kwarg_list["v2"]="q"

        excuteSQL(sql, **kwarg_list)
    '''
    logger.dblog("sql[%%] kwargs[%%]", sql, kwargs)

    conn = _get_connection()
    cursor = conn.cursor()

    # pyMySql에 입력될 수 있는 형태로 변환한다.
    new_sql, new_args = _parse_sql(sql, **kwargs)

    # logger.debug("new_args[%%]", new_args)
    # logger.debug("new_args[%%][%%]", type(new_args), new_args)
    cursor.execute(new_sql, new_args)



    # data = ('ramen', 1)
    # logger.debug("data[%%][%%]", type(data), data)
    # cursor.execute(new_sql, data)


    res = cursor.fetchall()
    # logger.debug("res[%%]", res)

    for r in res:
        logger.debug("r[%%]", r)









if __name__ == '__main__':

    sql = """select *
    from tbtmp
    where K1 = #{K1}
    and V1 = #{v1}"""

    kwarg_list = {}
    kwarg_list["K1"]="3"
    kwarg_list["v1"]="4"

    excuteSQL(sql, **kwarg_list)





