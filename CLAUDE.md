# Cribl Telemetry Interceptor - Proje Özeti

Bu proje Cribl'in cdn.cribl.io adresine gönderdiği telemetry verilerini yakalamak ve analiz etmek için oluşturuldu.

## 🎯 Amaç

1. Cribl'in gönderdiği telemetry trafiğini yakalamak
2. Mock server oluşturup telemetry endpoint'ini simüle etmek
3. DNS redirect ile Cribl'i mock server'a yönlendirmek

## 📊 Keşfedilen Telemetry Formatı

Cribl telemetry'si şu şekilde çalışıyor:

- **Endpoint:** `GET https://cdn.cribl.io/telemetry/index.html`
- **Method:** GET (POST değil!)
- **Format:** Query parameters (47 adet)
- **Response:** `cribl /// living the stream!\n`

Örnek parametreler:
- `v` - Cribl version
- `lic` - License bilgisi
- `iid` - Instance ID
- `os` - İşletim sistemi
- `fc.giv`, `fc.gev`, vb. - Feature kullanım metrikleri

## 🏗️ Sistem Mimarisi

```
┌─────────────┐     DNS redirect      ┌──────────────────┐
│   Cribl     │ ──────────────────►   │  telemetry-mock  │
│  Container  │   cdn.cribl.io        │   (FastAPI)      │
│             │   → 172.25.0.10       │   Port 80/443    │
└─────────────┘                       └──────────────────┘
                                              │
                                              ▼
                                      ┌──────────────────┐
                                      │   logs/*.json    │
                                      │  (JSON loglar)   │
                                      └──────────────────┘
```

## 📦 Docker Image

- **Docker Hub:** `kenankarakoc/logparse-test:latest`
- **Platform:** linux/amd64
- **Size:** ~60 MB

## 🚀 Kullanım

```bash
# Container'ları başlat
docker-compose up -d

# Test et
curl http://localhost:8000/health
curl http://localhost:8888/telemetry/index.html?test=1

# Logları kontrol et
ls -la logs/
cat logs/telemetry_*.json
```

## ⚠️ Bilinen Sınırlama: SSL Certificate

Cribl'in telemetry client'ı **hardcoded SSL validation** yapıyor. Denenen ama işe yaramayan yöntemler:

1. ❌ `NODE_TLS_REJECT_UNAUTHORIZED=0` - Cribl bunu yok sayıyor
2. ❌ `NODE_EXTRA_CA_CERTS` - Çalışmıyor
3. ❌ System CA store'a sertifika ekleme - Çalışmıyor
4. ❌ SAN (Subject Alternative Names) sertifikası - Çalışmıyor
5. ❌ Proxy ayarları (HTTP_PROXY/HTTPS_PROXY) - Mock server proxy değil

**Sonuç:** Mock server curl ile test edilebiliyor ve çalışıyor, ama Cribl'in kendi telemetry client'ı self-signed certificate kabul etmiyor. Bu Cribl'in bir sınırlaması.

## 📁 Dosya Yapısı

```
.
├── docker-compose.yml          # Ana compose dosyası
├── logs/                       # Telemetry JSON logları
└── telemetry-mock/             # Mock server kaynak kodu (worktree'de)
    ├── app/
    │   ├── main.py             # FastAPI endpoints
    │   ├── logger.py           # JSON logging
    │   └── models.py           # Pydantic models (47 param)
    ├── Dockerfile
    └── requirements.txt
```

## 🔧 docker-compose.yml Açıklaması

```yaml
services:
  cribl:
    extra_hosts:
      - "cdn.cribl.io:172.25.0.10"  # DNS redirect
    depends_on:
      - telemetry-mock

  telemetry-mock:
    image: kenankarakoc/logparse-test:latest
    networks:
      obs_net:
        ipv4_address: 172.25.0.10   # Sabit IP
```

## 📚 Detaylı Dökümanlar

Worktree'de (`.worktrees/telemetry-interceptor/`) şu dökümanlar var:

- `QUICKSTART.md` - Hızlı başlangıç
- `DEPLOYMENT.md` - Detaylı deployment kılavuzu
- `DOCKER-HUB.md` - Docker Hub kullanımı
- `CHEATSHEET.md` - Komut referansı
- `docs/analysis/telemetry-capture-20260205.md` - Yakalanan telemetry analizi

## 🧪 Test Komutları

```bash
# Health check
curl http://localhost:8000/health

# Telemetry endpoint
curl http://localhost:8888/telemetry/index.html?test=1

# DNS kontrolü (Cribl içinden)
docker exec cribl getent hosts cdn.cribl.io

# Container logları
docker logs telemetry-mock --tail 20

# Telemetry logları
cat $(ls -t logs/telemetry_*.json | head -1) | jq .
```

## 🔄 Sonraki Adımlar

1. SSL sorunu için Cribl'in kaynak koduna erişim gerekebilir
2. Alternatif olarak mitmproxy ile transparent proxy denenebilir
3. Veya telemetry'yi tamamen disable etme seçeneği araştırılabilir

---

**Son güncelleme:** 2026-02-05
**Oluşturan:** Claude Code (Opus 4.5)
