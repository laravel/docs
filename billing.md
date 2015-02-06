# Laravel Cashier

- [介紹](#introduction)
- [設定檔](#configuration)
- [訂購方案](#subscribing-to-a-plan)
- [免信用卡試用](#no-card-up-front)
- [訂購轉換](#swapping-subscriptions)
- [訂購數量](#subscription-quantity)
- [取消訂購](#cancelling-a-subscription)
- [恢復訂購](#resuming-a-subscription)
- [確認訂購狀態](#checking-subscription-status)
- [處理交易失敗](#handling-failed-payments)
- [處理其它 Stripe Webhooks](#handling-other-stripe-webhooks)
- [收據](#invoices)

<a name="introduction"></a>
## 介紹

Laravel Cashier 提供口語化，流暢的介面和 [Stripe](https://stripe.com) 的訂購管理服務介接。它幾乎處理了所有讓人退步三舍的訂購管理相關邏輯。除了基本的訂購管理，Cashier 還可以處理折價券，訂購轉換，管理訂購「數量」、服務有效期限，甚至產生收據的 PDF。

<a name="configuration"></a>
## 設定檔

#### Composer

首先，把 Cashier 套件加到 `composer.json`：

	"laravel/cashier": "~3.0"

#### 註冊服務

再來，在 `app` 設定檔註冊 `Laravel\Cashier\CashierServiceProvider`。

#### 遷移

使用 Cashier 前，我們需要增加幾個欄位到資料庫。別擔心，你可以使用 `cashier:table` Artisan 命令，建立遷移檔來新增必要欄位。例如，要增加欄位到 users 資料表，使用 `php artisan cashier:table users`。建立完遷移檔後，只要執行 `migrate` 命令即可。

#### 設定模型

再來，把 `Billable` trait 和相關的日期欄位參數加到模型裡：

	use Laravel\Cashier\Billable;
	use Laravel\Cashier\Contracts\Billable as BillableContract;

	class User extends Eloquent implements BillableContract {

		use Billable;

		protected $dates = ['trial_ends_at', 'subscription_ends_at'];

	}

#### Stripe Key

最後，在起始檔或服務註冊裡（像是 `AppServiceProvider` ）加入 Stripe key：

	User::setStripeKey('stripe-key');

<a name="subscribing-to-a-plan"></a>
## 訂購方案

當有了模型實例，你可以很簡單的處理客戶訂購的 Stripe 裡的方案：

	$user = User::find(1);

	$user->subscription('monthly')->create($creditCardToken);

如果你想在建立訂購的時候使用折價券，可以使用 `withCoupon` 方法：

	$user->subscription('monthly')
	     ->withCoupon('code')
	     ->create($creditCardToken);

`subscription` 方法會自動建立與 Stripe 的交易，以及將 Stripe customer ID 和其他相關帳款資訊更新到資料庫。如果你的方案有在 Stripe 設定試用期，試用到期日也會自動記錄起來。

如果你的方案有試用期間，但是**沒有**在 Stripe 裡設定，你必須在處理訂購後手動儲存試用到期日。

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

### 自定額外使用者詳細資料

如果你想自定額外的顧客詳細資料，你可以將資料陣列作為 `create` 方法的第二個參數傳入：

	$user->subscription('monthly')->create($creditCardToken, [
		'email' => $email, 'description' => 'Our First Customer'
	]);

想知道更多 Stripe 支援的額外欄位，瞧瞧 Stripe 的線上文件 [建立客戶](https://stripe.com/docs/api#create_customer)。

<a name="no-card-up-front"></a>
## 免信用卡試用

如果你提供免信用卡試用服務，把 `cardUpFront` 屬性設為 `false`：

	protected $cardUpFront = false;

建立帳號時，記得把試用到期日記錄起來：

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

<a name="swapping-subscriptions"></a>
## 訂購轉換

使用 `swap` 方法可以把使用者轉換到新的訂購：

	$user->subscription('premium')->swap();

如果使用者還在試用期間，試用服務會跟之前一樣可用。如果訂單有「數量」，也會和之前一樣。

<a name="subscription-quantity"></a>
## 訂購數量

有時候訂購行為會跟「數量」有關。例如，你的應用程式可能會依照帳號的使用者人數，每人每月收取 $10 元。你可以使用 `increment` 和 `decrement` 方法簡單的調整訂購數量：

	$user = User::find(1);

	$user->subscription()->increment();

	// Add five to the subscription's current quantity...
	$user->subscription()->increment(5);

	$user->subscription->decrement();

	// Subtract five to the subscription's current quantity...
	$user->subscription()->decrement(5);

<a name="cancelling-a-subscription"></a>
## 取消訂購

取消訂購相當簡單：

	$user->subscription()->cancel();

當客戶取消訂購時，Cashier 會自動更新資料庫的 `subscription_ends_at` 欄位。這個欄位會被用來判斷 `subscribed` 方法是否該回傳 `false`。例如，如果顧客在三月一號取消訂購，但是服務可以使用到三月五號為止，那麼 `subscribed` 方法在三月五號前都會傳回 `true`。

<a name="resuming-a-subscription"></a>
## 恢復訂購

如果你想要恢復客戶之前取消的訂購，使用 `resume` 方法：

	$user->subscription('monthly')->resume($creditCardToken);

如果客戶取消訂購後，在服務過期前恢復，他們不用在當下付款。他們的服務會立刻重啟，而付款則會循平常的流程。

<a name="checking-subscription-status"></a>
## 確認訂購狀態

要確認使用者是否訂購了服務，使用 `subscribed` 方法：

	if ($user->subscribed())
	{
		//
	}

`subscribed` 方法很適合用在 [route middleware](/docs/5.0/middleware):

	public function handle($request, Closure $next)
	{
		if ($request->user() && ! $request->user()->subscribed())
		{
			return redirect('billing');
		}

		return $next($request);
	}

你可以使用 `onTrial` 方法，確認使用者是否還在試用期間：

	if ($user->onTrial())
	{
		//
	}

要確認使用者是否曾經訂購但是已經取消了服務，可已使用 `cancelled` 方法：

	if ($user->cancelled())
	{
		//
	}

你可以可能想確認使用者是否已經取消訂單，但是服務還沒有到期。例如，如果使用者在三月五號取消了訂購，但是服務會到三月十號才過期。那麼使用者到三月十號前都是有效期間。注意， `subscribed` 方法在過期前都會回傳 `true` 。

	if ($user->onGracePeriod())
	{
		//
	}

`everSubscribed` 方法可以用來確認使用者是否訂購過應用程式裡的方案：

	if ($user->everSubscribed())
	{
		//
	}

`onPlan` 方法可以用方案 ID 來確認使用者是否訂購某方案：

	if ($user->onPlan('monthly'))
	{
		//
	}

<a name="handling-failed-payments"></a>
## 處理交易失敗

如果顧客的信用卡過期了呢？無需擔心，Cashier 包含了 Webhook 控制器，可以幫你簡單的取消顧客的訂單。只要在路由註冊控制器：

	Route::post('stripe/webhook', 'Laravel\Cashier\WebhookController@handleWebhook');

這樣就成了！失敗的交易會經由控制器捕捉並進行處理。控制器會進行至多三次再交易嘗試，都失敗後才會取消顧客的訂單。上面的 `stripe/webhook` URI 只是一個範例，你必須使用設定在 Stripe 裡的 URI 才行。

<a name="handling-other-stripe-webhooks"></a>
## 處理其它 Stripe Webhooks

如果你想要處理額外的 Stripe webhook 事件，可以繼承 Webhook 控制器。你的方法名稱要對應到 Cashier 預期的名稱，尤其是方法名稱應該使用 `handle` 前綴，後面接著你想要處理的 Stripe webhook 。例如，如果你想要處理 `invoice.payment_succeeded` webhook ，你應該增加一個 `handleInvoicePaymentSucceeded` 方法到控制器。

	class WebhookController extends Laravel\Cashier\WebhookController {

		public function handleInvoicePaymentSucceeded($payload)
		{
			// Handle The Event
		}

	}

> **注意：** 除了更新你資料庫裡的訂購資訊以外， Webhook 控制器也會經由 Stripe API 取消你的訂購。

<a name="invoices"></a>
## 收據

你可以很簡單的經由 `invoices` 方法拿到客戶的收據資料陣列：

	$invoices = $user->invoices();

你可以使用這些輔助方法，列出收據的相關資訊給客戶看：

	{{ $invoice->id }}

	{{ $invoice->dateString() }}

	{{ $invoice->dollars() }}

使用 `downloadInvoice` 方法產生收據的 PDF 下載。是的，它非常容易：

	return $user->downloadInvoice($invoice->id, [
		'vendor'  => 'Your Company',
		'product' => 'Your Product',
	]);
