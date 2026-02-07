#!/bin/bash
# Setup script - CA sertifikasını oluşturur

set -e

echo "🔧 Cribl Telemetry Proxy Setup"
echo "=============================="

# Dizinleri oluştur
mkdir -p certs logs

# Eğer CA sertifikası yoksa, mitmproxy ile oluştur
if [ ! -f "certs/mitmproxy-ca-cert.pem" ]; then
    echo "📜 CA sertifikası oluşturuluyor..."

    # mitmproxy'yi geçici olarak çalıştır (sertifika oluşturması için)
    docker run --rm -v $(pwd)/certs:/home/mitmproxy/.mitmproxy mitmproxy/mitmproxy:latest \
        mitmdump --set confdir=/home/mitmproxy/.mitmproxy -n 2>/dev/null || true

    echo "✅ CA sertifikası oluşturuldu: certs/mitmproxy-ca-cert.pem"
else
    echo "✅ CA sertifikası zaten mevcut"
fi

# Sertifika kontrolü
if [ -f "certs/mitmproxy-ca-cert.pem" ]; then
    echo ""
    echo "📋 Sertifika bilgisi:"
    openssl x509 -in certs/mitmproxy-ca-cert.pem -noout -subject -dates 2>/dev/null || echo "  (openssl yüklü değil, atlıyorum)"
else
    echo "❌ HATA: Sertifika oluşturulamadı!"
    exit 1
fi

echo ""
echo "🚀 Başlatmak için:"
echo "   docker-compose up -d"
echo ""
echo "📊 Logları kontrol etmek için:"
echo "   docker logs mitmproxy -f"
echo "   ls -la logs/"
