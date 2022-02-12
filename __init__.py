# -*- coding:utf-8 -*-
"""2022 冬奥会"""
from botoy import GroupMsg, FriendMsg, Picture, Text, Picture
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, startswith
from botoy.parser import group as gp# 群消息(GroupMsg)相关解析
from botoy.parser import friend as fp # 好友消息(FriendMsg)相关解析
from botoy import jconfig, logger

from PIL import Image,ImageFont,ImageDraw
import os
from PIL import Image,ImageFont,ImageDraw
import pandas as pd



import datetime
import time
import demjson,httpx

# 获取赛事日程
def get_Winter_Olympics_schedule(date_text):
    result = ""  # 最终返回文本
    Winter_Olympics_schedule_name = './plugins/bot_2022_Winter_Olympics/2022_Winter_Olympics.json'  # json文件路径

    # 读取数据
    with open(Winter_Olympics_schedule_name, 'r', encoding='utf-8') as fo:
        schedule_Data = demjson.decode(fo.read())
        fo.close()
        if schedule_Data[0][date_text]:
            dateID = schedule_Data[0][date_text][0]
            schedule_text=dateID
            schedule_date_text=schedule_text['date']  # date_text为冬奥会第几天
            schedule_date_tody=schedule_text['today']  # date_text为星期几

            result = date_text+" " + schedule_date_tody +"\n"
            for i in range(len(schedule_Data)-2):  # 排除掉第一个日期json
                if schedule_Data[i+1][schedule_date_text] != "":
                    result = result + schedule_Data[i+1][""]+":\n"+ schedule_Data[i+1][schedule_date_text]+"\n\n"
                    
            im = Image.new("RGB", (700, result.count('\n')*24), (255, 255, 255))
            # 设置所使用的字体
            date_font = ImageFont.truetype("./plugins/bot_2022_Winter_Olympics/font/DroidSansFallback.ttf", 17)  # 日期字体：方正粗圆宋简体，19
        
            # 画图
            dr = ImageDraw.Draw(im)
            dr.text((10, 10), result, (7, 51, 113), font=date_font)  # 年 设置日期文字位置/内容/颜色/字体
            dr = ImageDraw.Draw(im)  # Just draw it!
            
            #输出
            today = time.strftime("%d", time.localtime())
            im.save(r'./plugins/bot_2022_Winter_Olympics/output'+today+'.png')
            return result
        else:
            return "获取失败"
            
# 获取奖牌榜
def get_Winter_Olympics_medal():
    url = "https://app.sports.qq.com/m/oly/medalsRank?seasonID=2022&callback=jQuery19006330078021719667_1644122210304&_=1644122210305"
    try:
        res = httpx.get(url).json()
    except Exception as e:
        logger.warning(f"冬奥会奖牌榜请求失败\r\n {e}")
        return
    # logger.success(f"冬奥会奖牌: {res}")
    return res

# 获取emoji国旗
def get_emoji(text):
    text_1=text.replace("俄罗斯奥委会", "俄罗斯")
    CountryCodeFileName='./plugins/bot_2022_Winter_Olympics/CountryCode.json'
    emojiFileName='./plugins/bot_2022_Winter_Olympics/emoji.json'
    if not os.path.isfile(CountryCodeFileName):
        return""
    fo = open(CountryCodeFileName, "r")
    CountryCode_Data = demjson.decode(fo.read())
    fo.close()
    for i in range(len(CountryCode_Data)):
        try:
            if CountryCode_Data[i]["name"] == text_1:
                CountryCode_text=CountryCode_Data[i]["abbreviate"]
                if not os.path.isfile(emojiFileName):
                    return"❤️"
                fo2 = open(emojiFileName, "r")
                emoji_Data = demjson.decode(fo2.read())
                fo2.close()
                for i in range(len(emoji_Data)):
                    try:
                        if emoji_Data[i][1] == CountryCode_text:
                                return emoji_Data[i][0]
                    except Exception as e:
                        return "❤️"
        except Exception as e:
            return "❤️"

def checkUser():#判断是否今天获取过
    today = time.strftime("%d", time.localtime())
    cacheFileName = './plugins/bot_2022_Winter_Olympics/output'+today+'.png'
    if not os.path.isfile(cacheFileName):
        execute()
        return True
    return False
    
def execute():#删除旧记录
    filePath = '/root/opqbot/client/botoy/plugins/bot_2022_Winter_Olympics/'
    name = os.listdir(filePath)
    for i in name:
        path = '/root/opqbot/client/botoy/plugins/bot_2022_Winter_Olympics/{}'.format(i)
        print(path)
        if 'output' in i:
            os.remove(path)

