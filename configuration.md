# Konfigürasyon

- [Giriş](#giris)
- [Ortam Konfigürasyonu](#ortam-konfigurasyonu)
- [Bakım Modu](#bakim-modu)

<a name="giris"></a>
## Giriş

Laravel'in tüm konfigürasyon dosyaları `app/config` klasörü içindedir. Dosyalardaki konfigürasyonlar son derece iyi bir şekilde dökümante edilmiştir, dosyalara göz gezdirip size sunulan opsiyonlara bir bakabilirsiniz.

Bazen konfigürasyon ayarlarına run-time esnasında erişmeniz gerekir. Bunu `Config` sınıfını kullanarak yapabilirsiniz:

**Bir Konfigürasyon Değerine Erişmek**

	Config::get('app.timezone');

Eğer konfigürasyon değeri bulunamazsa dönecek değeri ise ikinci bir parametreyle belirleyebilirsiniz:

	$timezone = Config::get('app.timezone', 'UTC');

Lütfen dikkat edin, "nokta" şeklindeki kullanım stili tüm konfigürasyon dosyalarına erişmenizi sağlar. Dilerseniz konfigürasyon değerlerini run-time esnasında da ekleyebilirsiniz:

**Bir Konfigürasyon Değeri Eklemek**

	Config::set('database.default', 'sqlite');

<a name="ortam-konfigurasyonu"></a>
## Ortam Konfigürasyonu

Uygulamanın çalışma ortamına göre konfigürasyonlar ayarlamak çoğu zaman iyidir. Örneğin, kişisel bilgisayarınızda, sunucudan farklı bir önbellekleme uygulaması kullanmak isteyebilirsiniz. Bunu ortam tabanlı konfigürasyonlar oluşturarak sağlayabilirsiniz.

Bunu yapmak çok basit!  `config` klasörü içerisinde, ortam isminizi kullandığınız (örneğin  `local`)  bir klasör daha oluşturun. Şimdi, belirttiğiniz ortam için üzerine yazmak istediğiniz konfigürasyon dosyalarınızı ve ayarlarınızı geçirin. Örneğin, önbellekleme konfigürasyonunun üzerine yazmak için, `app/config/local` klasörü içerisinde  `cache.php` dosyası oluşturmanız gerekir. Oluşturduğunuz dosyanın içerisine şunları yazın:

	<?php

	return array(

		'driver' => 'file',

	);

> **Not:** 'testing' adını ortam ismi olarak kullanmayın. Bu isim Unit Testing amacıyla rezerve edilmiştir.

Dikkat ederseniz, bu dosyada _bütün_ ayarları yazmanıza gerek yok. Sadece üzerine yazmak istediklerinizi eklemeniz yeterli. Geri kalan değerler, öntanımlı konfigürasyon ayarlarından alınacaktır.

Şimdi yapmamız gereken Laravel'e hangi ortamda çalıştığını belirtmek. Öntanımlı ortam daima `production` ortamıdır. Ancak ana klasördeki `bootstrap/start.php` dosya içerisine eklemeler yaparak farklı ortamlar oluşturmak mümkündür. Bu dosya içerisinde `$app->detectEnvironment` adında bir çağrı bulacaksınız. Bu methoda eklenen bir parametre ile Laravel'e hangi ortamda çalıştığını belirtebilirsiniz. Hatta ihtiyacınız olursa, diğer ortam ve makine isimlerini de dizi olarak ekleyebilirsiniz:

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
