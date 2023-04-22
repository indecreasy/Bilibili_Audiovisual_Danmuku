import re
import os
import requests
import json
import time
from lxml import etree
from tqdm import tqdm
import json as js
import pandas as pd
import random

fold_path = '/Volumes/SSD/Data'
ERROR_CID_PATH = "/Volumes/SSD/Data/Video/error_bvids.csv"
SUCCESS_CID_PATH = "/Volumes/SSD/Data/Video/successful_bvids.csv"
i = 1

# 设置请求头
"""
这部分代码定义了请求头和生活区API接口的URL。其中，请求头用于伪装成浏览器发送请求，防止被B站识别为爬虫。API接口的URL是获取生活区视频数据的接口，可以通过修改接口参数来获取不同的数据。
"""
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Referer': 'https://www.bilibili.com/',
    'cookie': "buvid3=186D113F-4146-3350-E1FE-CE58905ECF9518532infoc; b_nut=1678082318; "
              "i-wanna-go-back=-1; bsource=search_bing; "
              "_uuid=2A1BB510F-107D4-11109-9172-BB37365BB2F318443infoc; "
              "buvid_fp=5c6b050e8f96262960bb30028d201beb; is-2022-channel=1; CURRENT_FNVAL=4048; "
              "nostalgia_conf=-1; rpdid=|(umk)Yklu)k0J'uY~)|)R~R|; "
              "buvid4=D6D5E980-A95D-9514-9184-2C4042404E8519401-023030613-wx/36t7aYWixCb1RoAvlwA"
              "==; DedeUserID=14912106; DedeUserID__ckMd5=b3e3a7794ac9f603; b_ut=5; "
              "header_theme_version=CLOSE; b_lsid=2EE34684_186D08F88D5; SESSDATA=dd67aabe,"
              "1694088314,26394*31; bili_jct=dd4a6f2f644f20b89b760a9da13eeb2b; "
              "bp_video_offset_14912106=771795332581294100; home_feed_column=5; sid=6sq3hg7r; "
              "PVID=2; innersign=1",
    'origin': 'https://www.bilibili.com'
}

bilibili_url = 'https://www.bilibili.com/video/'
videolist_url = 'https://api.bilibili.com/x/web-interface/web/channel/featured/list?'

# 读取csv中的bvid、cid
video_list = pd.read_csv('/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot_6.csv')
bvid_list = video_list['bvid'].values.tolist()
cid_list = video_list['cid'].values.tolist()

for bvid in tqdm(bvid_list):

    bvid_path = f"/Volumes/SSD/Data/Video/{bvid}"

    if os.path.exists(bvid_path):
        print(f"File for bvid {bvid} already exists. Skipping...")
        with open(SUCCESS_CID_PATH, "a") as success_file:
            success_file.write(f"{bvid}\n")
        continue


    page_url = bilibili_url + bvid
    print(page_url)
    response = requests.get(page_url, headers=headers)
    page_content = response.text
    # print(page_content)
    page_tree = etree.HTML(page_content)

    # 视频+音频
    video_content = page_tree.xpath('/html/head/script[5]/text()')
    # 这种没有id的只用[5]来标定的就不太稳定，所以改用正则
    pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
    no_video_pattern = r'视频去哪了呢？'

    if len(re.findall(no_video_pattern, page_content)) != 0:
        with open(ERROR_CID_PATH, "a") as error_file:
            error_file.write(f"{bvid}\n")
            print(f"Cannot get video for bvid {bvid}. Skipping...")
        continue

    try:

        temp = re.findall(pattern, page_content)[0]
    except:
        with open(ERROR_CID_PATH, "a") as error_file:
            error_file.write(f"{bvid}\n")
            print(f"Cannot get video for bvid {bvid}. Skipping...")
        continue

    video_content = json.loads(temp)

    if video_content['data'] is not None:
        if 'dash' in video_content['data'].keys():
            for item in video_content['data']['dash']['video']:
                if 'baseUrl' in item.keys():
                    video_url = item['baseUrl']
                    continue
            for item in video_content['data']['dash']['audio']:
                if 'baseUrl' in item.keys():
                    audio_url = item['baseUrl']
                    continue

        else:
            print(video_content)

    print(video_url)
    print(audio_url)

    videofold = fold_path + '/Video/' + str(bvid)

    if not os.path.exists(videofold):
        print(1)
        os.mkdir(videofold)

    title = bvid

    title = title.replace('/', '')
    title = title.replace(' ', '')
    title = title.replace('|', '')
    title = title.replace(':', '')
    title = title.replace('：', '')
    vfilename = videofold + '/' + title + '.mp4'
    afilename = videofold + '/' + title + '.mp3'

    header = headers
    header['Origin'] = 'https://www.bilibili.com'
    header['Referer'] = page_url

    with open(vfilename, 'wb') as f:
        with requests.get(url=video_url, headers=header, stream=True) as r:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
        # f.write(requests.get(url = videoinfo['video_url'],headers = self.videoheaders).content)

    with open(afilename, 'wb') as f:
        f.write(requests.get(url=audio_url, headers=header).content)
        with open(SUCCESS_CID_PATH, "a") as success_file:
            success_file.write(f"{bvid}\n")
        continue


    # time.sleep(3)


