# Laravel Hızlı Başlangıç

- [Kurulum](#kurulum)
- [Routing (Yönlendirme)](#routing)
- [Bir View Oluşturma](#bir-view-olusturma)
- [Bir Migration Oluşturma](#bir-migration-olusturma)
- [Eloquent ORM](#eloquent-orm)
- [Veri Gösterme](#veri-gosterme)

<a name="kurulum"></a>
## Kurulum

Laravel Framework'ü kurmak için aşağıdaki komutu, komut işleyici uygulamanızdan çalıştırabilirsiniz:

	composer create-project laravel/laravel your-project-name --prefer-dist

veya Laravel Framework'ü kurmak için [Github Kaynağı'nı](https://github.com/laravel/laravel/archive/master.zip) indirmelisiniz. Daha sonra [Composer'i kurup](http://getcomposer.org), `composer install` komutunu projenizin root (ana) dizininde çalıştırmalısınız. Bu komutu çalıştırmak, Laravel'i ve Laravel'in gereksinimlerini (dependencies) indirip kuracaktır.

Laravel kurulduktan sonra dizin yapısına göz gezdirin ve Laravel'in nasıl bir yapısı olduğuna bakın. `app` dizini içerisinde `views`, `controllers`, ve `models` gibi dizinler bulunmaktadır. Projenizi geliştirirken yazacağınız kodların çok büyük bir kısmı bu dizinlerin içine yazılacaktır. Ayrıca `app/config` dizini içerisine bakıp size ne tür ayar değerleri tanımlandığını görebilirsiniz.

<a name="routing"></a>
## Routing (Yönlendirme)

Başlangıç olarak Laravel'de ilk Route'umuzu yazalım. Laravel'de Route oluşturmak için en basit yol bir closure (anonim fonksiyon) kullanmaktır. `app/routes.php` dosyasını açın ve aşağıdaki kod parçacığını sayfanın en altına yapıştırın:

	Route::get('kullanicilar', function()
	{
		return 'Kullanıcılar!';
	});

Şimdi, eğer web tarayıcınızda `/kullanicilar` adresine girerseniz, ekranda `Kullanıcılar!` yazısını görmüş olmanız gerekir. Eğer gördüyseniz çok iyi! İlk Route'unuzu başarıyla oluşturdunuz.

Route'lar ayrıca controller sınıflarına da bağlanabilir. Örneğin:

	Route::get('kullanicilar', 'KullaniciController@getIndex');

Bu Route Laravel'e şunu belirtiyor: `/kullanicilar` adresine bir istek geldiği zaman, Laravel `UserController` kontroller sınıfının `getIndex` methodunu çağırmalı. Controller Routing hakkında daha fazla bilgi almak için [Controller Dökümantasyonu'na](/docs/controllers) bir göz atın.

<a name="bir-view-olusturma"></a>
## Bir View Oluşturma

Şimdi basit bir view dosyası oluşturup, kullanıcı bilgilerini ekrana view üzerinden yazdıracağız. View dosyaları `app/views` dizini içerisinde bulunmakta olup projenizin HTML dosyalarını barındırır. Şimdi bu dizin içerisine 2 tane dosya oluşturacağız: `layout.blade.php` ve `kullanicilar.blade.php`. Önce `layout.blade.php` dosyamızı oluşturalım:

	<html>
		<body>
			<h1>Laravel Hızlı Başlangıç</h1>

			@yield('content')
		</body>
	</html>

Şimdiki adımda ise `kullanicilar.blade.php` view dosyasını oluşturalım:

	@extends('layout')

	@section('content')
		Kullanıcılar!
	@stop

Bu syntax size ilk etapta biraz yabancı gelebilir. 
Bunun sebebi Laravel'in güçlü templating sisteminin (Blade) kullanılmasıdır. Blade son derece hızlı çalışır çünkü sadece birkaç tane regex kodları kullanıp Blade syntaxını PHP scriptlerine dönüştürür. Blade kullanıcılarına çok büyük fonksiyonellik sağlar. Tema kalıtımı (Template inheritance) ve PHP'nin `if` ve `for` gibi temel kontrol yapılarını Blade üzerinden kullanabilirsiniz. Daha fazla bilgi için [Blade Dökümantasyonu'na](/docs/templates) bakınız.

Şimdi gerekli view dosyalarımızı oluşturduğumuza göre, oluşturduğumuz viewi `/kullanicilar` isteğine bir cevap olarak döndürelim. `Kullanıcılar!` stringini döndürmek yerine, bu kez oluşturduğumuz view dosyalarını döndüreceğiz:

	Route::get('kullanicilar', function()
	{
		return View::make('kullanicilar');
	});

Harika! Bir layoutu genişleten bir view oluşturdunuz. Birdahaki bölümümümüzde Veritabanı Katmanı (Database Layer) üzerinde duracağız.

<a name="bir-migration-olusturma"></a>
## Bir Migration Oluşturma

Bir veritabanı tablosu oluşturmak için Laravel'in migration özelliğini kullanacağız. Migrationlar çok kolay bir şekilde veritabanında değişiklikler yapmayı ve bunları takım arkadaşlarınızla paylaşmanızı sağlar.

Öncelikle bir veritabanı konfigürasyonu ayarlayalım. Tüm veritabanı konfigürasyonlarınızı `app/config/database.php` dosyası içerisinde değiştirebilirsiniz. Öntanımlı olarak Laravel SQLite kullanmaya ayarlanmıştır ve SQLite veritabanı `app/database` dizininde bulunmaktadır. Dilerseniz `driver` değerini `mysql` yapıp, `mysql` bağlantı bilgilerini girebilirsiniz.

Sonra, bir migration oluşturmak için [Artisan CLI](/docs/artisan) kullanacağız. Projenizin ana dizinine gelerek, aşağıdaki kodu terminal üzerinde yazın:

	php artisan migrate:make create_users_table

Şimdi, oluşturulan migration dosyasını `app/database/migrations` dizininde bulun. Bu dosya 2 methoddan oluşmaktadır: `up` ve `down`. `up` methodunda, tablonuzdaki değişiklikleri yapmalısınız. `down` methodunda ise yaptığınız değişiklikleri geri almalısınız.

Şuna benzeyen bir migration oluşturalım:

	public function up()
	{
		Schema::create('users', function($table)
		{
			$table->increments('id');
			$table->string('email')->unique();
			$table->string('name');
			$table->timestamps();
		});
	}

	public function down()
	{
		Schema::drop('users');
	}

Şimdi bu migrationu Artisan CLI üzerinde `migrate` komutu kullanarak çalıştıralım. Projenizin ana dizinine gelip aşağıdaki kodu çalıştırın:

	php artisan migrate

Eğer bir migrationu geri almak isterseniz `migrate:rollback` komutunu çalıştırmanız yeterli olacaktır. Şimdi bir veritabanı tablosu oluşturduğumza göre, tablomuzdan veri çekmeyi öğrenerek devam edelim!

<a name="eloquent-orm"></a>
## Eloquent ORM

Laravel mükemmel bir ORM aracıyla beraber gelmektedir: Eloquent. 
Eğer daha önce Ruby on Rails frameworkü üzerinde çalıştıysanız Eloquent size çok tanıdık gelecektir, çünkü veritabanı işlemleri için ActiveRecord stilini kullanır.

Öncelikle, modeli tanımlayalım. Bir Eloquent modeli belirtilen bir veritabanı tablosunu sorgulamak ve o tablodaki verileri tutmak için kullanılır.
Merak etmenize gerek yok, örnekleri görünce ne kadar kolay olduğunu anlayacaksınız! Model dosyaları `app/models` dizininde bulunmaktadır. Şimdi o dizinde bir `User.php` modeli oluşturalım:

	class User extends Eloquent {}

Lütfen dikkat edin, herhangi bir veritabanı tablosu belirtmedik.

Eloquent'in içerisinde birçok hüküm vardır, bunlardan birisi model adının çoğul yapısını veritabanı tablosu olarak kullandırmaktır. Kullanışlı, değil mi?

İstediğiniz veritabanı yönetim aracını kullanarak `users` tablosunu oluşturun. Şimdi Eloquent'i kullanarak o tablodan bazı verileri çekip view dosyamıza göndereceğiz.

Şimdi `/users` routemizi editleyelim, ve şuna benzer bir hale getirelim:

	Route::get('users', function()
	{
		$users = User::all(); //Users tablosundaki tüm verileri $users değişkenine atar

		return View::make('users')->with('users', $users);
	});

Şimdi bu scripti biraz inceleyelim. Öncelikle, `User` modelindeki `all` methodu `users` tablosundaki tüm verileri çekecektir. Daha sonra bu veriler `with` methodu kullanılarak view dosyasına gönderilir. `with` methodu bir anahtar ve bir değer almaktadır, böylece gönderilen veriyi view dosyası tanıyabilir.

Harika. Artık kullanıcıları view dosyamızda göstermeye hazırız!

<a name="veri-gosterme"></a>
## Veri Gösterme

Artık `users` objesini view dosyamıza yönlendirdiğimiz için ekrana bastırabiliriz:

	@extends('layout')

	@section('content')
		@foreach($users as $user)
			<p>{{ $user->name }}</p>
		@endforeach
	@stop

`echo` ifadesinin nerede olduğunu merak ediyor olabilirsiniz. Blade kullanırken, çift köşeli parantezler arasına yazılan değişkenler aynı `echo` ifadesindeki gibi ekrana bastırılır. Şimdi `users` adresine girip veritabanınızda kayıtlı olan tüm kullanıcıların listesinin ekrana bastırıldığını görebilirsiniz.

Bu sadece bir başlangıç. Bu derste Laravel'in en basit konularını gördünüz, ancak daha göreceğiniz birçok heyecan verici özellikler var! Dökümantasyonu okumaya devam edin ve Laravel içerisinde gelen birçok farklı özellik hakkında daha fazla bilgiye sahip olun. Örneğin [Eloquent](/docs/eloquent) ve [Blade](/docs/templates). Belkide sizin ilginizi [Queues](/docs/queues) ve [Unit Testing](/docs/testing) çekiyordur?. Yada [IoC Container](/docs/ioc) kullanarak uygulamanızın mimarisini güçlendirmek istiyorsunuzdur? Seçim sizin!
