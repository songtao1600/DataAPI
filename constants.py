# -*- coding: utf-8 -*-
# @Author  :songtao
# @File    :constants.py

IMAGE_CODE_EXPIRES_SECONDS = 60 #图片验证码有效期,秒
SMS_CODE_EXPIRES_SECONDS = 60 #短信验证码有效期,秒

REDIS_AREA_INFO_EXPIRES_SECONDES = 86400 #redis缓存城区信息的有效期
REDIS_HOUSE_INFO_EXPIRES_SECONDES = 86400 #房屋信息缓存有效期

HOME_PAGE_DATA_REDIS_EXPIRE_SECOND = 7200 # 主页缓存数据过期时间 秒
HOME_PAGE_MAX_HOUSES = 5 #主页房屋展示最大数量

HOUSE_LIST_PAGE_CAPACITY = 5 # 房源列表页每页显示房屋数目
HOUSE_LIST_PAGE_CACHE_NUM = 2 # 房源列表页每次缓存页面书

REDIS_HOUSE_LIST_EXPIRES_SECONDS = 7200 # 列表页数据缓存时间 秒