# 存储常量值
url = 'https://www.hko.gov.hk/sc/cis/normal/1981_2010/dnormal'
root_url = 'https://www.hko.gov.hk/'
regulars = r'src="(..+?\.jpg)"'

week7_uri = '10.htm'

table_header = {
    '日期': 'date',
    '平均气压': 'press',
    '平均最高气温': 'temp tmax',
    '平均气温': 'temp tmean',
    '平均最低气温': 'temp tmin',
    '湿球温度': 'wet',
    '露点温度': 'dew',
    '相对湿度': 'rh',
    '平均日雨量': 'rain',
    '云量': 'cloud',
    '平均日照': 'sun',
    '盛行风向': 'wind2 dd',
    '平均风速': 'wind2 ff',
    '上午海水温度': 'wind seatemp',
    '下午海水温度': 'wind seatemp2'
}

table_h1 = [
    'date',
    'press',
    'temp tmax',
    'temp tmean',
    'temp tmin',
    'wet',
    'dew',
    'rh',
    'rain',
    'cloud',
]

table_h2 = [
    'sun',
    'wind2 dd',
    'wind2 ff',
    'wind seatemp',
    'wind seatemp2'
]