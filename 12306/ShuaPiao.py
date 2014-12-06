# -*- coding: utf-8 -*-
#coding:utf-8
"""
 ***All Rights Reserved
 run env: python 2.7
 @author frankiezhu
 @data 20140106
 ***
"""

import urllib, sys, os, time, json
import httplib
import StringIO, gzip
import traceback
import logging
import datetime
import cProfile
import subprocess

#加载你的配置文件名
#from conf_frankie_test import *
from conf_neil import *

#清理临时文件，如验证码等
g_clean_temp = False

##########################internal###############################

g_str_train_types = {
                    "G": u"高铁",
                    "L": u"临客",
                    "D": u"动车",
                    "Z": u"直达",
                    "T": u"特快",
                    "K": u"快速",
                    }
#g_seat_code
g_seat_code_dict =  {
            "yz_num":"1",
            "rz_num":"2",
            "yw_num":"3",
            "rw_num":"4",
            "gr_num":"6",
            "tz_num":"P",
            "wz_num":"WZ",
            "ze_num":"O",
            "zy_num":"M",
            "swz_num":"9",
            }



logger = logging.getLogger('shuapiao')
g_conn = httplib.HTTPConnection('kyfw.12306.cn', timeout=100)

#restart conn
def restart_conn(conn):
    print "restart connection"
    conn.close()
    conn = httplib.HTTPConnection('kyfw.12306.cn', timeout=100)
    conn.connect()

#装饰器
def retries(max_tries):
    def dec(func, conn=g_conn):
        def f2(*args, **kwargs):
            tries = range(max_tries)
            tries.reverse()
            for tries_remaining in tries:
                try:
                   return func(*args, **kwargs)
                except httplib.HTTPException as e:
                    print "conneciont error"
                    restart_conn(conn)        
                except Exception as e:
                    if tries_remaining > 0:
                        traceback.print_exc()
                        logger.error("errror %d" % tries_remaining)
                        logger.error(traceback.format_exc())
                    else:
                        raise e
                else:
                    break
        return f2
    return dec

#调用OCR
def call_tesseract(in_file):
    tesseract_exe_name = 'tesseract'
    expect_len = 4
    out_file = "o"
    
    args = [tesseract_exe_name, in_file, out_file]
    proc = subprocess.Popen(args)
    ret = proc.wait()
    if ret != 0:
        print "call tesseract failed:%d" % ret
        return ''
    out_full = out_file + '.txt'
    f = open(out_full)
    text = f.read()
    f.close()
    if g_clean_temp:
        os.remove(out_full)
    text = text.rstrip('\r\n')
    text = text.replace(" ", "")
    print "auto read rand_code:%s" % text
    if len(text) != expect_len:
        print "auto read faild:%s, %d" % (text, len(text))
        return ''
    return text

