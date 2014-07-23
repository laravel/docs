## Form

The `Form` object includes methods related to creating HTML forms. It's useful for makig sign-in or data entry forms on your pages.

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

