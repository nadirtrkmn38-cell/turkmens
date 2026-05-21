/**
 * Turkmen'S - İstemci Yapılandırması
 *
 * ÖNEMLİ: Bu URL'i Railway'de deploy ettiğin sunucunun URL'i ile değiştir.
 * Build almadan ÖNCE doğru URL girilmiş olmalı.
 *
 * Örnek: 'https://turkmens-production.up.railway.app'
 */
window.TURKMENS_CONFIG = {
  // PRODUCTION'DA BURAYI DEĞİŞTİR ↓↓↓
  SERVER_URL: 'https://turkmens-server-production.up.railway.app',

  // Yeniden bağlanma denemesi sayısı (sınırsız için Infinity)
  RECONNECT_ATTEMPTS: Infinity,

  // Mesaj geçmişi sınırı
  MESSAGE_HISTORY_LIMIT: 100
};
