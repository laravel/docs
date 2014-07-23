## Form

The `Form` object includes methods related to creating HTML forms. It's useful for makig sign-in or data entry forms on your pages.

Most methods have one or two required arguments, and allow a third optional argument as an array. The array can contain attributes like `class` or `lang` for extra customization. Here is a blade example:

    {{ Class::method('argument1', 'argument2', array('attribute1' => 'value1', 'attribute2' => 'value2')) }}

___

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

### Auth::label()

This method creates a form label, which is text next to another form element.

#### Usage

	{{ Form::label('FOR', 'TEXT') }}

`FOR` should be the element that label is for.

`TEXT` should be the plain text the label displays.

#### Blade Example

    {{ Form::label('name', 'Name') }}

___

### Auth::select()

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