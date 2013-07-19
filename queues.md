# Kuyruklar

- [Yapılandırma](#yapilandirma)
- [Basit Kullanım Şekli](#basic-usage)
- [Kuyruğa Closure Fonksiyonu Sokma](#queueing-closures)
- [Kuyruk Dinleyicileri Çalıştırma](#running-the-queue-listener)
- [Push Kuyrukları](#push-queues)

<a name="yapilandirma"></a>
## Yapılandırma

Laravel'in Queue (kuyruk) bileşeni bir takım farklı kuyruk servisleri için tek bir API sağlamaktadır. Kuyruklar e-mail göndermek gibi zaman harcayan görevleri ileri bir zamana kadar ertelemenize imkan verir ve böylece uygulamanıza yapılan web istekleri büyük ölçüde hızlanır.

Kuyruk yapılandırma dosyası `app/config/queue.php` olarak saklanır. Bu dosyada frameworke dahil edilmiş kuyruk sürücülerinin her birisi için bağlantı yapılandırmaları bulacaksınız. Laravel'deki kuyruk sürücüleri arasında [Beanstalkd](http://kr.github.com/beanstalkd), [IronMQ](http://iron.io), [Amazon SQS](http://aws.amazon.com/sqs) ve senkronize (lokal kullanım için) sürücü yer almaktadır.

Listelenen bu kuyruk sürücüleri için aşağıdaki bağımlılıklar gereklidir:

- Beanstalkd: `pda/pheanstalk`
- Amazon SQS: `aws/aws-sdk-php`
- IronMQ: `iron-io/iron_mq`

<a name="basic-usage"></a>
## Basit Kullanım Şekli

Kuyruğa yeni bir iş itmek için `Queue::push` metodunu kullanın:

**Bir İşin Kuyruğa Sokulması**

	Queue::push('SendEmail', array('message' => $message));

`push` metoduna gerilen ilk parametre işi yapmak için kullanılacak sınıfın adıdır. İkinci parametre işleyiciye geçirilecek veri dizisidir. Bir iş işleyicisi şu şekilde tanımlanmalıdır:

**Bir İş İşleyicisinin Tanımlanması**

	class SendEmail {

		public function fire($is, $veri)
		{
			//
		}

	}

Gerekli olan tek metodun `fire` olduğuna dikkat edin. Bu metod bir `iş` olgusu ve bir de kuyruğa sokulacak `veri` dizisi parametrelerini alır.

Eğer iş'in `fire`'den başka bir metod kullanmasını istiyorsanız, işi sokarken (yani push metodunda) metodu belirleyebilirsiniz:

**Özel Bir İşleyici Metodunun Belirlenmesi**

	Queue::push('SendEmail@send', array('message' => $message));

Bir iş işlendikten sonra kuyruktan silinmelidir. Silme işlemi ilgili `iş` olgusunda `delete` metodu kullanılarak yapılabilir:

**İşlenmiş Bir İşin Silinmesi**

	public function fire($is, $veri)
	{
		// İşi işle...

		$is->delete();
	}

Bir işi tekrar kuyruğa devretmek isterseniz, bunu `release` metodu aracılığıyla yapabilirsiniz:

**Bir İşin Tekrar Kuyruğa Koyulması**

	public function fire($is, $veri)
	{
		// İş sürecini yürüt...

		$is->release();
	}

İş tekrar salınmadan önce kaç saniye bekleneceğini de belirleyebilirsiniz:

	$is->release(5);

İş işlenirken bir istisna oluşursa, otomatik olarak kuyruğa tekrar salınacaktır. `attempts` metodunu kullanarak, işi çalıştırmak için yapılmış olan girişim sayısını da yoklayabilirsiniz:

**Çalıştırma Girişimlerinin Sayısını Yoklama**

	if ($is->attempts() > 3)
	{
		//
	}

İş tanımlayıcılarına da erişebilirsiniz:

**Bir İşin ID'ine Erişme**

	$is->getJobId();

<a name="queueing-closures"></a>
## Kuyruğa Closure Fonksiyonu Sokma

Kuyruğa bir Closure de push edebilirsiniz. Bu, kuyruğa sokulması gerekecek hızlı, basit görevler için çok uygundur:

**Kuyruğa Bir Closure Sokulması**

	Queue::push(function($is) use ($id)
	{
		Account::delete($id);

		$is->delete();
	});

> **Not:** Kuyruğa bir Closure sokarken `__DIR__` ve `__FILE__` sabitleri kullanılmamalıdır.

Iron.io [push kuyrukları](#push-queues) kullanılıyorken, Closure'ların kuyruğa sokulmasında daha fazla önlem almalısınız. Kuyruk mesajlarızı alan son nokta, isteğin gerçekten Iron.io'den mi geldiğini doğrulayacak bir jeton yoklaması yapmalıdır. Örneğin, sizin push kuyruk son noktanız şuna benzer bir şey olmalıdır: `https://uygulamaniz.com/queue/receive?token=SecretToken`. Böylece, kuyruk istek sıralamasından önce uygulamanızdaki gizli jetonun değerini kontrol edebilirsiniz.

<a name="running-the-queue-listener"></a>
## Kuyruk Dinleyicileri Çalıştırma

Laravel, kuyruğa itildikçe yeni işler çalıştıran bir Artisan görevi içermektedir. Bu görevi çalıştırmak için `queue:listen` komutunu kullanabilirsiniz:

**Kuyruk Dinleyici Başlatılması**

	php artisan queue:listen

Ayrıca dinleyicinin kullanacağı kuyruk bağlantısını da belirtebilirsiniz:

	php artisan queue:listen connection

Unutmamanız gereken şey, bu görev başlatıldıktan sonra elle durdurulana kadar çalışmaya devam edeceğidir. Kuyruk dinleyicinin çalışmayı durdurmamasından emin olmak için [Supervisor](http://supervisord.org/) gibi bir süreç monitörü kullanabilirsiniz.

Ayrıca her işin çalışmasına izin verilecek zaman süresini (saniye cinsinden) de ayarlayabilirsiniz:

**İş Zaman Aşımı Parametresi Belirleme**

	php artisan queue:listen --timeout=60

Kuyruktaki sadece ilk sıradiki işi yürütmek için `queue:work` komutunu kullanabilirsiniz:

**Kuyruktaki İlk İşin İşleme Geçirilmesi**

	php artisan queue:work

<a name="push-queues"></a>
## Push Kuyrukları

Push kuyrukları size herhangi bir art alan veya arka plan dinleyici çalıştırmaksızın güçlü Laravel 4 kuyruk araçlarını kullanmanıza imkan verir. Push kuyrukları şu anda sadece [Iron.io](http://iron.io) sürücüsü tarafından desteklenmektedir. Başlamak için önce bir Iron.io hesabı oluşturun ve Iron kimlik bilgilerinizi `app/config/queue.php` yapılandırma dosyasına ekleyin.

Daha sonra, yeni push edilmiş kuyruk işlerini alacak bir URL son noktasını kayda geçirmek için `queue:subscribe` Artisan komutunu kullanabilirsiniz:

**Bir Push Kuyruk Aboneliğinin Kayda Geçirilmesi**

	php artisan queue:subscribe queue_name http://falan.com/queue/receive

Şimdi, sizin Iron panonuza giriş yaptığınız zaman, yeni push kuyruğunuzu ve abone olunan URL'yi göreceksiniz. Verilen bir kuyruk için istediğiniz kadar çok URL kaydedebilirsiniz. Sonra da, `queue/receive` son noktanız için bir rota oluşturun ve `Queue::marshal` metodundan cevap döndürün:

	Route::post('queue/receive', function()
	{
		return Queue::marshal();
	});

Doğru iş işleyici sınıfının ateşlenmesiyle `marshal` metodu ilgilenecektir. Push kuyruğundaki işleri ateşlemek için, konvansiyonal kuyruklar için kullanılan aynı `Queue::push` metodunu kullanmanız yeterlidir.
