# WechatBookNswttArenaTicket
用于自动订微信的南山文体通的场地卷，需要输入微信访问南山文体通的JSESSIONID

执行(需要安装python的requests库）：
```bash
python wechat_auto_book.py $YOUR_JSESSIONID
```

我的使用：
在linux系统中，采用cron在工作日的下午2点自动执行这个程序
```cron
0 14 * * 1,2,3,4,5 python /home/mania/Codes/badminton/wechat_auto_book.py $MY_JSESSIONID>> /home/mania/Codes/badminton/log
```

### 关键是获取JSESSIONID
我采用mitmproxy获取。
linux中安装mitmproxy后，
```bash
mitmproxy -p 1234
```
手机的wifi设置使用这个代理，IP为linux机器的ip，端口就是上面的1234.
这样，手机的流量都会被mitmproxy解析（即使是加密的信息也行，这才是它厉害的地方）
手机进入微信的南山文体通，点击抢劵，这时已经产生POST动作，可以在mitmproxy的输出中看到这个POST，enter进去可以找到JSESSIONID这个变量。
