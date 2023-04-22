import time

import pandas as pd
import requests
import google.protobuf.message as _message
import google.protobuf.text_format as text_format
import bilibili_pb2 as Danmaku
from tqdm import tqdm


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
            'cookie': "buvid3=02BCD2D1-8129-458C-A368-61A547780351167610infoc; b_nut=1641810078; "
                      "blackside_state=1; CURRENT_FNVAL=4048; "
                      "buvid4=88DF7015-38C5-514A-6AFE-3545F07A20C335687-022031319-tnbHT8NXYV66"
                      "+VWxVRQjkg==; i-wanna-go-back=-1; rpdid=|(u)~lkRllmJ0J'uY~|J|)JRJ; "
                      "CURRENT_QUALITY=16; DedeUserID=14912106; "
                      "DedeUserID__ckMd5=b3e3a7794ac9f603; "
                      "fingerprint=e2f3a1579282fcc61520136d52c16425; buvid_fp_plain=undefined; "
                      "b_ut=5; buvid_fp=e2f3a1579282fcc61520136d52c16425; is-2022-channel=1; "
                      "PVID=1; bp_video_offset_14912106=747598762403168300; nostalgia_conf=-1; "
                      "innersign=0; b_lsid=4ED58F87_185B55309BD; bsource=search_bing; "
                      "_uuid=D22D19CC-F18E-CF15-6545-1010D1F1A21AC996230infoc; SESSDATA=023bfd72,"
                      "1689336398,fad2f*11; bili_jct=3d804d633efe41207c922808d926d6c4; "
                      "sid=6zep113r".encode(
                'utf-8').decode('latin1'),
            'origin': 'https://www.bilibili.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
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
            print(f"cid {cid} begin!")
            date_former = "2023-03-13"
            with open(f"/Volumes/SSD/Data/Danmuku/{cid}.csv", "a") as f:
                f.write("danmaku_id,progress,mode,fontsize,color,midHash,content,ctime,orderStyleTime,weight,action,pool,idStr\n")
            date_latter = 0
            api = 'http://api.bilibili.com/x/v2/dm/web/history/seg.so'

            while True:
                params = {
                    'type': 1,
                    'oid': cid,
                    'date': date_former
                }
                cookies = {
                    'SESSDATA': '023bfd72%2C1689336398%2Cfad2f%2A11'
                }
                resp = requests.get(api, params=params, cookies=cookies)
                data = resp.content

                try:
                    danmaku_seg = Danmaku.DmSegMobileReply()
                    danmaku_seg.ParseFromString(data)
                except _message.DecodeError:
                    # time.sleep(10)
                    print("error")
                    self.error_list.append(cid)
                    continue

                ctime = self.save_danmaku(danmaku_seg, cid)
                date_latter = self._timestamp2date(ctime)
                print(f"get new date: {date_latter}")

                if date_latter == date_former:
                    break

                date_former = date_latter
                time.sleep(3)

            # self.save_sample(cid)
            print(f"cid {cid} done! rest for 30s!")
            time.sleep(3)

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
            "otherStyleTime":"",
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
        return min(ctime_list)

    def save_sample(self):
        with open("./danmaku/sample.csv", "a") as f:
            f.write("cid,title,duration,ctime\n")
            for cid in self.CID_DICT:
                f.write(f"{cid}," + ",".join(self.CID_DICT[cid]) + "\n")


if __name__ == "__main__":
    info_pd = pd.read_csv('/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot.csv')
    cid_list = info_pd['cid'].values.tolist()

    print(cid_list)

    bdc = BilibiliDanmakuCrawler(
        cid=cid_list
    )

    bdc.get_danmaku()
    # with open("todo.txt", "w") as f:
    #     for cid in bdc.error_list:
    #         f.write(f"\"{cid}\"\n")
