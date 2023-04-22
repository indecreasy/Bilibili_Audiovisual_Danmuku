import numpy as np
import pandas as pd
from pydub import AudioSegment
import librosa
from tqdm import tqdm
import os

'''
loudness：响度，表示音频信号的振幅大小。
pitch_0, pitch_1, ...：基频，表示音频信号中的主要频率成分。这些列包含了不同时间节点上的基频信息。
chroma_0, chroma_1, ...：音调，表示音频信号中的音高信息。这些列包含了不同时间节点上的音调信息。
mfcc_0, mfcc_1, ...：梅尔频率倒谱系数（MFCC），表示音频信号中的频谱特性。这些列包含了不同时间节点上的MFCC特征。
spectral_centroid：谱质心，表示音频信号的亮度或音色。这一列包含了不同时间节点上的谱质心信息。
spectral_rolloff：谱衰减，表示音频信号中的频率分布。这一列包含了不同时间节点上的谱衰减信息。
zero_crossing_rate：零交叉率，表示音频波形在零点上穿越的次数。这一列包含了不同时间节点上的零交叉率信息。
上述特征分别对应于不同的音频属性，如响度、音高、音色等。这些特征可以用于音频分析、音乐信息检索、音频分类等任务。

hop_length：512个样本（即每两个相邻帧之间的样本数）
frame_rate：音频的采样率（在load_audio_file()函数中获取）
要计算每帧的持续时间（以秒为单位），可以使用以下公式：
frame_duration = hop_length / frame_rate
要计算每秒钟的帧数，可以使用以下公式：
frames_per_second = frame_rate / hop_length
以一个具有44100Hz采样率的音频文件为例：
frame_duration = 512 / 44100 ≈ 0.0116秒
frames_per_second = 44100 / 512 ≈ 86帧
所以，在这个例子中，每帧持续时间约为0.0116秒，每秒钟有约86帧。这些值会根据音频的实际采样率和hop_length参数而有所不同。

要将每秒钟的帧数限制为60帧，您需要根据音频的采样率（frame_rate）调整hop_length参数。您可以使用以下公式计算所需的hop_length：
hop_length = frame_rate / frames_per_second
例如，对于具有44100Hz采样率的音频文件，要使每秒钟分成60帧，可以这样计算hop_length：
hop_length = 44100 / 60 ≈ 735
由于hop_length必须是整数，您可以将其四舍五入到最接近的整数，例如735。
然后，您可以在分析音频的analyze_audio()函数中更新hop_length参数

'''


def load_audio_file(file_path):
    audio = AudioSegment.from_file(file_path)
    audio_samples = audio.get_array_of_samples()
    audio_samples = np.array(audio_samples, dtype=np.float32)
    return audio_samples, audio.frame_rate

# 音调色度加权平均
def calculate_weighted_chroma(chroma_features):
    # 为每个音调分配权重
    weights = np.arange(1, 13)

    # 将Chroma features乘以相应的权重
    weighted_chroma = chroma_features * weights[:, np.newaxis]

    # 计算每个时间窗口中加权Chroma features的和
    weighted_chroma_sum = np.sum(weighted_chroma, axis=0)

    # 标准化加权和，使其在0到1之间
    weighted_chroma_normalized = (weighted_chroma_sum - np.min(weighted_chroma_sum)) / (
            np.max(weighted_chroma_sum) - np.min(weighted_chroma_sum))

    return weighted_chroma_normalized


def frequency_bands_pitch(pitches, low_freq=300, mid_freq=3000):
    # 根据给定的频率界限划分频率带
    low_band = np.mean(pitches[(pitches >= 0) & (pitches <= low_freq)], axis=0)
    mid_band = np.mean(pitches[(pitches > low_freq) & (pitches <= mid_freq)], axis=0)
    high_band = np.mean(pitches[pitches > mid_freq], axis=0)

    return low_band, mid_band, high_band

