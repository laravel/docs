# Laravel Cashier for Mollie

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Plans and Coupons Configuration](#plans-and-coupons-configuration)
    - [Run Cashier](#run-cashier)
- [Subscriptions](#subscriptions)
	- [Creating Subscriptions](#creating-subscriptions)
	- [Coupons](#coupons)
	- [Checking Subscription Status](#checking-subscription-status)
	- [Changing Plans](#changing-plans)
	- [Subscription Quantity](#subscription-quantity)
	- [Subscription Taxes](#subscription-taxes)
	- [Prorating](#prorating)
	- [Subscription Anchor Date](#subscription-anchor-date)
	- [Cancelling Subscriptions](#cancelling-subscriptions)
	- [Resuming Subscriptions](#resuming-subscriptions)
- [Subscription Trials](#subscription-trials)
	- [With Mandate Up Front](#with-mandate-up-front)
	- [Without Mandate Up Front](#without-mandate-up-front)
- [One-off Charges](#one-off-charges)
- [Invoices](#invoices)
- [Customer Balance](#customer-balance)
- [Customer Locale](#customer-locale)
- [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
- [All Cashier Events](#all-cashier-events)
- [Customization](#customization)
	- [Metered Billing With Variable Amounts](#metered-billing-with-variable-amounts)
	- [Customizing The Coupon And Plan Repositories](#customizing-the-coupon-and-plan-repositories)
- [How Cashier Mollie works](#how-cashier-mollie-works)

<a name="introduction"></a>
## Introduction

Laravel Cashier Mollie provides an expressive, fluent interface to subscriptions using [Mollie](https://www.mollie.com)'s billing services.
It handles almost all of the boilerplate subscription billing code you are dreading writing.
In addition to basic subscription management, Cashier Mollie can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs.

<a name="installation"></a>
## Installation

You can pull this package in using composer:

	composer require laravel/cashier-mollie "^1.0"

Next, install the cashier migrations and configuration files:

	php artisan cashier:install

#### Database Migrations

Add these fields to your billable model's migration (typically the default "create_user_table" migration):

    $table->string('mollie_customer_id')->nullable();
    $table->string('mollie_mandate_id')->nullable();
    $table->decimal('tax_percentage', 6, 4)->default(0); // optional
    $table->dateTime('trial_ends_at')->nullable(); // optional
    $table->text('extra_billing_information')->nullable(); // optional

Now run the migrations:

	php artisan migrate

## Configuration

<a name="billable-model"></a>
### Billable Model

Before using Cashier, add the `Billable` trait to your model definition. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information.
Also, implement the `Laravel\Cashier\Order\Contracts\ProvidesInvoiceInformation` contract.

    use Laravel\Cashier\Billable;
    use Laravel\Cashier\Order\Contracts\ProvidesInvoiceInformation;

    class User extends Authenticatable implements ProvidesInvoiceInformation
    {
        use Billable;

        /**
            * Get the receiver information for the invoice.
            * Typically includes the name and some sort of (E-mail/physical) address.
            *
            * @return array An array of strings
            */
           public function getInvoiceInformation()
           {
               return [$this->name, $this->email];
           }

           /**
            * Get additional information to be displayed on the invoice. Typically a note provided by the customer.
            *
            * @return string|null
            */
           public function getExtraBillingInformation()
           {
               return null;
           }
    }

Optionally, override the `mollieCustomerFields()` method to configure what billable model fields are stored with Mollie while creating the Mollie Customer.
Out of the box the `mollieCustomerFields()` method uses the default Laravel User model fields:

    public function mollieCustomerFields() {
        return [
            'email' => $this->email,
            'name' => $this->name,
        ];
    }

> {tip} Learn more about storing data on the Mollie Customer [here](https://docs.mollie.com/reference/v2/customers-api/create-customer#parameters).

<a name="api-keys"></a>
### API Keys

Next, add the `MOLLIE_KEY` to your .env file. You can obtain an API key from the [Mollie dashboard](https://www.mollie.com/dashboard/developers/api-keys):

	MOLLIE_KEY="test_xxxxxxxxxxx"

<a name="plans-and-coupons-configuration"></a>
### Plans And Coupons Configuration

Now prepare the configuration files:

- configure at least one subscription plan in `config/cashier_plans.php`.

- in `config/cashier_coupons.php` you can manage any coupons. By default an example coupon is enabled. Consider
disabling it before deploying to production.

- the base configuration is in `config/cashier`. Be careful while modifying this, in most cases you will not need to.

<a name="run-cashier"></a>
### Run Cashier

Schedule a periodic job to execute `Cashier::run()`:

    $schedule->command('cashier:run')
        ->daily() // run as often as you like (Daily, monthly, every minute, ...)
        ->withoutOverlapping(); // make sure to include this

> {tip} You can find more about scheduling jobs using Laravel [here](https://laravel.com/docs/scheduling).

<a name="subscriptions"></a>
## Subscriptions

<a name="creating-subscriptions"></a>
### Creating Subscriptions

To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of
`App\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's
subscription:

	$user = User::find(1);
	// Make sure to configure the 'premium' plan in config/cashier_plans.php
	$result = $user->newSubscription('main', 'premium')->create();

If the customer already has a valid Mollie mandate, the `$result` will be a `Subscription`.

If the customer has no valid Mollie mandate yet, the `$result` will be a `RedirectToCheckoutResponse`, redirecting the
customer to the Mollie checkout to make the first payment. Once the payment has been received the subscription will
start.

Here's a basic controller example for creating the subscription:

	namespace App\Http\Controllers;

	use Laravel\Cashier\SubscriptionBuilder\RedirectToCheckoutResponse;
	use Illuminate\Support\Facades\Auth;

	class CreateSubscriptionController extends Controller
	{
		/**
		 * @param string $plan
		 * @return \Illuminate\Http\RedirectResponse
		 */
		public function __invoke(string $plan)
		{
			$user = Auth::user();

			$name = ucfirst($plan) . ' membership';

			if(!$user->subscribed($name, $plan)) {

				$result = $user->newSubscription($name, $plan)->create();

				if(is_a($result, RedirectToCheckoutResponse::class)) {
					return $result; // Redirect to Mollie checkout
				}

				return back()->with('status', 'Welcome to the ' . $plan . ' plan');
			}

			return back()->with('status', 'You are already on the ' . $plan . ' plan');
		}
	}

In order to always enforce a redirect to the Mollie checkout page and obtain a new mandate, use the `newSubscriptionViaMollieCheckout` method
instead of `newSubscription`:

    $redirect = $user->newSubscriptionViaMollieCheckout('main', 'premium')->create(); // make sure to configure the 'premium' plan in config/cashier.php

<a name="coupons"></a>
### Coupons

Coupon handling in Cashier Mollie is designed with full flexibility in mind.
Coupons can be defined and configured in `config/cashier_coupons.php`.

You can provide your own coupon handler by extending `\Cashier\Discount\BaseCouponHandler`.

Out of the box, a basic `FixedDiscountHandler` is provided.

#### Redeeming A Coupon For An Existing Subscription

For redeeming a coupon for an existing subscription, use the `redeemCoupon()` method on the billable trait:

    $user->redeemCoupon('your-coupon-code');

This will validate the coupon code and redeem it. The coupon will be applied to the upcoming Order.

Optionally, specify the subscription it should be applied to:

    $user->redeemCoupon('your-coupon-code', 'main');

By default all other active redeemed coupons for the subscription will be revoked. You can prevent this by setting the
`$revokeOtherCoupons` flag to false:

    $user->redeemCoupon('your-coupon-code', 'main', false);

<a name="checking-subscription-status"></a>
### Checking Subscription Status

Once a user is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the user has an active subscription, even if the subscription is currently within its trial period:

	if ($user->subscribed('main')) {
		//
	}

The `subscribed` method also makes a great candidate for a [route middleware](https://www.laravel.com/docs/middleware), allowing you to filter access to routes and controllers based on the user's subscription status:

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

The `subscribedToPlan` method may be used to determine if the user is subscribed to a given plan based on a configured plan. In this example, we will determine if the user's `main` subscription is actively subscribed to the `monthly` plan:

	if ($user->subscribedToPlan('monthly', 'main')) {
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

<a name="changing-plans"></a>
### Changing Plans

After a user is subscribed to your application, they may occasionally want to change to a new subscription plan. To swap a user to a new subscription, pass the plan's identifier to the `swap` or `swapNextCycle` method:

	$user = App\User::find(1);

	// Swap right now
	$user->subscription('main')->swap('other-plan-id');

	// Swap once the current cycle has completed
	$user->subscription('main')->swapNextCycle('other-plan-id');

If the user is on trial, the trial period will be maintained. Also, if a "quantity" exists for the subscription, that quantity will also be maintained.

<a name="subscription-quantity"></a>
### Subscription Quantity

Sometimes subscriptions are affected by "quantity". For example, your application might charge €10 per month **per user** on an account. To easily increment or decrement your subscription quantity, use the `incrementQuantity` and `decrementQuantity` methods:

	$user = User::find(1);

	$user->subscription('main')->incrementQuantity();

	// Add five to the subscription's current quantity...
	$user->subscription('main')->incrementQuantity(5);

	$user->subscription('main')->decrementQuantity();

	// Subtract five to the subscription's current quantity...
	$user->subscription('main')->decrementQuantity(5);

Alternatively, you may set a specific quantity using the `updateQuantity` method:

	$user->subscription('main')->updateQuantity(10);

<a name="subscription-taxes"></a>
### Subscription Taxes

To specify the tax percentage a user pays on a subscription, implement the `taxPercentage` method on your billable model, and return a numeric value between 0 and 100, with no more than 2 decimal places.

	public function taxPercentage() {
		return 20;
	}

The `taxPercentage` method enables you to apply a tax rate on a model-by-model basis, which may be helpful for a user base that spans multiple countries and tax rates.

#### Syncing Tax Percentages

When changing the hard-coded value returned by the `taxPercentage` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the returned `taxPercentage` value, you should call the `syncTaxPercentage` method on the user's subscription instance:

	$user->subscription('main')->syncTaxPercentage();

<a name="prorating"></a>
### Prorating

Cashier Mollie prorates all subscriptions, meaning that customers are billed at the start of each billing cycle.

When the subscription quantity is updated or the subscription is switched to another plan:

1. the billing cycle is reset
2. the customer is credited for unused time, meaning that the amount that was overpaid is added to the customer's balance.
3. a new billing cycle is started with the new subscription settings. An Order (and payment) is generated to deal with
all of the previous, including applying the credited balance to the Order.

This does not apply to the `$subscription->swapNextCycle('other-plan')`, which simply waits for the next billing cycle
to update the subscription plan. A common use case for this is downgrading the plan at the end of the billing cycle.

<a name="subscription-anchor-date"></a>
### Subscription anchor date
By default, the billing cycle anchor is the date the subscription was created, or if a trial period is used, the date that the trial ends.
Cashier Mollie does not support changing the anchored subscription date.
You may schedule `Cashier::run()` to only execute on a specific day of the month instead.

<a name="cancelling-subscriptions"></a>
### Cancelling Subscriptions

To cancel a subscription, call the `cancel` method on the user's subscription:

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

If the user cancels a subscription and then resumes that subscription before the subscription has fully expired, they will not be billed immediately. Instead, their subscription will be re-activated, and they will be billed on the original billing cycle.

<a name="subscription-trials"></a>
## Subscription Trials

<a name="with-mandate-upfront"></a>
### With Mandate Up Front

If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions:

	$user = User::find(1);

	$user->newSubscription('main', 'monthly')
				->trialDays(10)
				->create();

This method will set the trial period ending date on the subscription record within the database.

> {note} The customer will be redirected to the Mollie checkout page to make the first payment in order to register a mandate. You can modify the amount in the cashier config file.

> {note} If the customer's subscription is not cancelled before the trial ending date they will be charged as soon as the trial expires, so you should be sure to notify your users of their trial ending date.

The `trialUntil` method allows you to provide a `Carbon` instance to specify when the trial period should end:

	use Carbon\Carbon;

	$user->newSubscription('main', 'monthly')
				->trialUntil(Carbon::now()->addDays(10))
				->create();

You may determine if the user is within their trial period using either the `onTrial` method of the user instance, or the `onTrial` method of the subscription instance. The two examples below are identical:

	if ($user->onTrial('main')) {
		//
	}

	if ($user->subscription('main')->onTrial()) {
		//
	}

<a name="without-mandate-upfront"></a>
### Without Mandate Up Front

If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration:

	$user = User::create([
		// Populate other user properties...
		'trial_ends_at' => now()->addDays(10),
	]);

> {note}  Be sure to add a [date mutator](https://laravel.com/docs/eloquent-mutators#date-mutators) for `trial_ends_at` to your model definition.

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

	$user->newSubscription('main', 'monthly')->create();

<a name="one-off-charges"></a>
## One-off Charges

Cashier Mollie does not (yet) support one-off charges.

<a name="invoices"></a>
## Invoices

Listen for the `OrderInvoiceAvailable` event (in the `Laravel\Cashier\Events` namespace).
When a new order has been processed, you can grab the invoice by

	$invoice = $event->order->invoice();
	$invoice->view(); // get a Blade view
	$invoice->pdf(); // get a pdf of the Blade view
	$invoice->download(); // get a download response for the pdf

To list invoices, access the user's orders using: `$user->orders->invoices()`.
This includes invoices for all orders, even unprocessed or failed orders.

<a name="customer-balance"></a>
## Customer Balance

In some cases (i.e. when swapping to a cheaper plan), a customer can have overpaid. The amount that has been overpaid
will be added to the customer balance.

The customer balance is automatically processed in each Order.

A separate balance is kept for each currency.

There are a few methods available to interact with the balance directly.
__Use these with care:__

	$credit = $user->credit('EUR');
	$user->addCredit(new Amount(10, 'EUR'); // add €10.00
	$user->hasCredit('EUR');

When an Order with a negative total amount due is processed, that amount is credited to the user balance.
A `BalanceTurnedStale` event will be raised if the user has no active subscriptions at that moment.
Listen for this event if you'd like to refund the remaining balance and/or want to notify the user.

<a name="customer-locale"></a>
## Customer Locale

Mollie provides a checkout tailored to the customer's locale. For this it guesses the visitor's locale. To override the
default locale, configure it in `config/cashier.php`. This is convenient for servicing a single country.

If you're dealing with multiple locales and want to override Mollie's default behaviour, implement the `getLocale()`
method on the billable model. A common way is to add a nullable `locale` field to the user table and retrieve its value:

	class User extends Model
	{
		/**
		 * @return string
		 * @link https://docs.mollie.com/reference/v2/payments-api/create-payment#parameters
		 * @example 'nl_NL'
		 */
		public function getLocale() {
			return $this->locale;
		}
	}

<a name="defining-webhook-event-handlers"></a>
## Defining Webhook Event Handlers

Cashier automatically handles subscription cancellation on failed charges.

Additionally, listen for the following events (in the `Laravel\Cashier\Events` namespace) to add app specific behaviour:
- `OrderPaymentPaid` and `OrderPaymentFailed`
- `FirstPaymentPaid` and `FirstPaymentFailed`

<a name="all-cashier-events"></a>
## All Cashier Events

You can listen for the following events from the `Laravel\Cashier\Events` namespace:

#### `BalanceTurnedStale` event
The user has a positive account balance, but no active subscriptions. Consider a refund.

#### `CouponApplied` event
A coupon was applied to an OrderItem. Note the distinction between _redeeming_ a coupon and _applying_ a coupon. A
redeemed coupon can be applied to multiple orders. I.e. applying a 6 month discount on a monthly subscription using a
single (redeemed) coupon.

#### `FirstPaymentFailed` event
The first payment (used for obtaining a mandate) has failed.

#### `FirstPaymentPaid` event
The first payment (used for obtaining a mandate) was successful.

#### `MandateClearedFromBillable` event
The `mollie_mandate_id` was cleared on the billable model. This happens when a payment has failed because of a invalid
mandate.

#### `MandateUpdated` event
The billable model's mandate was updated. This usually means a new payment card was registered.

#### `OrderCreated` event
An Order was created.

#### `OrderInvoiceAvailable` event
An Invoice is available on the Order. Access it using `$event->order->invoice()`.

#### `OrderPaymentFailed` event
The payment for an order has failed.

#### `OrderPaymentPaid` event
The payment for an order was successful.

#### `OrderProcessed` event
The order has been fully processed.

#### `SubscriptionStarted` event
A new subscription was started.

#### `SubscriptionCancelled` event
The subscription was cancelled.

#### `SubscriptionResumed` event
The subscription was resumed.

#### `SubscriptionPlanSwapped` event
The subscription plan was swapped.

#### `SubscriptionQuantityUpdated` event
The subscription quantity was updated.

<a name="customization"></a>
## Customization

<a name="metered-billing-with-variable-amounts"></a>
### Metered Billing With Variable Amounts

Some business cases will require dynamic subscription amounts.

To allow for full flexibility Cashier Mollie allows you to define your own set of Subscription OrderItem preprocessors.
These preprocessors are invoked when the OrderItem is due, right before being processed into a Mollie payment.

If you're using metered billing, this is a convenient place to calculate the amount based on the usage statistics and
reset any counters for the next billing cycle.

You can define the preprocessors in the `cashier_plans` config file.

<a name="customizing-the-coupon-and-plan-repositories"></a>
### Customizing The Coupon And Plan Repositories

Plans and coupons are managed in the `cashier_plans` and `cashier_coupons` configuration files by default.
For advanced use cases it may be necessary to keep these in the database instead. You can do so by implementing the following contracts:

- `Laravel\Cashier\Plan\Contracts\PlanRepository`
- `Laravel\Cashier\Coupon\Contracts\CouponRepository`

Then, bind your own implementation into the service container:

	class AppServiceProvider extends ServiceProvider
	{
		public function register()
		{
			$this->app->bind(\Laravel\Cashier\Plan\Contracts\PlanRepository::class, MyDatabasePlanRepository::class);
			$this->app->bind(\Laravel\Cashier\Coupon\Contracts\CouponRepository::class, MyDatabaseCouponRepository::class);
		}
	}

<a name="how-cashier-mollie-works"></a>
## How Cashier Mollie works

Cashier Mollie is designed for full flexibility and tight integration with your application.
Therefore Cashier Mollie schedules mandated Mollie payments from the client side, instead of relying on a remote subscription management service.

From a high level perspective, this is what the process looks like:

1. A `Subscription` is created using the `FirstPaymentSubscriptionBuilder` (redirecting to Mollie's checkout to create
a `Mandate`) or `MandatedSubscriptionBuilder` (using an existing `Mandate`).
2. The `Subscription` yields a scheduled `OrderItem` at the beginning of each billing cycle.
3. `OrderItems` which are due are preprocessed and bundled into `Orders` whenever possible by a scheduled job (i.e.
daily). This is done so your customer will receive a single payment/invoice for multiple items later on in the chain.
Preprocessing the `OrderItems` may involve applying dynamic discounts or metered billing, depending on your
configuration.
4. The `Order` is processed by the same scheduled job into a payment:
    - First, (if available) the customer's balance is processed in the `Order`.
    - If the total due is positive, a Mollie payment is incurred.
    - If the total due is 0, nothing happens.
    - If the total due is negative, the amount is added to the user's balance. If the user has no active subscriptions left, the `BalanceTurnedStale` event will be raised.
5. You can generate an `Invoice` (html/pdf) for the user.