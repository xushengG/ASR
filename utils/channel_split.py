from pydub import AudioSegment

def audio_split(in_path, out_path1, out_path2):
# 加载MP3或wav文件
    audio = AudioSegment.from_mp3(in_path)

    # 分离左声道和右声道
    left_channel = audio.split_to_mono()[0]
    right_channel = audio.split_to_mono()[1]

    # 导出左声道和右声道到单独的MP3文件
    left_channel.export(out_path1, format="wav")
    right_channel.export(out_path2, format="wav")

    print("双音轨分离完成!")

audio_split(in_path='/home/admini/gxs/ASR/download/2.mp3',
            out_path1='/home/admini/gxs/ASR/spl/test_1.wav',
            out_path2='/home/admini/gxs/ASR/spl/test_2.wav')