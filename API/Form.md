## Form

The `Form` object includes methods related to creating HTML forms. It's useful for makig sign-in or data entry forms on your pages.

Most methods have one or two required arguments, and allow a third optional argument as an array. The array can contain attributes like `class` or `lang` for extra customization. Here is a blade example:

    {{ Class::method('argument1', 'argument2', array('attribute1' => 'value1', 'attribute2' => 'value2')) }}

- [Open](#open)
- [Label](#label)
- [Text](#text)
- [Password](#password)
- [Select](#select)
- [Submit](#submit)
- [Close](#close)

___

<a name="open"></a>

### Form::open()

This method begins the form. It needs to be placed before the other elemnts, and needs to be followed by a `Form::close()` after the elements.

#### Usage

    Form::open(array('url' => 'DESTINATION', [KEY' => 'VALUE']))

`DESTINATION` should be the url the `submit` button will take the user (usually the current page). This is required.

`KEY` should be another selector, such as `class`. This is optional.

'VALUE' should be the value of that class, for example the Bootstrap class `form-inline`.

#### Blade examples

    {{ Form::open(array('url' => 'admin', 'class' => 'form-inline')) }}

___

<a name="label"></a>

### Auth::label()

This method creates a form label, which is text next to another form element.

#### Usage

	{{ Form::label('FOR', 'TEXT') }}

`FOR` should be the element that label is for.

`TEXT` should be the plain text the label displays.

#### Blade Example

    {{ Form::label('name', 'Name') }}

___

<a name="text"></a>

### Form::text()

This method defines a route that's tri

#### Usage

	{{ Form::text(FORM_NAME, DEFAULT_TEXT array(ATTRIBUTE => VALUE)) }}

FORM_NAME should be the form's name in single quotes.

DEFAULT_TEXT should be the text in the form by default in single quotes, or just empty single quotes `''` for blank.

ATTRIBUTE should be any other HTML attributes for your text form, such as `class` or `placeholder`.

VALUE should be the value of the attribute.

NOTE: Default text is different thank placeholder text, becuase placeholder text usually disappears when a user begins typing in a form, while default text stays.

#### Examples

Asks the user for their email and assigns the Bootstrap 3 class for `form-control`.
	
	{{ Form::text('email', '' array('class' => 'form-control')) }}


___

<a name="password"></a>

### Form::password()

This method creates a password form, usually used for login.

#### Usage

	{{ Form::password(FORM_NAME, array(ATTRIBUTE => VALUE)) }}

FORM_NAME should be the name of the form.

ATTRIBUTE should be any HTML attribute you want to add.

VALUE should be the value of that attribute.

#### Examples

Creates a password form named 'password' and gives it the Bootstrap 3 class of `form-control`.

	{{ Form::password('password', array('class' => 'form-control')) }}


___

<a name="select"></a>

### Form::select()

This method creates a drop-down selector form element.

#### Usage
	
	<?php $ITEMS = array('1' => 'ITEM1', '2' => 'ITEM2') ?>
	{{ Form::select('NAME', $ITEMS, 'NULL', array('ATTRIBUTE' => 'VALUE')) }}

`NAME` should be the name of the form element. It's required.

`$ITEMS` should be an array with the options as the key and the plain text the form displays as the value. It is required.

`NULL` ???

`ATRIBUTE` and `VALUE` can be any additionaly HTML attributes added to this page element. They are not required.

#### Blade Example

	<?php $outList = array('0' => 'Fine', '1' => 'Iffy', '2' => 'Doomed'); ?>
	{{ Form::label('outlook', 'Outlook') }}
	{{ Form::select('outlook', $outList, 'NULL', array('class' => 'form-control')) }}

___

<a name="submit"></a>

### Form::submit()

This method ends the form. It needs to be placed after all the other elemnts, and needs to follow a `Form::open()` as the first `Form` item.

#### Usage

    Form::submit(BUTTON_TEXT, array(ATTRIBUTE => VALUE));

BUTTON_TEXT should be the text that will appear on the button.

ATTRIBUTE should be any HTML attribute you want to add, such as `class`.

VALUE should be the value of the attribute.

#### Blade examples

Creates a button with the label `Login` and the Bootstrap 3 classes of `btn`, `btn-primary` and `form-control`.

    {{ Form::submit('Login', array('class' => 'btn btn-primary form-control')) }}

___

<a name="close"></a>

### Form::close()

This method ends the form. It needs to be placed after all the other elemnts, and needs to follow a `Form::open()` as the first `Form` item.

#### Usage

    Form::close();

This method needs no arguments.

#### Blade examples

    {{ Form::close() }}