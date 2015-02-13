# 辅助方法

- [数组](#arrays)
- [路径](#paths)
- [字串](#strings)
- [网址](#urls)
- [其他](#miscellaneous)

<a name="arrays"></a>
## 数组

### array_add

如果给定的键不在数组中，`array_add` 函式会把给定的键值对加到数组中。

	$array = array('foo' => 'bar');

	$array = array_add($array, 'key', 'value');

### array_divide

`array_divide` 函式返回两个数组，一个包含原本数组的键，另一个包含原本数组的值。

	$array = array('foo' => 'bar');

	list($keys, $values) = array_divide($array);

### array_dot

`array_dot` 函式把多维数组扁平化成一维数组，并用「点」符号表示深度。

	$array = array('foo' => array('bar' => 'baz'));

	$array = array_dot($array);

	// array('foo.bar' => 'baz');

### array_except

`array_except` 函式从数组移除给定的键值对。

	$array = array_except($array, array('keys', 'to', 'remove'));

### array_fetch

`array_fetch` 函式返回包含被选择的嵌套元素的扁平化数组。

	$array = array(
		array('developer' => array('name' => 'Taylor')),
		array('developer' => array('name' => 'Dayle')),
	);

	$array = array_fetch($array, 'developer.name');

	// array('Taylor', 'Dayle');

### array_first

`array_first` 函式返回数组中第一个通过给定的测试为真的元素。

	$array = array(100, 200, 300);

	$value = array_first($array, function($key, $value)
	{
		return $value >= 150;
	});

也可以传递默认值当作第三个参数：

	$value = array_first($array, $callback, $default);

### array_last

`array_last` 函式返回数组中最后一个通过给定的测试为真的元素。

	$array = array(350, 400, 500, 300, 200, 100);

	$value = array_last($array, function($key, $value)
	{
		return $value > 350;
	});

	// 500

也可以传递默认值当作第三个参数：

	$value = array_last($array, $callback, $default);

### array_flatten

`array_flatten` 函式将会把多维数组扁平化成一维。

	$array = array('name' => 'Joe', 'languages' => array('PHP', 'Ruby'));

	$array = array_flatten($array);

	// array('Joe', 'PHP', 'Ruby');

### array_forget

`array_forget` 函式将会用「点」符号从深度嵌套数组移除给定的键值对。

	$array = array('names' => array('joe' => array('programmer')));

	array_forget($array, 'names.joe');

### array_get

`array_get` 函式将会使用「点」符号从深度嵌套数组取回给定的值。

	$array = array('names' => array('joe' => array('programmer')));

	$value = array_get($array, 'names.joe');

	$value = array_get($array, 'names.john', 'default');

> **注意:** 想要把 `array_get` 用在对象上？ 请使用 `object_get`。

### array_only

`array_only` 函式将会只从数组返回给定的键值对。

	$array = array('name' => 'Joe', 'age' => 27, 'votes' => 1);

	$array = array_only($array, array('name', 'votes'));

### array_pluck

`array_pluck` 函式将会从数组拉出给定键值对的清单。

	$array = array(array('name' => 'Taylor'), array('name' => 'Dayle'));

	$array = array_pluck($array, 'name');

	// array('Taylor', 'Dayle');

### array_pull

`array_pull` 函式将会从数组返回给定的键值对，并移除它。

	$array = array('name' => 'Taylor', 'age' => 27);

	$name = array_pull($array, 'name');

### array_set

`array_set` 函式将会使用「点」符号在深度嵌套数组中指定值。

	$array = array('names' => array('programmer' => 'Joe'));

	array_set($array, 'names.editor', 'Taylor');

### array_sort

`array_sort` 函式借由给定闭包的结果来排序数组。

	$array = array(
		array('name' => 'Jill'),
		array('name' => 'Barry'),
	);

	$array = array_values(array_sort($array, function($value)
	{
		return $value['name'];
	}));

### array_where

使用给定的闭包过滤数组。

	$array = array(100, '200', 300, '400', 500);

	$array = array_where($array, function($key, $value)
	{
		return is_string($value);
	});

	// Array ( [1] => 200 [3] => 400 )

### head

返回数组中第一个元素。对 PHP 5.3.x 的方法链很有用。

	$first = head($this->returnsArray('foo'));

### last

返回数组中最后一个元素。对方法链很有用。

	$last = last($this->returnsArray('foo'));

<a name="paths"></a>
## 路径

### app_path

取得 `app` 文件夹的完整路径。

	$path = app_path();

### base_path

取得应用程序安装根目录的完整路径。

### public_path

取得 `public` 文件夹的完整路径。

### storage_path

取得 `app/storage` 文件夹的完整路径。

<a name="strings"></a>
## 字串

### camel_case

把给定的字串转换成 `驼峰式命名`。

	$camel = camel_case('foo_bar');

	// fooBar

### class_basename

取得给定类别的类别名称，不含任何命名空间的名称。

	$class = class_basename('Foo\Bar\Baz');

	// Baz

### e

对给定字串执行 `htmlentities`，并支持 UTF-8。

	$entities = e('<html>foo</html>');

### ends_with

判断句子结尾是否有给定的字串。

	$value = ends_with('This is my name', 'name');

### snake_case

把给定的字串转换成 `蛇形命名`。

	$snake = snake_case('fooBar');

	// foo_bar

### str_limit

限制字串的字符数量。

	str_limit($value, $limit = 100, $end = '...')

例子：

	$value = str_limit('The PHP framework for web artisans.', 7);

	// The PHP...

### starts_with

判断句子是否开头有给定的字串。

	$value = starts_with('This is my name', 'This');

### str_contains

判断句子是否有给定的字串。

	$value = str_contains('This is my name', 'my');

### str_finish

加一个给定字串到句子结尾。多余一个的给定字串则移除。

	$string = str_finish('this/string', '/');

	// this/string/

### str_is

判断字串是否符合给定的模式。星号可以用来当作万用字符。

	$value = str_is('foo*', 'foobar');

### str_plural

把字串转换成它的多数形态 (只有英文)。

	$plural = str_plural('car');

### str_random

产生给定长度的随机字串。

	$string = str_random(40);

### str_singular

把字串转换成它的单数形态 (只有英文)。

	$singular = str_singular('cars');

### str_slug

从给定字串产生一个对网址友善的「slug」。

	str_slug($title, $separator);

例子：

	$title = str_slug("Laravel 5 Framework", "-");

	// laravel-5-framework

### studly_case

把给定字串转换成 `首字大写命名`。

	$value = studly_case('foo_bar');

	// FooBar

### trans

翻译给定的语句。等同 `Lang::get`。

	$value = trans('validation.required'):

### trans_choice

随着词形变化翻译给定的语句。等同 `Lang::choice`。

	$value = trans_choice('foo.bar', $count);

<a name="urls"></a>
## 网址

### action

产生给定控制器行为的网址。

	$url = action('HomeController@getIndex', $params);

### route

产生给定路由名称的网址。

	$url = route('routeName', $params);

### asset

产生资源的网址。

	$url = asset('img/photo.jpg');

### link_to

产生给定网址的 HTML 链接。

	echo link_to('foo/bar', $title, $attributes = array(), $secure = null);

### link_to_asset

产生给定资源的 HTML 链接。

	echo link_to_asset('foo/bar.zip', $title, $attributes = array(), $secure = null);

### link_to_route

产生给定路由的 HTML 链接。

	echo link_to_route('route.name', $title, $parameters = array(), $attributes = array());

### link_to_action

产生给定控制器行为的 HTML 链接。

	echo link_to_action('HomeController@getIndex', $title, $parameters = array(), $attributes = array());

### secure_asset

产生给定资源的 HTTPS HTML 链接。

	echo secure_asset('foo/bar.zip', $title, $attributes = array());

### secure_url

产生给定路径的 HTTPS 完整网址。

	echo secure_url('foo/bar', $parameters = array());

### url

产生给定路径的完整网址。

	echo url('foo/bar', $parameters = array(), $secure = null);

<a name="miscellaneous"></a>
## 其他

### csrf_token
返回
取得现在 CSRF token 的值。

	$token = csrf_token();

### dd

印出给定变量并结束脚本执行。

	dd($value);

### value

如果给定的值是个 `闭包`，返回 `闭包` 的返回值。不是的话，则返回值。

	$value = value(function() { return 'bar'; });

### with

返回给定对象。对 PHP 5.3.x 的建构式方法链很有用。

	$value = with(new Foo)->doWork();
