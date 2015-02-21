# 分頁

- [設置](#configuration)
- [用法](#usage)
- [添加參數至分頁連結](#appending-to-pagination-links)
- [轉換至 JSON](#converting-to-json)

<a name="configuration"></a>
## 設置

在其他的框架中，實作分頁是令人感到苦惱的事，但是 Laravel 令它實作起來變得輕鬆。 Laravel 可以產生基於當前頁面的智能「範圍」連結。所產生的 HTML 兼容 Bootstrap CSS 框架.

<a name="usage"></a>
## 用法

有幾種方式來做到項目分頁。最簡單的方式是在查詢架構器或 Eloquent 模型上使用 `paginate` 方法。

#### 對資料庫結果分頁

	$users = DB::table('users')->paginate(15);

> **注意：** 目前 Laravel 的分頁對於使用 `groupBy` 的查詢無法有效率的執行，如果您需要使用 `groupBy` 來分頁結果，建議您查詢資料庫後並手動建立分頁機制。

#### 手動建立一個分頁機制

有時你想手動建立一個分頁機制，傳遞項目陣列進去。你可以依據你的需求，選擇 `Illuminate\Pagination\Paginator` 或是 `Illuminate\Pagination\LengthAwarePaginator` 實例。

#### 對 Eloquent 模型分頁

您也可以對 [Eloquent](/docs/5.0/eloquent) 模型分頁:

	$allUsers = User::paginate(15);

	$someUsers = User::where('votes', '>', 100)->paginate(15);

傳送給 `paginate` 方法的參數是您希望每頁要顯示的項目數目，只要您取得查詢結果後，您可以在視圖中顯示結果，並使用 `render` 方法去建立分頁連結：

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
- `hasMorePages`
- `url`
- `nextPageUrl`
- `total`
- `count`

#### 「簡易分頁」

如果您只是要在您的分頁視圖顯示「上一頁」和「下一頁」連結，您有個選擇使用 `simplePaginate` 方法來更有效率地達成。當您不需要顯示頁碼在視圖上時，這個方法在龐大的資料庫上非常有用：

	$someUsers = User::where('votes', '>', 100)->simplePaginate(15);

#### 自訂分頁 URL

您還可以透過 `setPath` 方法自訂分頁的 URI：

	$users = User::paginate();

	$users->setPath('custom/url');

上面的範例將產生類似如下的鏈結：
http://example.com/custom/url?page=2

<a name="appending-to-pagination-links"></a>
## 添加參數至分頁連結

您可以在分頁器上使用 `appends` 方法添加查詢參數至分頁連結上：

	<?php echo $users->appends(['sort' => 'votes'])->render(); ?>

這樣會產生類似下列的連結：

	http://example.com/something?page=2&sort=votes

如果您想要將「雜湊片段」加到分頁的連結，您可以使用 `fragment` 方法：

	<?php echo $users->fragment('foo')->render(); ?>

此方法呼叫後將產生如下的連結：

	http://example.com/something?page=2#foo

<a name="converting-to-json"></a>
## 轉換至 JSON

`Paginator` 類別實作了 `Illuminate\Contracts\Support\JsonableInterface` 介面，且多了 `toJson` 方法。你可以從路由透過轉換 `Paginator` 實體成 JSON 並回傳。而這實體的 JSON 格式包含了一些 `meta` 資訊，例如 `total`, `current_page` 和 `last_page`。該實體資料將可透過在 JSON 陣列中 `data` 的鍵取得。
