# Laravel Cashier

- [介绍](#introduction)
- [设置档](#configuration)
- [订购方案](#subscribing-to-a-plan)
- [免信用卡试用](#no-card-up-front)
- [订购转换](#swapping-subscriptions)
- [订购数量](#subscription-quantity)
- [取消订购](#cancelling-a-subscription)
- [恢复订购](#resuming-a-subscription)
- [确认订购状态](#checking-subscription-status)
- [处理交易失败](#handling-failed-payments)
- [处理其它 Stripe Webhooks](#handling-other-stripe-webhooks)
- [收据](#invoices)

<a name="introduction"></a>
## 介绍

Laravel Cashier 提供口语化，流畅的接口和 [Stripe](https://stripe.com) 的订购管理服务介接。它几乎处理了所有让人退步三舍的订购管理相关逻辑。除了基本的订购管理，Cashier 还可以处理折价券，订购转换，管理订购「数量」、服务有效期限，甚至产生收据的 PDF。

<a name="configuration"></a>
## 设置档

#### Composer

首先，把 Cashier 套件加到 `composer.json`：

	"laravel/cashier": "~3.0"

#### 注册服务

再来，在 `app` 设置档注册 `Laravel\Cashier\CashierServiceProvider`。

#### 迁移

使用 Cashier 前，我们需要增加几个字段到数据库。别担心，你可以使用 `cashier:table` Artisan 命令，建立迁移档来添加必要字段。例如，要增加字段到 users 数据表，使用 `php artisan cashier:table users`。建立完迁移档后，只要执行 `migrate` 命令即可。

#### 设置模型

再来，把 `Billable` trait 和相关的日期字段参数加到模型里：

	use Laravel\Cashier\Billable;
	use Laravel\Cashier\Contracts\Billable as BillableContract;

	class User extends Eloquent implements BillableContract {

		use Billable;

		protected $dates = ['trial_ends_at', 'subscription_ends_at'];

	}

#### Stripe Key

最后，在起始档或服务注册里（像是 `AppServiceProvider` ）加入 Stripe key：

	User::setStripeKey('stripe-key');

<a name="subscribing-to-a-plan"></a>
## 订购方案

当有了模型实例，你可以很简单的处理客户订购的 Stripe 里的方案：

	$user = User::find(1);

	$user->subscription('monthly')->create($creditCardToken);

如果你想在建立订购的时候使用折价券，可以使用 `withCoupon` 方法：

	$user->subscription('monthly')
	     ->withCoupon('code')
	     ->create($creditCardToken);

`subscription` 方法会自动建立与 Stripe 的交易，以及将 Stripe customer ID 和其他相关帐款信息更新到数据库。如果你的方案有在 Stripe 设置试用期，试用到期日也会自动记录起来。

如果你的方案有试用期间，但是**没有**在 Stripe 里设置，你必须在处理订购后手动保存试用到期日。

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

### 自定额外用户详细数据

如果你想自定额外的顾客详细数据，你可以将数据数组作为 `create` 方法的第二个参数传入：

	$user->subscription('monthly')->create($creditCardToken, [
		'email' => $email, 'description' => 'Our First Customer'
	]);

想知道更多 Stripe 支持的额外字段，瞧瞧 Stripe 的在线文档 [建立客户](https://stripe.com/docs/api#create_customer)。

<a name="no-card-up-front"></a>
## 免信用卡试用

如果你提供免信用卡试用服务，把 `cardUpFront` 属性设为 `false`：

	protected $cardUpFront = false;

建立帐号时，记得把试用到期日记录起来：

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

<a name="swapping-subscriptions"></a>
## 订购转换

使用 `swap` 方法可以把用户转换到新的订购：

	$user->subscription('premium')->swap();

如果用户还在试用期间，试用服务会跟之前一样可用。如果订单有「数量」，也会和之前一样。

<a name="subscription-quantity"></a>
## 订购数量

有时候订购行为会跟「数量」有关。例如，你的应用程序可能会依照帐号的用户人数，每人每月收取 $10 元。你可以使用 `increment` 和 `decrement` 方法简单的调整订购数量：

	$user = User::find(1);

	$user->subscription()->increment();

	// Add five to the subscription's current quantity...
	$user->subscription()->increment(5);

	$user->subscription->decrement();

	// Subtract five to the subscription's current quantity...
	$user->subscription()->decrement(5);

<a name="cancelling-a-subscription"></a>
## 取消订购

取消订购相当简单：

	$user->subscription()->cancel();

当客户取消订购时，Cashier 会自动更新数据库的 `subscription_ends_at` 字段。这个字段会被用来判断 `subscribed` 方法是否该回传 `false`。例如，如果顾客在三月一号取消订购，但是服务可以使用到三月五号为止，那么 `subscribed` 方法在三月五号前都会传回 `true`。

<a name="resuming-a-subscription"></a>
## 恢复订购

如果你想要恢复客户之前取消的订购，使用 `resume` 方法：

	$user->subscription('monthly')->resume($creditCardToken);

如果客户取消订购后，在服务过期前恢复，他们不用在当下付款。他们的服务会立刻重启，而付款则会循平常的流程。

<a name="checking-subscription-status"></a>
## 确认订购状态

要确认用户是否订购了服务，使用 `subscribed` 方法：

	if ($user->subscribed())
	{
		//
	}

`subscribed` 方法很适合用在 [route middleware](/docs/5.0/middleware):

	public function handle($request, Closure $next)
	{
		if ($request->user() && ! $request->user()->subscribed())
		{
			return redirect('billing');
		}

		return $next($request);
	}

你可以使用 `onTrial` 方法，确认用户是否还在试用期间：

	if ($user->onTrial())
	{
		//
	}

要确认用户是否曾经订购但是已经取消了服务，可已使用 `cancelled` 方法：

	if ($user->cancelled())
	{
		//
	}

你可以可能想确认用户是否已经取消订单，但是服务还没有到期。例如，如果用户在三月五号取消了订购，但是服务会到三月十号才过期。那么用户到三月十号前都是有效期间。注意， `subscribed` 方法在过期前都会回传 `true` 。

	if ($user->onGracePeriod())
	{
		//
	}

`everSubscribed` 方法可以用来确认用户是否订购过应用程序里的方案：

	if ($user->everSubscribed())
	{
		//
	}

`onPlan` 方法可以用方案 ID 来确认用户是否订购某方案：

	if ($user->onPlan('monthly'))
	{
		//
	}

<a name="handling-failed-payments"></a>
## 处理交易失败

如果顾客的信用卡过期了呢？无需担心，Cashier 包含了 Webhook 控制器，可以帮你简单的取消顾客的订单。只要在路由注册控制器：

	Route::post('stripe/webhook', 'Laravel\Cashier\WebhookController@handleWebhook');

这样就成了！失败的交易会经由控制器捕捉并进行处理。控制器会进行至多三次再交易尝试，都失败后才会取消顾客的订单。上面的 `stripe/webhook` URI 只是一个范例，你必须使用设置在 Stripe 里的 URI 才行。

<a name="handling-other-stripe-webhooks"></a>
## 处理其它 Stripe Webhooks

如果你想要处理额外的 Stripe webhook 事件，可以继承 Webhook 控制器。你的方法名称要对应到 Cashier 预期的名称，尤其是方法名称应该使用 `handle` 前缀，后面接着你想要处理的 Stripe webhook 。例如，如果你想要处理 `invoice.payment_succeeded` webhook ，你应该增加一个 `handleInvoicePaymentSucceeded` 方法到控制器。

	class WebhookController extends Laravel\Cashier\WebhookController {

		public function handleInvoicePaymentSucceeded($payload)
		{
			// Handle The Event
		}

	}

> **注意：** 除了更新你数据库里的订购信息以外， Webhook 控制器也会经由 Stripe API 取消你的订购。

<a name="invoices"></a>
## 收据

你可以很简单的经由 `invoices` 方法拿到客户的收据数据数组：

	$invoices = $user->invoices();

你可以使用这些辅助方法，列出收据的相关信息给客户看：

	{{ $invoice->id }}

	{{ $invoice->dateString() }}

	{{ $invoice->dollars() }}

使用 `downloadInvoice` 方法产生收据的 PDF 下载。是的，它非常容易：

	return $user->downloadInvoice($invoice->id, [
		'vendor'  => 'Your Company',
		'product' => 'Your Product',
	]);
