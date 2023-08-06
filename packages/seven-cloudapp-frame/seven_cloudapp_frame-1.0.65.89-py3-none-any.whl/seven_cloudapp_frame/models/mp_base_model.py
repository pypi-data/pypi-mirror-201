# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-12-20 16:07:52
@LastEditTime: 2023-03-21 09:43:51
@LastEditors: HuangJianYi
@Description: 中台接口相关处理业务模型
"""
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import SevenHelper

class MPBaseModel():
    """
    :description: 中台接口相关处理业务模型
    """
    def __init__(self, context=None, logging_error=None, logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def get_public_function_list(self, project_code, return_response_status=False):
        """
        :description:  获取公共功能列表
        :param project_code:收费项目代码（服务管理-收费项目列表）
        :param return_response_status:是否返回响应状态
        :return list: 
        :last_editors: HuangJianYi
        """
        response_status = False
        public_function_list = []
        if not project_code:
            if return_response_status:
                return public_function_list,response_status
            return public_function_list
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = share_config.get_value("power_project_id") # 权限产品id,SaaS走project_name,SaaS定制走power_project_id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            if return_response_status:
                return public_function_list,response_status
            return public_function_list
        requst_url = share_config.get_value("mp_url","http://taobao-mp-s.gao7.com") + "/general/project_code_list"
        data = {}
        data["project_code"] = project_code
        data["product_id"] = product_id
        result = HTTPHelper.get(requst_url, data, {"Content-Type": "application/json"})
        if result and result.ok and result.text:
            obj_data = SevenHelper.json_loads(result.text)
            if obj_data and obj_data["Data"]:
                public_function_list = obj_data["Data"]
                response_status = True
        if return_response_status:
                return public_function_list,response_status
        return public_function_list

    def get_custom_function_list(self, store_user_nick, return_response_status=False):
        """
        :description:  获取定制功能列表，权限产品id（power_project_id）,SaaS定制走power_project_id必须配置，SaaS可不配置走project_name,对应中台表function_product_tb的app_id字段
        :param store_user_nick:商家主账号昵称
        :param return_response_status:是否返回响应状态
        :return list: 
        :last_editors: HuangJianYi
        """
        response_status = False
        custom_function_list = []
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = share_config.get_value("power_project_id") # 权限产品id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            if return_response_status:
                return custom_function_list,response_status
            return custom_function_list
        requst_url = share_config.get_value("mp_url", "http://taobao-mp-s.gao7.com") + "/custom/query_skin_managemen_list"
        data = {}
        data["product_id"] = product_id
        data["store_user_nick"] = store_user_nick
        result = HTTPHelper.get(requst_url, data, {"Content-Type": "application/json"})
        if result and result.ok and result.text:
            obj_data = SevenHelper.json_loads(result.text)
            if obj_data and obj_data["Data"]:
                custom_function_list = obj_data["Data"]
                response_status = True
        if return_response_status:
                return custom_function_list,response_status
        return custom_function_list
    
    def get_key_power_list(self, store_user_nick, project_code, key_names, user_type=0, return_response_status=False):
        """
        :description:  指定模块权限列表，权限产品id（power_project_id）,SaaS定制走power_project_id必须配置，SaaS可不配置走project_name,对应中台表function_product_tb的app_id字段
        :param store_user_nick:商家主账号昵称
        :param project_code:项目编码
        :param key_names:权限代码，多个逗号分隔
        :param user_type:0-不限1-SAAS用户2-SAAS定制用户
        :param return_response_status:是否返回响应状态
        :return list: 
        :last_editors: HuangJianYi
        """
        response_status = False
        power_list = []
        #产品id
        product_id = config.get_value("project_name")
        power_project_id = share_config.get_value("power_project_id") # 权限产品id
        if power_project_id:
            product_id = power_project_id
        if not product_id:
            if return_response_status:
                return power_list,response_status
            return power_list
        requst_url = share_config.get_value("mp_url", "http://taobao-mp-s.gao7.com") + "/general/jurisdiction_list"
        data = {}
        data["product_id"] = product_id
        data["project_code"] = project_code
        data["store_user_nick"] = store_user_nick
        data["key_name"] = key_names
        if user_type > 0:
            data["user_type"] = user_type
        result = HTTPHelper.get(requst_url, data, {"Content-Type": "application/json"})
        if result and result.ok and result.text:
            obj_data = SevenHelper.json_loads(result.text)
            if obj_data and obj_data["Data"]:
                power_list = obj_data["Data"]
                response_status = True
        if return_response_status:
                return power_list,response_status
        return power_list
    
    def check_high_power(self, store_user_nick, project_code, key_names, user_type=0, return_response_status=False):
        """
        :description:  检验是否有指定模块的权限
        :param store_user_nick:商家主账号昵称
        :param project_code:项目编码
        :param key_names:权限代码，多个逗号分隔 
        :param user_type:0-不限1-SAAS用户2-SAAS定制用户
        :param return_response_status:是否返回响应状态
        :return bool: 是否有权限
        :last_editors: HuangJianYi
        """
        response_status = False
        if return_response_status == True:
            power_list, response_status = self.get_key_power_list(store_user_nick, project_code, key_names, user_type, return_response_status)
        else:
            power_list = self.get_key_power_list(store_user_nick, project_code, key_names, user_type)
        is_power = True    
        for key in power_list:
            if key["is_power"] == False:
                is_power = False
                break
        if return_response_status == True:
            return is_power,response_status
        return is_power