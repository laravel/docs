# Browser Tests (Laravel Dusk)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Using Other Browsers](#using-other-browsers)
- [Writing Tests](#writing-tests)
    - [Generating Tests](#generating-tests)
    - [Your First Test](#your-first-test)
- [Interacting With Your Application](#interacting-with-elements)
    - [Authentication](#authentication)
    - [Waiting For Elements](#waiting-for-elements)
    - [Making Assertions](#available-assertions)
- [Multi-Browser Tests](#multi-browser-tests)
- [Page Objects](#page-objects)
    - [Generating Page Objects](#generating-page-objects)
    - [Using Page Objects](#using-page-objects)
    - [Shorthand Selectors](#shorthand-selectors)
    - [Page Methods](#page-methods)
- [Running Tests](#running-tests)
    - [Environment Handling](#environment-handling)

<a name="introduction"></a>
## Introduction

Laravel Dusk provides an expressive, easy-to-use browser automation and testing API. By default, Dusk does not require you to install JDK or Selenium on your machine. Instead, Dusk uses a standalone [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home) installation. However, you are free to utilize any other Selenium compatible driver you wish.

<a name="installation"></a>
## Installation

To get started, you should add the `laravel/dusk` Composer dependency to your project:

    composer require laravel/dusk

Once Dusk is installed, you should register the `Laravel\Dusk\DuskServiceProvider` service provider. You should register the provider within the `register` method of your `AppServiceProvider` in order to limit the environments in which Dusk is available, since it exposes the ability to login as other users:

    use Laravel\Dusk\DuskServiceProvider;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        if ($this->app->environment('local', 'testing')) {
            $this->app->register(DuskServiceProvider::class);
        }
    }

Next, run the `dusk:install` Artisan command:

    php artisan dusk:install

A `Browser` directory will be created within your `tests` directory and will contain an example test. Next, set the `APP_URL` environment variable in your `.env` file. This value should match the URL you use to access your application in a browser.

To run your tests, use the `dusk` Artisan command. The `dusk` command accepts any argument that is also accepted by the `phpunit` command:

    php artisan dusk

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

Next, you may simply modify the `driver` method to connect to the URL and port of your choice. In addition, you may modify the "desired capabilities" that should be passed to the WebDriver:

    /**
     * Create the RemoteWebDriver instance.
     *
     * @return \Facebook\WebDriver\Remote\RemoteWebDriver
     */
    protected function driver()
    {
        return RemoteWebDriver::create(
            'http://localhost:4444', DesiredCapabilities::phantomjs()
        );
    }
