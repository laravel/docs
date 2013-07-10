# Forms & HTML

- [Form Açmak](#opening-a-form)
- [CSRF Koruması](#csrf-protection)
- [Form Model Bağlaması](#form-model-binding)
- [Labels](#labels)
- [Text, Text Area, Password & Hidden Fields](#text)
- [Checkboxes and Radio Buttons](#checkboxes-and-radio-buttons)
- [File Input](#file-input)
- [Drop-Down Lists](#drop-down-lists)
- [Buttonlar](#buttons)
- [Custom Macros](#custom-macros)

<a name="opening-a-form"></a>
## Form Açmak

**Form Açmak**

	{{ Form::open(array('url' => 'foo/bar')) }}
		//
	{{ Form::close() }}

Varsayılan olarak, `POST` metodu kullanılır; ancak, istediğiniz bir metodu da belirtebilirsiniz:

	echo Form::open(array('url' => 'foo/bar', 'method' => 'put'))

> **Not:** HTML formları, sadece `POST` metotlarını desteklediği için, `PUT` ve `DELETE` metotları otomatik olarak `_method` gizli alanıyla taklit edilir.

Ayrıca, isimlendirilmiş rotalar veya denetçi aksiyonlarına yönlendirilen formlar da açabilirsiniz:

	echo Form::open(array('route' => 'route.name'))

	echo Form::open(array('action' => 'Controller@method'))

Formunuz dosya yüklemelerini kabul edecekse, dizginize `files` seçeneğini ekleyin:

	echo Form::open(array('url' => 'foo/bar', 'files' => true))

<a name="csrf-protection"></a>
## CSRF Koruması

Laravel, uygulamanızı CSRF saldırılarından korumak için kolay bir metot sunar. Öncelikle, rastgele bir değer kullanıcının oturumuna yerleştirilir. Merak etmeyin, bu otomatik olarak yapılır. CSRF değeri, formlarınıza gizli bir alan olarak otomatik olarak yerleştirilir. Yine de, gizli alan için HTML kodunu oluşturmak isterseniz, `token` metodunu kullanabilirsiniz:

**Bir Forma CSRF Değeri Eklemek**

	echo Form::token();

**Bir Rotaya CSRF Filtresi Eklemek**

	Route::post('profile', array('before' => 'csrf', function()
	{
		//
	}));

<a name="form-model-binding"></a>
## Form Model Bağlaması

Sıklıkla, bir modelin içeriğine bağlı olarak bir form oluşturmak isteyebilirsiniz. Bunu yapmak için, `Form::model` metodunu kullanın:

**Model Formu Açmak**

	echo Form::model($user, array('route' => array('user.update', $user->id)))

Şimdi, bir form elementi oluşturduğunuzda, mesela bir text input, elementin ismiyle eşleşen modelin değeri, otomatik olarak alanın değeri olarak belirlenir. Yani, örneğin, `email` ismine sahip bir text alanı için, kullanıcı modelinin `email` değişkeni değer olarak atanır. Bununla birlikte, dahası da var! Session flash data'da alan adıyla eşleşen bir değer mevcutsa, bu değer, model'in değerine nazaran önceliği alacaktır. Yani, öncelik şu şekildedir:

1. Session Flash Data (Old Input)
2. Doğrudan Atanmış Değer
3. Model Değişken Değeri

This allows you to quickly build forms that not only bind to model values, but easily re-populate if there is a validation error on the server!

> **Note:** When using `Form::model`, be sure to close your form with `Form::close`!

<a name="labels"></a>
## Labels

**Generating A Label Element**

	echo Form::label('email', 'E-Mail Address');

**Specifying Extra HTML Attributes**

	echo Form::label('email', 'E-Mail Address', array('class' => 'awesome'));

> **Note:** After creating a label, any form element you create with a name matching the label name will automatically receive an ID matching the label name as well.

<a name="text"></a>
## Text, Text Area, Password & Hidden Fields

**Generating A Text Input**

	echo Form::text('username');

**Specifying A Default Value**

	echo Form::text('email', 'example@gmail.com');

> **Note:** The *hidden* and *textarea* methods have the same signature as the *text* method.

**Generating A Password Input**

	echo Form::password('password');

<a name="checkboxes-and-radio-buttons"></a>
## Checkboxes and Radio Buttons

**Generating A Checkbox Or Radio Input**

	echo Form::checkbox('name', 'value');
	
	echo Form::radio('name', 'value');

**Generating A Checkbox Or Radio Input That Is Checked**

	echo Form::checkbox('name', 'value', true);
	
	echo Form::radio('name', 'value', true);

<a name="file-input"></a>
## File Input

**Generating A File Input**

	echo Form::file('image');

<a name="drop-down-lists"></a>
## Drop-Down Lists

**Generating A Drop-Down List**

	echo Form::select('size', array('L' => 'Large', 'S' => 'Small'));

**Generating A Drop-Down List With Selected Default**

	echo Form::select('size', array('L' => 'Large', 'S' => 'Small'), 'S');

**Generating A Grouped List**

	echo Form::select('animal', array(
		'Cats' => array('leopard' => 'Leopard'),
		'Dogs' => array('spaniel' => 'Spaniel'),
	));

<a name="buttons"></a>
## Buttons

**Generating A Submit Button**

	echo Form::submit('Click Me!');

> **Note:** Need to create a button element? Try the *button* method. It has the same signature as *submit*.

<a name="custom-macros"></a>
## Custom Macros

It's easy to define your own custom Form class helpers called "macros". Here's how it works. First, simply register the macro with a given name and a Closure:

**Registering A Form Macro**

	Form::macro('myField', function()
	{
		return '<input type="awesome">';
	});

Now you can call your macro using its name:

**Calling A Custom Form Macro**

	echo Form::myField();
