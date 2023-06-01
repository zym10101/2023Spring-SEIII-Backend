import json
import re


def addLineNo():
    with open('人工标注.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        file.seek(0)
        for index, line in enumerate(lines, start=1):
            file.write(f"{index}. {line}")
        file.truncate()


def getSentiment():
    with open('人工标注sentiment.txt', 'r', encoding='utf-8') as file:
        sentiment_result = []
        for line in file:
            sentiment_result.append(line.split()[0])
    return sentiment_result


# if __name__ == "__main__":
def getAspectCluster():
    # addLineNo()
    sentiment = getSentiment()
    # print(sentiment)
    text = []
    aspect_table_lineNo = {
        'chart': [],
        'dashboard': [],
        'helm': [],
        'docker': [],
        'database': [],
        'access': [],
        'export': [],
        'api': [],
        'user': [],
        'filter': [],
        'language': [],
        'param': [],
        'button': [],
        'url': [],
        'import': [],
        'page': [],
        'connect': [],
        'security': [],
        'date': []
    }
    aspect_table = {
        'chart': [],
        'dashboard': [],
        'helm': [],
        'docker': [],
        'database': [],
        'access': [],
        'export': [],
        'api': [],
        'user': [],
        'filter': [],
        'language': [],
        'param': [],
        'button': [],
        'url': [],
        'import': [],
        'page': [],
        'connect': [],
        'security': [],
        'date': []
    }
    with open('人工标注.txt', 'r', encoding='utf-8') as file:
        for index, line in enumerate(file, start=1):
            text.append(line)
        # print(text)
    with open('人工标注.txt', 'r', encoding='utf-8') as file:
        for index, line in enumerate(file, start=1):
            # 匹配符号"【"和"】"之间的任意字符，非贪婪模式
            pattern = r'【(.*?)】'
            matches = re.findall(pattern, line)
            for aspect in matches:
                aspect = aspect.lower()
                if any(substring in aspect for substring in ["view", "chart", "table", "graph", "image"]):
                    aspect_table_lineNo['chart'].append(index)
                    aspect_table['chart'].append(text[index - 1])
                if "dashboard" in aspect:
                    aspect_table_lineNo['dashboard'].append(index)
                    aspect_table['dashboard'].append(text[index - 1])
                if "helm" in aspect:
                    aspect_table_lineNo['helm'].append(index)
                    aspect_table['helm'].append(text[index - 1])
                if "docker" in aspect:
                    aspect_table_lineNo['docker'].append(index)
                    aspect_table['docker'].append(text[index - 1])
                if any(substring in aspect for substring in ["database", "db", "data", "clickhouse", "mysql"]):
                    aspect_table_lineNo['database'].append(index)
                    aspect_table['database'].append(text[index - 1])
                if any(substring in aspect for substring in ["access", "site", "permission", "login"]):
                    aspect_table_lineNo['access'].append(index)
                    aspect_table['access'].append(text[index - 1])
                if any(substring in aspect for substring in ["export", "send", "download", "save"]):
                    aspect_table_lineNo['export'].append(index)
                    aspect_table['export'].append(text[index - 1])
                if "api" in aspect:
                    aspect_table_lineNo['api'].append(index)
                    aspect_table['api'].append(text[index - 1])
                if any(substring in aspect for substring in ["user", "custom"]):
                    aspect_table_lineNo['user'].append(index)
                    aspect_table['user'].append(text[index - 1])
                if any(substring in aspect for substring in ["filter", "query", "select", "schema"]):
                    aspect_table_lineNo['filter'].append(index)
                    aspect_table['filter'].append(text[index - 1])
                if any(substring in aspect for substring in ["language", "translate"]):
                    aspect_table_lineNo['language'].append(index)
                    aspect_table['language'].append(text[index - 1])
                if "param" in aspect:
                    aspect_table_lineNo['param'].append(index)
                    aspect_table['param'].append(text[index - 1])
                if "button" in aspect:
                    aspect_table_lineNo['button'].append(index)
                    aspect_table['button'].append(text[index - 1])
                if "url" in aspect:
                    aspect_table_lineNo['url'].append(index)
                    aspect_table['url'].append(text[index - 1])
                if any(substring in aspect for substring in ["import", "install"]):
                    aspect_table_lineNo['import'].append(index)
                    aspect_table['import'].append(text[index - 1])
                if any(substring in aspect for substring in ["page", "ui"]):
                    aspect_table_lineNo['page'].append(index)
                    aspect_table['page'].append(text[index - 1])
                if "connect" in aspect:
                    aspect_table_lineNo['connect'].append(index)
                    aspect_table['connect'].append(text[index - 1])
                if any(substring in aspect for substring in ["security", "alert"]):
                    aspect_table_lineNo['security'].append(index)
                    aspect_table['security'].append(text[index - 1])
                if any(substring in aspect for substring in ["date", "time"]):
                    aspect_table_lineNo['date'].append(index)
                    aspect_table['date'].append(text[index - 1])
        lineNo_sentiment = {}
        json_objs = []
        senti_score = 0
        for key in aspect_table_lineNo:
            linNo_array = aspect_table_lineNo.get(key)
            for index in linNo_array:
                senti_score += int(sentiment[index - 1])
            context = aspect_table[key]
            # 'NumOfSentence': len(linNo_array), 'sentiment': round(senti_score / len(linNo_array), 1)
            # lineNo_sentiment[key] = {'value': [len(linNo_array), round(senti_score / len(linNo_array), 1)],
            #                          'context': context}
            json_obj = {"name": key,
                        "value": [len(linNo_array), round(senti_score / len(linNo_array), 1)],
                        "context": context
            }
            json_objs.append(json_obj)
        # json_objs = []
        # for key in lineNo_sentiment:
        #     json_obj = {"name": key}
        #     # 添加到JSON对象列表中
        #     json_objs.append(json_obj)

        json_str = json.dumps(json_objs)
        print(json_str)

        # for key, value in aspect_table_lineNo.items():
        #     print(key, ':', value)
        # print()
        # for key, value in aspect_table.items():
        #     print(key, ':', value)
        # print()
        # for key, value in lineNo_sentiment.items():
        #     print(key, ':', value)
        # 返回值格式：{ name: "aspect1",
        #           value:[长度，情绪值],
        #           context:["..","..."]
        #           }

        return json_objs
