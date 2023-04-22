import pandas as pd
import os




# 读取bvid和cid之间的对应关系
corresponding_csv = "/Volumes/SSD/Data/VideoinfoCntSelected.csv"
corresponding_df = pd.read_csv(corresponding_csv)

# 遍历每一行的对应关系
for index, row in corresponding_df.iterrows():
    bvid = row['bvid']
    cid = row['cid']

    # 读取三个CSV文件的路径
    bvid_csv1 = '/Volumes/SSD/Data/video/{}/{}_1fps.csv'.format(bvid, bvid)
    bvid_csv2 = '/Volumes/SSD/Data/video/{}/{}_sound_1fps.csv'.format(bvid, bvid)
    cid_csv3 = f'/Volumes/SSD/Data/AnaDanmuku/{cid}.csv'

    # 检查三个CSV文件是否都存在，如果任意一个不存在，则跳过该bvid
    if not (os.path.exists(bvid_csv1) and os.path.exists(bvid_csv2) and os.path.exists(cid_csv3)):
        print(f"Skipping bvid {bvid} due to missing file(s).")
        continue

    df1 = pd.read_csv(bvid_csv1)
    df2 = pd.read_csv(bvid_csv2)
    df3 = pd.read_csv(cid_csv3)

    # 以秒为索引，合并三个CSV文件
    merged_temp = df1.merge(df2, on='second', how='outer').merge(df3, on='second', how='outer')

    # 为缺失的数据添加空值（np.nan）
    merged_temp.fillna(value=pd.np.nan, inplace=True)

    # 将对应文件中的某些列的当前行值添加到新生成的表中
    merged_temp['bvid'] = row['bvid']
    merged_temp['cid'] = row['cid']
    merged_temp['view'] = row['view']
    merged_temp['reply'] = row['reply']
    merged_temp['favorite'] = row['favorite']
    merged_temp['coin'] = row['coin']
    merged_temp['share'] = row['share']
    merged_temp['like'] = row['like']
    merged_temp['order_pubdate'] = row['order_pubdate']
    merged_temp['duration'] = row['video_cnt']
    merged_temp['danmuku_amount'] = row['danmuku_cnt']

    # 创建目录来保存合并后的CSV文件，如果目录不存在
    output_dir = "/Volumes/SSD/Data/Merge_selected"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 保存合并后的DataFrame到CSV文件
    output_file = os.path.join(output_dir, f"{bvid}_merged.csv")
    merged_temp.to_csv(output_file, index=False)
