import string
def merge_timestamps(timestamps, time_gap):
    # 初始化结果列表
    res = []
    t = []
    # 遍历时间戳列表
    for i, (start, end) in enumerate(timestamps):
        # 如果是第一个时间戳，直接记录开始索引
        if i == 0:
            t.append(start)
            continue

        if timestamps[i][0] - timestamps[i-1][1] > time_gap:
            res.append(i)
            if i!=len(timestamps)-1:
                t.append(start)

        if i==len(timestamps)-1:
            res.append(i+1)

    return res, t 


def split_text(text, idx):
    res = []
    s = ''
    count =0
    for char in text:
        if char not in ['，','。','！','？']:
            count+=1
            s+=char
        if count in idx and s!='':
            res.append(s)
            s=''
    return res


def make_json(texts, timestamps, speaker_id, gap_time):
    idx, ts = merge_timestamps(timestamps, gap_time)
    split_texts = split_text(texts, idx)
    d = [{"Text": a, "SpeakerId": speaker_id, "BeginTime": b} for a,b in zip(split_texts, ts)]
    return d

# 示例
texts = '你好，我是客服，有什么可以帮您的。'
timestamps = [[1,2],[2,3],[5,6],[6,9],[9,10],[10,12],[20,21],[21,22],[22,23],[24,25],[25,26],[26,27],[27,28],[28,29]]

d = make_json(texts, timestamps, 0, 3)
print(d)