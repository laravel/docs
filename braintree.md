# Laravel Cashier (Braintree)

- [Introduction](#introduction)
    - [Caveats](#caveats)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Plan Credit Coupon](#plan-credit-coupon)
    - [Database Migrations](#database-migrations)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Currency Configuration](#currency-configuration)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Changing Plans](#changing-plans)
    - [Subscription Taxes](#subscription-taxes)
    - [Cancelling Subscriptions](#cancelling-subscriptions)
    - [Resuming Subscriptions](#resuming-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Credit Card Up Front](#with-credit-card-up-front)
    - [Without Credit Card Up Front](#without-credit-card-up-front)
- [Customers](#customers)
    - [Creating Customers](#creating-customers)
- [Cards](#cards)
    - [Updating Credit Cards](#updating-credit-cards)
- [Handling Webhooks](#handling-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Failed Subscriptions](#handling-failed-subscriptions)
- [Single Charges](#single-charges)
    - [Simple Charge](#simple-charge)
    - [Charge With Invoice](#charge-with-invoice)
- [Invoices](#invoices)
    - [Generating Invoice PDFs](#generating-invoice-pdfs)

<a name="introduction"></a>
## Introduction

Laravel Cashier Braintree provides an expressive, fluent interface to [Braintree's](https://www.braintreepayments.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs.

> {note} These are the docs for the Cashier integration with Braintree. You may find the Stripe integration docs [here](/docs/{{version}}/billing).

> {note} If you're only performing "one-off" charges and do not offer subscriptions, you should not use Cashier. Instead, use the Braintree SDK directly.

<a name="caveats"></a>
### Caveats

For many operations, the Stripe and Braintree implementations of Cashier function the same. Both services provide subscription billing with credit cards but Braintree also supports payments via PayPal. However, Braintree also lacks some features that are supported by Stripe. You should keep the following in mind when deciding to use Stripe or Braintree:

<div class="content-list" markdown="1">

- Braintree supports PayPal while Stripe does not.
- Braintree does not support the `increment` and `decrement` methods on subscriptions. This is a Braintree limitation, not a Cashier limitation.
- Braintree does not support percentage based discounts. This is a Braintree limitation, not a Cashier limitation.

</div>

<a name="installation"></a>
## Installation

First, require the Cashier package for Braintree with Composer:

    composer require laravel/cashier-braintree

<a name="configuration"></a>
## Configuration

<a name="plan-credit-coupon"></a>
### Plan Credit Coupon

Before using Cashier with Braintree, you will need to define a `plan-credit` discount in your Braintree control panel. This discount will be used to properly prorate subscriptions that change from yearly to monthly billing, or from monthly to yearly billing.

The discount amount configured in the Braintree control panel can be any value you wish, as Cashier will override the defined amount with our own custom amount each time we apply the coupon. This coupon is needed since Braintree does not natively support prorating subscriptions across subscription frequencies.

<a name="database-migrations"></a>
### Database Migrations

Before using Cashier, we'll need to [prepare the database](/docs/{{version}}/migrations). We need to add several columns to your `users` table and create a new `subscriptions` table to hold all of our customer's subscriptions:

    Schema::table('users', function (Blueprint $table) {
        $table->string('braintree_id')->nullable();
        $table->string('paypal_email')->nullable();
        $table->string('card_brand')->nullable();
        $table->string('card_last_four')->nullable();
        $table->timestamp('trial_ends_at')->nullable();
    });

    Schema::create('subscriptions', function (Blueprint $table) {
        $table->increments('id');
        $table->unsignedInteger('user_id');
        $table->string('name');
        $table->string('braintree_id');
        $table->string('braintree_plan');
        $table->integer('quantity');
        $table->timestamp('trial_ends_at')->nullable();
        $table->timestamp('ends_at')->nullable();
        $table->timestamps();
    });

Once the migrations have been created, run the `migrate` Artisan command.

<a name="billable-model"></a>
### Billable Model

Next, add the `Billable` trait to your model definition:

    use Laravel\Cashier\Billable;

    class User extends Authenticatable
    {
        use Billable;
    }

<a name="api-keys"></a>
### API Keys

Next, you should configure the following options in your `services.php` file:

    'braintree' => [
        'model'  => App\User::class,
        'environment' => env('BRAINTREE_ENV'),
        'merchant_id' => env('BRAINTREE_MERCHANT_ID'),
        'public_key' => env('BRAINTREE_PUBLIC_KEY'),
        'private_key' => env('BRAINTREE_PRIVATE_KEY'),
    ],

Then you should add the following Braintree SDK calls to your `AppServiceProvider` service provider's `boot` method:

    \Braintree_Configuration::environment(config('services.braintree.environment'));
    \Braintree_Configuration::merchantId(config('services.braintree.merchant_id'));
    \Braintree_Configuration::publicKey(config('services.braintree.public_key'));
    \Braintree_Configuration::privateKey(config('services.braintree.private_key'));

<a name="currency-configuration"></a>
### Currency Configuration

The default Cashier currency is United States Dollars (USD). You can change the default currency by calling the `Cashier::useCurrency` method from within the `boot` method of one of your service providers. The `useCurrency` method accepts two string parameters: the currency and the currency's symbol:

    use Laravel\Cashier\Cashier;

    Cashier::useCurrency('eur', '€');

<a name="subscriptions"></a>
## Subscriptions

<a name="creating-subscriptions"></a>
### Creating Subscriptions

To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription:

    $user = User::find(1);

    $user->newSubscription('main', 'premium')->create($token);

The first argument passed to the `newSubscription` method should be the name of the subscription. If your application only offers a single subscription, you might call this `main` or `primary`. The second argument is the specific plan the user is subscribing to. This value should correspond to the plan's identifier in Braintree.

The `create` method, which accepts a credit card / source token, will begin the subscription as well as update your database with the customer ID and other relevant billing information.

#### Additional User Details

If you would like to specify additional customer details, you may do so by passing them as the second argument to the `create` method:

    $user->newSubscription('main', 'monthly')->create($token, [
        'email' => $email,
    ]);

To learn more about the additional fields supported by Braintree, check out the corresponding [Braintree documentation](https://developers.braintreepayments.com/reference/request/customer/create/php).

#### Coupons

If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method:

    $user->newSubscription('main', 'monthly')
         ->withCoupon('code')
         ->create($token);

<a name="checking-subscription-status"></a>
### Checking Subscription Status

Once a user is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the user has an active subscription, even if the subscription is currently within its trial period:

    if ($user->subscribed('main')) {
        //
    }

The `subscribed` method also makes a great candidate for a [route middleware](/docs/{{version}}/middleware), allowing you to filter access to routes and controllers based on the user's subscription status:

    public function handle($request, Closure $next)
    {
        if ($request->user() && ! $request->user()->subscribed('main')) {
            // This user is not a paying customer...
            return redirect('billing');
        }

        return $next($request);
    }

If you would like to determine if a user is still within their trial period, you may use the `onTrial` method. This method can be useful for displaying a warning to the user that they are still on their trial period:

    if ($user->subscription('main')->onTrial()) {
        //
    }

The `subscribedToPlan` method may be used to determine if the user is subscribed to a given plan based on a given plan ID. In this example, we will determine if the user's `main` subscription is actively subscribed to the `monthly` plan:

    if ($user->subscribedToPlan('monthly', 'main')) {
        //
    }

The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trail period:

    if ($user->subscription('main')->recurring()) {
        //
    }

#### Cancelled Subscription Status

To determine if the user was once an active subscriber, but has cancelled their subscription, you may use the `cancelled` method:

    if ($user->subscription('main')->cancelled()) {
        //
    }

You may also determine if a user has cancelled their subscription, but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time:

    if ($user->subscription('main')->onGracePeriod()) {
        //
    }

To determine if the user has cancelled their subscription is no longer within their "grace period", you may use the `ended` method:

    if ($user->subscription('main')->ended()) {
        //
    }

<a name="changing-plans"></a>
### Changing Plans

After a user is subscribed to your application, they may occasionally want to change to a new subscription plan. To swap a user to a new subscription, pass the plan's identifier to the `swap` method:

    $user = App\User::find(1);

    $user->subscription('main')->swap('provider-plan-id');

If the user is on trial, the trial period will be maintained. Also, if a "quantity" exists for the subscription, that quantity will also be maintained.

If you would like to swap plans and cancel any trial period the user is currently on, you may use the `skipTrial` method:

    $user->subscription('main')
            ->skipTrial()
            ->swap('provider-plan-id');

<a name="subscription-taxes"></a>
### Subscription Taxes

To specify the tax percentage a user pays on a subscription, implement the `taxPercentage` method on your billable model, and return a numeric value between 0 and 100, with no more than 2 decimal places.

    public function taxPercentage()
    {
        return 20;
    }

The `taxPercentage` method enables you to apply a tax rate on a model-by-model basis, which may be helpful for a user base that spans multiple countries and tax rates.

> {note} The `taxPercentage` method only applies to subscription charges. If you use Cashier to make "one off" charges, you will need to manually specify the tax rate at that time.

<a name="cancelling-subscriptions"></a>
### Cancelling Subscriptions

To cancel a subscription, call the `cancel` method on the user's subscription:

    $user->subscription('main')->cancel();

When a subscription is cancelled, Cashier will automatically set the `ends_at` column in your database. This column is used to know when the `subscribed` method should begin returning `false`. For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th.

You may determine if a user has cancelled their subscription but are still on their "grace period" using the `onGracePeriod` method:

    if ($user->subscription('main')->onGracePeriod()) {
        //
    }

If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription:

    $user->subscription('main')->cancelNow();

<a name="resuming-subscriptions"></a>
### Resuming Subscriptions

If a user has cancelled their subscription and you wish to resume it, use the `resume` method. The user **must** still be on their grace period in order to resume a subscription:

    $user->subscription('main')->resume();

If the user cancels a subscription and then resumes that subscription before the subscription has fully expired, they will not be billed immediately. Instead, their subscription will be re-activated, and they will be billed on the original billing cycle.

<a name="subscription-trials"></a>
## Subscription Trials

<a name="with-credit-card-up-front"></a>
### With Credit Card Up Front

If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions:

    $user = User::find(1);

    $user->newSubscription('main', 'monthly')
                ->trialDays(10)
                ->create($token);

This method will set the trial period ending date on the subscription record within the database, as well as instruct Braintree to not begin billing the customer until after this date.

> {note} If the customer's subscription is not cancelled before the trial ending date they will be charged as soon as the trial expires, so you should be sure to notify your users of their trial ending date.

You may determine if the user is within their trial period using either the `onTrial` method of the user instance, or the `onTrial` method of the subscription instance. The two examples below are identical:

    if ($user->onTrial('main')) {
        //
    }

    if ($user->subscription('main')->onTrial()) {
        //
    }

<a name="without-credit-card-up-front"></a>
### Without Credit Card Up Front

If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration:

    $user = User::create([
        // Populate other user properties...
        'trial_ends_at' => now()->addDays(10),
    ]);

> {note}  Be sure to add a [date mutator](/docs/{{version}}/eloquent-mutators#date-mutators) for `trial_ends_at` to your model definition.

Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the `User` instance will return `true` if the current date is not past the value of `trial_ends_at`:

    if ($user->onTrial()) {
        // User is within their trial period...
    }

You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not created an actual subscription yet:

    if ($user->onGenericTrial()) {
        // User is within their "generic" trial period...
    }

Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual:

    $user = User::find(1);

    $user->newSubscription('main', 'monthly')->create($token);

<a name="customers"></a>
## Customers

<a name="creating-customers"></a>
### Creating Customers

Occasionally, you may wish to create a Braintree customer without beginning a subscription. You may accomplish this using the `createAsBraintreeCustomer` method:

    $user->createAsBraintreeCustomer();

Once the customer has been created in Braintree, you may begin a subscription at a later date.

<a name="cards"></a>
## Cards

<a name="updating-credit-cards"></a>
### Updating Credit Cards

The `updateCard` method may be used to update a customer's credit card information. This method accepts a Braintree token and will assign the new credit card as the default billing source:

    $user->updateCard($token);

<a name="handling-webhooks"></a>
## Handling Webhooks

Braintree can notify your application of a variety of events via webhooks. To handle webhooks, define a route that points to Cashier's webhook controller. This controller will handle all incoming webhook requests and dispatch them to the proper controller method:

    Route::post(
        'braintree/webhook',
        '\Laravel\Cashier\Http\Controllers\WebhookController@handleWebhook'
    );

> {note} Once you have registered your route, be sure to configure the webhook URL in your Braintree control panel settings.

By default, this controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Braintree settings); however, as we'll soon discover, you can extend this controller to handle any webhook event you like.

#### Webhooks & CSRF Protection

Since webhooks need to bypass Laravel's [CSRF protection](/docs/{{version}}/csrf), be sure to list the URI as an exception in your `VerifyCsrfToken` middleware or list the route outside of the `web` middleware group:

    protected $except = [
        'braintree/*',
    ];

<a name="defining-webhook-event-handlers"></a>
### Defining Webhook Event Handlers

Cashier automatically handles subscription cancellation on failed charges, but if you have additional webhook events you would like to handle, extend the Webhook controller. Your method names should correspond to Cashier's expected convention, specifically, methods should be prefixed with `handle` and the "camel case" name of the webhook you wish to handle. For example, if you wish to handle the `dispute_opened` webhook, you should add a `handleDisputeOpened` method to the controller:

    <?php

    namespace App\Http\Controllers;

    use Braintree\WebhookNotification;
    use Laravel\Cashier\Http\Controllers\WebhookController as CashierController;

    class WebhookController extends CashierController
    {
        /**
         * Handle a new dispute.
         *
         * @param  \Braintree\WebhookNotification  $webhook
         * @return \Symfony\Component\HttpFoundation\Responses
         */
        public function handleDisputeOpened(WebhookNotification $webhook)
        {
            // Handle The Webhook...
        }
    }

<a name="handling-failed-subscriptions"></a>
### Failed Subscriptions

What if a customer's credit card expires? No worries - Cashier includes a Webhook controller that can easily cancel the customer's subscription for you. Just point a route to the controller:

    Route::post(
        'braintree/webhook',
        '\Laravel\Cashier\Http\Controllers\WebhookController@handleWebhook'
    );

That's it! Failed payments will be captured and handled by the controller. The controller will cancel the customer's subscription when Braintree determines the subscription has failed (normally after three failed payment attempts). Don't forget: you will need to configure the webhook URI in your Braintree control panel settings.

<a name="single-charges"></a>
## Single Charges

<a name="simple-charge"></a>
### Simple Charge

> {note} You should pass the full dollar amount to the `charge` method:

If you would like to make a "one off" charge against a subscribed customer's credit card, you may use the `charge` method on a billable model instance.

    $user->charge(1);

The `charge` method accepts an array as its second argument, allowing you to pass any options you wish to the underlying charge creation. Consult the Braintree documentation regarding the options available to you when creating charges:

    $user->charge(1, [
        'custom_option' => $value,
    ]);

The `charge` method will throw an exception if the charge fails. If the charge is successful, the full Braintree response will be returned from the method:

    try {
        $response = $user->charge(1);
    } catch (Exception $e) {
        //
    }

<a name="charge-with-invoice"></a>
### Charge With Invoice

Sometimes you may need to make a one-time charge but also generate an invoice for the charge so that you may offer a PDF receipt to your customer. The `invoiceFor` method lets you do just that. For example, let's invoice the customer $5.00 for a "One Time Fee":

    $user->invoiceFor('One Time Fee', 5);

The invoice will be charged immediately against the user's credit card. The `invoiceFor` method also accepts an array as its third argument. This array contains the billing options for the invoice item. You must include a `description` option when calling the `invoiceFor` method:

    $user->invoiceFor('One Time Fee', 5, [
        'description' => 'your invoice description here',
    ]);

<a name="invoices"></a>
## Invoices

You may easily retrieve an array of a billable model's invoices using the `invoices` method:

    $invoices = $user->invoices();

    // Include pending invoices in the results...
    $invoices = $user->invoicesIncludingPending();

When listing the invoices for the customer, you may use the invoice's helper methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them:

    <table>
        @foreach ($invoices as $invoice)
            <tr>
                <td>{{ $invoice->date()->toFormattedDateString() }}</td>
                <td>{{ $invoice->total() }}</td>
                <td><a href="/user/invoice/{{ $invoice->id }}">Download</a></td>
            </tr>
        @endforeach
    </table>

<a name="generating-invoice-pdfs"></a>
### Generating Invoice PDFs

From within a route or controller, use the `downloadInvoice` method to generate a PDF download of the invoice. This method will automatically generate the proper HTTP response to send the download to the browser:

    use Illuminate\Http\Request;

    Route::get('user/invoice/{invoice}', function (Request $request, $invoiceId) {
        return $request->user()->downloadInvoice($invoiceId, [
            'vendor'  => 'Your Company',
            'product' => 'Your Product',
        ]);
    });
