# Kuyruklar

- [Yapılandırma](#yapilandirma)
- [Basit Kullanım Şekli](#basic-usage)
- [Kuyruğa Closure Fonksiyonu Sokma](#queueing-closures)
- [Kuyruk Dinleyicileri Çalıştırma](#running-the-queue-listener)
- [Push Queues](#push-queues)

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

The first argument given to the `push` metoduna gerilen ilk parametre işi yapmak için kullanılacak sınıfın adıdır. İkinci parametre işleyiciye geçirilecek veri dizisidir. Bir iş işleyicisi şu şekilde tanımlanmalıdır:

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

İş işlenirken bir istisna oluşursa, otomatik olarak kuyguğa tekrar salınacaktır. `attempts` metodunu kullanarak, işi çalıştırmak için yapılmış olan girişim sayısını da yoklayabilirsiniz:

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

Iron.io [push queues](#push-queues) kullanılıyorken, Closure'ların kuyruğa sokulmasında daha fazla önlem almalısınız. Kuyruk mesajlarızı alan son nokta, isteğin gerçekten Iron.io'den mi geldiğini doğrulayacak bir jeton yoklaması yapmalıdır. Örneğin, sizin push kuyruk son noktanız şuna benzer bir şey olmalıdır: `https://yourapp.com/queue/receive?token=SecretToken`. Böylece, kuyruk istek sıralamasından önce uygulamanızdaki gizli jetonun değerini kontrol edebilirsiniz.

<a name="running-the-queue-listener"></a>
## Kuyruk Dinleyicileri Çalıştırma

Laravel, kuyruğa itildikçe yeni işler çalıştıran bir Artisan görevi içermektedir. Bu görevi çalıştırmak için `queue:listen` komutunu kullanabilirsiniz:

**Kuyruk Dinleyici Başlatılması**

	php artisan queue:listen

Ayrıca dinleyicinin kullanacağı kuyruk bağlantısını da belirtebilirsiniz:

	php artisan queue:listen connection

Unutmamanız gereken şey, bu görev başlatıldıktan sonra elle durdurulana kadar çalışmaya devam edeceğidir. Kuyruk dinleyicinin çalışmayı durdurmamasından emin olmak için [Supervisor](http://supervisord.org/) gibi bir süreç monitörü kullanabilirsiniz.

Ayrıca her işin çalışmasına izin verilecek zaman süresini (saniye cinsinden) de ayarlayabilirsiniz:

**Specifying The Job Timeout Parameter**

	php artisan queue:listen --timeout=60

To process only the first job on the queue, you may use the `queue:work` command:

**Processing The First Job On The Queue**

	php artisan queue:work

<a name="push-queues"></a>
## Push Queues

Push queues allow you to utilize the powerful Laravel 4 queue facilities without running any daemons or background listeners. Currently, push queues are only supported by the [Iron.io](http://iron.io) driver. Before getting started, create an Iron.io account, and add your Iron credentials to the `app/config/queue.php` configuration file.

Next, you may use the `queue:subscribe` Artisan command to register a URL end-point that will receive newly pushed queue jobs:

**Registering A Push Queue Subscriber**

	php artisan queue:subscribe queue_name http://foo.com/queue/receive

Now, when you login to your Iron dashboard, you will see your new push queue, as well as the subscribed URL. You may subscribe as many URLs as you wish to a given queue. Next, create a route for your `queue/receive` end-point and return the response from the `Queue::marshal` method:

	Route::post('queue/receive', function()
	{
		return Queue::marshal();
	});

The `marshal` method will take care of firing the correct job handler class. To fire jobs onto the push queue, just use the same `Queue::push` method used for conventional queues.
