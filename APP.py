from flask import Flask, request, jsonify
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from funasr import AutoModel
import os

from utils.channel_split import audio_split
from utils.url_loader import get_file_from_url

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# 配置服务器以解析JSON数据
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.json.ensure_ascii = False

# 设置文件上传的目录,确保上传文件夹存在
UPLOAD_FOLDER = '/home/admini/gxs/ASR/download'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 全局变量，用于存储模型
spilt_model = None
recognize_model = None

def load_model():
    global split_model
    global recognize_model
    # 加载模型，这里替换为你加载模型的代码
    split_model = pipeline(
        Tasks.speech_separation,
        model='damo/speech_mossformer_separation_temporal_8k')

    recognize_model = AutoModel(model="paraformer-zh", model_revision="v2.0.4",
                    vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                    punc_model="ct-punc-c", punc_model_revision="v2.0.4",
                    # spk_model="cam++", spk_model_revision="v2.0.2",
                    )


@app.before_first_request
def initialize_model():
    load_model()


@app.route('/upload', methods=['POST'])
def ASR_func():

    # 文件上传
    data = request.form
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
                
        if file:
            # 保存文件到本地目录
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
    elif 'url' in data:
        url = data['url']
        path = get_file_from_url(url, UPLOAD_FOLDER)
        if path:
            pass
        else:
            return jsonify({"error": "Failed to download file from URL"}), 400
    else:
        return jsonify({"error": "No file or URL provided"}), 400

    # 人声分离
    file_name = path.split('/')[-1]
    file_name = file_name.split('.')[0]

    # 基于音轨
    audio_split(in_path=path,
            out_path1=f'./spl/{file_name}_spk0.wav',
            out_path2=f'./spl/{file_name}_spk1.wav')

    # 基于模型
    # spl = split_model(path)
    # r = []
    # for i, signal in enumerate(spl['output_pcm_list']):
    #     save_file = f'./spl/{file_name}_spk{i}.wav'
    #     sf.write(save_file, numpy.frombuffer(signal, dtype=numpy.int16), 8000)
    

    # 识别模块
    r1 = recognize_model.generate(input=f'./spl/{file_name}_spk0.wav', 
                batch_size_s=300, 
                hotword='魔搭')[0]
    r2 = recognize_model.generate(input=f'./spl/{file_name}_spk1.wav', 
                batch_size_s=300, 
                hotword='魔搭')[0]
    s1 = r1['text']
    s2 = r2['text']

    # 数字转写
    from chinese_itn import chinese_to_num
    s1=chinese_to_num(s1)
    s2=chinese_to_num(s2)

    print('speaker1: ', s1)
    print('speaker2: ', s2)
    t1 = r1['timestamp']
    t2 = r2['timestamp']

    from utils.post_process import make_json
    d1 = make_json(s1, t1, speaker_id=0, gap_time=1000)
    d2 = make_json(s2, t2, speaker_id=1, gap_time=1000)
    res = d1+d2
    res.sort(key=lambda x: x['BeginTime'])
        
    return jsonify({'message': 'File uploaded successfully', "status": "success", "result": res}), 200

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8766, debug=True, threaded=True)  # 运行在8765端口，允许外部访问
    app.run()
