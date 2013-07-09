# Helper Functions

- [Arrayler](#arrays)
- [Dizinler](#paths)
- [Yazı İşlemleri](#strings)
- [URL İşlemleri](#urls)
- [Diğer](#miscellaneous)

<a name="arrays"></a>
## Arrayler

### array_add

`array_add` fonksiyonu, verilen anahtar / değer çiftini, eğer daha önce eklenmemişse array'e eklemeye yarar.

	$array = array('foo' => 'bar');

	$array = array_add($array, 'key', 'value');

### array_divide

`array_divide` fonksiyonu, birincisi anahtarlar, ikincisi değerler olacak şekilde iki farklı array döndürür.

	$array = array('foo' => 'bar');

	list($keys, $values) = array_divide($array);

### array_dot
`array_dot` fonksiyonu, çok boyutlu bir array'i derinlikleri 'nokta (dot)' notasyonunu sağlayacak şekilde 1 boyutlu array'e çevirir.

	$array = array('foo' => array('bar' => 'baz'));

	$array = array_dot($array);

	// array('foo.bar' => 'baz');

### array_except

`array_except` fonksiyonu, verilen anahtar / değer çiftini array'den siler.

	$array = array_except($array, array('keys', 'to', 'remove'));

### array_fetch

`array_fetch` fonksiyonu, seçilen anahtar'a göre yeni bir sıkıştırılmış array yaratır.

	$array = array(array('name' => 'Taylor'), array('name' => 'Dayle'));

	var_dump(array_fetch($array, 'name'));

	// array('Taylor', 'Dayle');

### array_first

`array_first` fonksiyonu, verilen doğruluk testine uyan ilk array elemanını döndürür.

	$array = array(100, 200, 300);

	$value = array_first($array, function($key, $value)
	{
		return $value >= 150;
	});

Ayrıca varsayılan bir değer, üçüncü eleman olarak verilebilir.

	$value = array_first($array, $callback, $default);

### array_flatten

`array_flatten` fonksiyonu, çok boyutlu bir array'i tek boyutlu olacak hale getirir.

	$array = array('name' => 'Joe', 'languages' => array('PHP', 'Ruby'));

	$array = array_flatten($array);

	// array('Joe', 'PHP', 'Ruby');

### array_forget

`array_forget` fonksiyonu, verilen array'den 'nokta (dot)' notasyonuna göre girilmiş elemanı siler.

	$array = array('names' => array('joe' => array('programmer')));

	$array = array_forget($array, 'names.joe');

### array_get

`array_get` fonksiyonu, verilen array'den 'nokta (dot)' notasyonuna göre girilmiş elemanı döndürür.

	$array = array('names' => array('joe' => array('programmer')));

	$value = array_get($array, 'names.joe');

### array_only

`array_only` fonksiyonu, array'den sadece verilen anahtar / değer çiftlerini döndürür.

	$array = array('name' => 'Joe', 'age' => 27, 'votes' => 1);

	$array = array_only($array, array('name', 'votes'));

### array_pluck

`array_pluck` fonksiyonu, girilen anahtara göre, yeni bir array döndürür.

	$array = array(array('name' => 'Taylor'), array('name' => 'Dayle'));

	$array = array_pluck($array, 'name');

	// array('Taylor', 'Dayle');

### array_pull

`array_pull` fonksiyonu, girilen anahtara göre yeni bir array döndürür, aynı zamanda döndürdüğü elemanları siler.

	$array = array('name' => 'Taylor', 'age' => 27);

	$name = array_pluck($array, 'name');

### array_set

`array_set` fonksiyonu, 'nokta (dot)' notasyonunu kullanarak çok boyutlu array'lerin elemanlarına değer atamaya yarar.

	$array = array('names' => array('programmer' => 'Joe'));

	array_set($array, 'names.editor', 'Taylor');

### head

Array'in son elemanını döndürür. Metod zincirleme işlemi için çok yararlı.

	$first = head($this->returnsArray('foo'));

### last

Array'in son elemanını döndürür. Metod zincirleme işlemi için çok yararlı.
Return the last element in the array. Useful for method chaining.

	$last = last($this->returnsArray('foo'));

<a name="paths"></a>
## Dizinler

### app_path

`app` klasörünün sisteme göre tam dizin adresini döndürür.

### base_path

Uygulamanın ana klasörünün sisteme göre tam dizin adresini döndürür.

### public_path

`public` klasörünün sisteme göre tam dizin adresini döndürür.

### storage_path

`app/storage` klasörünün sisteme göre tam dizin adresini döndürür.
Get the fully qualified path to the `application/storage` directory.

<a name="strings"></a>
## Yazı İşlemleri

### camel_case

Yazıyı `camelCase` olacak şekilde düzenler.

	$camel = camsel_case('foo_bar');

	// fooBar

### class_basename

Girilen class'ın namespace'ler olmadan sadece adını dondürür.

	$class = class_basename('Foo\Bar\Baz');

	// Baz

### e

Girilen yazıya UTF-8 desteğiyle `htmlentites` fonksiyonunu uygular.

	$entities = e('<html>foo</html>');

### ends_with

Girilen yazının verilen değerle bitip bitmediğine karar verir.

	$value = ends_with('This is my name', 'name');

### snake_case

Yazıyı `snake_case` olacak şekilde düzenler.

	$snake = snake_case('fooBar');

	// foo_bar

### starts_with

Girilen yazının verilen değerle başlayıp başlamadığına karar verir.

	$value = starts_with('This is my name', 'This');

### str_contains

Girilen yazının içinde verilen değerin olup olmadığına karar verir.

	$value = str_contains('This is my name', 'my');

### str_finish

Girilen yazının sonuna verilen değeri ekler. Verilen değerden oluşan ekstraları yok eder.

	$string = str_finish('this/string', '/');

	// this/string/

### str_is

Girilen yazıyla verilen değerin eşleşip eşleşmediğine karar verir. Yıldız işareti (*) genel arama karakteri olarak kullanılabilir.

	$value = str_is('foo*', 'foobar');

### str_plural

Girilen kelimeyi çoğul hale getirir (Sadece ingilizce için geçerli).

	$plural = str_plural('car');

### str_random

Girilen değer kadar uzunlukta rastgele karakterlerden oluşan bir yazı üretir.

	$string = str_random(40);

### str_singular

Girilen kelimeyi tekil hale getirir (Sadece ingilizce için geçerli).

	$singular = str_singular('cars');

### studly_case

Girilen yazıyı `StudlyCase` olacak şekilde düzenler.

	$value = studly_case('foo_bar');

	// FooBar

### trans

Girilen dil satırını çevirir. `Lang::get` fonksiyonunun kısayolu.

	$value = trans('validation.required'):

### trans_choice


Tranlate a given language line with inflection. Alias of `Lang::choice`.

	$value = trans_choice('foo.bar', $count);

<a name="urls"></a>
## URL İşlemleri

### action

Girilen denetçinin URL'ini oluşturur.

	$url = action('HomeController@getIndex', $params);

### asset

Girilen elemanın URL'ini oluşturur.

	$url = asset('img/photo.jpg');

### link_to

Girilen URL'e gerekli HTML linkini oluşturur.

	echo link_to('foo/bar', $title, $attributes = array(), $secure = null);

### link_to_asset

Girilen eleman için gerekli HTML linkini oluşturur.

	echo link_to_asset('foo/bar.zip', $title, $attributes = array(), $secure = null);

### link_to_route

Girilen rota için gerekli HTML linkini oluşturur.

	echo link_to_route('route.name', $title, $parameters = array(), $attributes = array());

### link_to_action

Girilen denetçi fonksiyonu için gerekli HTML linkini oluşturur.

	echo link_to_action('HomeController@getIndex', $title, $parameters = array(), $attributes = array());

### secure_asset

Girilen eleman için gerekli HTML linkini HTTPS kullanarak oluşturur.

	echo secure_asset('foo/bar.zip', $title, $attributes = array());

### secure_url

Girilen URL'e gerekli HTML linkini HTTPS kullanarak oluşturur.

	echo secure_url('foo/bar', $parameters = array());

### url

Girilen URL'e gerekli HTML linkini oluşturur.

	echo url('foo/bar', $parameters = array(), $secure = null);

<a name="miscellaneous"></a>
## Miscellaneous

### csrf_token

CSRF token'inin güncel değerini döndürür.

	$token = csrf_token();

### dd

Girilen veriyi ekrana basar ve uygulamayı durdurur.

	dd($value);

### value

Eğer girilen değer anonim bir fonksiyonsa, değer olarak anonim fonksiyonun döndürdüğü değer döndürür. Eğer değilse direk değeri döndürür.

	$value = value(function() { return 'bar'; });

### with

Girilen objeyi döndürür. PHP 5.3.x kullanımında metod zincirleme işlemi için çok yararlı.

	$value = with(new Foo)->doWork();
