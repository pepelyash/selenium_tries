import datetime
import random

from selenium.webdriver.common.by import By

import globvar
import webdr
import time
import newacc
import rwrf
import csv
from time import sleep


def read_amals_txt(path):
    c = []
    with open(path, mode='r', encoding='utf-8') as f:
        a = f.read().splitlines()
        for b in a:
            if 'https://vk.aliexpress.ru/' in b:
                c.append(b)
    return c


def log_info_to_txt(_str, path):
    with open(path, mode='a', encoding='utf-8', newline='') as f:
        f.write(_str)


def launch_driver(uax):
    driver = webdr.config_webdr(uax)
    link0 = 'about:blank'
    driver.get(link0)
    return driver


def perform_action(driver, ama, num):
    driver.get(f'{ama}#/alibox')
    driver.implicitly_wait(2)
    try:
        play_btn = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/section/div[1]/div/div/div/div/div[3]/div/button')
        play_btn.click()
        driver.implicitly_wait(2)
        if driver.current_url == f'{ama}#/alibox-game':
            for nk in range(0, 5):
                if num > 6:
                    num = 1
                try:
                    #num = random.randint(1, 6)
                    num_btn = driver.find_element(By.XPATH, f'/html/body/div/div/div[1]/section/div[1]/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[{num}]')
                    num_btn.click()
                    num += 1
                    sleep(2)
                    try:
                        open_btn = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/section/div[1]/div/div/div/div/div[3]/div/div/div[2]/button/div/div')
                        open_btn.click()
                        sleep(1)
                        driver.refresh()
                        sleep(2)
                    except:
                        print('couldnot press open_btn')
                except:
                    print('couldnot press num_btn')
        return True
    except:
        return False


def get_coups_info(driver, ama):
    driver.get(f'{ama}#/my-account-coupons')
    sleep(2)
    # when there are two coupon types and more than 1 of the same type
    # /html/body/div/div/div[1]/section/div[1]/div/div/div/div/div[3]/div/div[1]/div[1]/div[2]/div[1]/div[1]    # new
    # /html/body/div/div/div[1]/section/div[1]/div/div/div/div/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[1]    # new
    # when there are two coupon types and only 1 of the same type
    # /html/body/div/div/div[1]/section/div[1]/div/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div/div[1]   # old
    # when it's only one coupon type then:
    # /html/body/div/div/div[1]/section/div[1]/div/div/div/div/div[3]/div/div[1]/div/div[2]/div[2]/div[1]   #
    xpath_old = '/html/body/div/div/div[1]/section/div[1]/div/div/div/div/div[3]/div/div[1]/div'  # for old coups
    old_coups = get_coups(driver, xpath_old)
    coups_text = parse_coups(old_coups)
    return coups_text


def get_coups(driver, xp):
    try:
        coups = driver.find_elements(By.XPATH, xp)
        return coups
    except:
        print('locating coups fail')
        return []


def parse_coups(coups):
    coups_text = []
    for i in coups:
        coups_text.append(i.text)
    return coups_text


# def preudomain():
#     path0 = 'resources/amals_to_workout.txt'
#     curdate = datetime.datetime.now().strftime("%Y-%m-%d")
#     path1 = f'resources/ama_logs/coups_by_{curdate}.txt'
#     amaslist = read_amals_txt(path0)
#     print(f'amalinks read: {len(amaslist)}')
#     n0 = 0
#     n1 = 0
#     for amaa in amaslist:
#         ua0 = globvar.rndm_ua(0)
#         driver0 = launch_driver(ua0)
#         res_str = ''
#         if perform_action(driver0, amaa):
#             res_str = 'alibox played successfully\n'
#             n1 += 1
#         else:
#             res_str = 'alibox wasnot played\n'
#             n0 += 1
#             print(f'{amaa}\nfailed')
#         # go to coupons and try parse its values
#         coups_info = get_coups_info(driver0, amaa)
#         driver0.quit()
#         for n in coups_info:
#             res_str += f'{n}\n'
#         log_info_to_txt(f'{amaa}\n{res_str}', path1)
#     print(f'amas with alibox played: {n1}')
#     print(f'amas with alibox wasnot played: {n0}')


if __name__ == '__main__':
    path0 = 'resources/amals_to_workout.txt'
    curdate = datetime.datetime.now().strftime("%Y-%m-%d")
    path1 = f'resources/ama_logs/coups_by_{curdate}.txt'
    amaslist = read_amals_txt(path0)
    print(f'amalinks read: {len(amaslist)}')
    n0 = 0
    n1 = 0
    ndec = 0
    numbtn = 1
    numbtn_max = 6
    # ua0 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    for amaa in amaslist:
        if numbtn > numbtn_max:
            numbtn = 1
        ua0 = globvar.rndm_ua(0)
        driver0 = launch_driver(ua0)
        res_str = ''
        if perform_action(driver0, amaa, numbtn):
            res_str = 'alibox played successfully\n'
            n1 += 1
            numbtn += 1
        else:
            res_str = 'alibox wasnot played\n'
            n0 += 1
            print(f'{amaa}\nfailed')
        # go to coupons and try parse its values
        coups_info = get_coups_info(driver0, amaa)
        driver0.quit()
        for n in coups_info:
            res_str += f'{n}\n'
        if 'декабря' in res_str:
            ndec += 1
            print(f'{amaa}\n{res_str}')
        log_info_to_txt(f'{amaa}\n{res_str}', path1)
    print(f'amas with alibox played: {n1}')
    print(f'amas with alibox wasnot played: {n0}')
    print(f'number of decembers: {ndec}')
