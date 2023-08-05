from random import Random

import m3u8
import requests
import datetime
import os
import glob
import wget

from Cryptodome.Cipher import AES

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

def download(ts_urls,downloadPath,keys=[]):
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)

    decrypt = True
    if len(keys) == 0 or keys[0] is None:
        decrypt = False;

    for i in range(len(ts_urls)):
        ts_url = ts_urls[i]
        file_name = ts_url.uri
        start = datetime.datetime.now().replace(microsecond=0)
        try:
            response = requests.get(file_name,stream=True,verify=False)
        except Exception as e:
            print(e)
            return
        ts_path = downloadPath+"/{0}.ts".format(i)
        if decrypt:
            key = keys[i]
            iv = Random.new().read(AES.block_size)
            cryptor = AES.new(key.encode('utf-8'),AES.MODE_CBC)

        with open(ts_path,"wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    if decrypt:
                        file.write(cryptor.decrypt(chunk))
                    else:
                        file.write(chunk)
        end = datetime.datetime.now().replace(microsecond=0)

def merge_to_mp4(dest_file,source_path,delete=False):
        with open(dest_file,'wb') as fw:
            files = glob.glob(source_path+'/*.ts')
            for file in files:
                with open(file,'rb') as fr:
                    fw.write(fr.read())
                if delete:
                    os.remove(file)

if __name__=="__main__":
    url = "http://pl-ali.youku.com/playlist/m3u8?vid=XNTk0MjIyMTM2NA%3D%3D&type=mp4hdv3&ups_client_netip=67ac29c7&utid=l%2BqrHBR7cggCAWesKcW%2FnXHo&ccode=0524&psid=3dcb36581d7209a6a6c790cf047ab03a41346&duration=2748&expire=18000&drm_type=1&drm_device=10&drm_default=1&hotvt=1&dyt=0&ups_ts=1680145560&onOff=0&encr=0&ups_key=040554dd6a5fdb943cf6d9e47e7d3e7c&ckt=3&m_onoff=0"
    #out_fname = wget.download(url)
    video = m3u8.load(url)
    print('url数据',video.data)
    download(video.segments,'tmp',video.keys)
    merge_to_mp4('result.mp4','tmp',False)





