from funasr import AutoModel
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def recognize(path):
    # paraformer-zh is a multi-functional asr model
    # use vad, punc, spk or not as you need
    # model = AutoModel(model="paraformer-zh", model_revision="v2.0.4",
    #                 vad_model="fsmn-vad", vad_model_revision="v2.0.4",
    #                 punc_model="ct-punc-c", punc_model_revision="v2.0.4",
    #                 # spk_model="cam++", spk_model_revision="v2.0.2",
    #                 )
    model = AutoModel(model="Whisper-large-v3",
                    # vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                    # punc_model="ct-punc-c", punc_model_revision="v2.0.4",
                    # spk_model="cam++", spk_model_revision="v2.0.2",
                    )
    res = model.generate(input=path, 
                batch_size_s=300, 
                hotword='魔搭')
    return res

if __name__=='__main__':
    path = './download/2.wav'
    res = recognize(path)
    print(res)
    # texts=res[0]['text']
    # timestamps = res[0]['timestamp']
    # print(texts)

    # from utils.post_process import make_json
    # d = make_json(texts, timestamps, 0, 500)
    # print(d)
    