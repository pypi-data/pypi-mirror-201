from assertpy import assert_that
import requests
from deepdriver.sdk.interface import interface
from deepdriver import logger
from deepdriver.sdk import util
# deepdriver 실험환경을 사용하기위한 로그인 과정
# 서버의 login api를 호출하여 key를 서버로 전송하고 결과로서 jwt key를 받는다

def login(key: str=None, id: str =None, pw: str=None) -> (bool, str):
    #assert_that(key).is_not_none()
    if key is None and id is None:
        if util.is_notebook():
            import getpass
            id = input('Enter your email:')
            pw = getpass.getpass('Enter your password:')
        else:
            assert_that(id).is_not_none()
            assert_that(pw).is_not_none()
    else:
        assert_that(pw).is_not_none()

    try:
        return interface.login(key,id,pw)[0]
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
        logger.error(f"Could Login to Server[{interface.get_http_host()}]. Set Server IP/PORT using deepdriver.setting()")
        return False



