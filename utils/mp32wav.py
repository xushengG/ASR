from pydub import AudioSegment

# 加载MP3文件
mp3_audio = AudioSegment.from_file("./examples/1.mp3")

# 导出为WAV格式
mp3_audio.export("output.wav", format="wav")