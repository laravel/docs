# Validation

- [Basic Usage](#basic-usage)
- [Controller Validation](#controller-validation)
- [Form Request Validation](#form-request-validation)
- [Working With Error Messages](#working-with-error-messages)
- [Error Messages & Views](#error-messages-and-views)
- [Available Validation Rules](#available-validation-rules)
- [Conditionally Adding Rules](#conditionally-adding-rules)
- [Custom Error Messages](#custom-error-messages)
- [Custom Validation Rules](#custom-validation-rules)

<a name="basic-usage"></a>
## Basic Usage

Laravel ships with a simple, convenient facility for validating data and retrieving validation error messages via the `Validation` class.

#### Basic Validation Example

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => 'required|min:5')
	);

The first argument passed to the `make` method is the data under validation. The second argument is the validation rules that should be applied to the data.

#### Using Arrays To Specify Rules

Multiple rules may be delimited using either a "pipe" character, or as separate elements of an array.

	$validator = Validator::make(
		array('name' => 'Dayle'),
		array('name' => array('required', 'min:5'))
	);

#### Validating Multiple Fields

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

Once a `Validator` instance has been created, the `fails` (or `passes`) method may be used to perform the validation.

	if ($validator->fails())
	{
		// The given data did not pass validation
	}

If validation has failed, you may retrieve the error messages from the validator.

	$messages = $validator->messages();

You may also access an array of the failed validation rules, without messages. To do so, use the `failed` method:

	$failed = $validator->failed();

#### Validating Files

The `Validator` class provides several rules for validating files, such as `size`, `mimes`, and others. When validating files, you may simply pass them into the validator with your other data.

### After Validation Hook

The validator also allows you to attach callbacks to be run after validation is completed. This allows you to easily perform further validation, and even add more error messages to the message collection. To get started, use the `after` method on a validator instance:

	$validator = Validator::make(...);

	$validator->after(function($validator)
	{
		if ($this->somethingElseIsInvalid())
		{
			$validator->errors()->add('field', 'Something is wrong with this field!');
		}
	});

	if ($validator->fails())
	{
		//
	}

You may add as many `after` callbacks to a validator as needed.

<a name="controller-validation"></a>
## Controller Validation

Of course, manually creating and checking a `Validator` instance each time you do validation is a headache. Don't worry, you have other options! The base `App\Http\Controllers\Controller` class included with Laravel uses a `ValidatesRequests` trait. This trait provides a single, convenient method for validating incoming HTTP requests. Here's what it looks like:

	/**
	 * Store the incoming blog post.
	 *
	 * @param  Request  $request
	 * @return Response
	 */
	public function store(Request $request)
	{
		$this->validate($request, [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		]);

		//
	}

If validation passes, your code will keep executing normally. However, if validation fails, an `Illuminate\Contracts\Validation\ValidationException` will be thrown. This exception is automatically caught and a redirect is generated to the user's previous location. The validation errors are even automatically flashed to the session!

If the incoming request was an AJAX request, no redirect will be generated. Instead, an HTTP response with a 422 status code will be returned to the browser containing a JSON representation of the validation errors.

For example, here is the equivalent code written manually:

	/**
	 * Store the incoming blog post.
	 *
	 * @param  Request  $request
	 * @return Response
	 */
	public function store(Request $request)
	{
		$v = Validator::make($request->all(), [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		]);

		if ($v->fails())
		{
			return redirect()->back()->withErrors($v->errors());
		}

		//
	}

### Customizing The Flashed Error Format

If you wish to customize the format of the validation errors that are flashed to the session when validation fails, override the `formatValidationErrors` on your base controller. Don't forget to import the `Illuminate\Validation\Validator` class at the top of the file:

	/**
	 * {@inheritdoc}
	 */
	protected function formatValidationErrors(Validator $validator)
	{
		return $validator->errors()->all();
	}

<a name="form-request-validation"></a>
## Form Request Validation

For more complex validation scenarios, you may wish to create a "form request". Form requests are custom request classes that contain validation logic. To create a form request class, use the `make:request` Artisan CLI command:

	php artisan make:request StoreBlogPostRequest

The generated class will be placed in the `app/Http/Requests` directory. Let's add a few validation rules to the `rules` method:

	/**
	 * Get the validation rules that apply to the request.
	 *
	 * @return array
	 */
	public function rules()
	{
		return [
			'title' => 'required|unique|max:255',
			'body' => 'required',
		];
	}

So, how are the validation rules executed? All you need to do is type-hint the request on your controller method:

	/**
	 * Store the incoming blog post.
	 *
	 * @param  StoreBlogPostRequest  $request
	 * @return Response
	 */
	public function store(StoreBlogPostRequest $request)
	{
		// The incoming request is valid...
	}

The incoming form request is validated before the controller method is called, meaning you do not need to clutter your controller with any validation logic. It has already been validated!

If validation fails, a redirect response will be generated to send the user back to their previous location. The errors will also be flashed to the session so they are available for display. If the request was an AJAX request, a HTTP response with a 422 status code will be returned to the user including a JSON representation of the validation errors.

### Authorizing Form Requests

The form request class also contains an `authorize` method. Within this method, you may check if the authenticated user actually has the authority to update a given resource. For example, if a user is attempting to update a blog post comment, do they actually own that comment? For example:

	/**
	 * Determine if the user is authorized to make this request.
	 *
	 * @return bool
	 */
	public function authorize()
	{
		$commentId = $this->route('comment');

		return Comment::where('id', $commentId)
                      ->where('user_id', Auth::id())->exists();
	}

Note the call to the `route` method in the example above. This method grants you access to the URI parameters defined on the route being called, such as the `{comment}` parameter in the example below:

	Route::post('comment/{comment}');

If the `authorize` method returns `false`, a HTTP response with a 403 status code will automatically be returned and your controller method will not execute.

If you plan to have authorization logic in another part of your application, simply return `true` from the `authorize` method:

	/**
	 * Determine if the user is authorized to make this request.
	 *
	 * @return bool
	 */
	public function authorize()
	{
		return true;
	}

### Customizing The Flashed Error Format

If you wish to customize the format of the validation errors that are flashed to the session when validation fails, override the `formatValidationErrors` on your base request (`App\Http\Requests\Request`). Don't forget to import the `Illuminate\Validation\Validator` class at the top of the file:

	/**
	 * {@inheritdoc}
	 */
	protected function formatErrors(Validator $validator)
	{
		return $validator->errors()->all();
	}

<a name="working-with-error-messages"></a>
## Working With Error Messages

After calling the `messages` method on a `Validator` instance, you will receive a `MessageBag` instance, which has a variety of convenient methods for working with error messages.

#### Retrieving The First Error Message For A Field

	echo $messages->first('email');

#### Retrieving All Error Messages For A Field

	foreach ($messages->get('email') as $message)
	{
		//
	}

#### Retrieving All Error Messages For All Fields

	foreach ($messages->all() as $message)
	{
		//
	}

#### Determining If Messages Exist For A Field

	if ($messages->has('email'))
	{
		//
	}

#### Retrieving An Error Message With A Format

	echo $messages->first('email', '<p>:message</p>');

> **Note:** By default, messages are formatted using Bootstrap compatible syntax.

#### Retrieving All Error Messages With A Format

	foreach ($messages->all('<li>:message</li>') as $message)
	{
		//
	}

<a name="error-messages-and-views"></a>
## Error Messages & Views

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
			return redirect('register')->withErrors($validator);
		}
	});

Note that when validation fails, we pass the `Validator` instance to the Redirect using the `withErrors` method. This method will flash the error messages to the session so that they are available on the next request.

However, notice that we do not have to explicitly bind the error messages to the view in our GET route. This is because Laravel will always check for errors in the session data, and automatically bind them to the view if they are available. **So, it is important to note that an `$errors` variable will always be available in all of your views, on every request**, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `MessageBag`.

So, after redirection, you may utilize the automatically bound `$errors` variable in your view:

	<?php echo $errors->first('email'); ?>

### Named Error Bags

If you have multiple forms on a single page, you may wish to name the `MessageBag` of errors. This will allow you to retrieve the error messages for a specific form. Simply pass a name as the second argument to `withErrors`:

	return redirect('register')->withErrors($validator, 'login');

You may then access the named `MessageBag` instance from the `$errors` variable:

	<?php echo $errors->login->first('email'); ?>

<a name="available-validation-rules"></a>
## Available Validation Rules

Below is a list of all available validation rules and their function:

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
- [String](#rule-string)
- [Timezone](#rule-timezone)
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

<a name="rule-array"></a>
#### array

The field under validation must be of type array.

<a name="rule-before"></a>
#### before:_date_

The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function.

<a name="rule-between"></a>
#### between:_min_,_max_

The field under validation must have a size between the given _min_ and _max_. Strings, numerics, and files are evaluated in the same fashion as the `size` rule.

<a name="rule-boolean"></a>
#### boolean

The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"` and `"0"`.

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

The file under validation must be an image (jpeg, png, bmp, gif, or svg)

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

The field under validation must be less than or equal to a maximum _value_. Strings, numerics, and files are evaluated in the same fashion as the [`size`](#rule-size) rule.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

The file under validation must have a MIME type corresponding to one of the listed extensions.

#### Basic Usage Of MIME Rule

	'photo' => 'mimes:jpeg,bmp,png'

<a name="rule-min"></a>
#### min:_value_

The field under validation must have a minimum _value_. Strings, numerics, and files are evaluated in the same fashion as the [`size`](#rule-size) rule.

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
#### required_if:_field_,_value_,...

The field under validation must be present if the _field_ field is equal to any _value_.

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

The field under validation must be present _only when_ all of the other specified fields are not present.

<a name="rule-same"></a>
#### same:_field_

The given _field_ must match the field under validation.

<a name="rule-size"></a>
#### size:_value_

The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value. For files, _size_ corresponds to the file size in kilobytes.

<a name="rule-string"></a>
#### string:_value_

The field under validation must be a string type.

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

In some cases, you may wish to specify your custom messages in a language file instead of passing them directly to the `Validator`. To do so, add your messages to `custom` array in the `resources/lang/xx/validation.php` language file.

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
