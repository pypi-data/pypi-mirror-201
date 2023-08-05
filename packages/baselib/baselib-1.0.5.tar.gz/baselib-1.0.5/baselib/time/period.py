# -*- coding:utf-8 -*-
""" 时间段计算，用于获取某个时间段的起止时间（如1小时内，24小时内，7天内等）
"""
import datetime
import time


class Period(object):

    @classmethod
    def get_recent_hour(cls, n, minutes_ago=0):
        """ 截止到 minutes_ago 前，获取近 n 个小时的起止时间
        @param n: n 个小时到截止时间
        @param minutes_ago: 截止统计时间，默认为 0， 表示截止到当前位置
        """
        return cls.get_recent_minute(n * 60, minutes_ago)

    @classmethod
    def get_recent_minute(cls, n, minutes_ago=0):
        """ 截止到 minutes_ago 前，获取近 n 分钟的起止时间
        @param n: int, 到截止时间之前 n 分钟
        @param minutes_ago: int, 截止统计时间，默认为 0， 表示截止到当前位置
        """
        start_time = (datetime.datetime.now() -
                      datetime.timedelta(minutes=n + minutes_ago)).replace(microsecond=0)
        end_time = (datetime.datetime.now() -
                    datetime.timedelta(minutes=minutes_ago)).replace(microsecond=0)
        return (start_time, end_time)

    @classmethod
    def get_recent_day(cls, n, minutes_ago=0):
        """ 截止到 minutes_ago 前，获取近 n 分钟的起止时间
        @param n: int, 到截止时间之前 n 分钟
        @param minutes_ago: int, 截止统计时间，默认为 0， 表示截止到当前位置
        """
        start_time = (datetime.datetime.now() -
                      datetime.timedelta(days=n, minutes=minutes_ago)).replace(microsecond=0)
        end_time = (datetime.datetime.now() -
                    datetime.timedelta(minutes=minutes_ago)).replace(microsecond=0)
        return (start_time, end_time)

    @classmethod
    def get_day_begin(cls, dt=None):
        """ 获取指定某一天的起始时间，即当天的0时0分0秒
        @param dt: datetime， 指定的日期，默认为None，表示今天
        """
        if dt is None:
            dt = datetime.datetime.now()
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    @classmethod
    def get_day_end(cls, dt=None):
        """ 获取指定某一天的结束时间，即当天的23时59分59秒
        @param dt: datetime， 指定的日期，默认为None，表示今天
        """
        if dt is None:
            dt = datetime.datetime.now()
        return dt.replace(hour=23, minute=59, second=59, microsecond=0)

    @classmethod
    def get_month_begin(cls, dt=None):
        """ 获取指定某一天所在月的起始时间，即当月的1号的0时0分0秒
        @param dt: datetime， 指定的日期，默认为None，表示今天
        """
        if dt is None:
            dt = datetime.datetime.now()
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    @classmethod
    def get_month_end(cls, dt=None):
        """ 获取指定某一天所在月的结束时间，即当天所在月最后一天的23时59分59秒
        @param dt: datetime， 指定的日期，默认为None，表示今天
        """
        if dt is None:
            dt = datetime.datetime.now()
        # TODO: 待实现
        return dt.replace(hour=23, minute=59, second=59, microsecond=0)

    @classmethod
    def now(cls):
        """ 获取当前时间
        :rtype: datetime
        :return: 返回当前的时间（datetime格式）
        """
        return datetime.datetime.now()

    @classmethod
    def format_datetime(cls, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def format_t_datetime(cls, dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    @classmethod
    def format_date(cls, dt):
        return dt.strftime("%Y-%m-%d")

    @classmethod
    def format_time(cls, dt):
        return dt.strftime("%H:%M:%S")

    @classmethod
    def format_timestamp(cls, dt):
        """
        :param datetime dt:
        :rtype: int
        :return: dt 对应的时间戳
        """
        return int(time.mktime(dt.timetuple()))


if __name__ == "__main__":
    start_time, end_time = Period.get_recent_day(10, 10)
    print(start_time, end_time)
    print(Period.format_date(start_time))
    print(Period.format_time(start_time))
    print(Period.format_datetime(start_time))
    print(Period.format_t_datetime(start_time))
    print(1)
    print(Period.get_day_begin(start_time))
    print(Period.format_t_datetime(Period.get_day_end(end_time)))
