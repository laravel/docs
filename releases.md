# Release Notes

- [Versioning Scheme](#versioning-scheme)
    - [Exceptions](#exceptions)
- [Support Policy](#support-policy)
- [Laravel 9](#laravel-9)

<a name="versioning-scheme"></a>
## Versioning Scheme

Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~January), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes.

When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^9.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less.

<a name="support-policy"></a>
## Support Policy

For LTS releases, such as Laravel 9, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide the longest window of support and maintenance. For general releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/{{version}}/database#introduction).

| Version | PHP (*) | Release | Bug Fixes Until | Security Fixes Until |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2 - 8.0 | September 3rd, 2019 | January 25th, 2022 | September 6th, 2022 |
| 7 | 7.2 - 8.0 | March 3rd, 2020 | October 6th, 2020 | March 3rd, 2021 |
| 8 | 7.3 - 8.1 | September 8th, 2020 | July 26th, 2022 | January 24th, 2023 |
| 9 (LTS) | 8.0 - 8.1 | January 25th, 2022 | January 30th, 2024 | January 28th, 2025 |
| 10 | 8.0 - 8.1 | January 24th, 2023 | July 30th, 2024 | January 28th, 2025 |

<div class="sm:flex dark:text-gray-400 mb-1">
    <div class="flex items-center mr-4">
        <div class="w-3 h-3 mr-2 bg-red-500"></div>
        <div>End of life</div>
    </div>
    <div class="flex items-center">
        <div class="w-3 h-3 mr-2 bg-orange-600"></div>
        <div>Security fixes only</div>
    </div>
</div>

(*) Supported PHP versions

<a name="laravel-9"></a>
## Laravel 9

As you may know, Laravel transitioned to yearly releases with the release of Laravel 8. Previously, major versions were released every 6 months. This transition is intended to ease the maintenance burden on the community and challenge our development team to ship amazing, powerful new features without introducing breaking changes. Therefore, we have shipped a variety of robust features to Laravel 8 without breaking backwards compatibility, such as parallel testing support, improved Breeze starter kits, HTTP client improvements, and even new Eloquent relationship types such as "has one of many".

Therefore, this commitment to ship great new features during the current release will likely lead to future "major" releases being primarily used for "maintenance" tasks such as upgrading upstream dependencies, which can be seen in these release notes.

Laravel 9 continues the improvements made in Laravel 8.x by introducing support for Symfony 6.0 components, Symfony Mailer, Flysystem 2.0, improved `route:list` output, a Laravel Scout database driver, new Eloquent accessor / mutator syntax, implicit route bindings via Enums, and a variety of other bug fixes and usability improvements.

<a name="php-8"></a>
### PHP 8.0

Laravel 9.x requires a minimum PHP version of 8.0.

<a name="laravel-jetstream"></a>
### Symfony Mailer

_Symfony Mailer support was contributed by [Dries Vints](https://github.com/driesvints)_, [James Brooks](https://github.com/jbrooksuk), and [Julius Kiekbusch](https://github.com/Jubeki).

Previous releases of Laravel utilized the [Swift Mailer](https://swiftmailer.symfony.com/docs/introduction.html) library to send outgoing email. However, that library is no longer maintained and has been succeeded by Symfony Mailer.

Please review the [upgrade guide](/docs/{{version}}/upgrade#symfony-mailer) to learn more about ensuring your application is compatible with Symfony Mailer.

<a name="flysystem-2"></a>
### Flysystem 2.0

_Flysystem 2.0 support was contributed by [Dries Vints](https://github.com/driesvints)_.

Laravel 9.x upgrades our upstream Flysystem dependency to Flysystem 2.x. Flysystem powers all of filesystem interactions offered by the `Storage` facade.

Please review the [upgrade guide](/docs/{{version}}/upgrade#flysystem-2) to learn more about ensuring your application is compatible with Flysystem 2.0.

<a name="eloquent-accessors-and-mutators"></a>
### Improved Eloquent Accessors / Mutators

_Improved Eloquent accessors / mutators was contributed by [Taylor Otwell](https://github.com/taylorotwell)_.

Laravel 9.x offers a new way to define Eloquent [accessors and mutators](/docs/{{version}}/eloquent-mutators#accessors-and-mutators). In previous releases of Laravel, the only way to define accessors and mutators was by defining prefixed methods on your model like so:

```php
public function getNameAttribute($value)
{
    return strtoupper($value);
}

public function setNameAttribute($value)
{
    $this->attributes['name'] = $value;
}
```

However, in Laravel 9.x you may define an accessor and mutator using a single, non-prefixed method by type-hinting a return type of `Illuminate\Database\Eloquent\Casts\Attribute`:

```php
use Illuminate\Database\Eloquent\Casts\Attribute;

public function name(): Attribute
{
    return new Attribute(
        get: fn ($value) => strtoupper($value),
        set: fn ($value) => $value,
    );
}
```

In addition, this new approach to defining accessors will cache object values that are returned by the attribute, just like [custom cast classes](/docs/{{version}}/eloquent-mutators#custom-casts):

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

public function address(): Attribute
{
    return new Attribute(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```

<a name="implicit-route-bindings-with-enums"></a>
### Implicit Route Bindings With Enums

_Implicit Enum bindings was contributed by [Nuno Maduro](https://github.com/nunomaduro)_.

PHP 8.1 introduces support for [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). Laravel 9.x introduces the ability to type-hint an Enum on your route definition and Laravel will only invoke the route if that route segment is a valid Enum value in the URI. Otherwise, an HTTP 404 response will be returned automatically. For example, given the following Enum:

```php
enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

You may define a route that will only be invoked if the `{category}` route segment is `fruits` or `people`. Otherwise, an HTTP 404 response will be returned:

```php
Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="laravel-scout-database-engine"></a>
### Laravel Scout Database Engine

_The Laravel Scout database engine was contributed by [Taylor Otwell](https://github.com/taylorotwell) and [Dries Vints](https://github.com/driesvints)_.

If your application interacts with small to medium sized databases or has a light workload, you may now use Scout's "database" engine instead of a dedicated search service such as Algolia or MeiliSerach. The database engine will use "where like" clauses and full text indexes when filtering results from your existing database to determine the applicable search results for your query.

To learn more about the Scout database engine, consult the [Scout documentation](/docs/{{version}}/scout).

<a name="full-text"></a>
### Full Text Indexes / Where Clauses

_Full text indexes and "where" clauses were contributed by [Taylor Otwell](https://github.com/taylorotwell) and [Dries Vints](https://github.com/driesvints)_.

When using MySQL or PostgreSQL, the `fullText` method may now be added to column definitions to generate full text indexes:

    $table->text('bio')->fullText();

In addition, the `whereFullText` and `orWhereFullText` methods may be used to add full text "where" clauses to a query for columns that have [full text indexes](/docs/{{version}}/migrations#available-index-types). These methods will be transformed into the appropriate SQL for the underlying database system by Laravel. For example, a `MATCH AGAINST` clause will be generated for applications utilizing MySQL:

    $users = DB::table('users')
               ->whereFullText('bio', 'web developer')
               ->get();

### Improved `route:list` CLI Output

_Improved `route:list` CLI output was contributed by [Nuno Maduro](https://github.com/nunomaduro)_.

The `route:list` CLI output has been significantly improved for the Laravel 9.x release, offering a beautiful new experience when exploring your route definitions.
