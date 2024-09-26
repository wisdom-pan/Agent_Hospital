# coding: utf-8
import sparkai
import time
#以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35
appid = "b8b44f1e"     #填写控制台中获取的 APPID 信息
api_secret = "NjIxYWNjNjE5NWFmNjdjZDRjZGI2YTI4"   #填写控制台中获取的 APISecret 信息
api_key ="d0dfd8116a2e5031123a5ef8736dbdf9"    #填写控制台中获取的 APIKey 信息

domain = "4.0Ultra"      # Max版本
#domain = "generalv3"       # Pro版本
#domain = "general"         # Lite版本

Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat"   # Max服务地址
#Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
#Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址

#初始上下文内容，当前可传system、user、assistant 等角色
text =[
    # {"role": "system", "content": "你现在扮演李白，你豪情万丈，狂放不羁；接下来请用李白的口吻和用户对话。"} , # 设置对话背景或者模型角色
    # {"role": "user", "content": "你是谁"},  # 用户的历史问题
    # {"role": "assistant", "content": "....."} , # AI的历史回答结果
    # # ....... 省略的历史对话
    # {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
]


def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text



if __name__ == '__main__':

    while(1):
        Input = input("\n" +"我:")
        prompt = '''
        Hello, I need your expertise in Named Entity Recognition (NER) for medical abstracts with a 
focus on accurately identifying entities and their acronyms. Each identified entity should be 
classified into one of the following categories: Modifier, SpecificDisease, or DiseaseClass. 
For acronyms, please indicate the full term alongside the acronym and classify both consistently. 
Here are the categories defined:
1. Modifier: This category includes terms that modify or describe medical conditions but are 
not diseases themselves, such as symptoms or diagnostic procedures.
2. SpecificDisease: Use this category for names of specific diseases or medical conditions.
3. DiseaseClass: This category is for broader classes or types of diseases.
For example, 'CT' when first mentioned should be expanded to 'Copper Toxicosis' and classified as 
SpecificDisease if it is a specific condition being discussed or as a Modifier if it's modifying another term.
I am providing you with several examples of medical abstracts where specific entities have been identified 
and classified into categories: Modifier, SpecificDisease, or DiseaseClass. After reviewing these examples, 
you will process a new abstract in a similar manner.

Example 1:
Abstract: A common human skin tumour is caused by activating mutations in beta-catenin. WNT signalling orchestrates a number of developmental programs. In response to this stimulus, cytoplasmic beta-catenin (encoded by CTNNB1) is stabilized, enabling downstream transcriptional activation by members of the LEF/TCF family. One of the target genes for beta-catenin/TCF encodes c-MYC, explaining why constitutive activation of the WNT pathway can lead to cancer, particularly in the colon. Most colon cancers arise from mutations in the gene encoding adenomatous polyposis coli (APC), a protein required for ubiquitin-mediated degradation of beta-catenin, but a small percentage of colon and some other cancers harbour beta-catenin-stabilizing mutations. Recently, we discovered that transgenic mice expressing an activated beta-catenin are predisposed to developing skin tumours resembling pilomatricomas. Given that the skin of these adult mice also exhibits signs of de novo hair-follicle morphogenesis, we wondered whether human pilomatricomas might originate from hair matrix cells and whether they might possess beta-catenin-stabilizing mutations. Here, we explore the cell origin and aetiology of this common human skin tumour. We found nuclear LEF-1 in the dividing tumour cells, providing biochemical evidence that pilomatricomas are derived from hair matrix cells.
Identified Entities and Classes:
1. Skin tumour - DiseaseClass
2. Cancer - DiseaseClass
3. Colon cancers - DiseaseClass
4. Adenomatous polyposis coli (APC) - SpecificDisease
5. Skin tumours - DiseaseClass
6. Pilomatricomas - SpecificDisease
7. Tumour - Modifier
8. Tumours - DiseaseClass

Now, based on the structure and classification shown in the examples above, please analyze the following abstract and 
identify the entities with their correct classification:
Abstract: {{context}}

Your output should be in the form of a comma-separated list and should contain only the entity and category我想要按照我的sample修改一下prompt
        
        '''
        question = checklen(getText("user",prompt))
        sparkai.answer =""
        print("星火:",end ="")
        sparkai.main(appid,api_key,api_secret,Spark_url,domain,question)
        print(sparkai.answer)
        getText("assistant",sparkai.answer)




