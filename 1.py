import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET
from jinja2 import Template
from weasyprint import HTML
import time
import logging
import pandas as pd
from selenium.webdriver.chrome.options import Options

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
        "plugins.always_open_pdf_externally": True,
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
        logging.error("Tra cứu không thành công: %s", str(e))

def xu_ly_download(driver, url):
    try:
        if "meinvoice" in url:
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/span').click()
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[1]').click()

        elif "tracuuhoadon.fpt" in url:
            try:
                download_dir = "E:\\download"

                # Click nút tải
                driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button').click()
                time.sleep(3)

                # Tìm file XML mới nhất
                import glob
                xml_files = glob.glob(os.path.join(download_dir, "*.xml"))
                if not xml_files:
                    print("Không tìm thấy file XML đã tải.")
                    exit()
                xml_file = max(xml_files, key=os.path.getctime)

                # Parse XML
                tree = ET.parse(xml_file)
                root = tree.getroot()

                h = root.find(".//DLHDon")
                tt = h.find("TTChung")
                nlap = tt.findtext("NLap", "")

                nb = root.find(".//NDHDon/NBan")
                nm = root.find(".//NDHDon/NMua")
                ten_ban = nb.findtext("Ten", "")
                ten_mua = nm.findtext("Ten", "")

                items_html = ""
                for hv in root.findall(".//NDHDon/DSHHDVu/HHDVu"):
                    ten = hv.findtext("THHDVu", "")
                    sl = hv.findtext("SLuong", "")
                    dg = hv.findtext("DGia", "")
                    ttien = hv.findtext("ThTien", "")
                    items_html += f"<tr><td>{ten}</td><td>{sl}</td><td>{dg}</td><td>{ttien}</td></tr>"

                tt_toan = root.find(".//TToan")
                tong_chu = tt_toan.findtext("TgTTTBChu", "")

                html_tmpl = """
                <html><body>
                <h2>HÓA ĐƠN ĐIỆN TỬ</h2>
                <p><b>Người bán:</b> {{ ten_ban }}</p>
                <p><b>Người mua:</b> {{ ten_mua }}</p>
                <p><b>Ngày lập:</b> {{ nlap }}</p>
                <table border="1" cellpadding="5" cellspacing="0">
                <tr><th>Sản phẩm</th><th>SL</th><th>Đơn giá</th><th>Thành tiền</th></tr>
                {{ items|safe }}
                </table>
                <p><b>Tổng bằng chữ:</b> {{ tong_chu }}</p>
                </body></html>
                """

                html = Template(html_tmpl).render(
                    ten_ban=ten_ban, ten_mua=ten_mua,
                    nlap=nlap, items=items_html, tong_chu=tong_chu
                )

                # Tên PDF theo file XML
                pdf_name = os.path.splitext(os.path.basename(xml_file))[0] + ".pdf"
                pdf_path = os.path.join(download_dir, pdf_name)
                HTML(string=html).write_pdf(pdf_path)
                print("✅ Đã tạo PDF:", pdf_path)

            except Exception as e:
                import traceback
                logging.error("FPT tải PDF lỗi: %s", traceback.format_exc())


        elif "van.ehoadon.vn" in url:
            try:
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
                download_button_pdf = driver.find_element(By.ID, "LinkDownPDF")
                download_button_pdf.click()
                time.sleep(3)

                driver.switch_to.default_content()  # Quay lại nội dung chính
            except Exception as e:
                logging.error("Lỗi khi tải xuống hóa đơn từ van.ehoadon.vn: %s", str(e))

        else:
            logging.warning(f"URL không hỗ trợ: {url}")
            return False

        logging.info("Tải xuống hóa đơn thành công.")
    except Exception as e:
        logging.error("Lỗi khi tải xuống hóa đơn: %s", str(e))

def main():
    logging.info("Bắt đầu quá trình tải xuống hóa đơn.")
    df = pd.read_excel("input.xlsx", dtype={"Mã số thuế": str})
    driver = open_chrome()

    try:
        for index, row in df.iterrows():
            masothue = str(row['Mã số thuế']).strip()
            ma = str(row['Mã tra cứu']).strip()
            url = str(row['URL']).strip()

            if not ma or not url:
                continue

            if not masothue or masothue.lower() == 'nan':
                masothue = ""

            logging.info(f"Đang tra cứu mã: {ma}")
            xu_ly_du_lieu_input(driver, ma, masothue, url)
            xu_ly_tra_cuu(driver, url)
            xu_ly_download(driver, url)
            time.sleep(5)

    finally:
        driver.quit()
        logging.info("Quá trình tải xuống hóa đơn kết thúc.")

if __name__ == "__main__":
    main()
