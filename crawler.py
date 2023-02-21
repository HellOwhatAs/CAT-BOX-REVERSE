from seleniumwire.webdriver import Edge
from selenium.webdriver.common.by import By
import time, os, json

driver = Edge()
data = {}

def response_interceptor(request, response):
    t = response.headers['Content-Type']
    if t and 'image' in t:
        data[request.url] = response.body
            
driver.response_interceptor = response_interceptor

def get_cpt(cpt_url: str, cpt_name: str):
    driver.get(cpt_url)
    if not os.path.exists(cpt_name): os.makedirs(cpt_name)
    else: return len(os.listdir(cpt_name))
    for idx, elem in enumerate(driver.find_elements(By.CSS_SELECTOR, 'article > div > div > div > div > div > div > img')):
        while not "lazyloaded" in elem.get_attribute("class"):
            if "error" in elem.get_attribute("class"):
                data[elem.get_attribute("src")] = b''
                break
            driver.execute_script("arguments[0].scrollIntoView();", elem)
            time.sleep(1)
            print(elem.get_attribute("src"))
        with open(f"{cpt_name}/{idx}.png", "wb") as f:
            f.write(data[elem.get_attribute("src")])
    data.clear()
    return idx + 1

driver.get('https://cn.godamanga.com/chapterlist/maoxiangfanzhuan-shenman/')
catalog = [(cpt.get_attribute("href"), driver.execute_script("return arguments[0].firstChild.textContent;", cpt).strip()) for cpt in driver.find_elements(By.CSS_SELECTOR, "article > div > div.wp-block-stackable-columns > div > div > div > div > div.chapter-content-listing > div > ul > a")]
data.clear()

cpt_img_count = []
cpt_names = []
for cpt_url, cpt_name in reversed(catalog):
    cpt_img_count.append(get_cpt(cpt_url, cpt_name))
    cpt_names.append(cpt_name)

driver.quit()

with open("data.js", "w", encoding='utf-8') as f:
    f.write(f"var data={json.dumps(cpt_img_count, ensure_ascii=False)};\nvar charpter={json.dumps(cpt_names, ensure_ascii=False)};")