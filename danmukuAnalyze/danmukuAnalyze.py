# 导入必要的库
import pandas as pd
import jieba
import re
from snownlp import SnowNLP
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
from tqdm import tqdm


def document_to_list(path):
    """
    读取文档，按行划分，返回列表

    :param path: 目标文档路径
    :return doc_l: 文档内容列表
    """
    print("正在将%s转换为文本列表, 请稍等..." % path)
    doc_list = []
    with open(path, 'r', encoding='utf-8') as doc_f:
        for line in doc_f.readlines():
            line = line.strip('\n')
            doc_list.append(line)
    return doc_list

# 对弹幕内容进行分词和清理
def clean_text(text):
    # 使用正则表达式删除特殊字符
    text = re.sub(r"[^\w\s]", "", text)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    return text.strip()


def count(cut_list):
    """
    闭包函数B，构建情绪向量 emo_cnt, 判断微博情绪（存在无情绪 None 和复杂情绪 [..., ...]情况）

    :param cut_list:
    :return emo_cnt: 情绪向量
            wb_emo: 判断的本条微博情绪
    """
    emo_cnt = {"anger": 0, "disgust": 0, "fear": 0, "joy": 0, "sadness": 0}
    danmuku_emotion = []
    for word in cut_list:
        if word in anger:
            emo_cnt["anger"] += 1
        if word in disgust:
            emo_cnt["disgust"] += 1
        if word in fear:
            emo_cnt["fear"] += 1
        if word in joy:
            emo_cnt["joy"] += 1
        if word in sadness:
            emo_cnt["sadness"] += 1

    emo_max = max(emo_cnt.values())

    if emo_max == 0:
        danmuku_emotion.append("none")
    else:
        for key, value in emo_cnt.items():
            if value == emo_max:
                danmuku_emotion.append(key)

    if len(danmuku_emotion) == 1:
        danmuku_emotion = danmuku_emotion[0]
    else:
        danmuku_emotion = "complex"

    return emo_cnt

# SNowNLP情感分析
def sentiment_score(text):
    if not text or text.isspace():
        return 0  # 返回默认值，例如0
    # 使用snownlp进行情感分析
    s = SnowNLP(text)
    # 返回情感分析得分
    return s.sentiments


global anger_path, disgust_path, fear_path, joy_path, sadness_path
anger_path = "0_Res/anger.txt"
disgust_path = "0_Res/disgust.txt"
fear_path = "0_Res/fear.txt"
joy_path = "0_Res/joy.txt"
sadness_path = "0_Res/sadness.txt"

anger = document_to_list(anger_path)
disgust = document_to_list(disgust_path)
fear = document_to_list(fear_path)
joy = document_to_list(joy_path)
sadness = document_to_list(sadness_path)

global stopwords
stopwords = document_to_list("0_Res/stopwords_list.txt")
document_list = document_to_list("0_Res/weibo.txt")

def Analyze(cid):

    DANMUKU_PATH = f'/Volumes/SSD/Data/Danmuku/{cid}.csv'
    SAVE_PATH = f'/Volumes/SSD/Data/AnaDanmuku/{cid}.csv'

    print(cid)

    df = pd.read_csv(DANMUKU_PATH, encoding='utf-8', error_bad_lines=False)

    # 删除重复数据
    df = df.drop_duplicates()

    df['content'] = df['content'].astype(str)
    df['content_clean'] = df['content'].apply(clean_text)

    df['emo_cnt'] = df['content_clean'].apply(count)

    df['anger'] = df['emo_cnt'].apply(lambda x:x['anger'])
    df['disgust'] = df['emo_cnt'].apply(lambda x:x['disgust'])
    df['fear'] = df['emo_cnt'].apply(lambda x:x['fear'])
    df['joy'] = df['emo_cnt'].apply(lambda x:x['joy'])
    df['sadness'] = df['emo_cnt'].apply(lambda x:x['sadness'])
    df['sentiment'] = df['content_clean'].apply(sentiment_score)


    # 将progress列的数据类型转换为浮点数
    df['progress'] = pd.to_numeric(df['progress'], errors='coerce')

    # 去除progress为空的行
    df = df.dropna(subset=['progress'])

    # 将毫秒转换为秒并向下取整
    df['progress'] = df['progress'].astype(int)
    df['second'] = df['progress'] // 1000

    # 按照progress_seconds分组并计算每秒的angry、joy、disgust、fear和sadness值总和
    sum_per_second = df.groupby('second')[['anger', 'joy', 'disgust', 'fear', 'sadness']].sum().reset_index()

    # 将结果赋值给一个新的数据框
    result_df = pd.DataFrame(sum_per_second)

    # 按照progress_seconds分组并计算每秒的sentiment列的平均值
    sentiment_mean_per_second = df.groupby('second')['sentiment'].mean().reset_index()

    # 按照second分组并计算每秒的弹幕总数
    danmuku_count_per_second = df.groupby('second')['content'].count().reset_index()

    # 将计算得到的sentiment平均值和弹幕总数添加到result_df数据框中
    result_df = result_df.merge(sentiment_mean_per_second, on='second')
    result_df = result_df.merge(danmuku_count_per_second, on='second')

    # 计算sentiment_count_product列的值，该值为每组的弹幕总数与sentiment平均值的乘积
    result_df['sentiment_count_product'] = result_df['sentiment'] * result_df['content']

    # 保存结果到CSV文件
    result_df.to_csv(SAVE_PATH)

    return


# 读取csv中的bvid、cid
video_list = pd.read_csv('/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot.csv')
cid_list = video_list['cid'].values.tolist()

for cid in tqdm(cid_list):
    DANMUKU_PATH = f'/Volumes/SSD/Data/Danmuku/{cid}.csv'
    SAVE_PATH = f'/Volumes/SSD/Data/AnaDanmuku/{cid}.csv'

    # 读取弹幕文件
    if not os.path.exists(DANMUKU_PATH):
        print(f"Skipping bvid {cid} due to missing file(s).")
        continue

    if os.path.exists(SAVE_PATH):
        print(f"Skipping bvid {cid} due to finish.")
        continue

    Analyze(cid)
