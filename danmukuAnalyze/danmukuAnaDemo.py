from snownlp import SnowNLP
import pandas as pd
import matplotlib.pyplot as plt


# SNowNLP情感分析
def sentiment_score(text):
    if not text or text.isspace():
        return 0  # 返回默认值，例如0
    # 使用snownlp进行情感分析
    s = SnowNLP(text)
    # 返回情感分析得分
    return s.sentiments


df = pd.read_csv('/Users/indecreasy/Desktop/毕业设计/绘图数据/884514768.csv')
five_class = ['joy', 'disgust', 'fear', 'anger', 'sadness']
sentiment = ['sentiment_count_product']
coco = {'joy':'#ED8B16', 'disgust':'#C2BB00', 'fear':"#003547", 'anger':"#E1523D", 'sadness':"#003547", 'sentiment_count_product':'#ED8B16'}

# 定义移动平均窗口大小
window_size = 20

# 对每个情感维度计算移动平均
for column in df.columns:
    df[f'{column}_moving_average'] = df[column].rolling(window=window_size).mean()

selected_columns = five_class

plt.rcParams['font.sans-serif'] = ['Arial']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）

# 设置图形大小
plt.figure(figsize=(10, 6))

for column in selected_columns:
    if not column.endswith('_moving_average'):
        plt.plot(df[column], label=column, color=coco[column])

plt.xlabel('Time', fontsize=18)
plt.ylabel('Emotion Value', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.title('')
plt.legend(fontsize=14)
plt.show()


plt.figure(figsize=(10, 6))

for column in selected_columns:
    if column + '_moving_average' in df.columns:
        plt.plot(df[column + '_moving_average'], label=column + '_moving_average', linestyle='--', color=coco[column])

plt.xlabel('Time', fontsize=18)
plt.ylabel('Emotion Value', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.title('')
plt.legend(fontsize=14)
plt.show()



# 显示图形
plt.show()




# p = sentiment_score('Up主赶上的天气很好啊')
# p = sentiment_score('堵车堵成这个样子，难受')
# print(p)