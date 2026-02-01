# GitHub Release Checklist

Bu dosya, CooPad v5.1'i GitHub'da yayınlamak için adım adım talimatlar içerir.

## 📋 Ön Hazırlık

### 1. Build'leri Oluştur

#### Linux Build (.deb)
```bash
cd /yol/to/v5.1
./scripts/build_deb.sh 1.0.0
```

Çıktı: `dist/coopad_1.0.0_amd64.deb`

#### Windows Build (.exe)
Windows bilgisayarında:
```batch
cd C:\yol\to\v5.1
scripts\build_windows.bat 1.0.0
```

veya PowerShell ile:
```powershell
cd C:\yol\to\v5.1
.\scripts\build_windows.ps1 1.0.0
```

Çıktı: `dist\coopad.exe`

### 2. Build'leri Test Et

#### Linux'ta Test
```bash
# Temiz bir sistem gerekli (veya Docker/VM kullan)
sudo dpkg -i dist/coopad_1.0.0_amd64.deb
coopad
# GUI açılmalı ve Host/Client/Settings sekmesi olmalı
```

#### Windows'ta Test
```
1. dist\coopad.exe dosyasını çift tıkla
2. GUI açılmalı
3. Tüm sekmeleri kontrol et (Host, Client, Settings)
4. Settings'te 30/60/90 Hz seçeneklerini kontrol et
```

## 🚀 GitHub Release Oluşturma

### Adım 1: GitHub'da Releases Sayfasına Git

1. https://github.com/uozer7050/v5.1 adresine git
2. Sağ tarafta "Releases" linkine tıkla
3. "Draft a new release" butonuna tıkla

### Adım 2: Tag ve Başlık Oluştur

**Tag version:** `v5.1.0`
- Format: `v` + MAJOR.MINOR.PATCH
- Bu sürüm için: `v5.1.0`

**Release title:** `CooPad v5.1 - Cross-Platform Remote Gamepad`

**Target:** `main` (veya aktif branch)

### Adım 3: Release Notes'u Ekle

RELEASE_NOTES.md dosyasının içeriğini kopyala ve "Describe this release" alanına yapıştır.

veya kısa versiyon:

```markdown
# CooPad v5.1 - Major Public Release

🎉 **First major public release ready for open source distribution!**

## 🆕 What's New

### Key Features
- ⚙️ **Settings Tab**: Configure UDP rates (30/60/90 Hz)
- 📊 **Network Telemetry**: Real-time latency, jitter, packet rate
- 🔒 **Security**: Packet validation & rate limiting
- 📦 **Easy Install**: .deb for Linux, .exe for Windows

### Distribution
- **Linux**: One-command install, automatic setup
- **Windows**: Single executable, no dependencies

## 📥 Downloads

- **Linux**: `coopad_1.0.0_amd64.deb` (~XX MB)
- **Windows**: `coopad.exe` (~XX MB)

## 🎮 Quick Start

### Linux
```bash
sudo dpkg -i coopad_1.0.0_amd64.deb
coopad
```

### Windows
1. Download `coopad.exe`
2. (Optional) Install ViGEm Bus Driver for Host mode
3. Double-click to run

## 📖 Documentation

- **README.md**: Complete English documentation
- **CHANGELOG_TR.md**: Detailed changes in Turkish
- **Platform Help**: Built-in help system in the app

## 🔗 Links

- [Full Release Notes](RELEASE_NOTES.md)
- [README](README.md)
- [Changelog (Turkish)](CHANGELOG_TR.md)

---

**Compatible with:** Windows 10/11, Ubuntu 20.04+, Debian 11+  
**Network:** LAN, VPN (ZeroTier, Tailscale, etc.)
```

### Adım 4: Dosyaları Yükle

"Attach binaries" bölümüne aşağıdaki dosyaları sürükle:

1. **coopad_1.0.0_amd64.deb** - Linux paketi
2. **coopad.exe** - Windows çalıştırılabilir dosyası

