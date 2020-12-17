# Laravel Dusk

- [Introduction](#introduction)
- [Installation](#installation)
    - [Managing ChromeDriver Installations](#managing-chromedriver-installations)
    - [Using Other Browsers](#using-other-browsers)
- [Getting Started](#getting-started)
    - [Generating Tests](#generating-tests)
    - [Database Migrations](#migrations)
    - [Running Tests](#running-tests)
    - [Environment Handling](#environment-handling)
- [Browser Basics](#browser-basics)
    - [Creating Browsers](#creating-browsers)
    - [Navigation](#navigation)
    - [Resizing Browser Windows](#resizing-browser-windows)
    - [Browser Macros](#browser-macros)
    - [Authentication](#authentication)
    - [Cookies](#cookies)
    - [Executing JavaScript](#executing-javascript)
    - [Taking A Screenshot](#taking-a-screenshot)
    - [Storing Console Output To Disk](#storing-console-output-to-disk)
    - [Storing Page Source To Disk](#storing-page-source-to-disk)
- [Interacting With Elements](#interacting-with-elements)
    - [Dusk Selectors](#dusk-selectors)
    - [Text, Values, & Attributes](#text-values-and-attributes)
    - [Interacting With Forms](#interacting-with-forms)
    - [Attaching Files](#attaching-files)
    - [Pressing Buttons](#pressing-buttons)
    - [Clicking Links](#clicking-links)
    - [Using The Keyboard](#using-the-keyboard)
    - [Using The Mouse](#using-the-mouse)
    - [JavaScript Dialogs](#javascript-dialogs)
    - [Scoping Selectors](#scoping-selectors)
    - [Waiting For Elements](#waiting-for-elements)
    - [Scrolling An Element Into View](#scrolling-an-element-into-view)
- [Available Assertions](#available-assertions)
- [Pages](#pages)
    - [Generating Pages](#generating-pages)
    - [Configuring Pages](#configuring-pages)
    - [Navigating To Pages](#navigating-to-pages)
    - [Shorthand Selectors](#shorthand-selectors)
    - [Page Methods](#page-methods)
- [Components](#components)
    - [Generating Components](#generating-components)
    - [Using Components](#using-components)
- [Continuous Integration](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## Introduction

Laravel Dusk provides an expressive, easy-to-use browser automation and testing API. By default, Dusk does not require you to install JDK or Selenium on your local computer. Instead, Dusk uses a standalone [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home) installation. However, you are free to utilize any other Selenium compatible driver you wish.

<a name="installation"></a>
## Installation

To get started, you should add the `laravel/dusk` Composer dependency to your project:

    composer require --dev laravel/dusk

> {note} If you are manually registering Dusk's service provider, you should **never** register it in your production environment, as doing so could lead to arbitrary users being able to authenticate with your application.

After installing the Dusk package, execute the `dusk:install` Artisan command. The `dusk:install` command will create a `tests/Browser` directory and an example Dusk test:

    php artisan dusk:install

Next, set the `APP_URL` environment variable in your application's `.env` file. This value should match the URL you use to access your application in a browser.

> {tip} If you are using [Laravel Sail](/docs/{{version}}/sail) to manage your local development environment, please also consult the Sail documentation on [configuring and running Dusk tests](/docs/{{version}}/sail#laravel-dusk).

<a name="managing-chromedriver-installations"></a>
### Managing ChromeDriver Installations

If you would like to install a different version of ChromeDriver than what is included with Laravel Dusk, you may use the `dusk:chrome-driver` command:

    # Install the latest version of ChromeDriver for your OS...
    php artisan dusk:chrome-driver

    # Install a given version of ChromeDriver for your OS...
    php artisan dusk:chrome-driver 86

    # Install a given version of ChromeDriver for all supported OSs...
    php artisan dusk:chrome-driver --all

    # Install the version of ChromeDriver that matches the detected version of Chrome / Chromium for your OS...
    php artisan dusk:chrome-driver --detect

> {note} Dusk requires the `chromedriver` binaries to be executable. If you're having problems running Dusk, you should ensure the binaries are executable using the following command: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### Using Other Browsers

By default, Dusk uses Google Chrome and a standalone [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home) installation to run your browser tests. However, you may start your own Selenium server and run your tests against any browser you wish.

To get started, open your `tests/DuskTestCase.php` file, which is the base Dusk test case for your application. Within this file, you can remove the call to the `startChromeDriver` method. This will stop Dusk from automatically starting the ChromeDriver:

    /**
     * Prepare for Dusk test execution.
     *
     * @beforeClass
     * @return void
     */
    public static function prepare()
    {
        // static::startChromeDriver();
    }

Next, you may modify the `driver` method to connect to the URL and port of your choice. In addition, you may modify the "desired capabilities" that should be passed to the WebDriver:

    /**
     * Create the RemoteWebDriver instance.
     *
     * @return \Facebook\WebDriver\Remote\RemoteWebDriver
     */
    protected function driver()
    {
        return RemoteWebDriver::create(
            'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs()
        );
    }

<a name="getting-started"></a>
## Getting Started

<a name="generating-tests"></a>
### Generating Tests

To generate a Dusk test, use the `dusk:make` Artisan command. The generated test will be placed in the `tests/Browser` directory:

    php artisan dusk:make LoginTest

<a name="migrations"></a>
### Database Migrations

Most of the tests you write will interact with pages that retrieve data from your application's database; however, your Dusk tests should never use the `RefreshDatabase `trait. The `RefreshDatabase` trait leverages database transactions which will not be applicable or available across HTTP requests. Instead, use the `DatabaseMigrations` trait, which re-migrates the database for each test:

    <?php

    namespace Tests\Browser;

    use App\Models\User;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Laravel\Dusk\Chrome;
    use Tests\DuskTestCase;

    class ExampleTest extends DuskTestCase
    {
        use DatabaseMigrations;
    }

> {note} SQLite in-memory databases may not be used when executing Dusk tests. Since the browser executes within its own process, it will not be able to access the in-memory databases of other processes.

<a name="running-tests"></a>
### Running Tests

To run your browser tests, execute the `dusk` Artisan command:

    php artisan dusk

If you had test failures the last time you ran the `dusk` command, you may save time by re-running the failing tests first using the `dusk:fails` command:

    php artisan dusk:fails

The `dusk` command accepts any argument that is normally accepted by the PHPUnit test runner, such as allowing you to only run the tests for a given [group](https://phpunit.de/manual/current/en/appendixes.annotations.html#appendixes.annotations.group):

    php artisan dusk --group=foo

> {tip} If you are using [Laravel Sail](/docs/{{version}}/sail) to manage your local development environment, please consult the Sail documentation on [configuring and running Dusk tests](/docs/{{version}}/sail#laravel-dusk).

<a name="manually-starting-chromedriver"></a>
#### Manually Starting ChromeDriver

By default, Dusk will automatically attempt to start ChromeDriver. If this does not work for your particular system, you may manually start ChromeDriver before running the `dusk` command. If you choose to start ChromeDriver manually, you should comment out the following line of your `tests/DuskTestCase.php` file:

    /**
     * Prepare for Dusk test execution.
     *
     * @beforeClass
     * @return void
     */
    public static function prepare()
    {
        // static::startChromeDriver();
    }

In addition, if you start ChromeDriver on a port other than 9515, you should modify the `driver` method of the same class to reflect the correct port:

    /**
     * Create the RemoteWebDriver instance.
     *
     * @return \Facebook\WebDriver\Remote\RemoteWebDriver
     */
    protected function driver()
    {
        return RemoteWebDriver::create(
            'http://localhost:9515', DesiredCapabilities::chrome()
        );
    }

<a name="environment-handling"></a>
### Environment Handling

To force Dusk to use its own environment file when running tests, create a `.env.dusk.{environment}` file in the root of your project. For example, if you will be initiating the `dusk` command from your `local` environment, you should create a `.env.dusk.local` file.

When running tests, Dusk will back-up your `.env` file and rename your Dusk environment to `.env`. Once the tests have completed, your `.env` file will be restored.

<a name="browser-basics"></a>
## Browser Basics

<a name="creating-browsers"></a>
### Creating Browsers

To get started, let's write a test that verifies we can log into our application. After generating a test, we can modify it to navigate to the login page, enter some credentials, and click the "Login" button. To create a browser instance, you may call the `browse` method from within your Dusk test:

    <?php

    namespace Tests\Browser;

    use App\Models\User;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Laravel\Dusk\Chrome;
    use Tests\DuskTestCase;

    class ExampleTest extends DuskTestCase
    {
        use DatabaseMigrations;

        /**
         * A basic browser test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $user = User::factory()->create([
                'email' => 'taylor@laravel.com',
            ]);

            $this->browse(function ($browser) use ($user) {
                $browser->visit('/login')
                        ->type('email', $user->email)
                        ->type('password', 'password')
                        ->press('Login')
                        ->assertPathIs('/home');
            });
        }
    }

As you can see in the example above, the `browse` method accepts a closure. A browser instance will automatically be passed to this closure by Dusk and is the main object used to interact with and make assertions against your application.

<a name="creating-multiple-browsers"></a>
#### Creating Multiple Browsers

Sometimes you may need multiple browsers in order to properly carry out a test. For example, multiple browsers may be needed to test a chat screen that interacts with websockets. To create multiple browsers, simply add more browser arguments to the signature of the closure given to the `browse` method:

    $this->browse(function ($first, $second) {
        $first->loginAs(User::find(1))
              ->visit('/home')
              ->waitForText('Message');

        $second->loginAs(User::find(2))
               ->visit('/home')
               ->waitForText('Message')
               ->type('message', 'Hey Taylor')
               ->press('Send');

        $first->waitForText('Hey Taylor')
              ->assertSee('Jeffrey Way');
    });

<a name="navigation"></a>
### Navigation

The `visit` method may be used to navigate to a given URI within your application:

    $browser->visit('/login');

You may use the `visitRoute` method to navigate to a [named route](/docs/{{version}}/routing#named-routes):

    $browser->visitRoute('login');

You may navigate "back" and "forward" using the `back` and `forward` methods:

    $browser->back();

    $browser->forward();

You may use the `refresh` method to refresh the page:

    $browser->refresh();

<a name="resizing-browser-windows"></a>
### Resizing Browser Windows

You may use the `resize` method to adjust the size of the browser window:

    $browser->resize(1920, 1080);

The `maximize` method may be used to maximize the browser window:

    $browser->maximize();

The `fitContent` method will resize the browser window to match the size of its content:

    $browser->fitContent();

When a test fails, Dusk will automatically resize the browser to fit the content prior to taking a screenshot. You may disable this feature by calling the `disableFitOnFailure` method within your test:

    $browser->disableFitOnFailure();

You may use the `move` method to move the browser window to a different position on your screen:

    $browser->move($x = 100, $y = 100);

<a name="browser-macros"></a>
### Browser Macros

If you would like to define a custom browser method that you can re-use in a variety of your tests, you may use the `macro` method on the `Browser` class. Typically, you should call this method from a [service provider's](/docs/{{version}}/providers) `boot` method:

    <?php

    namespace App\Providers;

    use Illuminate\Support\ServiceProvider;
    use Laravel\Dusk\Browser;

    class DuskServiceProvider extends ServiceProvider
    {
        /**
         * Register Dusk's browser macros.
         *
         * @return void
         */
        public function boot()
        {
            Browser::macro('scrollToElement', function ($element = null) {
                $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");

                return $this;
            });
        }
    }

The `macro` function accepts a name as its first argument, and a closure as its second. The macro's closure will be executed when calling the macro as a method on a `Browser` instance:

    $this->browse(function ($browser) use ($user) {
        $browser->visit('/pay')
                ->scrollToElement('#credit-card-details')
                ->assertSee('Enter Credit Card Details');
    });

<a name="authentication"></a>
### Authentication

Often, you will be testing pages that require authentication. You can use Dusk's `loginAs` method in order to avoid interacting with your application's login screen during every test. The `loginAs` method accepts a primary key associated with your authenticatable model or an authenticatable model instance:

    use App\Models\User;

    $this->browse(function ($browser) {
        $browser->loginAs(User::find(1))
              ->visit('/home');
    });

> {note} After using the `loginAs` method, the user session will be maintained for all tests within the file.

<a name="cookies"></a>
### Cookies

You may use the `cookie` method to get or set an encrypted cookie's value. By default, all of the cookies created by Laravel are encrypted:

    $browser->cookie('name');

    $browser->cookie('name', 'Taylor');

You may use the `plainCookie` method to get or set an unencrypted cookie's value:

    $browser->plainCookie('name');

    $browser->plainCookie('name', 'Taylor');

You may use the `deleteCookie` method to delete the given cookie:

    $browser->deleteCookie('name');

<a name="executing-javascript"></a>
### Executing JavaScript

You may use the `script` method to execute arbitrary JavaScript statements within the browser:

    $output = $browser->script('document.documentElement.scrollTop = 0');

    $output = $browser->script([
        'document.body.scrollTop = 0',
        'document.documentElement.scrollTop = 0',
    ]);

<a name="taking-a-screenshot"></a>
### Taking A Screenshot

You may use the `screenshot` method to take a screenshot and store it with the given filename. All screenshots will be stored within the `tests/Browser/screenshots` directory:

    $browser->screenshot('filename');

<a name="storing-console-output-to-disk"></a>
### Storing Console Output To Disk

You may use the `storeConsoleLog` method to write the current browser's console output to disk with the given filename. Console output will be stored within the `tests/Browser/console` directory:

    $browser->storeConsoleLog('filename');

<a name="storing-page-source-to-disk"></a>
### Storing Page Source To Disk

You may use the `storeSource` method to write the current page's source to disk with the given filename. The page source will be stored within the `tests/Browser/source` directory:

    $browser->storeSource('filename');

<a name="interacting-with-elements"></a>
## Interacting With Elements

<a name="dusk-selectors"></a>
### Dusk Selectors

Choosing good CSS selectors for interacting with elements is one of the hardest parts of writing Dusk tests. Over time, frontend changes can cause CSS selectors like the following to break your tests:

    // HTML...

    <button>Login</button>

    // Test...

    $browser->click('.login-page .container div > button');

Dusk selectors allow you to focus on writing effective tests rather than remembering CSS selectors. To define a selector, add a `dusk` attribute to your HTML element. Then, when interacting with a Dusk browser, prefix the selector with `@` to manipulate the attached element within your test:

    // HTML...

    <button dusk="login-button">Login</button>

    // Test...

    $browser->click('@login-button');

<a name="text-values-and-attributes"></a>
### Text, Values, & Attributes

<a name="retrieving-setting-values"></a>
#### Retrieving & Setting Values

Dusk provides several methods for interacting with the current display text, value, and attributes of elements on the page. For example, to get the "value" of an element that matches a given CSS or Dusk selector, use the `value` method:

    // Retrieve the value...
    $value = $browser->value('selector');

    // Set the value...
    $browser->value('selector', 'value');

You may use the `inputValue` method to get the "value" of an input element that has a given field name:

    $value = $browser->inputValue('field');

<a name="retrieving-text"></a>
#### Retrieving Text

The `text` method may be used to retrieve the display text of an element that matches the given selector:

    $text = $browser->text('selector');

<a name="retrieving-attributes"></a>
#### Retrieving Attributes

Finally, the `attribute` method may be used to retrieve the value of an attribute of an element matching the given selector:

    $attribute = $browser->attribute('selector', 'value');

<a name="interacting-with-forms"></a>
### Interacting With Forms

<a name="typing-values"></a>
#### Typing Values

Dusk provides a variety of methods for interacting with forms and input elements. First, let's take a look at an example of typing text into an input field:

    $browser->type('email', 'taylor@laravel.com');

Note that, although the method accepts one if necessary, we are not required to pass a CSS selector into the `type` method. If a CSS selector is not provided, Dusk will search for an `input` or `textarea` field with the given `name` attribute.

To append text to a field without clearing its content, you may use the `append` method:

    $browser->type('tags', 'foo')
            ->append('tags', ', bar, baz');

You may clear the value of an input using the `clear` method:

    $browser->clear('email');

You can instruct Dusk to type slowly using the `typeSlowly` method. By default, Dusk will pause for 100 milliseconds between key presses. To customize the amount of time between key presses, you may pass the appropriate number of milliseconds as the third argument to the method:

    $browser->typeSlowly('mobile', '+1 (202) 555-5555');

    $browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);

You may use the `appendSlowly` method to append text slowly:

    $browser->type('tags', 'foo')
            ->appendSlowly('tags', ', bar, baz');

<a name="dropdowns"></a>
#### Dropdowns

To select a value available on a `select` element, you may use the `select` method. Like the `type` method, the `select` method does not require a full CSS selector. When passing a value to the `select` method, you should pass the underlying option value instead of the display text:

    $browser->select('size', 'Large');

You may select a random option by omitting the second argument:

    $browser->select('size');

<a name="checkboxes"></a>
#### Checkboxes

To "check" a checkbox input, you may use the `check` method. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a checkbox with a matching `name` attribute:

    $browser->check('terms');

The `uncheck` method may be used to "uncheck" a checkbox input:

    $browser->uncheck('terms');

<a name="radio-buttons"></a>
#### Radio Buttons

To "select" a `radio` input option, you may use the `radio` method. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a `radio` input with matching `name` and `value` attributes:

    $browser->radio('size', 'large');

<a name="attaching-files"></a>
### Attaching Files

The `attach` method may be used to attach a file to a `file` input element. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a `file` input with a matching `name` attribute:

    $browser->attach('photo', __DIR__.'/photos/mountains.png');

> {note} The attach function requires the `Zip` PHP extension to be installed and enabled on your server.

<a name="pressing-buttons"></a>
### Pressing Buttons

The `press` method may be used to click a button element on the page. The first argument given to the `press` method may be either the display text of the button or a CSS / Dusk selector:

    $browser->press('Login');

When submitting forms, many application's disable the form's submission button after it are pressed and then re-enable the button when the form submission's HTTP request is complete. To press a button and wait for the button to be re-enabled, you may use the `pressAndWaitFor` method:

    // Press the button and wait a maximum of 5 seconds for it to be enabled...
    $browser->pressAndWaitFor('Save');

    // Press the button and wait a maximum of 1 second for it to be enabled...
    $browser->pressAndWaitFor('Save', 1);

<a name="clicking-links"></a>
### Clicking Links

To click a link, you may use the `clickLink` method on the browser instance. The `clickLink` method will click the link that has the given display text:

    $browser->clickLink($linkText);

You may use the `seeLink` method to determine if a link with the given display text is visible on the page:

    if ($browser->seeLink($linkText)) {
        // ...
    }

> {note} These methods interact with jQuery. If jQuery is not available on the page, Dusk will automatically inject it into the page so it is available for the test's duration.

<a name="using-the-keyboard"></a>
### Using The Keyboard

The `keys` method allows you to provide more complex input sequences to a given element than normally allowed by the `type` method. For example, you may instruct Dusk to hold modifier keys while entering values. In this example, the `shift` key will be held while `taylor` is entered into the element matching the given selector. After `taylor` is typed, `swift` will be typed without any modifier keys:

    $browser->keys('selector', ['{shift}', 'taylor'], 'swift');

Another valuable use case for the `keys` method is sending a "keyboard shortcut" combination to the primary CSS selector for your application:

    $browser->keys('.app', ['{command}', 'j']);

> {tip} All modifier keys such as `{command}` are wrapped in `{}` characters, and match the constants defined in the `Facebook\WebDriver\WebDriverKeys` class, which can be [found on GitHub](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="using-the-mouse"></a>
### Using The Mouse

<a name="clicking-on-elements"></a>
#### Clicking On Elements

The `click` method may be used to click on an element matching the given CSS or Dusk selector:

    $browser->click('.selector');

The `clickAtXPath` method may be used to click on an element matching the given XPath expression:

    $browser->clickAtXPath('//div[@class = "selector"]');

The `clickAtPoint` method may be used to click on the topmost element at a given pair of coordinates relative to the viewable area of the browser:

    $browser->clickAtPoint($x = 0, $y = 0);

The `doubleClick` method may be used to simulate the double click of a mouse:

    $browser->doubleClick();

The `rightClick` method may be used to simulate the right click of a mouse:

    $browser->rightClick();

    $browser->rightClick('.selector');

The `clickAndHold` method may be used to simulate a mouse button being clicked and held down. A subsequent call to the `releaseMouse` method will undo this behavior and release the mouse button:

    $browser->clickAndHold()
            ->pause(1000)
            ->releaseMouse();

<a name="mouseover"></a>
#### Mouseover

The `mouseover` method may be used when you need to move the mouse over an element matching the given CSS or Dusk selector:

    $browser->mouseover('.selector');

<a name="drag-drop"></a>
#### Drag & Drop

The `drag` method may be used to drag an element matching the given selector to another element:

    $browser->drag('.from-selector', '.to-selector');

Or, you may drag an element in a single direction:

    $browser->dragLeft('.selector', $pixels = 10);
    $browser->dragRight('.selector', $pixels = 10);
    $browser->dragUp('.selector', $pixels = 10);
    $browser->dragDown('.selector', $pixels = 10);

Finally, you may drag an element by a given offset:

    $browser->dragOffset('.selector', $x = 10, $y = 10);

<a name="javascript-dialogs"></a>
### JavaScript Dialogs

Dusk provides various methods to interact with JavaScript Dialogs. For example, you may use the `waitForDialog` method to wait for a JavaScript dialog to appear. This method accepts an optional argument indicating how many seconds to wait for the dialog to appear:

    $browser->waitForDialog($seconds = null);

The `assertDialogOpened` method may be used to assert that a dialog has been displayed and contains the given message:

    $browser->assertDialogOpened('Dialog message');

If the JavaScript dialog contains a prompt, you may use the `typeInDialog` method to type a value into the prompt:

    $browser->typeInDialog('Hello World');

To close an open JavaScript dialog by clicking the "OK" button, you may invoke the `acceptDialog` method:

    $browser->acceptDialog();

To close an open JavaScript dialog by clicking the "Cancel" button, you may invoke the `dismissDialog` method:

    $browser->dismissDialog();

<a name="scoping-selectors"></a>
### Scoping Selectors

Sometimes you may wish to perform several operations while scoping all of the operations within a given selector. For example, you may wish to assert that some text exists only within a table and then click a button within that table. You may use the `with` method to accomplish this. All operations performed within the closure given to the `with` method will be scoped to the original selector:

    $browser->with('.table', function ($table) {
        $table->assertSee('Hello World')
              ->clickLink('Delete');
    });

You may occasionally need to execute assertions outside of the current scope. You may use the `elsewhere` method to accomplish this:

     $browser->with('.table', function ($table) {
        // Current scope is `body .table`...

        $browser->elsewhere('.page-title', function ($title) {
            // Current scope is `body .page-title`...
            $title->assertSee('Hello World');
        });
     });

<a name="waiting-for-elements"></a>
### Waiting For Elements

When testing applications that use JavaScript extensively, it often becomes necessary to "wait" for certain elements or data to be available before proceeding with a test. Dusk makes this a cinch. Using a variety of methods, you may wait for elements to be visible on the page or even wait until a given JavaScript expression evaluates to `true`.

<a name="waiting"></a>
#### Waiting

If you just need to pause the test for a given number of milliseconds, use the `pause` method:

    $browser->pause(1000);

<a name="waiting-for-selectors"></a>
#### Waiting For Selectors

The `waitFor` method may be used to pause the execution of the test until the element matching the given CSS or Dusk selector is displayed on the page. By default, this will pause the test for a maximum of five seconds before throwing an exception. If necessary, you may pass a custom timeout threshold as the second argument to the method:

    // Wait a maximum of five seconds for the selector...
    $browser->waitFor('.selector');

    // Wait a maximum of one second for the selector...
    $browser->waitFor('.selector', 1);

You may also wait until the element matching the given selector contains the given text:

    // Wait a maximum of five seconds for the selector to contain the given text...
    $browser->waitForTextIn('.selector', 'Hello World');

    // Wait a maximum of one second for the selector to contain the given text...
    $browser->waitForTextIn('.selector', 'Hello World', 1);

You may also wait until the element matching the given selector is missing from the page:

    // Wait a maximum of five seconds until the selector is missing...
    $browser->waitUntilMissing('.selector');

    // Wait a maximum of one second until the selector is missing...
    $browser->waitUntilMissing('.selector', 1);

<a name="scoping-selectors-when-available"></a>
#### Scoping Selectors When Available

Occasionally, you may wish to wait for an element to appear that matches a given selector and then interact with the element. For example, you may wish to wait until a modal window is available and then press the "OK" button within the modal. The `whenAvailable` method may be used to accomplish this. All element operations performed within the given closure will be scoped to the original selector:

    $browser->whenAvailable('.modal', function ($modal) {
        $modal->assertSee('Hello World')
              ->press('OK');
    });

<a name="waiting-for-text"></a>
#### Waiting For Text

The `waitForText` method may be used to wait until the given text is displayed on the page:

    // Wait a maximum of five seconds for the text...
    $browser->waitForText('Hello World');

    // Wait a maximum of one second for the text...
    $browser->waitForText('Hello World', 1);

You may use the `waitUntilMissingText` method to wait until the displayed text has been removed from the page:

    // Wait a maximum of five seconds for the text to be removed...
    $browser->waitUntilMissingText('Hello World');

    // Wait a maximum of one second for the text to be removed...
    $browser->waitUntilMissingText('Hello World', 1);

<a name="waiting-for-links"></a>
#### Waiting For Links

The `waitForLink` method may be used to wait until the given link text is displayed on the page:

    // Wait a maximum of five seconds for the link...
    $browser->waitForLink('Create');

    // Wait a maximum of one second for the link...
    $browser->waitForLink('Create', 1);

<a name="waiting-on-the-page-location"></a>
#### Waiting On The Page Location

When making a path assertion such as `$browser->assertPathIs('/home')`, the assertion can fail if `window.location.pathname` is being updated asynchronously. You may use the `waitForLocation` method to wait for the location to be a given value:

    $browser->waitForLocation('/secret');

You may also wait for a [named route's](/docs/{{version}}/routing#named-routes) location:

    $browser->waitForRoute($routeName, $parameters);

<a name="waiting-for-page-reloads"></a>
#### Waiting for Page Reloads

If you need to make assertions after a page has been reloaded, use the `waitForReload` method:

    $browser->click('.some-action')
            ->waitForReload()
            ->assertSee('something');

<a name="waiting-on-javascript-expressions"></a>
#### Waiting On JavaScript Expressions

Sometimes you may wish to pause the execution of a test until a given JavaScript expression evaluates to `true`. You may easily accomplish this using the `waitUntil` method. When passing an expression to this method, you do not need to include the `return` keyword or an ending semi-colon:

    // Wait a maximum of five seconds for the expression to be true...
    $browser->waitUntil('App.data.servers.length > 0');

    // Wait a maximum of one second for the expression to be true...
    $browser->waitUntil('App.data.servers.length > 0', 1);

<a name="waiting-on-vue-expressions"></a>
#### Waiting On Vue Expressions

The `waitUntilVue` and `waitUntilVueIsNot` methods may be used to wait until a [Vue component](https://vuejs.org) attribute has a given value:

    // Wait until the component attribute contains the given value...
    $browser->waitUntilVue('user.name', 'Taylor', '@user');

    // Wait until the component attribute doesn't contain the given value...
    $browser->waitUntilVueIsNot('user.name', null, '@user');

<a name="waiting-with-a-callback"></a>
#### Waiting With A Callback

Many of the "wait" methods in Dusk rely on the underlying `waitUsing` method. You may use this method directly to wait for a given closure to return `true`. The `waitUsing` method accepts the maximum number of seconds to wait, the interval at which the closure should be evaluated, the closure, and an optional failure message:

    $browser->waitUsing(10, 1, function () use ($something) {
        return $something->isReady();
    }, "Something wasn't ready in time.");

<a name="scrolling-an-element-into-view"></a>
### Scrolling An Element Into View

Sometimes you may not be able to click on an element because it is outside of the viewable area of the browser. The `scrollIntoView` method will scroll the browser window until the element at the given selector is within the view:

    $browser->scrollIntoView('.selector')
            ->click('.selector');

<a name="available-assertions"></a>
## Available Assertions

Dusk provides a variety of assertions that you may make against your application. All of the available assertions are documented in the list below:

<style>
    .collection-method-list > p {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    .collection-method-list a {
        display: block;
    }
</style>

<div class="collection-method-list" markdown="1">
[assertTitle](#assert-title)
[assertTitleContains](#assert-title-contains)
[assertUrlIs](#assert-url-is)
[assertSchemeIs](#assert-scheme-is)
[assertSchemeIsNot](#assert-scheme-is-not)
[assertHostIs](#assert-host-is)
[assertHostIsNot](#assert-host-is-not)
[assertPortIs](#assert-port-is)
[assertPortIsNot](#assert-port-is-not)
[assertPathBeginsWith](#assert-path-begins-with)
[assertPathIs](#assert-path-is)
[assertPathIsNot](#assert-path-is-not)
[assertRouteIs](#assert-route-is)
[assertQueryStringHas](#assert-query-string-has)
[assertQueryStringMissing](#assert-query-string-missing)
[assertFragmentIs](#assert-fragment-is)
[assertFragmentBeginsWith](#assert-fragment-begins-with)
[assertFragmentIsNot](#assert-fragment-is-not)
[assertHasCookie](#assert-has-cookie)
[assertHasPlainCookie](#assert-has-plain-cookie)
[assertCookieMissing](#assert-cookie-missing)
[assertPlainCookieMissing](#assert-plain-cookie-missing)
[assertCookieValue](#assert-cookie-value)
[assertPlainCookieValue](#assert-plain-cookie-value)
[assertSee](#assert-see)
[assertDontSee](#assert-dont-see)
[assertSeeIn](#assert-see-in)
[assertDontSeeIn](#assert-dont-see-in)
[assertSeeAnythingIn](#assert-see-anything-in)
[assertSeeNothingIn](#assert-see-nothing-in)
[assertScript](#assert-script)
[assertSourceHas](#assert-source-has)
[assertSourceMissing](#assert-source-missing)
[assertSeeLink](#assert-see-link)
[assertDontSeeLink](#assert-dont-see-link)
[assertInputValue](#assert-input-value)
[assertInputValueIsNot](#assert-input-value-is-not)
[assertChecked](#assert-checked)
[assertNotChecked](#assert-not-checked)
[assertRadioSelected](#assert-radio-selected)
[assertRadioNotSelected](#assert-radio-not-selected)
[assertSelected](#assert-selected)
[assertNotSelected](#assert-not-selected)
[assertSelectHasOptions](#assert-select-has-options)
[assertSelectMissingOptions](#assert-select-missing-options)
[assertSelectHasOption](#assert-select-has-option)
[assertSelectMissingOption](#assert-select-missing-option)
[assertValue](#assert-value)
[assertAttribute](#assert-attribute)
[assertAriaAttribute](#assert-aria-attribute)
[assertDataAttribute](#assert-data-attribute)
[assertVisible](#assert-visible)
[assertPresent](#assert-present)
[assertMissing](#assert-missing)
[assertDialogOpened](#assert-dialog-opened)
[assertEnabled](#assert-enabled)
[assertDisabled](#assert-disabled)
[assertButtonEnabled](#assert-button-enabled)
[assertButtonDisabled](#assert-button-disabled)
[assertFocused](#assert-focused)
[assertNotFocused](#assert-not-focused)
[assertAuthenticated](#assert-authenticated)
[assertGuest](#assert-guest)
[assertAuthenticatedAs](#assert-authenticated-as)
[assertVue](#assert-vue)
[assertVueIsNot](#assert-vue-is-not)
[assertVueContains](#assert-vue-contains)
[assertVueDoesNotContain](#assert-vue-does-not-contain)
</div>

<a name="assert-title"></a>
#### assertTitle

Assert that the page title matches the given text:

    $browser->assertTitle($title);

<a name="assert-title-contains"></a>
#### assertTitleContains

Assert that the page title contains the given text:

    $browser->assertTitleContains($title);

<a name="assert-url-is"></a>
#### assertUrlIs

Assert that the current URL (without the query string) matches the given string:

    $browser->assertUrlIs($url);

<a name="assert-scheme-is"></a>
#### assertSchemeIs

Assert that the current URL scheme matches the given scheme:

    $browser->assertSchemeIs($scheme);

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

Assert that the current URL scheme does not match the given scheme:

    $browser->assertSchemeIsNot($scheme);

<a name="assert-host-is"></a>
#### assertHostIs

Assert that the current URL host matches the given host:

    $browser->assertHostIs($host);

<a name="assert-host-is-not"></a>
#### assertHostIsNot

Assert that the current URL host does not match the given host:

    $browser->assertHostIsNot($host);

<a name="assert-port-is"></a>
#### assertPortIs

Assert that the current URL port matches the given port:

    $browser->assertPortIs($port);

<a name="assert-port-is-not"></a>
#### assertPortIsNot

Assert that the current URL port does not match the given port:

    $browser->assertPortIsNot($port);

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

Assert that the current URL path begins with the given path:

    $browser->assertPathBeginsWith('/home');

<a name="assert-path-is"></a>
#### assertPathIs

Assert that the current path matches the given path:

    $browser->assertPathIs('/home');

<a name="assert-path-is-not"></a>
#### assertPathIsNot

Assert that the current path does not match the given path:

    $browser->assertPathIsNot('/home');

<a name="assert-route-is"></a>
#### assertRouteIs

Assert that the current URL matches the given [named route's](/docs/{{version}}/routing#named-routes) URL:

    $browser->assertRouteIs($name, $parameters);

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

Assert that the given query string parameter is present:

    $browser->assertQueryStringHas($name);

Assert that the given query string parameter is present and has a given value:

    $browser->assertQueryStringHas($name, $value);

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

Assert that the given query string parameter is missing:

    $browser->assertQueryStringMissing($name);

<a name="assert-fragment-is"></a>
#### assertFragmentIs

Assert that the URL's current hash fragment matches the given fragment:

    $browser->assertFragmentIs('anchor');

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

Assert that the URL's current hash fragment begins with the given fragment:

    $browser->assertFragmentBeginsWith('anchor');

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

Assert that the URL's current hash fragment does not match the given fragment:

    $browser->assertFragmentIsNot('anchor');

<a name="assert-has-cookie"></a>
#### assertHasCookie

Assert that the given encrypted cookie is present:

    $browser->assertHasCookie($name);

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

Assert that the given unencrypted cookie is present:

    $browser->assertHasPlainCookie($name);

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

Assert that the given encrypted cookie is not present:

    $browser->assertCookieMissing($name);

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

Assert that the given unencrypted cookie is not present:

    $browser->assertPlainCookieMissing($name);

<a name="assert-cookie-value"></a>
#### assertCookieValue

Assert that an encrypted cookie has a given value:

    $browser->assertCookieValue($name, $value);

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

Assert that an unencrypted cookie has a given value:

    $browser->assertPlainCookieValue($name, $value);

<a name="assert-see"></a>
#### assertSee

Assert that the given text is present on the page:

    $browser->assertSee($text);

<a name="assert-dont-see"></a>
#### assertDontSee

Assert that the given text is not present on the page:

    $browser->assertDontSee($text);

<a name="assert-see-in"></a>
#### assertSeeIn

Assert that the given text is present within the selector:

    $browser->assertSeeIn($selector, $text);

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

Assert that the given text is not present within the selector:

    $browser->assertDontSeeIn($selector, $text);

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

Assert that any text is present within the selector:

    $browser->assertSeeAnythingIn($selector);

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

Assert that no text is present within the selector:

    $browser->assertSeeNothingIn($selector);

<a name="assert-script"></a>
#### assertScript

Assert that the given JavaScript expression evaluates to the given value:

    $browser->assertScript('window.isLoaded')
            ->assertScript('document.readyState', 'complete');

<a name="assert-source-has"></a>
#### assertSourceHas

Assert that the given source code is present on the page:

    $browser->assertSourceHas($code);

<a name="assert-source-missing"></a>
#### assertSourceMissing

Assert that the given source code is not present on the page:

    $browser->assertSourceMissing($code);

<a name="assert-see-link"></a>
#### assertSeeLink

Assert that the given link is present on the page:

    $browser->assertSeeLink($linkText);

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

Assert that the given link is not present on the page:

    $browser->assertDontSeeLink($linkText);

<a name="assert-input-value"></a>
#### assertInputValue

Assert that the given input field has the given value:

    $browser->assertInputValue($field, $value);

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

Assert that the given input field does not have the given value:

    $browser->assertInputValueIsNot($field, $value);

<a name="assert-checked"></a>
#### assertChecked

Assert that the given checkbox is checked:

    $browser->assertChecked($field);

<a name="assert-not-checked"></a>
#### assertNotChecked

Assert that the given checkbox is not checked:

    $browser->assertNotChecked($field);

<a name="assert-radio-selected"></a>
#### assertRadioSelected

Assert that the given radio field is selected:

    $browser->assertRadioSelected($field, $value);

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

Assert that the given radio field is not selected:

    $browser->assertRadioNotSelected($field, $value);

<a name="assert-selected"></a>
#### assertSelected

Assert that the given dropdown has the given value selected:

    $browser->assertSelected($field, $value);

<a name="assert-not-selected"></a>
#### assertNotSelected

Assert that the given dropdown does not have the given value selected:

    $browser->assertNotSelected($field, $value);

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

Assert that the given array of values are available to be selected:

    $browser->assertSelectHasOptions($field, $values);

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

Assert that the given array of values are not available to be selected:

    $browser->assertSelectMissingOptions($field, $values);

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

Assert that the given value is available to be selected on the given field:

    $browser->assertSelectHasOption($field, $value);

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

Assert that the given value is not available to be selected:

    $browser->assertSelectMissingOption($field, $value);

<a name="assert-value"></a>
#### assertValue

Assert that the element matching the given selector has the given value:

    $browser->assertValue($selector, $value);

<a name="assert-attribute"></a>
#### assertAttribute

Assert that the element matching the given selector has the given value in the provided attribute:

    $browser->assertAttribute($selector, $attribute, $value);

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

Assert that the element matching the given selector has the given value in the provided aria attribute:

    $browser->assertAriaAttribute($selector, $attribute, $value);

For example, given the markup `<button aria-label="Add"></button>`, you may assert against the `aria-label` attribute like so:

    $browser->assertAriaAttribute('button', 'label', 'Add')

<a name="assert-data-attribute"></a>
#### assertDataAttribute

Assert that the element matching the given selector has the given value in the provided data attribute:

    $browser->assertDataAttribute($selector, $attribute, $value);

For example, given the markup `<tr id="row-1" data-content="attendees"></tr>`, you may assert against the `data-label` attribute like so:

    $browser->assertDataAttribute('#row-1', 'content', 'attendees')

<a name="assert-visible"></a>
#### assertVisible

Assert that the element matching the given selector is visible:

    $browser->assertVisible($selector);

<a name="assert-present"></a>
#### assertPresent

Assert that the element matching the given selector is present:

    $browser->assertPresent($selector);

<a name="assert-missing"></a>
#### assertMissing

Assert that the element matching the given selector is not visible:

    $browser->assertMissing($selector);

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

Assert that a JavaScript dialog with the given message has been opened:

    $browser->assertDialogOpened($message);

<a name="assert-enabled"></a>
#### assertEnabled

Assert that the given field is enabled:

    $browser->assertEnabled($field);

<a name="assert-disabled"></a>
#### assertDisabled

Assert that the given field is disabled:

    $browser->assertDisabled($field);

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

Assert that the given button is enabled:

    $browser->assertButtonEnabled($button);

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

Assert that the given button is disabled:

    $browser->assertButtonDisabled($button);

<a name="assert-focused"></a>
#### assertFocused

Assert that the given field is focused:

    $browser->assertFocused($field);

<a name="assert-not-focused"></a>
#### assertNotFocused

Assert that the given field is not focused:

    $browser->assertNotFocused($field);

<a name="assert-authenticated"></a>
#### assertAuthenticated

Assert that the user is authenticated:

    $browser->assertAuthenticated();

<a name="assert-guest"></a>
#### assertGuest

Assert that the user is not authenticated:

    $browser->assertGuest();

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

Assert that the user is authenticated as the given user:

    $browser->assertAuthenticatedAs($user);

<a name="assert-vue"></a>
#### assertVue

Dusk even allows you to make assertions on the state of [Vue component](https://vuejs.org) data. For example, imagine your application contains the following Vue component:

    // HTML...

    <profile dusk="profile-component"></profile>

    // Component Definition...

    Vue.component('profile', {
        template: '<div>{{ user.name }}</div>',

        data: function () {
            return {
                user: {
                    name: 'Taylor'
                }
            };
        }
    });

You may assert on the state of the Vue component like so:

    /**
     * A basic Vue test example.
     *
     * @return void
     */
    public function testVue()
    {
        $this->browse(function (Browser $browser) {
            $browser->visit('/')
                    ->assertVue('user.name', 'Taylor', '@profile-component');
        });
    }

<a name="assert-vue-is-not"></a>
#### assertVueIsNot

Assert that a given Vue component data property does not match the given value:

    $browser->assertVueIsNot($property, $value, $componentSelector = null);

<a name="assert-vue-contains"></a>
#### assertVueContains

Assert that a given Vue component data property is an array and contains the given value:

    $browser->assertVueContains($property, $value, $componentSelector = null);

<a name="assert-vue-does-not-contain"></a>
#### assertVueDoesNotContain

Assert that a given Vue component data property is an array and does not contain the given value:

    $browser->assertVueDoesNotContain($property, $value, $componentSelector = null);

<a name="pages"></a>
## Pages

Sometimes, tests require several complicated actions to be performed in sequence. This can make your tests harder to read and understand. Dusk Pages allow you to define expressive actions that may then be performed on a given page via a single method. Pages also allow you to define short-cuts to common selectors for your application or for a single page.

<a name="generating-pages"></a>
### Generating Pages

To generate a page object, execute the `dusk:page` Artisan command. All page objects will be placed in your application's `tests/Browser/Pages` directory:

    php artisan dusk:page Login

<a name="configuring-pages"></a>
### Configuring Pages

By default, pages have three methods: `url`, `assert`, and `elements`. We will discuss the `url` and `assert` methods now. The `elements` method will be [discussed in more detail below](#shorthand-selectors).

<a name="the-url-method"></a>
#### The `url` Method

The `url` method should return the path of the URL that represents the page. Dusk will use this URL when navigating to the page in the browser:

    /**
     * Get the URL for the page.
     *
     * @return string
     */
    public function url()
    {
        return '/login';
    }

<a name="the-assert-method"></a>
#### The `assert` Method

The `assert` method may make any assertions necessary to verify that the browser is actually on the given page. It is not actually necessary to place anything within this method; however, you are free to make these assertions if you wish. These assertions will be run automatically when navigating to the page:

    /**
     * Assert that the browser is on the page.
     *
     * @return void
     */
    public function assert(Browser $browser)
    {
        $browser->assertPathIs($this->url());
    }

<a name="navigating-to-pages"></a>
### Navigating To Pages

Once a page has been defined, you may navigate to it using the `visit` method:

    use Tests\Browser\Pages\Login;

    $browser->visit(new Login);

Sometimes you may already be on a given page and need to "load" the page's selectors and methods into the current test context. This is common when pressing a button and being redirected to a given page without explicitly navigating to it. In this situation, you may use the `on` method to load the page:

    use Tests\Browser\Pages\CreatePlaylist;

    $browser->visit('/dashboard')
            ->clickLink('Create Playlist')
            ->on(new CreatePlaylist)
            ->assertSee('@create');

<a name="shorthand-selectors"></a>
### Shorthand Selectors

The `elements` method within page classes allow you to define quick, easy-to-remember shortcuts for any CSS selector on your page. For example, let's define a shortcut for the "email" input field of the application's login page:

    /**
     * Get the element shortcuts for the page.
     *
     * @return array
     */
    public function elements()
    {
        return [
            '@email' => 'input[name=email]',
        ];
    }

Once the shortcut has been defined, you may use the shorthand selector anywhere you would typically use a full CSS selector:

    $browser->type('@email', 'taylor@laravel.com');

<a name="global-shorthand-selectors"></a>
#### Global Shorthand Selectors

After installing Dusk, a base `Page` class will be placed in your `tests/Browser/Pages` directory. This class contains a `siteElements` method which may be used to define global shorthand selectors that should be available on every page throughout your application:

    /**
     * Get the global element shortcuts for the site.
     *
     * @return array
     */
    public static function siteElements()
    {
        return [
            '@element' => '#selector',
        ];
    }

<a name="page-methods"></a>
### Page Methods

In addition to the default methods defined on pages, you may define additional methods which may be used throughout your tests. For example, let's imagine we are building a music management application. A common action for one page of the application might be to create a playlist. Instead of re-writing the logic to create a playlist in each test, you may define a `createPlaylist` method on a page class:

    <?php

    namespace Tests\Browser\Pages;

    use Laravel\Dusk\Browser;

    class Dashboard extends Page
    {
        // Other page methods...

        /**
         * Create a new playlist.
         *
         * @param  \Laravel\Dusk\Browser  $browser
         * @param  string  $name
         * @return void
         */
        public function createPlaylist(Browser $browser, $name)
        {
            $browser->type('name', $name)
                    ->check('share')
                    ->press('Create Playlist');
        }
    }

Once the method has been defined, you may use it within any test that utilizes the page. The browser instance will automatically be passed as the first argument to custom page methods:

    use Tests\Browser\Pages\Dashboard;

    $browser->visit(new Dashboard)
            ->createPlaylist('My Playlist')
            ->assertSee('My Playlist');

<a name="components"></a>
## Components

Components are similar to Dusk’s “page objects”, but are intended for pieces of UI and functionality that are re-used throughout your application, such as a navigation bar or notification window. As such, components are not bound to specific URLs.

<a name="generating-components"></a>
### Generating Components

To generate a component, execute the `dusk:component` Artisan command. New components are placed in the `tests/Browser/Components` directory:

    php artisan dusk:component DatePicker

As shown above, a "date picker" is an example of a component that might exist throughout your application on a variety of pages. It can become cumbersome to manually write the browser automation logic to select a date in dozens of tests throughout your test suite. Instead, we can define a Dusk component to represent the date picker, allowing us to encapsulate that logic within the component:

    <?php

    namespace Tests\Browser\Components;

    use Laravel\Dusk\Browser;
    use Laravel\Dusk\Component as BaseComponent;

    class DatePicker extends BaseComponent
    {
        /**
         * Get the root selector for the component.
         *
         * @return string
         */
        public function selector()
        {
            return '.date-picker';
        }

        /**
         * Assert that the browser page contains the component.
         *
         * @param  Browser  $browser
         * @return void
         */
        public function assert(Browser $browser)
        {
            $browser->assertVisible($this->selector());
        }

        /**
         * Get the element shortcuts for the component.
         *
         * @return array
         */
        public function elements()
        {
            return [
                '@date-field' => 'input.datepicker-input',
                '@year-list' => 'div > div.datepicker-years',
                '@month-list' => 'div > div.datepicker-months',
                '@day-list' => 'div > div.datepicker-days',
            ];
        }

        /**
         * Select the given date.
         *
         * @param  \Laravel\Dusk\Browser  $browser
         * @param  int  $year
         * @param  int  $month
         * @param  int  $day
         * @return void
         */
        public function selectDate(Browser $browser, $year, $month, $day)
        {
            $browser->click('@date-field')
                    ->within('@year-list', function ($browser) use ($year) {
                        $browser->click($year);
                    })
                    ->within('@month-list', function ($browser) use ($month) {
                        $browser->click($month);
                    })
                    ->within('@day-list', function ($browser) use ($day) {
                        $browser->click($day);
                    });
        }
    }

<a name="using-components"></a>
### Using Components

Once the component has been defined, we can easily select a date within the date picker from any test. And, if the logic necessary to select a date changes, we only need to update the component:

    <?php

    namespace Tests\Browser;

    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Laravel\Dusk\Browser;
    use Tests\Browser\Components\DatePicker;
    use Tests\DuskTestCase;

    class ExampleTest extends DuskTestCase
    {
        /**
         * A basic component test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->browse(function (Browser $browser) {
                $browser->visit('/')
                        ->within(new DatePicker, function ($browser) {
                            $browser->selectDate(2019, 1, 30);
                        })
                        ->assertSee('January');
            });
        }
    }

<a name="continuous-integration"></a>
## Continuous Integration

> {note} Most Dusk continuous integration configurations expect your Laravel application to be served using the built-in PHP development server on port 8000. Therefore, before continuing, you should ensure that your continous integration environment has an `APP_URL` environment variable value of `http://127.0.0.1:8000`.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

To run Dusk tests on [Heroku CI](https://www.heroku.com/continuous-integration), add the following Google Chrome buildpack and scripts to your Heroku `app.json` file:

    {
      "environments": {
        "test": {
          "buildpacks": [
            { "url": "heroku/php" },
            { "url": "https://github.com/heroku/heroku-buildpack-google-chrome" }
          ],
          "scripts": {
            "test-setup": "cp .env.testing .env",
            "test": "nohup bash -c './vendor/laravel/dusk/bin/chromedriver-linux > /dev/null 2>&1 &' && nohup bash -c 'php artisan serve > /dev/null 2>&1 &' && php artisan dusk"
          }
        }
      }
    }

<a name="running-tests-on-travis-ci"></a>
### Travis CI

To run your Dusk tests on [Travis CI](https://travis-ci.org), use the following `.travis.yml` configuration. Since Travis CI is not a graphical environment, we will need to take some extra steps in order to launch a Chrome browser. In addition, we will use `php artisan serve` to launch PHP's built-in web server:

    language: php

    php:
      - 7.3

    addons:
      chrome: stable

    install:
      - cp .env.testing .env
      - travis_retry composer install --no-interaction --prefer-dist --no-suggest
      - php artisan key:generate
      - php artisan dusk:chrome-driver

    before_script:
      - google-chrome-stable --headless --disable-gpu --remote-debugging-port=9222 http://localhost &
      - php artisan serve &

    script:
      - php artisan dusk

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

If you are using [Github Actions](https://github.com/features/actions) to run your Dusk tests, you may use the following configuration file as a starting point. Like TravisCI, we will use the `php artisan serve` command to launch PHP's built-in web server:

    name: CI
    on: [push]
    jobs:

      dusk-php:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - name: Prepare The Environment
            run: cp .env.example .env
          - name: Create Database
            run: |
              sudo systemctl start mysql
              mysql --user="root" --password="root" -e "CREATE DATABASE 'my-database' character set UTF8mb4 collate utf8mb4_bin;"
          - name: Install Composer Dependencies
            run: composer install --no-progress --no-suggest --prefer-dist --optimize-autoloader
          - name: Generate Application Key
            run: php artisan key:generate
          - name: Upgrade Chrome Driver
            run: php artisan dusk:chrome-driver `/opt/google/chrome/chrome --version | cut -d " " -f3 | cut -d "." -f1`
          - name: Start Chrome Driver
            run: ./vendor/laravel/dusk/bin/chromedriver-linux &
          - name: Run Laravel Server
            run: php artisan serve &
          - name: Run Dusk Tests
            env:
              APP_URL: "http://127.0.0.1:8000"
            run: php artisan dusk
          - name: Upload Screenshots
            if: failure()
            uses: actions/upload-artifact@v2
            with:
              name: screenshots
              path: tests/Browser/screenshots
          - name: Upload Console Logs
            if: failure()
            uses: actions/upload-artifact@v2
            with:
              name: console
              path: tests/Browser/console
