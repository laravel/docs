# CSRF Protection

- [Introduction](#csrf-introduction)
- [Excluding URIs](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## Introduction

Laravel makes it easy to protect your application from [cross-site request forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) attacks. Cross-site request forgeries are a type of malicious exploit whereby unauthorized commands are performed on behalf of an authenticated user.

Laravel automatically generates a CSRF "token" for each active user session managed by the application. This token is used to verify that the authenticated user is the one actually making the requests to the application.

Anytime you define a HTML form in your application, you should include a hidden CSRF token field in the form so that the CSRF protection middleware will be able to validate the request. To generate a hidden input field containing the CSRF token, you may use the `csrf_field` helper function:

    // Blade Syntax...
    {{ csrf_field() }}

    // Generates the following HTML...
    <input type="hidden" name="_token" value="{{ csrf_token() }}">

The `VerifyCsrfToken` [middleware](/docs/{{version}}/middleware), which is included in the `web` middleware group, will automatically verify that the token in the request input matches the token stored in the session.

<a name="csrf-excluding-uris"></a>
## Excluding URIs From CSRF Protection

Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your Stripe webhook handler route from Laravel's CSRF protection.

Typically, you should place these kinds of routes outside of the `web` middleware group that the `RouteServiceProvider` applies to all routes in the default `routes.php` file. However, you may also exclude routes by adding their URIs to the `$except` property of the `VerifyCsrfToken` middleware:

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as BaseVerifier;

    class VerifyCsrfToken extends BaseVerifier
    {
        /**
         * The URIs that should be excluded from CSRF verification.
         *
         * @var array
         */
        protected $except = [
            'stripe/*',
        ];
    }

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

In addition to checking for the CSRF token as a POST parameter, the Laravel `VerifyCsrfToken` middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in a "meta" tag:

    <meta name="csrf-token" content="{{ csrf_token() }}">

Once you have created the `meta` tag, you can instruct a library like jQuery to add the token to all request headers. This provides simple, convenient CSRF protection for your AJAX based applications:

    $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
    });

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel also stores the CSRF token in a `XSRF-TOKEN` cookie. You can use the cookie value to set the `X-XSRF-TOKEN` request header. Some JavaScript frameworks, like Angular, do this automatically for you. It is unlikely that you will need to use this value manually.
