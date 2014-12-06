#Author frankiezhu@foxmail.com 
#DATE: 20140108

一、运行环境：
	基于python2.7

二、原理:
	图像识别基于tesseract
	数据抓包使用httpwatch, IE，识别出所有的POST请求，获取各步骤中数据，分析页面里token等

三、用法:
	修改conf_example.py里的买票信息, 然后运行
	在不繁重情况下，可以验证提交买票请求，买完后自己去"未完成订单"页面付款
	春运的压力环境下，有bug，待完善, python初学乍用，很多地方不 pythonic

四、Todo:
	1. 压力下的抢票测试, fixbug
	2. 寻找最优server ip
    3. httplib 的接口需要封装,包括重连机制
	4. 优化不必要的请求



