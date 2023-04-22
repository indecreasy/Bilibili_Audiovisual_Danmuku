import time
import requests
import json
import random
import pandas as pd

# 设置请求头
"""
这部分代码定义了请求头和生活区API接口的URL。其中，请求头用于伪装成浏览器发送请求，防止被B站识别为爬虫。API接口的URL是获取生活区视频数据的接口，可以通过修改接口参数来获取不同的数据。
"""

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

# 旅游频道API接口
api_url = 'https://api.bilibili.com/x/web-interface/web/channel/featured/list?channel_id=6572&filter_type=2023&offset=289635780_5%s&page_size=30'
ticks = time.time()

# 获取频道内视频的bvid
"""
这部分代码通过循环从API接口获取生活区视频的bvid，并存储到列表中。为了获取1000个视频，代码将请求50页数据，每页包含20个视频。
"""
df = pd.DataFrame()
bvid_list = []
item_list = []
for i in range(1, 200):  # 从第1页到第200页视频
    page_url = api_url % int(random.random() * 1000000)
    response = requests.get(page_url, headers=headers)
    data = json.loads(response.text)
    for item in data['data']['list']:
        # print(item)
        df = df.append(item, ignore_index=True)

df.to_csv('getVideoid_2023.csv')
