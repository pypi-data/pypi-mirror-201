# -*- coding: utf-8 -*-
"""
企业微信机器人消息类封装
- 消息类型：https://developer.work.weixin.qq.com/document/path/90236
- 加解密方案说明: https://developer.work.weixin.qq.com/devtool/introduce?id=36388
@author     : coreylin
@createTime : 2018/12/22
"""
from baselib.py import urllib2
import json
import base64
import hashlib


class QyWechat(object):
    """ 企业微信处理类
    """
    font_tmpl = '<font color="{color}">{info}</font>'

    class EnumPageType:
        # 按字符分页
        SPLIT = "split"
        # 按行分页
        SPLIT_BY_LINES = "split_by_lines"
        # 截断
        CUT = "cut"

    class EnumMsgType:
        MARKDOWN = "markdown"
        NEWS = "news"
        TEXT = "text"
        IMAGE = "image"

    def __init__(
            self,
            key,
            proxy="",
            is_ssl=True,
            debug=False):
        # 在 init 中定义所有私有变量，方便查找，无特别意义
        self.key = None
        self.url = self.__proxy = None

        self.debug = debug
        self.set_proxy(proxy)
        self.set_ssl(is_ssl)
        self.update_key(key)

    def update_key(self, key):
        self.key = key
        self.url = "%s/cgi-bin/webhook/send?key=%s" % (self.domain, self.key)

    def set_ssl(self, is_ssl=False):
        if is_ssl:
            self.domain = "https://qyapi.weixin.qq.com"
        else:
            self.domain = "http://qyapi.weixin.qq.com"

    def set_proxy(self, proxy):
        self.__proxy = proxy

    def format_text(self, content, m_list=None, mm_list=None):
        """
        将输入文本转换为企业微信的请求格式
        :param content: 文本内容，最长不超过2048个字节，必须是utf8编码
        :param m_list:  userid的列表，提醒群中的指定成员(@某个成员)，
                        @all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
        :param mm_list: 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        :return:
        """
        if isinstance(m_list, str):
            m_list = [m_list]

        if isinstance(mm_list, str):
            mm_list = [mm_list]

        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }

        if m_list is not None and len(m_list) > 0:
            data["text"]["mentioned_list"] = m_list
        if mm_list is not None and len(mm_list) > 0:
            data["text"]["mentioned_mobile_list"] = m_list
        return data

    def format_image(self, base64_data, md5):
        data = {
            "msgtype": "image",
            "image": {
                "base64": base64_data,
                "md5": md5
            }
        }
        return data

    def format_news(self, title, target_url, desc=None, pic_url=None):
        data = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": title,
                        "url": target_url
                    }
                ],

            }
        }
        if desc is not None:
            data["news"]["articles"][0]["description"] = desc
        if pic_url is not None:
            data["news"]["articles"][0]["picurl"] = pic_url
        return data

    def md5sum(self, filename):
        with open(filename, "rb") as f:
            fcont = f.read()
        f.close()
        fmd5 = hashlib.md5(fcont)
        return fmd5.hexdigest()

    def _send(self, data):
        """
        使用post方法，向企业微信发送消息
        :param data: 发送消息内容，为字典类型，通过get_xxx_data获得
        :return:企业微信返回的json消息，如：{u'errcode': 0, u'errmsg': u'ok'}
        """
        if len(self.__proxy) > 0:
            proxy = urllib2.ProxyHandler({'http': self.__proxy})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
        post_json = json.dumps(data)
        if self.debug:
            print("url :{}, \ndata :{}".format(self.url, post_json))
            print("proxy : {}".format(self.__proxy))
        rsp = urllib2.urlopen(self.url, post_json.encode('utf-8')).read()
        if self.debug:
            print(rsp)
        return json.loads(rsp)

    def send_image(self, img_path):
        """ 发送图片
        :param img_path: 图片文件的本地路径
        :return: 企业微信返回的json消息，如：{u'errcode': 0, u'errmsg': u'ok'}
        """
        md5 = self.md5sum(img_path)
        with open(img_path, "rb") as f:
            # b64encode是编码，b64decode是解码
            base64_data = base64.b64encode(f.read())
        self._send(self.format_image(base64_data, md5))

    def send_news(self, data):
        pass

    def send_markdown(
            self, msg, page_type=EnumPageType.CUT, limit=4096, post_msg="\n...",
            to_user=None, to_party=None, to_tag=None, agent_id=None,
            enable_duplicate_check=None, duplicate_check_interval=None):
        """ 发送 markdown 格式的数据
        :param string msg: 发送的数据内容（markdown格式）
        :param int limit: 分页参数，每条消息的最大长度（企业微信默认4096），超过该长度报错
        :param string page_type: 分页参数，消息内容超长的处理方法， 取值范围：EnumPageType.CUT
        :param string post_msg: 分页参数，选择截断时，加在消息末尾的补充信息
        :param list to_user: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）
            特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param list to_party:  指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个,
            当touser为"@all"时忽略本参数
        :param list to_tag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。
            当touser为"@all"时忽略本参数
        :param int agent_id: 企业应用的id，整型。企业内部开发，可在应用的设置页面查看；第三方服务商，可通过接口 获取企业授权信息 获取该参数值
        :param int enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param int duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :return:
        """
        # 根据分页方式，对页面数据进行剪切
        if page_type.lower() == self.EnumPageType.SPLIT:
            msg_list = self.split_msg(msg, limit)
        elif page_type.lower() == self.EnumPageType.SPLIT_BY_LINES:
            msg_list = self.split_msg_by_line(msg, limit)
        else:
            msg_list = [self.cut_msg(msg, limit, post_msg)]

        rsp_list = []
        for msg in msg_list:
            rsp_list.append(self.raw_send_markdown(
                msg, to_user, to_party, to_tag, agent_id,
                enable_duplicate_check, duplicate_check_interval))
        if len(rsp_list) == 1:
            return rsp_list[0]
        return rsp_list

    def raw_send_markdown(
            self, content, to_user=None, to_party=None, to_tag=None, agent_id=None,
            enable_duplicate_check=None, duplicate_check_interval=None):
        """ 发送 markdown 消息
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        if to_user is not None:
            data['touser'] = "|".join(to_user)
        if to_party is not None:
            data["toparty"] = " | ".join(to_party)
        if to_tag is not None:
            data["totag"] = " | ".join(to_tag)
        if agent_id is not None:
            data["agentid"] = agent_id
        if enable_duplicate_check is not None:
            data["enable_duplicate_check"] = enable_duplicate_check
        if duplicate_check_interval is not None:
            data["duplicate_check_interval"] = duplicate_check_interval
        return self._send(data)

    def send_text(self, data):
        pass

    def cut_msg(self, msg, limit=4096, post_msg="\n..."):
        """ 将 msg 长度限制在 limit 以内
            - 如果大于 limit， 则截断多余部分，并补充 post_msg
            - 如果小于等于 limit，则直接返回
        :param string msg: 消息内容
        :param int limit: 消息长度限制
        :param string post_msg: 截断末尾补充消息
        :rtype: string
        :return: 返回截断后数据
        """
        msg_len = len(msg.encode("utf-8"))
        if msg_len <= limit:
            return msg
        post_msg_len = len(post_msg.encode("utf-8"))
        idx = 0
        for idx in range(len(msg)):
            if len(msg[:-1 - idx].encode("utf-8")) <= limit - post_msg_len:
                break
        return msg[:-1 - idx] + post_msg

    def split_msg(self, msg, limit=4096):
        """ 将消息 msg 的长度限制（limit），拆分成多条消息(一条消息即一页）
        :param string msg: 消息内容
        :param int limit: 消息长度限制
        :rtype: list
        :return: 返回分页后的数据列表
        """
        msg_len = len(msg.encode("utf-8"))
        if msg_len <= limit:
            return [msg]
        lines = [""]
        line_no = 0
        for char in msg:
            if len(lines[line_no].encode("utf-8")) <= limit - \
                    len(char.encode("utf-8")):
                lines[line_no] += char
                continue
            lines.append(char)
            line_no += 1
        return lines

    def split_msg_by_line(self, msg, limit=4096):
        """ 将数据按行分页
            本函数适用场景： 消息分多行，单行不超过 limit的情况，单行limit会直接截断
        :param string msg: 消息内容
        :param int limit: 消息长度限制
        :rtype: list
        :return: 返回分页后的数据列表
        """
        msg = msg.strip()
        msg_len = len(msg.encode("utf-8"))
        if msg_len < limit:
            return [msg]
        page_len = page_no = 0
        page_list = [""]
        for aline in msg.split("\n"):
            len_aline = len("{}\n".format(aline).encode("utf-8"))
            if page_len + len_aline <= limit:
                page_len += len_aline
                page_list[page_no] += "{}\n".format(aline)
                continue
            page_len = 0
            page_no += 1
            page_list.append(self.cut_msg(aline, limit, "..."))
        return [i.strip() for i in page_list]


if __name__ == "__main__":
    def demo():
        key = ""  # robot key
        robot = QyWechat(key=key, is_ssl=True, debug=True)
        aline = "[hello](http://www.baidu.com)"*100
        print(robot.send_markdown(
            "# test\n" + aline + "\n" + aline + "\n",
            page_type=robot.EnumPageType.SPLIT_BY_LINES))
    demo()
