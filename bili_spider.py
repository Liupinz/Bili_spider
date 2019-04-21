# coding: utf-8
import ffmpeg
import requests
import subprocess
import re
import os

headers = {
    'Origin': 'https://www.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*',
    'Referer': 'https://www.bilibili.com/video/av46460193/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
}


def get_cupn():
    """get cid url and page numbers"""
    url = "https://www.bilibili.com/video/av46460193/"
    r = requests.get(url=url, headers=headers, verify=False).text
    ret = re.findall(r"\"cid\":\d+\,\"page\":\d+", r)
    result_end = []
    for i in ret:
        dic = {}
        result = i.split(',')
        cid_key = result[0].split(':')[0]
        cid_value = result[0].split(':')[1]
        page_key = result[1].split(':')[0]
        page_value = result[1].split(':')[1]
        dic[cid_key] = cid_value
        dic[page_key] = page_value
        result_end.append(dic)
    return result_end


def bilibili_video_download():
    cupns = get_cupn()
    for cupn in cupns:
        cid = cupn['"cid"']
        page = cupn['"page"']
        if page in [str(i) for i in range(1, 54)]:
            continue
        url = "https://api.bilibili.com/x/player/playurl?avid=46460193&cid=" + cid + "&qn=0&type=&otype=json&fnver=0&fnval=16"
        proxies = {"http": "http://181.29.206.71:8080"}
        r = requests.get(url, headers, verify=False, proxies=proxies)
        data_json = r.json()
        video_json = data_json['data']['dash']['video']
        audio_json = data_json['data']['dash']['audio']
        video_json_length = len(video_json)
        for i in range(video_json_length):
            if video_json[i]['id'] == 64:
                vurl = video_json[i]['baseUrl']
                aurl = audio_json[0]['baseUrl']
                vresponse = requests.get(url=vurl, headers=headers, verify=False)
                aresponse = requests.get(url=aurl, headers=headers, verify=False)
                mvideo = "D:\spider\mvideo" + page + ".mp4"
                maudio = "D:\spider\maudio" + page + ".mp4"
                output = "D:\spider\\" + page + ".mp4"
                with open(mvideo, "wb") as f1:
                    f1.write(vresponse.content)
                with open(maudio, "wb") as f2:
                    f2.write(aresponse.content)
                cmd = 'D:\spider\\ffmpeg-20190419-96fc0cb-win64-static\\bin\\ffmpeg.exe -i ' + mvideo + ' -i ' + maudio + ' -c copy ' + output
                subprocess.call(cmd, shell=True)
                os.remove(mvideo)
                os.remove(maudio)
                break


if __name__ == '__main__':
    bilibili_video_download()
