# Artisan CLI

- [Giriş](#giris)
- [Kullanım](#kullanim)

<a name="giris"></a>
## Giriş

Artisan, Laravel içerisinde gelen CLI'ın (Command-line Interface) adıdır. Artisan size uygulamanızı geliştirirken birçok yardımcı komut sağlar. Artisan güçlü Symfony Console component üzerinden geliştirilmiştir.

<a name="kullanim"></a>
## Kullanım

Tüm Artisan komutlarını görmek için `list` komutunu kullanabilirsiniz:

**Tüm Kullanılabilir Komutları Listelemek**

	php artisan list

Tüm komutların özel bir "yardım" ekranı vardır ve komut hakkındaki argüman sırası ile ayarlar gibi bilgilerin açıklanmasını sağlar. Yardım ekranını görmek için komutu yazmadan önce `help` kullanın:

**Bir Komut için Yardım Ekranını Görmek**

	php artisan help migrate

Bir komut kullanırken kullanılacak olan Ortam Ayarları'nı `--env` komutuyla belirleyebilirsiniz:

**Ortam Ayarlarını Belirlemek**

	php artisan migrate --env=local

Ayrıca şuan kullanmakta olduğunuz Laravel'in versiyonunu da `--version` komutunu kullanarak Artisan üzerinden görebilirsiniz:

**Laravel'in Versiyonunu Görmek**

	php artisan --version
