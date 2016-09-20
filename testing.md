# Testing

- [Introduction](#introduction)
- [Environment](#environment)
- [Creating & Running Tests](#creating-and-running-tests)

<a name="introduction"></a>
## Introduction

Laravel is built with testing in mind. In fact, support for testing with PHPUnit is included out of the box and a `phpunit.xml` file is already setup for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications.

An `ExampleTest.php` file is provided in the `tests` directory. After installing a new Laravel application, simply run `phpunit` on the command line to run your tests.

<a name="environment"></a>
## Environment

When running tests, Laravel will automatically set the configuration environment to `testing`. Laravel automatically configures the session and cache to the `array` driver while testing, meaning no session or cache data will be persisted while testing.

You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in the `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests!

<a name="creating-and-running-tests"></a>
## Creating & Running Tests

To create a new test case, use the `make:test` Artisan command:

    php artisan make:test UserTest

This command will place a new `UserTest` class within your `tests` directory. You may then define test methods as you normally would using PHPUnit. To run your tests, simply execute the `phpunit` command from your terminal:

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class UserTest extends TestCase
    {
        /**
         * A basic test example.
         *
         * @return void
         */
        public function testExample()
        {
            $this->assertTrue(true);
        }
    }

> {note} If you define your own `setUp` method within a test class, be sure to call `parent::setUp`.
