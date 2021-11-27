from dingtalkchatbot.chatbot import DingtalkChatbot
from django.conf import settings

def send(message, at_mobiles=None):
    # 引用settings中配置好的钉钉群消息通知的webhook地址
    if at_mobiles is None:
        at_mobiles = []
    webhook = settings.DINGTALK_WEB_HOOK

    # 初始化机器人小丁
    # 方式一：
    xiaoding = DingtalkChatbot(webhook)
    # 方式二：勾选”加签“选项时使用（v1.5以上）
    # xiaoding = DingtalkChatbot(webhook,secret=secret)

    # text消息@所有人
    msg = "面试通知： %s" % message
    # xiaoding.send_text(msg, at_mobiles=['18888888888'])
    xiaoding.send_text(msg, at_mobiles=at_mobiles)
