# 分頁

- [簡介](#introduction)
- [基本使用](#basic-usage)
    - [對查詢產生器分頁](#paginating-query-builder-results)
    - [對 Eloquent 模型分頁](#paginating-eloquent-results)
    - [手動建立分頁](#manually-creating-a-paginator)
- [將分頁結果顯示在視圖中](#displaying-results-in-a-view)
- [轉換至 JSON](#converting-results-to-json)

<a name="introduction"></a>
## 簡介

在其他的框架中，分頁是非常讓人苦惱的。而在 Laravel 中是很輕而易舉的。 Laravel 可以快速產生基於當前頁面的智能「範圍」，並且產生的 HTML 兼容於 [Bootstrap CSS 框架](http://getbootstrap.com/)。

<a name="basic-usage"></a>
## 基本使用

<a name="paginating-query-builder-results"></a>
### 對查詢產生器分頁

有幾種方法對項目進行分頁。最簡單的是使用 `paginate` 方法在使用[查詢產生器](/docs/{{version}}/queries)或是 [Eloquent 查詢](/docs/{{version}}/eloquent)時。由 Laravel 提供的 `paginate` 方法自動判定當前頁面正確的數量限制和偏移數。預設狀況下，當前頁數由 HTTP 請求所帶的 `?page` 參數來決定。當然，該值由 Laravel 自動檢測，並自動帶入由分頁器產生的連結。

首先，讓我們來看看在資料庫查詢時使用 `paginate` 方法。在這個例子中，傳遞給 `paginate` 唯一的參數是您想在「每頁」顯示的資料數。在這個例子中，我們指定每頁顯示 `15` 筆資料：

    <?php

    namespace App\Http\Controllers;

    use DB;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Show all of the users for the application.
         *
         * @return Response
         */
        public function index()
        {
            $users = DB::table('users')->paginate(15);

            return view('user.index', ['users' => $users]);
        }
    }

> **注意：**目前， Laravel 的分頁無法有效操作含有 `groupBy` 語句。如果您需要對使用 `groupBy` 的結果做分頁，建議您查詢資料庫後再手動製作分頁。

#### 「簡易分頁」

如果在您的視圖只需要顯示簡單的「下一步」和「上一步」連結，您可以選擇使用 `simplePaginate` 方法來進行更高效的查詢。如果您不需要在頁面上顯示每個頁碼時，這對於大型數據非常有用：

    $users = DB::table('users')->simplePaginate(15);

<a name="paginating-eloquent-results"></a>
### 對 Eloquent 模型分頁

您也可以對 Eloquent 進行分頁。在這個例子中，我們將對 `User` 模型進行分頁並且設定每頁有 `15` 筆資料。正如您所看到的，語法與對查詢產生器進行分頁幾乎是一樣的：

    $users = App\User::paginate(15);

當然，您可以對 `paginate` 設置其他限制的查詢，如 `where` 條件：

    $users = User::where('votes', '>', 100)->paginate(15);

您也可以在使用 Eloquent 模型進行分頁時使用 `simplePaginate` 方法：

    $users = User::where('votes', '>', 100)->simplePaginate(15);

<a name="manually-creating-a-paginator"></a>
### 手動建立分頁

有時候您可能會希望從項目的陣列中手動創建一個分頁實例。您可以依據您的需求決定創建 `Illuminate\Pagination\Paginator` 或是 `Illuminate\Pagination\LengthAwarePaginator` 。

`Paginator` 類別不需要知道資料的總筆數；然而因為這點，它也無法提供取得最後一頁的方法。`LengthAwarePaginator` 與 `Paginator` 的參數幾乎相同；但是它需要資料的總筆數。

換句話說， `Paginator` 對應於查詢產生器和 Eloquent 的 `simplePaginate` 方法，而 `LengthAwarePaginator` 相等於 `paginate` 方法。

當手動創建一個分頁器實例時，您應該手動「切割」傳遞給分頁器的陣列。如果您不確定如何做到這一點，請查閱 PHP 的 [array_slice](http://php.net/manual/en/function.array-slice.php) 函式。

<a name="displaying-results-in-a-view"></a>
## 將分頁結果顯示在視圖中

當在查詢產生器或 Eloquent 中使用 `simplePaginate` 方法或使用 `paginate` 方法，您會得到一個分頁器的實例。當使用 `paginate` 方法時，將得到 `Illuminate\Pagination\LengthAwarePaginator` 的實例。當使用 `simplePaginate` 方法時，會得到 `Illuminate\Pagination\Paginator` 的實例。這些對象提供幾種方法用來描述結果集。除了這些輔助方法，分頁器的實例也是個迭代器，並且可以像陣列一樣使用迴圈取值。

總之，一旦您已經取得結果，您可以顯示結果，並使用 [Blade 模板](/docs/{{version}}/blade)渲染頁面的連結：

    <div class="container">
        @foreach ($users as $user)
            {{ $user->name }}
        @endforeach
    </div>

    {!! $users->render() !!}

`render` 方法將給予查詢結果中其他頁面的連結。每一個連結中都已經包含正確的 `?page` 查詢字符串變量。請記住，由 `render` 方法產生的 HTML 皆兼容於 [Bootstrap CSS 框架](https://getbootstrap.com)。

> **注意：**當在 Blade 模版中使用 `render` 方法時，一定要使用 `{！ ！}` 語法，HTML 連結才不會被跳脫。

#### 自定義分頁器的 URI

`setPath` 方法允許您在產生連結時自定義 URI 。例如，如果您希望分頁器產生像 `http://example.com/custom/url?page=N` ，您應該使用 `setPath` 方法將 `custom/url` 將加到分頁中：

    Route::get('users', function () {
        $users = App\User::paginate(15);

        $users->setPath('custom/url');

        //
    });

#### 加入參數到分頁連結中

您可以使用 `appends` 方法添加所需要的參數到分頁連結中。例如，要加入 `&sort=votes` 到每個分頁連結時，您應該這樣使用 `appends` 方法：

    {!! $users->appends(['sort' => 'votes'])->render() !!}

如果您想加入一個有「雜湊片段」的分頁器連結網址，您可以使用 `fragment` 方法。例如，要在每個分頁連結的最後加入 `#foo` ，應該這樣使用 `fragment` 方法：

    {!! $users->fragment('foo')->render() !!}

#### 其他輔助方法

您也可以透過以下方法獲得額外的分頁資訊：

- `$results->count()`
- `$results->currentPage()`
- `$results->hasMorePages()`
- `$results->lastPage() (在 simplePaginate 中無法使用)`
- `$results->nextPageUrl()`
- `$results->perPage()`
- `$results->previousPageUrl()`
- `$results->total()（在 simplePaginate 中無法使用）`
- `$results->url($page)`

<a name="converting-results-to-json"></a>
## 轉換至 JSON

Laravel 的分頁類別實現了 `Illuminate\Contracts\Support\JsonableInterface` 的 `toJson` 方法，所以很容易將您的分頁結果轉換成 JSON 。

您可以將一個分頁器實例轉換為 JSON ，只需要簡單地從一個路由或控制器中回傳它：

    Route::get('users', function () {
        return App\User::paginate();
    });

分頁器的 JSON 將包括分頁相關的資訊，如 `total` ， `current_page` ， `last_page` ，等等。該實例資料可透過 JSON 陣列中的 `data` 鍵中取得。下方是從路由回傳的分頁器實例轉換成 JSON 的一個例子：

#### 分頁結果轉為 JSON 的例子

    {
       "total": 50,
       "per_page": 15,
       "current_page": 1,
       "last_page": 4,
       "next_page_url": "http://laravel.app?page=2",
       "prev_page_url": null,
       "from": 1,
       "to": 15,
       "data":[
            {
                // Result Object
            },
            {
                // Result Object
            }
       ]
    }
