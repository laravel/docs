# Sayfalandırma

- [Yapılandırma](#yapilandirma)
- [Kullanım](#usage)
- [Sayfalandırma Linkleri Ekleme](#appending-to-pagination-links)

<a name="yapilandirma"></a>
## Yapılandırma

Diğer çatılarda(frameworkler'de), sayfalandırma oldukça sıkıntılı olabilir. Laravel bu işi çocuk oyuncağı gibi yapar. `app/config/view.php` dosyasında bir tek ayar dosyası vardır. `pagination` seçeneği sayfalandırma bağlantıları(links) oluşturmak için kullanılması gereken görünümü(view) belirtir. Varsayılan olarak, Laravel iki görünüm(view) içerir.

Mevcut sayfada `pagination::slider` görünümde(view'de) akıllı "dizi(range)" bağlantılarını göstermekte olurken, `pagination::simple` görünümü(view'ı) sadece "önceki" ve "sonraki" butonlarını gösterecektir. **Her iki görünümde(view) Twitter Bootstrap ile uyumludur**

<a name="usage"></a>
## Kullanım

Birkaç sayfalandırma yolu bulunmaktadır. En kolayı ise `paginate` metodunu veya Eloquent model kullanarak.

**Sayfalandırma Veritaban Sonuçları**

	$uyeler = DB::table('uyeler')->paginate(15);

Ayrıca [Eloquent](/docs/eloquent) modeller ile sayfalandırma yapabilirsiniz:

**Eloquent Model Sayfalandırma**

	$uyeler = User::where('oylar', '>', 100)->paginate(15);

`paginate` metodundan geçen argüman sayfa başı görüntülemek istediğiniz öğelerin sayısıdır.Bir kez sonuçları aldıktan sonra görünümde(view'da) görüntüleyebilir ve `links` metodunu kullanarak sayfalandırma bağlantıları(links) oluşturabilirsiniz:

	<div class="container">
		<?php foreach ($uyeler as $uye): ?>
			<?php echo $uye->isim; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $uyeler->links(); ?>

Sayfalandırma sistemi oluşturmak işte bu kadar! Unutmayın,mevcut sayfa için çatıya(framework'e) bilgi vermedik. Laravel bunu sizin için otomatik olarak belirledi.

Ayrıca aşağıdaki metodlarla ek olarak sayfalandırma bilgisine erişebilirsiniz:

- `getCurrentPage`
- `getLastPage`
- `getPerPage`
- `getTotal`
- `getFrom`
- `getTo`

Bazen geçen(passing) dizi öğelerini, elle sayfalandırma oluşturmayı dileyebilirsiniz. Bunu yapmak için `Paginator::make` methodunu kullanınız:

**Elle Sayfalandırıcı Oluşturmak**

	$sayfalandirici = Paginator::make($ogeler, $toplamOgeler, $sayfaBasi);

<a name="appending-to-pagination-links"></a>
## Sayfalandırma Linkleri Ekleme

You can add to the query string of pagination links using the `appends` method on the Paginator:

	<?php echo $uyeler->appends(array('sira' => 'oylar'))->links(); ?>

Buna benzer URL'ler üretecektir:

	http://ornek.com/birsey?sayfa=2&sira=oylar
