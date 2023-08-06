# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 10:42
# @Author  : abo123456789
# @Desc    : free_chatgpt.py
import json
import urllib.parse
from abc import ABCMeta
from json import JSONDecodeError

import requests
import retrying
from requests import ReadTimeout


def retry_if_timeout_error(excep):
    return isinstance(excep, ReadTimeout)


class FreeChatgpt(object):

    @staticmethod
    def __ask_old(question: str):
        try:
            @retrying.retry(stop_max_attempt_number=4, stop_max_delay=100000,
                            wait_fixed=1500, retry_on_exception=retry_if_timeout_error)
            def ask_q():
                if not question or not question.strip():
                    return {'code': 0, 'error': 'question is null!'}
                # url = f'https://api.wqwlkj.cn/wqwlapi/chatgpt.php?msg={question.strip()}&type=json'
                # url = f"http://www.emmapi.com/chatgpt?text={question.strip()}"
                # url = f"https://v1.apigpt.cn/?q={question.strip()}"
                # url = f"https://api.caonm.net/api/ai/o.php?msg={question.strip()}"
                url = f"https://api.caonm.net/api/ai/o.php?msg={question.strip()}"
                print('AI问题思考中=====')
                res = requests.get(url, timeout=70)
                answer_q = None
                try:
                    if not res.text:
                        raise ReadTimeout()
                    res_json = json.loads(res.text)
                    answer_q = res_json.get("Output")
                    print(f'AI问题回答:{answer_q}')
                    if res_json.get('info'):
                        del res_json['info']
                except JSONDecodeError:
                    return {'code': 0, 'error': answer_q}
                return {'code': 1, 'text': answer_q}

            return ask_q()
        except ReadTimeout:
            return {'code': 0, 'error': 'ReadTimeout,please retry'}

    @staticmethod
    def ask(question: str):
        try:
            @retrying.retry(stop_max_attempt_number=4, stop_max_delay=100000,
                            wait_fixed=1500, retry_on_exception=retry_if_timeout_error)
            def ask_q():
                if not question or not question.strip():
                    return {'code': 0, 'error': 'question is null!'}
                print('AI问题思考中=====')
                answer_q = None
                try:
                    answer_q = PlatformGptStore(question)._get_chat_res()
                    print(f'AI问题回答:{answer_q}')
                    return answer_q
                except JSONDecodeError:
                    return {'code': 0, 'error': answer_q}

            return ask_q()
        except ReadTimeout:
            return {'code': 0, 'error': 'ReadTimeout,please retry'}


class BasePlatform(metaclass=ABCMeta):
    def __init__(self, question: str):
        self.question = question

    def _get_chat_res(self) -> str:
        pass


class PlatformGptStore(BasePlatform):
    def _get_chat_res(self) -> str:
        url = "http://free-gpt.store/chatgpt.php"
        msg = urllib.parse.quote(self.question)
        payload = f'message={msg}&mychat_ip=43.200.91.235&user_uuid=CHAT-APIGPT-6q1y-3u1p1p-iqoj-3u1y9ut'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '83',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'vtins__JyvVgnc34VsbRCoA=%7B%22sid%22%3A%20%2268124e43-9986-5086-b776-96164ead8e8a%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201680107892363%2C%20%22ct%22%3A%201680106092363%7D; __51uvsct__JyvVgnc34VsbRCoA=1; __51vcke__JyvVgnc34VsbRCoA=c8a8bfcd-bd47-529f-b14b-a195a473eb77; __51vuft__JyvVgnc34VsbRCoA=1680106092372; __gads=ID=0014e195aa647a4f-2295111fd1dc0088:T=1680106133:RT=1680106133:S=ALNI_MYvd73jS0gke9fGbravjygychOjqA; __gpi=UID=00000a35412fdd57:T=1680106133:RT=1680106133:S=ALNI_MZAzBmFwa0kUZj15iK6LCmKFAmaLw',
            'Host': 'free-gpt.store',
            'Origin': 'http://free-gpt.store',
            'Referer': 'http://free-gpt.store/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=60)
        rs = response.text.split('答：')[1].strip('<br />').strip('<br />')
        return rs


if __name__ == '__main__':
    # r = FreeChatgpt.ask(question='帮我优化这段话:pandas快速替换所有字符中的特殊字符')
    # print(r)
    # t = FreeChatgpt.ask(question='中国文化的特点是什么？')
    # print(t)
    q = '世界上最赚钱的公司是哪家？'
    s = FreeChatgpt.ask(question=q)
    print(s)
