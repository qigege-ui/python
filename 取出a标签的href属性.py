from bs4 import BeautifulSoup

file_path = 'C:/Users/qigege/Documents/bookmarks_2023_1_7.html'  # HTML文件的路径

# 读取HTML文件的内容
with open(file_path, 'r',encoding='utf-8') as f:
    html_doc = f.read()

# 使用BeautifulSoup解析HTML文档
soup = BeautifulSoup(html_doc, 'html.parser')

# 获取所有的A标签
a_tags = soup.find_all('a')

# 输出每个A标签的HREF属性值
for a in a_tags:
    print(a.get('href'))
