#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# @Author  : Jane
# @Time    : 2021/5/4 13:18
# @Function: 定期推送基金估值到微信
# @cron :50 14 * * * /usr/bin/python3 /root/fund/fund_wc.py


import datetime
import json
import re
import requests
from chinese_calendar import is_workday # pip install chinesecalendar



# 获取基金估值数据
def res(code):
    url = 'http://fundgz.1234567.com.cn/js/%s.js' % code
    result = requests.get(url)
    # 发送请求
    data = json.loads(re.match(".*?({.*}).*", result.text, re.S).group(1))

    if float(data['gszzl']) <= (-1.15):
        global today_fund, flag
        flag = True
        today_fund = ('基金编码：%s' % data['fundcode'] + '\n基金名称：%s' % data['name'] + '\n估算增量：%s' % data['gszzl'] +
                      '\n估值时间：%s' % data['gztime'])


today_fund = None
flag = False
get_access_token = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=企业ID&corpsecret'
                                '=应用密钥')
res_access_token = json.loads(get_access_token.text)
access_token = res_access_token['access_token']


# 推送数据到微信
def main():
    global today_fund
    send_data = {
        "toparty": "2",
        "msgtype": "text",
        "agentid": 1000002,
        "text": {
            "content": today_fund
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    send_msges = (bytes(json.dumps(send_data), 'utf-8'))
    # 判断是否为工作日
    date = datetime.date.today()
    if_workday = is_workday(date)
    if if_workday:
        requests.post('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token,
                      data=send_msges)
    else:
        print('非工作日时间，未推送至微信！')


if __name__ == '__main__':
    e = '005491', '005827', '004997', '004241', '519736'
    for i in e:
        res(i)
        if flag:
            main()
            flag = False
