# -*- coding:utf-8 -*-
""" json 文件读写与更新
"""
import os
import json


class JsonFile(object):

    @classmethod
    def read(cls, file_path):
        """ 读取 文件路径为 $file_path 的 json 文件
        :param file_path: 文件路径，包括目录，名称，后缀
        :return:
            - 正常情况下，返回 json 文件
            - json 文件不存在，读取失败，以及内容为空时，返回 {}
        """
        if not os.path.isfile(file_path):
            return {}
        try:
            with open(file_path, 'r') as fid:
                data = json.load(fid)
        except Exception:
            return {}
        return data

    @classmethod
    def write(cls, file_path, data, indent=None):
        """ 写入 文件路径为 $file_path 的 json 文件
        :param string file_path: 文件路径，包括目录，名称，后缀
        :param dict data: 要写入的数据
        :param int indent: json 格式对齐，默认为None，不做格式化
        :return: 实际写入的数据（即入参 data）
        """
        with open(file_path, 'w') as fid:
            fid.writelines(json.dumps(data, indent=indent))
        return data

    @classmethod
    def update(cls, file_path, data, indent=None):
        """
        :param string file_path: 文件路径，包括目录，名称，后缀
        :param dict data: 要写入的数据
        :param int indent: json 格式对齐，默认为None，不做格式化
        :return: 实际写入的数据（即入参 data）
        """
        org_data = cls.read(file_path)
        org_data.update(data)
        return cls.write(file_path, org_data, indent)
