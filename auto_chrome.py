#!/usr/bin/env python
# coding: utf-8

#ライブラリ読み込み
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse

parser = argparse.ArgumentParser(description='引数にLogin IDを指定せよ')
parser.add_argument('id', default="1", help='Set Login ID number for CAPF')
args = parser.parse_args()
id = "CA00" + args.id

# カメラ(マイク)の使用を許可しますか」ダイアログを回避
options = webdriver.ChromeOptions()
options.add_argument("--use-fake-ui-for-media-stream")# オプションを指定

# Chrome/Chromiumの立ち上げ
driver=webdriver.Chrome(options=options)

# ページ接続
driver.get('https://ignis2.ca-platform.org/login')

# キー入力
# driver.find_element_by_xpath('//*[@id="name"]').send_keys("CA001")
driver.find_element(By.XPATH, '//*[@id="name"]').send_keys(id)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(id)

# ログインボタン入力
driver.find_element(By.XPATH, '//*[@name="btn"]').click()

# 接続を12時間維持
time.sleep(43200)

# クロームの終了処理
driver.close()