### Adım 5: Yayınla

1. "This is a pre-release" kutusunu **İŞARETLEME** (bu stable sürüm)
2. "Create discussion for this release" kutusunu **İŞARETLE** (topluluk geri bildirimi için)
3. "Publish release" butonuna tıkla

## 📢 Duyuru

Release yayınlandıktan sonra:

1. **Repository Description'ı Güncelle**
   - GitHub repo ana sayfasında "About" kısmına tıkla
   - Description: "Cross-platform remote gamepad over network - Play games with friends remotely"
   - Website: Release sayfasının linki
   - Topics ekle: `gamepad`, `gaming`, `network`, `cross-platform`, `python`, `tkinter`

2. **README Badge Ekle** (İsteğe bağlı)
   ```markdown
   ![Latest Release](https://img.shields.io/github/v/release/uozer7050/v5.1)
   ![Downloads](https://img.shields.io/github/downloads/uozer7050/v5.1/total)
   ![License](https://img.shields.io/github/license/uozer7050/v5.1)
   ```

3. **Sosyal Medya** (İsteğe bağlı)
   - Reddit r/gamedev, r/linux_gaming
   - Twitter/X
   - Discord sunucuları (eğer varsa)

## 📋 Kontrol Listesi

Release'den önce bu kontrolleri yap:

- [ ] Tüm testler geçiyor (`python3 validate_features.py`)
- [ ] README.md güncel ve doğru
- [ ] CHANGELOG_TR.md güncel
- [ ] Linux .deb paketi test edildi
- [ ] Windows .exe test edildi
- [ ] Sürüm numaraları tutarlı (5.1.0)
- [ ] GitHub'da tag oluşturuldu (v5.1.0)
- [ ] Build dosyaları hazır (dist/ klasöründe)
- [ ] Dosya boyutları makul (<50MB)
- [ ] Release notes hazır
- [ ] Screenshots/GIF'ler hazır (isteğe bağlı ama önerilen)

## 🎯 Release Sonrası

1. **İlk Kullanıcı Geri Bildirimi**
   - GitHub Issues'u takip et
   - Hızlı yanıt ver
   - Bug varsa acil düzelt

2. **Dokümantasyon Güncellemeleri**
   - Kullanıcılardan gelen sorulara göre README'yi iyileştir
   - FAQ bölümü ekle (gerekirse)

3. **Metrikler**
   - Download sayısını takip et
   - Issue/PR'ları takip et
   - Star sayısını takip et

## 💡 İpuçları

### İyi Release Notes
- Kısa ve öz başlangıç
- Madde işaretleriyle öne çıkan özellikler
- Görsel ekle (screenshot/GIF)
- Kolay bulunur download linkleri
- Hızlı başlangıç talimatları

### Dosya İsimlendirme
- ✅ `coopad_1.0.0_amd64.deb` (versiyonlu, platforma özel)
- ✅ `coopad.exe` (basit, Windows için)
- ❌ `build.deb` veya `output.exe` (belirsiz)

### Versiyon Numarası
```
MAJOR.MINOR.PATCH
  5  . 1  .  0

MAJOR: Büyük değişiklikler (breaking changes)
MINOR: Yeni özellikler (geriye uyumlu)
PATCH: Bug düzeltmeleri
```

## 🔄 Güncelleme Süreci

Gelecekteki güncellemeler için:

1. Kod değişikliklerini yap
2. Versiyon numarasını artır (ör: 5.1.0 → 5.1.1)
3. CHANGELOG_TR.md'yi güncelle
4. Build'leri oluştur
5. Test et
6. Yeni release oluştur
7. Önceki sürümlerle karşılaştırma yap

## 📞 Destek

Sorularınız için:
- GitHub Issues: Bug raporu ve özellik istekleri
- GitHub Discussions: Genel sorular
- Pull Requests: Kod katkıları

---

**Hazırlayan:** CooPad Development Team  
**Son Güncelleme:** 2026-02-01  
**Sürüm:** 5.1.0
