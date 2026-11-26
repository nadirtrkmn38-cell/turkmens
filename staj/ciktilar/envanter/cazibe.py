# 2018/11201 EK-1 (RG 25.01.2018/30312, s.11) — görsel okuma
CAZIBE_EK1 = "Adıyaman Ağrı Ardahan Batman Bayburt Bingöl Bitlis Diyarbakır Elazığ Erzincan Erzurum Gümüşhane Hakkâri Iğdır Kars Malatya Mardin Muş Siirt Şanlıurfa Şırnak Tunceli Van".split()
# 2018/11201 EK-2 (7028 sayılı CBK ile eklendi, RG 05.04.2023/32154) — deprem ilçeleri
DEPREM_EK2 = {
"Adıyaman":"Besni Çelikhan Gerger Gölbaşı Kahta Merkez Samsat Sincik Tut",
"Elazığ":"Alacakaya Arıcak Baskil Karakoçan Keban Kovancılar Maden Palu Sivrice",
"Gaziantep":"Araban İslahiye Nurdağı",
"Hatay":"Altınözü Antakya Arsuz Belen Defne Dörtyol Erzin Hassa İskenderun Kırıkhan Kumlu Payas Reyhanlı Samandağ Yayladağı",
"Kahramanmaraş":"Afşin Andırın Çağlayancerit Dulkadiroğlu Ekinözü Elbistan Göksun Nurhak Onikişubat Pazarcık Türkoğlu",
"Kilis":"Musabeyli Polateli",
"Malatya":"Akçadağ Arapgir Arguvan Battalgazi Darende Doğanşehir Doğanyol Hekimhan Kale Kuluncak Pütürge Yazıhan Yeşilyurt",
"Osmaniye":"Bahçe Hasanbeyli",
"Sivas":"Gürün",
}
DEPREM_EK2 = {k: v.split() for k, v in DEPREM_EK2.items()}
