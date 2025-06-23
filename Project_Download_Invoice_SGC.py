from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

logging.basicConfig(
    filename='log_tai_hoa_don.log',     
    filemode='a',                       
    level=logging.INFO,               
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


def open_chrome():#mở trình duyệt Chrome
    driver = webdriver.Chrome()
    driver.get("https://www.meinvoice.vn/tra-cuu")
    return driver

def xu_ly_nhap_ma(driver):
    
    try:
        #b1 xuất Xpath cho ô nhập mã
        Xpart_input_ma = '//*[@id="txtCode"]'
        input_element = driver.find_element(By.XPATH, Xpart_input_ma)
    
        #b2 Nhập mã vào ô input
        input_element.clear()
        input_element.send_keys("B1HEIRR8N0WP") 
    
        #b3 Nhấn nút tìm kiếm
        Xpart_button_tim_kiem = '//*[@id="btnSearchInvoice"]'
        button_element = driver.find_element(By.XPATH, Xpart_button_tim_kiem)
        button_element.click()
        #b4 ghi log vào file log_tai_hoa_don.log
        logging.info("Mã đã được nhập và tìm kiếm thành công.")
    except Exception as e:
        logging.error(" Lỗi khi nhập mã tra cứu: %s", str(e))
def xu_ly_download(driver):
    try:
        #b1 xuất xpart nút tải xuống hóa đơn
        Xpart_button_tai_xuong = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/span'
        button_element = driver.find_element(By.XPATH, Xpart_button_tai_xuong)
        time.sleep(5)
        #b2 click vào nút tải xuống hóa đơn
        button_element.click()
         #b3 xuất Xpath cho nút tải xuống PDF
        Xpart_button_tai_xuong_pdf = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[1]'
        button_element_pdf = driver.find_element(By.XPATH, Xpart_button_tai_xuong_pdf)
        #b4 click vào nút tải xuống PDF
        button_element_pdf.click()
        time.sleep(5)
        
        #b5 ghi log vào file log_tai_hoa_don.log
        logging.info("Tải xuống hóa đơn thành công.")
    except Exception as e:
        logging.error(" Lỗi khi tải xuống hóa đơn: %s", str(e))
    
def main():
    logging.info("Bắt đầu quá trình tải xuống hóa đơn.")
    # Mở trình duyệt Chrome
    driver = open_chrome()
    # Xử lý nhập mã
    xu_ly_nhap_ma(driver)
    #xu_ly_download(driver)
    xu_ly_download(driver)
    logging.info("Quá trình tải xuống hóa đơn kết thúc.")
    driver.quit()
    
main()

