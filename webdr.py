from time import sleep
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

import globvar
import newacc


def config_webdr(ua):
    capabs = DesiredCapabilities.CHROME
    capabs["goog:loggingPrefs"] = {"performance": "ALL"}
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    # config Proxy
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = '185.80.202.69:59394'
    # #prox.socks_proxy = '185.80.202.69:59394'
    # prox.ssl_proxy = '185.80.202.69:59394'
    # prox.add_to_capabilities(capabs)
    # options.add_experimental_option("detach", True)     # -----------------------------------HOT FIX 350cs
    # options.add_argument("--incognito")     # -----------------------------------HOT FIX 350cs
    serv = Service(executable_path=globvar.PATH_CHRDR)
    options.add_argument(f'user-agent={ua}')
    driver = webdriver.Chrome(
        desired_capabilities=capabs,
        options=options,
        service=serv
    )
    return driver


# get neccessary info about ama acc
def amafirstgo(link, ua):  # ama instance
    driver = config_webdr(ua)
    driver.get(link)
    sleep(3)  # wait for the requests to take place
    mplog = logformp(driver)
    # cs page check
    # driver.switch_to.new_window('tab')
    # driver.get(f'{link+globvar.URLCUT_AMACS}')
    # sleep(3)
    driver.quit()
    return mplog


def hotcs350gourls(link, ua):
    driver = config_webdr(ua)
    driver.set_window_position(20, 20)
    driver.set_window_size(1582, 938)
    driver.get(link)
    driver.switch_to.new_window('tab')
    driver.get(f'{link}+{globvar.URLCUT_AMACS}')
    wk_login(driver)
    au_login(driver)
    # driver.switch_to.new_window('tab')
    # driver.get('https://accounts.aliexpress.com/user/organization/manage_person_profile.htm')
    # driver.switch_to.new_window('tab')
    # driver.get(globvar.URL_AU2WK)
    # driver.switch_to.new_window('tab')
    # driver.get('https://10minutemail.net/')
    # driver.switch_to.new_window('tab')
    # driver.get('https://temp-mail.org/en/')
    sleep(1200)


# wk login page
def wk_login(driver):
    driver.switch_to.new_window('tab')
    driver.get(globvar.URL_WK_LOGIN)


# au login page
def au_login(driver):
    driver.switch_to.new_window('tab')
    driver.get(globvar.URL_AULOGIN)


# log for ama main page
def logformp(driver):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    amadata = {
        'sns_c': 'none',  # ['data']['code']: 0 or 103
        'sns_ci': 'none',  # ['data']['codeInfo'] 'no sns binded' or 'success'
        'is_fr': True,  # ['data']['result'] isfrauduser set 'True' or 'False'
    }
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        a = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
        for line in a.items():
            if line[0] == 'body' and line[1]:
                jtemp = json.loads(line[1])  # line[1] body data
                # look for specific value at 'api' key; jtemp['data'] empty dictionary return 'False'
                if 'api' in jtemp.keys() and jtemp['data']:
                    match jtemp['api']:
                        # this api provides info if sns binded or not
                        case 'mtop.aliexpress.sns.visitor.registry.and.login':
                            amadata.update({'sns_c': jtemp['data']['code'],
                                            'sns_ci': jtemp['data']['codeInfo']})
                            break
                        # doesn't rely on au; only wk matters
                        case 'mtop.aliexpress.social.antifraud.isfrauduser':
                            amadata.update({'is_fr': jtemp['data']['result']})
                            break
    return amadata


def log_filter(log_):
    return (
        # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
    )


# ama casheveryday page
def ama_ce(driver, url0):
    url1 = url0 + '#/cash-everyday'
    driver.switch_to.new_window('tab')
    driver.get(url1)
    info = req_loggin(driver, 1)
    sleep(3)
    return info


def bind_autowk(auwk):  # auwk account
    driver = config_webdr(auwk.ua)
    au_dologin(driver, auwk)
    sleep(2)
    do_autowk(driver, auwk)
    # collect ama coupons
    #get_amacoups(driver, auwk)
    get_amacscoup(driver, auwk)
    # go to ama ce, find link
    # driver.get(f'{auwk.amal}{globvar.URLCUT_AMACE}')
    sleep(2)
    driver.quit()
    return True


def get_amacoups(driver, auwk):
    driver.switch_to.new_window('tab')
    driver.get(auwk.amal)
    sleep(5)
    # popup button
    claim_coups = driver.find_element(By.XPATH, '//*[@id="coupons-popup-collect"]/div')
    # get_coups = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[3]/div/div[2]/div[1]/div[3]/div/button/div')
    claim_coups.click()
    sleep(2)


def get_amacscoup(driver, auwk):
    driver.switch_to.new_window('tab')
    driver.get(auwk.amal + globvar.URLCUT_AMACS)
    sleep(5)
    claim_coup = driver.find_element(By.XPATH, '//*[@id="promoPage"]/section[2]/div[1]/div[2]/div/button/div/div/div')
    claim_coup.click()
    sleep(2)


def au_dologin(driver, auwk):
    driver.get(globvar.URL_AUSETCOOKS)
    driver.get(globvar.URL_AULOGIN)
    e_login = driver.find_element(By.ID, "fm-login-id")
    e_login.send_keys(auwk.aulog)
    e_pass = driver.find_element(By.ID, "fm-login-password")
    e_pass.send_keys(auwk.aupwd)
    sleep(1)
    e_submit = driver.find_element(By.CLASS_NAME, "fm-button")
    e_submit.click()
    sleep(4)
    auwk.autkn = log_foraulogin(driver)