@ignore_botself#忽略机器人自身的消息
def receive_group_msg(ctx: GroupMsg):
    if (ctx.Content == "冬奥会日程表"):
        today = time.strftime("%d", time.localtime())
        if checkUser():
            get_Winter_Olympics_schedule(time.strftime("%m/%d"))
        cacheFileName = './plugins/bot_2022_Winter_Olympics/output'+today+'.png'
        Picture(pic_path=cacheFileName)
    elif ctx.Content == "冬奥会奖牌榜" or ctx.Content == "奖牌榜":
        medal_data=get_Winter_Olympics_medal()
        medal_text="〖NO.1〗"+get_emoji(medal_data["data"]["list"][0]["nocName"])+medal_data["data"]["list"][0]["nocName"]+" 共: "+medal_data["data"]["list"][0]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][0]["gold"]+"  🥈 "+medal_data["data"]["list"][0]["silver"]+"  🏅 "+medal_data["data"]["list"][0]["bronze"]+"\n"+"〖NO.2〗"+get_emoji(medal_data["data"]["list"][1]["nocName"])+medal_data["data"]["list"][1]["nocName"]+" 共: "+medal_data["data"]["list"][1]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][1]["gold"]+"  🥈 "+medal_data["data"]["list"][1]["silver"]+"  🏅 "+medal_data["data"]["list"][1]["bronze"]+"\n"+"〖NO.3〗"+get_emoji(medal_data["data"]["list"][2]["nocName"])+medal_data["data"]["list"][2]["nocName"]+" 共: "+medal_data["data"]["list"][2]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][2]["gold"]+"  🥈 "+medal_data["data"]["list"][2]["silver"]+"  🏅 "+medal_data["data"]["list"][2]["bronze"]+"\n"+"〖NO.4〗"+get_emoji(medal_data["data"]["list"][3]["nocName"])+medal_data["data"]["list"][3]["nocName"]+" 共: "+medal_data["data"]["list"][3]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][3]["gold"]+"  🥈 "+medal_data["data"]["list"][3]["silver"]+"  🏅 "+medal_data["data"]["list"][3]["bronze"]+"\n"+"〖NO.5〗"+get_emoji(medal_data["data"]["list"][4]["nocName"])+medal_data["data"]["list"][4]["nocName"]+" 共: "+medal_data["data"]["list"][4]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][4]["gold"]+"  🥈 "+medal_data["data"]["list"][4]["silver"]+"  🏅 "+medal_data["data"]["list"][4]["bronze"]
        Text(medal_text)

@ignore_botself#忽略机器人自身的消息
def receive_friend_msg(ctx: FriendMsg):
    if (ctx.Content == "冬奥会日程表"):
        today = time.strftime("%d", time.localtime())
        if checkUser():
            get_Winter_Olympics_schedule(time.strftime("%m/%d"))
        cacheFileName = './plugins/bot_2022_Winter_Olympics/output'+today+'.png'
        Picture(pic_path=cacheFileName)
    elif ctx.Content == "冬奥会奖牌榜" or ctx.Content == "奖牌榜":
        medal_data=get_Winter_Olympics_medal()
        medal_text="〖NO.1〗"+get_emoji(medal_data["data"]["list"][0]["nocName"])+medal_data["data"]["list"][0]["nocName"]+" 共: "+medal_data["data"]["list"][0]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][0]["gold"]+"  🥈 "+medal_data["data"]["list"][0]["silver"]+"  🏅 "+medal_data["data"]["list"][0]["bronze"]+"\n"+"〖NO.2〗"+get_emoji(medal_data["data"]["list"][1]["nocName"])+medal_data["data"]["list"][1]["nocName"]+" 共: "+medal_data["data"]["list"][1]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][1]["gold"]+"  🥈 "+medal_data["data"]["list"][1]["silver"]+"  🏅 "+medal_data["data"]["list"][1]["bronze"]+"\n"+"〖NO.3〗"+get_emoji(medal_data["data"]["list"][2]["nocName"])+medal_data["data"]["list"][2]["nocName"]+" 共: "+medal_data["data"]["list"][2]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][2]["gold"]+"  🥈 "+medal_data["data"]["list"][2]["silver"]+"  🏅 "+medal_data["data"]["list"][2]["bronze"]+"\n"+"〖NO.4〗"+get_emoji(medal_data["data"]["list"][3]["nocName"])+medal_data["data"]["list"][3]["nocName"]+" 共: "+medal_data["data"]["list"][3]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][3]["gold"]+"  🥈 "+medal_data["data"]["list"][3]["silver"]+"  🏅 "+medal_data["data"]["list"][3]["bronze"]+"\n"+"〖NO.5〗"+get_emoji(medal_data["data"]["list"][4]["nocName"])+medal_data["data"]["list"][4]["nocName"]+" 共: "+medal_data["data"]["list"][4]["total"]+" 枚\n🥇 "+medal_data["data"]["list"][4]["gold"]+"  🥈 "+medal_data["data"]["list"][4]["silver"]+"  🏅 "+medal_data["data"]["list"][4]["bronze"]
        Text(medal_text)
