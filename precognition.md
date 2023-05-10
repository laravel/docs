# Precognition

- [Introduction](#introduction)
- [Live Validation With Vue](#live-validation)
    - [Working With Inertia](#working-with-inertia)
    - [Customizing Validation Rules](#customizing-validation-rules)
- [Managing Side-Effects](#managing-side-effects)

<a name="introduction"></a>
## Introduction

Laravel Precognition allows you to anticipate the outcome of a future request. One of the primary use cases of Precognition, and the one we will demonstrate here, is to provide live validation in your front-end application.

As we will see, Precognition works on a route by route basis. When Laravel receives a "precognitive request" it will execute all the route's middleware and resolve the route's controller dependencies, including form requests - but it will not execute the route's controller.

<a name="live-validation"></a>
## Live Validation With Vue

With Laravel Precognition you can create live validation experiences for your users without having to duplicate validation rules or logic. As an example, let's build a form for creating new users within our application.

To use Precognition on a route we must apply the `HandlePrecognitiveRequests` middleware in the route definition. You should also have your validation rules in a [FormRequest](/docs/{version}/validation#form-request-validation).

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware(HandlePrecognitiveRequests::class);
```

Switching gears to focus on the application's front end, we will first install the Vue package via NPM:

```sh
npm install laravel-precognition-vue
```

With the package installed we can now create a form object using Precognition's `useForm` function, passing through:

- the HTTP method: `post`
- the form submission route: `/users`
- and the initial form data.

To activate live validation we will call the form's `validate` function on each input's `change` event providing the input's name:

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

The form is now ready and will provide live validation powered by the route's Form Request.

> **Note** If you are familiar with the form helper from [Inertia](https://inertiajs.com/) you will notice distinct similarities in functionality. We cover using Inertia with Precognition in the "Working With Inertia" section below.

Whenever the form's inputs are changed a debounced "precognitive" validation request will be sent to the back end. You may configure the debounce timeout by calling the form's `setValidationTimeout` function:

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

Precognition's `useForm` function will automatically detect applications using Inertia and will return an Inertia form helper with all the added validation features shown above.

The helper's `submit` function has been streamlined, removing the need to pass through the method or URL. Instead, you may pass Inertia's [visit options](https://inertiajs.com/manual-visits) as the first, and only, argument.

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

It is possible to customize the validation rules executed during a precognitive request by using the request's `isPrecognitive` method.

In this example we will only check that the password is "uncompromised" on the final form submission. For precognitive validation requests we will validate that the password is required and has a minimum of 8 characters.

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

<a name="managing-side-effects"></a>
## Managing Side-Effects

When adding the `HandlePrecognitiveRequests` middleware to a route you should consider if there are any side-effects in _other_ middleware that you need to skip during a precognitive request.

As an example, imagine we have a middleware that increments a total number of "interactions" each user has with our application, but we don't want precognitive requests to count as an interaction. To achieve this we will check the request's `isPrecognitive` method before incrementing the interaction count:

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
