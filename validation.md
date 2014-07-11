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

Laravel 透過`Validation`類別讓你可以簡單，方便的驗證資料正確性及查看驗證的錯誤訊息

#### 基本驗證範例

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => 'required|min:5')
	);


我們透過`make`這個方法來的第一個參數設定該被驗證資料名稱，然後第二個參數我們定義該資料可被接受的規則

#### 使用陣列來定義規則

我們可以同時定義多個規則並且使用,(逗號)分隔或是多宣告一個陣列

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


當一個 `Validator` 實例被建立，`fails`或`passes`這二個方法就可以在驗證時使用，如下

	if ($validator->fails())
	{
		// The given data did not pass validation
	}


假如驗證失敗，你可能需要從驗證變數$validator查看錯誤驗證可使用下列方式

	$messages = $validator->messages();


你也有可能需要透過一個陣列來了解是哪些驗證規則無法通過驗證，這個時後你可以使用`failed`這個方法：
	$failed = $validator->failed();

#### 驗證欄位

`Validator`類別提供了許多規則讓你驗證檔案，例如`size`, `mimes`,以及其他參數. 當驗證檔案時你可以簡單的透過這些參數加入你的驗證器來驗證你其他的資料.

<a name="working-with-error-messages"></a>
## 使用錯誤訊息


當你呼叫一個`Validator`實例的`messages`方法後，你會得到一個`MessageBag`的變數，裡面有許多方便的方法讓你取得錯誤訊息

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

#### 隔分一個欄位是否有錯誤訊息

	if ($messages->has('email'))
	{
		//
	}

#### 定義錯誤訊息格式

	echo $messages->first('email', '<p>:message</p>');

> **注意:** 預設錯誤訊息使用Bootstrap語法.

#### 查看所有錯誤訊息並使用特定格式

	foreach ($messages->all('<li>:message</li>') as $message)
	{
		//
	}

<a name="error-messages-and-views"></a>
## 錯誤訊息 & 視圖

當你開始執行驗證，你將會需要一個簡單的方法去取的錯誤訊息並回傳到你的視圖，在Laravel你可以很方便的處理這些事，你可以透過下面的路由例子來了解：


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

記住當驗證失敗時，我們透過`Validator`的實例中`withErrors`的方法去重新導向頁面，這個方法將會存取錯誤訊息在session中，所以他們將會在下個頁面可以被使用.

僅管如此,  注意我們不需要特別去使用GET route在視圖中綁定錯誤訊息. 因為Laravel 將會一直確認seesion中的錯誤訊息並自動綁定他們在視圖當中當那些錯誤訊息是有效的時後. 

**所以這相當重要去了解，一個`$errors`變數將會永遠有效的存在你的所有的視圖中，在每個允許的頁面請求你都很直接的假設並且安全的使用`$errors`變數.這個變數將會是一個`MessageBag`的實例.

所以，當我們重新做頁面導向，你可以自然的在視圖中使用`$errors`變數

	<?php echo $errors->first('email'); ?>

### 命名錯誤清單

假如你在一個頁面中有許多的表單, 你可能希望為錯誤命名一個`MessageBag`. 這將允許你針對特定表單查看錯誤訊息, 我們只要簡單的在`withErrors`的第二個參數設定將可達到這個功能：

	return Redirect::to('register')->withErrors($validator, 'login');

你也可以接著從一個`$errors`變數中命名一個`MessageBag`實例

	<?php echo $errors->login->first('email'); ?>

<a name="available-validation-rules"></a>
## 有效的驗證規則

以下是一個有效的驗證規則清單與他們的函式

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
#### 同意accepted

這個欄位必需是_yes_, _on_, 或 _1_時驗證才會成立. 這將會在"使用者條款"的驗證中很有用

<a name="rule-active-url"></a>
#### 有效的網址active_url

The field under validation must be a valid URL according to the `checkdnsrr` PHP function.
這個欄位必需是一個有效的網址並通過`checkdnsrr`這個php函式的驗證

