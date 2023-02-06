#!/usr/bin/env python
# coding: utf-8

# selenium   4.7.2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time
import argparse
import sys

parser = argparse.ArgumentParser(description='引数にLogin IDを指定せよ')
parser.add_argument('id', default="1", help='Set Login ID number for CAPF')
args = parser.parse_args()
id = "CA00" + args.id

# カメラ(マイク)の使用を許可しますか」ダイアログを回避
options = webdriver.ChromeOptions()
#options.add_argument("--headless")# オプションを指定
options.add_argument("--use-fake-ui-for-media-stream")# オプションを指定

# Chrome/Chromiumの立ち上げ
driver=webdriver.Chrome(options=options)

# ページ接続
driver.get('https://ignis2.ca-platform.org/login')

# キー入力
driver.find_element(By.XPATH, '//*[@id="name"]').send_keys(id)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(id)

### orin固有の設定
# input_device = "Poly Sync 20-M Mono"
input_device = "Poly Sync 20-M Multichannel"
output_device1 = "Poly Sync 20-M Analog Stereo"
output_device2 = "Poly Sync 20-M Digital Stereo (IEC958)"

# 待機して、audioデバイスを選択  input/output_deviceを選択状態にする
time.sleep(5)
# Select(driver.find_element(By.XPATH, '//*[@id="deviceIdMic"]')).select_by_index(1)
Select(driver.find_element(By.XPATH, '//*[@id="deviceIdMic"]')).select_by_visible_text(input_device)
try:
	Select(driver.find_element(By.XPATH, '//*[@id="deviceIdSpk"]')).select_by_visible_text(output_device1)
#except NotFoundOutputDeviceError as e:
except:
	Select(driver.find_element(By.XPATH, '//*[@id="deviceIdSpk"]')).select_by_visible_text(output_device2)

# ログインボタン入力
driver.find_element(By.XPATH, '//*[@name="btn"]').click()

# 接続を12時間維持
# time.sleep(43200)

# 接続を無限に設定
while True:
	try:
		time.sleep(10)
	except KeyboardInterrupt :
		print("コマンドの割り込みにより接続を終了します。")
		break

# クロームの終了処理
driver.close()
sys.exit(1)
