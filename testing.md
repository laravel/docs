# Testing: Getting Started

- [Introduction](#introduction)
- [Environment](#environment)
- [Creating Tests](#creating-tests)
- [Running Tests](#running-tests)
    - [Running Tests In Parallel](#running-tests-in-parallel)

<a name="introduction"></a>
## Introduction

Laravel is built with testing in mind. In fact, support for testing with PHPUnit is included out of the box and a `phpunit.xml` file is already set up for your application. The framework also ships with convenient helper methods that allow you to expressively test your applications.

By default, your application's `tests` directory contains two directories: `Feature` and `Unit`. Unit tests are tests that focus on a very small, isolated portion of your code. In fact, most unit tests probably focus on a single method. Feature tests may test a larger portion of your code, including how several objects interact with each other or even a full HTTP request to a JSON endpoint.

An `ExampleTest.php` file is provided in both the `Feature` and `Unit` test directories. After installing a new Laravel application, run `vendor/bin/phpunit` on the command line to run your tests.

<a name="environment"></a>
## Environment

When running tests, Laravel will automatically set the configuration environment to `testing` because of the environment variables defined in the `phpunit.xml` file. Laravel also automatically configures the session and cache to the `array` driver while testing, meaning no session or cache data will be persisted while testing.

You are free to define other testing environment configuration values as necessary. The `testing` environment variables may be configured in the `phpunit.xml` file, but make sure to clear your configuration cache using the `config:clear` Artisan command before running your tests!

In addition, you may create a `.env.testing` file in the root of your project. This file will override the `.env` file when running PHPUnit tests or executing Artisan commands with the `--env=testing` option.

<a name="creating-tests"></a>
## Creating Tests

To create a new test case, use the `make:test` Artisan command:

    // Create a test in the Feature directory...
    php artisan make:test UserTest

    // Create a test in the Unit directory...
    php artisan make:test UserTest --unit

> {tip} Test stubs may be customized using [stub publishing](/docs/{{version}}/artisan#stub-customization)

Once the test has been generated, you may define test methods as you normally would using PHPUnit. To run your tests, execute the `phpunit` or `artisan test` command from your terminal:

    <?php

    namespace Tests\Unit;

    use PHPUnit\Framework\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * A basic test example.
         *
         * @return void
         */
        public function testBasicTest()
        {
            $this->assertTrue(true);
        }
    }

> {note} If you define your own `setUp` / `tearDown` methods within a test class, be sure to call the respective `parent::setUp()` / `parent::tearDown()` methods on the parent class.

<a name="running-tests"></a>
## Running Tests

As mentioned previously, once you've written tests, you may run them using `phpunit`:

    ./vendor/bin/phpunit

In addition to the `phpunit` command, you may use the `test` Artisan command to run your tests. The Artisan test runner provides verbose test reports in order to ease development and debugging:

    php artisan test

Any arguments that can be passed to the `phpunit` command may also be passed to the Artisan `test` command:

    php artisan test --testsuite=Feature --stop-on-failure


<a name="running-tests-in-parallel"></a>
### Running Tests In Parallel

The `test` Artisan command also provides the `--parallel` option that you may use to speed up your tests by running tests in parallel:

    php artisan test --parallel

By default, the number of processes is equal to the number of available cores on the machine. You may adjust the number of processes by using the `--processes` option:

    php artisan test --parallel --processes=4

When using database traits in your tests, Laravel automatically handles creating and migrating a test database for each process. The test databases will be suffixed with the process token, which is unique per process. For example, if you have 2 processes, Laravel will create and use the `your_db_test_1` and `your_db_test_2` test databases.

By default, the test databases persist between `test` runs, but you may re-create them using the `--refresh-databases` option:

    php artisan test --parallel --refresh-databases

While Laravel works out of the box with parallel testing, you may need to prepare certain resources in your application so they can be used in parallel.

Using the `ParallelTesting` facade you may specify code to be executed on the `setUp` and `tearDown` of a process or a test case. The given closures receive the `$token` and `$testCase` variables that contain the process token and the current test case, respectively.

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\ParallelTesting;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            ParallelTesting::setUpProcess(function ($token) {
                // ..
            });

            ParallelTesting::setUpTestCase(function ($token, $testCase) {
                // ..
            });

            ParallelTesting::tearDownTestCase(function ($token, $testCase) {
                // ..
            });

            ParallelTesting::tearDownProcess(function ($token) {
                // ..
            });
        }
    }

If you would like to access to current process token from any other place in your code, you may use the `token` method.

    $token = ParallelTesting::token();