<a name="rule-after"></a>
#### after:_date_

The field under validation must be a value after a given date. The dates will be passed into the PHP `strtotime` function.
這個欄位必需是在給允的日期後，而這個日期將會帶入`strtotime`函式進行驗證

<a name="rule-alpha"></a>
#### alpha

The field under validation must be entirely alphabetic characters.
這個欄位只能允許是字母

<a name="rule-alpha-dash"></a>
#### alpha_dash

The field under validation may have alpha-numeric characters, as well as dashes and underscores.
這個欄位只能允許字母、數字以及-及_

<a name="rule-alpha-num"></a>
#### alpha_num

The field under validation must be entirely alpha-numeric characters.
這個欄位只允許字母及數字

<a name="rule-array"></a>
#### array

The field under validation must be of type array.
這個欄位只允許陣列

<a name="rule-before"></a>
#### before:_date_

The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function.
這個欄位必需是在給允的日期早，而這個日期將會帶入`strtotime`函式進行驗證

<a name="rule-between"></a>
#### between:_min_,_max_

The field under validation must have a size between the given _min_ and _max_. Strings, numerics, and files are evaluated in the same fashion as the `size` rule.
這個欄位的大小必需介於 _min_ 及 _max_. 

<a name="rule-confirmed"></a>
#### confirmed

The field under validation must have a matching field of `foo_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input.

<a name="rule-date"></a>
#### date

The field under validation must be a valid date according to the `strtotime` PHP function.

<a name="rule-date-format"></a>
#### date_format:_format_

The field under validation must match the _format_ defined according to the `date_parse_from_format` PHP function.

<a name="rule-different"></a>
#### different:_field_

The given _field_ must be different than the field under validation.

<a name="rule-digits"></a>
#### digits:_value_

The field under validation must be _numeric_ and must have an exact length of _value_.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

The field under validation must have a length between the given _min_ and _max_.

<a name="rule-boolean"></a>
#### boolean

The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"` and `"0"`.

<a name="rule-email"></a>
#### email

The field under validation must be formatted as an e-mail address.

<a name="rule-exists"></a>
#### exists:_table_,_column_

The field under validation must exist on a given database table.

#### Basic Usage Of Exists Rule

	'state' => 'exists:states'

#### Specifying A Custom Column Name

	'state' => 'exists:states,abbreviation'

You may also specify more conditions that will be added as "where" clauses to the query:

	'email' => 'exists:staff,email,account_id,1'

Passing `NULL` as a "where" clause value will add a check for a `NULL` database value:

	'email' => 'exists:staff,email,deleted_at,NULL'

<a name="rule-image"></a>
#### image

The file under validation must be an image (jpeg, png, bmp, or gif)

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

The field under validation must be included in the given list of values.

<a name="rule-integer"></a>
#### integer

The field under validation must have an integer value.

<a name="rule-ip"></a>
#### ip

The field under validation must be formatted as an IP address.

<a name="rule-max"></a>
#### max:_value_

The field under validation must be less than or equal to a maximum _value_. Strings, numerics, and files are evaluated in the same fashion as the `size` rule.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

The file under validation must have a MIME type corresponding to one of the listed extensions.

#### Basic Usage Of MIME Rule

	'photo' => 'mimes:jpeg,bmp,png'

<a name="rule-min"></a>
#### min:_value_

The field under validation must have a minimum _value_. Strings, numerics, and files are evaluated in the same fashion as the `size` rule.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

The field under validation must not be included in the given list of values.

<a name="rule-numeric"></a>
#### numeric

The field under validation must have a numeric value.

<a name="rule-regex"></a>
#### regex:_pattern_

The field under validation must match the given regular expression.

**Note:** When using the `regex` pattern, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

<a name="rule-required"></a>
#### required

The field under validation must be present in the input data.

<a name="rule-required-if"></a>
#### required\_if:_field_,_value_

The field under validation must be present if the _field_ field is equal to _value_.

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
