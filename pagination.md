# Pagination

- [設置](#configuration)
- [使用](#usage)
- [加入分頁連結](#appending-to-pagination-links)
- [轉換至 JSON](#converting-to-json)
- [自定表示器（Presenter）](#custom-presenters)

<a name="configuration"></a>
## 設置

在其他的框架中，實作分頁是令人感到苦惱的事，但是 Laravel 令它實作起來變得輕鬆。在 `app/config/view.php` 檔案中有設置選項可以設定，`pagination` 選項需要指定用哪個視圖來建立分頁，而 Laravel 預設包含兩種視圖。

`pagination::slider` 視圖將會基於現在的頁面智慧的顯示「範圍」的頁數連結，`pagination::simple` 視圖將僅顯示「上一頁」和「下一頁」的按鈕。**兩種視圖都相容  Twitter Bootstrap 框架**

<a name="usage"></a>
## 使用

有幾種方法來分頁項目。最簡單的是在搜尋建立器或 Eloquent 模型使用 `paginate` 方法。

#### 對資料庫結果分頁

	$users = DB::table('users')->paginate(15);

#### 對 Eloquent 模型分頁

您也可以對 [Eloquent](/docs/eloquent) 模型分頁：

	$allUsers = User::paginate(15);

	$someUsers = User::where('votes', '>', 100)->paginate(15);

傳送給 `paginate` 方法的參數是您希望每頁要顯示的項目選項數目，只要您取得查詢結果後，您可以在視圖中顯示，並使用 `links` 方法去建立分頁連結：

	<div class="container">
		<?php foreach ($users as $user): ?>
			<?php echo $user->name; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $users->links(); ?>

這就是所有建立分頁系統的步驟了! 您會注意到我們還沒有告知 Laravel 我們目前的頁面是哪一頁，這個資訊 Laravel 會自動幫您做好。

如果您想要指定自訂的視圖來使用分頁，您可以透過 `links` 方法至視圖：

	<?php echo $users->links('view.name'); ?>

您也可以透過以下方法獲得額外的分頁資訊：

- `getCurrentPage`
- `getLastPage`
- `getPerPage`
- `getTotal`
- `getFrom`
- `getTo`
- `count`


#### 「簡單分頁」

如果您只是要在您的分頁視圖顯示「上一頁」和「下一頁」連結，您有個選項 `simplePaginate`  方法來執行更高效率的搜尋。當您不需要精準的顯示頁碼在視圖上時，這個方法在較大的資料集非常有用：

	$someUsers = User::where('votes', '>', 100)->simplePaginate(15);

#### 手動建立分頁

有的時候您可能會想要從陣列中項目手動建立分頁實例。您可以使用 `Paginator::make` 方法：

	$paginator = Paginator::make($items, $totalItems, $perPage);

#### 自訂分頁 URL

您還可以透過 `setBaseUrl` 方法自訂使用的 URL：

	$users = User::paginate();

	$users->setBaseUrl('custom/url');

上面的範例將建立 URL，類似以下內容： http://example.com/custom/url?page=2

<a name="appending-to-pagination-links"></a>
## 加入分頁連結

您可以使用 `appends` 方法增加搜尋字串到分頁連結中：

	<?php echo $users->appends(array('sort' => 'votes'))->links(); ?>

這樣會產生類似下列的連結：

	http://example.com/something?page=2&sort=votes

如果您想要將「雜湊片段」加到分頁的 URL，您可以使用 `fragment` 方法：

	<?php echo $users->fragment('foo')->links(); ?>

此方法呼叫後將產生 Url，看起來像這樣：

	http://example.com/something?page=2#foo

<a name="converting-to-json"></a>
## 轉換至 JSON

`Paginator` 類別實作 `Illuminate\Support\Contracts\JsonableInterface` 介面的 `toJson` 公開方法。 由路由返回的值，您可能將 `Paginator` 實力傳換成 JSON。JSON 表單的實力會包含一些「後設」資訊，例如 `total`, `current_page`, `last_page`, `from` , `to`。該實例資料將可透過在 JSON 陣列中 `data` 的鍵取得。

<a name="custom-presenters"></a>
## 自訂表示器（Presenter）

預設的分頁表示器是相容 Bootstarp的。不過，您也可以自訂表示器（presenter）

### 擴展抽象表示器（Presenter）

實作 `Illuminate\Pagination\Presenter` 類別的抽象方法。Zurb Foundation 的表示器（presenter）範例如下：

    class ZurbPresenter extends Illuminate\Pagination\Presenter {

        public function getActivePageWrapper($text)
        {
            return '<li class="current"><a href="">'.$text.'</a></li>';
        }

        public function getDisabledTextWrapper($text)
        {
            return '<li class="unavailable">'.$text.'</li>';
        }

        public function getPageLinkWrapper($url, $page)
        {
            return '<li><a href="'.$url.'">'.$page.'</a></li>';
        }

    }

### 使用自訂表示器（Presenter）

首先，在 `app/views` 建立新的視圖，這將會作為您的自定表示器（presenter）。並且用新的視圖取代 `app/config/view.php` 的 `pagination` 設定。最後，類似下方的程式碼會放在您的自定表示器（presenter）視圖中。

    <ul class="pagination">
        <?php echo with(new ZurbPresenter($paginator))->render(); ?>
    </ul>
