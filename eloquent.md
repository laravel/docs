# Eloquent: 入門

- [介紹](#introduction)
- [定義模型](#defining-models)
	- [Eloquent 模型規範](#eloquent-model-conventions)
- [取得多個模型](#retrieving-multiple-models)
- [取得單一模型／聚合](#retrieving-single-models)
	- [取得聚合查詢](#retrieving-aggregates)
- [新增和更新模型](#inserting-and-updating-models)
	- [基本新增](#basic-inserts)
	- [基本更新](#basic-updates)
	- [批量賦值](#mass-assignment)
- [刪除模型](#deleting-models)
	- [軟刪除](#soft-deleting)
	- [查詢被軟刪除的模型](#querying-soft-deleted-models)
- [查詢範圍](#query-scopes)
- [事件](#events)

<a name="introduction"></a>
## 介紹

Laravel 包含了 Eloquent ORM 提供了漂亮、簡潔的 ActiveRecord 實作來和資料庫互動。每個資料表有一個被用來跟表互動的對應「模型」。你可以透過模型查詢資料表內的資料，以及新增記錄到資料表中。

在開始之前，確認你的資料庫連結設定在 `config/database.php` 檔案內。更多資料庫的設定資訊，請參考[資料庫設定](/docs/{{version}}/database#configuration)。

<a name="defining-models"></a>
## 定義模型

開始之前，讓我們先建立一個 Eloquent 模型。模型通常放在 `app` 目錄，你可以自由的把他們放在任何可以透過你的 `composer.json` 自動載入的地方。所有的 Eloquent 模型都繼承 `Illuminate\Database\Eloquent\Model` 類別。

建立模型實例的最簡單的方法是使用，`make:model` [Artisan 指令](/docs/{{version}}/artisan)：

	php artisan make:model User

當你產生一個模型時，假設你想要產生一個[資料庫遷移](/docs/{{version}}/schema#database-migrations) ，可以使用 `--migration`：

	php artisan make:model User --migration

	php artisan make:model User -m

<a name="eloquent-model-conventions"></a>
### Eloquent 模型規範

現在，讓我們來看一個 `Flight` 模型類別的例子，我們會用它來從 `flights` 資料表取得與儲存資訊：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
	    //
	}


#### 資料表名稱

注意我們並沒有告訴 Eloquent `Flight` 模型該使用哪一張資料表。預設的規則是，類別的複數形式用來當作資料表的表單名稱，除非明確指定另一個名稱。所以，在這個情況下，Eloquent 會自動假設 `Flight` 模型儲存記錄在 `flights` 資料表。你可以在模型中定義一個 `table` 屬性，用來指定你自訂的資料表：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * The table associated with the model.
		 *
		 * @var string
		 */
		protected $table = 'my_flights';
	}

#### 主鍵

Eloquent 會假設每個資料表有一個主鍵欄位叫做 `id`。你可以定義一個 `$primaryKey` 屬性來指定你的主鍵。

#### 時間戳記

預設情況下，Eloquent 希望在資料表內存在 `created_at` 以及 `updated_at` 欄位。如果你不希望透過 Eloquent 來自動管理這兩個欄位，在你的模型內將 `$timestamps` 屬性設定為 `false`：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * Indicates if the model should be timestamped.
		 *
		 * @var bool
		 */
		public $timestamps = false;
	}

如果你需要自訂你的時間戳記的格式，可以在你的模型內設定 `$dateFormat` 屬性。這個屬性決定了日期屬性如何在資料庫中被儲存，以及模組被序列化成陣列或者是 JSON 格式時的日期屬性格式：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * The storage format of the model's date columns.
		 *
		 * @var string
		 */
		protected $dateFormat = 'U';
	}

<a name="retrieving-multiple-models"></a>
## 取得多個模型

一旦你建立了一個模型並且將模型 [關連到資料表](/docs/{{version}}/schema)，你就可以從資料庫中取得資料。把每個 Eloquent 模型想像成強大的 [查詢構造器](/docs/{{version}}/queries)，讓你可以流暢的查詢與模型關聯的資料表。例如：

	<?php

	namespace App\Http\Controllers;

	use App\Flight;
	use App\Http\Controllers\Controller;

	class FlightController extends Controller
	{
		/**
		 * Show a list of all available flights.
		 *
		 * @return Response
		 */
		public function index()
		{
			$flights = Flight::all();

			return view('flight.index', ['flights' => $flights]);
		}
	}

#### 存取欄位的值

假設你有一個 Eloquent 模型的實例，你可以從相對應的屬性透過模型來存取欄位的值。 例如，讓我們走訪查詢所回傳的每個 `Flight` 的實例，並且印出 `name` 欄位的值：

	foreach ($flights as $flight) {
		echo $flight->name;
	}

#### 增加額外的限制

Eloquent `all` 方法會回傳在模型資料表中所有的結果。由於每個 Eloquent 模型可以當作一個 [查詢構造器](/docs/{{version}}/queries)，所以你可以在查詢中增加規則，然後透過 `get` 方法來取得結果：

	$flights = App\Flight::where('active', 1)
				   ->orderBy('name', 'desc')
				   ->take(10)
				   ->get();

> **注意：** 由於 Eloquent 模型是查詢構造器，你應該檢查所有 [查詢構造器](/docs/{{version}}/queries) 中可用的方法。你可以在你的 Eloquent 查詢中使用任意一種方法。

#### 集合

在 Eloquent 方法中，像是 `all` 以及 `get` 可以得到多筆的結果，在 `Illuminate\Database\Eloquent\Collection` 實例中將會回傳。`Collection` 類別提供 [多樣的輔助方法](/docs/{{version}}/eloquent-collections) 用來處理你的 Eloquent 結果。當然，你可以簡單的走訪你的集合像陣列一樣：

	foreach ($flights as $flight) {
		echo $flight->name;
	}

#### 分塊結果

如果你需要處理成千上萬的 Eloquent 記錄，可以使用 `chunk` 命令。`chunk` 方法將會取得一個 Eloquent 模型的「分塊」，將他們送到給定的 `閉包 (Closure)` 進行處理。當你在處理大量的結果時，使用 `chunk` 方法可以節省記憶體：

	Flight::chunk(200, function ($flights) {
		foreach ($flights as $flight) {
			//
		}
	});

傳送到方法的第一個參數是你希望接收每個「分塊」的記錄數量。第二個參數傳遞的閉包，將會從資料庫取得並回傳每個分塊。

<a name="retrieving-single-models"></a>
## 取得單一模型／聚合

當然，除了在給定的資料表中取得所有記錄，你還可以取得單一的記錄，透過 `find` 以及 `first` 取得。而這不是回傳模型的集合，這個方法回傳的是單一模型的實例：

	// Retrieve a model by its primary key...
	$flight = App\Flight::find(1);

	// Retrieve the first model matching the query constraints...
	$flight = App\Flight::where('active', 1)->first();

#### 未發現異常

有時候你可能希望在找不到模型時拋出異常。這在路由或是控制器內是非常有幫助的。`findOrFail` 以及 `firstOrFail` 方法將會取得第一個查詢的結果。然而，如果沒有找到結果，將會拋出一個 `Illuminate\Database\Eloquent\ModelNotFoundException`：

	$model = App\Flight::findOrFail(1);

	$model = App\Flight::where('legs', '>', 100)->firstOrFail();

如果沒有取得異常，`404` HTTP 回應會自動的傳送給使用者，當使用這個方法時，沒有必要明白寫出回傳 `404` 回應確認：

	Route::get('/api/flights/{id}', function ($id) {
		return App\Flight::findOrFail($id);
	});

<a name="retrieving-aggregates"></a>
### 取得聚合查詢

當然，你也可以使用查詢構造器來聚合函式，像是 `count`、`sum`、`max`，和其他 [查詢構造器](/docs/{{version}}/queries) 提供的聚合函式。這些方法會回傳適當的純量值，而不是一個完整的模型實例：

	$count = App\Flight::where('active', 1)->count();

	$max = App\Flight::where('active', 1)->max('price');

<a name="inserting-and-updating-models"></a>
## 新增和更新模型

<a name="basic-inserts"></a>
### 基本新增

要在資料庫中，建立一個新的記錄，只要在模型上設定屬性，然後使用 `save` 方法：

	<?php

	namespace App\Http\Controllers;

	use App\Flight;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class FlightController extends Controller
	{
		/**
		 * Create a new flight instance.
		 *
		 * @param  Request  $request
		 * @return Response
		 */
		public function store(Request $request)
		{
			// Validate the request...

			$flight = new Flight;

			$flight->name = $request->name;

			$flight->save();
		}
	}

在這個範例中，我們把通過 HTTP 傳入請求的 `name` 參數指定到 `App\Flight` 模型實例的 `name` 屬性。當我們使用 `save` 方法，就會在資料庫中新增一筆記錄。當使用 `save` 方法時，`created_at` 以及 `updated_at` 會自動設定時間戳記，所以不需要透過手動去設定他們。

<a name="basic-updates"></a>
### 基本更新

`save` 方法也可用於更新資料庫中已經存在的模型。如果要更新模型，你應該先取得模型，設定任何你希望更新的屬性，之後再透過 `save` 方法儲存。接著，`updated_at` 時間戳記會自動更新，所以不需要手動設定這個值：

	$flight = App\Flight::find(1);

	$flight->name = 'New Flight Name';

	$flight->save();

此外可以對任意數量的模型給定匹配的查詢並且執行更新。在這個範例中，所有的航班 包含有 `active` 以及 `destination` 為 `San Diego`，將會被標記為延遲；

	App\Flight::where('active', 1)
			  ->where('destination', 'San Diego')
			  ->update(['delayed' => 1]);

`update` 方法希望可以透過一個陣列的鍵值對，來更新需要被更新的欄位。

<a name="mass-assignment"></a>
### 批量賦值

你也可以在使用 `create` 方法來儲存新的模型。新增的模型實例會從你的方法中來回傳。然而，在這樣做之前，你需要指定一個 `fillable` 或 `guarded` 屬性在你的模型中，可以保護所有 Eloquent 模型預防被批量賦值（Mass-Assignment）。

之所以會發生批量賦值（Mass-Assignment）的問題，是因為使用者透過 HTTP 請求傳入非法的參數，而且你沒想到這些參數可以更改你資料庫內的欄位。例如，惡意使用者可能會發送 `is_admin` 參數通過 HTTP 請求，然後對映到你模型中的 `create` 方法，這樣就可以讓使用者將自己升級為管理者了。

所以，在開始之前，你應該定義那些模型屬性是你希望可以被批量賦值的。你可以在你的模型中使用 `$fillable` 屬性。例如，我們讓 `Flight` 模型中的 `name` 屬性給予批量賦值：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * The attributes that are mass assignable.
		 *
		 * @var array
		 */
		protected $fillable = ['name'];
	}

一旦我們取得了屬性的批量賦值，我們可以使用 `create` 方法來新增新的記錄到資料庫。`create` 方法回傳已經保存的模型實例：

	$flight = App\Flight::create(['name' => 'Flight 10']);

雖然 `$fillable` 作為「白名單」的屬性可以被批量賦值，但你也可以選擇使用 `$guarded`。`$guarded` 屬性應該包含一個屬性的陣列，是你不想要被批量賦值的。並非所有的屬性在陣列中會被批量賦值。所以，`$guarded` 函式像是一個「黑名單」。當然，你應該使用 `$fillable` 或 `$guarded` - 而不是兩者：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class Flight extends Model
	{
		/**
		 * The attributes that aren't mass assignable.
		 *
		 * @var array
		 */
		protected $guarded = ['price'];
	}

在上面的範例當中，所有屬性 **除了 `price`** 以外，都會被批量賦值。

#### 其他建立的方法

透過批量賦值，你有兩種其他方法來建立你的模型： `firstOrCreate` 以及 `firstOrNew`。`firstOrCreate` 方法中使用給定的欄位／值對，來嘗試尋找資料庫中的記錄。如果在資料庫找不到模型，用給定的屬性來新增一筆記錄。

`firstOrNew` 方法，類似 `firstOrCreate`，會嘗試使用給定的屬性並且在資料庫中搜尋。然而，假設找不到模型，會回傳一個新的模型實例。請注意 `firstOrnew` 回傳的模型還尚未保留到資料庫。你需要透過手動調用 `save` 方法來儲存它：

	// Retrieve the flight by the attributes, or create it if it doesn't exist...
	$flight = App\Flight::firstOrCreate(['name' => 'Flight 10']);

	// Retrieve the flight by the attributes, or instantiate a new instance...
	$flight = App\Flight::firstOrNew(['name' => 'Flight 10']);

<a name="deleting-models"></a>
## 刪除模型

如果要刪除模型，在模型時實例中調用 `delete` 方法：

	$flight = App\Flight::find(1);

	$flight->delete();

#### 透過鍵值來刪除現有的模型

在上面的範例中，我們在調用 `delete` 方法之前，從資料庫取得了模型。然而，假設你知道模型中的主鍵，你可以不需要透過查詢就可以直接刪除。如果要這麼做，請調用 `destroy` 方法：

	App\Flight::destroy(1);

	App\Flight::destroy([1, 2, 3]);

	App\Flight::destroy(1, 2, 3);

#### 透過查詢來刪除模型

當然，你還可以在一個模型上執行刪除查詢。在這個範例，我們將會刪除所有被標記為非活動的航班：

	$deletedRows = App\Flight::where('active', 0)->delete();

<a name="soft-deleting"></a>
### 軟刪除

除了實際從資料庫中移除記錄，Eloquent 還可以使用「軟刪除」模型。當模型通過軟刪除時，它不是真的從資料庫中被移除。相反，`deleted_at` 屬性在模型上被設定，以及被新增到資料庫。如果模型有一個非空值的 `deleted_at`，代表模型已經被軟刪除了。如果要在模型啟動軟刪除，在模型上使用 `Illuminate\Database\Eloquent\SoftDeletes` trait 以及新增 `deleted_at` 欄位到你的 `$dates` 屬性：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;
	use Illuminate\Database\Eloquent\SoftDeletes;

	class Flight extends Model
	{
		use SoftDeletes;

		/**
		 * The attributes that should be mutated to dates.
		 *
		 * @var array
		 */
		protected $dates = ['deleted_at'];
	}

當然，你應該新增 `deleted_at` 欄位到你的資料表。Laravel [結構構造器](/docs/{{version}}/schema) 包含了一個說明的方法來建立這個欄位：

	Schema::table('flights', function ($table) {
		$table->softDeletes();
	});

現在，當你在模型中調用 `delete` 方法，`deleted_at` 欄位將會被設定成目前的日期和時間。而且，當使用軟刪除查詢模型時，軟刪除的模型將自動排除所有的查詢結果。

要確認給定的模型實例是否已經被軟刪除，使用 `trashed` 方法：

	if ($flight->trashed()) {
		//
	}

<a name="querying-soft-deleted-models"></a>
### 查詢被軟刪除的模型

#### 包含軟刪除的模型

如上面所述，軟刪除的模型將自動排除所有的查詢結果。然而，你可以在搜尋時設定 `withTrashed` 方法，強迫軟刪除顯示結果：

	$flights = App\Flight::withTrashed()
					->where('account_id', 1)
					->get();

`withTrashed` 方法應該使用 [關聯](/docs/{{version}}/eloquent-relationships) 搜尋：

	$flight->history()->withTrashed()->get();

#### 取得只有軟刪除的模型

`onlyTrashed` 方法會取得 **只有** 軟刪除的模型：

	$flights = App\Flight::onlyTrashed()
					->where('airline_id', 1)
					->get();

#### 恢復軟刪除的模型

有時候你可能希望「取消刪除」一個軟刪除模型。想要恢復一個軟刪除的模型為有效狀態，在你的模型實例中使用 `restore` 方法：

	$flight->restore();

你也可以使用 `restore` 方法，在查詢的時候快速恢復多個模型：

	App\Flight::withTrashed()
			->where('airline_id', 1)
			->restore();

類似 `withTrashed` 方法，`restore` 方法也可以使用在 [關聯](/docs/{{version}}/eloquent-relationships):

	$flight->history()->restore();

#### 永久刪除模型

有時候你可能真的要從資料庫中刪除你的模型。如果要從資料庫永久刪除軟模型，使用 `forceDelete` 方法：

	// Force deleting a single model instance...
	$flight->forceDelete();

	// Force deleting all related models...
	$flight->history()->forceDelete();

<a name="query-scopes"></a>
## 查詢範圍

範圍（Scopes）允許你定義共同的限制設定，你可以在應用程式中輕易地重複使用。例如，你可能需要頻繁的取得所有使用者，而且是最「受歡迎的」。如果要定義範圍，在 Eloquent 模型方法前面，加上前綴 `scope` 方法：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Scope a query to only include popular users.
		 *
		 * @return \Illuminate\Database\Eloquent\Builder
		 */
		public function scopePopular($query)
		{
			return $query->where('votes', '>', 100);
		}

		/**
		 * Scope a query to only include active users.
		 *
		 * @return \Illuminate\Database\Eloquent\Builder
		 */
		public function scopeActive($query)
		{
			return $query->where('active', 1);
		}
	}

#### 利用查詢範圍

一旦定義了範圍，當你在查詢模型時，你可以調用範圍方法。然而，當你調用方法時，你不需要包含 `scope` 前綴。你能甚至調用連結到不同的範圍，例如:

	$users = App\User::popular()->women()->orderBy('created_at')->get();

#### 動態範圍

有時候，你可能想要定義一個接受參數的範圍。在開始之前，只要在你的範圍增加額外的參數。範圍參數應該被定義在 `$query` 參數之後：

	<?php

	namespace App;

	use Illuminate\Database\Eloquent\Model;

	class User extends Model
	{
		/**
		 * Scope a query to only include users of a given type.
		 *
		 * @return \Illuminate\Database\Eloquent\Builder
		 */
		public function scopeOfType($query, $type)
		{
			return $query->where('type', $type);
		}
	}

現在，當你調用範圍時可以傳遞參數：

	$users = App\User::ofType('admin')->get();

<a name="events"></a>
## 事件

Eloquent 模型有很多事件可以觸發，使用下面的方法，讓你可以操作模型的生命週期：`creating`、`created`、`updating`、`updated`、`saving`、`saved`、`deleting`、`deleted`、`restoring`、`restored`。事件讓你每次可以輕鬆的執行程式碼，而被指定的模型類別在資料庫會被儲存或者更新。

<a name="basic-usage"></a>
### 基本用法

當一個物件初次被儲存到資料庫，`creating` 以及 `created` 事件會被觸發。如果模型已經存在資料庫，以及 `save` 方法被調用，`updating` 和 `updated` 事件將會被觸發。然而，兩者的 `saving` 和 `saved` 事件都會被觸發。

例如，讓我們定義一個 Eloquent 事件監聽器在 [服務提供者](/docs/{{version}}/providers)。在我們的事件監聽器，我們將會調用 `isValid` 方法對給定的模型，如果模型不是有效的，將會回傳 `false`。Eloquent 事件監聽器回傳 `false`，會取消 `save` 和 `update` 的操作：

	<?php

	namespace App\Providers;

	use App\User;
	use Illuminate\Support\ServiceProvider;

	class AppServiceProvider extends ServiceProvider
	{
	    /**
	     * Bootstrap any application services.
	     *
	     * @return void
	     */
		public function boot()
		{
			User::creating(function ($user) {
				if ( ! $user->isValid()) {
					return false;
				}
			});
		}

		/**
		 * Register the service provider.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}
