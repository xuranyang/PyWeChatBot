import base64
import hashlib
import configparser
import requests


class WeChatBot(object):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            # 直接指定key
            self.wx_key = args[0]
        elif len(args) == 2:
            ini, section = args[0], args[1]
            # 通过配置文件传参
            conf = configparser.ConfigParser()
            conf.read(ini, encoding='utf-8')

            self.wx_key = conf.get(section, "wx_key")

        self.url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={self.wx_key}"

    def send_text(self, content, mentioned_list: list = [], mentioned_mobile_list=["@all"]):
        """
        :param content: 让群机器人发送的消息内容；文本内容，最长不超过2048个字节，必须是utf8编码
        :param mentioned_list: userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
        :param mentioned_mobile_list: 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        :return:
        """
        # 这里就是群机器人的Webhook地址
        headers = {"Content-Type": "application/json"}  # http数据头，类型为json
        data = {
            "msgtype": "text",
            "text": {
                "content": content,  # 让群机器人发送的消息内容
                "mentioned_list": mentioned_list,  # @全体成员
                "mentioned_mobile_list": mentioned_mobile_list
            }
        }
        r = requests.post(self.url, headers=headers, json=data)  # 利用requests库发送post请求
        print(r.json())

    def send_markdown(self, content):
        """
        :param content: markdown内容，最长不超过4096个字节，必须是utf8编码
        :return:
        """
        headers = {"Content-Type": "application/json"}  # http数据头，类型为json
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content,
            }
        }
        r = requests.post(self.url, headers=headers, json=data)  # 利用requests库发送post请求
        print(r.json())

    def send_image(self, image_path):
        """
        发送 图片类型 消息
        注：图片（base64编码前）最大不能超过2M，支持JPG,PNG格式
        图片内容的base64编码
        图片内容（base64编码前）的md5值
        :param image_path: 图片地址
        :return:
        """
        base64_image, md5_image = self.wx_handle_image(image_path)
        headers = {"Content-Type": "application/json"}  # http数据头，类型为json
        data = {
            "msgtype": "image",
            "image": {
                "base64": base64_image,  # 图片内容的base64编码
                "md5": md5_image  # 图片内容（base64编码前）的md5值
            }
        }
        r = requests.post(self.url, headers=headers, json=data)  # 利用requests库发送post请求
        print(r.json())

    @staticmethod
    def wx_handle_image(image_path):
        """
        微信发送图片时，将图片处理成对应的 base64 和 md5 值
        :param image_path:
        :return:
        """
        # 如果是url 用 request.get 来解析读取bytes
        if image_path.startswith("http"):
            image_bytes = requests.get(image_path).content
        else:
            # 如果不是url，是本地路径 用 open 来解析读取bytes
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()

        base64_str = base64.b64encode(image_bytes).decode('utf-8')
        md5_str = hashlib.md5(image_bytes).hexdigest()
        return base64_str, md5_str

    def send_news(self, title, url, picurl, description=""):
        """
        发送图文（单条）
        参数	        是否必填	说明
        msgtype	    是	    消息类型，此时固定为news
        articles	是	    图文消息，一个图文消息支持1到8条图文
        title	    是	    标题，不超过128个字节，超过会自动截断
        description	否	    描述，不超过512个字节，超过会自动截断
        url	        是	    点击后跳转的链接
        picurl	    否	    图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150
        :return:
        """
        headers = {"Content-Type": "application/json"}  # http数据头，类型为json
        data = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": title,
                        "description": description,
                        "url": url,
                        "picurl": picurl
                    }
                ]
            }
        }
        r = requests.post(self.url, headers=headers, json=data)  # 利用requests库发送post请求
        print(r.json())

    def upload_media_file(self, type, file_path):
        """
        微信 文件上传接口
        普通文件(file)：文件大小不超过20M
        语音(voice)：文件大小不超过2M，播放长度不超过60s，仅支持AMR格式
        :param file_path:
        :param type: 文件类型，分别有语音(voice)和普通文件(file)
        :return:
        """
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={self.wx_key}&type={type}'
        params = {
            "type": type
        }

        files = {
            "media": open(file_path, "rb")
        }

        r = requests.post(upload_url, params=params, files=files)  # 利用requests库发送post请求
        return r.json()

    def send_file(self, media_id):
        """
        微信发送消息 文件类型
        :param media_id: 文件id，通过下文的文件上传接口获取
        :return:
        """
        headers = {"Content-Type": "application/json"}  # http数据头，类型为json
        data = {
            "msgtype": "file",
            "file": {
                "media_id": media_id,
            }
        }
        r = requests.post(self.url, headers=headers, json=data)  # 利用requests库发送post请求
        return r.json()

    def send_voice(self, media_id):
        """
        微信发送消息 语音类型
        :param media_id: 语音文件id，通过下文的文件上传接口获取
        :return:
        """
        headers = {"Content-Type": "application/json"}  # http数据头，类型为json
        data = {
            "msgtype": "voice",
            "voice": {
                "media_id": media_id,
            }
        }
        r = requests.post(self.url, headers=headers, json=data)  # 利用requests库发送post请求
        return r.json()


if __name__ == '__main__':
    wx_key = "xxxxxxxxxxx"
    wx = WeChatBot(wx_key)

    # 发送文本
    # wx.send_text("准备起床啦~~~")

    # 发送markdown
    # wx.send_markdown("""实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n
    #          >类型:<font color=\"comment\">用户反馈</font>
    #          >普通用户反馈:<font color=\"comment\">117例</font>
    #          >VIP用户反馈:<font color=\"comment\">15例</font>""")

    # 发送图片
    # wx.send_image(r"./xxx.png")
    # wx.send_image("http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png")

    # 发送图文
    # wx.send_news(title="该摸鱼了", url="zhihu.com", picurl="https://img0.baidu.com/it/u=490071974,3856819170&fm=253&fmt=auto&app=120&f=JPEG?w=608&h=304",
    #              description="是时候休息一下了")

    # 上传并发送文件
    # {'errcode': 0, 'errmsg': 'ok', 'type': 'file', 'media_id': 'xxx', 'created_at': '1725044502'}
    # resp = wx.upload_media_file('file', r'../test/test.txt')
    # wx.send_file(resp['media_id'])
