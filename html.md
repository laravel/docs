# HTML

- [Entities](#entities)
- [Scripts and Style Sheets](#scripts-and-style-sheets)
- [Links](#links)
- [Links to Named Routes](#links-to-named-routes)
- [Links to Controller Actions](#links-to-controller-actions)
- [Mail-To Links](#mail-to-links)
- [Lists](#lists)
- [Custom Macros](#custom-macros)

<a name="entities"></a>
## Entities

When displaying user input in your Views, it is important to convert all characters which have significance in HTML to their "entity" representation.

For example, the < symbol should be converted to its entity representation. Converting HTML characters to their entity representation helps protect your application from cross-site scripting:

Converting a string to its entity representation:

	echo HTML::entities('<h4>Taylor & Friends</h4>');

Using the "e" function global helper:

	echo e('<h4>Taylor & Friends</h4>');

You can also decode an entity string:

	echo decode('&lt;h4&gt;Taylor &amp; Friends&lt;/h4&gt;');

<a name="scripts-and-style-sheets"></a>
## Scripts and Style Sheets

Generating a reference to a JavaScript file:

	echo HTML::script('js/scrollTo.js');

Generating a reference to a CSS file:

	echo HTML::style('css/main.css');

Generating a reference to a CSS file using a given media type:

	echo HTML::style('css/common.css', array('media' => 'print'));

> **Note** The following attribute defaults are set for you: 'media'='all', 'type'='text/css', 'rel'='stylesheet'. The above simply overrides these defaults.

<a name="links"></a>
**Links**

Generating a link from a URI:

	echo HTML::link('user/profile', 'User Profile');

Generating a link from a URI using HTTPS:

	echo HTML::secureLink('user/profile', 'Secure User Profile');

Generating a link and specifiying extra HTML attributes:

	echo HTML::link('user/profile', 'User Profile', array('id' => 'profile_link'));

Generating links directly to assets:

	echo HTML::linkAsset('css/main.css', 'Check out our style!');

	echo HTML::linkSecureAsset('js/scrollTo.js');

> **Note** Many of these have global [helper function](/docs/helpers#urls) equivalents similar to the "e" function.

<a name="links-to-named-routes"></a>
**Links to Named Routes**

Generating a link to a named route:

	echo HTML::linkRoute('profile', 'User Profile', array($username));

> **Note** You should check out the [Route Parameters](/docs/routing#route-parameters) section of the docs for more info.

<a name="links-to-controller-actions"></a>
**Links to Controller Actions**

Generating a link to a controller action:

	echo HTML::linkAction('home@index', 'Home');

Generating a link to a controller action with wildcard values:

	echo HTML::linkAction('user@profile', 'User Profile', array($username));

<a name="mail-to-links"></a>
**Mail-To Links**

The "mailto" method on the HTML class obfuscates the given e-mail address so it is not sniffed by bots.

Creating a mail-to link:

	echo HTML::mailto('support@company.com');

Creating a mail-to links with a specified title:

	echo HTML::mailto('support@company.com', 'Get in touch');

<a name="lists"></a>
**Lists**

Creating lists from an array of items:

	echo HTML::ol(array('Fill out TPS reports', 'Meeting with the Bobs', 'Lunch'));

	echo HTML::ul(array('Reduce', 'Reuse', 'Recycle'));

<a name="custom-macros"></a>
**Custom Macros**

It's easy to define your own custom HTML class helpers called "macros". Here's how it works. First, simply register the macro with a given name and a Closure:

	HTML::macro('myElement', function($content)
	{
		return '<span class="product">' . $content . '</span>';
	});

Now you can call your macro using its name:

	HTML::myElement('Is awesome.');