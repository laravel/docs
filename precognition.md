# Precognition

- [Introduction](#introduction)
- [Installation](#installation)
- [Making Routes Precognitive](#making-routes-precognitive)
- [Validation](#validation)
    - [Working With Vue and Inertia](#validating-vue-inertia)
- [Polling](#polling)

<a name="introduction"></a>
## Introduction

Laravel Precognition allows you to anticipate the outcome of a future request. Some ways Precognition may be used include:

- Live validation of forms, powered by Laravel validation rules.
- Notifying users that a resource they are editing has been updated since it was retrieved.
- Notifying users their session has expired.

Precognition works by executing all middleware and resolving all dependencies (including form requests) of a particular route, but not executing the route's controller. You will also see that Precognition is part feature and part pattern.

<a name="installation"></a>
## Installation

We have created some frontend helper libraries to make working with Precognition a dreamy delight. If you are going to use Precognition, we recommend installing the appropriate libraries for your project. The Laravel starter kits and skeleton install and configure the Precognition libraries, however if your application does not yet have it installed, you can install it via NPM. There is a vanilla JavaScript, Vue, and Vue with Inertia flavoured packages available:

```
# vanilla JavaScript
npm install laravel-precognition

# Vue
npm install laravel-precognition-vue

# Vue and Inertia
npm install laravel-precognition-vue-inertia
```

If you are using vanilla JavaScript, you should also import Precognition into `resources/js/bootstrap.js` and attach the Precognition client to the `window` to make it globally available in your views:

```js
import precognition from 'laravel-precognition';
window.precognition = precognition;
```

<a name="making-routes-precognitive"></a>
## Making Routes Precognitive

To get started with Precognition an endpoint, we must apply the `HandlePrecognitiveRequests` middleware:

```php
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return redirect()->route('users.show', ['user' => $user]);
})->middleware(HandlePrecognitiveRequests::class);
```

When a Precognition request hits this route, all middleware will run and the form request will be resolved and execution will stop after the validation has passed or failed, i.e. the controller will not actually be invoked.

<a name="validation"></a>
## Validation

Offering frontend validation to your users can drastically improve their experience, however it requires you to duplicate validation rules in a frontend validation library. There are also validation rules that cannot be performed by frontend validation libraries, such as checking if a value is unique in the database.

With Laravel Precognition, you can create realtime validation experiences for your users without having to duplicate validation rules on the frontend. As an example, lets imagine we have an existing form that creates a user in our system. The route that powers this form is using a [Form Request](/docs/{version}/validation#form-request-validation) to house the validation rules:

```php
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    $user = User::create($request->validated());

    return redirect()->route('users.show', ['user' => $user]);
})->middleware(HandlePrecognitiveRequests::class);
```

<a name="validating-vue-inertia"></a>
### Working With Vue and Inertia

Precognition augments the Inertia form helper to add some validation functionality. Assuming we have the following form in our application:

```vue
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
        <VLabel for="name" />
        <VInput id="name" v-model="form.name" />
        <VError :message="form.errors.name" />

        <!-- ... -->
    </form>
</template>
```

We will swap out `useForm` for `usePrecognitiveForm`, additionally passing through the method and the URL before the form data:

```vue
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
        <VLabel for="name" />
        <VInput id="name" v-model="form.name" />
        <VError :message="form.errors.name" />

        <!-- ... -->
    </form>
</template>
```

We are now able to simplify the form submission logic, if we want to, by removing the method and the url:

```js
const submit = () => {
    form.submit({
        // Inertia options...
    });
};
```

The precognitive form already knows the url and method, so we are now able to call `form.submit()` without specifying them again. However, we have not implemented any validation logic yet, so now we will finally tell the inputs to validate whenever their value changes by invoking the `form.validate` function in the `@changed` handler, passing through the inputs name:

```vue
<form @submit.prevent="submit">
    <VLabel for="name" />
    <VInput id="name" v-model="form.name" @change="form.validate('name')" />
    <VError :message="form.errors.name" />

    <!-- ... -->
</form>
```

Precognitive validation is now in place for our form. Any errors that are received will be available via the reactive `form.errors` object, as you would normally expect. The final result is a Inertia form that has live validation powered by Precognition:

```vue
<script setup>
    import { usePrecognitiveForm } from 'laravel-precognition-vue-inertia';

    const form = usePrecognitiveForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = () => {
        form.submit({
            // Inertia options...
        });
    };
</script>

<template>
    <form @submit.prevent="submit">
        <VLabel for="name" />
        <VInput id="name" v-model="form.name" @change="form.validate('name')" />
        <VError :message="form.errors.name" />

        <!-- ... -->
    </form>
</template>
```

You can see the libraries readme for [full API documentation](#).

<a name="#polling"></a>
## Polling
