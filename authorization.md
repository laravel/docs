# 授權

- [簡介](#introduction)
- [定義權限](#defining-abilities)
- [檢查權限](#checking-abilities)
	- [透過 Gate Facade](#via-the-gate-facade)
	- [透過使用者模型](#via-the-user-model)
	- [使用 Blade 模板](#within-blade-templates)
    - [使用表單請求](#within-form-requests)
- [原則](#policies)
	- [建立原則](#creating-policies)
	- [撰寫原則](#writing-policies)
	- [檢查原則](#checking-policies)
- [控制器授權](#controller-authorization)

<a name="introduction"></a>
## 簡介

除了內建提供的[認證](/docs/{{version}}/authentication)服務外，Laravel 也提供了簡單的方式來組織認證邏輯及控制資源的存取。有很多種方法與輔助函式能幫助你組織你的授權邏輯，在本文件中我們將會涵蓋每一種方式。

> **注意：**授權已經在 Laravel 5.1.11 被加入，請在整合這些功能到應用程式前參考[升級導引](/docs/{{version}}/upgrade)。

<a name="defining-abilities"></a>
## 定義權限

判斷一個使用者是否可以執行特定行為，最簡單的方式就是使用 `Illuminate\Auth\Access\Gate` 類別定義「權限」。`AuthServiceProvider` 是 Laravel 提供的一個方便位置，以定義你應用程式中的所有權限。舉個例子，讓我們定義一個 `update-post` 的權限，以取得目前的 `User` 及 `Post` [模型](/docs/{{version}}/eloquent)。在我們的權限中，我們會判斷使用者的 `id` 與文章的 `user_id` 是否相符：

	<?php

	namespace App\Providers;

	use Illuminate\Contracts\Auth\Access\Gate as GateContract;
	use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;

	class AuthServiceProvider extends ServiceProvider
	{
	    /**
	     * 註冊任何應用程式的認證或授權服務。
	     *
	     * @param  \Illuminate\Contracts\Auth\Access\Gate  $gate
	     * @return void
	     */
	    public function boot(GateContract $gate)
	    {
	        $this->registerPolicies($gate);

	        $gate->define('update-post', function ($user, $post) {
	        	return $user->id === $post->user_id;
	        });
	    }
	}

注意，我們並不會檢查當給定的 `$user` 不是 `NULL`。當沒有經過認證的使用者或是特定的使用者沒有透過 `forUser` 方法指定，那麼 `Gate` 會自動為**所有權限**回傳 `false`。

#### 基於類別的權限

除了註冊`閉包`作為授權的回呼，你可以透過傳遞包含類別名稱及方法的字串來註冊類別的方法。當需要時，該類別會透過[服務容器](/docs/{{version}}/container)被解析：

    $gate->define('update-post', 'Class@method');

<a name="intercepting-all-checks"></a>
<a name="intercepting-authorization-checks"></a>
#### 攔截授權檢查

有時，你可能希望賦予所有權限給指定使用者。對於這種情況，使用 `before` 方法來定義當其他所有授權檢查前會被執行的回呼：

    $gate->before(function ($user, $ability) {
        if ($user->isSuperAdmin()) {
            return true;
        }
    });

如果 `before` 的回呼回傳一個非 null 的結果，則該結果會被作為檢查的結果。

你可以使用 `after` 方法定義一個當所有授權檢查後會被執行的回呼。但是，你不應該修改 `after` 回呼中授權檢查的結果：

    $gate->after(function ($user, $ability, $result, $arguments) {
        //
    });

<a name="checking-abilities"></a>
## 檢查權限

<a name="via-the-gate-facade"></a>
### 透過 Gate Facade

一旦權限被定義後，我們可以透過不同方式「檢查」。首先，我們可以使用 `Gate` [facade](/docs/{{version}}/facades) 的 `check`、`allows` 或 `denies` 方法。這些所有方法會取得權限的名稱及參數，並會被傳遞至權限的回呼中。你**不**需要傳遞目前的使用者至該方法，因為 `Gate` 會自動在回呼參數的前方加上目前的使用者。所以，當透過我們前面定義的 `update-post` 權限進行檢查時，我們只需傳遞一個 `Post` 實例至 `denies` 方法：

    <?php

    namespace App\Http\Controllers;

    use Gate;
    use App\User;
    use App\Post;
    use App\Http\Controllers\Controller;

    class PostController extends Controller
    {
        /**
         * 更新給定的文章。
         *
         * @param  int  $id
         * @return Response
         */
        public function update($id)
        {
        	$post = Post::findOrFail($id);

        	if (Gate::denies('update-post', $post)) {
        		abort(403);
        	}

        	// 更新文章...
        }
    }

當然，`allows` 方法只是簡單的將 `denies` 方法給顛倒過來，當行為被授權時會回傳 `true`。`check` 方法則是 `allows` 方法的別名。

#### 檢查指定使用者的權限

如果你想使用 `Gate` facade 檢查當**目前被驗證的使用者外的其他**使用者有給定的權限，你可以使用 `forUser` 方法：

	if (Gate::forUser($user)->allows('update-post', $post)) {
		//
	}

#### 傳遞多個參數

當然，權限的回呼可以取得多個參數：

	Gate::define('delete-comment', function ($user, $post, $comment) {
		//
	});

如果你的權限需要多個參數，只要簡單的傳遞一個陣列作為 `Gate` 方法的參數：

	if (Gate::allows('delete-comment', [$post, $comment])) {
		//
	}

<a name="via-the-user-model"></a>
### 透過使用者模型

另外，你也可以透過 `User` 模型的實例檢查權限。預設來說，Laravel 的 `App\User` 模型使用了 `Authorizable` trait，它提供了兩個方法：`can` 及 `cannot`。這些方法使用起來相似於 `Gate` facade 提供的 `allows` 與 `denies` 方法。所以，使用我們之前的例子，我們可以將程式碼改成如下：

    <?php

    namespace App\Http\Controllers;

    use App\Post;
    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class PostController extends Controller
    {
        /**
         * 更新給定的文章。
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  int  $id
         * @return Response
         */
        public function update(Request $request, $id)
        {
        	$post = Post::findOrFail($id);

        	if ($request->user()->cannot('update-post', $post)) {
        		abort(403);
        	}

        	// 更新文章...
        }
    }

當然，`can` 方法只是簡單的將 `cannot` 方法給顛倒過來：

	if ($request->user()->can('update-post', $post)) {
		// 更新文章...
	}

<a name="within-blade-templates"></a>
### 使用 Blade 模板

為了方便，Laravel 提供了 `@can` Blade 指令來快速的檢查，當目前認證的使用者擁有給定的權限。例如：

	<a href="/post/{{ $post->id }}">View Post</a>

	@can('update-post', $post)
		<a href="/post/{{ $post->id }}/edit">Edit Post</a>
	@endcan

你也可以將 `@else` 指令結合 `@can` 指令：

	@can('update-post', $post)
		<!-- 目前的使用者可以更新文章 -->
	@else
		<!-- 目前的使用者不可以更新文章 -->
	@endcan

<a name="within-form-requests"></a>
### 使用表單請求

你也可以選擇從[表單請求的](/docs/{{version}}/validation#form-request-validation) `authorize` 方法採用你的 `Gate` 定義的權限。舉個例子：

    /**
     * 判斷當使用者已被授權並發送此請求。
     *
     * @return bool
     */
    public function authorize()
    {
        $postId = $this->route('post');

        return Gate::allows('update', Post::findOrFail($postId));
    }

<a name="policies"></a>
## 原則

<a name="creating-policies"></a>
### 建立原則

由於將你所有的授權邏輯定義在 `AuthServiceProvider` 中可能成為大型應用程式中的累贅，Laravel 讓你可以切分你的授權邏輯至「原則」類別。原則是簡單的 PHP 類別，並基於授權的資源將授權邏輯進行分組。

首先，讓我們產生一個原則來管理 `Post` 模型的授權。你可以透過 `make:policy` [artisan 指令](/docs/{{version}}/artisan)產生一個原則。產生的原則會被放置於 `app/Policies` 目錄中：

	php artisan make:policy PostPolicy

#### 註冊原則

一旦該原則存在，我們需要將它與 `Gate` 類別進行註冊。`AuthServiceProvider` 包含了一個 `policies` 屬性，將各種實體對應至管理它們的原則。所以，我們需要指定 `Post` 模型的原則是 `PostPilicy` 類別：

	<?php

	namespace App\Providers;

	use App\Post;
	use App\Policies\PostPolicy;
	use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;

	class AuthServiceProvider extends ServiceProvider
	{
	    /**
	     * 應用程式的原則對應。
	     *
	     * @var array
	     */
	    protected $policies = [
	        Post::class => PostPolicy::class,
	    ];

	    /**
	     * 註冊任何應用程式的認證或授權服務。
	     *
	     * @param  \Illuminate\Contracts\Auth\Access\Gate  $gate
	     * @return void
	     */
	    public function boot(GateContract $gate)
	    {
	        $this->registerPolicies($gate);
	    }
	}

<a name="writing-policies"></a>
### 撰寫原則

一旦原則被產生且註冊，我們可以為每個權限的授權增加方法。例如，讓我們在 `PostPolicy` 中定義一個 `update` 方法，它會判斷給定的 `User` 是否可以「更新」一筆 `Post`：

	<?php

	namespace App\Policies;

	use App\User;
	use App\Post;

	class PostPolicy
	{
		/**
		 * 判斷給定的文章是否可以被該使用者更新。
		 *
		 * @param  \App\User  $user
		 * @param  \App\Post  $post
		 * @return bool
		 */
	    public function update(User $user, Post $post)
	    {
	    	return $user->id === $post->user_id;
	    }
	}

你可以接著在此原則定義額外的方法，作為各種權限需要的授權。例如，你可以定義 `show`、`destroy` 或 `addComment` 方法來授權 `Post` 的多種行為。

> **注意：**所有原則會透過 Laravel [服務容器](/docs/{{version}}/container)解析，意指你可以在原則的建構子對任何需要的依賴使用型別提示，它們將會被自動注入。

#### 攔截所有檢查

有時，你可能希望在原則賦予所有權限給指定使用者。對於這種情況，只要在原則中定義一個 `before` 方法。原則的此方法會在其他所有授權檢查前被執行：

    public function before($user, $ability)
    {
        if ($user->isSuperAdmin()) {
            return true;
        }
    }

如果 `before` 的回呼回傳一個非 null 的結果，則該結果會被作為檢查的結果。

<a name="checking-policies"></a>
### 檢查原則

原則方法的呼叫方式和基於授權的回呼`閉包`是完全相同的。你可以使用`Gate` facade、`User` 模型、`@can` Blade 指令或是 `policy` 輔助方法。

#### 透過 Gate Facade

`Gate` 會透過檢查傳遞給該類別方法的參數自動的判斷該使用原則。所以，如果我們傳遞一個 `Post` 實例至 `denies` 方法，`Gate` 會採用對應的 `PostPolicy` 來授權行為：

    <?php

    namespace App\Http\Controllers;

    use Gate;
    use App\User;
    use App\Post;
    use App\Http\Controllers\Controller;

    class PostController extends Controller
    {
        /**
         * 更新給定的文章。
         *
         * @param  int  $id
         * @return Response
         */
        public function update($id)
        {
        	$post = Post::findOrFail($id);

        	if (Gate::denies('update', $post)) {
        		abort(403);
        	}

        	// 更新文章...
        }
    }

#### 透過使用者模型

`User` 模型的 `can` 與 `cannot` 方法也會自動採用給定參數可用的原則。此方法提供一個簡單的方式在應用程式中為任何取得到的 `User` 實例授權行為：

	if ($user->can('update', $post)) {
		//
	}

	if ($user->cannot('update', $post)) {
		//
	}

#### 使用 Blade 模板

同樣的，`@can` Blade 指令會採用給定參數可用的授權。

	@can('update', $post)
		<!-- 目前的使用者可以更新文章 -->
	@endcan

#### 透過原則輔助方法

全域的 `policy` 輔助函式可以被用於為給定的類別實例取得 `Policy` 類別。例如，我們可以傳遞一個 `Post` 實例至 `policy` 輔助方法，取得對應的 `PostPolicy` 類別實例：

	if (policy($post)->update($user, $post)) {
		//
	}

<a name="controller-authorization"></a>
## 控制器授權

預設中，基底的 `App\Http\Controllers\Controller` 類別包含了 Laravel 使用的 `AuthorizesRequests` trait。此 trait 提供了 `authorize` 方法，它可以被用於快速授權一個給定的行為，當無權限執行該行為時會拋出 `HttpException`。

`authorize` 方法與其他授權方法共用了同樣的特徵，像是 `Gate::allows` 與 `$user->can()`。所以，讓我們使用 `authorize` 方法來快速授權一個請求以更新一筆 `Post`：

    <?php

    namespace App\Http\Controllers;

    use App\Post;
    use App\Http\Controllers\Controller;

    class PostController extends Controller
    {
        /**
         * 更新給定的文章。
         *
         * @param  int  $id
         * @return Response
         */
        public function update($id)
        {
        	$post = Post::findOrFail($id);

        	$this->authorize('update', $post);

        	// 更新文章...
        }
    }

如果該行為被授權了，控制器將會繼續正常執行；但是，如果 `authorize` 方法判斷沒有權限執行該行為，那麼將會自動產生一個帶有 `403 Not Authorized` 狀態碼的 HTTP 回應並拋出。如你所見，`authorize` 方法是進行授權行為或拋出例外簡單、快速的方法，只使用了一行的程式。

`AuthorizesRequests` trait 也提供了 `authorizeForUser` 方法來為非目前已認證的使用者授權行為：

	$this->authorizeForUser($user, 'update', $post);

#### 自動判斷原則方法

通常，一個原則的方法會對應至一個控制器方法。以下方的 `update` 方法為例，控制器方法及原則方法會共用相同的名稱：`update`。

因此，Laravel 讓你能夠簡單的傳遞實例參數至 `authorize` 方法，基於被呼叫的函式名稱，自動判斷出應該授權的權限。在本例中，因為 `authorize` 被控制器的 `update` 方法呼叫，所以也會呼叫 `PostPolicy` 中的 `update` 方法：

    /**
     * 更新給定的文章。
     *
     * @param  int  $id
     * @return Response
     */
    public function update($id)
    {
    	$post = Post::findOrFail($id);

    	$this->authorize($post);

    	// 更新文章...
    }
