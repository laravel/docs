# 分頁

- [設置](#configuration)
- [使用](#usage)
- [追加分頁連結](#appending-to-pagination-links)
- [轉換至 JSON](#converting-to-json)

<a name="configuration"></a>
## 設置

在其他的框架中，實作分頁是令人感到苦惱的事，但是 Laravel 令它實作起來變得輕鬆。 Laravel 可以產生基於當前頁面的智慧「範圍」連結，所產生的 HTML 兼容 Bootstrap CSS 框架.

<a name="usage"></a>
## 使用

有幾種方法來分頁項目。最簡單的是在搜尋建立器使用 `paginate` 方法或 Eloquent 模型。

#### 對資料庫結果分頁

	$users = DB::table('users')->paginate(15);

> **注意：** 目前 Laravel 使用 `groupBy` 來做分頁操作無法有效率的執行，如果您需要使用 `groupBy` 來分頁資料集，建議您手動查詢資料庫，並使用 `Paginator::make`。

#### 對 Eloquent 模型分頁

您也可以對 [Eloquent](/docs/5.0/eloquent) 模型分頁:

	$allUsers = User::paginate(15);

	$someUsers = User::where('votes', '>', 100)->paginate(15);

傳送給 `paginate` 方法的參數是您希望每頁要顯示的項目選項數目，只要您取得查詢結果後，您可以在視圖中顯示，並使用 `render` 方法去建立分頁連結：

	<div class="container">
		<?php foreach ($users as $user): ?>
			<?php echo $user->name; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $users->render(); ?>

這就是所有建立分頁系統的步驟了！您會注意到我們還沒有告知 Laravel 我們目前的頁面是哪一頁，這個資訊 Laravel 會自動幫您做好。

您也可以透過以下方法獲得額外的分頁資訊：

- `currentPage`
- `lastPage`
- `perPage`
- `total`
- `count`

#### 「簡單分頁」

如果您只是要在您的分頁視圖顯示「上一頁」和「下一頁」連結，您有個選項 `simplePaginate` 方法來執行更高效率的搜尋。當您不需要精準的顯示頁碼在視圖上時，這個方法在較大的資料集非常有用：

	$someUsers = User::where('votes', '>', 100)->simplePaginate(15);

#### 手動建立分頁

有的時候您可能會想要從陣列中項目手動建立分頁實體， 您可以根據您的需要透過 `Illuminate\Pagination\Paginator` 或 `Illuminate\Pagination\LengthAwarePaginator` 實體來建立。

#### 自訂分頁 URL

您還可以透過 `setPath` 方法自訂使用的 URL：

	$users = User::paginate();

	$users->setPath('custom/url');

上面的範例將建立 URL，類似以下內容：
http://example.com/custom/url?page=2

<a name="appending-to-pagination-links"></a>
## 追加分頁連結

您可以使用 `appends` 方法增加搜尋字串到分頁連結中：

	<?php echo $users->appends(['sort' => 'votes'])->render(); ?>

這樣會產生類似下列的連結：

	http://example.com/something?page=2&sort=votes

如果您想要將「雜湊片段」加到分頁的 URL，您可以使用 `fragment` 方法：

	<?php echo $users->fragment('foo')->render(); ?>

此方法呼叫後將產生 URL，看起來像這樣：

	http://example.com/something?page=2#foo

<a name="converting-to-json"></a>
## 轉換至 JSON

`Paginator` 類別實作 `Illuminate\Contracts\Support\JsonableInterface` 介面的 `toJson` 方法。由路由返回的值，您可能將 `Paginator` 實體傳換成 JSON。JSON 表單的實體會包含一些「後設」資訊，例如 `total`、`current_page`、`last_page`。該實體資料將可透過在 JSON 陣列中 `data` 的鍵取得。
