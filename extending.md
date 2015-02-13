# 扩展框架

- [管理者和工厂](#managers-and-factories)
- [缓存](#cache)
- [Session](#session)
- [认证](#authentication)
- [基于 IoC 的扩展](#ioc-based-extension)

<a name="managers-and-factories"></a>
## 管理者和工厂

Laravel 有几个 `Manager` 类别，用来管理创建基于驱动的组件。这些类别包括缓存、session 、认证和队列组件。管理者类别负责基于应用程序的设置建立一个特定的驱动实作。例如，`CacheManager` 类别可以建立 APC 、 Memcached 、文件和各种其他的缓存驱动实作。

这些管理者都拥有 `extend` 方法，可以简单地用它来注入新的驱动解析功能到管理者。我们将会在下面的例子，随着如何注入客制化驱动支持给它们，涵盖这些管理者的内容。

> **注意：** 建议花点时间来探索 Laravel 附带的各种 `Manager` 类别，例如：`CacheManager` 和 `SessionManager`。看过这些类别将会让你更彻底了解 Laravel 表面下是如何运作。所有的管理者类别继承  `Illuminate\Support\Manager` 基底类别，它提供一些有用、常见的功能给每一个管理者。

<a name="cache"></a>
## 缓存

为了扩展 Laravel 缓存功能，我们将会使用 `CacheManager` 的 `extend` 方法，这方法可以用来绑定一个客制化驱动解析器到管理者，并且是全部的管理者类别通用的。例如，注册一个新的缓存驱动名为「mongo」，我们将执行以下操作：

	Cache::extend('mongo', function($app)
	{
		return Cache::repository(new MongoStore);
	});

传递到 `extend` 方法的第一个参数是驱动的名称。这将会对应到你的 `config/cache.php` 设置档里的 `driver` 选项。第二个参数是个应该回传 `Illuminate\Cache\Repository` 实例的闭包。 `$app` 将会被传递到闭包，它是 `Illuminate\Foundation\Application` 和 IoC 容器的实例。

`Cache::extend` 的调用可以在新的 Laravel 应用程序缺省附带的 `App\Providers\AppServiceProvider` 的 `boot` 方法中完成，或者你可以建立自己的服务提供者来放置这个扩展 - 记得不要忘记在 `config/app.php` 的提供者数组注册提供者。

要建立客制化缓存驱动，首先需要实作 `Illuminate\Contracts\Cache\Store` contract 。所以，我们的 MongoDB 缓存实作将会看起来像这样：

	class MongoStore implements Illuminate\Contracts\Cache\Store {

		public function get($key) {}
		public function put($key, $value, $minutes) {}
		public function increment($key, $value = 1) {}
		public function decrement($key, $value = 1) {}
		public function forever($key, $value) {}
		public function forget($key) {}
		public function flush() {}

	}

我们只需要使用 MongoDB 连接来实作这些方法。当实作完成，就可以完成客制化驱动注册：

	Cache::extend('mongo', function($app)
	{
		return Cache::repository(new MongoStore);
	});

如果你正在考虑要把客制化缓存驱动代码放在哪里，请考虑把它放上  Packagist ！或者，你可以在 `app` 的目录中建立 `Extensions` 命名空间。记得 Laravel 没有严格的应用程序架构，你可以依照喜好自由的组织应用程序。

<a name="session"></a>
## Session

以客制化 session 驱动来扩展 Laravel 跟扩展缓存系统一样简单。再一次的，我们将会使用 `extend` 方法来注册客制化代码：

	Session::extend('mongo', function($app)
	{
		// Return implementation of SessionHandlerInterface
	});

### 在哪里扩展 Session

你应该把 session 扩展代码放置在 `AppServiceProvider` 的 `boot` 方法里。

### 实作 Session 扩展

要注意我们的客制化缓存驱动应该要实作 `SessionHandlerInterface` 。这个接口只包含少数需要实作的简单方法。一个基本的 MongoDB 实作会看起来像这样：

	class MongoHandler implements SessionHandlerInterface {

		public function open($savePath, $sessionName) {}
		public function close() {}
		public function read($sessionId) {}
		public function write($sessionId, $data) {}
		public function destroy($sessionId) {}
		public function gc($lifetime) {}

	}

因为这些方法不像缓存的 `StoreInterface` 一样容易理解，让我们快速地看过这些方法做些什么：

- `open` 方法通常会被用在基于文件的 session 保存系统。因为 Laravel 附带一个 `file` session 驱动，几乎不需要在这个方法放任何东西。你可以让它留空。PHP 要求我们去实作这个方法，事实上明显是个差劲的接口设计 (我们将会晚点讨论它)。
- `close` 方法，就像 `open` 方法，通常也可以忽略。对大部份的驱动来说，并不需要它。
- `read` 方法应该回传与给定 `$sessionId` 关联的 session 数据的字串形态。当你的驱动取回或保存 session 数据时不需要做任何串行化或进行其他编码，因为 Laravel 将会为你进行串行化
- `write` 方法应该写入给定 `$data` 字串与 `$sessionId` 的关联到一些永久存储系统，例如：MongoDB、 Dynamo、等等。
- `destroy` 方法应该从永久存储移除与 `$sessionId` 关联的数据。
- `gc` 方法应该销毁所有比给定 `$lifetime` UNIX 时间戳记还旧的 session 数据。对于会自己过期的系统如 Memcached 和 Redis，这个方法可以留空。

当 `SessionHandlerInterface` 实作完成，我们准备好要用 Session 管理者注册它：

	Session::extend('mongo', function($app)
	{
		return new MongoHandler;
	});

当 session 驱动已经被注册，我们可以在 `config/session.php` 设置档使用 `mongo` 驱动。

> **注意：** 记住，如果你写了个客制化 session 处理器，请在 Packagist 分享它！

<a name="authentication"></a>
## 认证

认证可以用与缓存和 session 功能相同的方法扩展。再一次的，使用我们已经熟悉的 `extend` 方法：

	Auth::extend('riak', function($app)
	{
		// 回传 Illuminate\Contracts\Auth\UserProvider 的实作
	});

`UserProvider` 实作只负责从永久存储系统抓取 `Illuminate\Contracts\Auth\Authenticatable` 实作，存储系统例如： MySQL 、 Riak ，等等。这两个接口让 Laravel 认证机制无论用户数据如何保存或用什么种类的类别来代表它都能继续运作。

让我们来看一下 `UserProvider` contract ：

	interface UserProvider {

		public function retrieveById($identifier);
		public function retrieveByToken($identifier, $token);
		public function updateRememberToken(Authenticatable $user, $token);
		public function retrieveByCredentials(array $credentials);
		public function validateCredentials(Authenticatable $user, array $credentials);

	}

`retrieveById` 函式通常接收一个代表用户的数字键，例如：MySQL 数据库的自动递增 ID。这方法应该取得符合 ID 的 `Authenticatable` 实作并回传。

`retrieveByToken` 函式用用户唯一的 `$identifier` 和保存在 `remember_token` 字段的「记住我」 `$token` 来取得用户。跟前面的方法一样，应该回传 `Authenticatable` 的实作。

`updateRememberToken` 方法用新的 `$token` 更新 `$user` 的 `remember_token` 字段。新 token 可以是在「记住我」成功地登录时，传入一个新的 token，或当用户注销时传入一个 null。

`retrieveByCredentials` 方法接收当尝试登录应用程序时，传递到 `Auth::attempt` 方法的凭证数组。这个方法应该接着「查找」底层使用的永久存储，找到符合凭证的用户。这个方法通常会对 `$credentials['username']` 用「 where 」条件查找。 **这个方法不应该尝试做任何密码验证或认证。**

`validateCredentials` 方法应该借由比较给定的 `$user` 与 `$credentials` 来验证用户。举例来说，这个方法可以比较 `$user->getAuthPassword()` 字串跟 `Hash::make` 后的 `$credentials['password']`。

现在我们已经看过 `UserProvider` 的每个方法，接着来看一下 `Authenticatable`。记住，提供者应该从 `retrieveById` 和 `retrieveByCredentials` 方法回传这个接口的实作：

	interface Authenticatable {

		public function getAuthIdentifier();
		public function getAuthPassword();
		public function getRememberToken();
		public function setRememberToken($value);
		public function getRememberTokenName();

	}

这个接口很简单。 The `getAuthIdentifier` 方法应该回传用户的「主键」。在 MySQL 后台，同样，这将会是个自动递增的主键。`getAuthPassword` 应该回传用户哈希过的密码。这个接口让认证系统可以与任何用户类别一起运作，无论你使用什么 ORM 或保存抽象层。缺省，Laravel 包含一个实作这个接口的 `User` 类别在 `app` 文件夹里，所以你可以参考这个类别当作实作的例子。

最后，当我们已经实作了 `UserProvider`，我们准备好用 `Auth` facade 来注册扩展：

	Auth::extend('riak', function($app)
	{
		return new RiakUserProvider($app['riak.connection']);
	});

用 `extend` 方法注册驱动之后，在你的 `config/auth.php` 设置档切换到新驱动。

<a name="ioc-based-extension"></a>
## 基于 IoC 的扩展

几乎每个 Laravel 框架引入的服务提供者都会绑定对象到 IoC 容器中。你可以在 `config/app.php` 设置档中找到应用程序的服务提供者清单。如果你有时间，你应该浏览过这里面每一个提供者的源代码。借由这样做，你将会更了解每一个提供者添加什么到框架，以及用什么键值来绑定各种服务到 IoC 容器。

例如， `HashServiceProvider` 绑定 `hash` 做为键值到 IoC 容器，它将解析成 `Illuminate\Hashing\BcryptHasher` 实例。你可以在应用程序中覆写这个 IoC 绑定，轻松地扩展并覆写这个类别。例如：

	<?php namespace App\Providers;

	class SnappyHashProvider extends \Illuminate\Hashing\HashServiceProvider {

		public function boot()
		{
			$this->app->bindShared('hash', function()
			{
				return new \Snappy\Hashing\ScryptHasher;
			});

			parent::boot();
		}

	}

要注意的是这个类别扩展 `HashServiceProvider`，不是缺省的 `ServiceProvider` 基底类别。当你扩展了服务提供者，在 `config/app.php` 设置档把 `HashServiceProvider` 换成你扩展的提供者名称。

这是被绑定在容器的所有核心类别的一般扩展方法。实际上，每个以这种方式绑定在容器的核心类别都可以被覆写。再次强调，看过每个框架引入的服务提供者将会使你熟悉：每个类别被绑在容器的哪里、它们是用什么键值绑定。这是个好方法可以了解更多关于 Laravel 如何结合它们。
