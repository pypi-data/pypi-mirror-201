'''
Application Error
    논리적으로는 이상이 없으나, 정의에 부합하지 않는 오류를 명시적으로 처리한다.
    
    사용법>
    raise AE()
    raise AE("입력값 : {0}, {1}".format(num1, num2))

    try:
        xxxxx
    except AE as e:
        print(e)
    except:
        print("어쨌던 에러")
'''


class AE(Exception):
    
    def __init__(self, msg=None):
        super().__init__(msg)
    