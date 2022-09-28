# Precognition

- [Introduction](#introduction)
- [Installation](#installation)
- [Validation](#validation)
    - [Backend](#backend)
    - [Frontend](#frontend)

<a name="introduction"></a>
## Introduction

Laravel Precognition allows you to anticipate the outcome of a future request. Some ways Precognition may be used include:

- Live validation of forms, powered by Laravel validation rules.
- Notifying users that a resource they are editing has been updated since it was retrieved.
- Notifying users their session has expired.

Precognition works by executing all a route's middleware and dependency resolution (including form requests), but not executing the route's controller. You will also see that Precognition is part feature and part pattern.

<a name="installation"></a>
## Installation

We have created some frontend helper libraries to make working with Precognition a dreamy delight. If you are going to use Precognition, we recommend installing the appropriate libraries for your project. The Laravel starter kits and skeleton install and configure the Precognition libraries, however if your application does not yet have it installed, you can install it via NPM. There is a vanilla JavaScript and a VueJS flavoured package available:

```
# vanilla JavaScript:
npm install laravel-precognition

# VueJS:
npm install laravel-precognition-vue
```

If you are using vanilla JavaScript, we also recommend importing Precognition into `resources/js/app.js` and attaching the Precognitive client to the `window` to make it globally available to your views:

```js
import precognitive from 'laravel-precognition';

window.precognitive = precognitive;
```

<a name="validation"></a>
## Validation

Offering frontend validation to your users can drastically improve their experience, however it requires you to duplicate validation rules in a frontend validation library. There are also validation rules that cannot be performed by frontend validation libraries, such as checking if a value is unique in the database.

With Laravel Precognition, you can create realtime validation experiences for your users without having to duplicate validation rules on the frontend.

<a name="validation-backend"></a>
### Backend

As an example, lets imagine we have an existing form that creates a user in our system. The route that powers this form is using a [Form Request](/docs/{version}/validation#form-request-validation) to house the validation rules:

```php
Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return to_route('users.show', ['user' => $user]);
});
```

To get started with Precognition on this endpoint, we must add the `HandlePrecognitiveRequests` middleware:

```php
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return redirect()->route('users.show', ['user' => $user]);
})->middleware(HandlePrecognitiveRequests::class);
```

When a Precognition request hits this route, the form request will be resolved and execution will stop after the validation has passed or failed, i.e. the controller will not actually be invoked.

Now we will take a look at how we can use the frontend library to create a realtime validation experience on the frontend of our application.

<a name="validation-frontend"></a>
### Frontend

You will need to have a mechanism to retrieve the current form data, show validation errors, and clear validation errors for your form. Once you have your form object, you may then set up your forms Precognitive validation:

```blade
<script>
    const form = {
        data() {
            // ...
        },
        setErrors(errors) {
            this.clearErrors();

            // ...
        },
        clearErrors() {
            // ...
        },
    };

    // Precognition...

    const { validate } = precognition.validate(client => client.post('/users', form.data(), {
        onPrecognitionSuccess: () => form.clearErrors(),
        onValidationError: (errors) => form.setErrors(errors),
    }));
</script>

<form action="/users" method="POST">
```

Finally, we will attach the returned `validate` function to the `onchange` event of the form's inputs.

```blade
<form action="/users" method="POST">
    <input name="name" onchange="validate">
    <input name="email" onchange="validate">
    <input name="phone" onchange="validate">
</form>
```

When the value of these inputs is changed, a Precognition request will be sent to our application. When the data is invalid our `onValidationError` callback will be invoked, but when the data is valid, our `onPrecognitionSuccess` callback will be invoked. These in combination will create a realtime validation experience for users.

<a name="validation-vanilla-javascript"></a>
---
From the readme:
This library provides a wrapper around [Axios](https://axios-http.com/) to make Precognition requests.

To get started you should install the package:

```sh
npm install laravel-precognition
```

The available request methods, which all return a `Promise`, are:

```js
import precognitive from 'laravel-precognition';

precognitive.get(url, config);

precognitive.post(url, data, config);

precognitive.patch(url, data, config);

precognitive.put(url, data, config);

precognitive.delete(url, config);
```

The optional `config` argument is the [Axios' configuration](https://axios-http.com/docs/req_config) object with some additional Precognition options, which are documented below.

## Handling Responses

The library has baked in configuration options that make handling common Precognition responses easier.

### Successful Responses

A `204 No Content` response with a `Precognition: true` header indicates that a Precognition request was successful. The `onPrecognitionSuccess` option is a convenient way to handle these responses:

```js
precognitive.post(url, data, {
    onPrecognitionSuccess: response => {
        // ...
    },
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object.

### Validation Responses

As validation is a common use-case for Precognition, we have included an `onValidationError` option:

```js
precognitive.post(url, data, {
    onValidationError: (errors, axiosError) => {
        emailError = errors.email[0];
    },
});
```

The function's `errors` argument is the error object from the [Laravel validation response](https://laravel.com/docs/validation#validation-error-response-format) and the `axiosError` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

> **Note** Unlike the other error handlers seen below, `onValidationError` does not receive the standard Axios response object as it's first argument, however it is still available via `axiosError.response`.

### Error Responses

There are a few additional error response handlers for common Precognition response codes:

```js
precognitive.post(url, data, {
    onUnauthorized: (response, error) => /* ... */,
    onForbidden: (response, error) => /* ... */,
    onNotFound: (response, error) => /* ... */,
    onConflict: (response, error) => /* ... */,
    onLocked: (response, error) => /* ... */,
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object and the `error` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

### Other Responses

You may handle additional response types as you normally would with Axios via the returned Promise:

```js
precognitive.post(url, data)
            .then(() => /* ... */)
            .catch(() => /* ... */)
            .finally(() => /* ... */);
```

### Non-Precognition Responses

If a response does not have the `Precognition: true` header, an error will be thrown. You should ensure that the Precognition middleware is in place.

## Specifying Inputs For Validation

One of the features of Precognition is the ability to specify which inputs should be validated against. To use this feature you should pass a list of input names to the `validate` option:

```js
precognitive.post('/users', data, {
    validate: ['username', 'email'],
    onValidationError: errors => {
        // ...
    },
});
```

When sending a request with the `validate` option, the backend will stop execution after validation, even when it passes.

## Using An Existing Axios Instance

If your application configures an Axios instance, you may use that instance for Precognition requests by passing it to the `use` function:

```js
import axios from 'axios';
import precognitive from 'laravel-precognition';

// Configure Axios...

window.axios = axios;
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

// Configure Precognition...

window.precognitive = precognitive.use(axios);
```

## Aborting Stale Requests

When an [`AbortController` or `CancelToken`](https://axios-http.com/docs/cancellation) is not present in the configuration, if a new request is made, any in-flight request with the same "fingerprint" will be automatically aborted. A request's fingerprint is comprised of the request's method and URL.

In the following example the method and URL match for both requests, so if the first request is still waiting on a response when second request is fired, the first request will be automatically aborted.

```js
precognitive.post('/projects/5', { name: 'Laravel' });

precognitive.post('/projects/5', { name: 'Laravel', repo: 'laravel/framework' });
```

If the URL or the method do not match, then the first request would not be aborted:

```js
precognitive.post('/projects/5', { name: 'Laravel' });

precognitive.post('/repositories/5', { name: 'Laravel' });
```

You may customize how fingerprints are calculated by passing a callback to `fingerprintRequestsUsing`:

```js
import precognitive from 'laravel-precognition';

// Configure Precognition...

precognitive.fingerprintRequestsUsing((config, axios) => config.headers['Request-Fingerprint']);
```

Alternatively, you may pass the `fingerprint` option per request:

```js
precognitive.post('/projects/5', data, {
    fingerprint: 'request-1',
});

precognitive.post('/projects/5', data, {
    fingerprint: 'request-2',
});
```

A fingerprint of `null` will disable this feature. You may disable it globally by passing `null` to `fingerprintRequestsUsing`:

```js
import precognitive from 'laravel-precognition';

// Configure Precognition...

precognitive.fingerprintRequestsUsing(null);
```

or by passing `null` to the `fingerprint` option per request:

```js
precognitive.post('/projects/5', form.data(), {
    fingerprint: null,
});
```

## Polling

As polling with Precognition is a common use-case, the library comes with some handy polling features. To create a "poll" instance, you should call the `poll` function, passing through a closure to be executed while polling:

```js
import precognitive, { Poll } from 'laravel-precognition';

const poll = Poll(() => precognitive.get('/users/me', {
    onUnauthorized: () => poll.stop() && handleUnauthorized(),
}));

// start polling...

poll.start();

// stop polling...

poll.stop();
```

### Timeout

By default, the poll will have a timeout of one minute. To configure a different timeout, you should pass the duration to the `every` function:

```js
import precognitive, { Poll } from 'laravel-precognition';

const poll = Poll(() => precognitive.get('/users/me', {
    onUnauthorized: () => poll.stop() && handleUnauthorized(),
}));

poll.every({ minutes: 10 }).start();
```

You may pass hours, minutes, seconds, and milliseconds to the `every` function to get fine-grained control of the timeout:

```js
poll.every({
    hours: 3,
    minutes: 20,
    seconds: 11,
    milliseconds: 87,
}).start();
```

### Checking the Status

To check if polling is active, you may use the `polling` function:

```js
if (poll.polling()) {
    // ...
}
```

You can also check the number of times the callback has been invoked by using the `invocations` function:

```js
if (poll.invocations() > 1000) {
    poll.stop();
}
```
