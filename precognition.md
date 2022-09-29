# Precognition

- [Introduction](#introduction)
- [Installation](#installation)
- [Making Routes Precognitive](#making-routes-precognitive)
    - [Handling Precognitive Requests](#handling-precognitive-requests)
- [Validation](#validation)
    - [Customizing Validation Rules](#customizing-validation-rules)
    - [Working With Vue and Inertia](#validating-vue-inertia)
- [Polling](#polling)
    - [Working With Vue and Inertia](#polling-vue-inertia)

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

```
# vanilla JavaScript
npm install laravel-precognition

# Vue
npm install laravel-precognition-vue
```

If you are using vanilla JavaScript, you should also import Precognition into `resources/js/bootstrap.js` and attach the Precognition client to the `window` to make it globally available in your views:

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

    return redirect()->route('users.show', ['user' => $user]);
})->middleware(HandlePrecognitiveRequests::class);
```

When a Precognition request hits this route all middleware will run, the form request will be resolved, and execution will stop after validation, regardless of if the validation passed or failed.

### Handling Precognitive Requests

Precognition requests are meant to be side-effect free. This is where the Precognition "pattern" comes in. It is recommend that you consider the side-effects triggered in your application's middleware and form requests and if the side-effects should be skipped for Precognitive requests. As an example, if you are polling an endpoint, we do not want to keep the user's session alive indefinitely. This is why, under the hood, Laravel does not persist or extend the session for Precognitive requests.

You can determine if a request is Precognitive by calling the `$request->isPrecognitive()` method:

```php
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

<a name="validation"></a>
## Validation

With Laravel Precognition, you can create realtime validation experiences for your users without having to duplicate validation rules on the frontend. As an example, lets imagine we have an existing form that creates a user in our system. The route that powers this form is using a [Form Request](/docs/{version}/validation#form-request-validation) to house the validation rules:

```php
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return redirect()->route('users.show', ['user' => $user]);
})->middleware(HandlePrecognitiveRequests::class);
```

<a name="customizing-validation-rules"></a>
### Customizing Validation Rules

You may also use this method in Form Requests to limit the validation rules applied during a Precognitive request:

```php
namespace App\Http\Requests;

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
            'username' => [
                ...$this->isPrecognitive() ? [
                        'unique:users',
                    ] : [
                        'required',
                        'string',
                        'min:3',
                        'max:16',
                        'unique:users',
                    ],
            ],
            // ...
        ];
    }
}
```

<a name="validating-vue"></a>
### Working With Vue

When working with Vue, you will already be keeping track of your forms data and the errors. When the form is submitted and a validation response is received, the `errors` are populated:

```vue
<script setup>
    import axios from 'axios';
    import { ref } from 'vue';

    const data = ref({
        username: '',
        // ...
    });

    const errors = ref({});

    const submit = () => {
        axios.post('/users', data.value)
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
        <VLabel for="username" />
        <VInput id="username" v-model="data.username" />
        <VError :message="errors.username" />

        <!-- ... -->
    </form>
</template>
```

We will augment this implementation to add live validation powered by Laravel Precognition.

First we will create a Precognitive form passing through the method, url and data. We will also then use:

- `form.username` where we were previously accessing `data.username`.
- `form.data()` in place of our accessing the existing `data` ref value.
- `form.setErrors(errors)` in place of setting the existing `errors` ref value.

```vue
<script setup>
    import axios from 'axios';
    import { ref } from 'vue';

    const form = usePrecognitiveForm('post', '/users', {
        username: '',
        // ...
    })

    const submit = () => {
        axios.post('/users', form.data())
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
        <VLabel for="username" />
        <VInput id="username" v-model="form.username" />
        <VError :message="form.errors.username" />

        <!-- ... -->
    </form>
</template>
```

Precognitive validation is now in place for the form. Any errors that are received during Precognition will populate the `form.errors`, as you would expect. The final result is a form that has live validation powered by Precognition.

If you are using the same Axios client to submit the form that Precognition is utilising (you can learn more about [customizing the client in API docs](#)), you may optionally replace the axios call with `form.submit()`:

```vue
<script setup>
    import axios from 'axios';
    import { ref } from 'vue';

    const form = usePrecognitiveForm('post', '/users', {
        username: '',
        // ...
    })

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
        <VLabel for="username" />
        <VInput id="username" v-model="form.username" />
        <VError :message="form.errors.username" />

        <!-- ... -->
    </form>
</template>
```