# 计算频率带强度
def frequency_bands_intensity(spectrum, frame_rate, low_freq=300, mid_freq=3000):
    n_fft = spectrum.shape[0] * 2
    freqs = np.fft.fftfreq(n_fft, 1 / frame_rate)[:n_fft // 2]
    low_band_intensity = np.mean(spectrum[(freqs >= 0) & (freqs <= low_freq), :], axis=0)
    mid_band_intensity = np.mean(spectrum[(freqs > low_freq) & (freqs <= mid_freq), :], axis=0)
    high_band_intensity = np.mean(spectrum[freqs > mid_freq, :], axis=0)

    return low_band_intensity, mid_band_intensity, high_band_intensity

# 下采样
def downsample(array, factor):
    # 计算需要删除的数据点的数量
    remainder = len(array) % factor
    if remainder != 0:
        # 删除数组末尾的余数个数据点
        array = array[:-remainder]
    # 重新调整数组形状并计算每个分组的平均值
    return np.mean(array.reshape(-1, factor), axis=1)


def analyze_audio(audio_samples, frame_rate, bvid):
    # 设置参数

    FRAMES = 0.5

    hop_length = int(round(frame_rate / FRAMES))  # 计算所需的hop_length
    n_fft = 2048

    # 计算响度
    loudness = librosa.feature.rms(y=audio_samples, frame_length=n_fft, hop_length=hop_length)

    # # 从音频样本中提取基频（pitch）
    # pitches, _ = librosa.piptrack(y=audio_samples, sr=frame_rate, n_fft=2048,
    #                               hop_length=frame_rate // 2)
    #
    # print(pitches)

    # # 计算基于基频的频率带
    # low_band_pitch, mid_band_pitch, high_band_pitch = frequency_bands_pitch(pitches, frame_rate, hop_length)

    # # Calculate total duration in seconds
    # pitches = np.transpose(pitches)
    # total_duration_seconds = pitches.shape[1] // frame_rate
    #
    # print(pitches, total_duration_seconds)
    #
    # # Initialize empty lists to store the averages
    # low_band_averages = []
    # mid_band_averages = []
    # high_band_averages = []
    #
    # for i in range(total_duration_seconds):
    #     # Calculate start and end frames for the current second
    #     start_frame = i * frame_rate
    #     end_frame = (i + 1) * frame_rate
    #
    #
    #
    #     # Calculate averages for the current second
    #     low_band_pitch, mid_band_pitch, high_band_pitch = frequency_bands_pitch(pitches, frame_rate,
    #                                                                             hop_length,
    #                                                                             start_frame,
    #                                                                             end_frame)
    #
    #     # Append the averages to the respective lists
    #     low_band_averages.append(low_band_pitch)
    #     mid_band_averages.append(mid_band_pitch)
    #     high_band_averages.append(high_band_pitch)
    #
    # print(low_band_averages,mid_band_averages,high_band_averages)

    # 计算音频信号的短时傅里叶变换（STFT）
    stft = np.abs(librosa.stft(audio_samples, n_fft=2048, hop_length=frame_rate // 2))

    # 计算频率带强度
    low_band_intensity, mid_band_intensity, high_band_intensity = frequency_bands_intensity(stft,
                                                                                            frame_rate)
    # 频率带强度进行下采样
    downsample_factor = 4
    low_band_intensity_downsampled = downsample(low_band_intensity, downsample_factor)
    mid_band_intensity_downsampled = downsample(mid_band_intensity, downsample_factor)
    high_band_intensity_downsampled = downsample(high_band_intensity, downsample_factor)


    # 计算音调色度
    chroma = librosa.feature.chroma_stft(y=audio_samples, sr=frame_rate, n_fft=n_fft,
                                         hop_length=hop_length)

    # 计算加权Chroma特征
    weighted_chroma = calculate_weighted_chroma(chroma)

    # 计算MFCC
    mfcc = librosa.feature.mfcc(y=audio_samples, sr=frame_rate, n_fft=n_fft, hop_length=hop_length)

    # 计算谱质心
    spectral_centroid = librosa.feature.spectral_centroid(y=audio_samples, sr=frame_rate,
                                                          n_fft=n_fft, hop_length=hop_length)

    # 计算谱衰减
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_samples, sr=frame_rate, n_fft=n_fft,
                                                        hop_length=hop_length)

    # 计算零交叉率
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=audio_samples, frame_length=n_fft,
                                                            hop_length=hop_length)

    # 创建数据序列
    data = {
        'loudness': loudness[0],
        # 'pitch': pitches,
        'chroma': chroma,
        'mfcc': mfcc,
        'spectral_centroid': spectral_centroid[0],
        'spectral_rolloff': spectral_rolloff[0],
        'zero_crossing_rate': zero_crossing_rate[0]
    }

    # 将数据序列保存到CSV文件
    loudness_df = pd.DataFrame(loudness.T, columns=['loudness'])
    chroma_df = pd.DataFrame(chroma.T, columns=[f'chroma_{i}' for i in range(chroma.shape[0])])
    mfcc_df = pd.DataFrame(mfcc.T, columns=[f'mfcc_{i}' for i in range(mfcc.shape[0])])
    spectral_centroid_df = pd.DataFrame(spectral_centroid.T, columns=['spectral_centroid'])
    spectral_rolloff_df = pd.DataFrame(spectral_rolloff.T, columns=['spectral_rolloff'])
    zero_crossing_rate_df = pd.DataFrame(zero_crossing_rate.T, columns=['zero_crossing_rate'])

    # 将基于基频的频率带信息添加到数据DataFrame中
    data_df = pd.concat(
        [loudness_df, chroma_df, mfcc_df, spectral_centroid_df, spectral_rolloff_df,
         zero_crossing_rate_df], axis=1)

    # # 获取数据的长度，以便为DataFrame创建索引
    # num_frames = len(data_df)
    #
    # low_band_pitch_df = pd.DataFrame({'low_band_pitch': low_band_pitch}, index=range(num_frames))
    # mid_band_pitch_df = pd.DataFrame({'mid_band_pitch': mid_band_pitch}, index=range(num_frames))
    # high_band_pitch_df = pd.DataFrame({'high_band_pitch': high_band_pitch}, index=range(num_frames))
    #
    # data_df = pd.concat([data_df, low_band_pitch_df, mid_band_pitch_df, high_band_pitch_df], axis=1)

    # 将频率带强度信息添加到数据DataFrame中
    low_band_intensity_df = pd.DataFrame(low_band_intensity_downsampled, columns=['low_band_intensity'])
    mid_band_intensity_df = pd.DataFrame(mid_band_intensity_downsampled, columns=['mid_band_intensity'])
    high_band_intensity_df = pd.DataFrame(high_band_intensity_downsampled, columns=['high_band_intensity'])

    data_df = pd.concat(
        [data_df, low_band_intensity_df, mid_band_intensity_df, high_band_intensity_df], axis=1)

    # 计算加权Chroma特征
    weighted_chroma = calculate_weighted_chroma(chroma)

    # 添加加权Chroma特征到DataFrame中
    weighted_chroma_df = pd.DataFrame({'weighted_chroma': weighted_chroma})
    data_df = pd.concat([data_df, weighted_chroma_df], axis=1)

    # 重置索引
    data_df = data_df.reset_index()

    # 重命名索引列为'second'
    data_df.rename(columns={'index': 'second'}, inplace=True)
    data_df.to_csv('/Volumes/SSD/Data/video/{}/{}_sound_1fps.csv'.format(bvid, bvid), index=True)


if __name__ == "__main__":
    # 读取csv中的bvid、cid
    video_list = pd.read_csv('/Volumes/SSD/Data/VideoinfoCntSelected.csv')
    bvid_list = video_list['bvid'].values.tolist()
    cid_list = video_list['cid'].values.tolist()

    for bvid in tqdm(bvid_list):
        mp3_file_path = '/Volumes/SSD/Data/video/{}/{}.mp3'.format(bvid, bvid)
        if not os.path.exists(mp3_file_path):
            continue

        csv_file_path = '/Volumes/SSD/Data/video/{}/{}_sound_1fps.csv'.format(bvid, bvid)
        # if os.path.exists(csv_file_path):
        #     print(f"File {bvid} already exists, skipping...")
        #     continue
        print(bvid)
        audio_samples, frame_rate = load_audio_file(mp3_file_path)
        analyze_audio(audio_samples, frame_rate, bvid)