'''
    HttpAuto
'''
class HttpAuto:
    def __init__(self):

        self.ext_header = {
            "Accept":"*/*",
            "X-Requested-With":"XMLHttpRequest",
            "Referer": "http://kyfw.12306.cn/otn/login/init#",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate",
            "Connection":"Keep-Alive",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        self.proxy_ext_header = {
            "Accept": "*/*",
            "X-Requested-With":"XMLHttpRequest",
            "Referer": "http://kyfw.12306.cn/otn/login/init#",
            "Accept-Language": "zh-cn",
            "Accept-Encoding": "gzip, deflate",
            "Proxy-Connection": "Keep-Alive",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        #cockies
        self.sid = ''
        self.sip = ''

        #passenger info to be POST
        self.passengerTicketStr = ''
        self.oldPassengerStr = ''

        #used to POST 
        self.globalRepeatSubmitToken = ''
        self.key_check_isChange = ''
        self.orderId = ''
        
        self.pass_code = 'abcd'
        self.rand_code = 'abcd'
        
        return

    def construct_passengerTicketStr(self):
        print "###construct_passengerTicketStr###"
        str1 = ''
        str2 = ''
        for p in g_passengers:
            str1 = str1 + '1,0,1,' + p['name'] + ',1,' + p['id'] + ','+ p['tel']+ ',N_'
            str2 = str2 +  p['name'] + ',1,' + p['id'] + ',1_'
        str1 = str1[:-1]
        self.passengerTicketStr = str1.encode('utf8')
        self.oldPassengerStr = str2.encode('utf8')
        print "new:%s" % self.passengerTicketStr
        print "old:%s" % self.oldPassengerStr

    def logout(self):
        url_logout = "http://kyfw.12306.cn/otn/login/loginOut"
        g_conn.request('540', url_logout, headers=self.proxy_ext_header)
        return True
                
    def __del__(self):
        self.logout()
        print "close connnection"
        g_conn.close()
        return

    def update_session_info(self, res):
        print "process header cookie"
        update = False
        for h in res.getheaders():
            if h[0] == "set-cookie":
                l = h[1].split(',')[0].strip()
                if l.startswith('JSESSIONID'):
                    self.sid = l.split(';')[0].strip()
                    update = True
                    print "Update sessionid "+self.sid
                if l.startswith('BIGipServerotn'):
                    self.sip = l.split(';')[0].strip()
                    update = True
                    print "Update sip:"+self.sip
                l = h[1].split(',')[1].strip()
                if l.startswith('BIGipServerotn'):
                    self.sip = l.split(';')[0].strip()
                    update = True
                    print "Update sip:"+self.sip
        return update

    def check_pass_code_common(self, module, rand_method):
        ret = False
        auto_times = g_max_auto_times
        while 1:
            url_pass_code = "http://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=%s&rand=%s" % (module, rand_method)
            print "send getPassCodeNew:%s" % datetime.datetime.now()
            header = ''
            if module == 'login':
                header = self.ext_header
            else:
                header = self.proxy_ext_header

            g_conn.request('GET', url_pass_code, headers=header)
            res = g_conn.getresponse()
            print "recv getPassCodeNew=====>:%s" % datetime.datetime.now()
            if module == 'login':
                self.update_session_info(res)
                self.ext_header["Cookie"] = self.sid+';'+self.sip
            
            #save file  
            pic_type = res.getheader('Content-Type').split(';')[0].split('/')[1]
            data = res.read()
            file_name = "./pass_code.%s" % pic_type
            f = open(file_name, 'wb')
            f.write(data)
            f.close()

            #auto read or manual
            read_pass_code = ''
            if g_max_auto_times > 0:
                auto_times = auto_times - 1
                read_pass_code = call_tesseract(file_name)

            if  read_pass_code == '':
                read_pass_code = raw_input("input passcode(%s):" % file_name)
                if read_pass_code == "no":
                    print "Get A new PassCode"
                    continue
                elif read_pass_code == "quit":
                    print "Quit"
                    break
                print "input:%s" % read_pass_code
            else:
                print "auto:%s" % read_pass_code

            if g_clean_temp:
                os.remove(file_name)

            data = []
            if module == 'passenger':
                self.proxy_ext_header["Referer"] = "http://kyfw.12306.cn/otn/confirmPassenger/initDc#nogo"
                self.rand_code = read_pass_code
                data = [
                        ("_json_att", ''),
                        ("rand", rand_method),
                        ("randCode", read_pass_code),
                        ("REPEAT_SUBMIT_TOKEN", self.globalRepeatSubmitToken),
                       ]
            elif module == 'login':
                self.pass_code = read_pass_code
                data = [
                        ("randCode", read_pass_code),
                        ("rand", rand_method)
                       ]
            else:
                pass

            post_data = urllib.urlencode(data)
            print "send checkRandCodeAnsyn=====>:" #% post_data
            
            url_check_rand = "http://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn"
            g_conn.request('POST', url_check_rand, body=post_data, headers=header)
            res = g_conn.getresponse()
            data = res.read()
            print "recv checkRandCodeAnsyn"
            resp = json.loads(data)
            if resp['data'] != 'Y':
                print "status error:%s" % resp['data']
                continue
            else:
                ret = True
                break
        return ret
        
    @retries(3)
    def check_pass_code(self):
        print "#############################Step1:Passcode#########"
        module = 'login'
        rand_method = 'sjrand'
        return self.check_pass_code_common(module, rand_method)

    @retries(3)
    def check_rand_code(self):
        print "#############################Step8:Randcode#########"
        ret = False
        module = 'passenger'
        rand_method = 'randp'
        return self.check_pass_code_common(module, rand_method)
    
    @retries(3)   
    def loginAysnSuggest(self):
        if not self.check_pass_code():
            return False
        print "#############################Step2:Login#########"
        url_login = "http://kyfw.12306.cn/otn/login/loginAysnSuggest"
        data = [
                ("loginUserDTO.user_name", user),
                ("userDTO.password", passwd),
                ("randCode", self.pass_code)
               ]
        post_data = urllib.urlencode(data)
        #post_data="loginUserDTO.user_name=frankiezhu%%40foxmail.com&userDTO.password=sky123&randCode=%s" % self.pass_code
        self.proxy_ext_header["Cookie"] = self.sid+';'+self.sip 
        print "send loginAysnSuggest=====>"  #% post_data
        g_conn.request('POST', url_login, body=post_data, headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        print "recv loginAysnSuggest"
        data = res.read()
        res_json = json.loads(data)
        if res_json['status'] != True or not res_json['data'].has_key('loginCheck'):
            print u"return error:%s" % ' '.join(res_json['messages'])
            return False
        if res_json['data']['loginCheck'] == 'Y':
            print u"login success"
            return True  
        else:
            print u"login error %s" % res_json['data']['loginCheck']
            return False
        
    def show_ticket(self, it):
         print it['station_train_code'], it['from_station_name'],it['to_station_name'],it['start_time'], it['arrive_time'],it['lishi'],  \
              it['swz_num'],it['tz_num'], it['zy_num'],it['ze_num'],it['gr_num'], it['rw_num'],it['yw_num'],it['rz_num'],it['wz_num'],it['canWebBuy']
         return

    ############
    #retcode: -2 for retry, -1 for error, 0 for success
    ############
    def do_ticket(self, json_data, result, want_special):
        ret = 0
        for item in json_data['data']:
            if item['queryLeftNewDTO']['canWebBuy'] == 'N':
                continue  
            train_code = item['queryLeftNewDTO']['station_train_code']
            if want_special and not train_code in g_buy_list:
                continue
            if train_code in g_ingnore_list:
                continue
            has_ticket = False
            for care_type in g_care_seat_types:
                if item['queryLeftNewDTO'][care_type] != "--"  and item['queryLeftNewDTO'][care_type] != u"无":
                    has_ticket = True
                    break
            if has_ticket:
                result[train_code] = item
        #query return none, retry
        if not len(result):
            return -2
        
        #as the list prority
        if want_special:
             for train_code in g_buy_list:
                if not result.has_key(train_code):
                    continue
                ret = self.buy(result[train_code])
                if not ret:
                    print "Err during buy"
                    return -1
                else:
                    return 0
        #show all
        for train_code, item in result.items():
            self.show_ticket(item['queryLeftNewDTO'])
        
        #get promote
        cmd = raw_input("input cmd[r|q|K101]:")
        cmd = cmd.strip()
        print "input:%s" % cmd
        if cmd == "r":
            print "retry"
            return -2
        elif cmd == "q":
            print "quit"
            return 0
        else:
            print "buy ticket:%s" % cmd
            ret = self.buy(result[cmd])
            if not ret:
                print "Err during buy"
                return -1
            else:
                return 0
    
    @retries(3)           
    def query(self):
        print "#############################Step3:Query#########"
        self.proxy_ext_header["Referer"] = "http://kyfw.12306.cn/otn/leftTicket/init"
        url_query = "http://kyfw.12306.cn/otn/leftTicket/query?" + urllib.urlencode(g_query_data)
        print "start query======>%s" % url_query
        want_special = False
        
        if len(g_buy_list) != 0:
            want_special = True
            print "JUST For:%s" % (','.join(g_buy_list))
        else:
            print u"车次 出发->到达 时间:到达 历时 商务座 特等座 一等座 二等座 高级软卧 软卧 硬卧 软座 硬座 无座 其他备注"
        #"http://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2014-01-04&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=NJH&purpose_codes=ADULT"
        q_cnt = 0
        while 1:
            q_cnt = q_cnt + 1
            g_conn.request('GET', url_query, headers=self.proxy_ext_header)
            res = g_conn.getresponse()
            data = ''
            if res.getheader('Content-Encoding') == 'gzip':
                tmp = StringIO.StringIO(res.read())
                gzipper = gzip.GzipFile(fileobj=tmp)
                data = gzipper.read()
            else:
                data = res.read()
            res_json = json.loads(data)
            if res_json['status'] != True:
                print "parse json failed! data %s" % data
                continue
            result = {}
            ret = self.do_ticket(res_json, result, want_special)
            if ret == 0:
                break
            elif ret == -2:
                print u"no ticket, refresh %d times!" % q_cnt
                time.sleep(g_query_sleep_time)
                continue

        return True

    @retries(3)
    def confirmPassenger_get_token(self):
        print "#############################Step6:confirmPassenger_get_token #########"
        url_confirm_passenger = "http://kyfw.12306.cn/otn/confirmPassenger/initDc"
        g_conn.request('GET', url_confirm_passenger, headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        data = res.read()
        
        if res.getheader('Content-Encoding') == 'gzip':
            tmp = StringIO.StringIO(data)
            gzipper = gzip.GzipFile(fileobj=tmp)
            data = gzipper.readlines()
            
        key_word = "globalRepeatSubmitToken"
        key_find = False
        line_token = ''
        line_request_info = ''
        for line in data:
            if line.startswith(u' var globalRepeatSubmitToken = '.encode("utf8")):
                line_token = line.decode("utf8")
                continue
            elif line.startswith(u'           var ticketInfoForPassengerForm'.encode("utf8")):
                line_request_info = line.decode("utf8")
                key_find = True
                break
        if key_find:
            self.globalRepeatSubmitToken = line_token.split('=')[1].strip()[1:-2]
            print "Update globalRepeatSubmitToken=%s" % self.globalRepeatSubmitToken
            req_data = line_request_info.split('=')[1].strip()[:-1]
            req_data = req_data.replace("null", "''")
            req_data = req_data.replace("true", "True")
            req_data = req_data.replace("false", "False")
            print "line_request_info"
            req_json = eval(req_data)
            self.key_check_isChange = req_json['key_check_isChange']
            self.leftTicketStr = req_json['leftTicketStr']
            print "Update key_check_isChange=%s" % self.key_check_isChange
            return True
        else:
            print "globalRepeatSubmitToken not found"
            return False
    
    @retries(3)
    def getQueueCount(self, item):
        print "#############################Step:getQueueCount #########"
        url_queue_count = "http://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
        #buy_date = 'Sun Jan 5 00:00:00 UTC+0800 2014'
        tlist = time.ctime().split()
        tlist[3] = '00:00:00'
        tlist.insert(4, 'UTC+0800')
        buy_date  = ' '.join(tlist)
        
        for t_type in g_care_seat_types:
            if item['queryLeftNewDTO'][t_type] != "--"  and item['queryLeftNewDTO'][t_type] != u"无":
                  break
        s_type = g_seat_code_dict[t_type]
         
        data = [
            ("train_date", buy_date),
            ("train_no", item['queryLeftNewDTO']['train_no']),
            ("stationTrainCode",item['queryLeftNewDTO']['station_train_code']),
            ("seatType", s_type),
            ("fromStationTelecode", item['queryLeftNewDTO']['from_station_telecode']),
            ("toStationTelecode", item['queryLeftNewDTO']['to_station_telecode']),
            ("leftTicket",item['queryLeftNewDTO']['yp_info']),
            ("purpose_codes", "00"),
            ("_json_att", ''),
            ("REPEAT_SUBMIT_TOKEN", self.globalRepeatSubmitToken),
            ]
        post_data = urllib.urlencode(data)
        print "send getQueueCount=====>"  #% post_data
        g_conn.request('POST', url_queue_count, body=post_data, headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        data = res.read()
        res_json = json.loads(data)
        print "recv getQueueCount:%s" % res_json
        if res_json['status'] != True:
            print "getQueueCount error :%s" % res_json
            return False
        return True

    @retries(3)
    def checkOrderInfo(self):
        print "#############################Step9:checkOrderInfo #########"
        url_check_order = "http://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        data = [
            ("cancel_flag", "2"),
            ("bed_level_order_num", "000000000000000000000000000000"),
            ("passengerTicketStr", self.passengerTicketStr),
            ("oldPassengerStr", self.oldPassengerStr),
            ("tour_flag","dc"),
            ("randCode",self.rand_code),
            ("_json_att", ''),
            ("REPEAT_SUBMIT_TOKEN", self.globalRepeatSubmitToken),
            ]
        post_data = urllib.urlencode(data)
        print "send checkOrderInfo=====>"
        #print "cancel_flag=2&bed_level_order_num=000000000000000000000000000000&passengerTicketStr=1%2C0%2C1%2C%E6%9C%B1%E5%AD%94%E6%B4%8B%2C1%2C320721198711180812%2C13430680458%2CN&oldPassengerStr=%E6%9C%B1%E5%AD%94%E6%B4%8B%2C1%2C320721198711180812%2C1_&tour_flag=dc&randCode=ewgw&_json_att=&REPEAT_SUBMIT_TOKEN=ad51ea02d933faf91d3d2eaeb5d85b3e"
        g_conn.request('POST', url_check_order, body=post_data, headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        data = res.read()
        res_json = json.loads(data)
        print "recv checkOrderInfo:%s" % res_json
        if res_json['status'] != True or res_json['data']['submitStatus'] != True:
            print "checkOrderInfo error :%s" % res_json['data']['errMsg']
            return False
        return True
    
    @retries(3)
    def checkUser(self):
        print "#############################Step4:checkUser #########"
        url_check_info = "http://kyfw.12306.cn/otn/login/checkUser"
        data = [
                ('_json_att', ''),
                ]
        post_data = urllib.urlencode(data)
        print post_data
        print "send checkUser=====>"  #% post_data
        g_conn.request('POST', url_check_info, body=post_data, headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        data = res.read()
        res_json = json.loads(data)
        print "recv checkUser"
        if not res_json['data'].has_key('flag') or res_json['data']['flag'] != True:
            print "check user failed, %s" % res_json
            return False
        else:
            return True
    
    @retries(3)
    def submitOrderRequest(self, item):
        print "#############################Step5:submitOrderRequest #########"
        url_submit = "http://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
        post_data = "secretStr=" + item['secretStr']+"&train_date=" \
                    + item['queryLeftNewDTO']['start_train_date'] \
                    + "&back_train_date=" + item['queryLeftNewDTO']['start_train_date'] \
                    + "&tour_flag=dc&purpose_codes=ADULT&query_from_station_name=" \
                    + item['queryLeftNewDTO']['from_station_name'] \
                    + "&query_to_station_name="+item['queryLeftNewDTO']['to_station_name']\
                    + "&undefined"
        print post_data
        print "send submitOrderRequest=====>"  #% post_data
        g_conn.request('POST', url_submit, body=post_data.encode("utf8"), headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        data = res.read()
        res_json = json.loads(data)
        if res_json['status'] != True:
            print u"submit order failed"
            print data
            print ''.join(res_json['messages']).encode('gb2312')
            return False
        else:
            return True
    
    @retries(3)
    def confirmSingleForQueue(self):
        print "#############################Step11:confirmSingleForQueue #########"
        url_check_info = "http://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        data = [
                ('passengerTicketStr', self.passengerTicketStr),
                ("oldPassengerStr", self.oldPassengerStr),
                ('randCode', self.rand_code),
                ('purpose_codes', "00"),
                ('key_check_isChange', self.key_check_isChange),
                ('leftTicketStr', self.leftTicketStr),
                ('train_location', 'H2'),
                ('_json_att', ''),
                ("REPEAT_SUBMIT_TOKEN", self.globalRepeatSubmitToken),
                ]
        post_data = urllib.urlencode(data)
        print "send confirmSingleForQueue=====>"  #% post_data
        g_conn.request('POST', url_check_info, body=post_data, headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        data = res.read()
        res_json = json.loads(data)
        print "recv confirmSingleForQueue"
        if not res_json['data'].has_key('submitStatus') or res_json['data']['submitStatus'] != True:
            print u"confirmSingleForQueue failed, %s" % res_json
            return False
        else:
            return True
    
    @retries(5)    
    def queryOrderWaitTime(self):
        print "#############################Step12:queryOrderWaitTime #########"
        url_query_wait = "http://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?"
        cnt = 0
        while 1: 
            data = [
                    ('random', int(time.time())),
                    ("tourFlag", "dc"),
                    ('_json_att', ''),
                    ("REPEAT_SUBMIT_TOKEN", self.globalRepeatSubmitToken),                       
                    ]
            url_query_wait = url_query_wait + urllib.urlencode(data)
            print "send queryOrderWaitTime:%d=====>" % cnt #% url
            g_conn.request('GET', url_query_wait, headers=self.proxy_ext_header)
            res = g_conn.getresponse()
            data = res.read()
            res_json = json.loads(data)
            print "recv queryOrderWaitTime:%s" % res_json
            cnt = cnt + 1
            if not res_json['data'].has_key('data') or res_json['data']['queryOrderWaitTimeStatus'] != True:
                print "queryOrderWaitTime error"
                print  res_json['messages']
                break
            if res_json['data']['waitCount']  == 0:
                self.orderId = res_json['data']['orderId']
                print "Update orderId:%s" % self.orderId
                break
            else:
                continue
        return True

    @retries(3)
    def resultOrderForDcQueue(self):
        print "#############################Step13:resultOrderForDcQueue #########"
        url_result = "http://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
        data = [
                ('orderSequence_no', self.orderId),
                ('_json_att', ''),
                ("REPEAT_SUBMIT_TOKEN", self.globalRepeatSubmitToken),                       
                ]
        post_data = urllib.urlencode(data)
        print "send resultOrderForDcQueue=====>" #% url
        g_conn.request('POST', url_result, body=post_data, headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        data = res.read()
        res_json = json.loads(data)
        print "recv queryOrderWaitTime"
        if not res_json['data'].has_key('submitStatus') or res_json['data']['submitStatus'] != True:
            print "submit error"
            print  data
            return False
        else:
            print "#############################Success check ticket in webbrowser #########"
            return True

    @retries(3)
    def get_passenger_info(self):
        print "#############################Step7:getPassengerDTOs #########"
        url_get_passager_info = "http://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
        data = [
                ('_json_att', ''),
                ('REPEAT_SUBMIT_TOKEN', self.globalRepeatSubmitToken)
                ]
        post_data = urllib.urlencode(data)
        print "send getPassengerDTOs=====>"  #% post_data
        g_conn.request('POST', url_get_passager_info, body=post_data, headers=self.proxy_ext_header)
        res = g_conn.getresponse()
        data = res.read()
        res_json = json.loads(data)
        print "recv getPassengerDTOs"
        return True
        
    def buy(self, item):
        #Step4
        if not self.checkUser():
            return False
        #Step5
        if not self.submitOrderRequest(item):
            return False
        #Step6
        if not self.confirmPassenger_get_token():
            return False
        self.proxy_ext_header["Referer"] = "http://kyfw.12306.cn/otn/confirmPassenger/initDc#nogo"
        #Step7
            #self.get_passenger_info
        #Step8
        if not self.check_rand_code():
            return False
        #Step9
        if not self.checkOrderInfo():
            return False
        #Step10
        if not self.getQueueCount(item):
            return False
        #Step11
        if not self.confirmSingleForQueue():
            return False
        if not self.queryOrderWaitTime():
            return False
        #Step13
        if not self.resultOrderForDcQueue():
            return False
        return True


def clean_temp_files():
    print "clean_temp_files"
    pass

##############################################test#############################
@retries(3)
def test_retries():
    print "test"
    raise NameError#httplib.HTTPException

def test_ocr():
    f_name = "pass_code.jpeg"
    text =  call_tesseract(f_name)
    print "read:%s" % text

@retries(3)
def test_reconnect():
    header = {
        "Accept":"*/*",
        "X-Requested-With":"XMLHttpRequest",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip, deflate",
        "Connection":"Keep-Alive",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    url = "http://www.baidu.com"
    for i in range(3):
        print "send"
        g_conn.request('GET', url, headers=header)
        res = g_conn.getresponse()
        data = res.read()
        print "send"
        restart_conn(g_conn)

def test_get_svr_ips():
    print "test_get_svr_ips"
    pass
##############################################test#############################


def show_conf():
    print "########show conf##############"
    print "Buy:%s" % (','.join(g_buy_list))
    print "Ingnore:%s" % (','.join(g_ingnore_list))
    print "Query data:", g_query_data
    print "Passengers:", g_passengers
    print "Sleep time:%f" % g_query_sleep_time
    print "Auto OCR: %d" % g_max_auto_times
    print "\n"
    

def main():

    show_conf()
    #set log
    hdlr = logging.FileHandler('.\log.txt')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)

    #test_retries()
    print "connecting......"
    g_conn.connect()

    ha = HttpAuto()
    
    ha.construct_passengerTicketStr()
    if not ha.loginAysnSuggest():
        return False

    while 1:
        try:
            ha.query()
        except Exception as e:
            traceback.print_exc()
    return True


if __name__ == '__main__':
    #test_ocr()
    #test_reconnect()
    main() 
