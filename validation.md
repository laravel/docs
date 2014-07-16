# 驗證

- [基本用法](#basic-usage)
- [使用錯誤訊息](#working-with-error-messages)
- [錯誤訊息 & 視圖](#error-messages-and-views)
- [使用驗證規則](#available-validation-rules)
- [有條件新增規則](#conditionally-adding-rules)
- [自訂錯誤訊息](#custom-error-messages)
- [自訂驗證規則](#custom-validation-rules)

<a name="basic-usage"></a>
## 基本用法

Laravel 透過 `Validation` 類別讓你可以簡單、方便的驗證資料正確性及查看驗證的錯誤訊息。

#### 基本驗證範例

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => 'required|min:5')
	);


我們透過 `make` 這個方法來的第一個參數設定該被驗證資料名稱，然後第二個參數我們定義該資料可被接受的規則。

#### 使用陣列來定義規則

多個規則可以使用"|"符號分隔，或是單一陣列作為單獨的元素分隔。

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => array('required', 'min:5'))
	);

#### 驗證多個欄位

    $validator = Validator::make(
        array(
            'name' => 'Dayle',
            'password' => 'lamepassword',
            'email' => 'email@example.com'
        ),
        array(
            'name' => 'required',
            'password' => 'required|min:8',
            'email' => 'required|email|unique:users'
        )
    );


當一個 `Validator` 實例被建立，`fails`（或 `passes`） 這二個方法就可以在驗證時使用，如下：

	if ($validator->fails())
	{
		// The given data did not pass validation
	}


假如驗證失敗，您可以從驗證器中接收錯誤資訊。

	$messages = $validator->messages();


您可能不需要錯誤訊息，只想取得無法通過驗證的規則，您可以使用 'failed' 方法：

	$failed = $validator->failed();

#### 驗證檔案

`Validator` 類別提供了一些規則用來驗證檔案，例如 `size`, `mimes` 等等。當需要驗證檔案時，你僅需將它們和你其他的資料一同送給驗證器即可。

<a name="working-with-error-messages"></a>
## 使用錯誤訊息

當你呼叫一個 `Validator` 實例的 `messages` 方法後，你會得到一個 `MessageBag` 的變數，裡面有許多方便的方法讓你取得錯誤訊息。

#### 查看一個欄位的第一個錯誤訊息

	echo $messages->first('email');

#### 查看一個欄位的所有錯誤訊息

	foreach ($messages->get('email') as $message)
	{
		//
	}

#### 查看所有欄位的所有錯誤訊息

	foreach ($messages->all() as $message)
	{
		//
	}

#### 判斷一個欄位是否有錯誤訊息

	if ($messages->has('email'))
	{
		//
	}

#### 錯誤訊息格式化輸出

	echo $messages->first('email', '<p>:message</p>');

> **注意:** 預設錯誤訊息以 Bootstrap 相容語法輸出。

#### 查看所有錯誤訊息並以格式化輸出

	foreach ($messages->all('<li>:message</li>') as $message)
	{
		//
	}

<a name="error-messages-and-views"></a>
## 錯誤訊息 & 視圖

當你開始進行驗證，你將會需要一個簡易的方法去取得錯誤訊息並回傳到你的視圖中，在 Laravel 你可以很方便的處理這些事，你可以透過下面的路由例子來了解：


	Route::get('register', function()
	{
		return View::make('user.register');
	});

	Route::post('register', function()
	{
		$rules = array(...);

		$validator = Validator::make(Input::all(), $rules);

		if ($validator->fails())
		{
			return Redirect::to('register')->withErrors($validator);
		}
	});

記得當驗證失敗後，我們會使用 `withErrors` 方法來將 `Validator` 實例進行重新導向。這方法會將錯誤訊息存入 session 中，這樣才能在下個請求中被使用。

然而，我們並不需要特別去將錯誤訊息綁定在我們 GET 路由的視圖中。因為 Laravel 會確認在 Session 資料中是否有錯誤訊息，並且自動將它們綁定至視圖中。**所以請注意，`$errors` 變數存在於所有的視圖中，所有的請求裡，**讓你可以直接假設 `$errors` 變數已被定義且可以安全地使用。`$errors` 變數是 `MessageBag` 類別的一個實例。

所以，重新導向之後，你可以自然的在視圖中使用 `$errors` 變數：

	<?php echo $errors->first('email'); ?>

### 命名錯誤清單

假如你在一個頁面中有許多的表單, 你可能希望為錯誤命名一個`MessageBag`. 這將讓你針對特定的表單查看其錯誤訊息, 我們只要簡單的在 `withErrors` 的第二個參數設定名稱即可：

	return Redirect::to('register')->withErrors($validator, 'login');

接著你可以從一個 `$errors` 變數中取得已命名的 `MessageBag` 實例：

	<?php echo $errors->login->first('email'); ?>

<a name="available-validation-rules"></a>
## 既存的驗證規則

以下是既存的驗證規則清單與他們的函式名稱：

- [Accepted](#rule-accepted)
- [Active URL](#rule-active-url)
- [After (Date)](#rule-after)
- [Alpha](#rule-alpha)
- [Alpha Dash](#rule-alpha-dash)
- [Alpha Numeric](#rule-alpha-num)
- [Array](#rule-array)
- [Before (Date)](#rule-before)
- [Between](#rule-between)
- [Boolean](#rule-boolean)
- [Confirmed](#rule-confirmed)
- [Date](#rule-date)
- [Date Format](#rule-date-format)
- [Different](#rule-different)
- [Digits](#rule-digits)
- [Digits Between](#rule-digits-between)
- [E-Mail](#rule-email)
- [Exists (Database)](#rule-exists)
- [Image (File)](#rule-image)
- [In](#rule-in)
- [Integer](#rule-integer)
- [IP Address](#rule-ip)
- [Max](#rule-max)
- [MIME Types](#rule-mimes)
- [Min](#rule-min)
- [Not In](#rule-not-in)
- [Numeric](#rule-numeric)
- [Regular Expression](#rule-regex)
- [Required](#rule-required)
- [Required If](#rule-required-if)
- [Required With](#rule-required-with)
- [Required With All](#rule-required-with-all)
- [Required Without](#rule-required-without)
- [Required Without All](#rule-required-without-all)
- [Same](#rule-same)
- [Size](#rule-size)
- [Timezone](#rule-timezone)
- [Unique (Database)](#rule-unique)
- [URL](#rule-url)

<a name="rule-accepted"></a>
#### accepted

欄位值為 _yes_, _on_, 或是 _1_ 時，驗證才會通過。這在確認"服務條款"是否同意時很有用。

<a name="rule-active-url"></a>
#### active_url

欄位值透過 PHP 函式 `checkdnsrr` 來驗證是否為一個有效的網址。

<a name="rule-after"></a>
#### after:_date_

驗證欄位是否是在指定日期之後。這個日期將會使用 PHP `strtotime` 函式驗證。

<a name="rule-alpha"></a>
#### alpha

欄位僅全數為字母字元時通過驗證。

<a name="rule-alpha-dash"></a>
#### alpha_dash

欄位值僅允許字母、數字、破折號（-）以及底線（_）

<a name="rule-alpha-num"></a>
#### alpha_num

欄位值僅允許字母、數字

<a name="rule-array"></a>
#### array

欄位值僅允許為陣列

<a name="rule-before"></a>
#### before:_date_

驗證欄位是否是在指定日期之前。這個日期將會使用 PHP `strtotime` 函式驗證。

<a name="rule-between"></a>
#### between:_min_,_max_

欄位值需介於指定的 _min_ 和 _max_ 值之間。字串、數值或是檔案都是用同樣的方式來進行驗證。


<a name="rule-confirmed"></a>
#### confirmed

欄位值需與對應的欄位值 `foo_confirmation` 相同。例如，如果驗證的欄位是 `password` ，那對應的欄位 `password_confirmation` 就必須存在且與 `password` 欄位相符。

<a name="rule-date"></a>
#### date

欄位值透過 PHP `strtotime` 函式驗證是否為一個合法的日期。

<a name="rule-date-format"></a>
#### date_format:_format_

欄位值透過 PHP `date_parse_from_format` 函式驗證符合 _format_ 制定格式的日期是否為合法日期。

<a name="rule-different"></a>
#### different:_field_

欄位值需與指定的欄位 _field_ 值不同。


<a name="rule-digits"></a>
#### digits:_value_

欄位值需為數字且長度需為 _value_。

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

欄位值需為數字，且長度需介於 _min_ 與 _max_ 之間。

<a name="rule-boolean"></a>
#### boolean

欄位必須可以轉換成布林值，可接受的值為 `true`, `false`, `1`, `0`, `"1"`, `"0"`。

<a name="rule-email"></a>
#### email

欄位值需符合 email 格式。

<a name="rule-exists"></a>
#### exists:_table_,_column_

欄位值需與存在於資料庫 _table_ 中的 _column_ 欄位值其一相同。

#### Exists 規則的基本使用方法

	'state' => 'exists:states'

#### 指定一個自訂的欄位名稱

	'state' => 'exists:states,abbreviation'

你可以指定更多條件且那些條件將會被新增至 "where" 查詢裡：

	'email' => 'exists:staff,email,account_id,1'
	/* 這個驗證規則為 email 需存在於 staff 這個資料表中 email 欄位中且 account_id=1 */

透過`NULL`搭配"where"的縮寫寫法去檢查資料庫的是否為`NULL`

	'email' => 'exists:staff,email,deleted_at,NULL'

<a name="rule-image"></a>
#### image

檔案必需為圖片(jpeg, png, bmp 或 gif)

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

The field under validation must be included in the given list of values.
這個欄位必需符合事先給予的清單的其中一個值

<a name="rule-integer"></a>
#### integer

The field under validation must have an integer value.
這個欄位必需是一個整數值

<a name="rule-ip"></a>
#### ip

The field under validation must be formatted as an IP address.
這個欄位必需符合IP位置的格式([1~255].[1~255].[1~255].[1~255])

<a name="rule-max"></a>
#### max:_value_

The field under validation must be less than or equal to a maximum _value_. Strings, numerics, and files are evaluated in the same fashion as the `size` rule.
這個欄位必需小於_value_，而字串，數字和檔案則是判斷`size`大小

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

The file under validation must have a MIME type corresponding to one of the listed extensions.
這個檔案必需要有一個 MIME且必需對應清單中其中一個值

#### MIME規則基本用法

	'photo' => 'mimes:jpeg,bmp,png'

<a name="rule-min"></a>
#### min:_value_

The field under validation must have a minimum _value_. Strings, numerics, and files are evaluated in the same fashion as the `size` rule.
這個欄位必需大於_value_，而字串，數字和檔案則是判斷`size`大小

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

The field under validation must not be included in the given list of values.
這個欄位的值必需不存在清單之中

<a name="rule-numeric"></a>
#### numeric

The field under validation must have a numeric value.
這個欄位必需是個數字(interger是指整數)

<a name="rule-regex"></a>
#### regex:_pattern_

The field under validation must match the given regular expression.
這個欄位必需符合你定義的正規表示法

**Note:** When using the `regex` pattern, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

**注意:** 當使用`regex`模式時，你必需在陣列中指定一個正規表示法規則

<a name="rule-required"></a>
#### required

The field under validation must be present in the input data.
這個欄位必需要有值

<a name="rule-required-if"></a>
#### required\_if:_field_,_value_

The field under validation must be present if the _field_ field is equal to _value_.
這個欄位必需符合_field_等於_value_的條件

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

The field under validation must be present _only if_ any of the other specified fields are present.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

The field under validation must be present _only if_ all of the other specified fields are present.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

The field under validation must be present _only when_ any of the other specified fields are not present.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

The field under validation must be present _only when_ the all of the other specified fields are not present.

<a name="rule-same"></a>
#### same:_field_

The given _field_ must match the field under validation.


<a name="rule-size"></a>
#### size:_value_

The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value. For files, _size_ corresponds to the file size in kilobytes.

<a name="rule-timezone"></a>
#### timezone

The field under validation must be a valid timezone identifier according to the `timezone_identifiers_list` PHP function.

<a name="rule-unique"></a>
#### unique:_table_,_column_,_except_,_idColumn_

The field under validation must be unique on a given database table. If the `column` option is not specified, the field name will be used.

#### Basic Usage Of Unique Rule

	'email' => 'unique:users'

#### Specifying A Custom Column Name

	'email' => 'unique:users,email_address'

#### Forcing A Unique Rule To Ignore A Given ID

	'email' => 'unique:users,email_address,10'

#### Adding Additional Where Clauses

You may also specify more conditions that will be added as "where" clauses to the query:

	'email' => 'unique:users,email_address,NULL,id,account_id,1'

In the rule above, only rows with an `account_id` of `1` would be included in the unique check.

<a name="rule-url"></a>
#### url

The field under validation must be formatted as an URL.

> **Note:** This function uses PHP's `filter_var` method.

<a name="conditionally-adding-rules"></a>
## Conditionally Adding Rules

In some situations, you may wish to run validation checks against a field **only** if that field is present in the input array. To quickly accomplish this, add the `sometimes` rule to your rule list:

	$v = Validator::make($data, array(
		'email' => 'sometimes|required|email',
	));

In the example above, the `email` field will only be validated if it is present in the `$data` array.

#### Complex Conditional Validation

Sometimes you may wish to require a given field only if another field has a greater value than 100. Or you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change:

	$v = Validator::make($data, array(
		'email' => 'required|email',
		'games' => 'required|numeric',
	));

Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game re-sell shop, or maybe they just enjoy collecting. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance.

	$v->sometimes('reason', 'required|max:500', function($input)
	{
		return $input->games >= 100;
	});

The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is the rules we want to add. If the `Closure` passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once:

	$v->sometimes(array('reason', 'cost'), 'required', function($input)
	{
		return $input->games >= 100;
	});

> **Note:** The `$input` parameter passed to your `Closure` will be an instance of `Illuminate\Support\Fluent` and may be used as an object to access your input and files.

<a name="custom-error-messages"></a>
## Custom Error Messages

If needed, you may use custom error messages for validation instead of the defaults. There are several ways to specify custom messages.

#### Passing Custom Messages Into Validator

	$messages = array(
		'required' => 'The :attribute field is required.',
	);

	$validator = Validator::make($input, $rules, $messages);

> *Note:* The `:attribute` place-holder will be replaced by the actual name of the field under validation. You may also utilize other place-holders in validation messages.

#### Other Validation Place-Holders

	$messages = array(
		'same'    => 'The :attribute and :other must match.',
		'size'    => 'The :attribute must be exactly :size.',
		'between' => 'The :attribute must be between :min - :max.',
		'in'      => 'The :attribute must be one of the following types: :values',
	);

#### Specifying A Custom Message For A Given Attribute

Sometimes you may wish to specify a custom error messages only for a specific field:

	$messages = array(
		'email.required' => 'We need to know your e-mail address!',
	);

<a name="localization"></a>
#### Specifying Custom Messages In Language Files

In some cases, you may wish to specify your custom messages in a language file instead of passing them directly to the `Validator`. To do so, add your messages to `custom` array in the `app/lang/xx/validation.php` language file.

	'custom' => array(
		'email' => array(
			'required' => 'We need to know your e-mail address!',
		),
	),

<a name="custom-validation-rules"></a>
## Custom Validation Rules

#### Registering A Custom Validation Rule

Laravel provides a variety of helpful validation rules; however, you may wish to specify some of your own. One method of registering custom validation rules is using the `Validator::extend` method:

	Validator::extend('foo', function($attribute, $value, $parameters)
	{
		return $value == 'foo';
	});

The custom validator Closure receives three arguments: the name of the `$attribute` being validated, the `$value` of the attribute, and an array of `$parameters` passed to the rule.

You may also pass a class and method to the `extend` method instead of a Closure:

	Validator::extend('foo', 'FooValidator@validate');

Note that you will also need to define an error message for your custom rules. You can do so either using an inline custom message array or by adding an entry in the validation language file.

#### Extending The Validator Class

Instead of using Closure callbacks to extend the Validator, you may also extend the Validator class itself. To do so, write a Validator class that extends `Illuminate\Validation\Validator`. You may add validation methods to the class by prefixing them with `validate`:

	<?php

	class CustomValidator extends Illuminate\Validation\Validator {

		public function validateFoo($attribute, $value, $parameters)
		{
			return $value == 'foo';
		}

	}

#### Registering A Custom Validator Resolver

Next, you need to register your custom Validator extension:

	Validator::resolver(function($translator, $data, $rules, $messages)
	{
		return new CustomValidator($translator, $data, $rules, $messages);
	});

When creating a custom validation rule, you may sometimes need to define custom place-holder replacements for error messages. You may do so by creating a custom Validator as described above, and adding a `replaceXXX` function to the validator.

	protected function replaceFoo($message, $attribute, $rule, $parameters)
	{
		return str_replace(':foo', $parameters[0], $message);
	}

If you would like to add a custom message "replacer" without extending the `Validator` class, you may use the `Validator::replacer` method:

	Validator::replacer('rule', function($message, $attribute, $rule, $parameters)
	{
		//
	});
