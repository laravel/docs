# İstek Yaşam Döngüsü

- [Genel Bakış](#genel-bakis)
- [Start Dosyaları](#start-dosyalari)
- [Application Olayları (Events)](#application-olaylari)

<a name="genel-bakis"></a>
## Genel Bakış

Laravel'de İstek Yaşam Döngüsü (Request Lifecycle) gerçekten çok basit bir yapıdadır. Bir istek uygulamanıza girer ve uygun rota veya kontrolöre gönderilir. Bu rotadan gelen cevap daha sonra tarayıcıya geri gönderilir ve ekranda görüntülenir. Bazen, rotalarınız gerçekten çağrılmadan önce ya da sonra bazı işlemler yapmak isteyebilirsiniz. Laravel'de bunu yapmanın birkaç yolu vardır. Bu yollardan ikisi "start" dosyaları ve application olaylarıdır (events). 

<a name="start-dosyalari"></a>
## Start Dosyaları

Uygulamanızın start dosyaları `app/start` dizininde bulunmaktadır. Varsayılan olarak bunlardan üçü uygulamanızın içine dahil edilmiştir. Bunlar `global.php`, `local.php`, ve `artisan.php`'dir. `artisan.php` hakkında daha fazla bilgiye sahip olmak için [Artisan komut satırı](/docs/commands#registering-commands) dökümanlarına bakınız.

Bunlardan `global.php` start dosyası [Günlüklerin](/docs/errors) kayda geçirilmesi ve `app/filters.php` dosyanızın dahil edilmesi gibi ön tanımlı birkaç temel öğe içerir. Ancak, bu dosyaya istediğiniz her şeyi ekleyebilirsiniz. Bu dosya ortam ne olursa olsun uygulamanıza gelen _her_ istekte otomatik olarak dahil edilecektir. Öte yandan `local.php` dosyası yalnızca uygulamanız `local` ortamda çalışırken çağrılır. Ortamlar hakkında daha fazla bilgi için [Yapılandırma](/docs/configuration) belgelerine bakınız.

`local`'e ilaveten başka ortamlarınız da varsa, pek tabii bu ortamlar için de start dosyaları oluşturabilirsiniz. Uygulamanız o ortamda çalıştığı zaman bunlar otomatik olarak dahil edileceklerdir.

<a name="application-olaylari"></a>
## Application Olayları (Events)

Bunlara ek olarak `before`, `after`, `close`, `finish` ve `shutdown` uygulama olaylarını kayda geçirmek suretiyle istek öncesinde ve sonrasında bazı işlemler de yapabilirsiniz:

**Uygulama Olaylarının Kayda Geçirilmesi**

	App::before(function()
	{
		//İstek öncesi olayları
	});

	App::after(function($request, $response)
	{
		//İstek sonrası olayları
	});

Bu olay dinleyicileri, uygulamanıza yapılan her istek öncesinde `(before)` ve sonrasında `(after)` çalışacaktır.
