from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import pwinput
from traceback import print_exception
import sys


def excepthook(type_, value, traceback):
    print_exception(type_, value, traceback)
    print("\n\nHata oluştu.")
    input("Çıkış için ENTER.")
    try:
        driver.quit()
    except:
        pass
    exit()


sys.excepthook = excepthook

options = Options()
options.add_argument("--headless=new")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("start-maximized")

driver = webdriver.Chrome(options=options)

tc = str(input("TCKN: "))
sifre = pwinput.pwinput(prompt="E-Devlet şifresi: ")
msu_test = str(input("MSÜ sonuçları alınacaksa yes, alınmayacaksa boş: "))

print("Giriş deneniyor...")

driver.get("https://ais.osym.gov.tr/")
wait = WebDriverWait(driver, 30)
edevletgiris = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="edevletgirisbuton"]'))
)
driver.execute_script("arguments[0].click();", edevletgiris)

tcinput = wait.until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="tridField"]'))
)
tcinput.send_keys(tc)

sifreinput = wait.until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="egpField"]'))
)
sifreinput.send_keys(sifre)

edevletlogin = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[2]/input[4]'))
)
edevletlogin.click()

print("Giriş yapıldı.")

sonuclarim = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="anaMenu"]/ul[1]/li[3]/a'))
)
sonuclarim.click()

sonuc_tablo = wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, "sinav-surec"))
)

print("Sonuçlar bulundu, okunuyor...")

while True:
    sonuclar = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "tr")))
    sonuc_var = False
    for i in sonuclar:
        sonuc_tdleri = i.find_elements(By.TAG_NAME, "td")
        sinav = ""

        if "MSÜ" in i.text and msu_test.strip().lower() == "yes":
            sinav = "MSÜ"

        if "YKS" in i.text:
            sinav = "YKS"

        print(f"{sinav} sonucu bulundu ve kaydediliyor!")
        driver.execute_script(
            "arguments[0].click();", sonuc_tdleri[2].find_element(By.TAG_NAME, "a")
        )
        for i in driver.window_handles:
            driver.switch_to.window(i)
            time.sleep(3)
            driver.get_screenshot_as_file(
                f"{sinav}_sonuc_{random.randint(0, 1000)}.png"
            )
        print(f"{sinav} sonucu ekran görüntüsü olarak kaydedildi.")
        sonuc_var = True
        break

    if sonuc_var:
        break

    print("Mevcut sonuç yok. 30 saniye içinde yeniden kontrol edilecek.")
    time.sleep(30)
    driver.refresh()

driver.quit()
input("Sonuç bulundu ve kaydedildi. Çıkış için ENTER.")
