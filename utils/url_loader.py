import requests
import os

def get_file_from_url(url, folder):
    # 从 URL 获取内容
    response = requests.get(url)
    if response.status_code == 200:
        # 为下载的文件设置一个安全文件名
        filename = url.split('/')[-1]
        file_path = os.path.join(folder, filename)
        # 保存文件
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    else:
        return None