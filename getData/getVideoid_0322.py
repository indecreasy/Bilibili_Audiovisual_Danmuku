import time
import requests
import json
import random
import pandas as pd
from tqdm import tqdm

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

# 旅游频道API接口 - 时间
# api_url = 'https://api.bilibili.com/x/web-interface/web/channel/featured/list?channel_id=6572&filter_type=2023&offset=289635780_%s&page_size=30'
# 使用offset方法
# api_url = 'https://api.bilibili.com/x/web-interface/web/channel/featured/list?channel_id=6572&filter_type=2023&offset=%s&page_size=30'


# 旅游频道API接口-热门
# api_url = 'https://api.bilibili.com/x/web-interface/web/channel/multiple/list?channel_id=6572&sort_type=hot&offset=268084080_%s&page_size=30'
# 使用offset方法
api_url = 'https://api.bilibili.com/x/web-interface/web/channel/multiple/list?channel_id=6572&sort_type=hot&offset=%s&page_size=30'
ticks = time.time()

# 获取频道内视频的bvid
"""
这部分代码通过循环从API接口获取生活区视频的bvid，并存储到列表中。为了获取1000个视频，代码将请求50页数据，每页包含20个视频。
"""
df = pd.DataFrame()
bvid_list = []
item_list = []
i = 0

offset = "865828963_1679311956"

while i <= 6000:
    # # 生成一个范围在0000000到999999999之间的随机整数
    # random_number = random.randint(0, 999999999)
    #
    # # 将整数格式化为七位数，用0填充前面的空位
    # random_number_formatted = f"{random_number:09d}"
    #
    # # 生成一个范围在0到9之间的随机整数
    # random_number = random.randint(0, 9)
    # # print(random_number)
    #
    # random_number_formatted_all = str(random_number) + str(random_number_formatted)
    #
    # page_url = api_url % random_number_formatted_all
    # # print(page_url)

    page_url = api_url % offset

    response = requests.get(page_url, headers=headers)
    data = json.loads(response.text)

    offset = data['data']['offset']
    print(offset)
    # print(data)
    for item in data['data']['list']:

        # 将新行数据转换为一个DataFrame
        item_df = pd.DataFrame(item, index=[0])

        if i == 0:
            df = pd.concat([df, item_df], ignore_index=True)
            i += 1
            print(i)
        else:
            # 检查新行的'bvid'值是否与原始DataFrame中的任意一个'bvid'不同
            if item['bvid'] not in df['bvid'].values:
                # 如果不在，则将新行数据添加到原始DataFrame
                df = pd.concat([df, item_df], ignore_index=True)
                i += 1
                print(i)


df.to_csv('/Volumes/SSD/Data/getVideoid_new.csv')
