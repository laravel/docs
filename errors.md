# Hatalar ve Günlüğe Ekleme

- [Hata Ayrıntısı](#error-detail)
- [Hataların İşlenmesi](#handling-errors)
- [HTTP İstisnaları](#http-exceptions)
- [404 Hatalarının İşlenmesi](#handling-404-errors)
- [Günlüğe Ekleme](#logging)

<a name="error-detail"></a>
## Hata Ayrıntısı

Ön tanımlı olarak hata ayrıntısı uygulamanızda etkindir. Yani bir hata oluştuğu zaman ayrıntılı bir sorun listesi ve hata iletisi gösterebileceksiniz. `app/config/app.php` dosyanızdaki `debug` seçeneğini `false` ayarlayarak hata ayrıntılarını devre dışı bırakabilirsiniz. **Bir üretim ortamında hata ayrıntılarını devre dışı bırakmanız şiddetle önerilir.**

<a name="handling-errors"></a>
## Hataların İşlenmesi

Ön tanımlı olarak, `app/start/global.php` dosyasında tüm istisnalar için bir hata işleyici bulunmaktadır:

	App::error(function(Exception $exception)
	{
		Log::error($exception);
	});

En temel hata işleyici budur. Ancak siz gerektiği kadar işleyici belirleyebilirsiniz. İşleyicilere işledikleri İstisnaların tipine işaret eden isimler verilir. Örneğin, sadece `RuntimeException` olgularını işleyen bir işleyici oluşturabilirsiniz:

	App::error(function(RuntimeException $exception)
	{
		// İstisnayı işle...
	});

Bir istisna işleyicisinin bir cevap döndürmesi halinde, bu cevap tarayıcıya gönderilecek ve başka bir hata işleyici çağrılmayacaktır:

	App::error(function(InvalidUserException $exception)
	{
		Log::error($exception);

		return 'Maalesef bu hesapla ilgili yanlış bir şeyler var!';
	});

PHP'nin önemli hatalarını (fatal error) izlemek için, `App::fatal` metodunu kullanabilirsiniz:

	App::fatal(function($exception)
	{
		//
	});

<a name="http-exceptions"></a>
## HTTP İstisnaları

HTTP istisnaları bir istemci isteği sırasında oluşabilecek hatalar demektir. Bu bir sayfa bulunamadı hatası (404), bir yetkisizlik hatası (401), hatta genel 500 hatası olabilir. Böyle bir cevap döndürmek için aşağıdaki biçimi kullanın:

	App::abort(404, 'Sayfa bulunamadı');

Buradaki ilk parametre HTTP durum kodu, ikinci parametre ise bu hata durumunda göstermek istediğiniz özel bir mesajdır.

401 Yetkisizlik istisnası çıkarmak için tek yapacağınız şudur:

	App::abort(401, 'Yetkili değilsiniz.');

Bu istisnalar, isteğin yaşam döngüsü boyunca her an çalışabilecektir.

<a name="handling-404-errors"></a>
## 404 Hatalarının İşlenmesi

Uygulamanızdaki tüm "404 Not Found" hatalarını işleyerek özel 404 hata hata sayfaları döndürmenize imkan veren bir hata işleyici kaydı yapabilirsiniz:

	App::missing(function($exception)
	{
		return Response::view('errors.missing', array(), 404);
	});

<a name="logging"></a>
## Günlüğe Ekleme

Laravel'in günlüğe ekleme imkanlanları güçlü [Monolog](http://github.com/seldaek/monolog) üstünde basit bir katman sağlar. Laravel, ön tanımlı olarak uygulamanız için günlük dosyaları oluşturacak şekilde yapılandırılmıştır ve bu dosyalar `app/storage/logs` klasörü içinde tutulmaktadır. Bu dosyalara aşağıdakilere benzer şekilde bilgi yazabilirsiniz:

	Log::info('İşte bu yararlı bir bilgidir.');

	Log::warning('Yanlış giden bir şeyler olabilir.');

	Log::error('Gerçekten yanlış giden bir şey var.');

Günlük tutucu, [RFC 5424](http://tools.ietf.org/html/rfc5424)'de tanımlanmış yedi günlük ekleme düzeyi sağlamaktadır: **debug**, **info**, **notice**, **warning**, **error**, **critical** ve **alert**.

Monolog, günlüğe ekleme için kullanabileceğiniz bir takım başka işleyicilere de sahiptir. Gerektiğinde, Laravel tarafından kullanılan Monolog olgusuna şu şekilde ulaşabilirsiniz:

	$monolog = Log::getMonolog();

Ayrıca, günlüğe geçirilen tüm mesajları yakalamak için bir olay kaydı da yapabilirsiniz:

**Bir günlük izleyici kaydı yapılması**

	Log::listen(function($level, $message, $context)
	{
		//
	});
