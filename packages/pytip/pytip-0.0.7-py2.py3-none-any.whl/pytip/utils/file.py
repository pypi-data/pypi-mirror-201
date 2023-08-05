import os
import json
import socket
import pickle
import requests
import subprocess
from tqdm import tqdm
from urllib import request
from multiprocessing import Pool


# https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
def download_file(
        url:str=None, folder:str=None, 
        chunk_size:int=8192, 
        overwite=False
    ) -> str:
    r"""웹사이트 파일 다운로드
    url (str) : 다운로드 파일 url 주소
    foler (str) : `./data` 파일 저장 경로
    chunk_size (int) : encoded response set chunk_size parameter to None.
    overwrite (bool) : download file overwrite"""

    local_filename = url.split('/')[-1]
    local_filename = f"{folder}/{local_filename}"

    if overwite == False:
        if os.path.exists(local_filename):
            print(f'{local_filename} is existed\n`overwrite` changes to `True`')
            return local_filename

    headers = {"Referer":url,
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",}
    with requests.get(url, headers=headers,stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
    print(f'{local_filename} downloading is done.')
    return local_filename


def multiprocess_items(funcion, items:int, worker:list, display=False):
    r"""list() 데이터를  function 에 multiprocessing 반복적용
    function : 반복적용할 함수
    items    : function 에 입력할 데이터"""

    with Pool(worker) as pool:
        if display:
            items = list(tqdm(pool.imap(funcion, items), total=len(items)))
        else:
            items = pool.map(funcion, items)
        return items


# http://taewan.kim/tip/python_pickle/
def pickle_data(file_path:str=None, option='w', data=None):
    r"""파이썬 객체를 Pickle 로 저장하고 호출
    file (str) : 파일이름
    option (str) : w,r (Write / Read)
    data (any) : pickle 로 저장할 
    """
    
    assert option in ['w', 'r'], f"`option` 은 `w`,`r` 하나를 입력하세요."
    option = {'w':'wb', 'r':'rb'}[option]
    
    with open(file_path, option) as f:
        if option == 'wb':
            assert data is not None, f"{data} 값을 저장 할 수 없습니다."
            pickle.dump(data, f)
            print(f"{file_path} saving done.")
            return None

        elif option == 'rb':
            assert data is None, f"불러오는 경우, {data}는 필요 없습니다."
            return pickle.load(f)
