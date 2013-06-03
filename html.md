# Forms & HTML

- [Opening A Form](#opening-a-form)
- [CSRF Protection](#csrf-protection)
- [Form Model Binding](#form-model-binding)
- [Labels](#labels)
- [Text, Text Area, Password & Hidden Fields](#text)
- [Checkboxes and Radio Buttons](#checkboxes-and-radio-buttons)
- [File Input](#file-input)
- [Drop-Down Lists](#drop-down-lists)
- [Buttons](#buttons)
- [Custom Macros](#custom-macros)

<a name="opening-a-form"></a>
## Opening A Form

<a name="opening-a-form"></a>
**Opening A Form**

	{{ Form::open(array('url' => 'foo/bar')) }}
		//
	{{ Form::close() }}

By default, a `POST` method will be assumed; however, you are free to specify another method:

	echo Form::open(array('url' => 'foo/bar', 'method' => 'put'))

> **Note:** Since HTML forms only support `POST`, `PUT` and `DELETE` methods will be spoofed by automatically adding a `_method` hidden field to your form.

You may also open forms that point to named routes or controller actions:

	echo Form::open(array('route' => 'route.name'))

	echo Form::open(array('action' => 'Controller@method'))

If your form is going to accept file uploads, add a `files` option to your array:

	echo Form::open(array('url' => 'foo/bar', 'files' => true))

<a name="csrf-protection"></a>
## CSRF Protection

Laravel provides an easy method of protecting your application from cross-site request forgeries. First, a random token is placed in your user's session. Don't sweat it, this is done automatically. The CSRF token will be added to your forms as a hidden field automatically. However, if you wish to generate the HTML for the hidden field, you may use the `token` method:

<a name="adding-the-csrf-token-to-a-form"></a>
**Adding The CSRF Token To A Form**

	echo Form::token();

<a name="attaching-the-csrf-filter-to-a-route"></a>
**Attaching The CSRF Filter To A Route**

	Route::post('profile', array('before' => 'csrf', function()
	{
		//
	}));

<a name="form-model-binding"></a>
## Form Model Binding

Often, you will want to populate a form based on the contents of a model. To do so, use the `Form::model` method:

<a name="opening-a-model-form"></a>
**Opening A Model Form**

	echo Form::model($user, array('route' => array('user.update', $user->id)))

Now, when you generate a form element, like a text input, the model's value matching the field's name will automatically be set as the field value. So, for example, for a text input named `email`, the user model's `email` attribute would be set as the value. However, there's more! If there is an item in the Session flash data matching the input name, that will take precedence over the model's value. So, the priority looks like this:

1. Session Flash Data (Old Input)
2. Explicitly Passed Value
3. Model Attribute Data

This allows you to quickly build forms that not only bind to model values, but easily re-populate if there is a validation error on the server!

> **Note:** When using `Form::model`, be sure to close your form with `Form::close`!

<a name="labels"></a>
## Labels

<a name="generating-a-label-element"></a>
**Generating A Label Element**

	echo Form::label('email', 'E-Mail Address');

<a name="specifying-extra-html-attributes"></a>
**Specifying Extra HTML Attributes**

	echo Form::label('email', 'E-Mail Address', array('class' => 'awesome'));

> **Note:** After creating a label, any form element you create with a name matching the label name will automatically receive an ID matching the label name as well.

<a name="text"></a>
## Text, Text Area, Password & Hidden Fields

<a name="generating-a-text-input"></a>
**Generating A Text Input**

	echo Form::text('username');

<a name="specifying-a-default-value"></a>
**Specifying A Default Value**

	echo Form::text('email', 'example@gmail.com');

> **Note:** The *hidden* and *textarea* methods have the same signature as the *text* method.

<a name="generating-a-password-input"></a>
**Generating A Password Input**

	echo Form::password('password');

<a name="checkboxes-and-radio-buttons"></a>
## Checkboxes and Radio Buttons

<a name="generating-a-checkbox-or-radio-input"></a>
**Generating A Checkbox Or Radio Input**

	echo Form::checkbox('name', 'value');

	echo Form::radio('name', 'value');

<a name="generating-a-checkbox-or-radio-input-that-is-checked"></a>
**Generating A Checkbox Or Radio Input That Is Checked**

	echo Form::checkbox('name', 'value', true);

	echo Form::radio('name', 'value', true);

<a name="file-input"></a>
## File Input

<a name="generating-a-file-input"></a>
**Generating A File Input**

	echo Form::file('image');

<a name="drop-down-lists"></a>
## Drop-Down Lists

<a name="generating-a-drop-down-list"></a>
**Generating A Drop-Down List**

	echo Form::select('size', array('L' => 'Large', 'S' => 'Small'));

<a name="generating-a-drop-down-list-with-selected-default"></a>
**Generating A Drop-Down List With Selected Default**

	echo Form::select('size', array('L' => 'Large', 'S' => 'Small'), 'S');

<a name="generating-a-grouped-list"></a>
**Generating A Grouped List**

	echo Form::select('animal', array(
		'Cats' => array('leopard' => 'Leopard'),
		'Dogs' => array('spaniel' => 'Spaniel'),
	));

<a name="buttons"></a>
## Buttons

<a name="generating-a-submit-button"></a>
**Generating A Submit Button**

	echo Form::submit('Click Me!');

> **Note:** Need to create a button element? Try the *button* method. It has the same signature as *submit*.

<a name="custom-macros"></a>
## Custom Macros

It's easy to define your own custom Form class helpers called "macros". Here's how it works. First, simply register the macro with a given name and a Closure:

<a name="registering-a-form-macro"></a>
**Registering A Form Macro**

	Form::macro('myField', function()
	{
		return '<input type="awesome">';
	});

Now you can call your macro using its name:

<a name="calling-a-custom-form-macro"></a>
**Calling A Custom Form Macro**

	echo Form::myField();
