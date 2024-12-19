# E-Fatura Otomasyonu

Bu proje, bir Excel dosyasından alınan sipariş bilgilerini kullanarak e-faturalar oluşturmak için bir otomasyon scripti sağlar.

## Gereksinimler

- Python 3.x
- Pandas
- Requests

## Kurulum

Gereksinimleri yüklemek için aşağıdaki komutu çalıştırın:
```bash
pip install pandas requests
```
## Kullanım
## 1- Excel Dosyasını Hazırlayın:

Excel dosyanızın belirlediğniz path'inde olduğundan emin olun.
Dosya sütunları: "Vergi Kimlik Numarası", "Alıcı - Fatura Adresi", "Ürün Adı", "Faturalanacak Tutar", "Adet", "Fatura Adresi".
Kodun İçindeki Kullanıcı Bilgilerini Güncelleyin:

username ve password değişkenlerini e-fatura portalı kullanıcı bilgilerinizle güncelleyin.
## 2- Scripti Çalıştırın:
```bash
python main.py
```
## Fonksiyonlar
dosya_oku(path): Excel dosyasını okur ve vergi kimlik numarası bulunan satırları çıkarır.
veri_hazirla(veri): Fatura verilerini hazırlar.
login_efatura(username, password): E-fatura portalına giriş yapar ve token döner.
create_e_invoice(token, veri): E-fatura oluşturur.
## Örnek Çıktı
```bash
plaintext
Dosya okunuyor...
ilk satırlar
   Vergi Kimlik Numarası Alıcı - Fatura Adresi  ...  Adet      Fatura Adresi
0                 1234567      Ali Veli          ...     1   Adres 1
1                 NaN           Ahmet Yılmaz      ...     2   Adres 2
...
Login yapılıyor...
Login başarılı.
Fatura oluşturuluyor...
{'ad': 'Ali', 'soyad': 'Veli', 'adres': 'Adres 1', ...}
Ali Veli. fatura oluşturuldu.
{'ad': 'Ahmet', 'soyad': 'Yılmaz', 'adres': 'Adres 2', ...}
Ahmet Yılmaz. fatura oluşturuldu.
```

