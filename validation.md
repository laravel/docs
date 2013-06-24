# Doğrulama

- [Basit Kullanım](#basit-kullanim)
- [Hata Mesajlarıyla Çalışmak](#hata-mesajlariyla-calismak)
- [Hata Mesajları ve Viewlar](#hata-mesajlari-ve-viewlar)
- [Mevcut Doğrulama Kuralları](#mevcut-dogrulama-kurallari)
- [Özel Hata Mesajları](#ozel-hata-mesajlari)
- [Özel Doğrulama Kuralları](#ozel-dogrulama-kurallari)

<a name="basit-kullanim"></a>
## Basit Kullanım

Laravel ships with a simple, convenient facility for validating data and retrieving validation error messages via the `Validation` class.

**Basit Doğrulama Örneği**

	$validator = Validator::make(
		array('isim' => 'Mehmet'),
		array('isim' => 'required|min:5')
	);

The first argument passed to the `make` method is the data under validation. The second argument is the validation rules that should be applied to the data.

Multiple rules may be delimited using either a "pipe" character, or as separate elements of an array.

**Kural Tanımlamak İçin Array Kullanmak**

	$validator = Validator::make(
		array('isim' => 'Mehmet'),
		array('isim' => array('required', 'min:5'))
	);

Once a `Validator` instance has been created, the `fails` (or `passes`) method may be used to perform the validation.

	if ($validator->fails())
	{
		// The given data did not pass validation
	}

If validation has failed, you may retrieve the error messages from the validator.

	$messages = $validator->messages();

You may also access an array of the failed validation rules, without messages. To do so, use the `failed` method:

	$failed = $validator->failed();

**Dosyaları Doğrulamak**

The `Validator` class provides several rules for validating files, such as `size`, `mimes`, and others. When validating files, you may simply pass them into the validator with your other data.

<a name="hata-mesajlariyla-calismak"></a>
## Hata Mesajlarıyla Çalışmak

After calling the `messages` method on a `Validator` instance, you will receive a `MessageBag` instance, which has a variety of convenient methods for working with error messages.

**Bir Alan İçin Oluşan İlk Hata Mesajını Almak**

	echo $mesaj->first('email');

**Bir Alan İçin Oluşan Tüm Hata Mesajlarını Almak**

	foreach ($mesajlar->get('email') as $mesaj)
	{
		//
	}

**Tüm Alanlar İçin Oluşan Tüm Hata Mesajlarını Almak**

	foreach ($mesajlar->all() as $mesaj)
	{
		//
	}

**Belirtilen Alan İçin Hata Mesajı Olup Olmadığını Anlamak**

	if ($mesajlar->has('email'))
	{
		//
	}

**Hata Mesajını Düzenleyerek Almak**

	echo $mesajlar->first('email', '<p>:mesaj</p>');

> **Not:** Varsayılan olarak, mesajlar Bootstrap'a (CSS Framework) uygun olarak şekillendirilmektedir.

**Tüm Hata Mesajlarını Düzenleyerek Almak**

	foreach ($mesajlar->all('<li>:mesaj</li>') as $mesaj)
	{
		//
	}

<a name="hata-mesajlari-ve-viewlar"></a>
## Hata Mesajları ve Viewlar

Once you have performed validation, you will need an easy way to get the error messages back to your views. This is conveniently handled by Laravel. Consider the following routes as an example:

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

Note that when validation fails, we pass the `Validator` instance to the Redirect using the `withErrors` method. This method will flash the error messages to the session so that they are available on the next request.

However, notice that we do not have to explicitly bind the error messages to the view in our GET route. This is because Laravel will always check for errors in the session data, and automatically bind them to the view if they are available. **So, it is important to note that an `$errors` variable will always be available in all of your views, on every request**, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `MessageBag`.

So, after redirection, you may utilize the automatically bound `$errors` variable in your view:

	<?php echo $errors->first('email'); ?>

<a name="mevcut-dogrulama-kurallari"></a>
## Mevcut Doğrulama Kuralları

Below is a list of all available validation rules and their function:

- [Accepted](#rule-accepted)
- [Active URL](#rule-active-url)
- [After (Date)](#rule-after)
- [Alpha](#rule-alpha)
- [Alpha Dash](#rule-alpha-dash)
- [Alpha Numeric](#rule-alpha-num)
- [Before (Date)](#rule-before)
- [Between](#rule-between)
- [Confirmed](#rule-confirmed)
- [Date](#rule-date)
- [Date Format](#rule-date-format)
- [Different](#rule-different)
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
- [Same](#rule-same)
- [Size](#rule-size)
- [Unique (Database)](#rule-unique)
- [URL](#rule-url)

<a name="rule-accepted"></a>
#### accepted

The field under validation must be _yes_, _on_, or _1_. This is useful for validating "Terms of Service" acceptance.

<a name="rule-active-url"></a>
#### active_url

The field under validation must be a valid URL according to the `checkdnsrr` PHP function.

<a name="rule-after"></a>
#### after:_date_

The field under validation must be a value after a given date. The dates will be passed into the PHP `strtotime` function.

<a name="rule-alpha"></a>
#### alpha

The field under validation must be entirely alphabetic characters.

<a name="rule-alpha-dash"></a>
#### alpha_dash

The field under validation may have alpha-numeric characters, as well as dashes and underscores.

<a name="rule-alpha-num"></a>
#### alpha_num

The field under validation must be entirely alpha-numeric characters.

<a name="rule-before"></a>
#### before:_date_

The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function.

<a name="rule-between"></a>
#### between:_min_,_max_

The field under validation must have a size between the given _min_ and _max_. Strings, numerics, and files are evaluated in the same fashion as the `size` rule.

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

<a name="rule-email"></a>
#### email

The field under validation must be formatted as an e-mail address.

<a name="rule-exists"></a>
#### exists:_table_,_column_

The field under validation must exists on a given database table.

**Basic Usage Of Exists Rule**

	'state' => 'exists:states'

**Specifying A Custom Column Name**

	'state' => 'exists:states,abbreviation'

You may also specify more conditions that will be added as "where" clauses to the query:

	'email' => 'exists:staff,email,account_id,1'

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

The field under validation must be less than a maximum _value_. Strings, numerics, and files are evaluated in the same fashion as the `size` rule.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

The file under validation must have a MIME type corresponding to one of the listed extensions.

**Basic Usage Of MIME Rule**

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
#### required_if:_field_,_value_

The field under validation must be present if the _field_ field is equal to _value_.

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

The field under validation must be present _only if_ the other specified fields are present.

<a name="rule-same"></a>
#### same:_field_

The given _field_ must match the field under validation.

<a name="rule-size"></a>
#### size:_value_

The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value. For files, _size_ corresponds to the file size in kilobytes.

<a name="rule-unique"></a>
#### unique:_table_,_column_,_except_,_idColumn_

The field under validation must be unique on a given database table. If the `column` option is not specified, the field name will be used.

**Basic Usage Of Unique Rule**

	'email' => 'unique:users'

**Specifying A Custom Column Name**

	'email' => 'unique:users,email_address'

**Forcing A Unique Rule To Ignore A Given ID**

	'email' => 'unique:users,email_address,10'

<a name="rule-url"></a>
#### url

The field under validation must be formatted as an URL.

<a name="ozel-hata-mesajlari"></a>
## Özel Hata Mesajları

If needed, you may use custom error messages for validation instead of the defaults. There are several ways to specify custom messages.

**Passing Custom Messages Into Validator**

	$messages = array(
		'required' => 'The :attribute field is required.',
	);

	$validator = Validator::make($input, $rules, $messages);

*Note:* The `:attribute` place-holder will be replaced by the actual name of the field under validation. You may also utilize other place-holders in validation messages.

**Other Validation Place-Holders**

	$messages = array(
		'same'    => 'The :attribute and :other must match.',
		'size'    => 'The :attribute must be exactly :size.',
		'between' => 'The :attribute must be between :min - :max.',
		'in'      => 'The :attribute must be one of the following types: :values',
	);

Sometimes you may wish to specify a custom error messages only for a specific field:

**Specifying A Custom Message For A Given Attribute**

	$messages = array(
		'email.required' => 'We need to know your e-mail address!',
	);

In some cases, you may wish to specify your custom messages in a language file instead of passing them directly to the `Validator`. To do so, add your messages to `custom` array in the `app/lang/xx/validation.php` language file.

**Specifying Custom Messages In Language Files**

	'custom' => array(
		'email' => array(
			'required' => 'We need to know your e-mail address!',
		),
	),

<a name="ozel-dogrulama-kurallari"></a>
## Özel Doğrulama Kuralları

Laravel provides a variety of helpful validation rules; however, you may wish to specify some of your own. One method of registering custom validation rules is using the `Validator::extend` method:

**Registering A Custom Validation Rule**

	Validator::extend('foo', function($attribute, $value, $parameters)
	{
		return $value == 'foo';
	});

> **Note:** The name of the rule passed to the `extend` method must be "snake cased".

The custom validator Closure receives three arguments: the name of the `$attribute` being validated, the `$value` of the attribute, and an array of `$parameters` passed to the rule.

You may also pass a class and method to the `extend` method instead of a Closure:

	Validator::extend('foo', 'FooValidator@validate');

Note that you will also need to define an error message for your custom rules. You can do so either using an inline custom message array or by adding an entry in the validation language file.

Instead of using Closure callbacks to extend the Validator, you may also extend the Validator class itself. To do so, write a Validator class that extends `Illuminate\Validation\Validator`. You may add validation methods to the class by prefixing them with `validate`:

**Extending The Validator Class**

	<?php

	class CustomValidator extends Illuminate\Validation\Validator {

		public function validateFoo($attribute, $value, $parameters)
		{
			return $value == 'foo';
		}

	}

Next, you need to register your custom Validator extension:

**Registering A Custom Validator Resolver**

	Validator::resolver(function($translator, $data, $rules, $messages)
	{
		return new CustomValidator($translator, $data, $rules, $messages);
	});

When creating a custom validation rule, you may sometimes need to define custom place-holder replacements for error messages. You may do so by creating a custom Validator as described above, and adding a `replaceXXX` function to the validator.

	protected function replaceFoo($message, $attribute, $rule, $parameters)
	{
		return str_replace(':foo', $parameters[0], $message);
	}
