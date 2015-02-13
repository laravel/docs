# Command Bus

- [简介](#introduction)
- [建立命令](#creating-commands)
- [派送命令](#dispatching-commands)
- [命令队列](#queued-commands)
- [命令管线](#command-pipeline)

<a name="introduction"></a>
## 简介

Command bus 提供一个简便的方法来封装任务，使你的程序更加容易阅读与执行，为了帮助我们更加了解使用「命令」的目的，让我们来仿真建立一个可以购买 podcast 的网站。

用户购买 podcasts 的过程中需要做很多事。例如，我们需要从用户的信用卡扣款，将纪录添加到数据库以表示购买，并发送购买确认的电子邮件，或许，我们还需要进行许多验证来确认用户是否可以购买。

我们可以将这些逻辑通通放在控制器的方法内，然而，这样做会有一些缺点，首先，控制器可能还需要处理许多其他的 HTTP 动作，包含复杂的逻辑，这会让控制器变得很肥大且难易阅读，第二点，这些逻辑无法在这个控制器以外被重复使用，第三，这些命令无法被单元测试，为此我们还得额外产生一个 HTTP 请求，并向网站进行完整购买 podcast 的流程。

比起将逻辑放在控制器内，我们可以选择使用一个「命令」对象来封装它，像是 `PurchasePodcast` 命令。

<a name="creating-commands"></a>
## 建立命令

使用 `make:command` 这个 Artisan 指令可以产生一个新的命令类别 ：

	php artisan make:command PurchasePodcast

新产生的类别会被放在 `app/Commands` 目录中，命令缺省包含了两个方法：建构子和 `handle` 。当然，`handle` 方法执行命令时，你可以使用建构子传入相关的对象到这个命令中。例如：

	class PurchasePodcast extends Command implements SelfHandling {

		protected $user, $podcast;

		/**
		 * Create a new command instance.
		 *
		 * @return void
		 */
		public function __construct(User $user, Podcast $podcast)
		{
			$this->user = $user;
			$this->podcast = $podcast;
		}

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle()
		{
			// Handle the logic to purchase the podcast...

			event(new PodcastWasPurchased($this->user, $this->podcast));
		}

	}
	
`handle` 方法也可以使用型别暗示相依，并且借由 [IoC 容器](/docs/5.0/container) 机制自动进行依赖注入。例如：

		/**
		 * Execute the command.
		 *
		 * @return void
		 */
		public function handle(BillingGateway $billing)
		{
			// Handle the logic to purchase the podcast...
		}

<a name="dispatching-commands"></a>
## 派送命令

所以，我们建立的命令该如何派送它呢？当然，我们可以直接调用 `handle` 方法，然而使用 Laravel 的 "command bus" 来派送命令将会有许多优点，待会我们会讨论这个部分。

如果你有浏览过内置的基本控制器，将会发现 `DispatchesCommands` trait ，它将允许我们在控制器内调用 `dispatch` 方法，例如：

	public function purchasePodcast($podcastId)
	{
		$this->dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);
	}

Command bus 将会负责执行命令和调用 IoC 容器来将所需的相依注入到 `handle` 方法。

你也可以将 `Illuminate\Foundation\Bus\DispatchesCommands` trait 加入任何要使用的类别内。若你想要在任何类别的建构子内接收 command bus 的实体 ，你可以使用型别暗示 `Illuminate\Contracts\Bus\Dispatcher` 这个接口。
最后，你也可以使用 `Bus` facade 来快速派发命令：

		Bus::dispatch(
			new PurchasePodcast(Auth::user(), Podcast::findOrFail($podcastId))
		);

### 从请求映射要注入命令的属性

映射 HTTP 请求到命令是很常见的，所以，与其要你针对每个请求苦命地进行手动对应，Laravel 则提供一些有用的方法来轻松达到，让我们来看一下 `DispatchesCommands` trait 提供的 `dispatchFrom` 方法：

	$this->dispatchFrom('Command\Class\Name', $request);

这个方法将会检查这个被传入的命令类别的建构子，并取出来自于 HTTP 请求的变量(或其他任何的 `ArrayAccess` 对象) 并将其填入建构子，所以，若命令类在建构子接受 `firstName` 参数，command bus 将会试图从 HTTP 请求取出 `firstName` 参数。

`dispatchFrom` 方法的第三个参数允许你传入数组，那些不在 HTTP 请求内的参数可用这个数组来填入建构子：

	$this->dispatchFrom('Command\Class\Name', $request, [
		'firstName' => 'Taylor',
	]);

<a name="queued-commands"></a>
## 命令队列

Command bus 不仅仅作为当下请求的同步作业，也可以作为 Laravel 队列任务的主要方法，所以，我们要如何指示 command bus 在背景作业而不是同步处理呢？非常简单，首先，在建立新的命令时加上 `--queued` 参数：

	php artisan make:command PurchasePodcast --queued

正如你所见的，这让命令增加了一点功能，即 `Illuminate\Contracts\Queue\ShouldBeQueued` 接口和`SerializesModels` trait 。 他们指示 command bus 使用队列来执行命令，以及优雅的串行化和反串行化任何在命令内被保存的 Eloquent 模型。

若你想将已存在的命令转换为队列命令，只需手动修改让命令类别实作 `Illuminate\Contracts\Queue\ShouldBeQueued` 接口，它不包含方法，而是仅仅给调度员作为"标记接口"。

然后，一如往常撰写你的命令，当你将命令派发到 bus，它将会自动将命令丢到背景队列执行，没有比这个更容易的方法了。

想了解更多关于队列命令的方法，请见[队列文档](/docs/5.0/queues).

<a name="command-pipeline"></a>
## 命令管线

在命令被派发到处理器之前，你也可以将它借由"命令管线"传递到其他类别去。命令管线操作上像是 HTTP 中介层，除了是专门来给命令用的，例如，一个命令管线能够在数据库交易期间包装全部的命令操作，或者仅作为执行纪录。

要将管线添加到 bus，只要从`App\Providers\BusServiceProvider::boot` 方法调用调度员的`pipeThrough` 方法：

	$dispatcher->pipeThrough(['UseDatabaseTransactions', 'LogCommand']);

一个命令管线被定义在 `handle` 方法，就像是个中介层：

	class UseDatabaseTransactions {

		public function handle($command, $next)
		{
			return DB::transaction(function() use ($command, $next)
			{
				return $next($command);
			}
		}

	}

命令管线是透过 IoC 容器来达成，所以请自行在建构子型别暗示所需的相依。

你甚至可以定义一个 `闭包` 来作为命令管线：

	$dispatcher->pipeThrough([function($command, $next)
	{
		return DB::transaction(function() use ($command, $next)
		{
			return $next($command);
		}
	}]);
