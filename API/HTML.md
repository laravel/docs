## HTML

The HTML object includes methods to create links, include scripts or define styles. They are shorthand ways to return common HTML elements.

- [Style](#style)
- [Script](#script)
- [Link](#link)

___

<a name="style"></a>

### HTML::style()

This method sets the styesheet of a page. It returns the HTML element `link href` and sets the `type` to stylesheet. It can be much shorter and easier to remember than writing the HTML.

#### Usage

    echo HTML::style('PATH_TO_STYLE');

#### Blade example

    {{ HTML::style('../css/bootstrap.min.css') }}

___

<a name="script"></a>

### HTML::script()

This method loads a script. It returns the HTML element `<script>` and sets the type. It's useful for initiating javascript in the `head` or elsewhere.

#### Usage

    echo HTML::script('PATH_TO_SCRIPT');

#### Blade example

    {{ HTML::script('../js/bootstrap.min.js') }}

___

<a name="link"></a>

### HTML::link()

This method creates a link.

#### Usage

    echo HTML::link('PATH_TO_LINK', 'HYPERLINK_TEXT');

#### Blade example

    <li>{{ HTML::link('/', 'Home') }}</li>

___