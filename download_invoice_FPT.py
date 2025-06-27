from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import pandas as pd
from selenium.webdriver.chrome.options import Options
import os
import xml.etree.ElementTree as ET

logging.basicConfig(
    filename='log_dow_flt.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def open_chrome(download_dir="E:\\download"):
    options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "profile.default_content_settings.popups": 0,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=options)

def xu_ly_du_lieu_input(driver, ma, masothue, url):
    try:
        driver.get(url)
        if "meinvoice" in url:
            input_element = driver.find_element(By.XPATH, '//*[@id="txtCode"]')
            input_element.clear()
            input_element.send_keys(ma)

        elif "tracuuhoadon.fpt" in url:
            wait = WebDriverWait(driver, 10)
            input_mst = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[2]/div/input')))
            input_mst.clear()
            input_mst.send_keys(masothue)

            input_ma = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[3]/div/input')))
            input_ma.clear()
            input_ma.send_keys(ma)

        elif "van.ehoadon.vn" in url:
            input_element = driver.find_element(By.XPATH, '//*[@id="txtInvoiceCode"]')
            input_element.clear()
            input_element.send_keys(ma)

        else:
            logging.warning(f"URL không hỗ trợ: {url}")
            return False
        logging.info("Mã đã được nhập.")
    except Exception as e:
        logging.error("Lỗi khi nhập mã tra cứu: %s", str(e))

def xu_ly_tra_cuu(driver, url):
    try:
        if "meinvoice" in url:
            driver.find_element(By.XPATH, '//*[@id="btnSearchInvoice"]').click()
            time.sleep(5)
        elif "tracuuhoadon.fpt" in url:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button').click()
            time.sleep(5)
        elif "van.ehoadon.vn" in url:
            driver.find_element(By.XPATH, '//*[@id="Button1"]').click()
            time.sleep(5)
        else:
            logging.warning(f"URL không hỗ trợ: {url}")
            return False
        logging.info("Tra cứu thành công.")
    except Exception as e:
        logging.error("Tra cứu không thành công")

def xu_ly_download(driver, url):
    try:
        if "meinvoice" in url:
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/span').click()
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[2]').click()

        elif "tracuuhoadon.fpt" in url:
                # Click nút tải
                driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button').click()
                time.sleep(3)

        elif "van.ehoadon.vn" in url:
                # Đợi iframe chứa PDF
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "frameViewInvoice"))
                )
                iframe = driver.find_element(By.ID, "frameViewInvoice")
                driver.switch_to.frame(iframe)  # Chuyển vào iframe
                
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btnDownload"))
                )
                download_button = driver.find_element(By.ID, "btnDownload")
                download_button.click()
                time.sleep(3)
                download_button_pdf = driver.find_element(By.ID, "LinkDownXML")
                download_button_pdf.click()
                time.sleep(3)

                driver.switch_to.default_content()  # Quay lại nội dung chính

        else:
            logging.warning(f"URL không hỗ trợ: {url}")
            return False

        logging.info("Tải xuống hóa đơn thành công.")
    except Exception as e:
        logging.error("Lỗi khi tải xuống hóa đơn")
        
def xu_ly_xuat_output(ma, masothue, url, output_file="output.xlsx", download_dir="E:\\download"):
    latest_file = None
    latest_time = 0

    for file in os.listdir(download_dir):
        if file.endswith(".xml"):
            path = os.path.join(download_dir, file)
            t = os.path.getmtime(path)
            if t > latest_time:
                latest_file = path
                latest_time = t

    if latest_file:
        try:
            tree = ET.parse(latest_file)
            root = tree.getroot()

            def safe_find(xpath):
                e = root.find(xpath)
                return e.text.strip() if e is not None and e.text else ""

            data = {
                "Mã số thuế": masothue,
                "Mã tra cứu": ma,
                "URL": url,
                "Số hóa đơn": safe_find(".//TTChung/SHDon"),
                "Đơn vị bán hàng": safe_find(".//NDHDon/NBan/Ten"),
                "Mã số thuế bán": safe_find(".//NDHDon/NBan/MST"),
                "Địa chỉ bán": safe_find(".//NDHDon/NBan/DChi"),
                "Số tài khoản bán": safe_find(".//NDHDon/NBan/STKNHang"),
                "Họ tên người mua hàng": safe_find(".//NDHDon/NMua/Ten"),
                "Địa chỉ mua": safe_find(".//NDHDon/NMua/DChi"),
                "Mã số thuế mua": safe_find(".//NDHDon/NMua/MST")
            }

        except Exception as e:
            logging.error(f"Lỗi khi đọc XML {latest_file}: {e}")
            data = {
                "Mã số thuế": masothue,
                "Mã tra cứu": ma,
                "URL": url,
                "Lỗi": f"Lỗi đọc XML: {e}"
            }
    else:
        data = {
            "Mã số thuế": masothue,
            "Mã tra cứu": ma,
            "URL": url,
            "Lỗi": "Không tải được XML"
        }

    try:
        df = pd.read_excel(output_file) if os.path.exists(output_file) else pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_excel(output_file, index=False)
    except Exception as e:
        logging.error(f"Lỗi khi ghi output: {e}")


    
    
def main():
    logging.info("Bắt đầu quá trình tải xuống hóa đơn.")
    df = pd.read_excel("input.xlsx", dtype={"Mã số thuế": str})
    driver = open_chrome()
    download_dir = "E:\\download"
    output_data = []

    try:
        for index, row in df.iterrows():
            masothue = str(row['Mã số thuế']).strip()
            ma = str(row['Mã tra cứu']).strip()
            url = str(row['URL']).strip()

            if not ma or not url:
                continue
            if not masothue or masothue.lower() == 'nan':
                masothue = ""

            logging.info(f"Đang xử lý mã: {ma}")
            xu_ly_du_lieu_input(driver, ma, masothue, url)
            xu_ly_tra_cuu(driver, url)
            xu_ly_download(driver, url)
            time.sleep(2)

            # Ghi dữ liệu sau mỗi lần xử lý
            xu_ly_xuat_output(ma, masothue, url)

    finally:
        driver.quit()
        logging.info("Quá trình tải xuống kết thúc.")

main()
