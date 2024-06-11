import numpy
import soundfile as sf
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def speaker_diarization(path):
    # path可以是本地文件路径

    # 将两个人的对话的音频分离为两个文件
    separation = pipeline(
        Tasks.speech_separation,
        model='damo/speech_mossformer2_separation_temporal_8k')
    result = separation(path)
    for i, signal in enumerate(result['output_pcm_list']):
        save_file = f'output_spk{i}.wav'
        sf.write(save_file, numpy.frombuffer(signal, dtype=numpy.int16), 8000)
    
if __name__=='__main__':
    path = 'mix_speech1.wav'
    speaker_diarization(path)