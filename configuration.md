# Yapılandırma

- [Giriş](#giris)
- [Ortam Yapılandırması](#ortam-yapilandirilmasi)
- [Bakım Modu](#bakim-modu)

<a name="giris"></a>
## Giriş

Laravel'in tüm yapılandırma dosyaları `app/config` dizini içindedir. Tüm dosyalardaki yapılandırma seçenekleri açıklanmıştır, dosyalara göz gezdirip size sunulan seçeneklere göz atabilirsiniz.

Bazen yapılandırma değerlerine run-time (çalışma anı) esnasında erişmeniz gerekir. Bunu `Config` sınıfını kullanarak yapabilirsiniz:

**Bir Yapılandırma Değerine Erişmek**

	Config::get('app.timezone');

Eğer yapılandırma değeri bulunamazsa dönecek değeri ise ikinci bir parametreyle belirleyebilirsiniz:

	$timezone = Config::get('app.timezone', 'UTC');

Lütfen dikkat edin, "nokta" şeklindeki kullanım biçimi tüm yapılandırma dosyalarına erişmenizi sağlar. Dilerseniz yapılandırma değerlerini run-time (çalışma anı) esnasında da ekleyebilirsiniz:

**Bir Yapılandırma Değeri Eklemek**

	Config::set('database.default', 'sqlite');

<a name="ortam-yapilandirilmasi"></a>
## Ortam Yapılandırması

Uygulamanın çalışma ortamına göre farklı yapılandırma değerlerine sahip olmak çoğu zaman iyidir. Örneğin, kişisel bilgisayarınızda, sunucudan farklı bir önbellekleme uygulaması kullanmak isteyebilirsiniz. Bunu ortam tabanlı yapılandırmalar oluşturarak sağlayabilirsiniz.

Bunu yapmak çok basit! `config` dizini içerisinde, ortam isminizi kullandığınız (örneğin `local`) bir dizin daha oluşturun. Şimdi, belirttiğiniz ortam için üzerine yazmak istediğiniz yapılandırma dosyalarınızı ve seçeneklerinizi geçirin. Örneğin, önbellekleme yapılandırmasının üzerine yazmak için, `app/config/local` dizini içerisinde `cache.php` dosyası oluşturmanız gerekir. Oluşturduğunuz dosyanın içerisine şunları yazın:

	<?php

	return array(

		'driver' => 'file',

	);

> **Not:** 'testing' adını ortam ismi olarak kullanmayın. Bu isim Unit Testing amacıyla rezerve edilmiştir.

Dikkat ederseniz, bu dosyada _bütün_ değerleri yazmanıza gerek yok. Sadece üzerine yazmak istediklerinizi eklemeniz yeterli. Geri kalan değerler, öntanımlı yapılandırma değerlerinden alınacaktır.

Şimdi yapmamız gereken Laravel'e hangi ortamda çalıştığını belirtmek. Öntanımlı ortam daima `production` ortamıdır. Ancak ana dizindeki `bootstrap/start.php` dosya içerisine eklemeler yaparak farklı ortamlar oluşturmak mümkündür. Bu dosya içerisinde `$app->detectEnvironment` adında bir tanım bulacaksınız. Bu methoda eklenen bir parametre ile Laravel'e hangi ortamda çalıştığını belirtebilirsiniz. Hatta ihtiyacınız olursa, diğer ortam ve makine isimlerini de dizi olarak ekleyebilirsiniz:

    <?php

    $env = $app->detectEnvironment(array(

        'local' => array('your-machine-name'),

    ));

Dilerseniz, `detectEnvironment` methoduna `Closure` ekleyip ortam algılama özelliğini kendiniz de yazabilirsiniz:

	$env = $app->detectEnvironment(function()
	{
		return $_SERVER['MY_LARAVEL_ENV'];
	});

Şuanki uygulama ortamına `environment` methoduyla erişebilirsiniz:

**Şuanki Uygulama Ortamına Erişmek**

	$environment = App::environment();

<a name="bakim-modu"></a>
## Bakım Modu

Uygulamanız bakım modundayken, her istek için standart bir view gösterilir. Böylece uygulamanız güncellenirken, bir süreliğine uygulamayı "çalışmaz hale" getirebilirsiniz. Halihazırda `App::down` methoduna yapılan bir istek `app/start/global.php` dosyasında bulunmaktadır. Bu methoddan dönen yanıt ise tüm kullanıcılara gösterilmektedir.

Bakım modunu açmak için `down` komutunu Artisan üzerinde çalıştırın:

	php artisan down

Bakım modunu kapatmak içinse, `up` komutunu çalıştırabilirsiniz:

	php artisan up

Uygulamanız bakım modundayken kullanıcılara özel bir view göstermek için `app/start/global.php` dosyası içerisindeki `down` methodunu dilediğiniz gibi değiştirebilirsiniz:

	App::down(function()
	{
		return Response::view('bakim_sayfasi', array(), 503);
	})
