# Kurulum

- [Composer Kurulumu](#composer-kurulumu)
- [Laravel Yükleme](#laravel-yukleme)
- [Sunucu Gereksinimleri](#sunucu-gereksinimleri)
- [Yapılandırma](#yapilandirma)
- [İzinler](#izinler)
- [Yollar](#yollar)
- [Zarif URL'ler](#zarif-urller)

<a name="composer-kurulumu"></a>
## Composer Kurulumu

Laravel bağımlılıklarını yönetmek için [Composer](http://getcomposer.org) kullanır. Öncelikle `composer.phar` dosyasını indiriniz. PHAR arşivini yerel proje dosyanızda tutabileceğiniz gibi `usr/local/bin` içerisine taşıyarak sisteminizde evrensel olarak da kullanabilirsiniz. Windows'ta Composer [Windows kurulumu](https://getcomposer.org/Composer-Setup.exe)nu kullanabilirsiniz.

<a name="laravel-yukleme"></a>
## Laravel Yükleme

Composer kuruldu ise, Laravel framework'ün [son sürümü](https://github.com/laravel/laravel/archive/master.zip)nü indirip, içeriğini sunucunuzdaki bir dizine çıkarınız. Ardından, Laravel uygulamanızın ana dizininde, Laravel gereksinimlerini yüklemek için, `php composer.phar install` (veya `composer install`) komutunu çalıştırınız. Bu işlemin başarıyla tamamlanabilmesi için sunucunuzda [Git](http://git-scm.com/downloads) yüklü olması gerekmektedir.

Laravel kurulumu tamamlandıysa `php composer.phar update` komutu ile framework güncellemesi yapabilirsiniz.

- Composer kurulumu için Türkçe kaynak: [Composer’ı Evrensel Olarak Kuralım](http://www.sinaneldem.com.tr/composeri-evrensel-olarak-kuralim/)
- Laravel kurulumu için Türkçe kaynak: [Laravel Framework Kurulumu](http://www.sinaneldem.com.tr/laravel-framework-kurulumu/)

<a name="sunucu-gereksinimleri"></a>
## Sunucu Gereksinimleri

Laravel framework'un birkaç sistem gereksinimi bulunmaktadır:

- PHP >= 5.3.7
- MCrypt PHP Eklentisi

<a name="yapilandirma"></a>
## Yapılandırma

Laravel'in çalışabilmesi için neredeyse hiç yapilandırma ayarı gerekmez. Geliştirmeye başlamak için serbestsiniz! Ancak `app/config/app.php` dosyasını ve dokümantasyonunu gözden geçirebilirsiniz. Buradaki `timezone` (saat dilimi) ve `locale` (lisan) gibi değerleri uygulamanızın ihtiyaçlarına göre düzenleyebilirsiniz.

> **Not:** Mutlaka ayarlamanız gereken bir seçenek olan `anahtar` `app/config/app.php` dosyası içerisindedir. Bu değer rastgele seçilmiş 32 karakterden oluşmalıdır. Bu anahtar şifreleme değerlerinde kullanılmaktadır ve eğer doğru ayarlanmazsa güvenli olmayacaktır. `php artisan key:generate` artisan komutu ile bu değeri kolayca sağlayabilirsiniz.

<a name="izinler"></a>
### İzinler
Laravel `app/storage` dizin içeriğinin web sunucu tarafından yazılabilir olmasını gerektirmektedir.

<a name="yollar"></a>
### Yollar

Framework dizin yollarının birkaçı yapılandırılabilirdir. Bu dizin yollarını değiştirebilmek için `bootstrap/paths.php` dosyasını gözden geçiriniz.

> **Not:** Laravel kodlarınızı koruyacak biçimde tasarlanmıştır bu sebeple yerel dosyalarınız uygulamanızdan farklı olarak public dizini içinde yer alır. Önerilen, public dizinizi documentRoot (sunucu temel dizini / root) içine yerleştirmeniz veya public dizin içeriğini ana dizininize kopyalayıp Laravel'in tüm dosyalarını ana dizin dışına yerleştirmenizdir.

<a name="zarif-urller"></a>
## Zarif URL'ler

Framework ile beraber gelen `public/.htaccess` dosyası URL'lerin `index.php` olmadan kullanımına olanak sağlamaktadır. Laravel uygulamanızın sunumu için Apache kullanıyorsanız `mod_rewrite` modülünün etkin olduğundan emin olunuz.

Eğer Laravel ile birlikte gelen `.htaccess` dosyası Apache kurulumunuz ile işlev göstermezse, bunu deneyiniz:

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteRule ^(.+)/$ http://%{HTTP_HOST}/$1 [R=301,L]

	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]
