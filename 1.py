import os
import time
import logging
import pandas as pd
import xmltodict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Thiết lập logging
logging.basicConfig(
    filename='log_dow_flt.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Mở Chrome với cấu hình tải về
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

# Base class cho handler
class BaseInvoiceHandler:
    def __init__(self, driver, ma, masothue, url):
        self.driver = driver
        self.ma = ma
        self.masothue = masothue
        self.url = url

    def process(self):
        self.driver.get(self.url)
        self.input_data()
        self.search()
        self.download()

    def input_data(self): pass
    def search(self): pass
    def download(self): pass

# Handler: meinvoice.vn
class MeInvoiceHandler(BaseInvoiceHandler):
    def input_data(self):
        input_element = self.driver.find_element(By.XPATH, '//*[@id="txtCode"]')
        input_element.clear()
        input_element.send_keys(self.ma)
        logging.info("Đã nhập mã meinvoice")

    def search(self):
        self.driver.find_element(By.XPATH, '//*[@id="btnSearchInvoice"]').click()
        time.sleep(5)
        logging.info("Tra cứu meinvoice thành công.")

    def download(self):
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/span').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[2]').click()
        time.sleep(3)
        logging.info("Tải meinvoice thành công.")

# Handler: tracuuhoadon.fpt
class FPTInvoiceHandler(BaseInvoiceHandler):
    def input_data(self):
        wait = WebDriverWait(self.driver, 10)
        input_mst = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[2]/div/input')))
        input_mst.clear()
        input_mst.send_keys(self.masothue)

        input_ma = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[3]/div/input')))
        input_ma.clear()
        input_ma.send_keys(self.ma)
        logging.info("Đã nhập mã FPT")

    def search(self):
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button').click()
        time.sleep(5)
        logging.info("Tra cứu FPT thành công.")

    def download(self):
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button').click()
        time.sleep(3)
        logging.info("FPT đã tải thành công.")

# Handler: van.ehoadon.vn
class EHoaDonHandler(BaseInvoiceHandler):
    def input_data(self):
        input_element = self.driver.find_element(By.XPATH, '//*[@id="txtInvoiceCode"]')
        input_element.clear()
        input_element.send_keys(self.ma)
        logging.info("Đã nhập mã ehoadon")

    def search(self):
        self.driver.find_element(By.XPATH, '//*[@id="Button1"]').click()
        time.sleep(5)
        logging.info("Tra cứu ehoadon thành công.")

    def download(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "frameViewInvoice")))
        iframe = self.driver.find_element(By.ID, "frameViewInvoice")
        self.driver.switch_to.frame(iframe)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "btnDownload")))
        self.driver.find_element(By.ID, "btnDownload").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "LinkDownXML").click()
        time.sleep(3)
        self.driver.switch_to.default_content()
        logging.info("Tải ehoadon thành công.")

# Factory để chọn đúng handler
class InvoiceHandlerFactory:
    handler_map = {
        "meinvoice": MeInvoiceHandler,
        "tracuuhoadon.fpt": FPTInvoiceHandler,
        "van.ehoadon.vn": EHoaDonHandler
    }

    @staticmethod
    def get_handler(driver, ma, masothue, url):
        for key, handler_class in InvoiceHandlerFactory.handler_map.items():
            if key in url:
                return handler_class(driver, ma, masothue, url)
        logging.warning(f"URL không được hỗ trợ: {url}")
        return None

# Hàm xuất Excel cuối cùng
def xu_ly_xuat_output(all_data):
    folder_path = "E:\\download"
    output_file = "output.xlsx"
    rows = []

    for record in all_data:
        ma = record['Mã tra cứu']
        masothue = record['Mã số thuế']
        url = record['URL']

        for filename in os.listdir(folder_path):
            if filename.endswith(".xml") and ma in filename:
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                    try:
                        data = xmltodict.parse(file.read())
                        if 'TDiep' in data:
                            hdon = data.get('TDiep', {}).get('DLieu', {}).get('HDon', {}).get('DLHDon', {})
                        elif 'HDon' in data:
                            hdon = data['HDon']['DLHDon']
                        else:
                            raise ValueError("Không tìm thấy cấu trúc HDon trong XML")
                        ttchung = hdon['TTChung']
                        nban = hdon['NDHDon']['NBan']
                        nmua = hdon['NDHDon']['NMua']

                        rows.append({
                            "Mã số thuế": masothue,
                            "Mã tra cứu": ma,
                            "URL": url,
                            "Số hóa đơn": ttchung.get('SHDon', ''),
                            "Đơn vị bán hàng": nban.get('Ten', ''),
                            "Mã số thuế bán": nban.get('MST', ''),
                            "Địa chỉ bán": nban.get('DChi', ''),
                            "Số tài khoản bán": nban.get('STKNHang', ''),
                            "Họ tên người mua hàng": nmua.get('Ten', ''),
                            "Địa chỉ mua": nmua.get('DChi', ''),
                            "Mã số thuế mua": nmua.get('MST', '')
                        })
                    except Exception as e:
                        logging.error(f"Lỗi khi xử lý {filename}: {e}")

    if rows:
        df_new = pd.DataFrame(rows)
        if os.path.exists(output_file):
            df_old = pd.read_excel(output_file)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_all = df_new
        df_all.to_excel(output_file, index=False, engine='openpyxl')
        logging.info(f"Đã ghi dữ liệu ra {output_file}.")

# Chương trình chính
def main():
    df = pd.read_excel("input.xlsx", dtype={"Mã số thuế": str})
    driver = open_chrome()
    all_data = []

    try:
        for _, row in df.iterrows():
            masothue = str(row['Mã số thuế']).strip()
            ma = str(row['Mã tra cứu']).strip()
            url = str(row['URL']).strip()

            if not ma or not url:
                continue
            if not masothue or masothue.lower() == 'nan':
                masothue = ""

            logging.info(f"Đang xử lý mã: {ma}")
            handler = InvoiceHandlerFactory.get_handler(driver, ma, masothue, url)
            if handler:
                try:
                    handler.process()
                    all_data.append({
                        "Mã số thuế": masothue,
                        "Mã tra cứu": ma,
                        "URL": url
                    })
                    time.sleep(2)
                except Exception as e:
                    logging.error(f"Lỗi khi xử lý mã {ma}: {e}")
    finally:
        driver.quit()
        logging.info("Kết thúc quá trình tải hóa đơn.")
        xu_ly_xuat_output(all_data)

if __name__ == "__main__":
    main()
