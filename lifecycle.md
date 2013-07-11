# İstek Yaşam Döngüsü

- [Genel Bakış](#genel-bakis)
- [Start Dosyaları](#start-dosyalari)
- [Application Olayları (Events)](#application-olaylari)

<a name="genel-bakis"></a>
## Genel Bakış

Laravel'de İstek Yaşam Döngüsü (Request Lifecycle) gerçekten çok basit bir yapıdadır. Bir istek application'a (?) girdikten sonra belirtilen bir route veya controller'a yönlendirilir. Daha sonra Route'un döndürdüğü cevap tarayıcıya yönlendirilir ve ekranda görünür. Bazen Route'lar çağırılmadan önce veya sonra bazı işlemleri yapmak isteyebilirsiniz. Laravel'de bunu yapmanın birkaç yolu vardır. Bu yollardan ikisi "start" dosyaları ve application olaylarıdır. (events)

<a name="start-dosyalari"></a>
## Start Dosyaları

Uygulamanızın start dosyaları `app/start` dizininde bulunmaktadır. Varsayılan olarak bunlardan üçü uygulamanızın içine dahil edilmiştir. Bunlar `global.php`, `local.php`, ve `artisan.php`'dir. `artisan.php` hakkında daha fazla bilgiye sahip olmak için [Artisan command line](/docs/commands#registering-commands) dökümanlarına bakınız.

The `global.php` start file contains a few basic items by default, such as the registration of the [Logger](/docs/errors) and the inclusion of your `app/filters.php` file. However, you are free to add anything to this file that you wish. It will be automatically included on _every_ request to your application, regardless of environment. The `local.php` file, on the other hand, is only called when the application is executing in the `local` environment. For more information on environments, check out the [configuration](/docs/configuration) documentation.

Of course, if you have other environments in addition to `local`, you may create start files for those environments as well. They will be automatically included when your application is running in that environment.

<a name="application-olaylari"></a>
## Application Olayları (Events)

You may also do pre and post request processing by registering `before`, `after`, `close`, `finish`, and `shutdown` application events:

**Registering Application Events**

	App::before(function()
	{
		//İstek öncesi olayları
	});

	App::after(function($request, $response)
	{
		//İstek sonrası olayları
	});

Bu olayların dinleyicileri, uygulamanıza yapılan her istek öncesinde `(before)` ve sonrasında `(after)` çalışacaktır.
