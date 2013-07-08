# Hatalar ve Günlüğe Ekleme

- [Error Detail](#error-detail)
- [Handling Errors](#handling-errors)
- [HTTP Exceptions](#http-exceptions)
- [Handling 404 Errors](#handling-404-errors)
- [Logging](#logging)

<a name="error-detail"></a>
## Hata Ayrıntısı

Ön tanımlı olarak hata ayrıntısı uygulamanızda etkindir. Yani bir hata oluştuğu zaman ayrıntılı bir sorun listesi ve hata iletisi gösterebileceksiniz. `app/config/app.php` dosyanızdaki `debug` seçeneğini `false` ayarlayarak hata ayrıntılarını devre dışı bırakabilirsiniz. **Bir üretim ortamında hata ayrıntılarını devre dışı bırakmanız kuvvetle önerilir.**

<a name="handling-errors"></a>
## Hataların İşlenmesi

Ön tanımlı olarak, `app/start/global.php` dosyasında tüm istisnalar için bir hata işleyici bulunmaktadır:

	App::error(function(Exception $exception)
	{
		Log::error($exception);
	});

En temel hata işleyici budur. Ama siz gerektiği kadar işleyici belirleyebilirsiniz. İşleyicilere işledikleri İstisnaların tipine işaret eden isimler verilir. Örneğin, sadece `RuntimeException` olgularını işleyen bir işleyici oluşturabilirsiniz:

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

PHP'nin fatal hatalarını izlemek için, `App::fatal` metodunu kullanabilirsiniz:

	App::fatal(function($exception)
	{
		//
	});

<a name="http-exceptions"></a>
## HTTP İstisnaları

HTTP istisnaları bir istemci isteği sırasında oluşabilecek hatalar demektir. Bu bir sayfa bulunamadı hatası (404), bir yetkisizlik hatası (401) hatta genel 500 hatası olabilir. Böyle bir cevap döndürmek için aşağıdaki biçimi kullanın:

	App::abort(404, 'Sayfa bulunamadı');

Buradaki ilk parametre HTTP durum kodu, ikinci parametre ise bu hata durumunda göstermek istediğiniz özel bir mesajdır.

401 Yetkisizlik istisnası çıkarmak için tek yapacağınız şudur:

	App::abort(401, 'Yetkili değilsiniz.');

Bu istisnalar, isteğin yaşam döngüsü boyunca her an çalışabilecektir.

<a name="handling-404-errors"></a>
## Handling 404 Errors

You may register an error handler that handles all "404 Not Found" errors in your application, allowing you to return custom 404 error pages:

	App::missing(function($exception)
	{
		return Response::view('errors.missing', array(), 404);
	});

<a name="logging"></a>
## Logging

The Laravel logging facilities provide a simple layer on top of the powerful [Monolog](http://github.com/seldaek/monolog). By default, Laravel is configured to create daily log files for your application, and these files are stored in `app/storage/logs`. You may write information to these logs like so:

	Log::info('This is some useful information.');

	Log::warning('Something could be going wrong.');

	Log::error('Something is really going wrong.');

The logger provides the seven logging levels defined in [RFC 5424](http://tools.ietf.org/html/rfc5424): **debug**, **info**, **notice**, **warning**, **error**, **critical**, and **alert**.

Monolog has a variety of additional handlers you may use for logging. If needed, you may access the underlying Monolog instance being used by Laravel:

	$monolog = Log::getMonolog();

You may also register an event to catch all messages passed to the log:

**Registering A Log Listener**

	Log::listen(function($level, $message, $context)
	{
		//
	});
