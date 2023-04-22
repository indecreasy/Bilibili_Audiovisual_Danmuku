import time
from tqdm import tqdm
import requests
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import random

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

# 或许视频基本信息API接口
api_url = 'https://api.bilibili.com/x/web-interface/view?bvid='


def get_video_info(bvid):
    page_url = api_url + bvid
    response = requests.get(page_url, headers=headers)
    data = json.loads(response.text)
    # print(data)

    info_dic = dict(data['data']['stat'])
    info_dic['bvid'] = data['data']['bvid']
    info_dic['title'] = data['data']['title']
    info_dic['pubdate'] = data['data']['pubdate']
    info_dic['ctime'] = data['data']['ctime']
    info_dic['cid'] = data['data']['cid']

    pubdate_timeStamp = int(info_dic['pubdate'])
    timeArray = time.localtime(pubdate_timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    info_dic['order_pubdate'] = otherStyleTime

    ctime_timeStamp = int(info_dic['ctime'])
    timeArray = time.localtime(ctime_timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    info_dic['order_ctime'] = otherStyleTime

    time.sleep(0.5)

    return info_dic


def crawler(read_path, save_path):
    # 读取csv中的bvid
    video_list = pd.read_csv(read_path)
    bvid_list = video_list['bvid'].values.tolist()

    stat_pd = pd.DataFrame()

    # 使用 ThreadPoolExecutor 创建一个线程池
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 使用 map 函数将 get_video_info 应用到每个 bvid，并将结果转换为列表
        results = list(tqdm(executor.map(get_video_info, bvid_list), total=len(bvid_list)))

    # 遍历每个线程的结果，并将其添加到 stat_pd
    for info_dic in results:
        info_pd = pd.DataFrame(info_dic, index=[0])
        stat_pd = pd.concat([stat_pd, info_pd], ignore_index=True)

    stat_pd.to_csv(save_path)


if __name__ == "__main__":
    for i in range(7,61):
        read_path = '/Volumes/SSD/Data/getVideoid_byhot_{}.csv'.format(i)
        save_path = '/Volumes/SSD/Data/getVideoinfo_byhot_{}.csv'.format(i)
        crawler(read_path, save_path)
