import hashlib
import requests
import time
import json
import difflib

def compare_files(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, \
         open(file2, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        diff = difflib.ndiff(lines1, lines2)
        diffs = list(diff)
        similarity = 1 - (len(diffs) / max(len(lines1), len(lines2)))
        return diffs, similarity

def baidu_translate(content, from_lang, to_lang):
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    appid = '20181128000240536'
    secretKey = 'M7VYNBlDDU6VnrshD8dG'
    salt = '1435660288'

    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    data = {
        'q': content,
        'from': from_lang,
        'to': to_lang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }
    res = requests.get(url, params=data)
    print(res)
    result = json.loads(res.text)
    if 'error_code' in result:
        print('翻译失败，错误码：', result['error_code'])
        return ''
    else:
        return result['trans_result'][0]['dst']

languages = ['zh', 'en', 'ru', 'fra','de','jp','th','kor','pt', 'it', 'en', 'zh']
output_file = 'test.txt'
input_file = 'cx.txt'
output_file_compare = 'test_compare.txt'

with open(input_file, 'r', encoding='utf-8') as f_input, \
     open(output_file, 'w', encoding='utf-8') as f_output, \
     open(output_file_compare, 'w', encoding='utf-8') as f_compare:
    for line in f_input:
        original_line = line.strip()
        for i in range(len(languages)-1):
            from_lang = languages[i]
            to_lang = languages[i+1]
            line = baidu_translate(line, from_lang, to_lang)
            time.sleep(1)
        f_output.write(line + '\n')
        print(line)
        diffs, similarity = compare_files(input_file, output_file)
        f_compare.write(f'Original: {original_line}\n')
        f_compare.write(f'Translated: {line}\n')
        f_compare.write(f'Similarity: {similarity}\n')
        f_compare.write('\n')
        print(f'相似度: {similarity}')
