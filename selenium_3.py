from selenium import webdriver
from selenium.webdriver.common.by import By
import pytesseract
from PIL import Image
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import base64
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def open_chrome():
    driver = webdriver.Chrome()
    driver.get("https://www.csgt.vn/")
    return driver

def xu_ly_bien_kiem_soat(driver, str_bien_so):
    xpart_bien_kiem_soat = '//*[@id="formBSX"]/div[2]/div[1]/input'
    elemint_bien_kiem_soat = driver.find_element(By.XPATH, xpart_bien_kiem_soat)
    elemint_bien_kiem_soat.send_keys(str_bien_so)
    print()
   
   
   
def xu_ly_loai_phuong_tien(driver, loai_phuong_tien):
    xpart_option_loai_phuong_tien = '//*[@id="formBSX"]/div[2]/div[2]/select'
    elemint_loai_phuong_tien = driver.find_element(By.XPATH, xpart_option_loai_phuong_tien)
    elemint_loai_phuong_tien.click()
    
    xpart_option_loai_phuong_tien = '//*[@id="formBSX"]/div[2]/div[2]/select/option'
    options_loai_phuong_tien = driver.find_elements(By.XPATH, xpart_option_loai_phuong_tien)
    for option in options_loai_phuong_tien:
        str_option = str(option.text).strip()
        if str_option == loai_phuong_tien:
            option.click()
            time.sleep(3)
            break 


def xu_ly_capcha(driver):
    #1 save capcha image
    capcha_element = driver.find_element(By.ID, "imgCaptcha")
    src = capcha_element.get_attribute("src")
    if "base64," in src:
        base64_data = src.split(",")[1]
        with open("captcha.png", "wb") as f:
            f.write(base64.b64decode(base64_data))
    else:
        capcha_element.screenshot("captcha.png")
    #2 xử dụng thư viện để trích xuất sang text
    #   ví dụ: pytesseract
    image = Image.open("captcha.png")
    captcha_text = pytesseract.image_to_string(image, config='--psm 8 --oem 3').strip()
    #3 nhập capcha vào ô input
    xpart_input_captcha = '//*[@id="formBSX"]/div[2]/div[3]/div/input' 
    input_element = driver.find_element(By.XPATH, xpart_input_captcha)  
    input_element.clear()
    input_element.send_keys(captcha_text)
    print(f"[CAPTCHA]: {captcha_text}")
    if "base64," in src:
        print("[CAPTCHA]: Ảnh ở định dạng base64")
    else:
        print("[CAPTCHA]: Ảnh từ URL (không phải base64)")

    #4 click vào nút tra cứu
    #đẩy qua def tra cứu phạt nguội
    
    
def tra_cuu_phat_nguoi(driver, bien_so, loai_phuong_tien):
    driver.get("https://www.csgt.vn/")  # Tải lại trang mỗi lần
    time.sleep(2)

    xu_ly_bien_kiem_soat(driver, bien_so)
    xu_ly_loai_phuong_tien(driver, loai_phuong_tien)
    xu_ly_capcha(driver)

    tra_cuu_button_xpath = '//*[@id="formBSX"]/div[2]/input[1]'
    driver.find_element(By.XPATH, tra_cuu_button_xpath).click()

    try:
        ketqua_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ketqua"]'))
        )
        print(f"[Kết quả - {loai_phuong_tien}]:{ketqua_element.text}")
    except:
        print(f"[Không có kết quả - {loai_phuong_tien}]: CAPTCHA sai hoặc không có vi phạm.")
def main():
    driver = open_chrome()
    
    bien_so = "29A12345" 

    for loai_phuong_tien in ["Ô tô", "Xe máy", "Xe đạp điện"]:
        tra_cuu_phat_nguoi(driver, bien_so, loai_phuong_tien)
        time.sleep(2)

    driver.quit()

main()
