# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 5.7](#laravel-5.7)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel's versioning scheme maintains the following convention: `paradigm.major.minor`. Major framework releases are released every six months (February and August), while minor releases may be released as often as every week. Minor releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `5.7.*`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less.

Paradigm shifting releases are separated by many years and represent fundamental shifts in the framework's architecture and conventions. Currently, there is no paradigm shifting release under development.

<a name="support-policy"></a>
## Support Policy

For LTS releases, such as Laravel 5.5, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide the longest window of support and maintenance. For general releases, bug fixes are provided for 6 months and security fixes are provided for 1 year.

| Version | Release | Bug Fixes Until | Security Fixes Until |
| --- | --- | --- | --- |
| 5.0 | February 4th, 2015 | August 4th, 2015 | February 4th, 2016 |
| 5.1 (LTS) | June 9th, 2015 | June 9th, 2017 | June 9th, 2018 |
| 5.2 | December 21st, 2015 | June 21st, 2016 | December 21st, 2016 |
| 5.3 | August 23rd, 2016 | February 23rd, 2017 | August 23rd, 2017 |
| 5.4 | January 24th, 2017 | July 24th, 2017 | January 24th, 2018 |
| 5.5 (LTS) | August 30th, 2017 | August 30th, 2019 | August 30th, 2020 |
| 5.6 | February 7th, 2018 | August 7th, 2018 | February 7th, 2019 |
| 5.7 | September 4th, 2018 | March 4th, 2019 | September 4th, 2019 |

<a name="laravel-5.7"></a>
## Laravel 5.7

Laravel 5.7 continues the improvements made in Laravel 5.6 by introducing [Laravel Nova](https://nova.laravel.com), optional email verification to the authentication scaffolding, support for guest users in authorization gates and policies, console testing improvements, Symfony `dump-server` integration, localizable notifications, and a variety of other bug fixes and usability improvements.

### Laravel Nova

[Laravel Nova](https://nova.laravel.com) is a beautiful, best-in-class administration dashboard for Laravel applications. Of course, the primary feature of Nova is the ability to administer your underlying database records using Eloquent. Additionally, Nova offers support for filters, lenses, actions, queued actions, metrics, authorization, custom tools, custom cards, custom fields, and more.

To learn more about Laravel Nova, check out the [Nova website](https://nova.laravel.com).

### Email Verification

Laravel 5.7 introduces optional email verification to the authentication scaffolding included with the framework. To accommodate this feature, an `email_verified_at` timestamp column has been added to the default `users` table migration that is included with the framework.

To prompt newly registered users to verify their email, the `User` model should be marked with the `MustVerifyEmail` interface:

    <?php

    namespace App;

    use Illuminate\Notifications\Notifiable;
    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        // ...
    }

Once the `User` model is marked with the `MustVerifyEmail` interface, newly registered users will receive an email containing a signed verification link. Once this link has been clicked, Laravel will automatically record the verification time in the database and redirect users to a location of your choosing.

A `verified` middleware has been added to the default application's HTTP kernel. This middleware may be attached to routes that should only allow verified users:

    'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,

> {tip} To learn more about email verification, check out the [complete documentation](/docs/{{version}}/verification).

### Guest User Gates / Policies

In previous versions of Laravel, authorization gates and policies automatically returned `false` for unauthenticated visitors to your application. However, you may now allow guests to pass through authorization checks by declaring an "optional" type-hint or supplying a `null` default value for the user argument definition:

    Gate::define('update-post', function (?User $user, Post $post) {
        // ...
    });

### Symfony Dump Server

Laravel 5.7 offers integration with Symfony's `dump-server` command via [a package by Marcel Pociot](https://github.com/beyondcode/laravel-dump-server). To get started, run the `dump-server` Artisan command:

    php artisan dump-server

Once the server has started, all calls to `dump` will be displayed in the `dump-server` console window instead of in your browser, allowing you to inspect the values without mangling your HTTP response output.

### Notification Localization

Laravel now allows you to send notifications in a locale other than the current language, and will even remember this locale if the notification is queued.

To accomplish this, the `Illuminate\Notifications\Notification` class now offers a `locale` method to set the desired language. The application will change into this locale when the notification is being formatted and then revert back to the previous locale when formatting is complete:

    $user->notify((new InvoicePaid($invoice))->locale('es'));

Localization of multiple notifiable entries may also be achieved via the `Notification` facade:

    Notification::locale('es')->send($users, new InvoicePaid($invoice));

### Console Testing

Laravel 5.7 allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command:

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you program in?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you program in '.$language.'.');
    });

You may test this command with the following test which utilizes the `expectsQuestion`, `expectsOutput`, and `assertExitCode` methods:

    /**
     * Test a console command.
     *
     * @return void
     */
    public function test_console_command()
    {
        $this->artisan('question')
             ->expectsQuestion('What is your name?', 'Taylor Otwell')
             ->expectsQuestion('Which language do you program in?', 'PHP')
             ->expectsOutput('Your name is Taylor Otwell and you program in PHP.')
             ->assertExitCode(0);
    }

### URL Generator & Callable Syntax

Instead of only accepting strings, Laravel's URL generator now accepts "callable" syntax when generating URLs to controller actions:

    action([UserController::class, 'index']);

### Paginator Links

Laravel 5.7 allows you to control how many additional links are displayed on each side of the paginator's URL "window". By default, three links are displayed on each side of the primary paginator links. However, you may control this number using the `onEachSide` method:

    {{ $paginator->onEachSide(5)->links() }}

### Filesystem Read / Write Streams

Laravel's Flysystem integration now offers `readStream` and `writeStream` methods:

    Storage::disk('s3')->writeStream(
        'remote-file.zip',
        Storage::disk('local')->readStream('local-file.zip')
    );
