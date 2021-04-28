#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author Jiangwang,Neolead
import requests
import xlrd
import xlwt
import json
import hashlib
import sys
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
day=time.strftime("%Y-%m-%d",time.localtime(time.time()))
scanid='11111111-1111-1111-1111-111111111111'#default scan id   11111111-1111-1111-1111-111111111111
u = 'demo@demo.com'
p = 'pa$$word123'



def logout_wvs(headers): 
    headers=headers
    url='https://acunetix_url:3443/api/v1/me/logout'
    requests.packages.urllib3.disable_warnings()
    r=requests.post(url=url,headers=headers,verify=False)
    print ( 'Logged out')

def login_wvs(username,passwd): 
    hash_256 = hashlib.sha256()
    hash_str = "%s" % passwd
    hash_256.update(hash_str.encode('utf-8'))
    pwd_hash = hash_256.hexdigest()
    uname=username
    url='https://acunetix_url:3443/api/v1/me/login'
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36','Content-Type': 'application/json;charset=UTF-8','Referer': 'https://acunetix_url:3443/'}
    datas={"email":"%s" % uname,"password":"%s" % pwd_hash,"remember_me":"false","logout_previous":"true"}
    s=json.dumps(datas)
    requests.packages.urllib3.disable_warnings()
    r=requests.post(url=url,data=s,headers=headers,verify=False)
    x_auth=r.headers['X-Auth']
    c=r.headers['Set-cookie']
    c1=c.find(';')
    cookie=c[0:c1]
    headers={'X-Auth':'%s' % x_auth,'cookie':'%s' % cookie,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36','Content-Type': 'application/json;charset=UTF-8','Referer': 'https://acunetix_url:3443/'}
    return headers

def add_target(files,headers):
    url='https://acunetix_url:3443/api/v1/targets'
    headers=headers
    xld=xlrd.open_workbook(files)
    table=xld.sheet_by_index(0)
    nrows=table.nrows
    target_ids = []
    for i in range(0,nrows):
        address=table.cell(i, 0).value
        d={"address":"%s" % address,"description":"%s" % day,"criticality":"10"}
        data=json.dumps(d)
        r=requests.post(url=url,data=data,headers=headers,verify=False)
        d=json.loads(r.text)
        target_id=d['target_id']
        target_ids.append(target_id)
    return target_ids
def start_job(target_ids,headers): 
    l=len(target_ids)
    print(l)
    url = 'https://acunetix_url:3443/api/v1/scans'
    headers = headers
    for i in range(0,l):
        d={"target_id":"%s" % target_ids[i],"profile_id":"%s" % scanid,"report_template_id":"11111111-1111-1111-1111-111111111111","schedule":{"disable":False,"start_date":None,"time_sensitive":False}}
        data=json.dumps(d)
        requests.packages.urllib3.disable_warnings()
        r=requests.post(url=url,headers=headers,data=data,verify=False)
    print ( 'A total of %d targets were scanned this time'% l )

def get_current_target_ids(headers):
    current_target_ids=[]
    url='https://acunetix_url:3443/api/v1/targets'
    for i in range(0,999):
        d = {'c': '%d' % i}
        requests.packages.urllib3.disable_warnings()
        s = requests.session()
        s.keep_alive = False
        r=requests.get(url=url,params=d,headers=headers,verify=False)
        data=json.loads(r.text)
        t=data['targets']
        if t:
            t_value = t[0]
            current_target_id = t_value['target_id']
            current_target_ids.append(current_target_id)
        else:
            break
    return current_target_ids

if __name__ == '__main__':
    headers = login_wvs(u,p)
    print("We are now importing Targets")
    print ( 'Logging in to WVS' )
    headers = login_wvs(u, p)
    print ( 'Login is successful, start to add scan target' )
    target_ids = add_target('./wvs_url.xls', headers)
    print ( 'The scan target is added, start to execute the scan task' )
    start_job(target_ids, headers)
    print ( 'Scan tasks have been executed' )
    logout_wvs(headers)
    print ( 'logout' )
    print('')
