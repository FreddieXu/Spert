import json
from collections import OrderedDict
import re

#读取json文件
baidu_train_path='data/train_data.json'
# 由于文件中有多行，直接读取会出现错误，因此一行一行读取
file = open(baidu_train_path, 'r', encoding='utf-8')
papers = []
for line in file.readlines():
    dic = json.loads(line)
    papers.append(dic)

#建立spert模式文本框架
spert_py=[]

for text_id in range(len(papers)):
    #读取文本
    text_load=papers[text_id]['text']
    #文本token化
    text_tokenizer=list(text_load)

    spert_py.append({"tokens":[],"entities":[],"relations":[],"orig_id":text_id})
    #插入文本的token化
    spert_py[text_id]['tokens']=list(papers[text_id]['text'])
    # print(spert_py)

    #读取spo
    spo_load=[]
    for i in range(len(papers[text_id]['spo_list'])):
        # print(papers[0]['spo_list'][i])
        spo_load.append(papers[text_id]['spo_list'][i])
    num_relation=len(spo_load)
    # print(spo_load[0]['predicate'])

    #
    entity2index=[]
    entity_start=[]
    entity_end=[]
    entity_type=[]
    #从每个spo里抽取信息
    for n in range(num_relation):
        # input_num=0
        subject_name = spo_load[n]['subject']
        #给特殊字符加上转义字符
        subject_name1 = subject_name.replace('\\', "\\\\")
        subject_name1=subject_name1.replace('(',"\(")
        subject_name1 = subject_name1.replace(')', "\)")
        subject_name1=subject_name1.replace('*',"\*")
        subject_name1 = subject_name1.replace(':', "\:")
        subject_name1 = subject_name1.replace('《',"\《")
        subject_name1 = subject_name1.replace('》', "\》")
        subject_name1 = subject_name1.replace('?',"\?")
        subject_name1 = subject_name1.replace('!','\!')
        subject_name1 = subject_name1.replace('+','\+')
        subject_name1 = subject_name1.replace('[','\[')
        subject_name1 = subject_name1.replace(']','\]')
        subject_name1 = subject_name1.replace('^','\^')



        object_name = spo_load[n]['object']['@value']
        object_name1 = object_name.replace("\\", "\\\\")
        object_name1 = object_name1.replace('(', "\(")
        object_name1 = object_name1.replace(')', "\)")
        object_name1=object_name1.replace("*","\*")
        object_name1=object_name1.replace(":","\:")
        object_name1 = object_name1.replace("《", "\《")
        object_name1 = object_name1.replace("》", "\》")
        object_name1 = object_name1.replace('?',"\?")
        object_name1 = object_name1.replace('!','\!')
        object_name1 = object_name1.replace('+','\+')
        object_name1 = object_name1.replace('[','\[')
        object_name1 = object_name1.replace(']','\]')
        object_name1 = object_name1.replace('^','\^')

        subject_type = spo_load[n]['subject_type']
        object_type = spo_load[n]['object_type']['@value']

        print(subject_name1)
        print(object_name1)
        # print(subject_name)
        subject_label=[re.search(subject_name1, text_load).span()]
        entity2index.append(subject_name)
        # input_num=input_num+1
        entity_start.append(subject_label[0][0])
        entity_end.append(subject_label[0][1])
        entity_type.append(subject_type)


        object_label=[re.search(object_name1, text_load).span()]
        entity2index.append(object_name)
        entity_start.append(object_label[0][0])
        entity_end.append(object_label[0][1])
        entity_type.append(object_type)
    #
    # print(len(entity2index),len(entity_start),len(entity_end),len(entity_type))
    # print(entity2index)
    # print(entity_start)
    # print(entity_end)
    # print(entity_type)

    #录入实体信息到spert_py[tedt_id]中
    for i in range(len(entity2index)):
        spert_py[text_id]['entities'].append({'type':entity_type[i],'start':entity_start[i],'end':entity_end[i]})
    for j in range(num_relation):
        head_input=spo_load[j]['subject']
        tail_input=spo_load[j]['object']['@value']
        head=entity2index.index(head_input)
        tail=entity2index.index(tail_input)
        spert_py[text_id]['relations'].append({'type': spo_load[j]['predicate'], 'head': head, 'tail': tail})


    #判断是否有异常
    if len(spert_py[text_id]['entities'])!=len(spo_load)*2:
        print(2)

print(spert_py[0])
print(len(spert_py))
print(len(papers))

filename='data/convert2spert/train.json'
with open(filename,'w',encoding='utf-8') as file_obj:
    json.dump(spert_py,file_obj,ensure_ascii=False, indent=4, separators=(',', ':'))