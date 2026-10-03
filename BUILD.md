# Uygulamayı hazırlama

## Windows'ta EXE oluşturma

Python 3.12 veya üzerini kurun. PowerShell'i proje klasöründe açıp aşağıdaki komutları çalıştırın:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name "PosterPrint-Pro" --icon "app_icon.ico" --add-data "app_icon.png;." poster_app.py
```

Hazırlanan tek dosyalı uygulama `dist\PosterPrint-Pro.exe` konumunda bulunur. Logo bu EXE'nin içine eklenir; ayrıca bir logo dosyası dağıtmanız gerekmez.

## GitHub Releases üzerinden otomatik oluşturma

`.github\workflows\release.yml` iş akışı, `v` ile başlayan bir Git etiketi GitHub'a gönderildiğinde Windows EXE dosyasını oluşturur ve aynı etiket için bir Release olarak yayımlar.

Örnek:

```powershell
git tag v1.0.0
git push origin v1.0.0
```

İş akışının tamamlanmasının ardından EXE dosyası, GitHub deposunun **Releases** bölümünde indirilebilir.

## Lisans notu

`LICENSE`, projeye ait kod için MIT lisansını belirtir. Pillow, PyQt6 ve Qt gibi bağımlılıklar kendi lisanslarına tabidir; oluşturulan EXE'yi dağıtmadan önce ilgili lisans koşullarını ve gerekli bildirimleri ayrıca kontrol edin.
