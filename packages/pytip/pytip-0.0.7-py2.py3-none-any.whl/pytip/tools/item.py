import re
import datetime
import itertools


REGEX_DATETIME = {
    '[\d]{4}-[\d]{2}-[\d]{2}.[A-Z]{2}[\d]{1,2}:[\d]{1,2}:[\d]{1,2}':
    '%Y-%m-%d.%p%I:%M:%S', # '2022-07-31.AM3:02:30'
    '[\d]{4}\.[\d]{2}\.[\d]{2}\.[A-Z]{2}[\d]{1,2}:[\d]{1,2}':
    '%Y.%m.%d.%p%I:%M',    # '2022.07.31.AM3:02'
}


# Input params 전처리 작업용
# Input params 전처리 작업용
def date_to_string(_date:any=None, datetime_obj:bool=False, split_index=True):

    r"""date 객체를 string 으로 자동변환
    _date    : 날짜객체
    datetime : datetime 객체로 출력
    return :: '2000-01-01'"""
    
    _return = None
    if _date is None:
        _return = datetime.date.today().isoformat()
    elif type(_date) == datetime.date:
        _return = _date.isoformat()
    elif type(_date) == datetime.datetime:
        _return = _date.date().isoformat()
    elif type(_date) == str:
        _check = "".join(re.findall(r'[\d]{8}', _date))
        _check_re = re.findall('[,-//.]', _date)
        if len(_check) == 8:
            _return = f"{_check[:4]}-{_check[4:6]}-{_check[6:]}"

        elif len(_check_re) > 0:
            for punct_string in ['-','/',',', '.']:
                if _date.find(punct_string) != -1:
                    _return = "-".join(list(map(
                        lambda x : (f'{x:0>2}'), _date.split(punct_string))))
                else:
                    pass

    assert _return is not None, f'TypeError : {_date} 를 분석할 수 없습니다'
    if datetime_obj:
        # datetime.datetime.strptime('09/19/22 13:55:26', '%m/%d/%y %H:%M:%S')
        return datetime.datetime.strptime(_return, '%Y-%m-%d').date()
    return _return



# 텍스트를 datetime 객체로 해석 (REGEX_DATETIME)
def string_to_datetime(text:str):
    r"""text -> datetime.str
    regex 추출값에 따라 `time regex format` 개별적용"""

    format = ''
    time_regex = REGEX_DATETIME
    for regex, time_string in time_regex.items():
        check = re.findall(regex, text)
        if len(check) > 0:
            format = time_string

    # regex 분석결과 없을 때, 원본 그대로 출력
    if format == '':
        return text
    return datetime.datetime.strptime(text, format)


# items to split lists
def divide_chunks(items:list=None, n:int=None):
    r"""Split items
    (list) items : 객체 나누기
    (int)  n : Number"""
    if type(items) == list:
        for i in range(0, len(items), n): # looping till length l
            yield items[i:i + n]          # list should have
    
    elif type(items) == dict:
        for i in range(0, len(items), n):
            yield dict(itertools.islice(items.items(), i ,i+n))

