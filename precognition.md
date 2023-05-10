# Precognition

- [Introduction](#introduction)
- [Installation](#installation)
- [Live Validation With Vue](#live-validation)
    - [Working With Inertia](#working-with-inertia)
    - [Customizing Validation Rules](#customizing-validation-rules)
- [Handling Side-Effects](#handling-side-effects)
- [The Precognitive Client](#precognitive-client)
    - [Aborting Stale Requests](#aborting-stale-requests)
    - [Using An Existing Axios Instance](#using-an-existing-axios-instance)
    - [Configuration](#configuration)

<a name="introduction"></a>
## Introduction

Laravel Precognition allows you to anticipate the outcome of a future request. One of the primary use cases of Precognition is to provide live validation in your front-end application.

As we will see, Precognition works on a route by route basis. When Laravel receives a "precognitive request" it will execute all the route's middleware and resolve the route's controller dependencies, including form requests - but it will not execute the route's controller.

<a name="installation"></a>
## Installation

Laravel provides front-end libraries to make working with Precognition a delight. There is a vanilla JavaScript and Vue flavoured package available via NPM:

```sh
# Vue
npm install laravel-precognition-vue

# vanilla JavaScript
npm install laravel-precognition
```

If you are using vanilla JavaScript, you should import Precognition into `resources/js/bootstrap.js` and attach the Precognition client to the `window`, making it globally available in your Blade views:

```js
import precognition from 'laravel-precognition';

window.precognition = precognition;
```

<a name="live-validation"></a>
## Live Validation With Vue

With Laravel Precognition you can create live validation experiences for your users without having to duplicate validation rules or logic. As an example, let's build a form that stores a user in our system.

To use Precognition on a route we must include the `HandlePrecognitiveRequests` middleware in the route definition and we recommend putting your validation rules in a [FormRequest](/docs/{version}/validation#form-request-validation).

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware(HandlePrecognitiveRequests::class);
```

We will now create a form object using Precognition's `useForm` function, passing through:

- the HTTP method: `post`
- the form submission route: `/users`
- and the initial form data.

To activate live validation we will call the form's `validate` function on each input's `change` event pass through the input's name:

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit();
</script>

<template>
    <form @submit.prevent="submit">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.errors.name">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.errors.email">
            {{ form.errors.email }}
        </div>
        <button>Create User</button>
    </form>
</template>
```

The form is ready for use and will provide live validation to our users powered by the validation rules defined in the route's Form Request.

> **Note** If you are familiar with the form helper from [Inertia](https://inertiajs.com/) you will notice distinct similarities in functionality. We cover using Inertia with Precognition in the "Working With Inertia" section.

Whenever the form's inputs are changed a debounced "precognitive" validation request will now be sent to the back end. You may configure the debounce timeout by calling the form's `setValidationTimeout` function:

```js
form.setValidationTimeout({ seconds: 3 });
```

Whenever a validation request is in-flight, the form's `processingValidation` property will be `true`:

```html
<div v-if="form.processingValidation">
    Validating...
</div>
```

Any validation errors returned during a validation request or a normal form submission will automatically populate in form's `errors` object:

```html
<div v-if="form.errors.email">
    {{ form.errors.email }}
</div>
```

You can determine if the form has _any_ errors with the form's `hasErrors` property:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

You may also check if an input has passed or failed validation by passing the input's name to the form's `valid` and `invalid` functions respectively:

```html
<span v-if="form.valid('email')">
    ✅
</span>
<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> **Note** A form input will only appear as valid or invalid once it has changed and a validation response has been received.

Of course, you will want to react to the outcome of a form submission which is why the form's `submit` function returns the Axios request promise. This can be handy if you would like to access the response payload, reset the form inputs on successful submission, or handle a failed request.

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('User created.');
    })
    .catch(error => {
        alert('An error occurred.');
    });
```

<a name="working-with-inertia"></a>
### Working With Inertia

Precognition's form helper will automatically detect applications using Inertia and the `useForm` function will return an Inertia form helper with all the added validation features shown above.

The `submit` function has also streamlined, removing the need to pass through the method or URL. Instead, you may pass Inertia's [visit options](https://inertiajs.com/manual-visits) as the first argument.

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit({
    preserveScroll: true,
    onSuccess: () => form.reset(),
});
</script>
```

> **Note** When using Inertia the `submit` function does not return a Promise as seen in the Vue example above.

<a name="customizing-validation-rules"></a>
### Customizing Validation Rules

It is possible to customize the validation rules executed during a precognitive request by using the request's `isPrecognitive()` method.

In this example we will only check that the password in "uncompromised" on the final form submission. For precognitive validation requests we will only validate that the password is "required" and has a minimum of 8 characters.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    protected function rules()
    {
        return [
            'password' => [
                'required',
                $this->isPrecognitive()
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```

<a name="handling-side-effects"></a>
## Handling Side-Effects

When adding the `HandlePrecognitiveRequests` middleware to a route you should consider if there are any side-effects in _other_ middleware that you need to skip during a precognitive request.

As an example, imagine we have a middleware that increments a total number of "interactions" each user has with our application, but we don't want precognitive requests to count as an interaction. To achieve this we will check if the request is precognitive using the `isPrecognitive` method before incrementing the interaction count:

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): mixed
    {
        if (! $request->isPrecognitive()) {
            Interaction::incrementFor($request->user());
        }

        return $next($request);
    }
}
```

If your middleware is returning HTML or redirects, which is the case for Blade applications and Inertia applications, you may need to return dedicated responses for incoming precognition requests:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Interaction;

class EnsureResourceHasNotBeenUpdated
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @param  string  $resource
     * @return mixed
     */
    public function handle($request, Closure $next, $resource)
    {
        if ($request->{$resource}->updated_at->lessThanOrEqualTo($request->last_updated_at)) {
            return $next($request);
        }

        return $request->isPrecognitive()
            ? response()->json({ conflict: true }, 409)
            : back()->withInput()->with('conflict', true);
    }
}
```

The Laravel error handler will seamlessly convert HTTP exceptions to JSON for Precognition requests, so this is only a concern if you are manually returning responses.

<a name="precognitive-client"></a>
## The Precognitive Client

The Precognitive client is a wrapper around the [Axios](https://axios-http.com/) client. It allows you to easily make precognitive requests to your backend:

```js
import precognitive from 'laravel-precognition';

precognitive.get(url, config);
precognitive.post(url, data, config);
precognitive.patch(url, data, config);
precognitive.put(url, data, config);
precognitive.delete(url, config);
```

The optional `config` argument is a [configuration object](#configuration). All of these methods return a `Promise` for you to work with as you need:

```js
precognitive.post(url, data)
            .then(/* ... */)
            .catch(/* ... */)
            .finally(/* ... */);
```

> **Warning** The Precognition client will throw an error if the response does not contain the `Precognition: true` header. All routes you are hitting should apply the [Precognition middleware](#making-routes-precognitive).

<a name="aborting-stale-requests"></a>
### Aborting Stale Requests

When the client makes a new request, if an [`AbortController` or `CancelToken`](https://axios-http.com/docs/cancellation) is not present in the configuration, any in-flight request with the same "fingerprint" will be aborted. A request's fingerprint is comprised of the request's method and URL.

In the following example the method and URL match for both requests, so if the first request is still waiting on a response when second request is fired, the first request will be automatically aborted.

```js
// fingerprint: "post:/projects/5"
precognitive.post('/projects/5', { name: 'Laravel' });

// fingerprint: "post:/projects/5"
precognitive.post('/projects/5', { name: 'Laravel', repo: 'laravel/framework' });
```

If the URL or the method do not match, then the first request would not be aborted:

```js
// fingerprint: "post:/projects/5"
precognitive.post('/projects/5', { name: 'Laravel' });

// fingerprint: "post:/repositories/5"
precognitive.post('/repositories/5', { name: 'Laravel' });
```

You may globally customize how fingerprints are calculated by passing a callback to `fingerprintRequestsUsing`:

```js
import precognitive from 'laravel-precognition';

precognitive.fingerprintRequestsUsing(
    (config, axios) => config.headers['Request-Fingerprint']
);
```

Alternatively, you may pass the `fingerprint` configuration option per request:

```js
precognitive.post('/projects/5', data, {
    fingerprint: 'request-1',
});

precognitive.post('/projects/5', data, {
    fingerprint: 'request-2',
});
```

To disable this feature you may specify a fingerprint of `null`. You may disable it globally by passing `null` to `fingerprintRequestsUsing`:

```js
import precognitive from 'laravel-precognition';

precognitive.fingerprintRequestsUsing(null);
```

or by passing `null` to the `fingerprint` option per request:

```js
precognitive.post('/projects/5', form.data(), {
    fingerprint: null,
});
```

<a name="using-an-existing-axios-instance"></a>
### Using An Existing Axios Instance

The precognitive client uses the default Axios client without any changes. If your application configures an Axios instance, you may use that instance for Precognition requests by passing it to the `use` function:

```js
import axios from 'axios';
import precognitive from 'laravel-precognition';

const client = axios.create({
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
});

precognitive.use(client);
```

<a name="configuration"></a>
### Configuration

The Precognition configuration object is the [Axios' configuration](https://axios-http.com/docs/req_config) object with some additional options to customize behaviour and also make handling common responses easier.

<a name="config-onprecognitionsuccess"></a>
#### `onPrecognitionSuccess`

A `204 No Content` response with a `Precognition: true` header indicates that a Precognition request was successful. The `onPrecognitionSuccess` option is a convenient way to handle these responses:

```js
precognitive.post(url, data, {
    onPrecognitionSuccess: response => { /* ... */ },
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object.

<a name="config-onvalidationerror"></a>
#### `onValidationError`

Handle `422 Unprocessable Entity` responses:

```js
precognitive.post(url, data, {
    onValidationError: (response, error) => {
        emailError = response.data.errors.email[0];
    },
});
```

The Precognition client has lot of [validation features baked in](#validation). If you are not using the baked in validation features and you are managing validation errors manually, you may need to use this option.

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object and the `error` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

<a name="config-onunauthorized"></a>
#### `onUnauthorized`

Handle `401 Unauthorized` responses:

```js
precognitive.post(url, data, {
    onUnauthorized: (response, error) => { /* ... */ },
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object and the `error` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

<a name="config-onforbidden"></a>
#### `onForbidden`

Handle `403 Forbidden` responses:

```js
precognitive.post(url, data, {
    onForbidden: (response, error) => { /* ... */ },
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object and the `error` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

<a name="config-onnotfound"></a>
#### `onNotFound`

Handle `404 Not Found` responses:

```js
precognitive.post(url, data, {
    onNotFound: (response, error) => { /* ... */ },
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object and the `error` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

<a name="config-onconflict"></a>
#### `onConflict`

Handle `409 Conflict` responses:

```js
precognitive.post(url, data, {
    onConflict: (response, error) => { /* ... */ },
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object and the `error` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

<a name="config-onlocked"></a>
#### `onLocked`

Handle `423 Locked` responses:

```js
precognitive.post(url, data, {
    onLocked: (response, error) => { /* ... */ },
});
```

The function's `response` argument is the [Axios response](https://axios-http.com/docs/res_schema) object and the `error` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

<a name="config-before"></a>
#### `onBefore`

The before hook allows you to execute some code before the request is sent. This is mostly useful for repeated requests when using [validation](#validation) or polling:

```js
precognitive.post(url, data, {
   onBefore: () => { /* ... */ },
});
```

<a name="config-after"></a>
#### `onAfter`

The after hook allows you to execute some code after the response is received and all other handlers have run. This is mostly useful for repeated requests when using [validation](#validation) or polling:

```js
precognitive.post(url, data, {
   onAfter: (promise) => promise.then(/* ... */),
});
```

<a name="config-fingerprint"></a>
#### `fingerprint`

The "fingerprint" to use when to automatically [abort stale requests](#aborting-stale-requests).

```js
precognitive.post(url, data, {
    fingerprint: 'create-form',
});
```

<a name="config-validate"></a>
#### `validate`

Input names to add to the `Precognition-Validate-Only` header. In the following example, the frontend is requesting that only `name` and `language` validation rules be run and not validation rules for `website`:

```js
const data = { 
    name: 'Laravel',
    language: 'PHP',
    website: '',
};

precognitive.post(url, data, {
    validate: ['name', 'language'],
    onValidationError: response => { /* ... */ },
});
```

This request would include a `Precognition-Validate-Only name,language` header.

The Precognition client has lot of [validation features baked in](#validation). If you are not using the baked in validation features, you may use this option to specify the input fields you would like to have validation rules run against. 

> **Note** When filtering results from the front-end, code execution will stop after the validator has run, even if it was successful.
