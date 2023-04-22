import pandas as pd
import os
from tqdm import tqdm

# 读取bvid和cid之间的对应关系
corresponding_csv = "/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot.csv"
corresponding_df = pd.read_csv(corresponding_csv)


# 定义一个函数，用于计算CSV文件的行数
def count_rows(csv_file):
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        return len(df)
    return None


# 初始化新的三列，用于存储行数
corresponding_df['bvid_csv1_rows'] = None
corresponding_df['bvid_csv2_rows'] = None
corresponding_df['cid_csv3_rows'] = None

# 遍历每一行的对应关系
for index, row in tqdm(corresponding_df.iterrows()):
    bvid = row['bvid']
    cid = row['cid']

    # 读取三个CSV文件的路径
    bvid_csv1 = '/Volumes/SSD/Data/video/{}/{}_1fps.csv'.format(bvid, bvid)
    bvid_csv2 = '/Volumes/SSD/Data/video/{}/{}_sound_1fps.csv'.format(bvid, bvid)
    cid_csv3 = f'/Volumes/SSD/Data/Danmuku/{cid}.csv'

    # 计算每个CSV文件的行数，并将结果存储在新的列中
    corresponding_df.loc[index, 'bvid_csv1_rows'] = count_rows(bvid_csv1)
    corresponding_df.loc[index, 'bvid_csv2_rows'] = count_rows(bvid_csv2)
    corresponding_df.loc[index, 'cid_csv3_rows'] = count_rows(cid_csv3)

# 保存结果到新的CSV文件
corresponding_df.to_csv('/Volumes/SSD/Data/VideoinfoCnt.csv', index=False)
