# Precognition

- [Introduction](#introduction)
- [Live Validation](#live-validation)
    - [Using Vue](#using-vue)
    - [Using Vue and Inertia](#using-vue-and-inertia)
    - [Using React](#using-react)
    - [Using React and Inertia](#using-react-and-inertia)
    - [Using Alpine and Blade](#using-alpine)
    - [Configuring Axios](#configuring-axios)
- [Customizing Validation Rules](#customizing-validation-rules)
- [Handling File Uploads](#handling-file-uploads)
- [Managing Side-Effects](#managing-side-effects)
- [Testing](#testing)

<a name="introduction"></a>
## Introduction

Laravel Precognition allows you to anticipate the outcome of a future HTTP request. One of the primary use cases of Precognition is the ability to provide "live" validation for your frontend JavaScript application without having to duplicate your application's backend validation rules. Precognition pairs especially well with Laravel's Inertia-based [starter kits](/docs/{{version}}/starter-kits).

When Laravel receives a "precognitive request", it will execute all of the route's middleware and resolve the route's controller dependencies, including validating [form requests](/docs/{{version}}/validation#form-request-validation) - but it will not actually execute the route's controller method.

<a name="live-validation"></a>
## Live Validation

<a name="using-vue"></a>
### Using Vue

Using Laravel Precognition, you can offer live validation experiences to your users without having to duplicate your validation rules in your frontend Vue application. To illustrate how it works, let's build a form for creating new users within our application.

First, to enable Precognition for a route, the `HandlePrecognitiveRequests` middleware should be added to the route definition. You should also create a [form request](/docs/{{version}}/validation#form-request-validation) to house the route's validation rules:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

Next, you should install the Laravel Precognition frontend helpers for Vue via NPM:

```shell
npm install laravel-precognition-vue
```

With the Laravel Precognition package installed, you can now create a form object using Precognition's `useForm` function, providing the HTTP method (`post`), the target URL (`/users`), and the initial form data.

Then, to enable live validation, invoke the form's `validate` method on each input's `change` event, providing the input's name:

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
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.invalid('email')">
            {{ form.errors.email }}
        </div>

        <button :disabled="form.processing">
            Create User
        </button>
    </form>
</template>
```

Now, as the form is filled by the user, Precognition will provide live validation output powered by the validation rules in the route's form request. When the form's inputs are changed, a debounced "precognitive" validation request will be sent to your Laravel application. You may configure the debounce timeout by calling the form's `setValidationTimeout` function:

```js
form.setValidationTimeout(3000);
```

When a validation request is in-flight, the form's `validating` property will be `true`:

```html
<div v-if="form.validating">
    Validating...
</div>
```

Any validation errors returned during a validation request or a form submission will automatically populate the form's `errors` object:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

You can determine if the form has any errors using the form's `hasErrors` property:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

You may also determine if an input has passed or failed validation by passing the input's name to the form's `valid` and `invalid` functions, respectively:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> A form input will only appear as valid or invalid once it has changed and a validation response has been received.

If you are validating a subset of a form's inputs with Precognition, it can be useful to manually clear errors. You may use the form's `forgetError` function to achieve this:

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
>
```

As we have seen, you can hook into an input's `change` event and validate individual inputs as the user interacts with them; however, you may need to validate inputs that the user has not yet interacted with. This is common when building a "wizard", where you want to validate all visible inputs, whether the user has interacted with them or not, before moving to the next step.

To do this with Precognition, you should call the `validate` method passing the field names you wish to validate to the `only` configuration key. You may handle the validation result with `onSuccess` or `onValidationError` callbacks:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

Of course, you may also execute code in reaction to the response to the form submission. The form's `submit` function returns an Axios request promise. This provides a convenient way to access the response payload, reset the form inputs on successful submission, or handle a failed request:

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

You may determine if a form submission request is in-flight by inspecting the form's `processing` property:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Using Vue and Inertia

> [!NOTE]
> If you would like a head start when developing your Laravel application with Vue and Inertia, consider using one of our [starter kits](/docs/{{version}}/starter-kits). Laravel's starter kits provide backend and frontend authentication scaffolding for your new Laravel application.

Before using Precognition with Vue and Inertia, be sure to review our general documentation on [using Precognition with Vue](#using-vue). When using Vue with Inertia, you will need to install the Inertia compatible Precognition library via NPM:

```shell
npm install laravel-precognition-vue-inertia
```

Once installed, Precognition's `useForm` function will return an Inertia [form helper](https://inertiajs.com/forms#form-helper) augmented with the validation features discussed above.

The form helper's `submit` method has been streamlined, removing the need to specify the HTTP method or URL. Instead, you may pass Inertia's [visit options](https://inertiajs.com/manual-visits) as the first and only argument. In addition, the `submit` method does not return a Promise as seen in the Vue example above. Instead, you may provide any of Inertia's supported [event callbacks](https://inertiajs.com/manual-visits#event-callbacks) in the visit options given to the `submit` method:

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue-inertia';

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

<a name="using-react"></a>
### Using React

Using Laravel Precognition, you can offer live validation experiences to your users without having to duplicate your validation rules in your frontend React application. To illustrate how it works, let's build a form for creating new users within our application.

First, to enable Precognition for a route, the `HandlePrecognitiveRequests` middleware should be added to the route definition. You should also create a [form request](/docs/{{version}}/validation#form-request-validation) to house the route's validation rules:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

Next, you should install the Laravel Precognition frontend helpers for React via NPM:

```shell
npm install laravel-precognition-react
```

With the Laravel Precognition package installed, you can now create a form object using Precognition's `useForm` function, providing the HTTP method (`post`), the target URL (`/users`), and the initial form data.

To enable live validation, you should listen to each input's `change` and `blur` event. In the `change` event handler, you should set the form's data with the `setData` function, passing the input's name and new value. Then, in the `blur` event handler invoke the form's `validate` method, providing the input's name:

```jsx
import { useForm } from 'laravel-precognition-react';

export default function Form() {
    const form = useForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = (e) => {
        e.preventDefault();

        form.submit();
    };

    return (
        <form onSubmit={submit}>
            <label htmlFor="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label htmlFor="email">Email</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                Create User
            </button>
        </form>
    );
};
```

Now, as the form is filled by the user, Precognition will provide live validation output powered by the validation rules in the route's form request. When the form's inputs are changed, a debounced "precognitive" validation request will be sent to your Laravel application. You may configure the debounce timeout by calling the form's `setValidationTimeout` function:

```js
form.setValidationTimeout(3000);
```

When a validation request is in-flight, the form's `validating` property will be `true`:

```jsx
{form.validating && <div>Validating...</div>}
```

Any validation errors returned during a validation request or a form submission will automatically populate the form's `errors` object:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

You can determine if the form has any errors using the form's `hasErrors` property:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

You may also determine if an input has passed or failed validation by passing the input's name to the form's `valid` and `invalid` functions, respectively:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> A form input will only appear as valid or invalid once it has changed and a validation response has been received.

If you are validating a subset of a form's inputs with Precognition, it can be useful to manually clear errors. You may use the form's `forgetError` function to achieve this:

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.value);

        form.forgetError('avatar');
    }}
>
```

As we have seen, you can hook into an input's `blur` event and validate individual inputs as the user interacts with them; however, you may need to validate inputs that the user has not yet interacted with. This is common when building a "wizard", where you want to validate all visible inputs, whether the user has interacted with them or not, before moving to the next step.

To do this with Precognition, you should call the `validate` method passing the field names you wish to validate to the `only` configuration key. You may handle the validation result with `onSuccess` or `onValidationError` callbacks:

```jsx
<button
    type="button"
    onClick={() => form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })}
>Next Step</button>
```

Of course, you may also execute code in reaction to the response to the form submission. The form's `submit` function returns an Axios request promise. This provides a convenient way to access the response payload, reset the form's inputs on a successful form submission, or handle a failed request:

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('User created.');
        })
        .catch(error => {
            alert('An error occurred.');
        });
};
```

You may determine if a form submission request is in-flight by inspecting the form's `processing` property:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### Using React and Inertia

> [!NOTE]
> If you would like a head start when developing your Laravel application with React and Inertia, consider using one of our [starter kits](/docs/{{version}}/starter-kits). Laravel's starter kits provide backend and frontend authentication scaffolding for your new Laravel application.

Before using Precognition with React and Inertia, be sure to review our general documentation on [using Precognition with React](#using-react). When using React with Inertia, you will need to install the Inertia compatible Precognition library via NPM:

```shell
npm install laravel-precognition-react-inertia
```

Once installed, Precognition's `useForm` function will return an Inertia [form helper](https://inertiajs.com/forms#form-helper) augmented with the validation features discussed above.

The form helper's `submit` method has been streamlined, removing the need to specify the HTTP method or URL. Instead, you may pass Inertia's [visit options](https://inertiajs.com/manual-visits) as the first and only argument. In addition, the `submit` method does not return a Promise as seen in the React example above. Instead, you may provide any of Inertia's supported [event callbacks](https://inertiajs.com/manual-visits#event-callbacks) in the visit options given to the `submit` method:

```js
import { useForm } from 'laravel-precognition-react-inertia';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = (e) => {
    e.preventDefault();

    form.submit({
        preserveScroll: true,
        onSuccess: () => form.reset(),
    });
};
```

<a name="using-alpine"></a>
### Using Alpine and Blade

Using Laravel Precognition, you can offer live validation experiences to your users without having to duplicate your validation rules in your frontend Alpine application. To illustrate how it works, let's build a form for creating new users within our application.

First, to enable Precognition for a route, the `HandlePrecognitiveRequests` middleware should be added to the route definition. You should also create a [form request](/docs/{{version}}/validation#form-request-validation) to house the route's validation rules:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

Next, you should install the Laravel Precognition frontend helpers for Alpine via NPM:

```shell
npm install laravel-precognition-alpine
```

Then, register the Precognition plugin with Alpine in your `resources/js/app.js` file:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

With the Laravel Precognition package installed and registered, you can now create a form object using Precognition's `$form` "magic", providing the HTTP method (`post`), the target URL (`/users`), and the initial form data.

To enable live validation, you should bind the form's data to its relevant input and then listen to each input's `change` event. In the `change` event handler, you should invoke the form's `validate` method, providing the input's name:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">Name</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">Email</label>
    <input
        id="email"
        name="email"
        x-model="form.email"
        @change="form.validate('email')"
    />
    <template x-if="form.invalid('email')">
        <div x-text="form.errors.email"></div>
    </template>

    <button :disabled="form.processing">
        Create User
    </button>
</form>
```

Now, as the form is filled by the user, Precognition will provide live validation output powered by the validation rules in the route's form request. When the form's inputs are changed, a debounced "precognitive" validation request will be sent to your Laravel application. You may configure the debounce timeout by calling the form's `setValidationTimeout` function:

```js
form.setValidationTimeout(3000);
```

When a validation request is in-flight, the form's `validating` property will be `true`:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

Any validation errors returned during a validation request or a form submission will automatically populate the form's `errors` object:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

You can determine if the form has any errors using the form's `hasErrors` property:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

You may also determine if an input has passed or failed validation by passing the input's name to the form's `valid` and `invalid` functions, respectively:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> A form input will only appear as valid or invalid once it has changed and a validation response has been received.

As we have seen, you can hook into an input's `change` event and validate individual inputs as the user interacts with them; however, you may need to validate inputs that the user has not yet interacted with. This is common when building a "wizard", where you want to validate all visible inputs, whether the user has interacted with them or not, before moving to the next step.

To do this with Precognition, you should call the `validate` method passing the field names you wish to validate to the `only` configuration key. You may handle the validation result with `onSuccess` or `onValidationError` callbacks:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

You may determine if a form submission request is in-flight by inspecting the form's `processing` property:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### Repopulating Old Form Data

In the user creation example discussed above, we are using Precognition to perform live validation; however, we are performing a traditional server-side form submission to submit the form. So, the form should be populated with any "old" input and validation errors returned from the server-side form submission:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

Alternatively, if you would like to submit the form via XHR you may use the form's `submit` function, which returns an Axios request promise:

```html
<form
    x-data="{
        form: $form('post', '/register', {
            name: '',
            email: '',
        }),
        submit() {
            this.form.submit()
                .then(response => {
                    this.form.reset();

                    alert('User created.')
                })
                .catch(error => {
                    alert('An error occurred.');
                });
        },
    }"
    @submit.prevent="submit"
>
```

<a name="configuring-axios"></a>
### Configuring Axios

The Precognition validation libraries use the [Axios](https://github.com/axios/axios) HTTP client to send requests to your application's backend. For convenience, the Axios instance may be customized if required by your application. For example, when using the `laravel-precognition-vue` library, you may add additional request headers to each outgoing request in your application's `resources/js/app.js` file:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

Or, if you already have a configured Axios instance for your application, you may tell Precognition to use that instance instead:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> The Inertia flavored Precognition libraries will only use the configured Axios instance for validation requests. Form submissions will always be sent by Inertia.

<a name="customizing-validation-rules"></a>
## Customizing Validation Rules

It is possible to customize the validation rules executed during a precognitive request by using the request's `isPrecognitive` method.

For example, on a user creation form, we may want to validate that a password is "uncompromised" only on the final form submission. For precognitive validation requests, we will simply validate that the password is required and has a minimum of 8 characters. Using the `isPrecognitive` method, we can customize the rules defined by our form request:

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

<a name="handling-file-uploads"></a>
## Handling File Uploads

By default, Laravel Precognition does not upload or validate files during a precognitive validation request. This ensure that large files are not unnecessarily uploaded multiple times.

Because of this behavior, you should ensure that your application [customizes the corresponding form request's validation rules](#customizing-validation-rules) to specify the field is only required for full form submissions:

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array
 */
protected function rules()
{
    return [
        'avatar' => [
            ...$this->isPrecognitive() ? [] : ['required'],
            'image',
            'mimes:jpg,png',
            'dimensions:ratio=3/2',
        ],
        // ...
    ];
}
```

If you would like to include files in every validation request, you may invoke the `validateFiles` function on your client-side form instance:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## Managing Side-Effects

When adding the `HandlePrecognitiveRequests` middleware to a route, you should consider if there are any side-effects in _other_ middleware that should be skipped during a precognitive request.

For example, you may have a middleware that increments the total number of "interactions" each user has with your application, but you may not want precognitive requests to be counted as an interaction. To accomplish this, we may check the request's `isPrecognitive` method before incrementing the interaction count:

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

<a name="testing"></a>
## Testing

If you would like to make precognitive requests in your tests, Laravel's `TestCase` includes a `withPrecognition` helper which will add the `Precognition` request header.

Additionally, if you would like to assert that a precognitive request was successful, e.g., did not return any validation errors, you may use the `assertSuccessfulPrecognition` method on the response:

```php tab=Pest
it('validates registration form with precognition', function () {
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();

    expect(User::count())->toBe(0);
});
```

```php tab=PHPUnit
public function test_it_validates_registration_form_with_precognition()
{
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();
    $this->assertSame(0, User::count());
}
```
