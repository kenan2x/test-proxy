# Cribl Telemetry Interceptor - Proje Özeti

Bu proje Cribl'in cdn.cribl.io adresine gönderdiği telemetry verilerini yakalamak ve analiz etmek için oluşturuldu.

## 🎯 Mimari (v2 - Proxy Tabanlı)

```
┌─────────────┐   HTTPS_PROXY    ┌─────────────┐     intercept     ┌─────────────┐
│   Cribl     │ ───────────────► │  mitmproxy  │ ────────────────► │  logs/*.json│
│  Container  │                  │   :8080     │  (cdn.cribl.io)   │             │
└─────────────┘                  └─────────────┘                   └─────────────┘
       │                                │
       │ NODE_EXTRA_CA_CERTS           │ CA cert
       └───────────────────────────────┘
```

**Nasıl çalışıyor:**
1. Cribl, `HTTPS_PROXY=http://mitmproxy:8080` ile tüm HTTPS trafiğini proxy'ye yönlendirir
2. mitmproxy, `cdn.cribl.io` isteklerini yakalar
3. `proxy-addon.py` scripti mock response döner: `cribl /// living the stream!`
4. Tüm istekler `logs/` dizinine JSON olarak kaydedilir
5. Cribl, mitmproxy'nin CA sertifikasına güvenir (NODE_EXTRA_CA_CERTS)

## 🚀 Kurulum

```bash
# 1. CA sertifikasını oluştur
./setup.sh

# 2. Container'ları başlat
docker-compose up -d

# 3. Logları izle
docker logs mitmproxy -f

# 4. Telemetry loglarını kontrol et
ls -la logs/
cat logs/telemetry_*.json
```

## 📁 Dosya Yapısı

```
.
├── docker-compose.yml     # Ana compose dosyası
├── proxy-addon.py         # mitmproxy interceptor scripti
├── setup.sh               # CA sertifika oluşturma scripti
├── certs/                 # mitmproxy CA sertifikaları
│   └── mitmproxy-ca-cert.pem
├── logs/                  # Yakalanan telemetry JSON'ları
└── CLAUDE.md              # Bu dosya
```

## 🔧 docker-compose.yml Açıklaması

```yaml
services:
  cribl:
    environment:
      - HTTP_PROXY=http://mitmproxy:8080    # Proxy ayarı
      - HTTPS_PROXY=http://mitmproxy:8080   # Proxy ayarı
      - NODE_EXTRA_CA_CERTS=/etc/ssl/certs/mitmproxy-ca.pem  # CA güveni
    volumes:
      - ./certs/mitmproxy-ca-cert.pem:/etc/ssl/certs/mitmproxy-ca.pem:ro

  mitmproxy:
    command: mitmdump -s /scripts/proxy-addon.py --set block_global=false
    volumes:
      - ./proxy-addon.py:/scripts/proxy-addon.py:ro
      - ./logs:/home/mitmproxy/logs
```

## 📊 Keşfedilen Telemetry Formatı

- **Endpoint:** `GET https://cdn.cribl.io/telemetry/index.html`
- **Method:** GET
- **Format:** 47 query parameter
- **Response:** `cribl /// living the stream!\n`

Örnek parametreler:
- `v` - Cribl version
- `lic` - License bilgisi
- `iid` - Instance ID
- `os` - İşletim sistemi
- `fc.*` - Feature kullanım metrikleri

## 🧪 Test Komutları

```bash
# Proxy çalışıyor mu?
curl -x http://localhost:8080 http://example.com

# Telemetry intercept test
curl -x http://localhost:8080 https://cdn.cribl.io/telemetry/index.html?test=1

# mitmproxy logları
docker logs mitmproxy --tail 50

# Telemetry JSON logları
cat $(ls -t logs/telemetry_*.json | head -1) | jq .
```

## 🔄 Eski Mimari (v1 - DNS Redirect)

Önceki versiyon DNS redirect kullanıyordu ama SSL sertifika hatası veriyordu:

```yaml
# ESKİ (çalışmıyordu - SSL hatası)
extra_hosts:
  - "cdn.cribl.io:172.25.0.10"
```

Yeni proxy-tabanlı mimari bu sorunu çözer çünkü:
1. mitmproxy MITM (Man-in-the-Middle) proxy olarak çalışır
2. Kendi CA sertifikasını oluşturur
3. Cribl bu CA'ya güvenecek şekilde yapılandırılır

## ⚠️ Önemli Notlar

- `setup.sh` ilk kurulumda **mutlaka** çalıştırılmalı
- CA sertifikası `certs/` dizininde saklanır
- Loglar `logs/` dizininde JSON formatında kaydedilir
- mitmproxy sadece `cdn.cribl.io` isteklerini yakalar, diğerleri geçer

---

**Son güncelleme:** 2026-02-07
**Mimari:** v2 (Proxy tabanlı)
**Oluşturan:** Claude Code (Opus 4.5)
