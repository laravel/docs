# Laravel Cashier

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Currency Configuration](#currency-configuration)
    - [Webhooks](#webhooks)
- [Customers](#customers)
    - [Creating Customers](#creating-customers)
- [Payment Methods](#payment-methods)
    - [Saving Payment Methods](#saving-payment-methods)
    - [Retrieving Payment Methods](#retrieving-payment-methods)
    - [Check For A Payment Method](#check-for-a-payment-method)
    - [Updating The Default Payment Method](#updating-the-default-payment-method)
    - [Adding Payment Methods](#adding-payment-methods)
    - [Deleting Payment Methods](#deleting-payment-methods)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Changing Plans](#changing-plans)
    - [Subscription Quantity](#subscription-quantity)
    - [Subscription Taxes](#subscription-taxes)
    - [Subscription Anchor Date](#subscription-anchor-date)
    - [Cancelling Subscriptions](#cancelling-subscriptions)
    - [Resuming Subscriptions](#resuming-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Payment Method Up Front](#with-payment-method-up-front)
    - [Without Payment Method Up Front](#without-payment-method-up-front)
- [Handling Stripe Webhooks](#handling-stripe-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Failed Subscriptions](#handling-failed-subscriptions)
    - [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
    - [Simple Charge](#simple-charge)
    - [Charge With Invoice](#charge-with-invoice)
    - [Refunding Charges](#refunding-charges)
- [Invoices](#invoices)
    - [Generating Invoice PDFs](#generating-invoice-pdfs)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [Handling Extra Payment Actions](#handling-extra-payment-actions)
    - [Off-session Payment Notification](#off-session-payment-notification)

<a name="introduction"></a>
## Introduction

Laravel Cashier provides an expressive, fluent interface to [Stripe's](https://stripe.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs. Cashier is also ready to handle [SCA](#strong-customer-authentication).

> {note} Cashier makes use of a fixed Stripe API version to send requests. The latest version of Cashier makes use of the Stripe API version `2019-05-16`. Beware that we will update this version on minor releases in order to make use of new Stripe features, updates or bug fixes.

<a name="upgrading-cashier"></a>
## Upgrading Cashier

When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier/blob/master/UPGRADE.md).

<a name="installation"></a>
## Installation

First, require the Cashier package for Stripe with Composer:

    composer require laravel/cashier

The Cashier service provider registers its own database migration directory with the framework, so you should migrate your database after installing the package. The Cashier migrations will add several columns to your `users` table and create a new `subscriptions` table to hold all of our customer's subscriptions:

    php artisan migrate

If you need to overwrite the migrations that ship with the Cashier package, you can publish them using the command below:

    php artisan vendor:publish --tag="cashier-migrations"

After publishing you should add the following setting to the `register` method of your `AppServiceProvider` in order to prevent the shipped migrations from running:

    use Laravel\Cashier\Cashier;

    Cashier::ignoreMigrations();

To make sure Cashier properly handles all Stripe events, you'll also need to [set up Cashier's webhook handling](#handling-stripe-webhooks).

<a name="configuration"></a>
## Configuration

<a name="billable-model"></a>
### Billable Model

Before using Cashier, we'll need to add the `Billable` trait to your model definition. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information:

    use Laravel\Cashier\Billable;

    class User extends Authenticatable
    {
        use Billable;
    }

Cashier assumes your Billable model will be the default `App\User` class that ships with Laravel. If you wish to change this you can update this in your `.env` file:

    CASHIER_MODEL=App\User

<a name="api-keys"></a>
### API Keys

Next, you should configure your Stripe key in your `.env` file. You can retrieve your Stripe API keys from the Stripe control panel. 

    STRIPE_KEY=
    STRIPE_SECRET=

<a name="currency-configuration"></a>
### Currency Configuration

The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` env variable:

    CASHIER_CURRENCY=EUR

In addition to setting the currency you can also set a locale for formatting the money values which are used in invoices. Cashier internally makes use of [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale for a money value:

    CASHIER_CURRENCY_LOCALE=nl_BE

> {note} In order to use other locales than the default "en" one, you'll need to make sure the `ext-intl` PHP extension is installed and configured on your server.

<a name="customers"></a>
## Customers

<a name="creating-customers"></a>
### Creating Customers

Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method:

    $user->createAsStripeCustomer();

Once the customer has been created in Stripe, you may begin a subscription at a later date.

<a name="payment-methods"></a>
## Payment Methods

<a name="saving-payment-methods"></a>
### Saving Payment Methods

In order to create subscriptions or perform "one off" charges with Stripe, we'll need to save a new payment method with Stripe first and retrieve its identifier. The process for this differs between these two use cases so let's go over them both.

#### Payment Methods For Subscriptions

When saving credit cards to a customer for future use we'll need to make sure that we use the Setup Intents API to make sure we can safely use the card when starting a new subscription. Cashier includes a method to easily start a new setup intents session:

    $setupIntent = $user->createSetupIntent();

In order to save a card for future use, [follow this guide by Stripe](https://stripe.com/docs/payments/cards/saving-cards#saving-card-without-payment) and use the Setup Intent object from above to save a new card.

When you have the `result.setupIntent.paymentMethod` we'll need to save it to the customer. You can either [add it as a new payment method](#adding-payment-methods) or [update the default payment method](#updating-the-default-payment-method). You can also immediately use the `result.setupIntent.paymentMethod` to [create a new subscription](#creating-subscriptions).

#### Payment Methods For Single Charges

When making single charges we'll only need to use a payment method one single time. While you could technically retrieve the default payment method from a customer (which is used for billing and invoicing) and use that to make the payment you can also opt to allow the customer to enter a one-time payment method with the Stripe.js library.

A detailed example can be examined [in the Stripe docs](https://stripe.com/docs/payments/payment-intents/migration#elements). More info about the `createPaymentMethod` call can be found [here](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method). When you have the `result.paymentMethod.id`, use it to [create single charges](#simple-charge).

<a name="retrieving-payment-methods"></a>
### Retrieving Payment Methods

The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances:

    $paymentMethods = $user->paymentMethods();

To retrieve the default payment method, the `defaultPaymentMethod` method may be used;

    $paymentMethod = $user->defaultPaymentMethod();

<a name="check-for-a-payment-method"></a>
### Check For A Payment Method

You may check if a customer has a payment method attached to their account using the `hasPaymentMethod` method:

    if ($user->hasPaymentMethod()) {
        //
    }

<a name="updating-the-default-payment-method"></a>
### Updating The Default Payment Method

The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method:

    $user->updateDefaultPaymentMethod($paymentMethod);

To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method:

    $user->updateDefaultPaymentMethodFromStripe();

> {note} The default payment method on a customer can only be used for invoicing and creating new subscriptions. Because of a limitation by Stripe, it cannot be used for single charges.

<a name="adding-payment-methods"></a>
### Adding Payment Methods

To add a new payment method, you can call the `addPaymentMethod` method on the billable user:

    $user->addPaymentMethod($paymentMethod);

<a name="deleting-payment-methods"></a>
### Deleting Payment Methods

To delete a payment method, you can call the `delete` method on the paymentMethod instance you wish to delete:

    $paymentMethod->delete();

The `deletePaymentMethods` method will delete all of the payment method information stored by your application:

    $user->deletePaymentMethods();

> {note} If the user has an active subscription, you should consider preventing them from deleting the default payment method.

<a name="subscriptions"></a>
## Subscriptions

<a name="creating-subscriptions"></a>
### Creating Subscriptions

To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription:

    $user = User::find(1);

    $user->newSubscription('main', 'premium')->create($paymentMethod);

The first argument passed to the `newSubscription` method should be the name of the subscription. If your application only offers a single subscription, you might call this `main` or `primary`. The second argument is the specific plan the user is subscribing to. This value should correspond to the plan's identifier in Stripe.

The `create` method, which accepts [a Stripe payment method identifier](#saving-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the customer ID and other relevant billing information.

#### Additional User Details

If you would like to specify additional customer details, you may do so by passing them as the second argument to the `create` method:

    $user->newSubscription('main', 'monthly')->create($paymentMethod, [
        'email' => $email,
    ]);

To learn more about the additional fields supported by Stripe, check out Stripe's [documentation on customer creation](https://stripe.com/docs/api#create_customer).

#### Coupons

If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method:

    $user->newSubscription('main', 'monthly')
         ->withCoupon('code')
         ->create($paymentMethod);

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

The `subscribedToPlan` method may be used to determine if the user is subscribed to a given plan based on a given Stripe plan ID. In this example, we will determine if the user's `main` subscription is actively subscribed to the `monthly` plan:

    if ($user->subscribedToPlan('monthly', 'main')) {
        //
    }

The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period:

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

To determine if the user has cancelled their subscription and is no longer within their "grace period", you may use the `ended` method:

    if ($user->subscription('main')->ended()) {
        //
    }

<a name="incomplete-and-past-due-status"></a>
#### Incomplete and Past Due Status

If a subscription requires a secondary payment action after creating a subscription the subscription becomes "incomplete". The same thing happens when swapping a plan but then the subscription becomes "past_due". When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Checking if a subscription has an incomplete payment can be done with the following method on the user or subscription:

    if ($user->hasIncompletePayment()) {
        //
    }

    if ($user->subscription('main')->hasIncompletePayment()) {
        //
    }

When your subscription has an incomplete payment you'll need to redirect your user to the payment page so the user can confirm the payment. You can use the `latestPayment` on the `Subscription` model for this:

    <a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
        Please confirm your payment.
    </a>

> {note} When your subscription is in an `incomplete` state it cannot be changed until payment was confirmed. This means that the `swap` and `updateQuantity` methods will throw an exception if you attempt to use them in this state.

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

If you want to swap plans and also immediately invoice the user instead of waiting for the next billing cyle, you can use the `swapAndInvoice` method:

    $user = App\User::find(1);

    $user->subscription('main')->swapAndInvoice('provider-plan-id');

<a name="subscription-quantity"></a>
### Subscription Quantity

Sometimes subscriptions are affected by "quantity". For example, your application might charge $10 per month **per user** on an account. To easily increment or decrement your subscription quantity, use the `incrementQuantity` and `decrementQuantity` methods:

    $user = User::find(1);

    $user->subscription('main')->incrementQuantity();

    // Add five to the subscription's current quantity...
    $user->subscription('main')->incrementQuantity(5);

    $user->subscription('main')->decrementQuantity();

    // Subtract five to the subscription's current quantity...
    $user->subscription('main')->decrementQuantity(5);

Alternatively, you may set a specific quantity using the `updateQuantity` method:

    $user->subscription('main')->updateQuantity(10);

The `noProrate` method may be used to update the subscription's quantity without pro-rating the charges:

    $user->subscription('main')->noProrate()->updateQuantity(10);

For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities).

<a name="subscription-taxes"></a>
### Subscription Taxes

To specify the tax percentage a user pays on a subscription, implement the `taxPercentage` method on your billable model, and return a numeric value between 0 and 100, with no more than 2 decimal places.

    public function taxPercentage()
    {
        return 20;
    }

The `taxPercentage` method enables you to apply a tax rate on a model-by-model basis, which may be helpful for a user base that spans multiple countries and tax rates.

> {note} The `taxPercentage` method only applies to subscription charges. If you use Cashier to make "one off" charges, you will need to manually specify the tax rate at that time.

#### Syncing Tax Percentages

When changing the hard-coded value returned by the `taxPercentage` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the returned `taxPercentage` value, you should call the `syncTaxPercentage` method on the user's subscription instance:

    $user->subscription('main')->syncTaxPercentage();

<a name="subscription-anchor-date"></a>
### Subscription Anchor Date

By default, the billing cycle anchor is the date the subscription was created, or if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method:

    use App\User;
    use Carbon\Carbon;

    $user = User::find(1);

    $anchor = Carbon::parse('first day of next month');

    $user->newSubscription('main', 'premium')
                ->anchorBillingCycleOn($anchor->startOfDay())
                ->create($paymentMethod);

For more information on managing subscription billing cycles, consult the [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle)

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

<a name="with-payment-method-up-front"></a>
### With Payment Method Up Front

If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions:

    $user = User::find(1);

    $user->newSubscription('main', 'monthly')
                ->trialDays(10)
                ->create($paymentMethod);

This method will set the trial period ending date on the subscription record within the database, as well as instruct Stripe to not begin billing the customer until after this date. When using the `trialDays` method, Cashier will overwrite any default trial period configured for the plan in Stripe.

> {note} If the customer's subscription is not cancelled before the trial ending date they will be charged as soon as the trial expires, so you should be sure to notify your users of their trial ending date.

The `trialUntil` method allows you to provide a `DateTime` instance to specify when the trial period should end:

    use Carbon\Carbon;

    $user->newSubscription('main', 'monthly')
                ->trialUntil(Carbon::now()->addDays(10))
                ->create($paymentMethod);

You may determine if the user is within their trial period using either the `onTrial` method of the user instance, or the `onTrial` method of the subscription instance. The two examples below are identical:

    if ($user->onTrial('main')) {
        //
    }

    if ($user->subscription('main')->onTrial()) {
        //
    }

<a name="without-payment-method-up-front"></a>
### Without Payment Method Up Front

If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration:

    $user = User::create([
        // Populate other user properties...
        'trial_ends_at' => now()->addDays(10),
    ]);

> {note} Be sure to add a [date mutator](/docs/{{version}}/eloquent-mutators#date-mutators) for `trial_ends_at` to your model definition.

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

    $user->newSubscription('main', 'monthly')->create($paymentMethod);

<a name="handling-stripe-webhooks"></a>
## Handling Stripe Webhooks

Stripe can notify your application of a variety of events via webhooks. By default a route that points to Cashier's webhook controller is configured through its service provider. This controller will handle all incoming webhook requests and dispatch them to the proper controller method.

By default, this controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any webhook event you like.

Next, make sure to configure the webhook URL in your Stripe control panel settings. The full list of all webhooks you should configure in the Stripe control panel are:

- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `invoice.payment_action_required`

> {note} Make sure you protect incoming requests with Cashier's included [webhook signature verification](/docs/{{version}}/billing#verifying-webhook-signatures) middleware.

#### Webhooks & CSRF Protection

Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/{{version}}/csrf), be sure to list the URI as an exception in your `VerifyCsrfToken` middleware or list the route outside of the `web` middleware group:

    protected $except = [
        'stripe/*',
    ];

<a name="defining-webhook-event-handlers"></a>
### Defining Webhook Event Handlers

Cashier automatically handles subscription cancellation on failed charges, but if you have additional webhook events you would like to handle, extend the Webhook controller. Your method names should correspond to Cashier's expected convention, specifically, methods should be prefixed with `handle` and the "camel case" name of the webhook you wish to handle. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you should add a `handleInvoicePaymentSucceeded` method to the controller:

    <?php

    namespace App\Http\Controllers;

    use Laravel\Cashier\Http\Controllers\WebhookController as CashierController;

    class WebhookController extends CashierController
    {
        /**
         * Handle invoice payment succeeded.
         *
         * @param  array  $payload
         * @return \Symfony\Component\HttpFoundation\Response
         */
        public function handleInvoicePaymentSucceeded($payload)
        {
            // Handle The Event
        }
    }

Next, define a route to your Cashier controller within your `routes/web.php` file. This will overwrite the default shipped route:

    Route::post(
        'stripe/webhook',
        '\App\Http\Controllers\WebhookController@handleWebhook'
    );

<a name="handling-failed-subscriptions"></a>
### Failed Subscriptions

What if a customer's credit card expires? No worries - Cashier's Webhook controller will cancel the customer's subscription for you. Failed payments will be captured and handled by the controller. The controller will cancel the customer's subscription when Stripe determines the subscription has failed (normally after three failed payment attempts).

<a name="verifying-webhook-signatures"></a>
### Verifying Webhook Signatures

To secure your webhooks, you may use [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures). For convenience, Cashier automatically includes a middleware which validates that the incoming Stripe webhook request is valid.

To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` env variable is set in your `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard.

<a name="single-charges"></a>
## Single Charges

<a name="simple-charge"></a>
### Simple Charge

> {note} The `charge` method accepts the amount you would like to charge in the **lowest denominator of the currency used by your application**.

If you would like to make a "one off" charge against a subscribed customer's payment method, you may use the `charge` method on a billable model instance. You'll need to [provide a payment method identifier](#saving-payment-methods) as the second argument:

    // Stripe Accepts Charges In Cents...
    $stripeCharge = $user->charge(100, $paymentMethod);

The `charge` method accepts a an array as its third argument, allowing you to pass any options you wish to the underlying Stripe charge creation. Consult the Stripe documentation regarding the options available to you when creating charges:

    $user->charge(100, $paymentMethod, [
        'custom_option' => $value,
    ]);

The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method:

    try {
        $payment = $user->charge(100, $paymentMethod);
    } catch (Exception $e) {
        //
    }

<a name="charge-with-invoice"></a>
### Charge With Invoice

Sometimes you may need to make a one-time charge but also generate an invoice for the charge so that you may offer a PDF receipt to your customer. The `invoiceFor` method lets you do just that. For example, let's invoice the customer $5.00 for a "One Time Fee":

    // Stripe Accepts Charges In Cents...
    $user->invoiceFor('One Time Fee', 500);

The invoice will be charged immediately against the user's default payment method. The `invoiceFor` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array. This final argument accepts the billing options for the invoice itself:

    $user->invoiceFor('Stickers', 500, [
        'quantity' => 50,
    ], [
        'tax_percent' => 21,
    ]);

> {note} The `invoiceFor` method will create a Stripe invoice which will retry failed billing attempts. If you do not want invoices to retry failed charges, you will need to close them using the Stripe API after the first failed charge.

<a name="refunding-charges"></a>
### Refunding Charges

If you need to refund a Stripe charge, you may use the `refund` method. This method accepts the Stripe Payment Intent ID as its first argument:

    $payment = $user->charge(100, $paymentMethod);

    $user->refund($payment->id);

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
            'vendor' => 'Your Company',
            'product' => 'Your Product',
        ]);
    });

<a name="strong-customer-authentication"></a>
## Strong Customer Authentication

If you have a business in Europe you should take into account Strong Customer Authentication (SCA). These regulations were imposed in September 2019 by the European Union to prevent payment fraud and require some extra setup. Luckily, Stripe and Cashier are fully ready for this and will help you tackle this with ease.

We recommend you review [Stripe's guide on PSD2 and SCA](https://stripe.com/en-be/guides/strong-customer-authentication) as well as [their docs on the new SCA API's](https://stripe.com/docs/strong-customer-authentication) before continuing.

<a name="handling-extra-payment-actions"></a>
### Handling Extra Payment Actions

One of the things SCA often requires is an extra verification action in order to verify a payment. When this happens, Cashier will throw an exception that informs you that this needed. You can do two things when that happens.

First, you could redirect your customer to a dedicated payment page which ships with Cashier. This page is already registered with a route through its service provider. Catch the thrown `IncompletePayment` exception and redirect like in the example below:

    use Laravel\Cashier\Exceptions\IncompletePayment;

    try {
        $subscription = $user->newSubscription('default', $planId)
            ->create($paymentMethod);
    } catch (IncompletePayment $exception) {
        return redirect()->route(
            'cashier.payment',
            [$exception->payment->id, 'redirect' => route('home')]
        );
    }

On this page, the customer will be prompted to enter their credit card info again and perform any extra actions that Stripe requires (like 3D Secure). After this is done, they'll be redirected to the page you've provided with the `redirect` parameter.

Secondly, you could opt to let Stripe handle this for you. In this case, instead of redirecting to the payment page, you can [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, you should still inform the user they will receive an email with further payment confirmation instructions.

Exceptions can be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on the `Billable` user. When handling subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Susbcription` model may throw exceptions. The payment page provided by Cashier offers an easy transition to handling these SCA requirements. 

#### Incomplete and Past Due State

As long as the payment wasn't verified, your subscription will remain in an `incomplete` or `past_due` state. This means it's not yet active until payment was fully completed with the extra action. Cashier will make automatically activate the customer's subscription through a webhook as soon as they've completed this extra action.

For more info on how to handle this, check [the above section](#incomplete-and-past-due-status).

<a name="off-session-payment-notification"></a>
### Off-session Payment Notification

Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a payment notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to its notification class. By default, this notification is disabled.

    CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment

This also gives you an easy way to swap out the notification class with a custom one if you want to configure more notification channels. [Make sure webhooks are set up](#handling-stripe-webhooks) for this and the `invoice.payment_action_required` webhook is configured in the Stripe dashboard.

> {note} One limitation of this is that notifications will be sent out even when customers are on-session during a payment that requires an extra action. This is because there's no way to know for Stripe that the payment was done on- or off-session. But a customer will never be charged twice and will simply see a "Payment Successful" message if they visit the payment page again.
