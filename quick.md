# Laravel Hızlı Başlangıç

- [Kurulum](#kurulum)
- [Routing (Yönlendirme)](#routing)
- [Bir View Oluşturma](#bir-view-olusturma)
- [Bir Migration Oluşturma](#bir-migration-olusturma)
- [Eloquent ORM](#eloquent-orm)
- [Veri Gösterme](#veri-gosterme)

<a name="kurulum"></a>
## Kurulum

Laravel'i kurmak için [Github Kaynağı'nı](https://github.com/laravel/laravel/archive/master.zip) indirmelisiniz. Daha sonra [Composer'i kurup](http://getcomposer.org), `composer install` komutunu projenizin root (ana) klasöründe çalıştırmalısınız. Bu komutu çalıştırmak, Laravel'i ve Laravel'in gereksinimlerini (dependencies) indirip kuracaktır.

Laravel kurulduktan sonra klasör yapısına göz gezdirin ve Laravel'in nasıl bir yapısı olduğuna bakın. `app` klasörü içerisinde `views`, `controllers`, ve `models` gibi klasörler bulunmaktadır. Projenizi geliştirirken yazacağınız kodların çok büyük bir kısmı bu klasörler içine yazılacaktır. Ayrıca `app/config` klasörü içerisine bakıp size ne tür konfigürasyon ayarları tanımlandığını görebilirsiniz.

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

Şimdi basit bir view dosyası oluşturup, kullanıcı bilgilerini ekrana view üzerinden yazdıracağız. View dosyaları `app/views` klasörü içerisinde bulunmakta olup projenizin HTML dosyalarını barındırır. Şimdi bu klasör içerisine 2 tane dosya oluşturacağız: `layout.blade.php` ve `kullanicilar.blade.php`. Önce `layout.blade.php` dosyamızı oluşturalım:

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

To create a table to hold our data, we'll use the Laravel migration system. Migrations let you expressively define modifications to your database, and easily share them with the rest of your team.

First, let's configure a database connection. You may configure all of your database connections from the `app/config/database.php` file. By default, Laravel is configured to use SQLite, and an SQLite database is included in the `app/database` directory. If you wish, you may change the `driver` option to `mysql` and configure the `mysql` connection credentials within the database configuration file.

Next, to create the migration, we'll use the [Artisan CLI](/docs/artisan). From the root of your project, run the following from your terminal:

	php artisan migrate:make create_users_table

Next, find the generated migration file in the `app/database/migrations` folder. This file contains a class with two methods: `up` and `down`. In the `up` method, you should make the desired changes to your database tables, and in the `down` method you simply reverse them.

Let's define a migration that looks like this:

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

Next, we can run our migrations from our terminal using the `migrate` command. Simply execute this command from the root of your project:

	php artisan migrate

If you wish to rollback a migration, you may issue the `migrate:rollback` command. Now that we have a database table, let's start pulling some data!

<a name="eloquent-orm"></a>
## Eloquent ORM

Laravel ships with a superb ORM: Eloquent. If you have used the Ruby on Rails framework, you will find Eloquent familiar, as it follows the ActiveRecord ORM style of database interaction.

First, let's define a model. An Eloquent model can be used to query an associated database table, as well as represent a given row within that table. Don't worry, it will all make sense soon! Models are typically stored in the `app/models` directory. Let's define a `User.php` model in that directory like so:

	class User extends Eloquent {}

Note that we do not have to tell Eloquent which table to use. Eloquent has a variety of conventions, one of which is to use the plural form of the model name as the model's database table. Convenient!

Using your preferred database administration tool, insert a few rows into your `users` table, and we'll use Eloquent to retrieve them and pass them to our view.

Now let's modify our `/users` route to look like this:

	Route::get('users', function()
	{
		$users = User::all();

		return View::make('users')->with('users', $users);
	});

Let's walk through this route. First, the `all` method on the `User` model will retrieve all of the rows in the `users` table. Next, we're passing these records to the view via the `with` method. The `with` method accepts a key and a value, and is used to make a piece of data available to a view.

Awesome. Now we're ready to display the users in our view!

<a name="displaying-data"></a>
## Displaying Data

Now that we have made the `users` available to our view. We can display them like so:

	@extends('layout')

	@section('content')
		@foreach($users as $user)
			<p>{{ $user->name }}</p>
		@endforeach
	@stop

You may be wondering where to find our `echo` statements. When using Blade, you may echo data by surrounding it with double curly braces. It's a cinch. Now, you should be able to hit the `/users` route and see the names of your users displayed in the response.

This is just the beginning. In this tutorial, you've seen the very basics of Laravel, but there are so many more exciting things to learn. Keep reading through the documentation and dig deeper into the powerful features available to you in [Eloquent](/docs/eloquent) and [Blade](/docs/templates). Or, maybe you're more interested in [Queues](/docs/queues) and [Unit Testing](/docs/testing). Then again, maybe you want to flex your architecture muscles with the [IoC Container](/docs/ioc). The choice is yours!
