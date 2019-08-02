import sendmail

msg = '从我们不断扩大的名单中选择一个符合你的游戏风格的霸主身份。每名霸主都能对游戏造成独特影响，每名玩家都能找到适合自己的霸主。'
sendmail.send(_from = r'ietarmailtest@163.com',to='d785@vip.qq.com',message=msg)
