# Precognition

- [Introduction](#introduction)
- [Installation](#installation)
- [Validation](#validation)
    - [Making Routes Precognitive](#making-routes-precognitive)
    - [Working With Vue and Inertia](#validating-vue-inertia)
    - [Validating a Form Object](#form-object)
    - [Working With Vanilla JavaScript](#validating-vanilla-javascript)


<a name="introduction"></a>
## Introduction

Laravel Precognition allows you to anticipate the outcome of a future request. Some ways Precognition may be used include:

- Live validation of forms, powered by Laravel validation rules.
- Notifying users that a resource they are editing has been updated since it was retrieved.
- Notifying users their session has expired.

Precognition works by executing all middleware and resolving all dependencies (including form requests) of a particular route, but not executing the route's controller. You will also see that Precognition is part feature and part pattern.

<a name="installation"></a>
## Installation

We have created some frontend helper libraries to make working with Precognition a dreamy delight. If you are going to use Precognition, we recommend installing the appropriate libraries for your project. The Laravel starter kits and skeleton install and configure the Precognition libraries, however if your application does not yet have it installed, you can install it via NPM. There is a vanilla JavaScript and a Vue flavoured packages available:

```
# vanilla JavaScript
npm install laravel-precognition

# Vue
npm install laravel-precognition-vue
```

If you are using vanilla JavaScript, you should also import Precognition into `resources/js/bootstrap.js` and attaching the Precognition client to the `window` to make it globally available in your views:

```js
import precognition from 'laravel-precognition';
window.precognition = precognition;
```

<a name="validation"></a>
## Validation

Offering frontend validation to your users can drastically improve their experience, however it requires you to duplicate validation rules in a frontend validation library. There are also validation rules that cannot be performed by frontend validation libraries, such as checking if a value is unique in the database.

With Laravel Precognition, you can create realtime validation experiences for your users without having to duplicate validation rules on the frontend. As an example, lets imagine we have an existing form that creates a user in our system. The route that powers this form is using a [Form Request](/docs/{version}/validation#form-request-validation) to house the validation rules:

```php
Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return to_route('users.show', ['user' => $user]);
});
```

<a name="making-routes-precognitive"></a>
### Making Routes Precognitive

To get started with Precognition on this endpoint, we must add the `HandlePrecognitiveRequests` middleware:

```php
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return redirect()->route('users.show', ['user' => $user]);
})->middleware(HandlePrecognitiveRequests::class);
```

When a Precognition request hits this route, the form request will be resolved and execution will stop after the validation has passed or failed, i.e. the controller will not actually be invoked.

<a name="validating-vue-inertia"></a>
### Working With Vue and Inertia

When working with Vue and Inertia, you are likely already familiar with the form helper. When using Precognition, we augment the form helper to add some useful functionality. Assuming we have the following set up in our application:

```html
<script setup>
    import { useForm } from '@inertiajs/inertia-vue3';

    const form = useForm({
        name: '',
        email: '',
    });

    const submit = () => {
        form.post('/users', {
            // Inertia options...
        });
    };
</script>

<template>
    <form @submit.prevent="submit">
        <input name="name" v-model="form.name" ... >
        <input name="email" v-model="form.email" ... >

        <!-- ... -->
    </form>
</template>
```

We will want to swap out `useForm` for `usePrecognitiveForm` passing through the method and the URL before the data values:

```html
<script setup>
    import { usePrecognitiveForm } from 'laravel-precognition-vue-inertia';

    const form = usePrecognitiveForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = () => {
        form.post('/users', {
            // Inertia options...
        });
    };
</script>

<template>
    <form @submit.prevent="submit">
        <input name="name" v-model="form.name" ... >
        <input name="email" v-model="form.email" ... >

        <!-- ... -->
    </form>
</template>
```

Now we are able to simplify the form submission logic:

```js
const submit = () => {
    form.submit({
        // Inertia options...
    });
};
```

The precognitive form already knows the url and method, so we are now able to just call `form.submit()` without again specifying the method and the URL. However we have not implemented any validation logic yet, so now we will tell the inputs to validate whenever the value changes:

```
<form @submit.prevent="submit">
    <input name="name" v-model="form.name" @change="form.validate" ... >
    <input name="email" v-model="form.email" @change="form.validate" ... >

    <!-- ... -->
</form>
```



<a name="form-object"></a>
### Validating a Form Object

Now we will take a look at how we can use the frontend library to create a realtime validation experience. For the best experience, we suggest creating a form object that offers the following API:

```blade
<script>
    const form = {
        method: 'post',
        url(): '/users',
        data() {
            // ...
        },
        setErrors(errors) {
            // ...
        },
        clearErrors() {
            // ...
        },
    };
</script>
```

<a name="validating-vanilla-javascript"></a>
### Working With Vanilla JavaScript

Once you have a form object implemented, you can create a validator for your form. You should attach the returned validator to the `window`:

```blade
<script type="module">
    window.validator = precognition.validate(form);
</script>
```

You can now validate your inputs on the `changed` event by invoking the `validator.validate()` function passing the name of the input:

```blade
<form action="/users" method="POST">
    @csrf
    <input name="name" onchange="window.validator.validate('name')">
    <input name="email" onchange="window.validator.validate('email')">
    <input name="phone" onchange="window.validator.validate('phone')">

    <!-- ... -->
</form>
```

When the value of these inputs are changed, a debounced Precognition request will be sent to our application. If the data is invalid, the form's `setErrors` function will be passed the received validation errors, but when the data is valid, the form's `clearErrors` function will be invoked. These in combination will create a realtime validation experience for users.

As the validator will run validation rules for inputs that have already "changed", it is a good idea in Blade applications to tell the validator which inputs already have validation errors on page load. This will account for any server-side validation errors:

```blade
<script type="module">
    window.validator = precognition.validate(form)
          .withChanged(@js($errors->keys()));
</script>
```

To see the full API of the validator, check out the [API docs](#).


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
import precognition from 'laravel-precognition';

precognition.get(url, config);

precognition.post(url, data, config);

precognition.patch(url, data, config);

precognition.put(url, data, config);

precognition.delete(url, config);
```

The optional `config` argument is the [Axios' configuration](https://axios-http.com/docs/req_config) object with some additional Precognition options, which are documented below.

## Handling Responses

The library has baked in configuration options that make handling common Precognition responses easier.

### Successful Responses

A `204 No Content` response with a `Precognition: true` header indicates that a Precognition request was successful. The `onPrecognitionSuccess` option is a convenient way to handle these responses:

```js
precognition.post(url, data, {
    onPrecognitionSuccess: response => {
        // ...
    },
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object.

### Validation Responses

As validation is a common use-case for Precognition, we have included an `onValidationError` option:

```js
precognition.post(url, data, {
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
precognition.post(url, data, {
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
precognition.post(url, data)
            .then(() => /* ... */)
            .catch(() => /* ... */)
            .finally(() => /* ... */);
```

### Non-Precognition Responses

If a response does not have the `Precognition: true` header, an error will be thrown. You should ensure that the Precognition middleware is in place.

## Specifying Inputs For Validation

One of the features of Precognition is the ability to specify which inputs should be validated against. To use this feature you should pass a list of input names to the `validate` option:

```js
precognition.post('/users', data, {
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
import precognition from 'laravel-precognition';

// Configure Axios...

window.axios = axios;
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

// Configure Precognition...

window.precognition = precognition.use(axios);
```

## Aborting Stale Requests

When an [`AbortController` or `CancelToken`](https://axios-http.com/docs/cancellation) is not present in the configuration, if a new request is made, any in-flight request with the same "fingerprint" will be automatically aborted. A request's fingerprint is comprised of the request's method and URL.

In the following example the method and URL match for both requests, so if the first request is still waiting on a response when second request is fired, the first request will be automatically aborted.

```js
precognition.post('/projects/5', { name: 'Laravel' });

precognition.post('/projects/5', { name: 'Laravel', repo: 'laravel/framework' });
```

If the URL or the method do not match, then the first request would not be aborted:

```js
precognition.post('/projects/5', { name: 'Laravel' });

precognition.post('/repositories/5', { name: 'Laravel' });
```

You may customize how fingerprints are calculated by passing a callback to `fingerprintRequestsUsing`:

```js
import precognition from 'laravel-precognition';

// Configure Precognition...

precognition.fingerprintRequestsUsing((config, axios) => config.headers['Request-Fingerprint']);
```

Alternatively, you may pass the `fingerprint` option per request:

```js
precognition.post('/projects/5', data, {
    fingerprint: 'request-1',
});

precognition.post('/projects/5', data, {
    fingerprint: 'request-2',
});
```

A fingerprint of `null` will disable this feature. You may disable it globally by passing `null` to `fingerprintRequestsUsing`:

```js
import precognition from 'laravel-precognition';

// Configure Precognition...

precognition.fingerprintRequestsUsing(null);
```

or by passing `null` to the `fingerprint` option per request:

```js
precognition.post('/projects/5', form.data(), {
    fingerprint: null,
});
```

## Polling

As polling with Precognition is a common use-case, the library comes with some handy polling features. To create a "poll" instance, you should call the `poll` function, passing through a closure to be executed while polling:

```js
import precognition, { Poll } from 'laravel-precognition';

const poll = Poll(() => precognition.get('/users/me', {
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
import precognition, { Poll } from 'laravel-precognition';

const poll = Poll(() => precognition.get('/users/me', {
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
