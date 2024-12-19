import requests
import json
from datetime import datetime

import pandas as pd


def dosya_oku(path):
    file_path = path

    df = pd.read_excel(file_path)

    print("ilk satırlar")
    print(df.head())
    rows_to_drop = []
    for index, row in df.iterrows():
        vergi_no = row["Vergi Kimlik Numarası"]
        if pd.notna(vergi_no):
            print("Vergi kimlik numarası bulundu:")
            print(row)
            rows_to_drop.append(index)
    df = df.drop(rows_to_drop)
    return df
def veri_hazirla(veri):
    isim_soyisim = veri["Alıcı - Fatura Adresi"]
    isim = " ".join(isim_soyisim.split(" ")[:-1])
    soyisim = isim_soyisim.split(" ")[-1]
    urun = veri["Ürün Adı"].replace("one size", "")
    urun_toplam_fiyat = veri["Faturalanacak Tutar"]
    urun_adet = veri["Adet"]
    urun_kdvsiz_fiyat = urun_toplam_fiyat / 1.2
    urun_birim_kdvsiz_fiyat = urun_kdvsiz_fiyat / urun_adet
    kdv = urun_birim_kdvsiz_fiyat * 0.2 * urun_adet
    result = {
        "ad" : isim,
        "soyad" : soyisim,
        "adres" : veri["Fatura Adresi"],
        "urun_adi" : urun,
        "urun_adet" : int(urun_adet),
        "urun_toplam_fiyat" : round(urun_kdvsiz_fiyat + kdv,2),    
        "urun_toplam_kdvsiz_fiyat" : round(urun_kdvsiz_fiyat,2),
        "urun_birim_kdvsiz_fiyat" : round(urun_birim_kdvsiz_fiyat,2),
        "kdv_tutari" : round(kdv,2)
    }
    print(result)
    return result



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


def create_e_invoice(token, veri):
    uuid_url = "https://earsivportal.efatura.gov.tr/earsiv-services/dispatch"
    uuid_headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
    }
    uuid_data = {
        "cmd": "EARSIV_PORTAL_UUID_GETIR",
        "callid": "eceb8097ec8cc-7",
        "pageName": "RG_BASITFATURA",
        "token": token,
        "jp": json.dumps({})
    }

    uuid_response = requests.post(uuid_url, headers=uuid_headers, data=uuid_data, timeout=20)
    uuid = uuid_response.json()["data"]
    url = "https://earsivportal.efatura.gov.tr/earsiv-services/dispatch"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
    }
    data = {
        "cmd": "EARSIV_PORTAL_FATURA_OLUSTUR",
        "callid": "eceb8097ec8cc-9",
        "pageName": "RG_BASITFATURA",
        "token": token,
        "jp": json.dumps({
            "faturaUuid": uuid,
            "belgeNumarasi": "",
            "faturaTarihi": datetime.now().strftime("%d/%m/%Y"),
            "saat": datetime.now().strftime("%H:%M:%S"),
            "paraBirimi": "TRY",
            "dovzTLkur": "0",
            "faturaTipi": "SATIS",
            "hangiTip": "5000/30000",
            "vknTckn": "11111111111",
            "aliciUnvan": "",
            "aliciAdi": veri["ad"],
            "aliciSoyadi": veri["soyad"],
            "binaAdi": "",
            "binaNo": "",
            "kapiNo": "",
            "kasabaKoy": "",
            "vergiDairesi": "",
            "ulke": "Türkiye",
            "bulvarcaddesokak": veri["adres"],
            "irsaliyeNumarasi": "",
            "irsaliyeTarihi": "",
            "mahalleSemtIlce": "",
            "sehir": " ",
            "postaKodu": "",
            "tel": "",
            "fax": "",
            "eposta": "",
            "websitesi": "",
            "iadeTable": [],
            "vergiCesidi": " ",
            "malHizmetTable": [{
                "malHizmet": veri["urun_adi"],
                "miktar": 1,
                "birim": "C62",
                "birimFiyat": veri["urun_birim_kdvsiz_fiyat"],
                "fiyat": veri["urun_toplam_kdvsiz_fiyat"],
                "iskontoOrani": 0,
                "iskontoTutari": "0",
                "iskontoNedeni": "",
                "malHizmetTutari": veri["urun_toplam_kdvsiz_fiyat"],
                "kdvOrani": "20",
                "vergiOrani": 0,
                "kdvTutari": veri["kdv_tutari"],
                "vergininKdvTutari": "0",
                "ozelMatrahTutari": "0",
                "hesaplananotvtevkifatakatkisi": "0"
            }],
            "tip": "İskonto",
            "matrah": "226.67",
            "malhizmetToplamTutari": "226.67",
            "toplamIskonto": "0",
            "hesaplanankdv": veri["kdv_tutari"],
            "vergilerToplami": veri["kdv_tutari"],
            "vergilerDahilToplamTutar": veri["urun_toplam_fiyat"],
            "odenecekTutar": veri["urun_toplam_fiyat"],
            "not": "",
            "siparisNumarasi": "",
            "siparisTarihi": "",
            "fisNo": "",
            "fisTarihi": "",
            "fisSaati": " ",
            "fisTipi": " ",
            "zRaporNo": "",
            "okcSeriNo": ""
        })}
    print(data)
    response = requests.post(url, headers=headers, data=data, timeout=10)



username = "your_username"
password = "your_password"


if __name__ == "__main__":
    print("Dosya okunuyor...")
    veri = dosya_oku()
    print("Login yapılıyor...")
    token = login_efatura(username, password)["token"]
    print("Fatura oluşturuluyor...")
    for i in range(len(veri)):
        istek_verisi = veri_hazirla(veri.iloc[i])
        create_e_invoice(token, istek_verisi)
        print(f"{istek_verisi['ad']} {istek_verisi['soyad']}. fatura oluşturuldu.")

