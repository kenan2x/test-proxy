# Cribl Telemetry Interceptor - Proje Özeti

Bu proje Cribl'in cdn.cribl.io adresine gönderdiği telemetry verilerini yakalamak ve analiz etmek için oluşturuldu.

## 🎯 Mimari (v3 - Tek Container)

```
┌─────────────┐   HTTPS_PROXY    ┌─────────────────────────────────┐
│   Cribl     │ ───────────────► │  kenankarakoc/logparse-test     │
│  Container  │                  │  (mitmproxy + addon + CA cert)  │
└─────────────┘                  └─────────────────────────────────┘
       │                                       │
       │ NODE_EXTRA_CA_CERTS                  │ logs/*.json
       └───────────────► shared volume ◄──────┘
```

**Nasıl çalışıyor:**
1. Proxy container başladığında otomatik CA sertifikası oluşturur
2. Sertifika shared volume'a yazılır
3. Cribl container sertifikayı volume'dan alır ve güvenir
4. Tüm telemetry trafiği yakalanır ve `logs/` dizinine JSON olarak kaydedilir

## 🚀 Kurulum (Otomatik)

```bash
# Sadece logs dizini oluştur
mkdir -p logs

# Container'ları başlat (her şey otomatik!)
docker-compose up -d

# Logları izle
docker logs cribl-proxy -f

# Telemetry loglarını kontrol et
cat logs/telemetry_*.json | jq .
```

## 📦 Docker Hub Image

```
kenankarakoc/logparse-test:latest
kenankarakoc/logparse-test:proxy
```

Image içeriği:
- mitmproxy + interceptor addon
- Otomatik CA sertifika oluşturma
- cdn.cribl.io telemetry yakalama

## 📁 Dosya Yapısı

```
.
├── docker-compose.yml     # Ana compose dosyası (çalıştırmak için tek gerekli)
├── Dockerfile             # Single container build
├── entrypoint.sh          # CA cert oluşturma + mitmproxy başlatma
├── proxy-addon.py         # mitmproxy interceptor scripti
├── logs/                  # Yakalanan telemetry JSON'ları
└── CLAUDE.md              # Bu dosya
```

## 🔧 docker-compose.yml

```yaml
services:
  mitmproxy:
    image: kenankarakoc/logparse-test:latest
    volumes:
      - proxy-certs:/certs          # CA cert shared volume
      - ./logs:/logs                # Telemetry JSON logları
    healthcheck:                    # CA cert hazır mı kontrol
      test: ["CMD", "test", "-f", "/certs/mitmproxy-ca-cert.pem"]

  cribl:
    environment:
      - HTTPS_PROXY=http://mitmproxy:8080
      - NODE_EXTRA_CA_CERTS=/etc/ssl/certs/mitmproxy-ca.pem
    volumes:
      - proxy-certs:/proxy-certs:ro  # CA cert'i al
    entrypoint: ["sh", "-c", "cp /proxy-certs/mitmproxy-ca-cert.pem /etc/ssl/certs/mitmproxy-ca.pem && exec /sbin/entrypoint.sh cribl"]
    depends_on:
      mitmproxy:
        condition: service_healthy  # CA cert hazır olana kadar bekle
```

## 📊 Telemetry Formatı

- **Endpoint:** `GET https://cdn.cribl.io/telemetry/index.html`
- **Method:** GET
- **Format:** 47+ query parameter

Örnek parametreler:
- `v` - Cribl version (örn: 4.16.1-20904e45)
- `lic` - License bilgisi (base64)
- `licls` - License status (free/enterprise)
- `guid` - Instance GUID
- `os` - İşletim sistemi (örn: ubuntu-24.04)
- `kv` - Kernel version
- `fc.*` - Feature kullanım metrikleri
- `pc`, `ic`, `oc` - Pipeline/Input/Output sayıları

## 🧪 Test Komutları

```bash
# Proxy çalışıyor mu?
docker logs cribl-proxy --tail 20

# Telemetry intercept test
curl -x http://localhost:8080 https://cdn.cribl.io/telemetry/index.html?test=1

# Son telemetry log
cat $(ls -t logs/telemetry_*.json | head -1) | jq .

# Tüm telemetry sayısı
ls logs/telemetry_*.json | wc -l
```

## 🔄 Versiyon Geçmişi

| Versiyon | Mimari | Durum |
|----------|--------|-------|
| v1 | DNS Redirect + nginx | SSL hatası - çalışmıyor |
| v2 | mitmproxy + manuel CA kurulum | Çalışıyor ama manuel setup gerekiyor |
| v3 | Single container + otomatik CA | **Aktif** - Tek komutla çalışır |

---

**Son güncelleme:** 2026-02-07
**Mimari:** v3 (Tek container, otomatik CA)
**Image:** kenankarakoc/logparse-test:latest
**Oluşturan:** Claude Code (Opus 4.5)
