# Laravel Cashier

- [Introduction](#introduction)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Changing Plans](#changing-plans)
    - [Subscription Quantity](#subscription-quantity)
    - [Subscription Taxes](#subscription-taxes)
    - [Cancelling Subscriptions](#cancelling-subscriptions)
    - [Resuming Subscriptions](#resuming-subscriptions)
- [Handling Stripe Webhooks](#handling-stripe-webhooks)
    - [Failed Subscriptions](#handling-failed-subscriptions)
    - [Other Webhooks](#handling-other-webhooks)
- [Single Charges](#single-charges)
- [Invoices](#invoices)
    - [Generating Invoice PDFs](#generating-invoice-pdfs)

<a name="introduction"></a>
## Introduction

Laravel Cashier provides an expressive, fluent interface to [Stripe's](https://stripe.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs.

<a name="configuration"></a>
### Configuration

#### Composer

First, add the Cashier package to your `composer.json` file and run the `composer update` command:

    "laravel/cashier": "~6.0"

#### Service Provider

Next, register the `Laravel\Cashier\CashierServiceProvider` [service provider](/docs/{{version}}/providers) in your `app` configuration file.

#### Migration

Before using Cashier, we'll need to prepare the database. We need to add several columns to your `users` table and create a new `subscriptions` table to hold all of our customer's subscriptions:

    Schema::table('users', function ($table) {
        $table->string('stripe_id')->nullable();
        $table->string('card_brand')->nullable();
        $table->string('card_last_four')->nullable();
    });

    Schema::create('subscriptions', function ($table) {
        $table->increments('id');
        $table->integer('user_id');
        $table->string('name');
        $table->string('stripe_id');
        $table->string('stripe_plan');
        $table->integer('quantity');
        $table->timestamp('trial_ends_at')->nullable();
        $table->timestamp('ends_at')->nullable();
        $table->timestamps();
    });

Once the migrations have been created, simply run the `migrate` command.

#### Model Setup

Next, add the `Billable` trait to your model definition:

    use Laravel\Cashier\Billable;

    class User extends Authenticatable
    {
        use Billable;
    }

#### Stripe Key

Finally, set your Stripe key in your `services.php` configuration file:

    'stripe' => [
        'model'  => App\User::class,
        'secret' => env('STRIPE_API_SECRET'),
    ],

<a name="subscriptions"></a>
## Subscriptions

<a name="creating-subscriptions"></a>
### Creating Subscriptions

To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription:

    $user = User::find(1);

    $user->newSubscription('main', 'monthly')->create($creditCardToken);

The first argument passed to the `newSubscription` method should be the name of the subscription. If your application only offers a single subscription, you might call this `main` or `primary`. The second argument is the specific Stripe plan the user is subscribing to. This value should correspond to the plan's identifier in Stripe.

The `create` method will automatically create the Stripe subscription, as well as update your database with Stripe customer ID and other relevant billing information. If your plan has a trial configured in Stripe, the trial end date will also automatically be set on the user record.

#### Additional User Details

If you would like to specify additional customer details, you may do so by passing them as the second argument to the `create` method:

    $user->newSubscription('main', 'monthly')->create($creditCardToken, [
        'email' => $email, 'description' => 'Our First Customer'
    ]);

To learn more about the additional fields supported by Stripe, check out Stripe's [documentation on customer creation](https://stripe.com/docs/api#create_customer).

#### Coupons

If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method:

    $user->newSubscription('main', 'monthly')
         ->withCoupon('code')
         ->create($creditCardToken);

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

The `onPlan` method may be used to determine if the user is subscribed to a given plan based on its Stripe ID:

    if ($user->onPlan('monthly')) {
        //
    }

#### Cancelled Subscription Status

To determine if the user was once an active subscriber, but has cancelled their subscription, you may use the `cancelled` method:

    if ($user->subscription('main')->cancelled()) {
        //
    }

You may also determine if a user has cancelled their subscription, but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time.

    if ($user->subscription('main')->onGracePeriod()) {
        //
    }

<a name="changing-plans"></a>
### Changing Plans

After a user is subscribed to your application, they may occasionally want to change to a new subscription plan. To swap a user to a new subscription, use the `swap` method. For example, we may easily switch a user to the `premium` subscription:

    $user = App\User::find(1);

    $user->subscription('main')->swap('stripe-plan-id');

If the user is on trial, the trial period will be maintained. Also, if a "quantity" exists for the subscription, that quantity will also be maintained. If you would like to invoice the customer immediately after swapping plans, use the `invoice` method:

    $user->subscription('main')->swap('stripe-plan-id');

    $user->invoice();

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

For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/guides/subscriptions#setting-quantities).

<a name="subscription-taxes"></a>
### Subscription Taxes

With Cashier, it's easy to provide the `tax_percent` value sent to Stripe. To specify the tax percentage a user pays on a subscription, implement the `taxPercentage` method on your billable model, and return a numeric value between 0 and 100, with no more than 2 decimal places.

    public function taxPercentage() {
        return 20;
    }

This enables you to apply a tax rate on a model-by-model basis, which may be helpful for a user base that spans multiple countries.

<a name="cancelling-subscriptions"></a>
### Cancelling Subscriptions

To cancel a subscription, simply call the `cancel` method on the user's subscription:

    $user->subscription('main')->cancel();

When a subscription is cancelled, Cashier will automatically set the `ends_at` column in your database. This column is used to know when the `subscribed` method should begin returning `false`. For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th.

You may determine if a user has cancelled their subscription but are still on their "grace period" using the `onGracePeriod` method:

    if ($user->subscription('main')->onGracePeriod()) {
        //
    }

<a name="resuming-subscriptions"></a>
### Resuming Subscriptions

If a user has cancelled their subscription and you wish to resume it, use the `resume` method. The user **must** still be on their grace period in order to resume a subscription:

    $user->subscription('main')->resume();

If the user cancels a subscription and then resumes that subscription before the subscription has fully expired, they will not be billed immediately. Instead, their subscription will simply be re-activated, and they will be billed on the original billing cycle.

<a name="handling-stripe-webhooks"></a>
## Handling Stripe Webhooks

<a name="handling-failed-subscriptions"></a>
### Failed Subscriptions

What if a customer's credit card expires? No worries - Cashier includes a Webhook controller that can easily cancel the customer's subscription for you. Just point a route to the controller:

    Route::post(
        'stripe/webhook',
        '\Laravel\Cashier\Http\Controllers\WebhookController@handleWebhook'
    );

That's it! Failed payments will be captured and handled by the controller. The controller will cancel the customer's subscription when Stripe determines the subscription has failed (normally after three failed payment attempts). Don't forget: you will need to configure the webhook URI in your Stripe control panel settings.

Since Stripe webhooks need to bypass Laravel's [CSRF verification](/docs/{{version}}/routing#csrf-protection), be sure to list the URI as an exception in your `VerifyCsrfToken` middleware:

    protected $except = [
        'stripe/*',
    ];

<a name="handling-other-webhooks"></a>
### Other Webhooks

If you have additional Stripe webhook events you would like to handle, simply extend the Webhook controller. Your method names should correspond to Cashier's expected convention, specifically, methods should be prefixed with `handle` and the "camel case" name of the Stripe webhook you wish to handle. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you should add a `handleInvoicePaymentSucceeded` method to the controller.

    <?php

    namespace App\Http\Controllers;

    use Laravel\Cashier\Http\Controllers\WebhookController as BaseController;

    class WebhookController extends BaseController
    {
        /**
         * Handle a stripe webhook.
         *
         * @param  array  $payload
         * @return Response
         */
        public function handleInvoicePaymentSucceeded($payload)
        {
            // Handle The Event
        }
    }

<a name="single-charges"></a>
## Single Charges

### Simple Charge

If you would like to make a "one off" charge against a subscribed customer's credit card, you may use the `charge` method on a billable model instance. The `charge` method accepts the amount you would like to charge in the **lowest denominator of the currency used by your application**. So, for example, the example below will charge 100 cents, or $1.00, against the user's credit card:

    $user->charge(100);

The `charge` method accepts an array as its second argument, allowing you to pass any options you wish to the underlying Stripe charge creation:

    $user->charge(100, [
        'source' => $token,
        'receipt_email' => $user->email,
    ]);

The `charge` method will return `false` if the charge fails. This typically indicates the charge was denied:

    if ( ! $user->charge(100)) {
        // The charge was denied...
    }

If the charge is successful, the full Stripe response will be returned from the method.

### Charge With Invoice

Sometimes you may need to make a one-time charge but also generate an invoice for the charge so that you may offer a PDF receipt to your customer. The `invoiceFor` method lets you do just that. For example, let's invoice the customer $5.00 for a "One Time Fee":

    $user->invoiceFor('One Time Fee', 500);

The invoice will be charged immediately against the user's credit card. The `invoiceFor` method also accepts an array as its third argument, allowing you to pass any options you wish to the underlying Stripe invoice item creation:

    $user->invoiceFor('One Time Fee', 500, [
        'discountable' => false,
    ]);

<a name="invoices"></a>
## Invoices

You may easily retrieve an array of a billable model's invoices using the `invoices` method:

    $invoices = $user->invoices();

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
#### Generating Invoice PDFs

Before generating invoice PDFs, you need to install the `dompdf` PHP library:

    composer require dompdf/dompdf

From within a route or controller, use the `downloadInvoice` method to generate a PDF download of the invoice. This method will automatically generate the proper HTTP response to send the download to the browser:

    Route::get('user/invoice/{invoice}', function ($invoiceId) {
        return Auth::user()->downloadInvoice($invoiceId, [
            'vendor'  => 'Your Company',
            'product' => 'Your Product',
        ]);
    });
