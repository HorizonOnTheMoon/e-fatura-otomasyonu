import requests
import json
import pandas as pd




def login_efatura(username, password):
    url = "https://earsivportal.efatura.gov.tr/earsiv-services/assos-login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
    }
    data = {
        "assoscmd": "anologin",
        "rtype": "json",
        "userid": username,
        "sifre": password,
        "sifre2": password,
        "parola": "1"
    }

    response = requests.post(url, headers=headers, data=data, timeout=10)

    if response.status_code == 200:
        print("Login başarılı.")
        return response.json()
    else:    
        print("Login başarısız. Hata kodu:", response.status_code)

def get_files(token):
    url = "https://earsivportal.efatura.gov.tr/earsiv-services/dispatch"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
    }
    data = {
        "cmd": "EARSIV_PORTAL_TASLAKLARI_GETIR",
        "callid": "14224ee2a3f7b-7",
        "pageName": "RG_BASITTASLAKLAR",
        "token": token,
        "jp": json.dumps({
            "baslangic": "04/12/2024",
            "bitis": "04/12/2024",
            "hangiTip": "5000/30000"
        })
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Dosyalar başarıyla alındı:")
        return response.json()
    else:
        print("Dosya alma başarısız. Hata kodu:", response.status_code)

def download_file(token,ettn,isim):
    url = f"https://earsivportal.efatura.gov.tr/earsiv-services/download?token={token}&ettn={ettn}&belgeTip=FATURA&onayDurumu=Onayland%C4%B1&cmd=EARSIV_PORTAL_BELGE_INDIR&"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        PATH = "path"
        zip_file_path = f"{PATH}{ettn}.zip"  # İndirilecek zip dosyasının yolu
        with open(zip_file_path, "wb") as f:
            f.write(response.content)
        print(f"{ettn} numaralı zip dosyası başarıyla {zip_file_path} konumuna indirildi.")

        # Zip dosyasını aç
        import zipfile
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(f"{PATH}{ettn}")  # Zip içeriğini çıkart

        # Çıkarılan HTML dosyasını aç
        import os
        html_files = [f for f in os.listdir(f"{PATH}{ettn}") if f.endswith('.html')]
        if html_files:
            html_file_path = os.path.join(f"{PATH}{ettn}", html_files[0])
            import shutil
            new_html_file_path = f"{PATH}htmls/{isim}.html"
            shutil.move(html_file_path, new_html_file_path)
            print(f"{html_file_path} dosyası htmls klasörüne taşındı ve adı {isim}.html olarak değiştirildi.")
        else:
            print("HTML dosyası bulunamadı.")
    else:
        print("Dosya indirme başarısız. Hata kodu:", response.status_code)

username = "Your Username"
password = "Your Password"


if __name__ == "__main__":
    token = login_efatura(username, password)["token"]  
    data = get_files(token)["data"]
    for veri in data:
        download_file(token, veri["ettn"], veri["aliciUnvanAdSoyad"])
