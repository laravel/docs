# Redis

- [Giriş](#introduction)
- [Yapılandırma](#configuration)
- [Kullanım](#usage)
- [Pipeline Kullanma](#pipelining)

<a name="introduction"></a>
## Giriş

[Redis](http://redis.io) açık kaynak, gelişmiş bir anahtar-değer deposudur. Anahtarlar [stringler](http://redis.io/topics/data-types#strings), [hashler](http://redis.io/topics/data-types#hashes), [listeler](http://redis.io/topics/data-types#lists), [kümeler](http://redis.io/topics/data-types#sets) ve [sıralı kümeler](http://redis.io/topics/data-types#sorted-sets) taşıyabildikleri için sıklıkla bir veri yapısı sunucusu olarak da ifade edilmektedir.

> **Not:** Eğer PECL aracılığıyla yüklenmiş Redis PHP eklentiniz varsa, `app/config/app.php` dosyanızda Redis için kullanılan lakabın ismini değiştirmeniz gereklidir.

<a name="configuration"></a>
## Yapılandırma

Uygulamanızdaki Redis yapılandırması **app/config/database.php** dosyasında saklanır. Bu dosya içerisinde, uygulamanız tarafından kullanılan Redis sunucularını içeren bir **redis** dizisi göreceksiniz:

	'redis' => array(

		'cluster' => true,

		'default' => array('host' => '127.0.0.1', 'port' => 6379),

	),

Geliştirme için bu "default" sunucu yapılandırması yeterlidir. Yine de siz ortamınıza göre bu diziyi değiştirmekte serbestsiniz. Sadece her Redis sunucusuna bir ad verin ve bu sunucu tarafından kullanılan ana bilgisayarı (host) ve bağlantı noktasını (port) belirtin.

Buradaki `cluster` seçeneği Laravel Redis istemcisine Redis düğümleriniz arasında istemci taraflı bölümlendirme (sharding) yapmasını söylemektedir. Böylece siz düğüm havuzu ve büyük miktarda kullanılabilir RAM oluşturabilirsiniz. Bununla birlikte istemci taraflı bölümlendirmenin başarısızlık durumlarını halledemediğini unutmayın. Bu nedenle, istemci taraflı bölümlendirme, esasında başka bir asıl veri deposunda olup da önbelleğe alınmış veriler için uygundurlar.

<a name="usage"></a>
## Kullanım

Bir Redis olgusunu `Redis::connection` metodunu çağırarak getirebilirsiniz:

	$redis = Redis::connection();

Bu size "default" Redis sunucusunun bir olgusunu verecektir. Eğer sunucu öbekleme (clustering) kullanmıyorsanız, Redis yapılandırmanızda tanımlanan belirli bir sunucuyu getirmek için `connection` metodunda parametre olarak o sunucunun adını geçersiniz:

	$redis = Redis::connection('digerbirsunucu');

Redis istemci olgusu oluşturduktan sonra, artık bu olguya her türlü [Redis komutu](http://redis.io/commands) verebiliriz. Laravel Redis sunucusuna komut geçerken sihirli metodlar tekniğini kullanır:

	$redis->set('isim', 'Taylor');

	$isim = $redis->get('isim');

	$degerler = $redis->lrange('isimler', 5, 10);

Görüldüğü gibi komut parametreleri basitçe sihirli metodlara geçilmektedir. Tabii ki siz sihirli metod tekniğini kullanmak zorunda değilsiniz, `command` metodunu kullanarak da sunucuya komut geçebilirsiniz:

	$degerler = $redis->command('lrange', array(5, 10));

Komutlarınızı sadece "default" bağlantıda çalıştıracağınız zaman, direkt `Redis` sınıfındaki statik sihirli metodları kullanın:

	Redis::set('isim', 'Taylor');

	$isim = Redis::get('isim');

	$degerler = Redis::lrange('isimler', 5, 10);

> **Not:** Redis [Önbellekleme](/docs/cache) ve [Oturum](/docs/session) sürücüleri Laravel'de mevcuttur.

<a name="pipelining"></a>
## Pipeline Kullanma

Bir operasyonda sunucuya birçok komut göndermeniz gerektiğinde pipeline kullanılmalıdır. Bunu yapmak için `pipeline` komutunu kullanın:

**Sunucularınıza Birden Çok Komutun Döşenmesi**

	Redis::pipeline(function($pipe)
	{
		for ($i = 0; $i < 1000; $i++)
		{
			$pipe->set("key:$i", $i);
		}
	});
