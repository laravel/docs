# Eloquent ORM

- [介紹](#introduction)
- [基本用法](#basic-usage)
- [批量賦值（ Mass Assignment ）](#mass-assignment)
- [新增、修改、刪除](#insert-update-delete)
- [軟刪除（ Soft Deleting ）](#soft-deleting)
- [時間戳](#timestamps)
- [範圍查詢](#query-scopes)
- [全域範圍查詢](#global-scopes)
- [關聯](#relationships)
- [關聯查詢](#querying-relations)
- [預載入（ Eager Loading ）](#eager-loading)
- [新增關聯模型](#inserting-related-models)
- [更新上層模型時間戳](#touching-parent-timestamps)
- [操作樞紐表](#working-with-pivot-tables)
- [集合](#collections)
- [存取器和修改器](#accessors-and-mutators)
- [日期轉換器](#date-mutators)
- [屬性型別轉換](#attribute-casting)
- [模型事件](#model-events)
- [模型觀察者](#model-observers)
- [轉換陣列 / JSON](#converting-to-arrays-or-json)

<a name="introduction"></a>
## 介紹

Laravel 的 Eloquent ORM 提供了漂亮、簡潔的 ActiveRecord 實作來和資料庫互動。 每個資料庫表會和一個對應的「模型」互動。

在開始之前，記得把 `config/database.php` 裡的資料庫連線設定好。

<a name="basic-usage"></a>
## 基本用法

我們先從建立一個 Eloquent 模型開始。模型通常放在 `app` 目錄下，但是您可以將它們放在任何地方，只要能通過 composer.json 自動載入。所有的 Eloquent 模型都繼承 `Illuminate\Database\Eloquent\Model`。

#### 定義一個 Eloquent 模型

	class User extends Model {}

也可以用 `make:model` 命令產生 Eloquent 模型：

	php artisan make:model User

注意我們並沒有告訴 Eloquent，`User` 模型會使用哪個資料表。若沒有特別指定，系統會預設自動對應名稱為「類別名稱的小寫複數形態」的資料表。所以，在上面的例子中，Eloquent 會假設 `User` 模型將把資料存在 `users` 資料表。您也可以在類別中定義 `table` 屬性自定要對應的資料表名稱。

	class User extends Model {

		protected $table = 'my_users';

	}

> **注意：** Eloquent 也會假設每個資料表都有一個欄位名稱為 `id` 的主鍵。您可以在類別裡定義 `primaryKey` 屬性覆寫這個預設。同樣的，你也可以定義 `connection` 屬性，指定模型需要的資料庫連線。

定義好模型之後，你就可以從資料表新增及取得資料了。注意預設上，在資料表裡需要有 `updated_at` 和 `created_at` 兩個欄位。如果你不想設定或自動更新這兩個欄位，將類別裡的 `$timestamps` 屬性設為 `false`。

#### 取出所有模型資料

	$users = User::all();

#### 根據主鍵取出一筆資料

	$user = User::find(1);

	var_dump($user->name);

> **提示：** 所有[查詢構造器](/docs/5.0/queries)裡的方法，查詢 Eloquent 模型時也可以使用。

#### 根據主鍵取出一條資料或拋出異常

有時, 你可能想要在找不到模型資料時拋出例外，以捕捉例外讓 `App::error` 處理並顯示 404 頁面。

	$model = User::findOrFail(1);

	$model = User::where('votes', '>', 100)->firstOrFail();

要註冊錯誤處理，可以監聽 `ModelNotFoundException`

	use Illuminate\Database\Eloquent\ModelNotFoundException;

	App::error(function(ModelNotFoundException $e)
	{
		return Response::make('Not Found', 404);
	});

#### Eloquent 模型結合查詢語法

	$users = User::where('votes', '>', 100)->take(10)->get();

	foreach ($users as $user)
	{
		var_dump($user->name);
	}

#### Eloquent 聚合查詢

當然，您也可以使用查詢產生器的聚合查詢方法。

	$count = User::where('votes', '>', 100)->count();

如果沒辦法使用流暢介面產生出查詢語句，也可以使用 `whereRaw` 方法：

	$users = User::whereRaw('age > ? and votes = 100', array(25))->get();

#### 切分查詢

如果你要處理非常多（數千筆）Eloquent 查詢結果，使用 `chunk` 方法可以讓你順利作業而不會吃掉記憶體：

	User::chunk(200, function($users)
	{
		foreach ($users as $user)
		{
			//
		}
	});

傳到方法裡的第一個參數表示每次「切分」要取出的資料數量。第二個參數的閉合函數會在每次取出資料時被呼叫。

#### 指定查詢時連線資料庫

您也可以指定在執行 Eloquent 查詢時要使用哪個資料庫連線。只要使用 `on` 方法：

	$user = User::on('connection-name')->find(1);

如果您有使用 [讀取 / 寫入連線](/docs/5.0/database#read-write-connections), 可以使用如下方法，強制使用 "write" 連線進行查詢：

	$user = User::onWriteConnection()->find(1);

<a name="mass-assignment"></a>
## 批量賦值（ Mass Assignment ）

在建立一個新的模型時，你把屬性資料陣列傳入建構子，這些屬性值會經由批量賦值存成模型資料。這一點非常方便，然而，若盲目地將使用者輸入存到模型，可能會造成**嚴重的**安全隱患。如果盲目的存入使用者輸入，使用者可以隨意的修改**任何**以及**所有**模型的屬性。基於這個理由，所有的 Eloquent 模型預設會防止批量賦值。

我們以在模型裡設定 `fillable` 或 `guarded` 屬性作為開始。

#### 定義模型 `Fillable` 屬性

`fillable` 屬性指定了可以被批量賦值的欄位。可以設定在類別裡或是建立實例後設定。

	class User extends Model {

		protected $fillable = array('first_name', 'last_name', 'email');

	}

在上面的例子裡，只有三個屬性允許被批量賦值。

#### 定義模型 Guarded 屬性

`guarded` 與 `fillable` 相反，是作為「黑名單」而不是「白名單」：

	class User extends Model {

		protected $guarded = array('id', 'password');

	}

> **注意：** 使用 `guarded` 時，`Input::get()` 或任何使用者可以控制的未過濾資料，永遠不應該傳入 `save` 或 `update` 方法，因為沒有在「黑名單」內的欄位可能被更新。

#### 阻擋所有屬性被批量賦值

上面的例子中，`id` 和 `password` 屬性**不會**被批量賦值，而所有其他的屬性則允許批量賦值。您也可以使用 guard 屬性阻止所有屬性被批量賦值：

	protected $guarded = array('*');

<a name="insert-update-delete"></a>
## 新增、更新、刪除

要從模型新增一筆資料到資料庫，只要建立一個模型例項並呼叫 `save` 方法即可。

#### 儲存新的模型資料

	$user = new User;

	$user->name = 'John';

	$user->save();

> **注意：** 通常 Eloquent 模型主鍵值會自動遞增。但是您若想自定主鍵，將 `incrementing` 屬性設成 false 。

也可以使用 `create` 方法存入新的模型資料，新增完後會返回新增的模型實例。但是在新增前，需要先在模型類別裡設定好 `fillable` 或 `guarded` 屬性，因為 Eloquent 預設會防止批量賦值。

在新模型資料被儲存或新增後，若模型有自動遞增主鍵，可以從物件取得 `id` 屬性值：

	$insertedId = $user->id;

#### 在模型裡設定 Guarded 屬性

	class User extends Model {

		protected $guarded = array('id', 'account_id');

	}

#### 使用模型的 Create 方法

	// 在資料庫中建立一個新的使用者...
	$user = User::create(array('name' => 'John'));

	// 以屬性找使用者，若沒有則新增並取得新的實例...
	$user = User::firstOrCreate(array('name' => 'John'));

	// 以屬性找使用者，若沒有則建立新的實例...
	$user = User::firstOrNew(array('name' => 'John'));

#### 更新取出的模型

要更新模型，可以取出它，更改屬性值，然後使用 `save` 方法：

	$user = User::find(1);

	$user->email = 'john@foo.com';

	$user->save();

#### 儲存模型和關聯資料

有時你可能不只想要儲存模型本身，也想要儲存關聯的資料。您可以使用 `push` 方法達到目的：

	$user->push();

你可以結合查詢語句，批次更新模型：

	$affectedRows = User::where('votes', '>', 100)->update(array('status' => 2));

> **注意：**若使用 Eloquent 查詢產生器批次更新模型，則不會觸發模型事件。

#### 刪除模型

要刪除模型，只要使用實例呼叫 `delete` 方法：

	$user = User::find(1);

	$user->delete();

#### 依主鍵值刪除模型

	User::destroy(1);

	User::destroy(array(1, 2, 3));

	User::destroy(1, 2, 3);

當然，您也可以結合查詢語句批次刪除模型：

	$affectedRows = User::where('votes', '>', 100)->delete();

#### 只更新模型的時間戳

如果您只想要更新模型的時間戳，您可以使用 `touch` 方法：

	$user->touch();

<a name="soft-deleting"></a>
## 軟刪除（ Soft Deleting ）

通過軟刪除方式刪除了一個模型後，資料並不是真的從資料庫被移除。而是會設定 `deleted_at` 時間戳。要讓模型使用軟刪除功能，只要在模型類別加入 `SoftDeletingTrait`：

	use Illuminate\Database\Eloquent\SoftDeletes;

	class User extends Model {

		use SoftDeletes;

		protected $dates = ['deleted_at'];

	}

要加入 `deleted_at` 欄位到資料庫表，可以在遷移檔案裡使用 `softDeletes` 方法：

	$table->softDeletes();

現在當您使用模型呼叫 `delete` 方法時， `deleted_at` 欄位會被更新成現在的時間戳。在查詢使用軟刪除功能的模型時，被「刪除」的模型資料不會出現在查詢結果裡。

#### 強制查詢軟刪除資料

要強制讓已被軟刪除的模型資料出現在查詢結果裡，在查詢時使用 `withTrashed` 方法：

	$users = User::withTrashed()->where('account_id', 1)->get();

`withTrashed` 也可以用在關聯查詢：

	$user->posts()->withTrashed()->get();

如果你**只想**查詢被軟刪除的模型資料，可以使用 `onlyTrashed` 方法：

	$users = User::onlyTrashed()->where('account_id', 1)->get();

要把被軟刪除的模型資料恢復，使用 `restore` 方法：

	$user->restore();

您也可以結合查詢語句使用 `restore`：

	User::withTrashed()->where('account_id', 1)->restore();

如同 `withTrashed`，`restore` 方法也可以用在關聯物件：

	$user->posts()->restore();

如果想要真的從模型資料庫刪除，使用 `forceDelete` 方法：

	$user->forceDelete();

`forceDelete` 方法也可以用在關聯物件：

	$user->posts()->forceDelete();

要確認模型是否被軟刪除了，可以使用 `trashed` 方法：

	if ($user->trashed())
	{
		//
	}

<a name="timestamps"></a>
## 時間戳

預設 Eloquent 會自動維護資料表的 `created_at` 和 `updated_at` 欄位。只要把這兩個「時間戳」欄位加到資料表， Eloquent 就會處理剩下的工作。如果不想讓 Eloquent 自動維護這些欄位，把下面的屬性加到模型類別裡：

#### 關閉自動更新時間戳

	class User extends Model {

		protected $table = 'users';

		public $timestamps = false;

	}

#### 自定義時間戳格式

如果想要自定義時間戳格式，可以在模型類別裡覆寫 `getDateFormat` 方法：

	class User extends Model {

		protected function getDateFormat()
		{
			return 'U';
		}

	}

<a name="query-scopes"></a>
## 範圍查詢

#### 定義範圍查詢

範圍查詢可以讓你輕鬆的重複利用模型的查詢邏輯。要設定範圍查詢，只要定義以 `scope` 前綴的模型方法：

	class User extends Model {

		public function scopePopular($query)
		{
			return $query->where('votes', '>', 100);
		}

		public function scopeWomen($query)
		{
			return $query->whereGender('W');
		}

	}

#### 使用範圍查詢

	$users = User::popular()->women()->orderBy('created_at')->get();

#### 動態範圍查詢

有時你可能想要定義可接受參數的範圍查詢方法。只要把參數加到方法裡：

	class User extends Model {

		public function scopeOfType($query, $type)
		{
			return $query->whereType($type);
		}

	}

然後把參數值傳到範圍查詢方法呼叫裡：

	$users = User::ofType('member')->get();

<a name="global-scopes"></a>
## 全域範圍查詢

有時你可能希望定義一個 scope，讓它統一作用在模型的所有查詢中。本質上，這也是 Eloquent 的「軟刪除」功能的實現原理。全域範圍查詢的功能，是通過 PHP traits 加上 `Illuminate\Database\Eloquent\ScopeInterface` 介面的實作來定義的。

首先，我們需要定義一個 trait。這裡我們用 Laravel 的 `SoftDeletes` 舉例：

	trait SoftDeletes {

		/**
		 * Boot the soft deleting trait for a model.
		 *
		 * @return void
		 */
		public static function bootSoftDeletes()
		{
			static::addGlobalScope(new SoftDeletingScope);
		}

	}

如果一個 Eloquent 模型引入了一個 trait，而這個 trait 中帶有符合 `bootNameOfTrait` 形式的命名方法 ,那麼這個方法會在 Eloquent 模型啟動的時候呼叫，
您可以在此時註冊全域範圍查詢，或者其他想進行的操作。scope 必須實作 `ScopeInterface` 介面，介面定義了兩個方法：`apply` 和 `remove`。

`apply` 方法會傳入 `Illuminate\Database\Eloquent\Builder` 查詢產生器物件，用來新增這個 scope 所需的額外的 `where` 查詢。而 `remove` 方法同樣接受一個 `Builder` 物件，用來反向執行 `apply` 操作。換句話說，`remove` 方法應該移除已經新增的 `where` 查詢（或者其他查詢子句）。因此，以 `SoftDeletingScope` 來說，方法看起來如下：

	/**
	 * Apply the scope to a given Eloquent query builder.
	 *
	 * @param  \Illuminate\Database\Eloquent\Builder  $builder
	 * @return void
	 */
	public function apply(Builder $builder)
	{
		$model = $builder->getModel();

		$builder->whereNull($model->getQualifiedDeletedAtColumn());
	}

	/**
	 * Remove the scope from the given Eloquent query builder.
	 *
	 * @param  \Illuminate\Database\Eloquent\Builder  $builder
	 * @return void
	 */
	public function remove(Builder $builder)
	{
		$column = $builder->getModel()->getQualifiedDeletedAtColumn();

		$query = $builder->getQuery();

		foreach ((array) $query->wheres as $key => $where)
		{
			// If the where clause is a soft delete date constraint, we will remove it from
			// the query and reset the keys on the wheres. This allows this developer to
			// include deleted model in a relationship result set that is lazy loaded.
			if ($this->isSoftDeleteConstraint($where, $column))
			{
				unset($query->wheres[$key]);

				$query->wheres = array_values($query->wheres);
			}
		}
	}

<a name="relationships"></a>
## 關聯

當然，你的資料表很可能跟另一張表相關聯。例如，一篇部落格文章可能有很多評論，或是一張訂單跟下單客戶相關聯。 Eloquent 讓管理和處理這些關聯變得很容易。Laravel 有很多種關聯類型：

- [一對一](#one-to-one)
- [一對多](#one-to-many)
- [多對多](#many-to-many)
- [遠層一對多關聯](#has-many-through)
- [多型關聯](#polymorphic-relations)
- [多型的多對多關聯](#many-to-many-polymorphic-relations)

<a name="one-to-one"></a>
### 一對一

#### 定義一對一關聯

一對一關聯是很基本的關聯。例如一個 `User` 模型會對應到一個 `Phone`。 在 Eloquent 裡可以像下面這樣定義關聯：

	class User extends Model {

		public function phone()
		{
			return $this->hasOne('App\Phone');
		}

	}

傳到 `hasOne` 方法裡的第一個參數是關聯模型的類別名稱。定義好關聯之後，就可以使用 Eloquent 的[動態屬性](#dynamic-properties)取得關聯物件：

	$phone = User::find(1)->phone;

SQL 會執行如下語句：

	select * from users where id = 1

	select * from phones where user_id = 1

注意，Eloquent 假設對應的關聯模型資料表裡，外鍵名稱是基於模型名稱。在這個例子裡，預設 `Phone` 模型資料表會以 `user_id` 作為外鍵。如果想要更改這個預設，可以傳入第二個參數到 `hasOne` 方法裡。更進一步，還可以傳入第三個參數，指定關聯的外鍵是與這個模型本身的哪個欄位對應：

	return $this->hasOne('App\Phone', 'foreign_key');

	return $this->hasOne('App\Phone', 'foreign_key', 'local_key');

#### 定義相對的關聯

要在 `Phone` 模型裡定義相對的關聯，可以使用 `belongsTo` 方法：

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User');
		}

	}

在上面的例子裡，Eloquent 預設會使用 `phones` 資料表的 `user_id` 欄位查詢關聯。如果想要自己指定外鍵欄位，可以在 `belongsTo` 方法裡傳入第二個參數：

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User', 'local_key');
		}

	}

除此之外，也可以傳入第三個參數，指定要參照上層資料庫表的哪個欄位：

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User', 'local_key', 'parent_key');
		}

	}

<a name="one-to-many"></a>
### 一對多

一對多關聯的例子如，一篇部落格文章可能「有很多」評論。可以像這樣定義關聯：

	class Post extends Model {

		public function comments()
		{
			return $this->hasMany('App\Comment');
		}

	}

現在可以經由[動態屬性](#dynamic-properties)取得文章的評論：

	$comments = Post::find(1)->comments;

如果需要增加更多條件限制，可以在呼叫 `comments` 方法後面串接查詢條件方法：

	$comments = Post::find(1)->comments()->where('title', '=', 'foo')->first();

同樣的，您可以傳入第二個參數到 `hasMany` 方法更改預設的外來鍵名稱。以及，如同 `hasOne` 關聯，可以指定本身的對應欄位：

	return $this->hasMany('App\Comment', 'foreign_key');

	return $this->hasMany('App\Comment', 'foreign_key', 'local_key');

#### 定義相對的關聯

要在 `Comment` 模型定義相對應的關聯，可使用 `belongsTo` 方法：

	class Comment extends Model {

		public function post()
		{
			return $this->belongsTo('App\Post');
		}

	}

<a name="many-to-many"></a>
### 多對多

多對多關聯更為複雜。這種關聯的例子如，一個使用者（ user ）可能用有很多身份（ role ），而一種身份可能很多使用者都有。例如很多使用者都是「管理者」。多對多關聯需要用到三個資料庫表：`users`、`roles` 和 `role_user`。`role_user` 樞紐表命名是以相關聯的兩個模型資料庫表，依照字母順序命名，樞紐表裡面應該要有 `user_id` 和 `role_id` 欄位。

可以使用 `belongsToMany` 方法定義多對多關係：

	class User extends Model {

		public function roles()
		{
			return $this->belongsToMany('App\Role');
		}

	}

現在我們可以從 `User` 模型取得 roles：

	$roles = User::find(1)->roles;

如果不想使用預設的樞紐資料表命名方式，可以傳遞資料表名稱作為 `belongsToMany` 方法的第二個參數：

	return $this->belongsToMany('App\Role', 'user_roles');

也可以更改預設的關聯欄位名稱：

	return $this->belongsToMany('App\Role', 'user_roles', 'user_id', 'foo_id');

當然，也可以在 `Role` 模型定義相對的關聯：

	class Role extends Model {

		public function users()
		{
			return $this->belongsToMany('App\User');
		}

	}

<a name="has-many-through"></a>
### Has Many Through 遠層一對多關聯

「遠層一對多關聯」提供了方便簡短的方法，可以經由多層間的關聯取得遠層的關聯。例如，一個 `Country` 模型可能通過 `Users` 關聯到很多 `Posts` 模型。 資料庫表間的關係可能看起來如下：

	countries
		id - integer
		name - string

	users
		id - integer
		country_id - integer
		name - string

	posts
		id - integer
		user_id - integer
		title - string

雖然 `posts` 資料庫表本身沒有 `country_id` 欄位，但 `hasManyThrough` 方法讓我們可以使用 `$country->posts` 取得 country 的 posts。我們可以定義以下關聯：

	class Country extends Model {

		public function posts()
		{
			return $this->hasManyThrough('App\Post', 'User');
		}

	}

如果想要手動指定關聯的欄位名稱，可以傳入第三和第四個參數到方法裡：

	class Country extends Model {

		public function posts()
		{
			return $this->hasManyThrough('App\Post', 'User', 'country_id', 'user_id');
		}

	}

<a name="polymorphic-relations"></a>
### 多型關聯

多型關聯可以用一個簡單的關聯方法，就讓一個模型同時關聯多個模型。例如，你可能想定義一個 photo 模型，可以屬於 staff 或 order 模型。可以定義關聯如下：

	class Photo extends Model {

		public function imageable()
		{
			return $this->morphTo();
		}

	}

	class Staff extends Model {

		public function photos()
		{
			return $this->morphMany('App\Photo', 'imageable');
		}

	}

	class Order extends Model {

		public function photos()
		{
			return $this->morphMany('App\Photo', 'imageable');
		}

	}

#### 取得多型關聯物件

現在我們可以從 staff 或 order 模型取得多型關聯物件：

	$staff = Staff::find(1);

	foreach ($staff->photos as $photo)
	{
		//
	}

#### 取得多型關聯物件的擁有者

然而，多型關聯真正神奇的地方，在於要從 `Photo` 模型取得 staff 或 order 物件時：

	$photo = Photo::find(1);

	$imageable = $photo->imageable;

Photo 模型裡的 `imageable` 關聯會返回 `Staff` 或 `Order` 實例，取決於這是哪一種模型擁有的照片。

#### 多型關聯的資料表結構

為了理解多型關聯的運作機制，來看看它們的資料庫表結構：

	staff
		id - integer
		name - string

	orders
		id - integer
		price - integer

	photos
		id - integer
		path - string
		imageable_id - integer
		imageable_type - string

要注意的重點是 `photos` 資料表的 `imageable_id` 和 `imageable_type`。在上面的例子裡，ID 欄位會包含 staff 或 order 的 ID，而 type 是擁有者的模型類別名稱。這就是讓 ORM 在取得 `imageable` 關聯物件時，決定要哪一種模型物件的機制。

<a name="many-to-many-polymorphic-relations"></a>
### 多型的多對多關聯

#### 多型的多對多關聯資料表結構

除了一般的多型關聯，也可以使用多對多的多型關聯。例如，部落格的 `Post` 和 `Video` 模型可以共用多型的 `Tag` 關聯模型。首先，來看看資料表結構：

	posts
		id - integer
		name - string

	videos
		id - integer
		name - string

	tags
		id - integer
		name - string

	taggables
		tag_id - integer
		taggable_id - integer
		taggable_type - string

現在，我們準備好設定模型關聯了。`Post` 和 `Video` 模型都可以經由 `tags` 方法建立 `morphToMany` 關聯：

	class Post extends Model {

		public function tags()
		{
			return $this->morphToMany('App\Tag', 'taggable');
		}

	}

在 `Tag` 模型裡針對每一種關聯建立一個方法：

	class Tag extends Model {

		public function posts()
		{
			return $this->morphedByMany('App\Post', 'taggable');
		}

		public function videos()
		{
			return $this->morphedByMany('App\Video', 'taggable');
		}

	}

<a name="querying-relations"></a>
## 關聯查詢

#### 根據關聯條件查詢

在取得模型資料時，你可能想要以關聯模型作為查詢限制。例如，您可能想要取得所有「至少有一篇評論」的部落格文章。可以使用 `has` 方法達成目的：

	$posts = Post::has('comments')->get();

也可以指定運算子和數量：

	$posts = Post::has('comments', '>=', 3)->get();

也可以使用「點號」的形式建構巢狀的 `has` 語句：

	$posts = Post::has('comments.votes')->get();

如果想要更進階的用法，可以使用 `whereHas` 和 `orWhereHas` 方法，在 `has` 查詢裡設定 "where" 條件：

	$posts = Post::whereHas('comments', function($q)
	{
		$q->where('content', 'like', 'foo%');

	})->get();

<a name="dynamic-properties"></a>
### 動態屬性

Eloquent 可以經由動態屬性取得關聯物件。Eloquent 會自動進行關聯查詢，而且會很聰明的知道應該要使用 `get`（用在一對多關聯）或是 `first` （用在一對一關聯）方法。可以使用和「關聯方法名稱相同」的動態屬性取得物件。例如，如下面的模型物件 `$phone`：

	class Phone extends Model {

		public function user()
		{
			return $this->belongsTo('App\User');
		}

	}

	$phone = Phone::find(1);

比起像這樣印出使用者的 email：

	echo $phone->user()->first()->email;

可以簡短寫成：

	echo $phone->user->email;

> **注意：**若取得的是許多關聯物件，會返回 `Illuminate\Database\Eloquent\Collection` 物件。

<a name="eager-loading"></a>
## 預載入（ Eager Loading ）

預載入是用來減少 N + 1 查詢問題。例如，一個 `Book` 模型資料會關聯到一個 `Author`。關聯會像下面這樣定義：

	class Book extends Model {

		public function author()
		{
			return $this->belongsTo('App\Author');
		}

	}

現在考慮下面的程式碼：

	foreach (Book::all() as $book)
	{
		echo $book->author->name;
	}

上面的迴圈會執行一次查詢取回所有資料表上的書籍，然而每本書都會執行一次查詢取得作者。所以若有 25 本書，就會進行 26 次查詢。

很幸運地，我們可以使用預載入大量減少查詢次數。使用 `with` 方法指定想要預載入的關聯物件：

	foreach (Book::with('author')->get() as $book)
	{
		echo $book->author->name;
	}

現在，上面的迴圈總共只會執行兩次查詢：

	select * from books

	select * from authors where id in (1, 2, 3, 4, 5, ...)

使用預載入可以大大提高程式的效能。

當然，也可以同時載入多種關聯：

	$books = Book::with('author', 'publisher')->get();

甚至可以預載入巢狀關聯：

	$books = Book::with('author.contacts')->get();

上面的例子中， `author` 關聯會被預載入，author 的 `contacts` 關聯也會被預載入。

### 預載入條件限制

有時你可能想要預載入關聯，並且指定預載入的查詢限制。下面有一個例子：

	$users = User::with(array('posts' => function($query)
	{
		$query->where('title', 'like', '%first%');

	}))->get();

上面的例子裡，我們打算預載入 user 的 posts 關聯，並限制條件為 post 的 title 欄位需包含 "first"。

當然，預載入的閉合函數裡不一定只能加上條件限制，也可以加上排序：

	$users = User::with(array('posts' => function($query)
	{
		$query->orderBy('created_at', 'desc');

	}))->get();

### 延遲預載入

也可以直接從模型的 collection 預載入關聯物件。這對於需要根據情況決定是否載入關聯物件時，或是跟快取一起使用時很有用。

	$books = Book::all();

	$books->load('author', 'publisher');

<a name="inserting-related-models"></a>
## 新增關聯模型

#### 附加一個關聯模型

你會常常需要加入新的關聯模型。例如新增一個 comment 到 post。除了手動設定模型的 `post_id` 外鍵，也可以從上層的 `Post` 模型新增關聯的 comment：

	$comment = new Comment(array('message' => 'A new comment.'));

	$post = Post::find(1);

	$comment = $post->comments()->save($comment);

上面的例子裡，新增的 comment 模型中，`post_id` 欄位會被自動設定。

如果想要同時新增很多關聯模型：

	$comments = array(
		new Comment(array('message' => 'A new comment.')),
		new Comment(array('message' => 'Another comment.')),
		new Comment(array('message' => 'The latest comment.'))
	);

	$post = Post::find(1);

	$post->comments()->saveMany($comments);

### 從屬關聯模型（ Belongs To ）

要更新 `belongsTo` 關聯時，可以使用 `associate` 方法。這個方法會設定子模型的外鍵：

	$account = Account::find(10);

	$user->account()->associate($account);

	$user->save();

### 新增多對多關聯模型（ Many To Many ）

您也可以新增多對多的關聯模型。讓我們繼續使用 `User` 和 `Role` 模型作為例子。我們可以使用 `attach` 方法簡單地把 roles 附加給一個 user：

#### 附加多對多模型

	$user = User::find(1);

	$user->roles()->attach(1);

也可以傳入要存在樞紐表中的屬性陣列：

	$user->roles()->attach(1, array('expires' => $expires));

當然，有 `attach` 方法就會有相反的 `detach` 方法：

	$user->roles()->detach(1);

`attach` 和 `detach` 都可以接受 ID 陣列作為參數：

	$user = User::find(1);

	$user->roles()->detach([1, 2, 3]);

	$user->roles()->attach([1 => ['attribute1' => 'value1'], 2, 3]);

#### 使用 Sync 方法同步多對多關聯

您也可以使用 `sync` 方法附加關聯模型。`sync` 方法會把根據 ID 陣列，同步樞紐表裡的關聯。同步完後，模型只會和 ID 陣列裡有的 id 相關聯：

	$user->roles()->sync(array(1, 2, 3));

#### Sync 時在樞紐表加入額外資料

也可以在把每個 ID 加入樞紐表時，加入其他欄位的資料：

	$user->roles()->sync(array(1 => array('expires' => true)));

有時候，你可能想要能只用一行指令，就建立一個新關聯模型，並且附加到模型上。可以使用 `save` 方法達成目的：

	$role = new Role(array('name' => 'Editor'));

	User::find(1)->roles()->save($role);

上面的例子裡，新的 `Role` 模型物件被儲存，同時附加關聯到 `user` 模型。也可以傳入屬性陣列，把資料加到關聯資料表：

	User::find(1)->roles()->save($role, array('expires' => $expires));

<a name="touching-parent-timestamps"></a>
## 更新上層時間戳

當模型 `belongsTo` 另一個模型時，比方說一個 `Comment` 屬於一個 `Post` ，如果能在子模型被更新時，更新上層的時間戳，這將會很有用。例如，當 `Comment` 模型更新時，你可能想要能夠同時自動更新 `Post` 的 `updated_at` 時間戳。Eloquent 讓事情變得很簡單。只要在子關聯的類別裡，把關聯方法名稱加入 `touches` 屬性即可：

	class Comment extends Model {

		protected $touches = array('post');

		public function post()
		{
			return $this->belongsTo('App\Post');
		}

	}

現在，當你更新 `Comment` 時，對應的 `Post` 會自動更新 `updated_at` 欄位：

	$comment = Comment::find(1);

	$comment->text = 'Edit to this comment!';

	$comment->save();

<a name="working-with-pivot-tables"></a>
## 使用樞紐表

如你所知，要操作多對多關聯需要一個中介的資料表。Eloquent 提供了一些有用的方法可以和這張表互動。例如，假設 `User` 物件關聯到很多 `Role` 物件。取出這些關聯物件時，我們可以在關聯模型上取得 `pivot` 資料表的資料：

	$user = User::find(1);

	foreach ($user->roles as $role)
	{
		echo $role->pivot->created_at;
	}

注意我們取出的每個 `Role` 模型物件，會自動賦予 `pivot` 屬性。這屬性是一個代表樞紐表模型，可以像一般的 Eloquent 模型一樣使用。

預設 `pivot` 物件只包含關聯鍵的屬性。如果想讓 pivot 包含樞紐表的其他欄位，可以在定義關聯方法時指定那些欄位：

	return $this->belongsToMany('App\Role')->withPivot('foo', 'bar');

現在可以在 `Role` 模型的 `pivot` 物件上取得 `foo` 和 `bar` 屬性了。

如果想要可以自動維護樞紐表的 `created_at` 和 `updated_at` 時間戳，在定義關聯方法時加上 `withTimestamps` 方法：

	return $this->belongsToMany('App\Role')->withTimestamps();

#### 刪除樞紐表的關聯資料

要刪除模型在樞紐表的所有關聯，可以使用 `detach` 方法：

	User::find(1)->roles()->detach();

注意，上面的操作不會移除 `roles` 資料表裡面的資料，只會移除樞紐表裡的關聯資料。

#### 更新樞紐表的資料

有時你只想更新樞紐表的資料，而沒有要移除關聯。如果您想更新樞紐表，可以像下面的例子使用 `updateExistingPivot` 方法：

	User::find(1)->roles()->updateExistingPivot($roleId, $attributes);

#### 自定義樞紐模型

Laravel 允許你自定義樞紐模型。要自定義模型，首先要建立一個繼承 Eloquent 的「基本」模型類別。其他的 Eloquent 模型要繼承這個自定義的基本類別，而不是預設的 Eloquent。在基本模型類別裡，加入下面的方法傳回自定義的樞紐模型實例：

	public function newPivot(Model $parent, array $attributes, $table, $exists)
	{
		return new YourCustomPivot($parent, $attributes, $table, $exists);
	}

<a name="collections"></a>
## 集合

所有 Eloquent 查詢返回的資料，如果結果多於一條，不管是經由 `get` 方法或是 `relationship`，都會轉換成集合物件返回。這個物件實現了 `IteratorAggregate` PHP 介面，所以可以像陣列一般進行迭代。而集合物件本身還擁有很多有用的方法可以操作模型資料。

#### 確認集合中裡是否包含特定鍵值

例如，我們可以使用 `contains` 方法，確認結果資料中，是否包含主鍵為特定值的物件。

	$roles = User::find(1)->roles;

	if ($roles->contains(2))
	{
		//
	}

集合也可以轉換成陣列或 JSON：

	$roles = User::find(1)->roles->toArray();

	$roles = User::find(1)->roles->toJson();

如果集合被轉換成字元串類型，會返回 JSON 格式：

	$roles = (string) User::find(1)->roles;

#### 集合迭代

Eloquent 集合裡包含了一些有用的方法可以進行迴圈或是進行過濾：

	$roles = $user->roles->each(function($role)
	{
		//
	});

#### 集合過濾

過濾集合時，閉合函數的使用方式和 [array_filter]((http://php.net/manual/en/function.array-filter.php)) 一樣。

	$users = $users->filter(function($user)
	{
		return $user->isAdmin();
	});

> **注意：**如果要在過濾集合之後轉成 JSON，考慮轉換之前先呼叫 `values` 方法，以重設陣列的鍵值。

#### 迭代傳入集合裡的每個物件到閉合函數

	$roles = User::find(1)->roles;

	$roles->each(function($role)
	{
		//
	});

#### 依照屬性值排序

	$roles = $roles->sortBy(function($role)
	{
		return $role->created_at;
	});

#### 依照屬性值排序

	$roles = $roles->sortBy('created_at');

#### 返回自定義的集合物件

有時您可能想要返回自定義的集合物件，讓您可以在集合類別里加入想要的方法。可以在 Eloquent 模型類別裡覆寫 `newCollection` 方法：

	class User extends Model {

		public function newCollection(array $models = array())
		{
			return new CustomCollection($models);
		}

	}

<a name="accessors-and-mutators"></a>
## 存取器和修改器

#### 定義存取器

Eloquent 提供了一種便利的方法，可以在取得或設定屬性時進行轉換。要定義存取器，只要在模型里加入類似 `getFooAttribute` 命名的方法。注意方法名稱應該使用駝峰式大小寫命名，而對應的資料表欄位名稱則是底線分隔小寫命名：

	class User extends Model {

		public function getFirstNameAttribute($value)
		{
			return ucfirst($value);
		}

	}

上面的例子中，first_name 欄位設定了一個存取器。注意傳入方法的參數是欄位的原始資料。

#### 定義修改器

修改器的定義方式也類似：

	class User extends Model {

		public function setFirstNameAttribute($value)
		{
			$this->attributes['first_name'] = strtolower($value);
		}

	}

<a name="date-mutators"></a>
## 日期轉換器

預設 Eloquent 會把 `created_at` 和 `updated_at` 欄位屬性轉換成 [Carbon](https://github.com/briannesbitt/Carbon) 實例，它提供了很多有用的方法，並繼承了 PHP 原生的 `DateTime` 類。

可以通過覆寫模型的 `getDates` 方法，自定義哪個欄位可以被自動轉換，或甚至完全關閉這個轉換：

	public function getDates()
	{
		return array('created_at');
	}

當欄位是表示日期的時候，可以將值設為 UNIX timestamp、日期字串（ `Y-m-d` ）、日期時間（ date-time ）字串，當然還有 `DateTime` 或 `Carbon` 實例。

要完全關閉日期轉換功能，只要從 `getDates` 方法回傳空陣列即可：

	public function getDates()
	{
		return array();
	}

<a name="attribute-casting"></a>
## 屬性型別轉換

如果想要某些屬性始終轉換成另一個型別, 可以在模型中增加 `casts` 屬性。否則需要為每個屬性定義修改器，這會很花時間。這裡有一個使用 `casts` 屬性的例子：

	/**
	 * 需要被轉換成基本型別的屬性值。
	 *
	 * @var array
	 */
	protected $casts = [
		'is_admin' => 'boolean',
	];

現在當你取用 `is_admin` 屬性時，總是會被轉換成布林型別，即便原本它在資料庫中是存成整數。其他支援的型別轉換有： `integer`、`real`、`float`、`double`、`string`、`boolean` 和 `array`。

如果原本欄位是被儲存的為序列化的 JSON 時，那麼 `array` 型別轉換將會非常有用。比如，資料表裡有一個 TEXT 型別的欄位儲存著序列化後的 JSON 資料，通過增加 `array` 型別轉換, 當取得這個屬性的時候會自動反序列化成 PHP 的陣列：

	/**
	 * 需要被轉換成基本類型的屬性值。
	 *
	 * @var array
	 */
	protected $casts = [
		'options' => 'array',
	];

現在，當你使用 Eloquent 模型時：

	$user = User::find(1);

	// $options 是一個數組...
	$options = $user->options;

	// options 會自動序列化成 JSON...
	$user->options = ['foo' => 'bar'];

<a name="model-events"></a>
## 模型事件

Eloquent 模型有很多事件可以觸發，讓您可以在模型操作的生命週期的不同時間點，使用下列方法綁定事件： `creating`、 `created`、`updating`、`updated`、`saving`、`saved`、`deleting`、`deleted`、`restoring`、`restored`。

當一個物件初次被儲存到資料庫，`creating` 和 `created` 事件會被觸發。如果不是新物件而呼叫了 `save` 方法， `updating` 和 `updated` 事件會被觸發。而兩者的 `saving` 和 `saved` 事件都會被觸發。

#### 使用事件取消資料庫操作

如果 `creating`、`updating`、`saving`、`deleting` 事件返回 false 的話，就會取消資料庫操作

	User::creating(function($user)
	{
		if ( ! $user->isValid()) return false;
	});

#### 註冊事件監聽的方式

你可以在 `EventServiceProvider` 中註冊您的模型事件綁定。比如：

	/**
	 * Register any other events for your application.
	 *
	 * @param  \Illuminate\Contracts\Events\Dispatcher  $events
	 * @return void
	 */
	public function boot(DispatcherContract $events)
	{
		parent::boot($events);

		User::creating(function($user)
		{
			//
		});
	}

<a name="model-observers"></a>
## 模型觀察者

要整合模型的事件處理，可以註冊一個模型觀察者。觀察者類別裡，設定欲對應模型事件的方法。例如，觀察者類別裡可能有 `creating`、`updating`、`saving` 方法，還有其他對應模型事件名稱的方法：

例如，一個模型觀察者類別可能看起來如下：

	class UserObserver {

		public function saving($model)
		{
			//
		}

		public function saved($model)
		{
			//
		}

	}

可以使用 `observe` 方法註冊一個觀察者實例：

	User::observe(new UserObserver);

<a name="converting-to-arrays-or-json"></a>
## 轉換成陣列 / JSON

#### 將模型資料轉成陣列

建構 JSON API 時，你可能常常需要把模型和關聯物件轉換成陣列或 JSON。所以 Eloquent 裡已經包含了這些方法。要把模型和已載入的關聯物件轉成陣列，可以使用 `toArray` 方法：

	$user = User::with('roles')->first();

	return $user->toArray();

注意也可以把模型集合整個轉換成陣列：

	return User::all()->toArray();

#### 將模型轉換成 JSON

要把模型轉換成 JSON，可以使用 `toJson` 方法：

	return User::find(1)->toJson();

#### 從路由中回傳模型

注意當模型或集合被轉換成字串時，會自動轉換成 JSON 格式，這意味著您可以直接從路由返回 Eloquent 物件！

	Route::get('users', function()
	{
		return User::all();
	});

#### 轉換成陣列或 JSON 時隱藏屬性

有時你可能想要限制能出現在陣列或 JSON 格式的屬性資料，比如密碼欄位。只要在模型裡增加 `hidden` 屬性即可

	class User extends Model {

		protected $hidden = array('password');

	}

> **注意：**要隱藏關聯資料，要使用關聯的**方法**名稱，而不是動態存取的屬性名稱。

此外，可以使用 `visible` 屬性定義白名單：

	protected $visible = array('first_name', 'last_name');

<a name="array-appends"></a>
有時候你可能想要增加不存在資料庫欄位的屬性資料。這時候只要定義一個存取器即可：

	public function getIsAdminAttribute()
	{
		return $this->attributes['admin'] == 'yes';
	}

定義好存取器之後，再把對應的屬性名稱加到模型裡的 `appends` 屬性：

	protected $appends = array('is_admin');

把屬性加到 `appends` 陣列之後，在模型資料轉換成陣列或 JSON 格式時就會有對應的值。在 `appends` 陣列中定義的值同樣遵循模型中 `visible` 和 `hidden` 的設定。
