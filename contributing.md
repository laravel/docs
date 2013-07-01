# Laravel'e Katkıda Bulunulması

- [Giriş](#introduction)
- [Alınsın Talepleri (Pull Requests)](#pull-requests)
- [Kodlama İlkeleri](#coding-guidelines)

<a name="introduction"></a>
## Giriş

Laravel ücretsiz ve açık kaynak bir yazılım olup, geliştirilmesine ve ilerletilmesine katkıda bulunabilinir. Laravel kaynak kodu [Github](http://github.com) da bulunmakta olup, oradan projeye kolayca bir çatal açılarak (forking), katkılarınız birleştirilebilir (merging).

<a name="pull-requests"></a>
## Alınsın Talepleri

Alınsın talebinin işleyişi, yeni özellikler için veya yazılım hataları için olmasına bağlı olarak farklılık gösterir. Yeni bir özellik için yapılacak bir alınsın talebi göndermeden önce, başlığında bir teklif `[Proposal]` konusu oluşturmanız gerekir. Teklifin, yeni özelliği ve uygulama fikirlerini tarif eder şekilde olması gerekir. Bu ilkeye uyulmamış olan alınsın talepleri hemen kapatılacaktır.

Yazılım hataları için gönderilecek olan alınsın talepleri, bir teklif oluşturulmadan gönderilebilinir. Eğer Github'da dosyalanmış olan bir yazılım hatası çözümünü bildiğinizi düşünüyorsanız, o durumda lütfen önerilen düzeltmenin detaylarını belirten bir not giriniz.

### Özellik Talepleri

Eğer Laravel'e ilave edildiğini görmek isteyeceğiniz bir 'yeni özellik' fikriniz varsa, Github'da başlığında 'Talep' `[Request]` olacak bir konu oluşturabilirsiniz. Özellik talebi, bir ana katılımcı tarafından gözden geçirilecektir.

<a name="coding-guidelines"></a>
## Kodlama İlkeleri

Laravel, [PSR-0](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-0.md) ve [PSR-1](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-1-basic-coding-standard.md) kodlama standartlarını takip eder. Bunlara ilave olarak, takip edilmesi gereken diğer standartların listesi şöyledir:

- 'Namespace' deklarasyonlarının `<?php` ile aynı satırda olması gerekir.
- Sınıf (Class) açılışlarının `{` , sınıf ismi ile aynı satırda olması gerekir.
- Fonksiyon (Function) ve kontrol bloğu (control structure) açılışlarının `{`, farklı satırlarda olması gerekir.
- Arayüz (Interface) isimleri `Interface` son ekini alırlar, örneğin (`FalancaInterface`).
