# Upgrade Guide

- [Upgrading To 5.5.0 From 5.4](#upgrade-5.5.0)

<a name="upgrade-5.5.0"></a>
## Upgrading To 5.5.0 From 5.4

#### Estimated Upgrade Time: 1 Hour

> {note} We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application.

### Updating Dependencies

Update your `laravel/framework` dependency to `5.5.*` in your `composer.json` file. In addition, you should update your `phpunit/phpunit` dependency to `~6.0`.

#### Laravel Dusk

Laravel Dusk `2.0.0` has been released to provide compatibility with Laravel 5.5 and headless Chrome testing.

#### Pusher

The Pusher event broadcasting driver now requires version `~3.0` of the Pusher SDK.

### Artisan

#### The `fire` Method

Any `fire` methods present on your Artisan commands should be renamed to `handle`.

### Authorization

#### The `authorizeResource` Controller Method

When passing a multi-word model name to the `authorizeResource` method, the resulting route segment will now be "snake" case, matching the behavior of resource controllers.

#### The `before` Policy Method

The `before` method of a policy class will not be called if the class doesn't contain a method with name matching the name of the ability being checked.

### Cache

#### Database Driver

If you are using the database cache driver, you should run `php artisan cache:clear` when deploying your upgraded Laravel 5.5 application for the first time.

### Eloquent

#### The `belongsToMany` Method

If you are overriding the `belongsToMany` method on your Eloquent model, you should update your method signature to reflect the addition of new arguments:

    /**
     * Define a many-to-many relationship.
     *
     * @param  string  $related
     * @param  string  $table
     * @param  string  $foreignPivotKey
     * @param  string  $relatedPivotKey
     * @param  string  $parentKey
     * @param  string  $relatedKey
     * @param  string  $relation
     * @return \Illuminate\Database\Eloquent\Relations\BelongsToMany
     */
    public function belongsToMany($related, $table = null, $foreignPivotKey = null,
                                  $relatedPivotKey = null,$parentKey = null,
                                  $relatedKey = null, $relation = null)
    {
        //
    }

#### Model `is` Method

If you are overriding the `is` method of your Eloquent model, you should remove the `Model` type-hint from the method. This allows the `is` method to receive `null` as an argument:

    /**
     * Determine if two models have the same ID and belong to the same table.
     *
     * @param  \Illuminate\Database\Eloquent\Model|null  $model
     * @return bool
     */
    public function is($model)
    {
        //
    }

#### Model `$events` Property

The `$events` property on your models should be renamed to `$dispatchesEvents`. This change was made because of a high number of users needing to define an `events` relationship, which caused a conflict with the old property name.

#### Pivot `$parent` Property

The protected `$parent` property on the `Illuminate\Database\Eloquent\Relations\Pivot` class has been renamed to `$pivotParent`.

#### Relationship `create` Methods

The `BelongsToMany`, `HasOneOrMany`, and `MorphOneOrMany` class' `create` methods have been modified to provide a default value for the `$attributes` argument. If you are overriding these methods, you should update your signatures to match the new definition:

    public function create(array $attributes = [])
    {
        //
    }

#### Soft Deleted Models

When deleting a "soft deleted" model, the `exists` property on the model will remain `true`.

#### `withCount` Column Formatting

When using an alias, the `withCount` method will no longer automatically append `_count` onto the resulting column name. For example, in Laravel 5.4, the following query would result in a `bar_count` column being added to the query:

    $users = User::withCount('foo as bar')->get();

However, in Laravel 5.5, the alias will be used exactly as it is given. If you would like to append `_count` to the resulting column, you must specify that suffix when defining the alias:

    $users = User::withCount('foo as bar_count')->get();

### Exception Format

In Laravel 5.5, all exceptions, including validation exceptions, are converted into HTTP responses by the exception handler. In addition, the default format for JSON validation errors has changed. The new format conforms to the following convention:

    {
        "message": "The given data was invalid.",
        "errors": {
            "field-1": [
                "Error 1",
                "Error 2"
            ],
            "field-2": [
                "Error 1",
                "Error 2"
            ],
        }
    }

However, if you would like to maintain the Laravel 5.4 JSON error format, you may add the following method to your `App\Exceptions\Handler` class:

    use Illuminate\Validation\ValidationException;

    /**
     * Convert a validation exception into a JSON response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Illuminate\Validation\ValidationException  $exception
     * @return \Illuminate\Http\JsonResponse
     */
    protected function invalidJson($request, ValidationException $exception)
    {
        return response()->json($exception->errors(), $exception->status);
    }

#### JSON Authentication Attempts

This change also affects the validation error formatting for authentication attempts made over JSON. In Laravel 5.5, JSON authentication failures will return the error messages following the new formatting convention described above.

#### A Note On Form Requests

If you were customizing the response format of an individual form request, you should now override the `failedValidation` method of that form request, and throw an `HttpResponseException` instance containing your custom response:

    use Illuminate\Http\Exceptions\HttpResponseException;

    /**
     * Handle a failed validation attempt.
     *
     * @param  \Illuminate\Contracts\Validation\Validator  $validator
     * @return void
     *
     * @throws \Illuminate\Validation\ValidationException
     */
    protected function failedValidation(Validator $validator)
    {
        throw new HttpResponseException(response()->json(..., 422));
    }

### Filesystem

#### The `files` Method

The `files` method now returns an array of `SplFileInfo` objects, similar to the `allFiles` method. Previously, the `files` method returned an array of string path names.

### Mail

#### Unused Parameters

The unused `$data` and `$callback` arguments were removed from the `Illuminate\Contracts\Mail\MailQueue` contract's `queue` and `later` methods:

    /**
     * Queue a new e-mail message for sending.
     *
     * @param  string|array|MailableContract  $view
     * @param  string  $queue
     * @return mixed
     */
    public function queue($view, $queue = null);

    /**
     * Queue a new e-mail message for sending after (n) seconds.
     *
     * @param  \DateTimeInterface|\DateInterval|int  $delay
     * @param  string|array|MailableContract  $view
     * @param  string  $queue
     * @return mixed
     */
    public function later($delay, $view, $queue = null);

### Requests

#### The `has` Method

The `$request->has` method will now return `true` for empty strings and `null`. A new `$request->filled` method has been added that provides the previous behavior of the `has` method.

#### The `intersect` Method

The `intersect` method has been removed. You may replicate this behavior using `array_filter` on a call to `$request->only`:

    return array_filter($request->only('foo'));

#### The `only` Method

The `only` method will now only return attributes that are actually present in the request payload. If you would like to preserve the old behavior of the `only` method, you may use the `all` method instead.

    return $request->all('foo');

#### The `request()` Helper

The `request` helper will no longer retrieve nested keys. If needed, you may use the `input` method of the request to achieve this behavior:

    return request()->input('filters.date');

### Testing

#### Authentication Assertions

Some authentication assertions were renamed for better consistency with the rest of the framework's assertions:

<div class="content-list" markdown="1">
- `seeIsAuthenticated` was renamed to `assertAuthenticated`.
- `dontSeeIsAuthenticated` was renamed to `assertGuest`.
- `seeIsAuthenticatedAs` was renamed to `assertAuthenticatedAs`.
- `seeCredentials` was renamed to `assertCredentials`.
- `dontSeeCredentials` was renamed to `assertInvalidCredentials`.
</div>

#### Mail Fake

If you are using the `Mail` fake to determine if a mailable was **queued** during a request, you should now use `Mail::assertQueued` instead of `Mail::assertSent`. This distinction allows you to specifically assert that the mail was queued for background sending and not sent during the request itself.

### Translation

#### The `LoaderInterface`

The `Illuminate\Translation\LoaderInterface` interface has been moved to `Illuminate\Contracts\Translation\Loader`.

### Validation

#### Validator Methods

All of the validator's validation methods are now `public` instead of `protected`.

### Views

#### Dynamic "With" Variable Names

When allowing the dynamic `__call` method to share variables with a view, these variables will automatically use "camel" case. For example, given the following:

    return view('pool')->withMaximumVotes(100);

The `maximumVotes` variable may be accessed in the template like so:

    {{ $maximumVotes }}
