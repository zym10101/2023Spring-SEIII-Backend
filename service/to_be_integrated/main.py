import requests
import json

'''
create by syj
'''
if __name__ == '__main__':
    pageNum = 1
    url = 'https://api.github.com/repos/apache/superset/issues'
    params = {'state': 'all','page':pageNum,'per_page':100}
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url, headers=headers, params=params)
    link_header = response.headers.get('Link')
    issuePath = './issues/'

    # 初始化自动翻页所需变量
    next_page_url = None


    # 记录issue链接与存放路径等
    f = open('./superset.csv', 'w', encoding='utf-8')
    f.write(','.join(['title', 'url', 'filepath']))
    f.write('\n')

    # 处理第一页响应
    print('正在爬取第{}页'.format(pageNum))
    json_data = json.loads(response.text)
    for issue in json_data:
        issue_details = {'title': issue['title'], 'url': issue['html_url'], 'body': issue['body']}
        issueId = issue_details['url'].split('/')[-1]
        filepath = issuePath + 'superset-issue-' + issueId + '.md'
        with open(filepath, 'w', encoding='utf-8') as ff:
            if issue_details['body'] is not None:
                ff.write(issue_details['body'])
            else:
                ff.write('null')
        line = ','.join([issue['title'], issue['url'], filepath])
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
        while pageNum<1:
            pageNum += 1
            print('正在爬取第{}页'.format(pageNum))
            response = requests.get(next_page_url, headers=headers)
            link_header = response.headers.get('Link')

            json_data = json.loads(response.text)
            for issue in json_data:
                issue_details = {'title': issue['title'].replace(',', '.'), 'url': issue['html_url'], 'body': issue['body']}
                issueId = issue_details['url'].split('/')[-1]
                filepath = issuePath + 'superset-issue-' + issueId + '.md'
                with open(filepath, 'w', encoding='utf-8') as ff:
                    if issue_details['body'] is not None:
                        ff.write(issue_details['body'])
                    else:
                        ff.write('null')
                line = ','.join([issue['title'], issue['url'], filepath])
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
        print('以达到最大请求次数！')
    finally:
        f.close()

