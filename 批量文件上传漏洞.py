import requests
import threading
import csv

# 设置测试的文件后缀名
extensions = ['php', 'jsp', 'html','jSp','Htm','Html','xml']

# 设置线程数量
thread_num = 10

# 读取目标URL列表
with open('targets.txt', 'r') as f:
    target_urls = f.read().splitlines()

with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = ['url', 'payload', 'status','data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

# 构造HTTP请求头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Referer': 'https://www.migu.cn/'
}

# 构造HTTP请求体，用于上传文件
data = {
    'uploadfile': 'test',
    'filename': 'test'
}

# 定义测试函数
def test_upload_vuln(url):
    for ext in extensions:
        # 构造要上传的文件名
        filename = 'test.' + ext
        # 尝试上传文件
        files = {'file': (filename, 'test')}
        try:
            response = requests.post(url, headers=headers, files=files, data=data)
            status = response.status_code
            # 将结果写入表格
            #writer.writerow({'url': url, 'payload': payload, 'status': status})
            # 判断是否上传成功
            if response.status_code == 200:
                writer.writerow({'url': url, 'payload': payload, 'status': status,'data':response.text})
                #print('[+] %s has arbitrary file upload vulnerability!' % url)
                break
        except:
            pass

# 定义多线程函数
def thread_work(start, end):
    for i in range(start, end):
        test_upload_vuln(target_urls[i])

# 定义主函数
def main():
    # 计算每个线程要处理的URL数量
    url_num = len(target_urls)
    thread_list = []
    each_thread_num = url_num // thread_num

    # 创建多个线程，并分配URL进行测试
    for i in range(thread_num):
        start = i * each_thread_num
        end = (i + 1) * each_thread_num
        if i == thread_num - 1:
            end = url_num
        t = threading.Thread(target=thread_work, args=(start, end))
        thread_list.append(t)

    # 启动多个线程
    for t in thread_list:
        t.start()

    # 等待所有线程结束
    for t in thread_list:
        t.join()

if __name__ == '__main__':
    main()
