# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 5.8](#laravel-5.8)

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
| 5.8 | February 26th, 2019 | August 26th, 2019 | February 26th, 2020 |

<a name="laravel-5.8"></a>
## Laravel 5.8

Laravel 5.8 continues the improvements made in Laravel 5.7 by introducing has-one-through Eloquent relationships, improved email validation, convention based automatic registration of authorization policies, DynamoDB cache and session drivers, improved scheduler timezone configuration, support for assigning multiple authentication guards to broadcast channels, PSR-16 cache driver compliance, improvements to the `artisan serve` command, PHPUnit 8.0 support, Carbon 2.0 support, Pheanstalk 4.0 support, and a variety of other bug fixes and usability improvements.

### Eloquent `HasOneThrough` Relationship

Eloquent now provides support for the `hasOneThrough` relationship type. For example, imagine a Supplier model `hasOne` Account model, and an Account model has one AccountHistory model. You may use a `hasOneThrough` relationship to access a supplier's account history through the account model:

    /**
     * Get the account history for the supplier.
     */
    public function accountHistory()
    {
        return $this->hasOneThrough(AccountHistory::class, Account::class);
    }

### Multiple Broadcast Authentication Guards

In previous releases of Laravel, private and presence broadcast channels authenticated the user via your application's default authentication guard. Beginning in Laravel 5.8, you may now assign multiple guards that should authenticate the incoming request:

    Broadcast::channel('channel', function() {
        // ...
    }, ['guards' => ['web', 'admin']])

### Mock / Spy Testing Helper Methods

In order to make mocking objects more convenient, new `mock` and `spy` methods have been added to the base Laravel test case class. These methods automatically bind the mocked class into the container. For example:

    // Laravel 5.7
    $this->instance(Service::class, Mockery::mock(Service::class, function ($mock) {
        $mock->shouldReceive('process')->once();
    }));

    // Laravel 5.8
    $this->mock(Service::class, function ($mock) {
        $mock->shouldReceive('process')->once();
    });

### Improved Email Validation

Laravel 5.8 introduces improvements to the validator's underlying email validation logic by adopting the `egulias/email-validator` package utilized by SwiftMailer. Laravel's previous email validation logic occasionally considered valid emails, such as `example@bär.se`, to be invalid.

### Default Scheduler Timezone

Laravel allows you to customize the timezone of a scheduled task using the `timezone` method:

    $schedule->command('inspire')
             ->hourly()
             ->timezone('America/Chicago');

However, this can become cumbersome and repetitive if you are specifying the same timezone for all of your scheduled tasks. For that reason, you may now define a `scheduleTimezone` method in your `app/Console/Kernel.php` file. This method should return the default timezone that should be assigned to all scheduled tasks:

    /**
     * Get the timezone that should be used by default for scheduled events.
     *
     * @return \DateTimeZone|string|null
     */
    protected function scheduleTimezone()
    {
        return 'America/Chicago';
    }

### Blade File Mapping

When compiling Blade templates, Laravel now adds a comment to the top of the compiled file which contains the path to the original Blade template.

### DynamoDB Cache / Session Drivers

Laravel 5.8 introduces [DynamoDB](https://aws.amazon.com/dynamodb/) cache and session drivers. DynamoDB is a serverless NoSQL database provided by Amazon Web Services. The default configuration for the `dynamodb` cache driver can be found in the Laravel 5.8 [cache configuration file](https://github.com/laravel/laravel/blob/master/config/cache.php).

### Carbon 2.0 Support

Laravel 5.8 provides support for the `~2.0` release of the Carbon date manipulation library.

### Pheanstalk 4.0 Support

Laravel 5.8 provides support for the `~4.0` release of the Pheanstalk queue library. If you are using Pheanstalk library in your application, please upgrade your library to the `~4.0` release via Composer.
