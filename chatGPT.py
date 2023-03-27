import requests
import json


def chat(prompt, stop=None):
    url = 'http://47.251.11.225:8080/chatGPT'

    val = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user"}],
        "apikey": 'oss6af3'
    }
    val['messages'][0]['content'] = prompt
    val['messages'] = json.dumps(val['messages'])
    val['stop'] = json.dumps(stop)

    ret = requests.post(url, json=val)
    print(ret.text)
    ret = ret.json()

    ret = ret['choices'][0]['message']['content']

    # print('---')
    # print(prompt)
    # print('---_')
    # print(ret)
    # print('------')
    return ret


message = '''
hi
'''


def test_chatgpt():
    ret = chat(message)
    print(ret)


if __name__ == '__main__':
    test_chatgpt()