# -*- coding: utf-8 -*-
"""
 ***All Rights Reserved
 @author frankiezhu@foxmail.com
 @data 20140106
 ***
"""
###################################CONFIG START##################################

#账户信息
user='xxx@xx.com'
passwd='xxxxxx'

#想买的车次,为空的话会进入交互阶段，需要手动输入车次,建议设置上
g_buy_list = ["K827", "K587", "K841", "K1224", "K836"]

#忽略的车次
g_ingnore_list = ["L74"]


#买票查询条件：时间、站点, 车站代码可以在info目录station_code.txt里查
g_query_data = [
             ("leftTicketDTO.train_date", "2014-01-27"),
             ("leftTicketDTO.from_station", "GZQ"),
             ("leftTicketDTO.to_station", "LZZ"),
             ("purpose_codes", "ADULT"),
            ]
#乘客信息
g_passengers = [
                {
                "name": u"某某",
                "id": "123061230612306123",
                "tel": "12306123060",
                },               
            ]

'''
g_str_seat_types = {
                    u"高级软卧":"gr_num",
                    u"软卧":"rw_num",
                    u"软座":"rz_num",
                    u"特等座":"tz_num",
                    u"无座":"wz_num",
                    u"硬卧":"yw_num",
                    u"硬座": "yz_num",
                    u"二等座":"ze_num",
                    u"一等座":"zy_num",
                    u"商务座":"swz_num",
            }
'''
#座位类型,类型名在g_str_seat_types里有对应
g_care_seat_types = ["rw_num", "yw_num"]

#自动识别验证码次数，验证码无重叠无背景时候识别率高，基于tesseract的OCR
#目前仅仅遇到过一次，几个小时，dns更新后连接到的服务器有背景干扰
#可以找到这种服务器并修改host让其一直连接此服务器
#或者做更多的图像相关处理，去除噪点再做OCR
g_max_auto_times = 0

#刷新间隔
g_query_sleep_time = 1

###################################End##################################


