import requests
import json

if __name__ == '__main__':
    pageNum = 1
    url = 'https://api.github.com/repos/apache/superset/issues'
    params = {'state': 'all', 'page': pageNum, 'per_page': 100}
    headers = {'Authorization': 'token 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',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    response = requests.get(url, headers=headers, params=params)
    link_header = response.headers.get('Link')
    issuePath = './issues/'

    # 初始化自动翻页所需变量
    next_page_url = None

    # 记录issue链接与存放路径等
    f = open('./superset_issues.csv', 'w', encoding='utf-8')
    f.write(','.join(['title', 'body', 'labels', 'created_at', 'user', 'reactions']))
    f.write('\n')

    # 处理第一页响应
    print('正在爬取第{}页'.format(pageNum))
    json_data = json.loads(response.text)
    for issue in json_data:
        labels = json.dumps(issue['labels'], indent=2)
        if not isinstance(issue['labels'], str):
            labels = '|'.join(label['name'] for label in issue['labels']),
        else:
            labels = issue['labels']

        reactions = json.dumps(issue['reactions'], indent=2).replace('\n', '').replace('\r', ' ').replace('\t',
                                                                                                          '').replace(
            ',', ';')
        user = json.dumps(issue['user'], indent=2).replace('\n', '').replace('\r', '').replace('\t', '').replace(',',
                                                                                                                 ';')
        if not issue['body']:
            issue['body'] = ''
        if not issue['title']:
            issue['title'] = ''

        body = issue['body'].replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace(',', ';')
        line = ','.join(
            [issue['title'].replace(',', ';'), body, '&'.join(labels), issue['created_at'], user, reactions])
        f.write(line)
        f.write('\n')

    # 检查Link响应头是否有下一页的URL
    if link_header:
        links = link_header.split(', ')
        for link in links:
            if 'rel="next"' in link:
                next_page_url = link[link.index('<') + 1:link.index('>')]
                break

    try:
        # 循环处理下一页，直到没有下一页为止
        while next_page_url:
            pageNum += 1
            print('正在爬取第{}页'.format(pageNum))
            response = requests.get(next_page_url, headers=headers)
            link_header = response.headers.get('Link')

            json_data = json.loads(response.text)
            for issue in json_data:
                labels = json.dumps(issue['labels'], indent=2)
                if not isinstance(issue['labels'], str):
                    labels = '|'.join(label['name'] for label in issue['labels']),
                else:
                    labels = issue['labels']
                reactions = json.dumps(issue['reactions'], indent=2).replace('\n', '').replace('\r', ' ').replace('\t',
                                                                                                                  ' ').replace(
                    ',', ';')
                user = json.dumps(issue['user'], indent=2).replace('\n', '').replace('\r', ' ').replace('\t',
                                                                                                        ' ').replace(
                    ',', ';')
                if not issue['body']:
                    issue['body'] = ''
                if not issue['title']:
                    issue['title'] = ''
                body = issue['body'].replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace(',', ';')
                line = ','.join(
                    [issue['title'].replace(',', ';'), body, '&'.join(labels), issue['created_at'], user, reactions])
                f.write(line)
                f.write('\n')
            next_page_url = None
            if link_header:
                links = link_header.split(', ')
                for link in links:
                    if 'rel="next"' in link:
                        next_page_url = link[link.index('<') + 1:link.index('>')]
                        break
    except():
        print('已达到最大请求次数！')
    finally:
        f.close()
