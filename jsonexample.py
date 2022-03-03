import json
from pickle import FALSE
from unicodedata import name

import random


def test1():
    name="salonname"
    address="addressssss"
    url="url.com"

    dic={name:url}
    rate=5.0
    rate_dic={"rate":rate}
    address="adressssssss"
    address_dic={"address":address}
    detail_dic={name:[address_dic, rate_dic]}
    details=[]
    details.append(detail_dic)
    details.append({"name2":[address_dic, rate_dic]})

    #with open('data.json','w') as f:
    #    json.dump(details, f)
    for i in range(4):
        nameplus=name + str(i)
        with open("data.json",'a') as f:
            append_dic=({nameplus:[address_dic, rate_dic]})
            json.dump(append_dic,f)


def test1_5():
    with open("data.json","r") as f:
        dics=json.load(f)
        print(dics)

def test2():
    for i in range(5):
        name="name"+str(i)
        dic={"name":name}
        print(i)
        with open("data.json","r") as f:
            dic_list=json.load(f)
            dic_list.append(dic)
            print(dic_list.keys())
            print(dic_list)
            f.close()
        with open("data.json","w") as f:
            json.dumps(dic_list,f)
            f.close()


def test3():
    one=[1,2,3]
    name="name1"
    data={"key":[one,{"name":name}]}
    with open("data.json","w") as f:
        json.dump(data,f)


def load_saloninfo():
    open_time_list=["10:00am-5:00pm","09:00am-4:00pm","10:00am-6:00pm"]
    with open("salon_info.json","r") as f:
        salon_info_list = json.load(f)
        #salon_url = salon_info.keys()
        for salon_info in salon_info_list:
            info = list(salon_info.values())[0]
            print("info:",info)
            salon_name = info[0]["name"]
            salon_rate = info[1]["rate"]
            salon_address = info[2]["address"]
            salon_price = float(random.randint(150, 500)) / 10
            #salon_busy_base = random.randint(0,1)
            salon_busy = FALSE
            if 1 == random.randint(0,1):
                salon_busy=True
            salon_phone = "0000000" + str(random.randint(0,999))
            salon_time = open_time_list[random.randint(0,2)]
            
            print(salon_name, salon_rate, salon_address, salon_price, salon_busy, salon_phone, salon_time)
        f.close()

def load_details():
    with open("details.json","r") as f:
        salon_detail_list = json.load(f)
        salon_id = 2
        for salon_detail in salon_detail_list:
            detail = list(salon_detail.values())[0]
            
            #print(detail[2])
            #print(detail[0])
            for name in detail[0]:
                service_name = name[0]["name"]
                print(service_name)
                service_type = random.randint(0,4)
                service_price = float(random.randint(15, 150))
                service_rate = float(random.randint(0,50)) / 10
                #s = Service(salon_id=salon_id, service_name=service_name, service_price=service_price, service_rate=service_rate, service_type=service_type)
                #s.save()
            salon_id = salon_id + 1

def load_comments():
    with open("details.json","r") as f:
        salon_detail_list = json.load(f)
        salon_id = 2
        for salon_detail in salon_detail_list:
            detail = list(salon_detail.values())[0]
            comments = detail[2]['comment']
            for comment in comments:
                print(comment)
            #print(detail[2]["comment"])
load_comments()