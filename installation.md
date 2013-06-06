# Kurulum

- [Composer Kurulumu](#composer-kurulumu)
- [Laravel Yükleme](#laravel-yukleme)
- [Sunucu Gereksinimleri](#sunucu-gereksinimleri)
- [Ayarlamalar](#ayarlamalar)
- [İzinler](#izinler)
- [Yollar](#yollar)
- [Sevimli URLler](#sevimli-urller)

<a name="composer-kurulumu"></a>
## Composer Kurulumu

Laravel gereksinimlerini düzenlemek için [Composer](http://getcomposer.org) kullanır. Öncelikle `composer.phar` dosyasını indiriniz. PHAR arşivini yerel proje dosyanızda tutabileceğiniz gibi `usr/local/bin` içerisine taşıyarak sisteminizde evrensel olarak da kullanabilirsiniz. Windows'ta Composer [Windows kurulumu](https://getcomposer.org/Composer-Setup.exe)nu kullanabilirsiniz.

<a name="laravel-yukleme"></a>
## Laravel Yükleme

Composer kuruldu ise, Laravel framework'ün [son sürümü](https://github.com/laravel/laravel/archive/master.zip)nü indirip, içeriğini sunucunuzdaki bir dizine çıkarınız. Ardından, Laravel uygulamanızın ana dizininde, Laravel gereksinimlerini yüklemek için, `php composer.phar install` (veya `composer install`) komutunu çalıştırınız. Bu işlemin başarıyla tamamlanabilmesi için sunucunuzda [Git](http://git-scm.com/downloads) yüklü olması gerekmektedir.

Laravel kurulumu tamamlandıysa `php composer.phar update` komutu ile framework güncellemesi yapabilirsiniz.

Composer kurulumu için Türkçe kaynak: [Composer’ı Evrensel Olarak Kuralım](http://www.sinaneldem.com.tr/composeri-evrensel-olarak-kuralim/)
Laravel kurulumu için Türkçe kaynak: [Laravel Framework Kurulumu](http://www.sinaneldem.com.tr/laravel-framework-kurulumu/)

<a name="sunucu-gereksinimleri"></a>
## Sunucu Gereksinimleri

Laravel framework'un birkaç sistem gereksinimi bulunmaktadır:

- PHP >= 5.3.7
- MCrypt PHP Eklentisi

<a name="ayarlamalar"></a>
## Ayarlamalar

Laravel'in çalışabilmesi için neredeyse hiç ayar gerekmez. Geliştirmeye başlamak için serbestsiniz! Ancak `app/config/app.php` dosyasını ve dokümantasyonunu gözden geçirebilirsiniz. Buradaki `Saat Dilimi` ve `lisan` gibi seçenekleri uygulamanızın ihtiyaçlarına göre düzenleyebilirsiniz.

> **Not:** Mutlaka ayarlamanız gereken bir seçenek olan `anahtar` `app/config/app.php` içerisindedir. Bu değer rastgele seçilmiş 32 karakterden oluşmalıdır. Bu anahtar şifreleme değerlerinde kullanılmaktadır ve eğer doğru ayarlanmazsa güvenli olmayacaktır. `php artisan key:generate` artisan komutu ile bu değeri kolayca sağlayabilirsiniz.

<a name="izinler"></a>
### İzinler
Laravel app/storage dizin içeriğinin wen sunucu tarafından yazılabilir olmasını gerektirmektedir.

<a name="yollar"></a>
### Yollar

Framework dizin yollarının birkaçı yapılandırılabilirdir. Bu dizin yollarını değiştirebilmek için `bootstrap/paths.php` dosyasını gözden geçiriniz.

> **Note:** Laravel is designed to protect your application code, and local storage by placing only files that are necessarily public in the public folder.  It is recommended that you either set the public folder as your site's documentRoot (also known as a web root) or to place the contents of public into your site's root directory and place all of Laravel's other files outside the web root.

<a name="sevimli-urller"></a>
## Sevimli URLler

The framework ships with a `public/.htaccess` file that is used to allow URLs without `index.php`. If you use Apache to serve your Laravel application, be sure to enable the `mod_rewrite` module.

If the `.htaccess` file that ships with Laravel does not work with your Apache installation, try this one:

	Options +FollowSymLinks
	RewriteEngine On

	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteRule ^(.+)/$ http://%{HTTP_HOST}/$1 [R=301,L]

	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteRule ^ index.php [L]
