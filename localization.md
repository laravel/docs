# Localization

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)
    - [Pluralization](#pluralization)
- [Overriding Vendor Language Files](#overriding-vendor-language-files)

<a name="introduction"></a>
## Introduction

Laravel's localization features provide a convenient way to retrieve strings in various languages, allowing you to easily support multiple languages within your application.

Language strings are stored in files within the `resources/lang` directory. Within this directory there should be a subdirectory for each language supported by the application:

    /resources
        /lang
            /en
                messages.php
            /es
                messages.php

All language files simply return an array of keyed strings. For example:

    <?php

    return [
        'welcome' => 'Welcome to our application'
    ];

#### Configuring The Locale

The default language for your application is stored in the `config/app.php` configuration file. Of course, you may modify this value to suit the needs of your application. You may also change the active language at runtime using the `setLocale` method on the `App` facade:

    Route::get('welcome/{locale}', function ($locale) {
        App::setLocale($locale);

        //
    });

You may also configure a "fallback language", which will be used when the active language does not contain a given language line. Like the default language, the fallback language is also configured in the `config/app.php` configuration file:

    'fallback_locale' => 'en',

You may check if a given locale is currently being used by calling the `isLocale` method on the `App` [facade](/docs/{{version}}/facades):

    if (App::isLocale('en')) {
        //
    }

To retrieve the current application locale, call the `getLocale` method on the `App` [facade](/docs/{{version}}/facades):

    return App::getLocale();

<a name="basic-usage"></a>
## Basic Usage

You may retrieve lines from language files using the `trans` helper function. The `trans` method accepts the file and key of the language line as its first argument. For example, let's retrieve the language line `welcome` in the `resources/lang/messages.php` language file:

    echo trans('messages.welcome');

Of course if you are using the [Blade templating engine](/docs/{{version}}/blade), you may use the `{{ }}` syntax to echo the language line or use the `@lang` directive:

    {{ trans('messages.welcome') }}

    @lang('messages.welcome')

If the specified language line does not exist, the `trans` function will simply return the language line key. So, using the example above, the `trans` function would return `messages.welcome` if the language line does not exist.

#### Replacing Parameters In Language Lines

If you wish, you may define place-holders in your language lines. All place-holders are prefixed with a `:`. For example, you may define a welcome message with a place-holder name:

    'welcome' => 'Welcome, :name',

To replace the place-holders when retrieving a language line, pass an array of replacements as the second argument to the `trans` function:

    echo trans('messages.welcome', ['name' => 'dayle']);

If your place-holder contains all capital letters, or only has its first letter capitalized, the translated value will be capitalized accordingly:

    'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
    'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle


<a name="pluralization"></a>
### Pluralization

Pluralization is a complex problem, as different languages have a variety of complex rules for pluralization. By using a "pipe" character, you may distinguish a singular and plural form of a string:

    'apples' => 'There is one apple|There are many apples',

Then, you may use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the language line is returned:

    echo trans_choice('messages.apples', 10);

Since the Laravel translator is powered by the Symfony Translation component, you may create even more complex pluralization rules:

    'apples' => '{0} There are none|[1,19] There are some|[20,Inf] There are many',

<a name="overriding-vendor-language-files"></a>
## Overriding Vendor Language Files

Some packages may ship with their own language files. Instead of hacking the package's core files to tweak these lines, you may override them by placing your own files in the `resources/lang/vendor/{package}/{locale}` directory.

So, for example, if you need to override the English language lines in `messages.php` for a package named `skyrim/hearthfire`, you would place a language file at: `resources/lang/vendor/hearthfire/en/messages.php`. In this file you should only define the language lines you wish to override. Any language lines you don't override will still be loaded from the package's original language files.
