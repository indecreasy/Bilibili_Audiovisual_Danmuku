import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import datetime

# mpl.use('TkAgg')  # !IMPORTANT

def duration(info_df):
    info_df.hist(column='video_cnt', bins=50, range=[0, 2000],
                 density=True, color='#005E54', label=False,
                 xlabelsize=18, ylabelsize=18, figsize=(10, 6), hatch="//")

    plt.xlabel('Duration(s)', fontsize=18)
    plt.ylabel('Frequency', fontsize=18)
    plt.title('')
    return

def danmuku(info_df):
    info_df.hist(column='danmuku_cnt', bins=50, range=[0, 3000],
                 density=True, color='#C2BB00', label=False,
                 xlabelsize=18, ylabelsize=18, figsize=(10, 6), hatch="//")

    plt.xlabel('Danmuku Amount', fontsize=18)
    plt.ylabel('Frequency', fontsize=18)
    plt.title('')
    return

def pdate(info_df):
    info_df.hist(column='datetime', bins=50,
                 density=False, color='#ED8B16', label=False,
                 xlabelsize=18, ylabelsize=18, figsize=(10, 6), hatch="//")
    # 设置横坐标轴标签的旋转角度
    plt.xticks(rotation=45)

    plt.xlabel('Publish Date', fontsize=18)
    plt.ylabel('Amount', fontsize=18)
    plt.tight_layout()
    plt.title('')
    return

def view_hist(info_df):
    info_df.hist(column='view', bins=50, range=[0, 1500000],
                 density=False, color='#E1523D', label=False,
                 xlabelsize=18, ylabelsize=18, figsize=(10, 6), hatch="")
    # 设置横坐标轴标签的旋转角度
    # plt.xticks(rotation=45)

    plt.xlabel('View', fontsize=18)
    plt.ylabel('Amount', fontsize=18)
    # plt.tight_layout()
    plt.title('')
    return

def quantile_data():
    # q1 = info_df['danmuku_cnt'].quantile(0.25)
    q1 = info_df['view'].quantile(0.25)
    q2 = info_df['danmuku_cnt'].quantile(0.5)
    q3 = info_df['danmuku_cnt'].quantile(0.75)
    p1 = info_df['video_cnt'].quantile(0.25)
    p2 = info_df['video_cnt'].quantile(0.5)
    p3 = info_df['video_cnt'].quantile(0.75)
    print(q1, q2, q3, p1, p2, p3)
    print(info_df['danmuku_cnt'].mean())
    print(info_df['video_cnt'].mean())

def select(df, index, threshold_value):
    # 根据条件筛选数据行
    condition = df[index] >= threshold_value
    selected_rows = df.loc[condition]

    # 将保留的数据行置于一个新表
    new_df = selected_rows.copy()

    return new_df


info_df = pd.read_csv('/Volumes/SSD/Data/VideoinfoCnt.csv')

info_df['datetime'] = pd.to_datetime(info_df['order_pubdate'])

plt.rcParams['font.sans-serif'] = ['Arial']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）

# info_df.hist(xlabelsize=10, ylabelsize=10, figsize=(12, 12))

# info_df = select(info_df, 'datetime', datetime.datetime(2022, 12, 1))
# info_df = select(info_df, 'video_cnt', 62)
# info_df = select(info_df, 'danmuku_cnt', 87)
# duration(info_df)
# danmuku(info_df)
# pdate(info_df)
# view_hist(info_df)
quantile_data()
print(len(info_df))

# info_df.to_csv("/Volumes/SSD/Data/VideoinfoCntNew.csv", index=False)
# plt.show()