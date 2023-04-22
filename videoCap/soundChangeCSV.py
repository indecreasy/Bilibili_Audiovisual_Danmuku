import pandas as pd
import os
from tqdm import tqdm

if __name__ == "__main__":
    # 读取csv中的bvid、cid
    video_list = pd.read_csv('/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot.csv')
    bvid_list = video_list['bvid'].values.tolist()
    cid_list = video_list['cid'].values.tolist()

    for bvid in tqdm(bvid_list):

        csv_file_path = '/Volumes/SSD/Data/video/{}/{}_sound_1fps.csv'.format(bvid, bvid)
        if not os.path.exists(csv_file_path):
            print(f"File {bvid} not exists, skipping...")
            continue

        df = pd.read_csv(csv_file_path, index_col=False)

        # 重命名索引列为'second'
        df.rename(columns={df.columns[0]: 'second'}, inplace=True)
        # 将"loudness.1"列重命名为"loudness"
        data = df.rename(columns={'loudness.1': 'loudness'})

        # 保存修改后的CSV文件
        new_csv_file_path = csv_file_path
        data.to_csv(new_csv_file_path, index=False)
