# Posta

- [Yapılandırma](#configuration)
- [Basit Kullanım](#basic-usage)
- [Ataşmanların Yazı İçine Gömülmesi](#embedding-inline-attachments)
- [Postaların Sıraya Sokulması](#queueing-mail)
- [Posta & Yerel Geliştirme](#mail-and-local-development)

<a name="configuration"></a>
## Yapılandırma

Laravel popüler [SwiftMailer](http://swiftmailer.org) kitaplığı üzerinden temiz ve basit bir API sağlamaktadır. Posta yapılandırma dosyası `app/config/mail.php`'dir ve sizin SMTP host, port ve kimlik bilgilerizi değiştirmenize, bunun yanında bu kitaplığın yolladığı tüm mesajlar için global bir `from` adresi ayarlamanıza imkan veren seçenekler içermektedir. İstediğiniz herhangi bir SMTP sunucusunu kullanabilirsiniz. Posta göndermek için şayet PHP'nin `mail` fonksiyonunu kullanmak istiyorsanız, yapılandırma dosyasındaki `driver`'ı `mail`'e değiştiriniz. Bir `sendmail` sürücüsü de bulunmaktadır.

<a name="basic-usage"></a>
## Basit Kullanım

Bir e-posta mesajı göndermek için `Mail::send` metodu kullanılabilir:

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->to('falan@numune.com', 'Can Simitci')->subject('Hoş geldiniz!');
	});

Burada `send` metoduna geçilen ilk parametre e-posta gövde metni olarak kullanılacak görünümün ("view"in) ismidir ve ikinci parametre `$data` ise bu görünüme geçilecek veriyi temsil eder. Üçüncü parametremiz e-posta mesajında çeşitli seçenekler belirlemize imkan veren bir bitirme fonksiyonudur.

> **Not:** E-posta görünümlerine mutlaka bir `$message` değişkeni geçilir ve bu değişken bize ataşmanların yazı içine gömülmesi imkanı verir. Dolayısıyla sizin görünüm elemanlarınız arasında bir `message` değişkeni olmaması iyi olur.

Bir HTML görünümüne ek olarak düz metin görünümü kullanmayı da belirtebilirsiniz:

	Mail::send(array('html.view', 'text.view'), $data, $callback);

Veya, `html` ya da `text` keylerini kullanmak suretiyle sadece bir tip görünüm belirleyebilirsiniz:

	Mail::send(array('text' => 'view'), $data, $callback);

E-posta mesajınızda bunlar yanında, karbon kopyalar veya ataşmanlar gibi başka seçenekler de belirtebilirsiniz:

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->from('bizden@numune.com', 'Laravel');

		$message->to('falan@numune.com')->cc('filan@numune.com');

		$message->attach($eklenecekDosya);
	});

Bir mesaja dosya eklediğinizde, bir MIME tipi ve / veya ne adla görüneceğini de belirleyebilirsiniz:

	$message->attach($eklenecekDosya, array('as' => $gorunecekAd, 'mime' => $mime));

> **Not:** Bir `Mail::send` bitirme fonksiyonuna geçilen "message" olgusu, SwiftMailer'in message sınıfını genişleterek, e-posta mesajlarınızı oluşturmak için sınıf üzerinden her türlü metodu çağırabilmenize imkan verir.

<a name="embedding-inline-attachments"></a>
## Ataşmanların Yazı İçine Gömülmesi

Ataşmanların yazı içine gömülmesi tipik olarak zahmetlidir; ama Laravel size e-postalarınıza resimler eklemek ve uygun CID elde etmeniz için pratik bir yol sağlar.

**Bir E-Posta Görünümüne Bir Resim Gömülmesi**

	<body>
		İşte bir resim:

		<img src="<?php echo $message->embed($resimDosyaYolu); ?>">
	</body>

**Bir E-Posta Görünümüne Ham Veri Gömülmesi**

	<body>
		Burada ise ham veriden elde edilen resim görüyoruz:

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

`Mail` sınıfı tarafından e-mail görünümlerine bu `$message` değişkeninin MUTLAKA geçileceğini unutmayın.

<a name="queueing-mail"></a>
## Postaların Sıraya Sokulması

E-mail mesajlarının gönderilmesi uygulamanızın cevap zamanını önemli ölçüde uzatabileceğin için, birçok geliştirici e-posta mesajlarını arka planda gönderilmek üzere kuyruğa sokmayı tercih eder. Laravel, dahili [tekleşmiş kuyruk API](/docs/queues)'sini kullanarak bunu kolaylaştırır. Bir e-posta mesajını kuyruğa sokmak için tek yapmanız gereken şey, `Mail` sınıfının `queue` metodunu kullanmaktır:

**Bir Mail Mesajının Kuyruğa Sokulması**

	Mail::queue('emails.welcome', $data, function($message)
	{
		$message->to('falan@numune.com', 'Can Simitci')->subject('Hoş geldiniz!');
	});

`later` metodunu kullanarak mail mesajınızın gönderilmek için bekleyeceği saniye sayısını da belirleyebilirsiniz:

	Mail::later(5, 'emails.welcome', $data, function($message)
	{
		$message->to('falan@numune.com', 'Can Simitci')->subject('Hoş geldiniz!');
	});

Mesajı yollamak için belirli bir kuyruk veya "tüpgeçit" belirlemek istiyorsanız bunu `queueOn` ve `laterOn` metodlarını kullanarak gerçekleştirebilirsiniz:

	Mail::queueOn('queue-name', 'emails.welcome', $data, function($message)
	{
		$message->to('falan@numune.com', 'Can Simitci')->subject('Hoş geldiniz!');
	});

<a name="mail-and-local-development"></a>
## Posta & Yerel Geliştirme

E-posta gönderen bir uygulama geliştirilirken, genelde lokal veya geliştirme ortamında mesaj göndermenin devre dışı bırakılması arzu edilmektedir. bunu yapmak için, ya `Mail::pretend` metodunu çağırın ya da `app/config/mail.php` yapılandırma dosyanızdaki `pretend` seçeneğini `true` olarak ayarlayın. Mailer `pretend` modunda olduğu zaman, mesajlar alıcıya gönderilmek yerine uygulamanızın günlük dosyalarına yazılacaktır.

**Taklit Posta Modunun Etkinleştirilmesi**

	Mail::pretend();
