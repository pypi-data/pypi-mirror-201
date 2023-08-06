#############################################################
# 숫자
#############################################################
# 소수점 자리수
PRECISION = 15

# 소수점 처리방법
# public static final RoundingMode ROUNDUP          = RoundingMode.HALF_UP;
# public static final RoundingMode CUT              = RoundingMode.DOWN;


#############################################################
# 문자
#############################################################
# 빈 문자열 : " " (1 BYTE SPACE) - DB 기본값
INIT_STRING = " "

# 빈 문자열 : "" (공백없음) - 변수 초기화등에 활용
EMPTY_STRING = ""

# DELIMITER : {TAB}
DELIM = "\t"


#############################################################
# 날짜
#############################################################
# MIN DATE : 1년 1월
MIN_YM = "000101"

# MIN DATE: 1년 1월 1일
MIN_DT = "00010101"

# MIN TIME: 0시 0분 0초
MIN_TM = "000000"

# MIN DATE TIME : 1년 1월 1일 0시 0분 0초
MIN_DTM = "00010101000000"

# MIN TIMESTAMP : 1년 1월 1일 0시 0분 0초
MIN_TIMESTAMP = "00010101000000000000"

# MIN TIMESTAMP : 0시 0분 0.000000초
MIN_TIMESTAMP_TM = "000000000000"

# MAX DATE : 9999년 12월
MAX_YM = "999912"

# MAX DATE : 9999년 12월 31일
MAX_DT = "99991231"

# MIN TIME: 23시 59분 59초
MAX_TM = "235959"

# MAX DATE TIME : 9999년 12월 31일 23시 59분 59초
MAX_DTM = "99991231235959"

# MAX TIMESTAMP : 9999년 12월 31일 23시 59분 59.999999초
MAX_TIMESTAMP = "99991231235959999999"

# MAX TIMESTAMP : 23시 59분 59.999999초
MAX_TIMESTAMP_TM = "235959999999"


