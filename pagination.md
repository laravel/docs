# Sayfalandırma

- [Yapılandırma](#yapilandirma)
- [Kullanım](#usage)
- [Sayfalandırma Linkleri Ekleme](#appending-to-pagination-links)

<a name="yapilandirma"></a>
## Yapılandırma

Diğer çatılarda (frameworkler'de), sayfalandırma oldukça sıkıntılı olabilir. Laravel bu işi çocuk oyuncağı gibi yapar. `app/config/view.php` dosyasında bir tek yapılandırma seçeneği bulunmaktadır. `pagination` seçeneği sayfalandırma bağlantıları (links) oluşturmak için kullanılması gereken görünümü (view) belirtir. Varsayılan olarak, Laravel iki görünüm içerir.

`pagination::slider` görünümü mevcut sayfaya dayalı olarak akıllı bir bağlantı aralığı gösterirken, `pagination::simple` görünümü sadece "önceki" ve "sonraki" butonlarını gösterecektir. **Her iki görünüm de Twitter Bootstrap ile uyumludur**

<a name="usage"></a>
## Kullanım

Öğeleri sayfalandırmak için çeşitli yollar vardır. En basiti sorgu oluşturucusunda veya bir Eloquent modelinde `paginate` metodunu kullanmaktır.

**Veritabanı Sonuçlarının Sayfalandırılması**

	$uyeler = DB::table('uyeler')->paginate(15);

[Eloquent](/docs/eloquent) modellerini de sayfalandırabilirsiniz:

**Bir Eloquent Modelinin Sayfalandırılması**

	$uyeler = User::where('oylar', '>', 100)->paginate(15);

`paginate` metodundan geçen argüman sayfa başı görüntülemek istediğiniz öğelerin sayısıdır. Bir kez sonuçları aldıktan sonra görünümde görüntüleyebilir ve `links` metodunu kullanarak sayfalandırma bağlantıları oluşturabilirsiniz:

	<div class="container">
		<?php foreach ($uyeler as $uye): ?>
			<?php echo $uye->isim; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $uyeler->links(); ?>

Sayfalandırma sistemi oluşturmak işte bu kadar! Unutmayın, mevcut sayfa için çatıya bilgi vermedik. Laravel bunu sizin için otomatik olarak belirledi.

Ayrıca aşağıdaki metodlarla ek olarak sayfalandırma bilgisine erişebilirsiniz:

- `getCurrentPage`
- `getLastPage`
- `getPerPage`
- `getTotal`
- `getFrom`
- `getTo`

Bazen bir sayfalandırma olgusunu kendiniz bir öğeler dizisi geçerek oluşturmak isteyebilirsiniz. Bunu yapmak için `Paginator::make` methodunu kullanınız:

**Elle Sayfalandırıcı Oluşturmak**

	$sayfalandirici = Paginator::make($ogeler, $toplamOgeler, $sayfaBasi);

<a name="appending-to-pagination-links"></a>
## Sayfalandırma Linklerine Ekleme Yapmak

Sayfalandırıcı üzerinde `appends` methodunu kullanarak sayfalandırma linklerinize sorgu katarı (query string) ekleyebilirsiniz:

	<?php echo $uyeler->appends(array('sira' => 'oylar'))->links(); ?>

Bu kod, sayfalandırma linkine "&sira=oylar" ekleyecek ve şöyle bir URL üretecektir:

	http://ornek.com/birsey?sayfa=2&sira=oylar
