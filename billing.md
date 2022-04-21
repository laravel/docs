# Laravel Cashier (Stripe)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
    - [Database Migrations](#database-migrations)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Currency Configuration](#currency-configuration)
    - [Tax Configuration](#tax-configuration)
    - [Logging](#logging)
    - [Using Custom Models](#using-custom-models)
- [Customers](#customers)
    - [Retrieving Customers](#retrieving-customers)
    - [Creating Customers](#creating-customers)
    - [Updating Customers](#updating-customers)
    - [Balances](#balances)
    - [Tax IDs](#tax-ids)
    - [Syncing Customer Data With Stripe](#syncing-customer-data-with-stripe)
    - [Billing Portal](#billing-portal)
- [Payment Methods](#payment-methods)
    - [Storing Payment Methods](#storing-payment-methods)
    - [Retrieving Payment Methods](#retrieving-payment-methods)
    - [Determining If A User Has A Payment Method](#check-for-a-payment-method)
    - [Updating The Default Payment Method](#updating-the-default-payment-method)
    - [Adding Payment Methods](#adding-payment-methods)
    - [Deleting Payment Methods](#deleting-payment-methods)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Changing Prices](#changing-prices)
    - [Subscription Quantity](#subscription-quantity)
    - [Multiprice Subscriptions](#multiprice-subscriptions)
    - [Metered Billing](#metered-billing)
    - [Subscription Taxes](#subscription-taxes)
    - [Subscription Anchor Date](#subscription-anchor-date)
    - [Canceling Subscriptions](#cancelling-subscriptions)
    - [Resuming Subscriptions](#resuming-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Payment Method Up Front](#with-payment-method-up-front)
    - [Without Payment Method Up Front](#without-payment-method-up-front)
    - [Extending Trials](#extending-trials)
- [Handling Stripe Webhooks](#handling-stripe-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
    - [Creating Payments](#creating-payments)
    - [Simple Charge](#simple-charge)
    - [Charge With Invoice](#charge-with-invoice)
    - [Refunding Charges](#refunding-charges)
- [Checkout](#checkout)
    - [Product Checkouts](#product-checkouts)
    - [Single Charge Checkouts](#single-charge-checkouts)
    - [Subscription Checkouts](#subscription-checkouts)
    - [Collecting Tax IDs](#collecting-tax-ids)
- [Invoices](#invoices)
    - [Retrieving Invoices](#retrieving-invoices)
    - [Upcoming Invoices](#upcoming-invoices)
    - [Previewing Subscription Invoices](#previewing-subscription-invoices)
    - [Generating Invoice PDFs](#generating-invoice-pdfs)
- [Handling Failed Payments](#handling-failed-payments)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [Payments Requiring Additional Confirmation](#payments-requiring-additional-confirmation)
    - [Off-session Payment Notifications](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [Testing](#testing)

<a name="introduction"></a>
## Introduction

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe) provides an expressive, fluent interface to [Stripe's](https://stripe.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading writing. In addition to basic subscription management, Cashier can handle coupons, swapping subscription, subscription "quantities", cancellation grace periods, and even generate invoice PDFs.

<a name="upgrading-cashier"></a>
## Upgrading Cashier

When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-stripe/blob/master/UPGRADE.md).

> {note} To prevent breaking changes, Cashier uses a fixed Stripe API version. Cashier 13 utilizes Stripe API version `2020-08-27`. The Stripe API version will be updated on minor releases in order to make use of new Stripe features and improvements.

<a name="installation"></a>
## Installation

First, install the Cashier package for Stripe using the Composer package manager:

```shell
composer require laravel/cashier
```

> {note} To ensure Cashier properly handles all Stripe events, remember to [set up Cashier's webhook handling](#handling-stripe-webhooks).

<a name="database-migrations"></a>
### Database Migrations

Cashier's service provider registers its own database migration directory, so remember to migrate your database after installing the package. The Cashier migrations will add several columns to your `users` table as well as create a new `subscriptions` table to hold all of your customer's subscriptions:

```shell
php artisan migrate
```

If you need to overwrite the migrations that ship with Cashier, you can publish them using the `vendor:publish` Artisan command:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```

If you would like to prevent Cashier's migrations from running entirely, you may use the `ignoreMigrations` method provided by Cashier. Typically, this method should be called in the `register` method of your `AppServiceProvider`:

    use Laravel\Cashier\Cashier;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        Cashier::ignoreMigrations();
    }

> {note} Stripe recommends that any column used for storing Stripe identifiers should be case-sensitive. Therefore, you should ensure the column collation for the `stripe_id` column is set to `utf8_bin` when using MySQL. More information regarding this can be found in the [Stripe documentation](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible).

<a name="configuration"></a>
## Configuration

<a name="billable-model"></a>
### Billable Model

Before using Cashier, add the `Billable` trait to your billable model definition. Typically, this will be the `App\Models\User` model. This trait provides various methods to allow you to perform common billing tasks, such as creating subscriptions, applying coupons, and updating payment method information:

    use Laravel\Cashier\Billable;

    class User extends Authenticatable
    {
        use Billable;
    }

Cashier assumes your billable model will be the `App\Models\User` class that ships with Laravel. If you wish to change this you may specify a different model via the `useCustomerModel` method. This method should typically be called in the `boot` method of your `AppServiceProvider` class:

    use App\Models\Cashier\User;
    use Laravel\Cashier\Cashier;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Cashier::useCustomerModel(User::class);
    }

> {note} If you're using a model other than Laravel's supplied `App\Models\User` model, you'll need to publish and alter the [Cashier migrations](#installation) provided to match your alternative model's table name.

<a name="api-keys"></a>
### API Keys

Next, you should configure your Stripe API keys in your application's `.env` file. You can retrieve your Stripe API keys from the Stripe control panel:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
```

<a name="currency-configuration"></a>
### Currency Configuration

The default Cashier currency is United States Dollars (USD). You can change the default currency by setting the `CASHIER_CURRENCY` environment variable within your application's `.env` file:

```ini
CASHIER_CURRENCY=eur
```

In addition to configuring Cashier's currency, you may also specify a locale to be used when formatting money values for display on invoices. Internally, Cashier utilizes [PHP's `NumberFormatter` class](https://www.php.net/manual/en/class.numberformatter.php) to set the currency locale:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```

> {note} In order to use locales other than `en`, ensure the `ext-intl` PHP extension is installed and configured on your server.

<a name="tax-configuration"></a>
### Tax Configuration

Thanks to [Stripe Tax](https://stripe.com/tax), it's possible to automatically calculate taxes for all invoices generated by Stripe. You can enable automatic tax calculation by invoking the `calculateTaxes` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

    use Laravel\Cashier\Cashier;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Cashier::calculateTaxes();
    }

Once tax calculation has been enabled, any new subscriptions and any one-off invoices that are generated will receive automatic tax calculation.

For this feature to work properly, your customer's billing details, such as the customer's name, address, and tax ID, need to be synced to Stripe. You may use the [customer data synchronization](#syncing-customer-data-with-stripe) and [Tax ID](#tax-ids) methods offered by Cashier to accomplish this.

> {note} Unfortunately, for now, no tax is calculated for [single charges](#single-charges) or [single charge checkouts](#single-charge-checkouts). In addition, Stripe Tax is currently "invite-only" during its beta period. You can request access to Stripe Tax via the [Stripe Tax website](https://stripe.com/tax#request-access).

<a name="logging"></a>
### Logging

Cashier allows you to specify the log channel to be used when logging fatal Stripe errors. You may specify the log channel by defining the `CASHIER_LOGGER` environment variable within your application's `.env` file:

```ini
CASHIER_LOGGER=stack
```

Exceptions that are generated by API calls to Stripe will be logged through your application's default log channel.

<a name="using-custom-models"></a>
### Using Custom Models

You are free to extend the models used internally by Cashier by defining your own model and extending the corresponding Cashier model:

    use Laravel\Cashier\Subscription as CashierSubscription;

    class Subscription extends CashierSubscription
    {
        // ...
    }

After defining your model, you may instruct Cashier to use your custom model via the `Laravel\Cashier\Cashier` class. Typically, you should inform Cashier about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class:

    use App\Models\Cashier\Subscription;
    use App\Models\Cashier\SubscriptionItem;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Cashier::useSubscriptionModel(Subscription::class);
        Cashier::useSubscriptionItemModel(SubscriptionItem::class);
    }

<a name="customers"></a>
## Customers

<a name="retrieving-customers"></a>
### Retrieving Customers

You can retrieve a customer by their Stripe ID using the `Cashier::findBillable` method. This method will return an instance of the billable model:

    use Laravel\Cashier\Cashier;

    $user = Cashier::findBillable($stripeId);

<a name="creating-customers"></a>
### Creating Customers

Occasionally, you may wish to create a Stripe customer without beginning a subscription. You may accomplish this using the `createAsStripeCustomer` method:

    $stripeCustomer = $user->createAsStripeCustomer();

Once the customer has been created in Stripe, you may begin a subscription at a later date. You may provide an optional `$options` array to pass in any additional [customer creation parameters that are supported by the Stripe API](https://stripe.com/docs/api/customers/create):

    $stripeCustomer = $user->createAsStripeCustomer($options);

You may use the `asStripeCustomer` method if you want to return the Stripe customer object for a billable model:

    $stripeCustomer = $user->asStripeCustomer();

The `createOrGetStripeCustomer` method may be used if you would like to retrieve the Stripe customer object for a given billable model but are not sure whether the billable model is already a customer within Stripe. This method will create a new customer in Stripe if one does not already exist:

    $stripeCustomer = $user->createOrGetStripeCustomer();

<a name="updating-customers"></a>
### Updating Customers

Occasionally, you may wish to update the Stripe customer directly with additional information. You may accomplish this using the `updateStripeCustomer` method. This method accepts an array of [customer update options supported by the Stripe API](https://stripe.com/docs/api/customers/update):

    $stripeCustomer = $user->updateStripeCustomer($options);

<a name="balances"></a>
### Balances

Stripe allows you to credit or debit a customer's "balance". Later, this balance will be credited or debited on new invoices. To check the customer's total balance you may use the `balance` method that is available on your billable model. The `balance` method will return a formatted string representation of the balance in the customer's currency:

    $balance = $user->balance();

To credit a customer's balance, you may provide a negative value to the `applyBalance` method. If you wish, you may also provide a description:

    $user->applyBalance(-500, 'Premium customer top-up.');

Providing a positive value to the `applyBalance` method will debit the customer's balance:

    $user->applyBalance(300, 'Bad usage penalty.');

The `applyBalance` method will create new customer balance transactions for the customer. You may retrieve these transaction records using the `balanceTransactions` method, which may be useful in order to provide a log of credits and debits for the customer to review:

    // Retrieve all transactions...
    $transactions = $user->balanceTransactions();

    foreach ($transactions as $transaction) {
        // Transaction amount...
        $amount = $transaction->amount(); // $2.31

        // Retrieve the related invoice when available...
        $invoice = $transaction->invoice();
    }

<a name="tax-ids"></a>
### Tax IDs

Cashier offers an easy way to manage a customer's tax IDs. For example, the `taxIds` method may be used to retrieve all of the [tax IDs](https://stripe.com/docs/api/customer_tax_ids/object) that are assigned to a customer as a collection:

    $taxIds = $user->taxIds();

You can also retrieve a specific tax ID for a customer by its identifier:

    $taxId = $user->findTaxId('txi_belgium');

You may create a new Tax ID by providing a valid [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type) and value to the `createTaxId` method:

    $taxId = $user->createTaxId('eu_vat', 'BE0123456789');

The `createTaxId` method will immediately add the VAT ID to the customer's account. [Verification of VAT IDs is also done by Stripe](https://stripe.com/docs/invoicing/customer/tax-ids#validation); however, this is an asynchronous process. You can be notified of verification updates by subscribing to the `customer.tax_id.updated` webhook event and inspecting [the VAT IDs `verification` parameter](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification). For more information on handling webhooks, please consult the [documentation on defining webhook handlers](#handling-stripe-webhooks).

You may delete a tax ID using the `deleteTaxId` method:

    $user->deleteTaxId('txi_belgium');

<a name="syncing-customer-data-with-stripe"></a>
### Syncing Customer Data With Stripe

Typically, when your application's users update their name, email address, or other information that is also stored by Stripe, you should inform Stripe of the updates. By doing so, Stripe's copy of the information will be in sync with your application's.

To automate this, you may define an event listener on your billable model that reacts to the model's `updated` event. Then, within your event listener, you may invoke the `syncStripeCustomerDetails` method on the model:

    use function Illuminate\Events\queueable;

    /**
     * The "booted" method of the model.
     *
     * @return void
     */
    protected static function booted()
    {
        static::updated(queueable(function ($customer) {
            if ($customer->hasStripeId()) {
                $customer->syncStripeCustomerDetails();
            }
        }));
    }

Now, every time your customer model is updated, its information will be synced with Stripe. For convenience, Cashier will automatically sync your customer's information with Stripe on the initial creation of the customer.

You may customize the columns used for syncing customer information to Stripe by overriding a variety of methods provided by Cashier. For example, you may override the `stripeName` method to customize the attribute that should be considered the customer's "name" when Cashier syncs customer information to Stripe:

    /**
     * Get the customer name that should be synced to Stripe.
     *
     * @return string|null
     */
    public function stripeName()
    {
        return $this->company_name;
    }

Similarly, you may override the `stripeEmail`, `stripePhone`, and `stripeAddress` methods. These methods will sync information to their corresponding customer parameters when [updating the Stripe customer object](https://stripe.com/docs/api/customers/update). If you wish to take total control over the customer information sync process, you may override the `syncStripeCustomerDetails` method.

<a name="billing-portal"></a>
### Billing Portal

Stripe offers [an easy way to set up a billing portal](https://stripe.com/docs/billing/subscriptions/customer-portal) so that your customer can manage their subscription, payment methods, and view their billing history. You can redirect your users to the billing portal by invoking the `redirectToBillingPortal` method on the billable model from a controller or route:

    use Illuminate\Http\Request;

    Route::get('/billing-portal', function (Request $request) {
        return $request->user()->redirectToBillingPortal();
    });

By default, when the user is finished managing their subscription, they will be able to return to the `home` route of your application via a link within the Stripe billing portal. You may provide a custom URL that the user should return to by passing the URL as an argument to the `redirectToBillingPortal` method:

    use Illuminate\Http\Request;

    Route::get('/billing-portal', function (Request $request) {
        return $request->user()->redirectToBillingPortal(route('billing'));
    });

If you would like to generate the URL to the billing portal without generating an HTTP redirect response, you may invoke the `billingPortalUrl` method:

    $url = $request->user()->billingPortalUrl(route('billing'));

<a name="payment-methods"></a>
## Payment Methods

<a name="storing-payment-methods"></a>
### Storing Payment Methods

In order to create subscriptions or perform "one off" charges with Stripe, you will need to store a payment method and retrieve its identifier from Stripe. The approach used to accomplish this differs based on whether you plan to use the payment method for subscriptions or single charges, so we will examine both below.

<a name="payment-methods-for-subscriptions"></a>
#### Payment Methods For Subscriptions

When storing a customer's credit card information for future use by a subscription, the Stripe "Setup Intents" API must be used to securely gather the customer's payment method details. A "Setup Intent" indicates to Stripe the intention to charge a customer's payment method. Cashier's `Billable` trait includes the `createSetupIntent` method to easily create a new Setup Intent. You should invoke this method from the route or controller that will render the form which gathers your customer's payment method details:

    return view('update-payment-method', [
        'intent' => $user->createSetupIntent()
    ]);

After you have created the Setup Intent and passed it to the view, you should attach its secret to the element that will gather the payment method. For example, consider this "update payment method" form:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button" data-secret="{{ $intent->client_secret }}">
    Update Payment Method
</button>
```

Next, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details:

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

Next, the card can be verified and a secure "payment method identifier" can be retrieved from Stripe using [Stripe's `confirmCardSetup` method](https://stripe.com/docs/js/setup_intents/confirm_card_setup):

```js
const cardHolderName = document.getElementById('card-holder-name');
const cardButton = document.getElementById('card-button');
const clientSecret = cardButton.dataset.secret;

cardButton.addEventListener('click', async (e) => {
    const { setupIntent, error } = await stripe.confirmCardSetup(
        clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: { name: cardHolderName.value }
            }
        }
    );

    if (error) {
        // Display "error.message" to the user...
    } else {
        // The card has been verified successfully...
    }
});
```

After the card has been verified by Stripe, you may pass the resulting `setupIntent.payment_method` identifier to your Laravel application, where it can be attached to the customer. The payment method can either be [added as a new payment method](#adding-payment-methods) or [used to update the default payment method](#updating-the-default-payment-method). You can also immediately use the payment method identifier to [create a new subscription](#creating-subscriptions).

> {tip} If you would like more information about Setup Intents and gathering customer payment details please [review this overview provided by Stripe](https://stripe.com/docs/payments/save-and-reuse#php).

<a name="payment-methods-for-single-charges"></a>
#### Payment Methods For Single Charges

Of course, when making a single charge against a customer's payment method, we will only need to use a payment method identifier once. Due to Stripe limitations, you may not use the stored default payment method of a customer for single charges. You must allow the customer to enter their payment method details using the Stripe.js library. For example, consider the following form:

```html
<input id="card-holder-name" type="text">

<!-- Stripe Elements Placeholder -->
<div id="card-element"></div>

<button id="card-button">
    Process Payment
</button>
```

After defining such a form, the Stripe.js library may be used to attach a [Stripe Element](https://stripe.com/docs/stripe-js) to the form and securely gather the customer's payment details:

```html
<script src="https://js.stripe.com/v3/"></script>

<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');
</script>
```

Next, the card can be verified and a secure "payment method identifier" can be retrieved from Stripe using [Stripe's `createPaymentMethod` method](https://stripe.com/docs/stripe-js/reference#stripe-create-payment-method):

```js
const cardHolderName = document.getElementById('card-holder-name');
const cardButton = document.getElementById('card-button');

cardButton.addEventListener('click', async (e) => {
    const { paymentMethod, error } = await stripe.createPaymentMethod(
        'card', cardElement, {
            billing_details: { name: cardHolderName.value }
        }
    );

    if (error) {
        // Display "error.message" to the user...
    } else {
        // The card has been verified successfully...
    }
});
```

If the card is verified successfully, you may pass the `paymentMethod.id` to your Laravel application and process a [single charge](#simple-charge).

<a name="retrieving-payment-methods"></a>
### Retrieving Payment Methods

The `paymentMethods` method on the billable model instance returns a collection of `Laravel\Cashier\PaymentMethod` instances:

    $paymentMethods = $user->paymentMethods();

By default, this method will return payment methods of the `card` type. To retrieve payment methods of a different type, you may pass the `type` as an argument to the method:

    $paymentMethods = $user->paymentMethods('sepa_debit');

To retrieve the customer's default payment method, the `defaultPaymentMethod` method may be used:

    $paymentMethod = $user->defaultPaymentMethod();

You can retrieve a specific payment method that is attached to the billable model using the `findPaymentMethod` method:

    $paymentMethod = $user->findPaymentMethod($paymentMethodId);

<a name="check-for-a-payment-method"></a>
### Determining If A User Has A Payment Method

To determine if a billable model has a default payment method attached to their account, invoke the `hasDefaultPaymentMethod` method:

    if ($user->hasDefaultPaymentMethod()) {
        //
    }

You may use the `hasPaymentMethod` method to determine if a billable model has at least one payment method attached to their account:

    if ($user->hasPaymentMethod()) {
        //
    }

This method will determine if the billable model has payment methods of the `card` type. To determine if a payment method of another type exists for the model, you may pass the `type` as an argument to the method:

    if ($user->hasPaymentMethod('sepa_debit')) {
        //
    }

<a name="updating-the-default-payment-method"></a>
### Updating The Default Payment Method

The `updateDefaultPaymentMethod` method may be used to update a customer's default payment method information. This method accepts a Stripe payment method identifier and will assign the new payment method as the default billing payment method:

    $user->updateDefaultPaymentMethod($paymentMethod);

To sync your default payment method information with the customer's default payment method information in Stripe, you may use the `updateDefaultPaymentMethodFromStripe` method:

    $user->updateDefaultPaymentMethodFromStripe();

> {note} The default payment method on a customer can only be used for invoicing and creating new subscriptions. Due to limitations imposed by Stripe, it may not be used for single charges.

<a name="adding-payment-methods"></a>
### Adding Payment Methods

To add a new payment method, you may call the `addPaymentMethod` method on the billable model, passing the payment method identifier:

    $user->addPaymentMethod($paymentMethod);

> {tip} To learn how to retrieve payment method identifiers please review the [payment method storage documentation](#storing-payment-methods).

<a name="deleting-payment-methods"></a>
### Deleting Payment Methods

To delete a payment method, you may call the `delete` method on the `Laravel\Cashier\PaymentMethod` instance you wish to delete:

    $paymentMethod->delete();

The `deletePaymentMethod` method will delete a specific payment method from the billable model:

    $user->deletePaymentMethod('pm_visa');

The `deletePaymentMethods` method will delete all of the payment method information for the billable model:

    $user->deletePaymentMethods();

By default, this method will delete payment methods of the `card` type. To delete payment methods of a different type you can pass the `type` as an argument to the method:

    $user->deletePaymentMethods('sepa_debit');

> {note} If a user has an active subscription, your application should not allow them to delete their default payment method.

<a name="subscriptions"></a>
## Subscriptions

Subscriptions provide a way to set up recurring payments for your customers. Stripe subscriptions managed by Cashier provide support for multiple subscription prices, subscription quantities, trials, and more.

<a name="creating-subscriptions"></a>
### Creating Subscriptions

To create a subscription, first retrieve an instance of your billable model, which typically will be an instance of `App\Models\User`. Once you have retrieved the model instance, you may use the `newSubscription` method to create the model's subscription:

    use Illuminate\Http\Request;

    Route::post('/user/subscribe', function (Request $request) {
        $request->user()->newSubscription(
            'default', 'price_monthly'
        )->create($request->paymentMethodId);

        // ...
    });

The first argument passed to the `newSubscription` method should be the internal name of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription name is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument is the specific price the user is subscribing to. This value should correspond to the price's identifier in Stripe.

The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information.

> {note} Passing a payment method identifier directly to the `create` subscription method will also automatically add it to the user's stored payment methods.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### Collecting Recurring Payments Via Invoice Emails

Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices:

    $user->newSubscription('default', 'price_monthly')->createAndSendInvoice();

The amount of time a customer has to pay their invoice before their subscription is canceled is determined by your subscription and invoice settings within the [Stripe dashboard](https://dashboard.stripe.com/settings/billing/automatic).

<a name="subscription-quantities"></a>
#### Quantities

If you would like to set a specific [quantity](https://stripe.com/docs/billing/subscriptions/quantities) for the price when creating the subscription, you should invoke the `quantity` method on the subscription builder before creating the subscription:

    $user->newSubscription('default', 'price_monthly')
         ->quantity(5)
         ->create($paymentMethod);

<a name="additional-details"></a>
#### Additional Details

If you would like to specify additional [customer](https://stripe.com/docs/api/customers/create) or [subscription](https://stripe.com/docs/api/subscriptions/create) options supported by Stripe, you may do so by passing them as the second and third arguments to the `create` method:

    $user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
        'email' => $email,
    ], [
        'metadata' => ['note' => 'Some extra information.'],
    ]);

<a name="coupons"></a>
#### Coupons

If you would like to apply a coupon when creating the subscription, you may use the `withCoupon` method:

    $user->newSubscription('default', 'price_monthly')
         ->withCoupon('code')
         ->create($paymentMethod);

Or, if you would like to apply a [Stripe promotion code](https://stripe.com/docs/billing/subscriptions/discounts/codes), you may use the `withPromotionCode` method. The given promotion code ID should be the Stripe API ID assigned to the promotion code and not the customer facing promotion code:

    $user->newSubscription('default', 'price_monthly')
         ->withPromotionCode('promo_code')
         ->create($paymentMethod);

<a name="adding-subscriptions"></a>
#### Adding Subscriptions

If you would like to add a subscription to a customer who already has a default payment method you may invoke the `add` method on the subscription builder:

    use App\Models\User;

    $user = User::find(1);

    $user->newSubscription('default', 'price_monthly')->add();

<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Creating Subscriptions From The Stripe Dashboard

You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a name of `default`. To customize the subscription name that is assigned to dashboard created subscriptions, [extend the `WebhookController`](/docs/{{version}}/billing#defining-webhook-event-handlers) and overwrite the `newSubscriptionName` method.

In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different names, only one type of subscription may be added through the Stripe dashboard.

Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database.

<a name="checking-subscription-status"></a>
### Checking Subscription Status

Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the name of the subscription as its first argument:

    if ($user->subscribed('default')) {
        //
    }

The `subscribed` method also makes a great candidate for a [route middleware](/docs/{{version}}/middleware), allowing you to filter access to routes and controllers based on the user's subscription status:

    <?php

    namespace App\Http\Middleware;

    use Closure;

    class EnsureUserIsSubscribed
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
            if ($request->user() && ! $request->user()->subscribed('default')) {
                // This user is not a paying customer...
                return redirect('billing');
            }

            return $next($request);
        }
    }

If you would like to determine if a user is still within their trial period, you may use the `onTrial` method. This method can be useful for determining if you should display a warning to the user that they are still on their trial period:

    if ($user->subscription('default')->onTrial()) {
        //
    }

The `subscribedToProduct` method may be used to determine if the user is subscribed to a given product based on a given Stripe product's identifier. In Stripe, products are collections of prices. In this example, we will determine if the user's `default` subscription is actively subscribed to the application's "premium" product. The given Stripe product identifier should correspond to one of your product's identifiers in the Stripe dashboard:

    if ($user->subscribedToProduct('prod_premium', 'default')) {
        //
    }

By passing an array to the `subscribedToProduct` method, you may determine if the user's `default` subscription is actively subscribed to the application's "basic" or "premium" product:

    if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
        //
    }

The `subscribedToPrice` method may be used to determine if a customer's subscription corresponds to a given price ID:

    if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
        //
    }

The `recurring` method may be used to determine if the user is currently subscribed and is no longer within their trial period:

    if ($user->subscription('default')->recurring()) {
        //
    }

> {note} If a user has two subscriptions with the same name, the most recent subscription will always be returned by the `subscription` method. For example, a user might have two subscription records named `default`; however, one of the subscriptions may be an old, expired subscription, while the other is the current, active subscription. The most recent subscription will always be returned while older subscriptions are kept in the database for historical review.

<a name="cancelled-subscription-status"></a>
#### Canceled Subscription Status

To determine if the user was once an active subscriber but has canceled their subscription, you may use the `canceled` method:

    if ($user->subscription('default')->canceled()) {
        //
    }

You may also determine if a user has canceled their subscription but are still on their "grace period" until the subscription fully expires. For example, if a user cancels a subscription on March 5th that was originally scheduled to expire on March 10th, the user is on their "grace period" until March 10th. Note that the `subscribed` method still returns `true` during this time:

    if ($user->subscription('default')->onGracePeriod()) {
        //
    }

To determine if the user has canceled their subscription and is no longer within their "grace period", you may use the `ended` method:

    if ($user->subscription('default')->ended()) {
        //
    }

<a name="incomplete-and-past-due-status"></a>
#### Incomplete and Past Due Status

If a subscription requires a secondary payment action after creation the subscription will be marked as `incomplete`. Subscription statuses are stored in the `stripe_status` column of Cashier's `subscriptions` database table.

Similarly, if a secondary payment action is required when swapping prices the subscription will be marked as `past_due`. When your subscription is in either of these states it will not be active until the customer has confirmed their payment. Determining if a subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance:

    if ($user->hasIncompletePayment('default')) {
        //
    }

    if ($user->subscription('default')->hasIncompletePayment()) {
        //
    }

When a subscription has an incomplete payment, you should direct the user to Cashier's payment confirmation page, passing the `latestPayment` identifier. You may use the `latestPayment` method available on subscription instance to retrieve this identifier:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```

If you would like the subscription to still be considered active when it's in a `past_due` state, you may use the `keepPastDueSubscriptionsActive` method provided by Cashier. Typically, this method should be called in the `register` method of your `App\Providers\AppServiceProvider`:

    use Laravel\Cashier\Cashier;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        Cashier::keepPastDueSubscriptionsActive();
    }

> {note} When a subscription is in an `incomplete` state it cannot be changed until the payment is confirmed. Therefore, the `swap` and `updateQuantity` methods will throw an exception when the subscription is in an `incomplete` state.

<a name="subscription-scopes"></a>
#### Subscription Scopes

Most subscription states are also available as query scopes so that you may easily query your database for subscriptions that are in a given state:

    // Get all active subscriptions...
    $subscriptions = Subscription::query()->active()->get();

    // Get all of the canceled subscriptions for a user...
    $subscriptions = $user->subscriptions()->canceled()->get();

A complete list of available scopes is available below:

    Subscription::query()->active();
    Subscription::query()->canceled();
    Subscription::query()->ended();
    Subscription::query()->incomplete();
    Subscription::query()->notCanceled();
    Subscription::query()->notOnGracePeriod();
    Subscription::query()->notOnTrial();
    Subscription::query()->onGracePeriod();
    Subscription::query()->onTrial();
    Subscription::query()->pastDue();
    Subscription::query()->recurring();

<a name="changing-prices"></a>
### Changing Prices

After a customer is subscribed to your application, they may occasionally want to change to a new subscription price. To swap a customer to a new price, pass the Stripe price's identifier to the `swap` method. When swapping prices, it is assumed that the user would like to re-activate their subscription if it was previously canceled. The given price identifier should correspond to a Stripe price identifier available in the Stripe dashboard:

    use App\Models\User;

    $user = App\Models\User::find(1);

    $user->subscription('default')->swap('price_yearly');

If the customer is on trial, the trial period will be maintained. Additionally, if a "quantity" exists for the subscription, that quantity will also be maintained.

If you would like to swap prices and cancel any trial period the customer is currently on, you may invoke the `skipTrial` method:

    $user->subscription('default')
            ->skipTrial()
            ->swap('price_yearly');

If you would like to swap prices and immediately invoice the customer instead of waiting for their next billing cycle, you may use the `swapAndInvoice` method:

    $user = User::find(1);

    $user->subscription('default')->swapAndInvoice('price_yearly');

<a name="prorations"></a>
#### Prorations

By default, Stripe prorates charges when swapping between prices. The `noProrate` method may be used to update the subscription's price without prorating the charges:

    $user->subscription('default')->noProrate()->swap('price_yearly');

For more information on subscription proration, consult the [Stripe documentation](https://stripe.com/docs/billing/subscriptions/prorations).

> {note} Executing the `noProrate` method before the `swapAndInvoice` method will have no effect on proration. An invoice will always be issued.

<a name="subscription-quantity"></a>
### Subscription Quantity

Sometimes subscriptions are affected by "quantity". For example, a project management application might charge $10 per month per project. You may use the `incrementQuantity` and `decrementQuantity` methods to easily increment or decrement your subscription quantity:

    use App\Models\User;

    $user = User::find(1);

    $user->subscription('default')->incrementQuantity();

    // Add five to the subscription's current quantity...
    $user->subscription('default')->incrementQuantity(5);

    $user->subscription('default')->decrementQuantity();

    // Subtract five from the subscription's current quantity...
    $user->subscription('default')->decrementQuantity(5);

Alternatively, you may set a specific quantity using the `updateQuantity` method:

    $user->subscription('default')->updateQuantity(10);

The `noProrate` method may be used to update the subscription's quantity without prorating the charges:

    $user->subscription('default')->noProrate()->updateQuantity(10);

For more information on subscription quantities, consult the [Stripe documentation](https://stripe.com/docs/subscriptions/quantities).

<a name="multiprice-subscription-quantities"></a>
#### Multiprice Subscription Quantities

If your subscription is a [multiprice subscription](#multiprice-subscriptions), you should pass the name of the price whose quantity you wish to increment or decrement as the second argument to the increment / decrement methods:

    $user->subscription('default')->incrementQuantity(1, 'price_chat');

<a name="multiprice-subscriptions"></a>
### Multiprice Subscriptions

[Multiprice subscriptions](https://stripe.com/docs/billing/subscriptions/multiple-products) allow you to assign multiple billing prices to a single subscription. For example, imagine you are building a customer service "helpdesk" application that has a base subscription price of $10 per month but offers a live chat add-on price for an additional $15 per month. Multiprice subscription information is stored in Cashier's `subscription_items` database table.

You may specify multiple prices for a given subscription by passing an array of prices as the second argument to the `newSubscription` method:

    use Illuminate\Http\Request;

    Route::post('/user/subscribe', function (Request $request) {
        $request->user()->newSubscription('default', [
            'price_monthly',
            'price_chat',
        ])->create($request->paymentMethodId);

        // ...
    });

In the example above, the customer will have two prices attached to their `default` subscription. Both prices will be charged on their respective billing intervals. If necessary, you may use the `quantity` method to indicate a specific quantity for each price:

    $user = User::find(1);

    $user->newSubscription('default', ['price_monthly', 'price_chat'])
        ->quantity(5, 'price_chat')
        ->create($paymentMethod);

If you would like to add another price to an existing subscription, you may invoke the subscription's `addPrice` method:

    $user = User::find(1);

    $user->subscription('default')->addPrice('price_chat');

The example above will add the new price and the customer will be billed for it on their next billing cycle. If you would like to bill the customer immediately you may use the `addPriceAndInvoice` method:

    $user->subscription('default')->addPriceAndInvoice('price_chat');

If you would like to add a price with a specific quantity, you can pass the quantity as the second argument of the `addPrice` or `addPriceAndInvoice` methods:

    $user = User::find(1);

    $user->subscription('default')->addPrice('price_chat', 5);

You may remove prices from subscriptions using the `removePrice` method:

    $user->subscription('default')->removePrice('price_chat');

> {note} You may not remove the last price on a subscription. Instead, you should simply cancel the subscription.

<a name="swapping-prices"></a>
#### Swapping Prices

You may also change the prices attached to a multiprice subscription. For example, imagine a customer has a `price_basic` subscription with a `price_chat` add-on price and you want to upgrade the customer from the `price_basic` to the `price_pro` price:

    use App\Models\User;

    $user = User::find(1);

    $user->subscription('default')->swap(['price_pro', 'price_chat']);

When executing the example above, the underlying subscription item with the `price_basic` is deleted and the one with the `price_chat` is preserved. Additionally, a new subscription item for the `price_pro` is created.

You can also specify subscription item options by passing an array of key / value pairs to the `swap` method. For example, you may need to specify the subscription price quantities:

    $user = User::find(1);

    $user->subscription('default')->swap([
        'price_pro' => ['quantity' => 5],
        'price_chat'
    ]);

If you want to swap a single price on a subscription, you may do so using the `swap` method on the subscription item itself. This approach is particularly useful if you would like to preserve all of the existing metadata on the subscription's other prices:

    $user = User::find(1);

    $user->subscription('default')
            ->findItemOrFail('price_basic')
            ->swap('price_pro');

<a name="proration"></a>
#### Proration

By default, Stripe will prorate charges when adding or removing prices from a multiprice subscription. If you would like to make a price adjustment without proration, you should chain the `noProrate` method onto your price operation:

    $user->subscription('default')->noProrate()->removePrice('price_chat');

<a name="swapping-quantities"></a>
#### Quantities

If you would like to update quantities on individual subscription prices, you may do so using the [existing quantity methods](#subscription-quantity) by passing the name of the price as an additional argument to the method:

    $user = User::find(1);

    $user->subscription('default')->incrementQuantity(5, 'price_chat');

    $user->subscription('default')->decrementQuantity(3, 'price_chat');

    $user->subscription('default')->updateQuantity(10, 'price_chat');

> {note} When a subscription has multiple prices the `stripe_price` and `quantity` attributes on the `Subscription` model will be `null`. To access the individual price attributes, you should use the `items` relationship available on the `Subscription` model.

<a name="subscription-items"></a>
#### Subscription Items

When a subscription has multiple prices, it will have multiple subscription "items" stored in your database's `subscription_items` table. You may access these via the `items` relationship on the subscription:

    use App\Models\User;

    $user = User::find(1);

    $subscriptionItem = $user->subscription('default')->items->first();

    // Retrieve the Stripe price and quantity for a specific item...
    $stripePrice = $subscriptionItem->stripe_price;
    $quantity = $subscriptionItem->quantity;

You can also retrieve a specific price using the `findItemOrFail` method:

    $user = User::find(1);

    $subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');

<a name="metered-billing"></a>
### Metered Billing

[Metered billing](https://stripe.com/docs/billing/subscriptions/metered-billing) allows you to charge customers based on their product usage during a billing cycle. For example, you may charge customers based on the number of text messages or emails they send per month.

To start using metered billing, you will first need to create a new product in your Stripe dashboard with a metered price. Then, use the `meteredPrice` to add the metered price ID to a customer subscription:

    use Illuminate\Http\Request;

    Route::post('/user/subscribe', function (Request $request) {
        $request->user()->newSubscription('default')
            ->meteredPrice('price_metered')
            ->create($request->paymentMethodId);

        // ...
    });

You may also start a metered subscription via [Stripe Checkout](#checkout):

    $checkout = Auth::user()
            ->newSubscription('default', [])
            ->meteredPrice('price_metered')
            ->checkout();

    return view('your-checkout-view', [
        'checkout' => $checkout,
    ]);

<a name="reporting-usage"></a>
#### Reporting Usage

As your customer uses your application, you will report their usage to Stripe so that they can be billed accurately. To increment the usage of a metered subscription, you may use the `reportUsage` method:

    $user = User::find(1);

    $user->subscription('default')->reportUsage();

By default, a "usage quantity" of 1 is added to the billing period. Alternatively, you may pass a specific amount of "usage" to add to the customer's usage for the billing period:

    $user = User::find(1);

    $user->subscription('default')->reportUsage(15);

If your application offers multiple prices on a single subscription, you will need to use the `reportUsageFor` method to specify the metered price you want to report usage for:

    $user = User::find(1);

    $user->subscription('default')->reportUsageFor('price_metered', 15);

Sometimes, you may need to update usage which you have previously reported. To accomplish this, you may pass a timestamp or a `DateTimeInterface` instance as the second parameter to `reportUsage`. When doing so, Stripe will update the usage that was reported at that given time. You can continue to update previous usage records as the given date and time is still within the current billing period:

    $user = User::find(1);

    $user->subscription('default')->reportUsage(5, $timestamp);

<a name="retrieving-usage-records"></a>
#### Retrieving Usage Records

To retrieve a customer's past usage, you may use a subscription instance's `usageRecords` method:

    $user = User::find(1);

    $usageRecords = $user->subscription('default')->usageRecords();

If your application offers multiple prices on a single subscription, you may use the `usageRecordsFor` method to specify the metered price that you wish to retrieve usage records for:

    $user = User::find(1);

    $usageRecords = $user->subscription('default')->usageRecordsFor('price_metered');

The `usageRecords` and `usageRecordsFor` methods return a Collection instance containing an associative array of usage records. You may iterate over this array to display a customer's total usage:

    @foreach ($usageRecords as $usageRecord)
        - Period Starting: {{ $usageRecord['period']['start'] }}
        - Period Ending: {{ $usageRecord['period']['end'] }}
        - Total Usage: {{ $usageRecord['total_usage'] }}
    @endforeach

For a full reference of all usage data returned and how to use Stripe's cursor based pagination, please consult [the official Stripe API documentation](https://stripe.com/docs/api/usage_records/subscription_item_summary_list).

<a name="subscription-taxes"></a>
### Subscription Taxes

> {note} Instead of calculating Tax Rates manually, you can [automatically calculate taxes using Stripe Tax](#tax-configuration)

To specify the tax rates a user pays on a subscription, you should implement the `taxRates` method on your billable model and return an array containing the Stripe tax rate IDs. You can define these tax rates in [your Stripe dashboard](https://dashboard.stripe.com/test/tax-rates):

    /**
     * The tax rates that should apply to the customer's subscriptions.
     *
     * @return array
     */
    public function taxRates()
    {
        return ['txr_id'];
    }

The `taxRates` method enables you to apply a tax rate on a customer-by-customer basis, which may be helpful for a user base that spans multiple countries and tax rates.

If you're offering multiprice subscriptions, you may define different tax rates for each price by implementing a `priceTaxRates` method on your billable model:

    /**
     * The tax rates that should apply to the customer's subscriptions.
     *
     * @return array
     */
    public function priceTaxRates()
    {
        return [
            'price_monthly' => ['txr_id'],
        ];
    }

> {note} The `taxRates` method only applies to subscription charges. If you use Cashier to make "one off" charges, you will need to manually specify the tax rate at that time.

<a name="syncing-tax-rates"></a>
#### Syncing Tax Rates

When changing the hard-coded tax rate IDs returned by the `taxRates` method, the tax settings on any existing subscriptions for the user will remain the same. If you wish to update the tax value for existing subscriptions with the new `taxRates` values, you should call the `syncTaxRates` method on the user's subscription instance:

    $user->subscription('default')->syncTaxRates();

This will also sync any multiprice subscription item tax rates. If your application is offering multiprice subscriptions, you should ensure that your billable model implements the `priceTaxRates` method [discussed above](#subscription-taxes).

<a name="tax-exemption"></a>
#### Tax Exemption

Cashier also offers the `isNotTaxExempt`, `isTaxExempt`, and `reverseChargeApplies` methods to determine if the customer is tax exempt. These methods will call the Stripe API to determine a customer's tax exemption status:

    use App\Models\User;

    $user = User::find(1);

    $user->isTaxExempt();
    $user->isNotTaxExempt();
    $user->reverseChargeApplies();

> {note} These methods are also available on any `Laravel\Cashier\Invoice` object. However, when invoked on an `Invoice` object, the methods will determine the exemption status at the time the invoice was created.

<a name="subscription-anchor-date"></a>
### Subscription Anchor Date

By default, the billing cycle anchor is the date the subscription was created or, if a trial period is used, the date that the trial ends. If you would like to modify the billing anchor date, you may use the `anchorBillingCycleOn` method:

    use Illuminate\Http\Request;

    Route::post('/user/subscribe', function (Request $request) {
        $anchor = Carbon::parse('first day of next month');

        $request->user()->newSubscription('default', 'price_monthly')
                    ->anchorBillingCycleOn($anchor->startOfDay())
                    ->create($request->paymentMethodId);

        // ...
    });

For more information on managing subscription billing cycles, consult the [Stripe billing cycle documentation](https://stripe.com/docs/billing/subscriptions/billing-cycle)

<a name="cancelling-subscriptions"></a>
### Cancelling Subscriptions

To cancel a subscription, call the `cancel` method on the user's subscription:

    $user->subscription('default')->cancel();

When a subscription is canceled, Cashier will automatically set the `ends_at` column in your `subscriptions` database table. This column is used to know when the `subscribed` method should begin returning `false`.

For example, if a customer cancels a subscription on March 1st, but the subscription was not scheduled to end until March 5th, the `subscribed` method will continue to return `true` until March 5th. This is done because a user is typically allowed to continue using an application until the end of their billing cycle.

You may determine if a user has canceled their subscription but are still on their "grace period" using the `onGracePeriod` method:

    if ($user->subscription('default')->onGracePeriod()) {
        //
    }

If you wish to cancel a subscription immediately, call the `cancelNow` method on the user's subscription:

    $user->subscription('default')->cancelNow();

If you wish to cancel a subscription immediately and invoice any remaining un-invoiced metered usage or new / pending proration invoice items, call the `cancelNowAndInvoice` method on the user's subscription:

    $user->subscription('default')->cancelNowAndInvoice();

You may also choose to cancel the subscription at a specific moment in time:

    $user->subscription('default')->cancelAt(
        now()->addDays(10)
    );

<a name="resuming-subscriptions"></a>
### Resuming Subscriptions

If a customer has canceled their subscription and you wish to resume it, you may invoke the `resume` method on the subscription. The customer must still be within their "grace period" in order to resume a subscription:

    $user->subscription('default')->resume();

If the customer cancels a subscription and then resumes that subscription before the subscription has fully expired the customer will not be billed immediately. Instead, their subscription will be re-activated and they will be billed on the original billing cycle.

<a name="subscription-trials"></a>
## Subscription Trials

<a name="with-payment-method-up-front"></a>
### With Payment Method Up Front

If you would like to offer trial periods to your customers while still collecting payment method information up front, you should use the `trialDays` method when creating your subscriptions:

    use Illuminate\Http\Request;

    Route::post('/user/subscribe', function (Request $request) {
        $request->user()->newSubscription('default', 'price_monthly')
                    ->trialDays(10)
                    ->create($request->paymentMethodId);

        // ...
    });

This method will set the trial period ending date on the subscription record within the database and instruct Stripe to not begin billing the customer until after this date. When using the `trialDays` method, Cashier will overwrite any default trial period configured for the price in Stripe.

> {note} If the customer's subscription is not canceled before the trial ending date they will be charged as soon as the trial expires, so you should be sure to notify your users of their trial ending date.

The `trialUntil` method allows you to provide a `DateTime` instance that specifies when the trial period should end:

    use Carbon\Carbon;

    $user->newSubscription('default', 'price_monthly')
                ->trialUntil(Carbon::now()->addDays(10))
                ->create($paymentMethod);

You may determine if a user is within their trial period using either the `onTrial` method of the user instance or the `onTrial` method of the subscription instance. The two examples below are equivalent:

    if ($user->onTrial('default')) {
        //
    }

    if ($user->subscription('default')->onTrial()) {
        //
    }

You may use the `endTrial` method to immediately end a subscription trial:

    $user->subscription('default')->endTrial();

<a name="defining-trial-days-in-stripe-cashier"></a>
#### Defining Trial Days In Stripe / Cashier

You may choose to define how many trial days your price's receive in the Stripe dashboard or always pass them explicitly using Cashier. If you choose to define your price's trial days in Stripe you should be aware that new subscriptions, including new subscriptions for a customer that had a subscription in the past, will always receive a trial period unless you explicitly call the `skipTrial()` method.

<a name="without-payment-method-up-front"></a>
### Without Payment Method Up Front

If you would like to offer trial periods without collecting the user's payment method information up front, you may set the `trial_ends_at` column on the user record to your desired trial ending date. This is typically done during user registration:

    use App\Models\User;

    $user = User::create([
        // ...
        'trial_ends_at' => now()->addDays(10),
    ]);

> {note} Be sure to add a [date cast](/docs/{{version}}/eloquent-mutators##date-casting) for the `trial_ends_at` attribute within your billable model's class definition.

Cashier refers to this type of trial as a "generic trial", since it is not attached to any existing subscription. The `onTrial` method on the billable model instance will return `true` if the current date is not past the value of `trial_ends_at`:

    if ($user->onTrial()) {
        // User is within their trial period...
    }

Once you are ready to create an actual subscription for the user, you may use the `newSubscription` method as usual:

    $user = User::find(1);

    $user->newSubscription('default', 'price_monthly')->create($paymentMethod);

To retrieve the user's trial ending date, you may use the `trialEndsAt` method. This method will return a Carbon date instance if a user is on a trial or `null` if they aren't. You may also pass an optional subscription name parameter if you would like to get the trial ending date for a specific subscription other than the default one:

    if ($user->onTrial()) {
        $trialEndsAt = $user->trialEndsAt('main');
    }

You may also use the `onGenericTrial` method if you wish to know specifically that the user is within their "generic" trial period and has not yet created an actual subscription:

    if ($user->onGenericTrial()) {
        // User is within their "generic" trial period...
    }

<a name="extending-trials"></a>
### Extending Trials

The `extendTrial` method allows you to extend the trial period of a subscription after the subscription has been created. If the trial has already expired and the customer is already being billed for the subscription, you can still offer them an extended trial. The time spent within the trial period will be deducted from the customer's next invoice:

    use App\Models\User;

    $subscription = User::find(1)->subscription('default');

    // End the trial 7 days from now...
    $subscription->extendTrial(
        now()->addDays(7)
    );

    // Add an additional 5 days to the trial...
    $subscription->extendTrial(
        $subscription->trial_ends_at->addDays(5)
    );

<a name="handling-stripe-webhooks"></a>
## Handling Stripe Webhooks

> {tip} You may use [the Stripe CLI](https://stripe.com/docs/stripe-cli) to help test webhooks during local development.

Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests.

By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like.

To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `invoice.payment_action_required`

For convenience, Cashier includes a `cashier:webhook` Artisan command. This command will create a webhook in Stripe that listens to all of the events required by Cashier:

```shell
php artisan cashier:webhook
```

By default, the created webhook will point to the URL defined by the `APP_URL` environment variable and the `cashier.webhook` route that is included with Cashier. You may provide the `--url` option when invoking the command if you would like to use a different URL:

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```

The webhook that is created will use the Stripe API version that your version of Cashier is compatible with. If you would like to use a different Stripe version, you may provide the `--api-version` option:

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```

After creation, the webhook will be immediately active. If you wish to create the webhook but have it disabled until you're ready, you may provide the `--disabled` option when invoking the command:

```shell
php artisan cashier:webhook --disabled
```

> {note} Make sure you protect incoming Stripe webhook requests with Cashier's included [webhook signature verification](#verifying-webhook-signatures) middleware.

<a name="webhooks-csrf-protection"></a>
#### Webhooks & CSRF Protection

Since Stripe webhooks need to bypass Laravel's [CSRF protection](/docs/{{version}}/csrf), be sure to list the URI as an exception in your application's `App\Http\Middleware\VerifyCsrfToken` middleware or list the route outside of the `web` middleware group:

    protected $except = [
        'stripe/*',
    ];

<a name="defining-webhook-event-handlers"></a>
### Defining Webhook Event Handlers

Cashier automatically handles subscription cancellations for failed charges and other common Stripe webhook events. However, if you have additional webhook events you would like to handle, you may do so by listening to the following events that are dispatched by Cashier:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

Both events contain the full payload of the Stripe webhook. For example, if you wish to handle the `invoice.payment_succeeded` webhook, you may register a [listener](/docs/{{version}}/events#defining-listeners) that will handle the event:

    <?php

    namespace App\Listeners;

    use Laravel\Cashier\Events\WebhookReceived;

    class StripeEventListener
    {
        /**
         * Handle received Stripe webhooks.
         *
         * @param  \Laravel\Cashier\Events\WebhookReceived  $event
         * @return void
         */
        public function handle(WebhookReceived $event)
        {
            if ($event->payload['type'] === 'invoice.payment_succeeded') {
                // Handle the incoming event...
            }
        }
    }

Once your listener has been defined, you may register it within your application's `EventServiceProvider`:

    <?php

    namespace App\Providers;

    use App\Listeners\StripeEventListener;
    use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;
    use Laravel\Cashier\Events\WebhookReceived;

    class EventServiceProvider extends ServiceProvider
    {
        protected $listen = [
            WebhookReceived::class => [
                StripeEventListener::class,
            ],
        ];
    }

<a name="verifying-webhook-signatures"></a>
### Verifying Webhook Signatures

To secure your webhooks, you may use [Stripe's webhook signatures](https://stripe.com/docs/webhooks/signatures). For convenience, Cashier automatically includes a middleware which validates that the incoming Stripe webhook request is valid.

To enable webhook verification, ensure that the `STRIPE_WEBHOOK_SECRET` environment variable is set in your application's `.env` file. The webhook `secret` may be retrieved from your Stripe account dashboard.

<a name="single-charges"></a>
## Single Charges

> {note} The `pay`, `payWith`, `charge`, `invoiceFor` and `refund` methods accept the amount you would like to use in the lowest denominator of the currency used by your application. For example, when using United States Dollars, amounts should be specified in pennies.

<a name="creating-payments"></a>
### Creating Payments

You can simply create a new payment for a customer by calling the `pay` method on a billable model instance. Calling this method will create a payment intent that's wrapped in a `Laravel\Cashier\Payment` object:

    use Illuminate\Http\Request;

    Route::post('/pay', function (Request $request) {
        $payment = $request->user()->pay(
            $request->get('amount')
        );

        return $payment->client_secret;
    });

After creating the payment intent, you can return the client secret to your front-end to complete the payment in the browser. See [a full guide by Stripe](https://stripe.com/docs/payments/accept-a-payment?platform=web) on this

Using the above `pay` method, the default payment methods that are enabled in the dashboard will be available to the customer to collect payment. Alternatively, if you only want to allow for some specific payment methods to be used, you may use the `payWith` method instead:

    use Illuminate\Http\Request;

    Route::post('/pay', function (Request $request) {
        $payment = $request->user()->payWith(
            $request->get('amount'), ['card', 'bancontact']
        );

        return $payment->client_secret;
    });

<a name="simple-charge"></a>
### Simple Charge

If you would like to make a one-time charge against a customer, you may use the `charge` method on a billable model instance. You will need to [provide a payment method identifier](#payment-methods-for-single-charges) as the second argument to the `charge` method:

    use Illuminate\Http\Request;

    Route::post('/purchase', function (Request $request) {
        $stripeCharge = $request->user()->charge(
            100, $request->paymentMethodId
        );

        // ...
    });

The `charge` method accepts an array as its third argument, allowing you to pass any options you wish to the underlying Stripe charge creation. More information regarding the options available to you when creating charges may be found in the [Stripe documentation](https://stripe.com/docs/api/charges/create):

    $user->charge(100, $paymentMethod, [
        'custom_option' => $value,
    ]);

You may also use the `charge` method without an underlying customer or user. To accomplish this, invoke the `charge` method on a new instance of your application's billable model:

    use App\Models\User;

    $stripeCharge = (new User)->charge(100, $paymentMethod);

The `charge` method will throw an exception if the charge fails. If the charge is successful, an instance of `Laravel\Cashier\Payment` will be returned from the method:

    try {
        $payment = $user->charge(100, $paymentMethod);
    } catch (Exception $e) {
        //
    }

<a name="charge-with-invoice"></a>
### Charge With Invoice

Sometimes you may need to make a one-time charge and offer a PDF receipt to your customer. The `invoicePrice` method lets you do just that. For example, let's invoice a customer for five new shirts:

    $user->invoicePrice('price_tshirt', 5);

The invoice will be immediately charged against the user's default payment method. The `invoicePrice` method also accepts an array as its third argument. This array contains the billing options for the invoice item. The fourth argument accepted by the method is also an array which should contain the billing options for the invoice itself:

    $user->invoicePrice('price_tshirt', 5, [
        'discounts' => [
            ['coupon' => 'SUMMER21SALE']
        ],
    ], [
        'default_tax_rates' => ['txr_id'],
    ]);

Similarly to `invoicePrice`, you may use the `tabPrice` method to create a one-time charge for multiple items (up to 250 items per invoice) by adding them to the customer's "tab" and then invoicing the customer. For example, we may invoice a customer for five shirts and two mugs:

    $user->tabPrice('price_tshirt', 5);
    $user->tabPrice('price_mug', 2);
    $user->invoice();

Alternatively, you may use the `invoiceFor` method to make a "one-off" charge against the customer's default payment method:

    $user->invoiceFor('One Time Fee', 500);

Although the `invoiceFor` method is available for you to use, it is recommendeded that you use the `invoicePrice` and `tabPrice` methods with pre-defined prices. By doing so, you will have access to better analytics and data within your Stripe dashboard regarding your sales on a per-product basis.

> {note} The `invoice`, `invoicePrice`, and `invoiceFor` methods will create a Stripe invoice which will retry failed billing attempts. If you do not want invoices to retry failed charges, you will need to close them using the Stripe API after the first failed charge.

<a name="refunding-charges"></a>
### Refunding Charges

If you need to refund a Stripe charge, you may use the `refund` method. This method accepts the Stripe [payment intent ID](#payment-methods-for-single-charges) as its first argument:

    $payment = $user->charge(100, $paymentMethodId);

    $user->refund($payment->id);

<a name="invoices"></a>
## Invoices

<a name="retrieving-invoices"></a>
### Retrieving Invoices

You may easily retrieve an array of a billable model's invoices using the `invoices` method. The `invoices` method returns a collection of `Laravel\Cashier\Invoice` instances:

    $invoices = $user->invoices();

If you would like to include pending invoices in the results, you may use the `invoicesIncludingPending` method:

    $invoices = $user->invoicesIncludingPending();

You may use the `findInvoice` method to retrieve a specific invoice by its ID:

    $invoice = $user->findInvoice($invoiceId);

<a name="displaying-invoice-information"></a>
#### Displaying Invoice Information

When listing the invoices for the customer, you may use the invoice's methods to display the relevant invoice information. For example, you may wish to list every invoice in a table, allowing the user to easily download any of them:

    <table>
        @foreach ($invoices as $invoice)
            <tr>
                <td>{{ $invoice->date()->toFormattedDateString() }}</td>
                <td>{{ $invoice->total() }}</td>
                <td><a href="/user/invoice/{{ $invoice->id }}">Download</a></td>
            </tr>
        @endforeach
    </table>

<a name="upcoming-invoices"></a>
### Upcoming Invoices

To retrieve the upcoming invoice for a customer, you may use the `upcomingInvoice` method:

    $invoice = $user->upcomingInvoice();

Similary, if the customer has multiple subscriptions, you can also retrieve the upcoming invoice for a specific subscription:

    $invoice = $user->subscription('default')->upcomingInvoice();

<a name="previewing-subscription-invoices"></a>
### Previewing Subscription Invoices

Using the `previewInvoice` method, you can preview an invoice before making price changes. This will allow you to determine what your customer's invoice will look like when a given price change is made:

    $invoice = $user->subscription('default')->previewInvoice('price_yearly');

You may pass an array of prices to the `previewInvoice` method in order to preview invoices with multiple new prices:

    $invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);

<a name="generating-invoice-pdfs"></a>
### Generating Invoice PDFs

From within a route or controller, you may use the `downloadInvoice` method to generate a PDF download of a given invoice. This method will automatically generate the proper HTTP response needed to download the invoice:

    use Illuminate\Http\Request;

    Route::get('/user/invoice/{invoice}', function (Request $request, $invoiceId) {
        return $request->user()->downloadInvoice($invoiceId, [
            'vendor' => 'Your Company',
            'product' => 'Your Product',
        ]);
    });

By default, all data on the invoice is derived from the customer and invoice data stored in Stripe. However, you can customize some of this data by providing an array as the second argument to the `downloadInvoice` method. This array allows you to customize information such as your company and product details:

    return $request->user()->downloadInvoice($invoiceId, [
        'vendor' => 'Your Company',
        'product' => 'Your Product',
        'street' => 'Main Str. 1',
        'location' => '2000 Antwerp, Belgium',
        'phone' => '+32 499 00 00 00',
        'email' => 'info@example.com',
        'url' => 'https://example.com',
        'vendorVat' => 'BE123456789',
    ], 'my-invoice');

The `downloadInvoice` method also allows for a custom filename via its third argument. This filename will automatically be suffixed with `.pdf`:

    return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');

<a name="custom-invoice-render"></a>
#### Custom Invoice Renderer

Cashier also makes it possible to use a custom invoice renderer. By default, Cashier uses the `DompdfInvoiceRenderer` implementation, which utilizes the [dompdf](https://github.com/dompdf/dompdf) PHP library to generate Cashier's invoices. However, you may use any renderer you wish by implementing the `Laravel\Cashier\Contracts\InvoiceRenderer` interface. For example, you may wish to render an invoice PDF using an API call to a third-party PDF rendering service:

    use Illuminate\Support\Facades\Http;
    use Laravel\Cashier\Contracts\InvoiceRenderer;
    use Laravel\Cashier\Invoice;

    class ApiInvoiceRenderer implements InvoiceRenderer
    {
        /**
         * Render the given invoice and return the raw PDF bytes.
         *
         * @param  \Laravel\Cashier\Invoice. $invoice
         * @param  array  $data
         * @param  array  $options
         * @return string
         */
        public function render(Invoice $invoice, array $data = [], array $options = []): string
        {
            $html = $invoice->view($data)->render();

            return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
        }
    }

Once you have implemented the invoice renderer contract, you should update the `cashier.invoices.renderer` configuration value in your application's `config/cashier.php` configuration file. This configuration value should be set to the class name of your custom renderer implementation.

<a name="checkout"></a>
## Checkout

Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page.

The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout).

<a name="product-checkouts"></a>
### Product Checkouts

You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID:

    use Illuminate\Http\Request;

    Route::get('/product-checkout', function (Request $request) {
        return $request->user()->checkout('price_tshirt');
    });

If needed, you may also specify a product quantity:

    use Illuminate\Http\Request;

    Route::get('/product-checkout', function (Request $request) {
        return $request->user()->checkout(['price_tshirt' => 15]);
    });

When a customer visits this route they will be redirected to Stripe's Checkout page. By default, when a user successfully completes or cancels a purchase they will be redirected to your `home` route location, but you may specify custom callback URLs using the `success_url` and `cancel_url` options:

    use Illuminate\Http\Request;

    Route::get('/product-checkout', function (Request $request) {
        return $request->user()->checkout(['price_tshirt' => 1], [
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
    });

When defining your `success_url` checkout option, you may instruct Stripe to add the checkout session ID as a query string parameter when invoking your URL. To do so, add the literal string `{CHECKOUT_SESSION_ID}` to your `success_url` query string. Stripe will replace this placeholder with the actual checkout session ID:

    use Illuminate\Http\Request;
    use Stripe\Checkout\Session;
    use Stripe\Customer;

    Route::get('/product-checkout', function (Request $request) {
        return $request->user()->checkout(['price_tshirt' => 1], [
            'success_url' => route('checkout-success') . '?session_id={CHECKOUT_SESSION_ID}',
            'cancel_url' => route('checkout-cancel'),
        ]);
    });

    Route::get('/checkout-success', function (Request $request) {
        $checkoutSession = $request->user()->stripe()->checkout->sessions->retrieve($request->get('session_id'));

        return view('checkout.success', ['checkoutSession' => $checkoutSession]);
    })->name('checkout-success');

<a name="checkout-promotion-codes"></a>
#### Promotion Codes

By default, Stripe Checkout does not allow [user redeemable promotion codes](https://stripe.com/docs/billing/subscriptions/discounts/codes). Luckily, there's an easy way to enable these for your Checkout page. To do so, you may invoke the `allowPromotionCodes` method:

    use Illuminate\Http\Request;

    Route::get('/product-checkout', function (Request $request) {
        return $request->user()
            ->allowPromotionCodes()
            ->checkout('price_tshirt');
    });

<a name="single-charge-checkouts"></a>
### Single Charge Checkouts

You can also perform a simple charge for an ad-hoc product that has not been created in your Stripe dashboard. To do so you may use the `checkoutCharge` method on a billable model and pass it a chargeable amount, a product name, and an optional quantity. When a customer visits this route they will be redirected to Stripe's Checkout page:

    use Illuminate\Http\Request;

    Route::get('/charge-checkout', function (Request $request) {
        return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
    });

> {note} When using the `checkoutCharge` method, Stripe will always create a new product and price in your Stripe dashboard. Therefore, we recommend that you create the products up front in your Stripe dashboard and use the `checkout` method instead.

<a name="subscription-checkouts"></a>
### Subscription Checkouts

> {note} Using Stripe Checkout for subscriptions requires you to enable the `customer.subscription.created` webhook in your Stripe dashboard. This webhook will create the subscription record in your database and store all of the relevant subscription items.

You may also use Stripe Checkout to initiate subscriptions. After defining your subscription with Cashier's subscription builder methods, you may call the `checkout `method. When a customer visits this route they will be redirected to Stripe's Checkout page:

    use Illuminate\Http\Request;

    Route::get('/subscription-checkout', function (Request $request) {
        return $request->user()
            ->newSubscription('default', 'price_monthly')
            ->checkout();
    });

Just as with product checkouts, you may customize the success and cancellation URLs:

    use Illuminate\Http\Request;

    Route::get('/subscription-checkout', function (Request $request) {
        return $request->user()
            ->newSubscription('default', 'price_monthly')
            ->checkout([
                'success_url' => route('your-success-route'),
                'cancel_url' => route('your-cancel-route'),
            ]);
    });

Of course, you can also enable promotion codes for subscription checkouts:

    use Illuminate\Http\Request;

    Route::get('/subscription-checkout', function (Request $request) {
        return $request->user()
            ->newSubscription('default', 'price_monthly')
            ->allowPromotionCodes()
            ->checkout();
    });

> {note} Unfortunately Stripe Checkout does not support all subscription billing options when starting subscriptions. Using the `anchorBillingCycleOn` method on the subscription builder, setting proration behavior, or setting payment behavior will not have any effect during Stripe Checkout sessions. Please consult [the Stripe Checkout Session API documentation](https://stripe.com/docs/api/checkout/sessions/create) to review which parameters are available.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout & Trial Periods

Of course, you can define a trial period when building a subscription that will be completed using Stripe Checkout:

    $checkout = Auth::user()->newSubscription('default', 'price_monthly')
        ->trialDays(3)
        ->checkout();

However, the trial period must be at least 48 hours, which is the minimum amount of trial time supported by Stripe Checkout.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### Subscriptions & Webhooks

Remember, Stripe and Cashier update subscription statuses via webhooks, so there's a possibility a subscription might not yet be active when the customer returns to the application after entering their payment information. To handle this scenario, you may wish to display a message informing the user that their payment or subscription is pending.

<a name="collecting-tax-ids"></a>
### Collecting Tax IDs

Checkout also supports collecting a customer's Tax ID. To enable this on a checkout session, invoke the `collectTaxIds` method when creating the session:

    $checkout = $user->collectTaxIds()->checkout('price_tshirt');

When this method is invoked, a new checkbox will be available to the customer that allows them to indicate if they're purchasing as a company. If so, they will have the opportunity to provide their Tax ID number.

> {note} If you have already configured [automatic tax collection](#tax-configuration) in your application's service provider then this feature will be enabled automatically and there is no need to invoke the `collectTaxIds` method.

<a name="handling-failed-payments"></a>
## Handling Failed Payments

Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed.

First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page:

    use Laravel\Cashier\Exceptions\IncompletePayment;

    try {
        $subscription = $user->newSubscription('default', 'price_monthly')
                                ->create($paymentMethod);
    } catch (IncompletePayment $exception) {
        return redirect()->route(
            'cashier.payment',
            [$exception->payment->id, 'redirect' => route('home')]
        );
    }

On the payment confirmation page, the customer will be prompted to enter their credit card information again and perform any additional actions required by Stripe, such as "3D Secure" confirmation. After confirming their payment, the user will be redirected to the URL provided by the `redirect` parameter specified above. Upon redirection, `message` (string) and `success` (integer) query string variables will be added to the URL. The payment page currently supports the following payment method types:

<div class="content-list" markdown="1">

- Credit Cards
- Alipay
- Bancontact
- BECS Direct Debit
- EPS
- Giropay
- iDEAL
- SEPA Direct Debit

</div>

Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [setup Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions.

Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions.

Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance:

    if ($user->hasIncompletePayment('default')) {
        //
    }

    if ($user->subscription('default')->hasIncompletePayment()) {
        //
    }

You can derive the specific status of an incomplete payment by inspecting the `payment` property on the exception instance:

    use Laravel\Cashier\Exceptions\IncompletePayment;

    try {
        $user->charge(1000, 'pm_card_threeDSecure2Required');
    } catch (IncompletePayment $exception) {
        // Get the payment intent status...
        $exception->payment->status;

        // Check specific conditions...
        if ($exception->payment->requiresPaymentMethod()) {
            // ...
        } elseif ($exception->payment->requiresConfirmation()) {
            // ...
        }
    }

<a name="strong-customer-authentication"></a>
## Strong Customer Authentication

If your business or one of your customers is based in Europe you will need to abide by the EU's Strong Customer Authentication (SCA) regulations. These regulations were imposed in September 2019 by the European Union to prevent payment fraud. Luckily, Stripe and Cashier are prepared for building SCA compliant applications.

> {note} Before getting started, review [Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication) as well as their [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication).

<a name="payments-requiring-additional-confirmation"></a>
### Payments Requiring Additional Confirmation

SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions be found can be found in the documentation on [handling failed payments](#handling-failed-payments).

Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification.

<a name="incomplete-and-past-due-state"></a>
#### Incomplete and Past Due State

When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion.

For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status).

<a name="off-session-payment-notifications"></a>
### Off-Session Payment Notifications

Since SCA regulations require customers to occasionally verify their payment details even while their subscription is active, Cashier can send a notification to the customer when off-session payment confirmation is required. For example, this may occur when a subscription is renewing. Cashier's payment notification can be enabled by setting the `CASHIER_PAYMENT_NOTIFICATION` environment variable to a notification class. By default, this notification is disabled. Of course, Cashier includes a notification class you may use for this purpose, but you are free to provide your own notification class if desired:

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```

To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait.

> {note} Notifications will be sent even when customers are manually making a payment that requires additional confirmation. Unfortunately, there is no way for Stripe to know that the payment was done manually or "off-session". But, a customer will simply see a "Payment Successful" message if they visit the payment page after already confirming their payment. The customer will not be allowed to accidentally confirm the same payment twice and incur an accidental second charge.

<a name="stripe-sdk"></a>
## Stripe SDK

Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method:

    $stripeSubscription = $subscription->asStripeSubscription();

    $stripeSubscription->application_fee_percent = 5;

    $stripeSubscription->save();

You may also use the `updateStripeSubscription` method to update a Stripe subscription directly:

    $subscription->updateStripeSubscription(['application_fee_percent' => 5]);

You may invoke the `stripe` method on the `Cashier` class if you would like to use the `Stripe\StripeClient` client directly. For example, you could use this method to access the `StripeClient` instance and retrieve a list of prices from your Stripe account:

    use Laravel\Cashier\Cashier;

    $prices = Cashier::stripe()->prices->all();

<a name="testing"></a>
## Testing

When testing an application that uses Cashier, you may mock the actual HTTP requests to the Stripe API; however, this requires you to partially re-implement Cashier's own behavior. Therefore, we recommend allowing your tests to hit the actual Stripe API. While this is slower, it provides more confidence that your application is working as expected and any slow tests may be placed within their own PHPUnit testing group.

When testing, remember that Cashier itself already has a great test suite, so you should only focus on testing the subscription and payment flow of your own application and not every underlying Cashier behavior.

To get started, add the **testing** version of your Stripe secret to your `phpunit.xml` file:

    <env name="STRIPE_SECRET" value="sk_test_<your-key>"/>

Now, whenever you interact with Cashier while testing, it will send actual API requests to your Stripe testing environment. For convenience, you should pre-fill your Stripe testing account with subscriptions / prices that you may use during testing.

> {tip} In order to test a variety of billing scenarios, such as credit card denials and failures, you may use the vast range of [testing card numbers and tokens](https://stripe.com/docs/testing) provided by Stripe.
