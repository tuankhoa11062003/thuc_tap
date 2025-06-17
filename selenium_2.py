from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

options = Options()
options.add_argument('--headless') 
driver = webdriver.Chrome(service=Service(), options=options)

base_url = "https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep"
driver.get(base_url)
time.sleep(3)

sheets = {}

page_num = 1
while True:
    print(f"Đang thu thập trang {page_num}...")
    rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
    
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 4:
            ten_dn = cols[1].text.strip()
            mst = cols[2].text.strip()
            ngay_cap = cols[3].text.strip()
            data.append({
                "Tên Doanh Nghiệp": ten_dn,
                "Mã Số Thuế": mst,
                "Ngày Cấp": ngay_cap
            })

    sheets[f"Trang_{page_num}"] = pd.DataFrame(data)

    try:
        next_button = driver.find_element(By.XPATH, '//a[contains(text(),"Sau")]')
        if 'disabled' in next_button.get_attribute('class'):
            break
        else:
            next_button.click()
            page_num += 1
            time.sleep(2)
    except:
        break

driver.quit()

with pd.ExcelWriter("ma_so_thue_doanh_nghiep.xlsx", engine='openpyxl') as writer:
    for sheet_name, df in sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)