def log_foraulogin(driver):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    for log in logs:
        try:
            if log['method'] == 'Network.requestWillBeSentExtraInfo' \
                    and '/tokenLogin.htm?aid=' in log['params']['headers'][':path']:
                return f"https://login.aliexpress.ru{log['params']['headers'][':path']}"
        except:
            return 'no_token'


# var xman_success={"person_data":{"login_id":"ru3101799367apbae","p_status":"enabled","first_name":"000000muna99999","email":"000000muna99999@mail.ru","last_name":"user","country":"RU"},"xlogin_urls":["https://login.alibaba.com/xman/tvs.htm?iframe_delete=true&switch=on&token=6e1ee8f91179466dbdd7a1bd7fd9466e&pid=4707494248"],"time_out":"30000","tbsessionToken":"6z_isezUJXoEi5S8E8hGvmg","switch":"on","forced_return":null,"proxy_cookies":["xman_mt1"],"cancel_icbu_tvs":true,"mutilDomainsLogin":["https://login.aliexpress.ru/tokenLogin.htm?aid=thznaQnUNY1Zfn1ttLkgBleD570JOmM0Pz6jCJsEgE7n2g6bC9uH%2BQ%3D%3D&sid=BA%2F%2BW6fnr4WX%2BTti9fbXPYnweyl2NpQMnjQmUxGqPCFg5Av9Q4LwArcs8AxzZU9ysOWORf6AsvM%3D"]}
def parse_autkn(tlist):
    for n in reversed(tlist):
        if 'tokenLogin.htm?aid=' in n:
            b = n.split('var xman_success=')[1]
            c = json.loads(b)
            d = c['mutilDomainsLogin']
            e = d[0]
            return e


def get_amaref(driver, auwk):
    driver.switch_to.new_window('tab')
    driver.get(auwk.amal)
    sleep(2)
    driver.switch_to.new_window('tab')
    driver.get(f'{auwk.amal}{globvar.URLCUT_AMACE}')
    sleep(4)
    auwk.amar = log_force(driver)
    if auwk.amar:
        return True
    return False


def log_force(driver):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    ama_ref = ''
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        a = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
        for line in a.items():
            if line[0] == 'body' and line[1]:
                jtemp = json.loads(line[1])  # line[1] body data
                if 'api' in jtemp.keys() and jtemp['data']:
                    if jtemp['api'] == 'mtop.aliexpress.social.cashout.create':
                        ama_ref = jtemp['data']['link']
                        return ama_ref
    return ama_ref


def au_dologin2(driver, auwk):
    # driver.get(globvar.URL_AUSETCOOKS)
    driver.get(globvar.URL_AULOGIN)
    sleep(0.3)
    e_login = driver.find_element(By.ID, "fm-login-id")
    e_login.send_keys(auwk.aulog)
    sleep(2)
    e_pass = driver.find_element(By.ID, "fm-login-password")
    e_pass.send_keys(auwk.aupwd)
    sleep(1)
    # try:
    #     driver.switch_to.frame(driver.find_element_by_id('baxia-dialog-content'))
    #     e_slider = driver.find_element_by_class_name("nc_iconfont.btn_slide")
    #     webdriver.ActionChains(driver).drag_and_drop_by_offset(e_slider, 301, 0).perform()
    #     #move_slowly(driver, e_slider)
    # finally:
    #     pass
    # sleep(15)
    e_submit = driver.find_element(By.CLASS_NAME, "fm-button")
    e_submit.click()
    # sleep(0.8)


def move_slowly(driver, e_slider):
    webdriver.ActionChains(driver).click_and_hold(e_slider).perform()
    intervals = 6
    interval_time = 1 / intervals
    for i in range(0, intervals):
        sleep(interval_time)
        webdriver.ActionChains(driver).move_by_offset(301 / intervals, 0).perform()


def do_autowk(driver, auwk):
    # driver.switch_to.new_window('tab')
    driver.get(globvar.URL_AU2WK)
    sleep(1)
    log_field = driver.find_element(By.XPATH, '//*[@id="login_submit"]/div/div/input[7]')
    log_field.send_keys(auwk.wklog)
    pwd_field = driver.find_element(By.XPATH, '//*[@id="login_submit"]/div/div/input[8]')
    pwd_field.send_keys(auwk.wkpwd)
    login_btn = driver.find_element(By.XPATH, '//*[@id="install_allow"]')
    login_btn.click()
    # <button class="flat_button fl_r button_indent" onclick="return allow(this);">Allow</button>
    try:
        allow_btn = driver.find_element(By.XPATH, '//*[@id="oauth_wrap_content"]/div[3]/div/div[1]/button[1]')
    except:
        sleep(10)
        allow_btn = driver.find_element(By.XPATH, '//*[@id="oauth_wrap_content"]/div[3]/div/div[1]/button[1]')
    allow_btn.click()


def test():
    auwk = newacc.DbRecord()
    auwk.aulog = 'test@port.com'
    auwk.aupwd = 'nhyhfgovw3ee0oop'
    driver = config_webdr(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36')
    # driver.get(globvar.URL_AUSETCOOKS)
    driver.get(globvar.URL_AULOGIN)
    e_login = driver.find_element(By.ID, "fm-login-id")
    e_login.send_keys(auwk.aulog)
    e_pass = driver.find_element(By.ID, "fm-login-password")
    e_pass.send_keys(auwk.aupwd)
    e_submit = driver.find_element(By.CLASS_NAME, "fm-button")
    e_submit.click()
    sleep(3)  # better make EC here
    logl = log_foraulogin(driver)
    print(logl)
    auwk.autkn = parse_autkn(logl)
    print(auwk.autkn)
    # auwk.wklog = '89523063824'
    # auwk.wkpwd = 'чашечкаводочкикаксмыслжизни'
    # do_autowk(driver, auwk)

# test()
