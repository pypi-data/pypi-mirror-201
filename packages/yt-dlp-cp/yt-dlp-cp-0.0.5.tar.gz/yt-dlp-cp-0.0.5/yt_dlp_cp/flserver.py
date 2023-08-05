from flask import Flask, request

import json

# 实例化app


import yt_dlp_cp


def create_flserever():
    flserever = Flask(__name__)
    return flserever

flserever = create_flserever()

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


def getUrl(json,source):
    try:
      json['url'] = source['url']
    except Exception as e:
      print(e)

def getExt(json,source):
    try:
      json['url'] = source['url']
    except Exception as e:
      print(e)

def getValue(json,source,name):
    try:
      json[name] = source[name]
    except Exception as e:
      print(e)


# 通过methods设置POST请求
@flserever.route('/test', methods=["POST"])
def form_request_request():
    print("hello")
    # 接收post请求的form表单参数
    print(request.data)
    data = json.loads(request.data)
    text = data['text']
    print("hello")
    print(text)
    list=[text]
    res = yt_dlp_cp.main(list)
    print(res[0])
    json_array =[];

    result = {}
    try:
      result['id'] = res[0]['id']
    except Exception as e:
      print(e)
    try:
      result['title'] = res[0]['title']
    except Exception as e:
      print(e)
    try:
      result['duration'] = res[0]['duration']
    except Exception as e:
      print(e)
    list = res[0]['formats']
    for i in list:
       json1 = {}
       getValue(json1,i,'url')
       getValue(json1,i,'ext')
       getValue(json1,i,'format_id')
       getValue(json1,i,'width')
       getValue(json1,i,'protocol')
       getValue(json1,i,'filesize')
       getValue(json1,i,'height')
       json_array.append(json1)
    result["urls"] = json_array
    response = json.dumps({'message': 'success', 'data': result})
    return response,200,{"Content-Type":"application/json"}

if __name__ == '__main__':
    flserever.run()
