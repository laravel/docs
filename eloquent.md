# Eloquent: 入門

- [簡介](#introduction)
- [定義模型](#defining-models)
    - [Eloquent 模型慣例](#eloquent-model-conventions)
- [取回多個模型](#retrieving-multiple-models)
- [取回單一模型／集合](#retrieving-single-models)
    - [取回集合](#retrieving-aggregates)
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
## 簡介

Laravel 的 Eloquent ORM 提供了漂亮、簡潔的 ActiveRecord 實作來和資料庫互動。每個資料庫表有一個對應的「模型」可以用來跟資料表互動。你可以透過模型查詢資料表內的資料，以及新增記錄到資料表中。

在開始之前，請確認有設定你的資料庫連結在 `config/database.php` 檔案內。更多資料庫的設定資訊，請查看[資料庫設定](/docs/{{version}}/database#configuration)。

<a name="defining-models"></a>
## 定義模型

開始之前，讓我們先建立一個 Eloquent 模型。模型通常放在 `app` 目錄，不過你可以自由地把他們放在任何可以透過你的 `composer.json` 自動載入的地方。所有的 Eloquent 模型都繼承 `Illuminate\Database\Eloquent\Model` 類別。

建立模型實例的最簡單的方法是使用 `make:model` [Artisan 指令](/docs/{{version}}/artisan)：

    php artisan make:model User

假設當你生成一個模型時，想要產生一個[資料庫遷移](/docs/{{version}}/schema#database-migrations)，可以使用 `--migration` 或 `-m` 選項：

    php artisan make:model User --migration

    php artisan make:model User -m

<a name="eloquent-model-conventions"></a>
### Eloquent 模型慣例

現在，讓我們來看一個 `Flight` 模型類別的例子，我們將會用它來從 `flights` 資料表取回與儲存資訊：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        //
    }


#### 資料表名稱

請注意，我們並沒有告訴 Eloquent `Flight` 模型該使用哪一個資料表。除非明確地指定其他名稱，不然類別的小寫、底線、複數形式會拿來當作資料表的表單名稱。所以，這個案例中，Eloquent 將會假設 `Flight` 模型儲存記錄在 `flights` 資料表。你可以在模型上定義一個 `table` 屬性，用來指定自訂的資料表：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 與模型關聯的資料表。
         *
         * @var string
         */
        protected $table = 'my_flights';
    }

#### 主鍵

Eloquent 也會假設每個資料表有一個主鍵欄位叫做 `id`。你可以定義一個 `$primaryKey` 屬性來覆寫這個慣例。

#### 時間戳記

預設情況下，Eloquent 預期你的資料表會有 `created_at` 和 `updated_at` 欄位。如果你不希望讓 Eloquent 來自動維護這兩個欄位，在你的模型內將 `$timestamps` 屬性設定為 `false`：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 指定是否模型應該被戳記時間。
         *
         * @var bool
         */
        public $timestamps = false;
    }

如果你需要客製化你的時間戳記格式，在你的模型內設定 `$dateFormat` 屬性。這個屬性決定日期如何在資料庫中儲存，以及當模型被序列化成陣列或是 JSON 時的格式：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 模型的日期欄位的儲存格式。
         *
         * @var string
         */
        protected $dateFormat = 'U';
    }

<a name="retrieving-multiple-models"></a>
## 取回多個模型

一旦你建立了一個模型並且將模型[關連到資料表](/docs/{{version}}/schema)，你就可以從資料庫中取得資料。把每個 Eloquent 模型想像成強大的[查詢產生器](/docs/{{version}}/queries)，讓你可以流暢地查詢與模型關聯的資料表。例如：

    <?php

    namespace App\Http\Controllers;

    use App\Flight;
    use App\Http\Controllers\Controller;

    class FlightController extends Controller
    {
        /**
         * 顯示所有可以的航班清單。
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

假設你有一個 Eloquent 模型的實例，你可以透過相對應的屬性來存取模型的欄位值。例如，讓我們遍歷查詢所返回的每個 `Flight` 實例，並且印出 `name` 欄位的值：

    foreach ($flights as $flight) {
        echo $flight->name;
    }

#### 增加額外的限制

Eloquent 的 `all` 方法會回傳在模型資料表中所有的結果。由於每個 Eloquent 模型可以當作一個[查詢產生器](/docs/{{version}}/queries)，所以你可以在查詢中增加規則，然後透過 `get` 方法來取得結果：

    $flights = App\Flight::where('active', 1)
                   ->orderBy('name', 'desc')
                   ->take(10)
                   ->get();

> **注意：**由於 Eloquent 模型是查詢產生器，應該檢閱所有[查詢產生器](/docs/{{version}}/queries)可用的方法。你可以在你的 Eloquent 查詢中使用這其中的任何方法。

#### 集合

像是 `all` 以及 `get` 之類可以取回多筆結果的 Eloquent 方法，將會回傳一個 `Illuminate\Database\Eloquent\Collection` 實例。`Collection` 類別提供[多樣的輔助方法](/docs/{{version}}/eloquent-collections#available-methods) 用來處理你的 Eloquent 結果。當然，你也可以簡單地像陣列一樣遍歷你的集合：

    foreach ($flights as $flight) {
        echo $flight->name;
    }

#### 分塊結果

如果你需要處理上千筆 Eloquent 查詢結果，可以使用 `chunk` 命令。`chunk` 方法將會取得一個 Eloquent 模型的「分塊」，將它們送到給定的 `閉包 (Closure)` 進行處理。當你在處理大量的結果時，使用 `chunk` 方法可以節省記憶體：

    Flight::chunk(200, function ($flights) {
        foreach ($flights as $flight) {
            //
        }
    });

傳遞到方法的第一個參數是表示你希望每次「分塊」要接收的資料數量。閉包則作為第二個參數傳遞，它將會在每次從資料取出分塊時被呼叫。

<a name="retrieving-single-models"></a>
## 取回單一模型／集合

當然，除了從給定的資料表取回所有記錄，你也可以透過 `find` 和 `first` 取回單一的記錄。這些方法回傳單一模型的實例，而不是回傳模型的集合：

    // 藉由主鍵取回一個模型...
    $flight = App\Flight::find(1);

    // 取回符合查詢限制的第一個模型 ...
    $flight = App\Flight::where('active', 1)->first();

#### 找不到的例外

有時候你可能希望在找不到模型時拋出例外，這在路由或是控制器內特別有用。`findOrFail` 以及 `firstOrFail` 方法會取回查詢的第一個結果。而如果沒有找到結果，將會拋出一個 `Illuminate\Database\Eloquent\ModelNotFoundException`：

    $model = App\Flight::findOrFail(1);

    $model = App\Flight::where('legs', '>', 100)->firstOrFail();

如果沒有捕捉到例外，會自動地送回 HTTP `404` 回應給使用者，所以當使用這些方法時，沒有必要明確的撰寫檢查以回傳 `404` 回應：

    Route::get('/api/flights/{id}', function ($id) {
        return App\Flight::findOrFail($id);
    });

<a name="retrieving-aggregates"></a>
### 取回集合

當然，你也可以使用 `count`、`sum`、`max`，和其他[查詢產生器](/docs/{{version}}/queries)提供的[聚合函式](/docs/{{version}}/queries#aggregates)。這些方法會回傳適當的純量值，而不是一個完整的模型實例：

    $count = App\Flight::where('active', 1)->count();

    $max = App\Flight::where('active', 1)->max('price');

<a name="inserting-and-updating-models"></a>
## 新增和更新模型

<a name="basic-inserts"></a>
### 基本新增

要在資料庫中建立一筆新記錄，只要建立一個新模型實例，並在模型上設定屬性，再呼叫 `save` 方法：

    <?php

    namespace App\Http\Controllers;

    use App\Flight;
    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class FlightController extends Controller
    {
        /**
         * 建立一個新的航班實例。
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            // 驗證請求...

            $flight = new Flight;

            $flight->name = $request->name;

            $flight->save();
        }
    }

在這個範例中，我們把進來的 HTTP 請求的 `name` 參數簡單地指定給 `App\Flight` 模型實例的 `name` 屬性。當我們呼叫 `save` 方法，就會新增一筆記錄到資料庫中。當 `save` 方法被呼叫時，`created_at` 以及 `updated_at` 時間戳記將會自動被設定，所以不需要手動去設定它們。

<a name="basic-updates"></a>
### 基本更新

`save` 方法也可以用於更新資料庫中已經存在的模型。要更新模型，你必須先取回模型，設定任何你希望更新的屬性，接著呼叫 `save` 方法。同樣的，`updated_at` 時間戳記將會自動被更新，所以不需要手動設定它的值：

    $flight = App\Flight::find(1);

    $flight->name = 'New Flight Name';

    $flight->save();

也可以針對符合給定查詢的任意數量模型執行更新。在這個範例中，所有 `active` 並且 `destination` 為 `San Diego` 的航班，將會被標記為延遲：

    App\Flight::where('active', 1)
              ->where('destination', 'San Diego')
              ->update(['delayed' => 1]);

`update` 方法預期收到一個欄位與值成對的陣列，來代表應該被更新的欄位。

<a name="mass-assignment"></a>
### 批量賦值

你也可以使用 `create` 方法來在一行間儲存一個新的模型。被新增的模型實例將會從你的方法回傳。然而，在這樣做之前，你需要在你的模型上指定一個 `fillable` 或 `guarded` 屬性，因為所有的 Eloquent 模型有針對批量賦值（Mass-Assignment）做保護。

當使用者透過 HTTP 請求傳入非預期的參數，並接著這些參數更改了資料庫中你不打算要改的欄位，就發生了批量賦值（Mass-Assignment）的漏洞。例如，惡意使用者可能會透過 HTTP 請求傳送 `is_admin` 參數，然後對應到你模型的 `create` 方法，這讓該使用者把自己升級為一個管理者。

所以，在開始之前，你應該定義你希望哪些模型屬性是可以被批量賦值的。你可以在模型上藉由 `$fillable` 屬性達到這個。例如，讓我們來使 `Flight` 模型的 `name` 屬性可以被批量賦值：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 可以被批量賦值的屬性。
         *
         * @var array
         */
        protected $fillable = ['name'];
    }

一旦我們已經設定屬性為可以被批量賦值的，我們可以使用 `create` 方法來新增一筆新記錄到資料庫。`create` 方法回傳已經被儲存的模型實例：

    $flight = App\Flight::create(['name' => 'Flight 10']);

`$fillable` 作為一個可以被批量賦值的屬性的「白名單」，然而你也可以選擇使用 `$guarded`。`$guarded` 屬性應該包含一個屬性的陣列，是你不想要被批量賦值的。所有不在陣列裡面的其他屬性將會是可以被批量賦值的。所以，`$guarded` 的功能像是一個「黑名單」。當然，你應該使用 `$fillable` 或 `$guarded` - 而不是兩者：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class Flight extends Model
    {
        /**
         * 不可以被批量賦值的屬性。
         *
         * @var array
         */
        protected $guarded = ['price'];
    }

在上面的範例當中，所有屬性**除了 `price`** 以外，都可以被批量賦值。

#### 其他建立的方法

還有兩種其他方法，你可以用來透過屬性批量賦值建立你的模型：`firstOrCreate` 和 `firstOrNew`。`firstOrCreate` 方法將會使用給定的欄位／值對，來嘗試尋找資料庫中的記錄。如果在資料庫找不到模型，將會用給定的屬性來新增一筆記錄。

`firstOrNew` 方法類似 `firstOrCreate`，會嘗試使用給定的屬性在資料庫中尋找符合的紀錄。然而，假設找不到模型，將會回傳一個新的模型實例。請注意 `firstOrnew` 回傳的模型還尚未保存到資料庫。你需要透過手動呼叫 `save` 方法來保存它：

    // 用屬性取回航班，或如果不存在則建立它...
    $flight = App\Flight::firstOrCreate(['name' => 'Flight 10']);

    // 用屬性取回航班，或實例化一個新實例...
    $flight = App\Flight::firstOrNew(['name' => 'Flight 10']);

<a name="deleting-models"></a>
## 刪除模型

要刪除模型，必須在模型實例上呼叫 `delete` 方法：

    $flight = App\Flight::find(1);

    $flight->delete();

#### 透過鍵來刪除現有的模型

在上面的範例中，我們在呼叫 `delete` 方法之前，先從資料庫取回了模型。然而，如果你知道模型中的主鍵，你可以不取回模型就直接刪除它。如果要這麼做，請呼叫 `destroy` 方法：

    App\Flight::destroy(1);

    App\Flight::destroy([1, 2, 3]);

    App\Flight::destroy(1, 2, 3);

#### 透過查詢來刪除模型

當然，你也可以在一組模型上執行刪除查詢。在這個範例中，我們將會刪除所有被標記為不活躍的航班：

    $deletedRows = App\Flight::where('active', 0)->delete();

<a name="soft-deleting"></a>
### 軟刪除

除了實際從資料庫中移除記錄，Eloquent 也可以「軟刪除」模型。當模型被軟刪除時，它們不是真的從資料庫中被移除。而是 `deleted_at` 屬性被設定在模型上並新增到資料庫。如果模型有一個非空值的 `deleted_at`，代表模型已經被軟刪除了。要在模型啟動軟刪除，必須在模型上使用 `Illuminate\Database\Eloquent\SoftDeletes` trait 並新增 `deleted_at` 欄位到你的 `$dates` 屬性：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\SoftDeletes;

    class Flight extends Model
    {
        use SoftDeletes;

        /**
         * 需要被轉換成日期的屬性。
         *
         * @var array
         */
        protected $dates = ['deleted_at'];
    }

當然，你應該添加 `deleted_at` 欄位到你的資料表。Laravel [結構產生器](/docs/{{version}}/migrations)包含了一個輔助的方法用來建立這個欄位：

    Schema::table('flights', function ($table) {
        $table->softDeletes();
    });

現在，當你在模型上呼叫 `delete` 方法，`deleted_at` 欄位將會被設定成目前的日期和時間。而且，當查詢有啟用軟刪除的模型時，被軟刪除的模型將會自動從所有的查詢結果中排除。

要確認給定的模型實例是否已經被軟刪除，可以使用 `trashed` 方法：

    if ($flight->trashed()) {
        //
    }

<a name="querying-soft-deleted-models"></a>
### 查詢被軟刪除的模型

#### 包含被軟刪除的模型

如上面所述，被軟刪除的模型將會自動從所有的查詢結果中排除。然而，你可以藉由在查詢上呼叫 `withTrashed` 方法， 強迫被軟刪除的模型出現在查詢結果：

    $flights = App\Flight::withTrashed()
                    ->where('account_id', 1)
                    ->get();

`withTrashed` 方法也可以被用在[關聯](/docs/{{version}}/eloquent-relationships)查詢：

    $flight->history()->withTrashed()->get();

#### 只取得被軟刪除的模型

`onlyTrashed` 方法會**只**取得被軟刪除的模型：

    $flights = App\Flight::onlyTrashed()
                    ->where('airline_id', 1)
                    ->get();

#### 恢復被軟刪除的模型

有時候你可能希望「取消刪除」一個被軟刪除的模型。要恢復一個被軟刪除的模型回到有效狀態，必須在模型實例上使用 `restore` 方法：

    $flight->restore();

你也可以在查詢上使用 `restore` 方法來快速地恢復多個模型：

    App\Flight::withTrashed()
            ->where('airline_id', 1)
            ->restore();

與 `withTrashed` 方法類似，`restore` 方法也可以被用在[關聯](/docs/{{version}}/eloquent-relationships):

    $flight->history()->restore();

#### 永久地刪除模型

有時候你可能需要真正地從資料庫移除模型。要永久地從資料庫移除一個被軟刪除的模型，必須使用 `forceDelete` 方法：

    // 強制刪除單一模型實例...
    $flight->forceDelete();

    // 強制刪除所有相關模型...
    $flight->history()->forceDelete();

<a name="query-scopes"></a>
## 查詢範圍

範圍（Scopes）讓你定義限制的共用集合，它可以輕鬆地在你的應用程式重複使用。例如，你可能需要頻繁地取得所有被認為是「受歡迎的」使用者。要定義範圍，必須簡單地在 Eloquent 模型方法前面加上前綴 `scope`：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 限制查詢只包括受歡迎的使用者。
         *
         * @return \Illuminate\Database\Eloquent\Builder
         */
        public function scopePopular($query)
        {
            return $query->where('votes', '>', 100);
        }

        /**
         * 限制查詢只包括活躍的使用者。
         *
         * @return \Illuminate\Database\Eloquent\Builder
         */
        public function scopeActive($query)
        {
            return $query->where('active', 1);
        }
    }

#### 利用查詢範圍

一旦定義了範圍，你可以在查詢模型時呼叫範圍方法。然而，當你呼叫方法時，你不需要加上 `scope` 前綴。你甚至能串接不同的範圍呼叫，例如：

    $users = App\User::popular()->active()->orderBy('created_at')->get();

#### 動態範圍

有時候，你可能希望定義一個接受參數的範圍。只要在你的範圍加上額外的參數即可。範圍參數應該被定義在 `$query` 參數之後：

    <?php

    namespace App;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 限制查詢只包括給定類型的使用者。
         *
         * @return \Illuminate\Database\Eloquent\Builder
         */
        public function scopeOfType($query, $type)
        {
            return $query->where('type', $type);
        }
    }

現在，你可以在呼叫範圍時傳遞參數：

    $users = App\User::ofType('admin')->get();

<a name="events"></a>
## 事件

Eloquent 模型會觸發許多事件，讓你可以藉由以下的方法，在模型的生命週期的多個時間點進行操作：`creating`、`created`、`updating`、`updated`、`saving`、`saved`、`deleting`、`deleted`、`restoring`、`restored`。事件讓你可以在每次特定的模型類別在資料庫被儲存或更新時，簡單地執行程式碼。

<a name="basic-usage"></a>
### 基本用法

當一個新模型初次被儲存，將會觸發 `creating` 以及 `created` 事件。如果一個模型已經存在於資料庫而且呼叫了 `save` 方法，將會觸發 `updating` 和 `updated` 事件。然而，在這兩個狀況下，都將會觸發 `saving` 和 `saved` 事件。

例如，讓我們來在[服務提供者](/docs/{{version}}/providers)中定義一個 Eloquent 事件監聽器。在我們的事件監聽器中，我們會在給定的模型上呼叫 `isValid` 方法，並在模型無效的時候回傳 `false`。從 Eloquent 事件監聽器回傳 `false` 會取消 `save` 和 `update` 的操作：

    <?php

    namespace App\Providers;

    use App\User;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 啟動所有應用程式服務。
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
         * 註冊服務提供者。
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }
