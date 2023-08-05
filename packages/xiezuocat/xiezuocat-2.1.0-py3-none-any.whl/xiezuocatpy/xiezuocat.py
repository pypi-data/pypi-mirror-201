import requests
import time
import base64
from xiezuocat import sm3_signature_util

class Xiezuocat:
    def __init__(self, secret_key):
        self._secret_key = secret_key
        self._check_url = "https://apicheck.xiezuocat.com/api/text_check"
        self._rewrite_url = "https://apicheck.xiezuocat.com/api/api/rewrite"
        self._ai_write_generate_url = "https://apicheck.xiezuocat.com/api/api/generate"
        self._ai_write_get_generate_result_url = "https://apicheck.xiezuocat.com/api/api/generation/{docId}"

    def set_check_url(self, check_url):
        self._check_url = check_url

    def set_rewrite_url(self, rewrite_url):
        self._rewrite_url = rewrite_url

    def set_ai_write_generate_url(self, ai_write_generate_url):
        self._ai_write_generate_url = ai_write_generate_url

    def set_ai_write_get_generate_result_url(self, ai_write_get_generate_result_url):
        self._ai_write_get_generate_result_url = ai_write_get_generate_result_url

    def check(self, data):
        return self._do_post(self._check_url, data)

    def rewrite(self, data):
        return self._do_post(self._rewrite_url, data)

    def generate(self, data):
        return self._do_post(self._ai_write_generate_url, data)

    def get_generate_result(self, doc_id):
        url = self._ai_write_get_generate_result_url.replace("{docId}", doc_id)
        return self._do_get(url)

    def _do_post(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'secret-key': self._secret_key
        }

        response = requests.request("POST", url, headers=headers, data=data)

        return response.text

    def _do_get(self, url):
        headers = {
            'Content-Type': 'application/json',
            'secret-key': self._secret_key
        }

        response = requests.request("GET", url, headers=headers)

        return response.text

    def get_sso_signature(self, appId, user_id):
        timestamp = time.time()
        para_map = {}
        para_map["appId"] = appId
        para_map["uid"] = user_id
        para_map["timestamp"] = timestamp
        sign = sm3_signature_util.signature_sm3(para_map, self._secret_key)
        para_map["sign"] = sign
        base64_str = str(base64.b64encode(str(para_map).encode('utf-8')), "utf-8")

        return base64_str