# Laravel Cashier

<<<<<<< HEAD
- [Introduction](#introduction)
- [Configuration](#configuration)
- [Subscribing To A Plan](#subscribing-to-a-plan)
- [Single Charges](#single-charges)
- [No Card Up Front](#no-card-up-front)
- [Swapping Subscriptions](#swapping-subscriptions)
- [Subscription Quantity](#subscription-quantity)
- [Cancelling A Subscription](#cancelling-a-subscription)
- [Resuming A Subscription](#resuming-a-subscription)
- [Checking Subscription Status](#checking-subscription-status)
- [Handling Failed Subscriptions](#handling-failed-subscriptions)
- [Handling Other Stripe Webhooks](#handling-other-stripe-webhooks)
- [Invoices](#invoices)
=======
- [Introdução](#introduction)
- [Configuração](#configuration)
- [Inscrevendo-se em um Plano](#subscribing-to-a-plan)
- [Não requerer cartão de crédito no período Trial](#no-card-up-front)
- [Trocando a assinatura de Plano](#swapping-subscriptions)
- [Subscription Quantity](#subscription-quantity)
- [Reativando uma assinatura](#cancelling-a-subscription)
- [Reativando uma assinatura](#resuming-a-subscription)
- [Verifiacando o Status Da Assinatura](#checking-subscription-status)
- [Lidando com Falha de Pagamentos](#handling-failed-payments)
- [Lidando com Outros Stripes Webhooks](#handling-other-stripe-webhooks)
- [Faturas](#invoices)
>>>>>>> 5.0

<a name="introduction"></a>
## Introdução

Laravel Cashier oferece uma interface expressiva e fluente para [Stripe's](https://stripe.com) sserviços de cobrança de assinatura. Ele ainda lida com quase todo o código de faturamento e subscrição que você tanto reluta em escrever. Além do gerenciamento de assinaturas básicas, o Laravel Cashier pode ligar com cupons, troca de subscrição, subscrição em grandes "quantidades", períodos de carência de cancelamento, até mesmo gerar faturas em PDF.


<a name="configuration"></a>
## Configuração 

#### Composer

Primiero, adicione o pacote Cashier em seu arquivo  `composer.json`:

	"laravel/cashier": "~5.0" (For Stripe SDK ~2.0, and Stripe APIs on 2015-02-18 version and later)
	"laravel/cashier": "~4.0" (For Stripe APIs on 2015-02-18 version and later)
	"laravel/cashier": "~3.0" (For Stripe APIs up to and including 2015-02-16 version)

#### Fornecedor de Serviços (Service Provider)

Após, registre o serviço `Laravel\Cashier\CashierServiceProvider` no seu aquivo de configuralção `app`.

#### Migração

Antes de usar o Cashier, nos precisaremos adicionar varias colunas no seu banco de dados. Não se preocupe, você pode usar o comando Artisan `cashier:table` para criar a migração necessária para criar as colunas. Por examplo, para adicionar a coluna à tabela usuários use `php artisan cashier:table users`. Uma vez que a migração for criada, apenas execute o comando `migrate`.


#### Setup do Modelo

Logo após, adicione a trait `Billable` e os mutators (metódos modificadores de dados "Sets") de dados apropriados na definição do seu modelo.

Após isso, adicione a trait `Billable` e os mutator de dados a definição do seu modelo:

	use Laravel\Cashier\Billable;
	use Laravel\Cashier\Contracts\Billable as BillableContract;

	class User extends Model implements BillableContract {

		use Billable;

		protected $dates = ['trial_ends_at', 'subscription_ends_at'];

	}

#### Chave Stripe

<<<<<<< HEAD
Finally, set your Stripe key in your `services.php` config file:

	'stripe' => [
		'model'  => 'User',
		'secret' => env('STRIPE_API_SECRET'),
	],

Alternatively you can store it in one of your bootstrap files or service providers, such as the `AppServiceProvider`:
=======
Por fim, defina sua chave Stripe em um dos seus arquivos do bootstrap ou nos fornecedores de serviço, como o `AppServiceProvider`: 
>>>>>>> 5.0

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

Se o seu plano tem um período experimental que é ** não ** configurado no Stripe, você tem que definir a data final do período trial manualment após a inscrição: 

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

### Especificando Detalhes Adicionais do Usuário 

Se você gostar de especificar detalhes adicionais dos clientes, você pode fazer, passando-os como segundo argumento para o méotodo `create`:

	$user->subscription('monthly')->create($creditCardToken, [
		'email' => $email, 'description' => 'Our First Customer'
	]);

Para aprender mais sobre os campos adicionais suportados pelo Stripe, dê uma olhada na documentação do Stripe [documentation on customer creation](https://stripe.com/docs/api#create_customer).

<a name="single-charges"></a>
## Single Charges

If you would like to make a "one off" charge against a subscribed customer's credit card, you may use the `charge` method:

	$user->charge(100);

The `charge` method accepts the amount you would like to charge in the **lowest denominator of the currency**. So, for example, the example above will charge 100 cents, or $1.00, against the user's credit card.

The `charge` method accepts an array as its second argument, allowing you to pass any options you wish to the underlying Stripe charge creation:

	$user->charge(100, [
		'source' => $token,
		'receipt_email' => $user->email,
	]);

The `charge` method will return `false` if the charge fails. This typically indicates the charge was denied:

	if ( ! $user->charge(100))
	{
		// The charge was denied...
	}

If the charge is successful, the full Stripe response will be returned from the method.

<a name="no-card-up-front"></a>
## Não requerer cartão de crédito no período Trial

Se sua aplicação ofrecer um período-trial gratís sem a requisão de cartão de crédito para a inscrição, defina a propriedade `cardUpFront` no seu modelo como `false`:

	protected $cardUpFront = false;

Na criação da conta, tenha certeza de definir a data final do período trial no modelo.

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

<a name="swapping-subscriptions"></a>
## Trocando a assinatura de Plano

Para trocar o plano do usuário, use o método `swap`: 

	$user->subscription('premium')->swap();

Se o usuário estiver no período trial, o plano trial será mantido normalmente, Além disso, se a "quantidade" de inscrições do plano existir, também será mantida normalmente. 

<a name="subscription-quantity"></a>
## Quantidade de Inscrições

Algumas vezes a inscrições dos planos são afetadas pela "quatidade". Por exemplo, sua aplicação pode cobrar $10 dólares pode mês por usuário em uma conta. Ta fácilmente incrementar ou decrementar sua quantidade de inscrições, você pode usar o os métodos `increment` e `decrement`:

	$user = User::find(1);

	$user->subscription()->increment();

	// Add five to the subscription's current quantity...
	$user->subscription()->increment(5);

	$user->subscription()->decrement();

	// Subtract five to the subscription's current quantity...
	$user->subscription()->decrement(5);

<a name="cancelling-a-subscription"></a>
## Cancelando uma Inscrição

Cancelar uma inscrição é um passeio no parque. 

	$user->subscription()->cancel();

Quando uma inscrição é cancelada, o Cashier irá automaticamente definir a coluna `subscription_ends_at` no seu banco de dados. Esta coluna é usada para saber quando o método `subscribed` deverá começar a retornar `false`. Por exemplo, se o cliente cancelar a incrição no dia 1º de março, mas a inscrição não foi agendada para terminar até o dia 5º de março, o método `subscribed` continuará a retornar `true` até 5º de março. 

<a name="resuming-a-subscription"></a>
## Reativando uma Assinatura 

Se um usuário tiver cancelado a sua assinatura e você deseja reativa-la, use o método `resume`:

	$user->subscription('monthly')->resume($creditCardToken);

Se  o usuário cancelar a assinatura e, em seguida, reativar a assinatura anterior antes do período da assinatura ter expirado totalmente, o usuário não será cobrado imediatamente. A assinatura deles será simplesmente reativada, e eles serão cobrados no ciclo original de cobranças.

<a name="checking-subscription-status"></a>
## Verifiacando o Status Da Assinatura


<<<<<<< HEAD
To verify that a user is subscribed to your application, use the `subscribed` method:
=======
Para verificar ser o usuário é inscrito na sua aplicação, user o método `subscribed`:
>>>>>>> 5.0

	if ($user->subscribed())
	{
		//
	}

<<<<<<< HEAD
The `subscribed` method makes a great candidate for a [route middleware](/docs/master/middleware):
=======
O método `subscribed` se faz um grande candidato para [route middleware](/docs/5.0/middleware):
>>>>>>> 5.0

	public function handle($request, Closure $next)
	{
		if ($request->user() && ! $request->user()->subscribed())
		{
			return redirect('billing');
		}

		return $next($request);
	}
Você também pode determinar se o usuário ainda está no seu período trial (se for o caso) usando o método `onTrial`:

	if ($user->onTrial())
	{
		//
	}

Para determinar se o usuário foi uma vez foi pagador da assinatura, mas cancelou a mesma, você pode suar o méotodo`cancelled` :

	if ($user->cancelled())
	{
		//
	}
Você pode também determinar se o usuário cancelou a assinatura, mas ainda está no seu prazo de "carência" até sua assinatura expirar. Por exemplo, se o usuário cancelar a assinatura no dia 5º de março e a assinatura estiver agendada para terminar no dia 10º, o usuário está no seu período de "carência" até o dia 10º de março. Note que o método  `subscribed` ainda retornará `true` durante esse período. 

	if ($user->onGracePeriod())
	{
		//
	}
O método `everSubscribed` pode ser usado para determinar se o usuário ja foi assinou algum plano da sua aplicação. 

	if ($user->everSubscribed())
	{
		//
	}
O método `onPlan` pode ser usado para determinar se o usuário é inscrito em determinado plano baseado pelo seu ID:

	if ($user->onPlan('monthly'))
	{
		//
	}

<<<<<<< HEAD
<a name="handling-failed-subscriptions"></a>
## Handling Failed Subscriptions
=======
<a name="handling-failed-payments"></a>
## Lidando com Falha de Pagamentos 
>>>>>>> 5.0

Se o cartão de crédito do cliente experar? Não se preocupe - Cashier inclui controlador Webhook que pode facilmente cancelar a assinatura do cliente para você. Basta apontar uma rota para o controlador. 

	Route::post('stripe/webhook', 'Laravel\Cashier\WebhookController@handleWebhook');

<<<<<<< HEAD
That's it! Failed payments will be captured and handled by the controller. The controller will cancel the customer's subscription when Stripe determines the subscription has failed (normally after three failed payment attempts). The `stripe/webhook` URI in this example is just for example. You will need to configure the URI in your Stripe settings.
=======

É isto! Falhas de pagamento irão ser capturadas e manipula-las pelo controlador. O controlador irá cancelar a assinatura do cliente depois de três tentativas falhas. A URI `stripe/webhook` neste exemplo é apenas ilustrativa. Você precisará configurar a URI nas suas configurações do Stripe. 
>>>>>>> 5.0

<a name="handling-other-stripe-webhooks"></a>
## Lidando com Outros Stripes Webhooks

Se você tem eventos webhook Stripe adicionais você deve gostar de lidar com isso, simplesmente extendendo do controlador(controller) Webhook. Os nomes dos seus métodos devem corresponder a convenção esperada do Cashier, especificamente, métodos devem ser préfixados com `handle` e o nome do webhook Stripe que você deseja manipular. Por exemplo, se você quer lidar com o Webhook `invoice.payment_succeeded`, você deve adicionar o método `handleInvoicePaymentSucceeded` ao controlador. 

	class WebhookController extends Laravel\Cashier\WebhookController {

		public function handleInvoicePaymentSucceeded($payload)
		{
			// Handle The Event
		}

	}

> **Nota:** Além de atualizar as informações de assinatura em seu banco de dados, o controlador Webhook também irá cancelar a assinatura através da API Stripe.

<a name="invoices"></a>
## Faturas

Você pode facilmente pode recuperar um array de faturas dos usuários com o método `invoices`:

	$invoices = $user->invoices();

Para listar as faturas para o cliente, você pode usar os seguintes métodos helpers para exibir as informações relevantes das faturas:

	{{ $invoice->id }}

	{{ $invoice->dateString() }}

	{{ $invoice->dollars() }}

Use o método `downloadInvoice` para gerar um download da fatura em PDF. Sim, é realmente fácil assim:

	return $user->downloadInvoice($invoice->id, [
		'vendor'  => 'Your Company',
		'product' => 'Your Product',
	]);
