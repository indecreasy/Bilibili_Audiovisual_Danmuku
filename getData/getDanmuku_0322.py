import time
import pandas as pd
import requests
import google.protobuf.message as _message
import google.protobuf.text_format as text_format
import bilibili_pb2 as Danmaku
from tqdm import tqdm
import random
import os
from random import choice

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
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

SUCCESS_CID_PATH = "/Volumes/SSD/Data/Danmuku/successful_cids.csv"
ERROR_CID_PATH = "/Volumes/SSD/Data/Danmuku/error_cids.csv"


class BilibiliDanmakuCrawler:
    CID_DICT = {}  # 该类将要爬取的cid对应字典
    error_list = []

    def __init__(self, aid=None, bvid=None, cid=None):
        self.aid = aid
        self.bvid = bvid
        self.cid = cid
        if self.aid:
            for a in self.aid:
                self.aid2cid(a)
        if self.bvid:
            for b in self.bvid:
                self.bvid2cid(b)
        if self.cid:
            for c in self.cid:
                self.CID_DICT[c] = 1
        # self.save_sample()

    def _timestamp2date(self, timestamp):
        return time.strftime("%Y-%m-%d", time.localtime(timestamp))

    def get_response(self, url, params):

        headers = {
            'User-Agent': random.choice(user_agents),
            'Referer': 'https://www.bilibili.com/',
            'cookie': "innersign=0; buvid3=11BA7585-F79D-84DA-D884-3D12E52C8D6A85488infoc; b_nut=1679624385; i-wanna-go-back=-1; b_ut=7; b_lsid=10115DF1D_187116A3643; bsource=search_bing; _uuid=2E25A9FE-1F9E-410CB-EA9A-6610AE1FCDFEE86123infoc; buvid_fp=02159999855aa23e58b705a96f3eb104; header_theme_version=undefined; home_feed_column=4; buvid4=C3C48BD5-4A70-A2BE-5DA1-F0EFEDE2C0E886737-023032410-lPDfLWkp3QAR0h64UBfgCQ%3D%3D; CURRENT_FNVAL=4048; SESSDATA=d4c2659d%2C1695176506%2C3d709%2A32; bili_jct=2580ec34129c08a095a53f64180a6533; DedeUserID=14912106; DedeUserID__ckMd5=b3e3a7794ac9f603; sid=qlwzah35",
            'origin': 'https://www.bilibili.com',
        }

        resp = requests.get(url=url, headers=headers, params=params)
        data = resp.json()
        return data

    def aid2cid(self, aid):
        api = f"https://api.bilibili.com/x/web-interface/view"
        params = {
            "aid": aid
        }
        data = self.get_response(api, params)["data"]
        pubdate = self._timestamp2date(data["pubdate"])
        for dic in data["pages"]:
            self.CID_DICT[str(dic["cid"])] = [dic["part"], str(dic["duration"]), pubdate]

    def bvid2cid(self, bvid):
        api = f"https://api.bilibili.com/x/web-interface/view"
        params = {
            "bvid": bvid
        }
        data = self.get_response(api, params)["data"]
        pubdate = self._timestamp2date(data["pubdate"])
        self.CID_DICT[str(data["cid"])] = [data["title"], data["duration"], pubdate]

    def get_danmaku(self):
        for cid in tqdm(self.CID_DICT):
            # 加载已成功保存的cid列表
            successful_cids = self.load_successful_cids()

            # 检查是否已经保存成功
            if cid in successful_cids:
                print(f"cid {cid} already saved, skipping...")
                continue

            print(f"cid {cid} begin!")
            date_former = "2023-03-23"
            with open(f"/Volumes/SSD/Data/Danmuku/{cid}.csv", "a") as f:
                f.write(
                    "danmaku_id,progress,mode,fontsize,color,midHash,content,ctime,orderStyleTime,weight,action,pool,idStr\n")
            date_latter = 0
            api = 'http://api.bilibili.com/x/v2/dm/web/history/seg.so'

            while True:
                params = {
                    'type': 1,
                    'oid': cid,
                    'date': date_former
                }
                cookies = {
                    'SESSDATA': 'd4c2659d%2C1695176506%2C3d709%2A32'
                }
                resp = requests.get(api, params=params, cookies=cookies)
                data = resp.content

                print(data)

                try:
                    danmaku_seg = Danmaku.DmSegMobileReply()
                    danmaku_seg.ParseFromString(data)
                except _message.DecodeError:
                    with open(ERROR_CID_PATH, "a") as error_file:
                        error_file.write(f"{cid}\n")
                        print(f"Cannot get danmaku_seg for cid {cid}. Skipping...")
                    break

                ctime = self.save_danmaku(danmaku_seg, cid)

                if ctime is None:
                    print(f"Empty ctime_list for cid {cid}. Skipping...")
                    break

                date_latter = self._timestamp2date(ctime)
                print(f"get new date: {date_latter}")

                if date_latter == date_former:
                    break

                date_former = date_latter
                time.sleep(10)

            # self.save_sample(cid)
            print(f"cid {cid} done! rest for 3s!")

            # 记录成功保存的cid
            self.record_successful_cid(cid)

            time.sleep(10)

    def load_successful_cids(self):
        successful_cids_filepath = SUCCESS_CID_PATH
        if not os.path.exists(successful_cids_filepath):
            with open(successful_cids_filepath, "w") as f:
                f.write("cid\n")
            return set()
        else:
            successful_cids_df = pd.read_csv(successful_cids_filepath)
            return set(successful_cids_df["cid"].values.tolist())

    def record_successful_cid(self, cid):
        with open(SUCCESS_CID_PATH, "a") as f:
            f.write(f"{cid}\n")

    def match(self, one_piece):
        dic = {
            "id": "",
            "progress": "",
            "mode": "",
            "fontsize": "",
            "color": "",
            "midHash": "",
            "content": "",
            "ctime": "",
            "otherStyleTime": "",
            "weight": "",
            "action": "",
            "pool": "",
            "idStr": ""
        }
        one_piece_ls = one_piece.split("\n")
        for ele in one_piece_ls:
            try:
                colname, value = ele.split(": ", maxsplit=1)
                if colname in dic:
                    if colname == "content":
                        value = value.replace(",", "，")
                    # if colname == "midHash":
                    #     dic["mid"] = str(HashAttack.attack(eval(value)))
                    #     print("attack success")
                    dic[colname] = str(eval(value))
                else:
                    continue
            except:
                continue
        return dic

    def remove_duplicates(self, cid):
        filepath = f"/Volumes/SSD/Data/Danmuku/{cid}.csv"
        df = pd.read_csv(filepath)
        df.drop_duplicates(subset='danmaku_id', inplace=True)
        df.to_csv(filepath, index=False)

    def save_danmaku(self, danmaku_seg, cid):
        n = len(danmaku_seg.elems)
        ctime_list = []
        with open(f"/Volumes/SSD/Data/Danmuku/{cid}.csv", "a") as f:
            for i in range(n):
                one_piece = text_format.MessageToString(danmaku_seg.elems[i], as_utf8=True)
                dic = self.match(one_piece)

                timeStamp = int(dic['ctime'])
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                dic['otherStyleTime'] = otherStyleTime

                res = ",".join(dic.values())
                f.write(res)
                f.write("\n")
                ctime_list.append(int(dic["ctime"]))

        # 去重并保存

        print('ctime_list:')
        print(ctime_list)
        if len(ctime_list) == 0:
            if len(ctime_list) == 0:
                with open(ERROR_CID_PATH, "a") as error_file:
                    error_file.write(f"{cid}\n")
                return None

        return min(ctime_list)

    def save_sample(self):
        with open("./danmaku/sample.csv", "a") as f:
            f.write("cid,title,duration,ctime\n")
            for cid in self.CID_DICT:
                f.write(f"{cid}," + ",".join(self.CID_DICT[cid]) + "\n")


if __name__ == "__main__":
    info_pd = pd.read_csv('/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot_1.csv')
    cid_list = info_pd['cid'].values.tolist()

    # print(cid_list)

    bdc = BilibiliDanmakuCrawler(
        cid=cid_list
    )

    bdc.get_danmaku()
    # with open("todo.txt", "w") as f:
    #     for cid in bdc.error_list:
    #         f.write(f"\"{cid}\"\n")
