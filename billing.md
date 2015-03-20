# Laravel Cashier

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Subscribing To A Plan](#subscribing-to-a-plan)
- [No Card Up Front](#no-card-up-front)
- [Swapping Subscriptions](#swapping-subscriptions)
- [Subscription Quantity](#subscription-quantity)
- [Cancelling A Subscription](#cancelling-a-subscription)
- [Resuming A Subscription](#resuming-a-subscription)
- [Checking Subscription Status](#checking-subscription-status)
- [Handling Failed Payments](#handling-failed-payments)
- [Handling Other Stripe Webhooks](#handling-other-stripe-webhooks)
- [Invoices](#invoices)

<a name="introduction"></a>
## Introduction

Laravel Cashier provides an expressive, fluent interface to [Stripe's](https://stripe.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs.

<a name="configuration"></a>
## Configuration

#### Composer

First, add the Cashier package to your `composer.json` file:

	"laravel/cashier": "~2.0"

#### Service Provider

Next, register the `Laravel\Cashier\CashierServiceProvider` in your `app` configuration file.

#### Migration

Before using Cashier, we'll need to add several columns to your database. Don't worry, you can use the `cashier:table` Artisan command to create a migration to add the necessary column. For example, to add the column to the users table use `php artisan cashier:table users`. Once the migration has been created, simply run the `migrate` command.

#### Model Setup

Next, add the BillableTrait and appropriate date mutators to your model definition:

	use Laravel\Cashier\BillableTrait;
	use Laravel\Cashier\BillableInterface;

	class User extends Eloquent implements BillableInterface {

		use BillableTrait;

		protected $dates = ['trial_ends_at', 'subscription_ends_at'];

	}

#### Stripe Key

Finally, set your Stripe key in one of your bootstrap files:

	User::setStripeKey('stripe-key');

<a name="subscribing-to-a-plan"></a>
## Subscribing To A Plan

Once you have a model instance, you can easily subscribe that user to a given Stripe plan:

	$user = User::find(1);

	$user->subscription('monthly')->create($creditCardToken);

If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method:

	$user->subscription('monthly')
	     ->withCoupon('code')
	     ->create($creditCardToken);

The `subscription` method will automatically create the Stripe subscription, as well as update your database with Stripe customer ID and other relevant billing information. If your plan has a trial configured in Stripe, the trial end date will also automatically be set on the user record.

If your plan has a trial period that is **not** configured in Stripe, you must set the trial end date manually after subscribing:

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

### Specifying Additional User Details

If you would like to specify additional customer details, you may do so by passing them as second argument to the `create` method:

	$user->subscription('monthly')->create($creditCardToken, [
		'email' => $email, 'description' => 'Our First Customer'
	]);

To learn more about the additional fields supported by Stripe, check out Stripe's [documentation on customer creation](https://stripe.com/docs/api#create_customer).

<a name="no-card-up-front"></a>
## No Card Up Front

If your application offers a free-trial with no credit-card up front, set the `cardUpFront` property on your model to `false`:

	protected $cardUpFront = false;

On account creation, be sure to set the trial end date on the model:

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

<a name="swapping-subscriptions"></a>
## Swapping Subscriptions

To swap a user to a new subscription, use the `swap` method:

	$user->subscription('premium')->swap();

If the user is on trial, the trial will be maintained as normal. Also, if a "quantity" exists for the subscription, that quantity will also be maintained.

<a name="subscription-quantity"></a>
## Subscription Quantity

Sometimes subscriptions are affected by "quantity". For example, your application might charge $10 per month per user on an account. To easily increment or decrement your subscription quantity, use the `increment` and `decrement` methods:

	$user = User::find(1);

	$user->subscription()->increment();

	// Add five to the subscription's current quantity...
	$user->subscription()->increment(5);

	$user->subscription()->decrement();

	// Subtract five to the subscription's current quantity...
	$user->subscription()->decrement(5);

<a name="cancelling-a-subscription"></a>
## Cancelling A Subscription

Cancelling a subscription is a walk in the park:

	$user->subscription()->cancel();

When a subscription is cancelled, Cashier will automatically set the `subscription_ends_at` column on your database. This column is used to know when the `subscribed` method should begin returning `false`. For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th.

<a name="resuming-a-subscription"></a>
## Resuming A Subscription

If a user has cancelled their subscription and you wish to resume it, use the `resume` method:

	$user->subscription('monthly')->resume($creditCardToken);

If the user cancels a subscription and then resumes that subscription before the subscription has fully expired, they will not be billed immediately. Their subscription will simply be re-activated, and they will be billed on the original billing cycle.

<a name="checking-subscription-status"></a>
## Checking Subscription Status

To verify that a user is subscribed to your application, use the `subscribed` command:

	if ($user->subscribed())
	{
		//
	}

The `subscribed` method makes a great candidate for a route filter:

	Route::filter('subscribed', function()
	{
		if (Auth::user() && ! Auth::user()->subscribed())
		{
			return Redirect::to('billing');
		}
	});

You may also determine if the user is still within their trial period (if applicable) using the `onTrial` method:

	if ($user->onTrial())
	{
		//
	}

To determine if the user was once an active subscriber, but has cancelled their subscription, you may use the `cancelled` method:

	if ($user->cancelled())
	{
		//
	}

You may also determine if a user has cancelled their subscription, but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was scheduled to end on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time.

	if ($user->onGracePeriod())
	{
		//
	}

The `everSubscribed` method may be used to determine if the user has ever subscribed to a plan in your application:

	if ($user->everSubscribed())
	{
		//
	}

The `onPlan` method may be used to determine if the user is subscribed to a given plan based on its ID:

	if ($user->onPlan('monthly'))
	{
		//
	}

<a name="handling-failed-payments"></a>
## Handling Failed Payments

What if a customer's credit card expires? No worries - Cashier includes a Webhook controller that can easily cancel the customer's subscription for you. Just point a route to the controller:

	Route::post('stripe/webhook', 'Laravel\Cashier\WebhookController@handleWebhook');

That's it! Failed payments will be captured and handled by the controller. The controller will cancel the customer's subscription after three failed payment attempts. The `stripe/webhook` URI in this example is just for example. You will need to configure the URI in your Stripe settings.

<a name="handling-other-stripe-webhooks"></a>
## Handling Other Stripe Webhooks

If you have additional Stripe webhook events you would like to handle, simply extend the Webhook controller. Your method names should correspond to Cashier's expected convention, specifically, methods should be prefixed with `handle` and the name of the Stripe webhook you wish to handle. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you should add a `handleInvoicePaymentSucceeded` method to the controller.

	class WebhookController extends Laravel\Cashier\WebhookController {

		public function handleInvoicePaymentSucceeded($payload)
		{
			// Handle The Event
		}

	}

> **Note:** In addition to updating the subscription information in your database, the Webhook controller will also cancel the subscription via the Stripe API.

<a name="invoices"></a>
## Invoices

You can easily retrieve an array of a user's invoices using the `invoices` method:

	$invoices = $user->invoices();

When listing the invoices for the customer, you may use these helper methods to display the relevant invoice information:

	{{ $invoice->id }}

	{{ $invoice->dateString() }}

	{{ $invoice->dollars() }}

Use the `downloadInvoice` method to generate a PDF download of the invoice. Yes, it's really this easy:

	return $user->downloadInvoice($invoice->id, [
		'vendor'  => 'Your Company',
		'product' => 'Your Product',
	]);
