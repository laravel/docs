# Laravel Cashier

- [Introdução](#introduction)
- [Configuração](#configuration)
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
## Introdução

Laravel Cashier oferece uma interface expressiva e fluente para [Stripe's](https://stripe.com) sserviços de cobrança de assinatura. Ele ainda lida com quase todo o código de faturamento e subscrição que você tanto reluta em escrever. Além do gerenciamento de assinaturas básicas, o Laravel Cashier pode ligar com cupons, troca de subscrição, subscrição em grandes "quantidades", períodos de carência de cancelamento, até mesmo gerar faturas em PDF.


<a name="configuration"></a>
## Configuração 

#### Composer

Primiero, adicione o pacote Cashier em seu arquivo  `composer.json`:

	"laravel/cashier": "~3.0"

#### Fornecedor de Serviços (Service Provider)

Após, registre o serviço `Laravel\Cashier\CashierServiceProvider` no seu aquivo de configuralção `app`.

#### Migração

Antes de usar o Cashier, nos precisaremos adicionar varias colunas no seu banco de dados. Não se preocupe, você pode usar o comando Artisan `cashier:table` para criar a migração necessária para criar as colunas. Por examplo, para adicionar a coluna à tabela usuários use `php artisan cashier:table users`. Uma vez que a migração for criada, apenas execute o comando `migrate`.


#### Setup do Modelo

Logo após, adicione a trait `Billable` e os mutators (metódos modificadores de dados "Sets") de dados apropriados na definição do seu modelo.

Após isso, adicione a trait `Billable` e os mutator de dados a definição do seu modelo:

	use Laravel\Cashier\Billable;
	use Laravel\Cashier\Contracts\Billable as BillableContract;

	class User extends Eloquent implements BillableContract {

		use Billable;

		protected $dates = ['trial_ends_at', 'subscription_ends_at'];

	}

#### Chave Stripe

Por fim, defina sua chave Stripe em um dos seus arquivos do bootstrap ou nos fornecedores de serviço, como o `AppServiceProvider`: 

	User::setStripeKey('stripe-key');

<a name="subscribing-to-a-plan"></a>
## Inscrevendo-se em um Plano.
Uma vez que você tenha uma instacia do seu modelo, você pode facilmente inscrever este usuário para um plano do Stripe. 

	$user = User::find(1);

	$user->subscription('monthly')->create($creditCardToken);
	
Se você desejar aplica algum cupon quando estiver criando a inscrição, você pode usar o método `withCoupon`:

	$user->subscription('monthly')
	     ->withCoupon('code')
	     ->create($creditCardToken);

O método `subscription` irá criar uma inscrição no Stripe automaticamente, bem como atualizar o seu banco de dados com o ID do cliente e outras informações importantes faturamento. Se seu plano foi configurado como trial(tempporário) no Stripe, a data final do trial será automaticamente definida no registro do usuário.

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

	$user->subscription->decrement();

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

The `subscribed` method makes a great candidate for a [route middleware](/docs/5.0/middleware):

	public function handle($request, Closure $next)
	{
		if ($request->user() && ! $request->user()->subscribed())
		{
			return redirect('billing');
		}

		return $next($request);
	}

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
