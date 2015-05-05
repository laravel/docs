# Localization

- [Language Files](#language-files)
- [Basic Usage](#basic-usage)
- [Pluralization](#pluralization)
- [Validation Localization](#validation)
- [Overriding Package Language Files](#overriding-package-language-files)

<a name="language-files"></a>
## Language Files

Laravel provides a convenient way of retrieving strings in various languages, allowing you to easily support multiple languages within your application.

Language strings are stored in files within the `resources/lang` directory. Within this directory there should be a subdirectory for each language supported by the application.

	/resources
		/lang
			/en
				messages.php
			/es
				messages.php

#### Example Language File

Language files simply return an array of keyed strings. For example:

	<?php

	return [
		'welcome' => 'Welcome to our application'
	];

#### Changing The Default Language At Runtime

The default language for your application is stored in the `config/app.php` configuration file. You may change the active language at any time using the `setLocale` method on the `App` facade:

	Route::get('welcome/{locale}', function ($locale) {
		App::setLocale($locale);

		//
	});

#### Setting The Fallback Language

You may also configure a "fallback language", which will be used when the active language does not contain a given language line. Like the default language, the fallback language is also configured in the `config/app.php` configuration file:

	'fallback_locale' => 'en',

<a name="basic-usage"></a>
## Basic Usage

#### Retrieving Lines From A Language File

You may retrieve lines from language files using the `trans` helper function:

	echo trans('messages.welcome');

Of course if you are using the [Blade templating engine](/docs/{{version}}/views#blade-templating), you may use the `{{ }}` syntax to echo the language line:

	{{ trans('messages.welcome') }}

The first segment of the string passed to the `get` method is the name of the language file, and the second is the name of the line that should be retrieved.

> **Note:** If a language line does not exist, the key will be returned by the `get` method.

#### Replacing Parameters In Language Lines

You may also define place-holders in your language lines like so:

	'welcome' => 'Welcome, :name',

Then, pass an array of replacements as the second argument to the `trans` function:

	echo trans('messages.welcome', ['name' => 'Dayle']);

#### Validation Message Localization

For more information on localization for validation errors and messages, take a look at the [documentation on validation](/docs/{{version}}/validation#localiation).

<a name="pluralization"></a>
## Pluralization

Pluralization is a complex problem, as different languages have a variety of complex rules for pluralization. By using a "pipe" character, you may separate the singular and plural forms of a string:

	'apples' => 'There is one apple|There are many apples',

You may then use the `trans_choice` function to retrieve the line:

	echo trans_choice('messages.apples', 10);

Since the Laravel translator is powered by the Symfony Translation component, you may create more explicit pluralization rules easily:

	'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',

<a name="overriding-package-language-files"></a>
## Overriding Package Language Files

Many packages ship with their own language files. Instead of hacking the package's core files to tweak these lines, you may override them by placing files in the `resources/lang/vendor/{package}/{locale}` directory.

So, for example, if you need to override the English language lines in `messages.php` for a package named `skyrim/hearthfire`, you would place a language file at: `resources/lang/vendor/hearthfire/en/messages.php`. In this file you should only define the language lines you wish to override. Any language lines you don't override will still be loaded from the package's original language files.
