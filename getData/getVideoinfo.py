import time
from tqdm import tqdm
import requests
import json
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
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

# 或许视频基本信息API接口
api_url = 'https://api.bilibili.com/x/web-interface/view?bvid='

# 读取csv中的bvid
video_list = pd.read_csv('/Volumes/SSD/Data/getVideoid_byhot.csv')

bvid_list = video_list['bvid'].values.tolist()

stat_pd = pd.DataFrame()

for bvid in tqdm(bvid_list):
    page_url = api_url + bvid
    response = requests.get(page_url, headers=headers)
    data = json.loads(response.text)
    # print(data)

    info_dic = dict(data['data']['stat'])
    info_dic['bvid'] = data['data']['bvid']  # 视频bvid
    info_dic['title'] = data['data']['title']  # 视频标题
    info_dic['pubdate'] = data['data']['pubdate']  # 稿件发布时间
    info_dic['ctime'] = data['data']['ctime']  # 用户上传时间
    info_dic['cid'] = data['data']['cid']  # 视频cid

    pubdate_timeStamp = int(info_dic['pubdate'])
    timeArray = time.localtime(pubdate_timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    info_dic['order_pubdate'] = otherStyleTime

    ctime_timeStamp = int(info_dic['ctime'])
    timeArray = time.localtime(ctime_timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    info_dic['order_ctime'] = otherStyleTime

    info_pd = pd.DataFrame(info_dic, index=[0])

    # print(info_dic)

    # stat_pd = stat_pd.append(info_dic, ignore_index=True)
    stat_pd = pd.concat([stat_pd, info_pd], ignore_index=True)
    # print(stat_pd)


stat_pd.to_csv('/Volumes/SSD/Data/getVideoinfo_byhot.csv')
