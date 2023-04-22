import numpy as np
import pandas as pd
from pydub import AudioSegment
import librosa
from tqdm import tqdm
import os


def load_audio_file(file_path):
    audio = AudioSegment.from_file(file_path)
    audio_samples = audio.get_array_of_samples()
    audio_samples = np.array(audio_samples, dtype=np.float32)
    return audio_samples, audio.frame_rate


def analyze_audio(audio_samples, frame_rate, bvid):
    # 设置参数

    FRAMES = 1

    hop_length = int(round(frame_rate / FRAMES))  # 计算每秒30帧所需的hop_length
    n_fft = 2048

    # 计算响度
    loudness = librosa.feature.rms(y=audio_samples, frame_length=n_fft, hop_length=hop_length)

    # 计算基频
    pitches, _ = librosa.piptrack(y=audio_samples, sr=frame_rate, n_fft=n_fft,
                                  hop_length=hop_length)

    # 计算音调
    chroma = librosa.feature.chroma_stft(y=audio_samples, sr=frame_rate, n_fft=n_fft,
                                         hop_length=hop_length)

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
        'pitch': pitches,
        'chroma': chroma,
        'mfcc': mfcc,
        'spectral_centroid': spectral_centroid[0],
        'spectral_rolloff': spectral_rolloff[0],
        'zero_crossing_rate': zero_crossing_rate[0]
    }

    # 将数据序列保存到CSV文件
    loudness_df = pd.DataFrame(loudness.T, columns=['loudness'])
    pitch_df = pd.DataFrame(pitches.T, columns=[f'pitch_{i}' for i in range(pitches.shape[0])])
    chroma_df = pd.DataFrame(chroma.T, columns=[f'chroma_{i}' for i in range(chroma.shape[0])])
    mfcc_df = pd.DataFrame(mfcc.T, columns=[f'mfcc_{i}' for i in range(mfcc.shape[0])])
    spectral_centroid_df = pd.DataFrame(spectral_centroid.T, columns=['spectral_centroid'])
    spectral_rolloff_df = pd.DataFrame(spectral_rolloff.T, columns=['spectral_rolloff'])
    zero_crossing_rate_df = pd.DataFrame(zero_crossing_rate.T, columns=['zero_crossing_rate'])

    data_df = pd.concat(
        [loudness_df, pitch_df, chroma_df, mfcc_df, spectral_centroid_df, spectral_rolloff_df,
         zero_crossing_rate_df], axis=1)
    data_df.to_csv('/Volumes/SSD/Data_demo/video/{}/{}_sound_1fps.csv'.format(bvid, bvid), index=True)


if __name__ == "__main__":
    # 读取csv中的bvid、cid
    video_list = pd.read_csv('/Volumes/SSD/Data/getVideoinfo/getVideoinfo_byhot_1.csv')
    bvid_list = video_list['bvid'].values.tolist()
    cid_list = video_list['cid'].values.tolist()

    for bvid in tqdm(bvid_list):
        mp3_file_path = '/Volumes/SSD/Data_demo/video/{}/{}.mp3'.format(bvid, bvid)
        if not os.path.exists(mp3_file_path):
            continue
        audio_samples, frame_rate = load_audio_file(mp3_file_path)
        analyze_audio(audio_samples, frame_rate, bvid)