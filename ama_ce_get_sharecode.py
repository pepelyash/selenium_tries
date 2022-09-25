import random

from selenium.webdriver.common.by import By

import globvar
import webdr
import time
import newacc
import rwrf
import csv
import json
from time import sleep
import datetime


def log_info_to_txt(_str, path):
    with open(path, mode='a', encoding='utf-8', newline='') as f:
        f.write(_str)


def launch_driver(uax):
    driver = webdr.config_webdr(uax)
    link0 = 'about:blank'
    driver.get(link0)
    return driver


def get_cereflink(driver, amal):
    driver.get(amal)
    driver.implicitly_wait(2)
    # driver.switch_to.new_window('tab')
    # driver.get(f'{amal}{globvar.URLCUT_AMACE}')
    sleep(1)
    try:
        ref = log_force(driver)
        return ref
    except:
        print('cant get ama ref')
        return 'no_sharecode'


def log_force(driver):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        a = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
        for line in a.items():
            if line[0] == 'body' and line[1]:
                jtemp = json.loads(line[1])  # line[1] body data
                if 'api' in jtemp.keys() and jtemp['data']:
                    if jtemp['api'] == 'mtop.aliexpress.social.cashout.create':
                        return jtemp['data']['link']
                    if jtemp['api'] == 'mtop.aliexpress.social.cashout.get':
                        return jtemp['data']['link']


def log_filter(log_):
    return (
        # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
    )


def read_auwks_csv(rpath):
    # fields = ['ts', 'wklog', 'wkpwd', 'wktkn', 'wkid', 'ua', 'amal', 'aulog', 'aupwd', 'autkn', 'amar']
    amasl = []
    with open(rpath, mode='r', encoding='utf-8', newline='') as f:
        r = csv.DictReader(f)
        for row in r:
            amasl.append(row)
    return amasl


def create_dbrs(auwks):
    dbrl = []
    for each in auwks:
        dbr = newacc.DbRecord()
        dbr.ts = each['ts']
        dbr.wklog = each['wklog']
        dbr.wkpwd = each['wkpwd']
        dbr.wktkn = each['wktkn']
        dbr.wkid = each['wkid']
        dbr.ua = each['ua']
        dbr.amal = each['amal']
        dbr.aulog = each['aulog']
        dbr.aupwd = each['aupwd']
        dbr.autkn = each['autkn']
        dbr.amar = each['amar']
        dbrl.append(dbr)
    return dbrl


def pseudomain(auwk):
    curdate = datetime.datetime.now().strftime("%Y-%m-%d")
    path2 = f'resources/01nov21_500300200/amas_reflinks_log_by_{curdate}.txt'
    driver0 = launch_driver(auwk.ua)
    auwk.amar = get_cereflink(driver0, auwk.amal)
    driver0.quit()
    log_info_to_txt(f'{globvar.URLCUT_AMAREF}{auwk.amar} for {auwk.amal}\n', path2)


def save_dbinfo(dbr, wrpath):
    fields = ['ts', 'wklog', 'wkpwd', 'wktkn', 'wkid', 'ua', 'amal', 'aulog', 'aupwd', 'autkn', 'amar']
    with open(wrpath, mode='a', encoding='utf-8', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        wr.writerow(dbr.__dict__)


if __name__ == '__main__':
    path0 = 'resources/db_info_tempuse.csv'
    path1 = 'resources/db_info_tempuse_output.csv'
    auwks0 = read_auwks_csv(path0)
    print(f'number of auwks loaded: {len(auwks0)}')
    dbrs = create_dbrs(auwks0)
    for i in dbrs:
        pseudomain(i)
        save_dbinfo(i, path1)
