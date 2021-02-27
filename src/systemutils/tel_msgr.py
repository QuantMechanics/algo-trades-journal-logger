import requests
import json
import os
from pathlib import Path


class TelUtil():

    def __init__(self):
        self.base_path = self.get_project_root()
        self.system_cred = self.loadJson(os.path.join(
            self.base_path, "credentials", "env_credential.json"))
        self.tel_url = "https://api.telegram.org/{secret}/sendmessage".format(
            secret=self.system_cred["telegram"]["secret"])
        self.chat_id = self.system_cred["telegram"]["chat_id"]

    def get_project_root(self) -> Path:
        return Path(__file__).parent.parent.parent

    def loadJson(self, filename=""):  # This helps in reading JSON files
        with open(filename, mode="r") as json_file:
            data = json.load(json_file)
            return data

    # @classmethod
    def sendMsg(self, msg: str):
        '''
        you can use below message payloads
        <b>bold</b>, <strong>bold</strong>
        <i>italic</i>, <em>italic</em>
        <u>underline</u>, <ins>underline</ins>
        <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
        <b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
        <a href="http://www.example.com/">inline URL</a>
        <a href="tg://user?id=123456789">inline mention of a user</a>
        <code>inline fixed-width code</code>
        <pre>pre-formatted fixed-width code block</pre>
        <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
        '''
        _msg = '''{}'''.format(msg)
        payload = {'chat_id': self.chat_id, 'text': _msg,
                   'disable_notification': 'false', 'parse_mode': 'HTML'}
        response = requests.request(
            "POST", self.tel_url, json=payload)
        return (response.text.encode('utf8'))
