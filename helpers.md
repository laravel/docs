# 輔助方法

- [陣列](#arrays)
- [路徑](#paths)
- [字串](#strings)
- [網址](#urls)
- [其他](#miscellaneous)

<a name="arrays"></a>
## 陣列

### array_add

如果給定的鍵不在陣列中，`array_add` 函式會把給定的鍵值對加到陣列中。

	$array = array('foo' => 'bar');

	$array = array_add($array, 'key', 'value');

### array_divide

`array_divide` 函式回傳兩個陣列，一個包含原本陣列的鍵，另一個包含原本陣列的值。

	$array = array('foo' => 'bar');

	list($keys, $values) = array_divide($array);

### array_dot

`array_dot` 函式把多維陣列扁平化成一維陣列，並用「點」符號表示深度。

	$array = array('foo' => array('bar' => 'baz'));

	$array = array_dot($array);

	// array('foo.bar' => 'baz');

### array_except

`array_except` 函式從陣列移除給定的鍵值對。

	$array = array_except($array, array('keys', 'to', 'remove'));

### array_fetch

`array_fetch` 函式回傳包含被選擇的巢狀元素的扁平化陣列。

	$array = array(
		array('developer' => array('name' => 'Taylor')),
		array('developer' => array('name' => 'Dayle')),
	);

	$array = array_fetch($array, 'developer.name');

	// array('Taylor', 'Dayle');

### array_first

`array_first` 函式回傳陣列中第一個通過給定的測試為真的元素。

	$array = array(100, 200, 300);

	$value = array_first($array, function($key, $value)
	{
		return $value >= 150;
	});

也可以傳遞預設值當作第三個參數：

	$value = array_first($array, $callback, $default);

### array_last

`array_last` 函式回傳陣列中最後一個通過給定的測試為真的元素。

	$array = array(350, 400, 500, 300, 200, 100);

	$value = array_last($array, function($key, $value)
	{
		return $value > 350;
	});

	// 500

也可以傳遞預設值當作第三個參數：

	$value = array_last($array, $callback, $default);

### array_flatten

`array_flatten` 函式將會把多維陣列扁平化成一維。

	$array = array('name' => 'Joe', 'languages' => array('PHP', 'Ruby'));

	$array = array_flatten($array);

	// array('Joe', 'PHP', 'Ruby');

### array_forget

`array_forget` 函式將會用「點」符號從深度巢狀陣列移除給定的鍵值對。

	$array = array('names' => array('joe' => array('programmer')));

	array_forget($array, 'names.joe');

### array_get

`array_get` 函式將會使用「點」符號從深度巢狀陣列取回給定的值。

	$array = array('names' => array('joe' => array('programmer')));

	$value = array_get($array, 'names.joe');

	$value = array_get($array, 'names.john', 'default');

> **注意:** 想要把 `array_get` 用在物件上？ 請使用 `object_get`。

### array_only

`array_only` 函式將會只從陣列回傳給定的鍵值對。

	$array = array('name' => 'Joe', 'age' => 27, 'votes' => 1);

	$array = array_only($array, array('name', 'votes'));

### array_pluck

`array_pluck` 函式將會從陣列拉出給定鍵值對的清單。

	$array = array(array('name' => 'Taylor'), array('name' => 'Dayle'));

	$array = array_pluck($array, 'name');

	// array('Taylor', 'Dayle');

### array_pull

`array_pull` 函式將會從陣列回傳給定的鍵值對，並移除它。

	$array = array('name' => 'Taylor', 'age' => 27);

	$name = array_pull($array, 'name');

### array_set

`array_set` 函式將會使用「點」符號在深度巢狀陣列中指定值。

	$array = array('names' => array('programmer' => 'Joe'));

	array_set($array, 'names.editor', 'Taylor');

### array_sort

`array_sort` 函式借由給定閉包的結果來排序陣列。

	$array = array(
		array('name' => 'Jill'),
		array('name' => 'Barry'),
	);

	$array = array_values(array_sort($array, function($value)
	{
		return $value['name'];
	}));

### array_where

使用給定的閉包過濾陣列。

	$array = array(100, '200', 300, '400', 500);

	$array = array_where($array, function($key, $value)
	{
		return is_string($value);
	});

	// Array ( [1] => 200 [3] => 400 )

### head

回傳陣列中第一個元素。對 PHP 5.3.x 的方法鏈很有用。

	$first = head($this->returnsArray('foo'));

### last

回傳陣列中最後一個元素。對方法鏈很有用。

	$last = last($this->returnsArray('foo'));

<a name="paths"></a>
## 路徑

### app_path

取得 `app` 資料夾的完整路徑。

	$path = app_path();

### base_path

取得應用程式安裝根目錄的完整路徑。

### public_path

取得 `public` 資料夾的完整路徑。

### storage_path

取得 `app/storage` 資料夾的完整路徑。

<a name="strings"></a>
## 字串

### camel_case

把給定的字串轉換成 `駝峰式命名`。

	$camel = camel_case('foo_bar');

	// fooBar

### class_basename

取得給定類別的類別名稱，不含任何命名空間的名稱。

	$class = class_basename('Foo\Bar\Baz');

	// Baz

### e

對給定字串執行 `htmlentities`，並支援 UTF-8。

	$entities = e('<html>foo</html>');

### ends_with

判斷句子結尾是否有給定的字串。

	$value = ends_with('This is my name', 'name');

### snake_case

把給定的字串轉換成 `蛇形命名`。

	$snake = snake_case('fooBar');

	// foo_bar

### str_limit

限制字串的字元數量。

	str_limit($value, $limit = 100, $end = '...')

例子：

	$value = str_limit('The PHP framework for web artisans.', 7);

	// The PHP...

### starts_with

判斷句子是否開頭有給定的字串。

	$value = starts_with('This is my name', 'This');

### str_contains

判斷句子是否有給定的字串。

	$value = str_contains('This is my name', 'my');

### str_finish

加一個給定字串到句子結尾。多餘一個的給定字串則移除。

	$string = str_finish('this/string', '/');

	// this/string/

### str_is

判斷字串是否符合給定的模式。星號可以用來當作萬用字元。

	$value = str_is('foo*', 'foobar');

### str_plural

把字串轉換成它的多數形態 (只有英文)。

	$plural = str_plural('car');

### str_random

產生給定長度的隨機字串。

	$string = str_random(40);

### str_singular

把字串轉換成它的單數形態 (只有英文)。

	$singular = str_singular('cars');

### str_slug

從給定字串產生一個對網址友善的「slug」。

	str_slug($title, $separator);

例子：

	$title = str_slug("Laravel 5 Framework", "-");

	// laravel-5-framework

### studly_case

把給定字串轉換成 `首字大寫命名`。

	$value = studly_case('foo_bar');

	// FooBar

### trans

翻譯給定的語句。等同 `Lang::get`。

	$value = trans('validation.required'):

### trans_choice

隨著詞形變化翻譯給定的語句。等同 `Lang::choice`。

	$value = trans_choice('foo.bar', $count);

<a name="urls"></a>
## 網址

### action

產生給定控制器行為的網址。

	$url = action('HomeController@getIndex', $params);

### route

產生給定路由名稱的網址。

	$url = route('routeName', $params);

### asset

產生資源的網址。

	$url = asset('img/photo.jpg');

### link_to

產生給定網址的 HTML 連結。

	echo link_to('foo/bar', $title, $attributes = array(), $secure = null);

### link_to_asset

產生給定資源的 HTML 連結。

	echo link_to_asset('foo/bar.zip', $title, $attributes = array(), $secure = null);

### link_to_route

產生給定路由的 HTML 連結。

	echo link_to_route('route.name', $title, $parameters = array(), $attributes = array());

### link_to_action

產生給定控制器行為的 HTML 連結。

	echo link_to_action('HomeController@getIndex', $title, $parameters = array(), $attributes = array());

### secure_asset

產生給定資源的 HTTPS HTML 連結。

	echo secure_asset('foo/bar.zip', $title, $attributes = array());

### secure_url

產生給定路徑的 HTTPS 完整網址。

	echo secure_url('foo/bar', $parameters = array());

### url

產生給定路徑的完整網址。

	echo url('foo/bar', $parameters = array(), $secure = null);

<a name="miscellaneous"></a>
## 其他

### csrf_token

取得現在 CSRF token 的值。

	$token = csrf_token();

### dd

印出給定變數並結束腳本執行。

	dd($value);

### value

如果給定的值是個 `閉包`，回傳 `閉包` 的回傳值。不是的話，則回傳值。

	$value = value(function() { return 'bar'; });

### with

回傳給定物件。對 PHP 5.3.x 的建構式方法鏈很有用。

	$value = with(new Foo)->doWork();
