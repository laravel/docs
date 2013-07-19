# Güvenlik

- [Yapılandırma](#yapilandirma)
- [Şifrelerin Saklanması](#storing-passwords)
- [Kullanıcı Kimliklerinin Doğrulanması](#authenticating-users)
- [Elle Kullanıcı Girişi](#manually)
- [Rotaların Korunması](#protecting-routes)
- [HTTP Basit Kimlik Doğrulaması](#http-basic-authentication)
- [Şifre Hatırlatıcıları & Sıfırlama](#password-reminders-and-reset)
- [Kriptolama](#encryption)

<a name="yapilandirma"></a>
## Yapılandırma

Laravel, kimlik doğrulanması işlerini çok basit hale getirmeyi amaçlamaktadır. Aslında, hemen her şey hazır yapılandırılmış durumdadır. Kimlik doğrulaması yapılandırma dosyası `app/config/auth.php` yerleşiminde bulunmaktadır ve kimlik doğrulama araçlarının davranışlarına nasıl ince ayarlar yapılacağı üzerine iyi belgelenmiş çeşitli seçenekler barındırır.

Ön tanımlı olarak, Laravel `app/models` dizininde bir `User` modeli içermektedir ve bu model ön tanımlı Eloquent kimlik doğrulama sürücüsü ile kullanıma hazırdır. Bu modelin şemasını oluştururken şifre alanının en az 60 karakter olmasını temin etmeniz gerektiğini unutmayın.

Şayet sizin uygulamanız Eloquent kullanmıyorsa, Laravel sorgu oluşturucusunu kullanan `database` kimlik doğrulama sürücüsünü kullanabilirsiniz.

<a name="storing-passwords"></a>
## Şifrelerin Saklanması

Laravel'deki `Hash` sınıfı güvenli Bcrypt karıştırması (hashing) sağlar:

**Bcrypt Kullanılarak Bir Şifrenin Karıştırılması**

	$parola = Hash::make('secret');

**Bir Şifrenin Karıştırılmışa Göre Doğrulanması**

	if (Hash::check('secret', $karistirilmisParola))
	{
		// Parola doğrulanmıştır...
	}

**Bir Şifrenin Yeniden Karıştırılması Gerekip Gerekmediğinin Yoklanması**

	if (Hash::needsRehash($karistirilmis))
	{
		$karistirilmis = Hash::make('secret');
	}

<a name="authenticating-users"></a>
## Kullanıcı Kimliklerinin Doğrulanması

Bir kullanıcının uygulamanıza girişi için `Auth::attempt` metodunu kullnabilirsiniz.

	if (Auth::attempt(array('email' => $email, 'password' => $parola)))
	{
		return Redirect::intended('pano');
	}

Buradaki `email`'in gerekli bir seçenek değil, sadece örnek olsun diye kullanılmış olduğunu bilin. Veritabanınızda bir "kullanıcı adı"na ("username"e) karşılık gelen sütunu kullanmanız gerekiyor. `Redirect::intended` fonksiyonu, kullanıcıları kimlik doğrulama filtresi tarafından yakalanmadan önce erişmeye çalıştıkları URL'ye yönlendirecektir. Kullanıcının önceden girmeye çalıştığı bir url olmayan durumlarda kullanılabilsin diye bu metoda bir dönüş URI parametresi verilebilir.

`attempt` metodu çağrıldığında, `auth.attempt` [olayı](/docs/events) ateşlenecektir. Şayet kimlik doğrulama girişimi başarılı olur ve kullanıcı giriş yapmış olursa, `auth.login` olayı da ateşlenecektir.

Bir kullanıcının uygulamanıza zaten giriş yapmış olduğunu tayin etmek için `check` metodunu kullanabilirsiniz:

**Bir Kullanıcının Doğrulanmış Olup Olmadığının Tayin Edilmesi**

	if (Auth::check())
	{
		// Kullanıcı giriş yapmıştır...
	}

Şayet uygulamanıza "beni hatırla" işlevselliği vermek istiyorsanız, `attempt` metoduna ikinci parametre olarak `true` geçebilirsiniz, böylece bu kullanıcı süresiz olarak "doğrulanmış" tutulacaktır (yada manuel olarak çıkış işlemi yapıncaya kadar):

**Bir Kullanıcının Kimliğinin Doğrulanması ve "Hatırlanması"**

	if (Auth::attempt(array('email' => $email, 'password' => $parola), true))
	{
		// Bu kullanıcı hatırlanacak...
	}

**Not:** `attempt` metodu `true` döndürürse, kullanıcı uygulamanıza girmiş kabul edilir.

Kimlik doğrulama sorgusuna ekstra şartlar da ekleyebilirsiniz:

**Bir Kullanıcının Ek Şartlara Göre Doğrulanması**

    if (Auth::attempt(array('email' => $email, 'password' => $parola, 'aktif' => 1)))
    {
        // Bu kullanıcı aktiftir, üyeliği askıya alınmış değildir ve mevcuttur.  
    }

Bir kullanıcının kimliği doğrulandıktan sonra, bu kullanıcının model / kaydına ulaşabilirsiniz:

**Login Yapmış Kullanıcıya Erişme**

	$email = Auth::user()->email;

Bir kullanıcıyı sadece ID'i ile uygulamanıza giriş yaptırtmak için `loginUsingId` metodunu kullanın:

	Auth::loginUsingId(1);

`validate` metodu gerçekte uygulamaya giriş yapılmaksızın bir kullanıcının kimlik bilgilerinin geçerlilik denetiminden geçirilmesine imkan verir:

**Login Olmaksızın Kullanıcı Bilgilerinin Geçerlilik Denetimi**

	if (Auth::validate($kimlikbilgileri))
	{
		//
	}

Bir kullanıcıyı uygulamanıza tek bir istek için giriş yapmak için de `once` metodunu kullanabilirsiniz. Bu durumda oturum veya çerezler kullanılmayacaktır.

**Bir Kullanıca Tek Bir İstek İçin Giriş Yapma**

	if (Auth::once($kimlikbilgileri))
	{
		//
	}

**Bir Kullanıcıya Uygulamadan Çıkış Yapma**

	Auth::logout();

<a name="manually"></a>
## Elle Kullanıcı Girişi

Şayet, mevcut bir kullanıcı olgusunu uygulamanıza giriş yaptırmak istiyorsanız, bu olguda `login` metodunu çağırmanız yeterlidir:

	$uye = Uye::find(1);

	Auth::login($uye);

Bu yöntem, bir kullanıcıyı `attempt` metodu kullanarak kimlik bilgileri ile giriş yaptırmaya eşdeğerdir.

<a name="protecting-routes"></a>
## Rotaların Korunması

Belli bir rotaya sadece kimliği doğrulanmış kullanıcıların erişebilmesini sağlamak amacıyla rota filtreleri kullanılabilir. Laravel ön tanımlı olarak `auth` filtresi sağlamıştır ve `app/filters.php` içinde tanımlanmıştır.

**Bir Rotanın Korunması**

	Route::get('profil', array('before' => 'auth', function()
	{
		// Sadece kimliği doğrulanmış üyeler girebilir...
	}));

### CSRF Koruması

Laravel, uygulamanızı siteler arası istek sahtekarlıklarından (cross-site request forgeries [CSRF]) korumak için kolay bir metod sağlamaktadır.

**Forma CSRF Jetonunun Eklenmesi**

    <input type="hidden" name="_token" value="<?php echo csrf_token(); ?>">

**Gönderilmiş CSRF Jetonunun Geçerlilik Yoklaması**

    Route::post('register', array('before' => 'csrf', function()
    {
        return 'Geçerli bir CSRF jetonu verdiniz!';
    }));

<a name="http-basic-authentication"></a>
## HTTP Basit Kimlik Doğrulaması

HTTP Basit Kimlik Doğrulaması, kullanıcıları özel bir "giriş" sayfası açmadan uygulamanıza giriş yapabilmeleri için hızlı bir yoldur. Bunun için, rotanıza `auth.basic` filtresi tutturun:

**HTTP Basit İle Bir Rotanın Korunması**

	Route::get('profil', array('before' => 'auth.basic', function()
	{
		// Sadece kimliği doğrulanmış üyeler girebilir...
	}));

Ön tanımlı olarak, bu `basic` filtresi kimlik doğrulaması yaparken kullanıcı kaydındaki `email` sütununu kullanacaktır. Siz başka bir sütunu kullanmak istiyorsanız, `basic` metoduna birinci parametre olarak bu sütunun adını geçirin:

	return Auth::basic('uyeismi');

HTTP Basit Kimlik Doğrulamasını oturumda kullanıcı tanıtıcı bir çerez ayarlamadan da kullanabilirsiniz, bu daha çok API kimlik doğrulamalarında işe yarayacaktır. Bunu yapmak için, `onceBasic` metodu döndüren bir filtre tanımlayın:

**Durum Bilgisi Olmaksızın Bir HTTP Basit Filtresi Ayarlanması**

	Route::filter('basic.once', function()
	{
		return Auth::onceBasic();
	});

<a name="password-reminders-and-reset"></a>
## Şifre Hatırlatıcıları & Sıfırlama

### Şifre Hatırlatıcı Göndermek

Çoğu web uygulaması, kullanıcılarına unutulmuş şifrelerini sıfırlayacak bir yol verir. Her uygulamada bunu tekrar tekrar  yapmaya zorlamak yerine Laravel size şifre hatırlatıcı mektup gönderme ve şifre sıfırlaması yapılması için pratik metodlar sağlar. Başlamak için sizin `User` modelinizin `Illuminate\Auth\Reminders\RemindableInterface` sözleşmesini yerine getirdiğini doğrulayın. Tabii ki, Laravel'le gelen `User` modeli bu arayüz kontratını zaten yerine getirmektedir.

**RemindableInterface Yürütme İşlemi**

	class User extends Eloquent implements RemindableInterface {

		public function getReminderEmail()
		{
			return $this->email;
		}

	}

Daha sonra, şifre sıfırlama jetonlarının saklanacağı bir tablo oluşturulmalıdır. Bu tablo için bir migrasyon üretmek için yapacağınız tek şey `auth:reminders` Artisan komutunu çalıştırmaktır:

**Hatırlatıcı Tablo Migrasyonunun Üretilmesi**

	php artisan auth:reminders

	php artisan migrate

Bir şifre hatırlatıcı göndermek için, `Password::remind` metodunu kullanabiliriz:

**Bir Şifre Hatırlatıcı Gönderme**

	Route::post('password/remind', function()
	{
		$kimlikbilgileri = array('email' => Input::get('email'));

		return Password::remind($kimlikbilgileri);
	});

`Password::remind` metoduna geçirilen parametrelerin `Auth::attempt` metoduna geçirilenle aynı olduğuna dikkat edin. Bu metod `User`'ı getirecek ve e-mail aracılığı ile ona bir şifre sıfırlama linki gönderecektir. Bu e-mail görünümüne, şifre sıfırlama formuna link oluşturmakta kullanılabilcek bir `token` değişkeni geçilecektir. Bu görünüme `user` nesnesi de geçilecektir.

> **Not:** `auth.reminder.email` yapılandırma seçeneğini değiştirmek suretiyle e-mail mesajı olarak hangi görünümün kullanılacağını belirleyebilirsiniz. Tabii ki, ön tanımlı bir görünüm mevcuttur.

`remind` metoduna ikinci bir parametre olarak bir bitirme fonksiyonu (Closure) geçerek, kullanıcıya gönderilecek mesaj olgusunu değiştirebilirsiniz:

	return Password::remind($kimlikbilgileri, function($mesaj, $uye)
	{
		$mesaj->subject('Şifre Hatırlatıcınız');
	});

Ayrıca, `remind` metodunun sonuçlarını doğrudan bir rotadan döndürdüğümüze dikkat ediniz. Ön tanımlı olarak, `remind` metodu mevcut URI'ye bir `Redirect` döndürecektir. Şifre sıfırlamaya çalışılırken eğer bir hata oluşursa, oturuma bir `error` değişkeni, bir de `reminders` dil dosyasından bir dil satırı çekmekte kullanılabilecek bir `reason` değişkeni flaş tarzında gönderilir. Şifre sıfırlama başarılı olursa bu sefer oturuma bir `success` değişkeni gönderilecektir. Bu durumda şifre sıfırlama form görünümünüz şöyle bir şey olacaktır:

	@if (Session::has('error'))
		{{ trans(Session::get('reason')) }}
	@elseif (Session::has('success'))
		Şifre sıfırlaması olan bir e-mail gönderildi.
	@endif

	<input type="text" name="email">
	<input type="submit" value="Hatırlatıcı Gönder">

### Şifrelerin Sıfırlanması

Bir kullanıcı hatırlatma e-mailindeki sıfırlama linkini tıkladıktan sonra, bir `password` ve `password_confirmation` alanı yanında gizli bir `token` alanı da olan bir forma yönlendirilmelidir. Aşağıda şifre sıfırlama formu için bir rota örneği görülüyor:

	Route::get('password/reset/{token}', function($token)
	{
		return View::make('auth.reset')->with('token', $token);
	});

Ve, bir şifre sıfırlama formu görünümü de şuna benzeyebilir:

	@if (Session::has('error'))
		{{ trans(Session::get('reason')) }}
	@endif

	<input type="hidden" name="token" value="{{ $token }}">
	<input type="text" name="email">
	<input type="password" name="password">
	<input type="password" name="password_confirmation">

Tekrar hatırlatmakta yarar var, şifre sıfırlaması sırasında Laravel tarafından saptanabilen herhangi bir hatayı göstermek için `Session`'u kullanıyoruz. Artık sıfırlama işini yapacak bir `POST` rotası tanımlayabiliriz:

	Route::post('password/reset/{token}', function()
	{
		$kimlikbilgileri = array('email' => Input::get('email'));

		return Password::reset($kimlikbilgileri, function($uye, $password)
		{
			$uye->password = Hash::make($password);

			$uye->save();

			return Redirect::to('home');
		});
	});

Şifre sıfırlama başarılı olursa `User` (üye) olgunuz ve şifre sizin bitirme fonksiyonunuza geçilecek, böylece burada gerçek save oparasyonu yapabileceksiniz. Daha sonra, `reset` metodu tarafından döndürülecek olan bitirme fonksiyonundan ya bir `Redirect` döndürebilirsiniz veya başka bir tipte cevap döndürebilirsiniz. Bu `reset` metodunun istekte geçerli bir `token`, geçerli kimlik bilgileri ve birbirine uyan şifreler olup olmadığını otomatik olarak kontrol ettiğini unutmayın.

Ayrıca, `remind` metoduna benzer şeklilde, şifre resetlemesi sırasında bir hata oluşması durumunda `reset` metodu da bir `error` ve bir `reason` eşliğinde mevcut URI'ye bir `Redirect` döndürecektir.

<a name="encryption"></a>
## Kriptolama

Laravel, mcrypt PHP uzantısı aracılığıyla güçlü AES-256 kriptolama imkanı sağlamaktadır:

**Bir Değerin Kriptolanması**

	$kriptolu = Crypt::encrypt('secret');

> **Not:** `app/config/app.php` dosyasının `key` seçeneğinde 32 karakterli rasgele string ayarladığınızdan emin olun. Aksi Takdirde kriptolanmış değerler güvenli olmayacaktır.

**Kriptolu Bir Değerin Çözülmesi**

	$cozuk = Crypt::decrypt($kriptoluDeger);

Ayrıca, kriptocu tarafından kullanılan cipher ve mod da ayarlayabilirsiniz

**Cipher ve Mod Ayarlanması**

	Crypt::setMode('crt');

	Crypt::setCipher($cipher);
