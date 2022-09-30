# Precognition

- [Introduction](#introduction)
- [Installation](#installation)
- [Making Routes Precognitive](#making-routes-precognitive)
    - [Handling Precognitive Requests](#handling-precognitive-requests)
    - [Executing Code In A Controller](#executing-controller)
- [The Precognitive Client](#precognitive-client)
    - [Aborting Stale Requests](#aborting-stale-requests)
    - [Using An Existing Axios Instance](#using-an-existing-axios-instance)
    - [Configuration](#configuration)
- [Validation](#validation)
    - [Customizing Validation Rules](#customizing-validation-rules)
    - [Working With Vue](#validating-vue)
    - [Working With Vue and Inertia](#validating-vue-inertia)
- [Polling](#polling)
- [Specification](#specification)

<a name="introduction"></a>
## Introduction

Laravel Precognition allows you to anticipate the outcome of a future request. Some ways Precognition may be used include:

- Live validation of forms, powered by Laravel validation rules.
- Notifying users that a resource they are editing has been updated since it was retrieved.
- Notifying users their session has expired.

Precognition works by executing all middleware and resolving all controller dependencies (including form requests) of a particular route, but not executing the route's controller. You will also see that Precognition is part feature and part pattern.

<a name="installation"></a>
## Installation

We have created some frontend helper libraries to make working with Precognition a dreamy delight. If you are going to use Precognition, we recommend installing the appropriate library for your project. The Laravel starter kits and skeleton install and configure the library, however if your application does not yet have it installed, you can install it via NPM. There is a vanilla JavaScript and Vue flavoured package available:

```sh
# vanilla JavaScript
npm install laravel-precognition

# Vue
npm install laravel-precognition-vue
```

If you are using vanilla JavaScript, you should also import Precognition into `resources/js/bootstrap.js` and attach the Precognition client to the `window`, making it globally available in your Blade views:

```js
import precognition from 'laravel-precognition';
window.precognition = precognition;
```

<a name="making-routes-precognitive"></a>
## Making Routes Precognitive

To add Precognition to a route, you must apply the `HandlePrecognitiveRequests` middleware:

```php
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return to_route('users.show', ['user' => $user]);
})->middleware(HandlePrecognitiveRequests::class);
```

When a precognitive request hits this route all middleware will run, the form request (or any other route dependencies) will be resolved and the form request's validation will run. After validation, regardless of if the validation passed or failed, the controller will not be executed.

<a name="handling-precognitive-requests"></a>
### Handling Precognitive Requests

Precognitive requests should generally be side-effect free. This is where the Precognition "pattern" comes in. It is recommend when you add Precognition to your routes that you consider the side-effects triggered in your application's middleware and form requests. If the side-effects present should be skipped for precognitive requests, you may need to add a conditional around the side-effect. 

As an example, if you are performing precognitive polling against an endpoint, we do not want to keep the user's session alive indefinitely. This is why, under the hood, Laravel does not persist or extend the session for precognitive requests.

You can determine if a request is precognitive by calling the `isPrecognitive()` method:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Interaction;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
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

<a name="executing-controller"></a>
### Executing the Controller

As previously discussed, Laravel Precognition with not invoke the controller, however many applications may not be using route model binding, form requests, and middleware and instead are doing this work in the controller. This is why we have created a mechanism for applications that want to use Precognition but also keep their code co-located within the controller. Imagine we have the following controller:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Resources\PostResource;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController
{
    public function update(Request $request, $id)
    {
        $post = Post::findOrFail($id);

        $this->authorize('update', $post);

        if ($this->updateConflicts($request, $post)) {
            return response('Post has been updated.', 409);
        }

        $payload = $request->validate([ /* ... */ ]);

        $post->update($payload);

        return PostResource::make($post);
    }
}
```

To use Precognition with this controller, you will need to re-bind the standard controller dispatchers. You may do this by extending the Precognition middleware:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Routing\CallableDispatcher;
use Illuminate\Routing\ControllerDispatcher;
use Illuminate\Routing\Contracts\CallableDispatcher as CallableDispatcherContract;
use Illuminate\Routing\Contracts\ControllerDispatcher as ControllerDispatcherContract;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests as BaseMiddleware;

class HandlePrecognitiveRequests extends BaseMiddleware
{
    /**
     * Prepare to handle a precognitive request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return void
     */
    protected function prepareForPrecognition($request)
    {
        parent::prepareForPrecognition($request);

        $this->container->bind(CallableDispatcherContract::class, fn ($app) => new CallableDispatcher($app));
        $this->container->bind(ControllerDispatcherContract::class, fn ($app) => new ControllerDispatcher($app));
    }
}
```

Now you must use the `precognitive` global function in your controller and place all the code that should be executed during a precognitive request within the Closure:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Resources\PostResource;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController
{
    public function update(Request $request, $id)
    {
        [$post, $payload] = precognitive(function ($bail) use ($request, $id) {
            $post = Post::findOrFail($id);

            $this->authorize('update', $post);

            if ($this->updateConflicts($request, $post)) {
                $bail(response('Post has been updated.', 409));
            }

            $payload = $request->validate([ /* ... */ ]);

            return [$post, $payload];
        });

        $post->update($payload);

        return PostResource::make($post);
    }
}
```

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

All of these methods return a `Promise` for you to work with as you need:

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

The optional `config` argument that the request methods accept is the [Axios' configuration](https://axios-http.com/docs/req_config) object with some additional Precognition options to customize behaviour and also make handling common responses easier.

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

The Precognition client has lot of [validation features baked in](#validation). If you are not using the baked in validation features, you may want to use this option to handle validation responses manually:

```js
precognitive.post(url, data, {
    onValidationError: (errors, axiosError) => {
        emailError = errors.email[0];
    },
});
```

The function's `errors` argument is the error object from the [Laravel validation response](https://laravel.com/docs/validation#validation-error-response-format) and the `axiosError` argument is the [Axios error](https://axios-http.com/docs/handling_errors) object.

> **Note** Unlike the other error handlers seen below, `onValidationError` does not receive the standard Axios response object as it's first argument, however it is still available via `axiosError.response`.

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
#### `before`

The before hook allows you to execute some code before the request is sent. This is mostly useful for repeated requests when using [validation](#validation) or [polling](#polling):

```js
precognitive.post(url, data, {
   before: () => { /* ... */ },
});
```

<a name="config-after"></a>
#### `after`

The after hook allows you to execute some code after the response is received and all other handlers have run. This is mostly useful for repeated requests when using [validation](#validation) or [polling](#polling):

```js
precognitive.post(url, data, {
   after: (promise) => promise.then(/* ... */),
});
```

<a name="config-fingerprint"></a>
#### `fingerprint`

The "fingerprint" to use when [aborting stale requests](#aborting-stale-requests).

```js
precognitive.post(url, data, {
    fingerprint: 'create-form',
});
```

<a name="config-validate"></a>
#### `validate`

The Precognition client has lot of [validation features baked in](#validation). If you are not using the baked in validation features, you may use this option to specify the input fields you would like to have validation rules run against. In the following example, the frontend is requesting that only `name` and `language` validation rules be run and not validation rules for `website`:

```js
const data = { 
    name: 'Laravel',
    language: 'PHP',
    website: '',
};

precognitive.post(url, data, {
    validate: ['name', 'language'],
    onValidationError: errors => { /* ... */ },
});
```

This request would include a `Precognition-Validate-Only name,language` header.

When filtering results from the front-end, code execution will stop after the validator has run, even if it was successful.

<a name="validation"></a>
## Validation

With Laravel Precognition, you can create realtime validation experiences for your users without having to duplicate validation rules on the frontend. As an example, lets imagine we have an existing form that creates a user in our system. The route that powers this form is using a [form request](/docs/{{version}}/validation#form-request-validation) to house the validation rules:

```php
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return to_route('users.show', ['user' => $user]);
})->middleware(HandlePrecognitiveRequests::class);
```

<a name="customizing-validation-rules"></a>
### Customizing Validation Rules

If you would like to customize the validation rules for precognitive requests, the `isPrecognitive()` method will allow you to do so:

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
                'confirmed',
                $this->isPrecognitive() 
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```

You may also find this useful in the form request's `after` validation hook.

<a name="validating-vue"></a>
### Working With Vue

When working with forms in Vue, you will already be keeping track of the form's data and validation errors. Your application may resemble the following:

```vue
<script setup>
import axios from 'axios';
import { ref } from 'vue';

const form = ref({
    username: '',
    // ...
});

const errors = ref({});

const submit = () => {
    axios.post('/users', form.value)
         .then(/* ... */)
         .catch(error => {
             if (error.response?.status !== 422) {
                 throw error;
             }

             errors.value = error.response.data.errors;
         });
};
</script>

<template>
    <form @submit.prevent="submit">
        <InputLabel for="username" />
        <TextInput id="username" v-model="form.username" />
        <InputError :message="errors.username?.[0]" />

        <!-- ... -->
    </form>
</template>
```

We will enhance this implementation by adding live validation powered by Laravel Precognition.

To achieve this we will create a precognitive form, passing through the method, url, and initial form data. Then we will use:

- `form.errors.username` where we were previously accessing `errors.username?.[0]`.
- `form.setErrors(errors)` in place of setting the `errors.value`.
- `form.submit()` in place of `axios.post(/* ... */)`.

```vue
<script setup>
import axios from 'axios';// [tl! remove]
import { ref } from 'vue';// [tl! remove]
import { usePrecognitiveForm } from 'laravel-precognition-vue';// [tl! add]

const data = ref({// [tl! remove] 
})// [tl! .hidden]
const form = usePrecognitiveForm('post', '/users', {// [tl! add]
    username: '',
    // ...
});
// [tl! remove]
const errors = ref({});// [tl! remove]

const submit = () => {
    axios.post('/users', data.value)// [tl! remove]
    form.submit()// [tl! add]
         .then(/* ... */)
         .catch(error => {
             if (error.response?.status !== 422) {
                 throw error;
             }

             errors.value = error.response.data.errors;// [tl! remove]
             form.setErrors(error.response.data.errors);// [tl! add]
         });
};
</script>

<template>
    <form @submit.prevent="submit">
        <InputLabel for="username" />
        <TextInput id="username" v-model="data.username" />
        <InputError :message="errors.username?.[0]" /><!-- [tl! remove] -->
        <InputError :message="form.errors.username" /><!-- [tl! add] -->

        <!-- ... -->
    </form>
</template>
```

> **Note** The form helper is very much inspired by Inertia's form helper.

We will now use the form helper to implement live validation. To do this we will want to call the `form.validate` function, passing through the input name. We recommend doing this in the `@change` event handler of your inputs:

```vue
<script setup>
import { usePrecognitiveForm } from 'laravel-precognition-vue';

const form = usePrecognitiveForm('post', '/users', {
    username: '',
    // ...
});

const submit = () => {
    form.submit()
         .then(/* ... */)
         .catch(error => {
             if (error.response?.status !== 422) {
                 throw error;
             }

             form.setErrors(error.response.data.errors);
         });
};
</script>

<template>
    <form @submit.prevent="submit">
        <InputLabel for="username" />
        <TextInput id="username" v-model="data.username" /><!-- [tl! remove] -->
        <TextInput id="username" v-model="form.username" @change="form.validate('username')" /><!-- [tl! add] -->
        <InputError :message="form.errors.username" />

        <!-- ... -->
    </form>
</template>
```

Precognitive validation is now in place for the form. As the form is filled out by a user, precognitive validation requests will be sent to the server and any errors that are returned will populate `form.errors`.

You will note that instead of exposing an array validation errors for a given input, the form only exposes the first validation error. If you would like to retrieve the array of errors for a given input, you may use `form.allErrors(name)` instead.

```vue
<template>
    <!-- ... -->

    <InputLabel for="username" />
    <TextInput id="username" v-model="form.username" />
    <InputError v-for="message in form.allErrors('username')" :key="message" :message="message" />

    <!-- ... -->
</template>
```

<a name="vue-validation-exposed-state"></a>
#### Exposed State

The form exposes some reactive properties, including:

- `passed`: An array of inputs that have passed validation.
- `validating`: `null` or, while validating, the last input name passed to `form.validate(name)`.

```vue
<template>
    <!-- ... -->

    <InputLabel for="username" />
    <TextInput id="username" v-model="form.username" />
    <IsValidIcon v-if="form.passed.includes('username')" /><!-- [tl! add] -->
    <ValidatingIndicator v-if="form.validating === 'username'" /><!-- [tl! add] -->
    <InputError :message="form.errors.username" />

    <!-- ... -->
<template>
```

<a name="vue-validation-configuration"></a>
#### Configuring The Validation Requests

You may pass [configuration options](#configuration) to the validator via the form's `validator.withConfig` function:

```js
let validationRequestCount = 0;

const form = usePrecognitiveForm(/* ... */);

form.validator.withConfig({
    before: () => validationRequestCount++,
});
```

If you would like to change the default debounce timeout for validation requests, you may use the `timeout` configuration option:

```js
form.validator.withConfig({ timeout: { seconds: 2 }});
```

<a name="validating-vue-inertia"></a>
### Working With Vue and Inertia

Inertia has a built-in form helper that makes working with forms a lovely experience. We wanted to maintain this experience while enabling realtime validation with Precognition, so we decided to wrap Inertia's form helper.

When using Inertia's form helper, your application may resemble the following:

```vue
<script setup>
import { useForm } from '@inertiajs/inertia-vue3';

const form = useForm({
    username: '',
    // ...
});

const submit = () => {
    form.post('/users', {
        onFinish: () => { /* ... */ },
    });
};
</script>

<template>
    <form @submit.prevent="submit">
        <InputLabel for="username" />
        <TextInput id="username" v-model="form.username" />
        <InputError :message="form.errors.username" />

        <!-- ... -->
    </form>
</template>
```

We will augment this implementation to add live validation powered by Laravel Precognition. First we will create a precognitive form, passing through the method, url, and Inertia form. We may also use `form.submit(config)` in place of `form.post(url, config)`:

```vue
<script setup>
import { useForm } from '@inertiajs/inertia-vue3';
import { usePrecognitiveForm } from 'laravel-precognition-vue';// [tl! add]

const form = useForm({// [tl! remove]
});// [tl! .hidden]
const form = usePrecognitiveForm('post', '/users', useForm({// [tl! add]
    username: '',
    // ...
}));({// [tl! .hidden]
});// [tl! remove]
(({// [tl! .hidden]
}));// [tl! add]

const submit = () => {
    form.post('/users', {// [tl! remove]
    form.submit({// [tl! add]
        onFinish: () => { /* ... */ },
    });
};
</script>

<template>
    <form @submit.prevent="submit">
        <InputLabel for="username" />
        <TextInput id="username" v-model="form.username" />
        <InputError :message="form.errors.username" />

        <!-- ... -->
    </form>
</template>
```

The `form` object is still the Inertia form helper, but we have added additional validation functionality.

We will now use the form helper to implement live validation. To do this we will want to call the `form.validate` function, passing through the input name. We recommend doing this in the `@change` event handler of your inputs:

```vue
<script setup>
import { useForm } from '@inertiajs/inertia-vue3';
import { usePrecognitiveForm } from 'laravel-precognition-vue';

const form = usePrecognitiveForm('post', '/users', useForm({
    username: '',
    // ...
}));

const submit = () => {
    form.submit({
        onFinish: () => { /* ... */ },
    });
};
</script>

<template>
    <form @submit.prevent="submit">
        <InputLabel for="username" />
        <TextInput id="username" v-model="form.username" /><!-- [tl! remove] -->
        <TextInput id="username" v-model="form.username" @change="form.validate('username')" /><!-- [tl! add] -->
        <InputError :message="form.errors.username" />

        <!-- ... -->
    </form>
</template>
```

Precognitive validation is now in place for the form. As the form is filled out by a user, precognitive validation requests will be sent to the server and any errors that are return will populate `form.errors`.

You may also like to checkout out:

- [Exposed State](#vue-validation-exposed-state)
- [Configuring the Validator](#vue-validation-configuration)

<a name="specification"></a>
## Specification

- Precognition requests MUST have a `Precognition` header with the value `true`.
- Precognition responses MUST have a `Precognition` header with the value `true`.
- When requesting specific inputs be validated, the `Precognition-Validate-Only` header SHOULD be used. The value MUST be a comma seperated list in input names e.g. `email,phone,address`.
- Routes that support Precognition MUST respond with a `Vary` header containing the value `Precognition`. This header MUST be returned for normal and Precognition requests.
- Successful Precognition requests should return a `204 No Content` response.
