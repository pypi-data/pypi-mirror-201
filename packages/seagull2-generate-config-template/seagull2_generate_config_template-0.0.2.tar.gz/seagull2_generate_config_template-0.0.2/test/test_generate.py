import unittest
import os
from generate_config import generate

# 构建参数
request_data = {
    'publicAppId': 'TestPublic',  # 公共应用appid
    'appId': 'TestApp'  # 当前应用id
}
config_result = 'config_result.txt'
configTemplates = [[config_result, '.\config_template.txt']]


class test(unittest.TestCase):

    def test_generate():
        try:
            generate.generate_config('apollo', 'DEV', '', False,
                                     False, '', '', configTemplates, request_data)
            file_object = open(config_result, 'r')
            all_the_text = file_object.read()  # 结果为str类型
            print(all_the_text)
            assert all_the_text == '我是DEV环境'
        finally:
            os.remove(config_result)
