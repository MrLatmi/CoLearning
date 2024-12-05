import json
BOT_TOKEN = "7572062143:AAH0lHM7jc_GpeRx3LdL_tL-HQ123now9gc"
ADMINS = "5358543785"

difficult_levels = 6

def get_subtopic(topic):
    with open('base.json', encoding="utf-8") as f:
        data = json.load(f)
    return data['topics'][f'{topic}']


def get_topic():
    with open('base.json', encoding="utf-8") as f:
        data = json.load(f)
    return data['topics']

def add_task(main_topic,subtopic, task_name, answer, solution, source, path):
    with open('base.json', encoding="utf-8") as f:
        data = json.load(f)
    data['topics'][f'{main_topic}'][f'{subtopic}'][f'{task_name}'] = [answer, solution, source, path]
    with open('base.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_subtopic(main_topic,subtopic):
    with open('base.json', encoding="utf-8") as f:
        data = json.load(f)
    data['topics'][f'{main_topic}'][f'{subtopic}'] = {}
    with open('base.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_subtopic_without_main_topic(subtopic):
    with open('base.json', encoding="utf-8") as f:
        data = json.load(f)
    data['subtopics'].append(subtopic)
    with open('base.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def add_topic(topic):
    with open('base.json', encoding="utf-8") as f:
        data = json.load(f)
    data['topics'][f'{topic}'] = {"Разное":{}}
    with open('base.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

