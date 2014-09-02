# Release Notes

- [Laravel 4.2](#laravel-4.2)
- [Laravel 4.1](#laravel-4.1)

<a name="laravel-4.2"></a>
## Laravel 4.2

此發行版本的完整更動列表可以從一個 4.2 的完整安裝下，執行 `php artisan changes` 命令，或者 [Github 上的更動紀錄](https://github.com/laravel/framework/blob/4.2/src/Illuminate/Foundation/changes.json)。此紀錄僅含括主要的強化更新和此發行的更動部分。

> **附註:** 在 4.2 發佈週期間，許多小的臭蟲修正與功能強化被整併至各個 4.1 的子發行版本中。所以最好確認 Laravel 4.1 版本的更新列表。 

### PHP 5.4 需求

Laravel 4.2 需要 PHP 5.4 以上的版本。此 PHP 更新版本讓我們可以使用 PHP 的新功能：traits 來為像是[Laravel 收銀台](/docs/billing) 來提供更具表達力的介面。PHP 5.4 也比 PHP 5.3 帶來顯著的速度及效能提升。

### Laravel Forge

Larvel Forge，一個網頁應用程式，提供一個簡單的介面去建立管理你雲端上的 PHP 伺服器，像是 Linode, DigitalOcean, Rackspace, 和 Amazon EC2。支援自動化 nginx 設定、SSH 金鑰管理、Cron job 自動化、透過 NewRelic & Papertrail 伺服器監控，"推送部署", Laravel queue worker 設定等等。Forge 提供最簡單且更實惠的方式來部署所有你的 Laravel 應用程式。

預設 Laravel 4.2 的安裝裡， `app/config/database.php` 設定檔預設已為 Forge 設定完成，讓在平台上的全新應用程式更方便部署。

關於 Laravel Forge 的更多資訊可以在[官方 Forge 網站](https://forge.laravel.com)上找到。

### Laravel Homestead

Laravel Homestead 是一個為部署健全的 Laravel 和 PHP 應用程式的官方 Vagrant 環境。絕大多數的封裝包的相依與軟體在發佈前已經部署處理完成，讓封裝包可以極快的被啟用。Homestead 包含 Nginx 1.6, PHP 5.5.12, MySQL, Postres, Redis, Memcached, Beanstalk, Node, Gulp, Grunt 和 Bower。Homestead 包含一個簡單的 `Homestead.yaml` 設定檔，讓你在單一個封裝包中管理多個 Laravel 應用程式。

預設的 Laravel 4.2 安裝中包含的 `app/config/local/database.php` 設定檔使用 Homestead 的資料庫作為預設。讓 Laravel 初始化安裝與設定更為方便。

官方文件已經更新並包含在 [Homestead 文件](/docs/homestead)中。

### Laravel 收銀台

Laravel 收銀台是一個簡單、具表達性的資源庫，用來管理 Stripe 的訂閱帳務。雖然在安裝中此元件依然是選用，我們依然將收銀台文件包含在主要 Laravel 文件中。此收銀台發布版本帶來了數個錯誤修正、多貨幣支援還有支援最新的 Stripe API。

### Queue Workers 常駐程式

Artisan `queue:work` 命令現在支援 `--daemon` 參數讓 worker 可以以"常駐程式"啟用。代表 worker 可以持續的處理隊列工作不需要重啓框架。這讓一個複雜的應用程式部署過程中，使得 CPU 的使用有顯著的降低。

更多關於 Queue Workers 常駐程式資訊請詳閱 [queue 文件](/docs/queues#daemon-queue-worker)。

### Mail API Drivers

Laravel 4.2 為 `Mail` 函式採用了新的 Mailgun 和 Mandrill API 驅動。對許多應用程式而言，他提供了比 SMTP 更快也更可靠的方法來遞送郵件。新的驅動使用了 Guzzle 4 HTTP 資源庫。

### 軟刪除 Traits

對於軟刪除和全作用域更簡潔的方案
PHP 5.4 的 `traits` 提供了一個更加簡潔的軟刪除架構和全局作用域, 這些新架構為框架提供了更有擴展性的功能, 並且讓框架更加簡潔.

更多關於軟刪除的文檔請見: [Eloquent documentation](/docs/eloquent#soft-deleting).

### 更為方便的 認證(auth) & Remindable Traits

得益於 PHP 5.4 traits , 我們有了一個更簡潔的 用戶認證 和 密碼提醒接口, 這也讓 `User` 模型文件更加精簡.

### "簡易分頁"

一個新的 `simplePaginate` 方法已被加入到查詢以及 Eloquent 查詢器中。讓你在分頁視圖中，使用簡單的"上一頁"和"下一頁"連結查詢更為高效。

### 遷移確認

在正式環境中，破壞性的遷移動作將會被再次確認。如果希望取消提示字元確認請使用 `--force` 參數。

<a name="laravel-4.1"></a>
## Laravel 4.1

### 完整更動列表

此發行版本的完整更動列表，可以在版本 4.1 的安裝中命令列執行 `php artisan changes` 取得，或者瀏覽 [Github 更動檔](https://github.com/laravel/framework/blob/4.1/src/Illuminate/Foundation/changes.json)中了解。其中只記錄了該版本比較主要的強化功能和更動。

### 新的 SSH 元件

一個全新的 `SSH` 元件在此發行版本中登場。此功能讓你可以輕易的 SSH 至遠端伺服器並執行命令。更多資訊，可以參閱 [SSH 元件文件](/docs/ssh)。

新的 `php artisan tail` 指令就是使用這個新的 SSH 元件。更多的資訊，請參閱 `tail` [指令集文件](http://laravel.com/docs/ssh#tailing-remote-logs)。

### Boris In Tinker

如果您的系統支援 [Boris REPL](https://github.com/d11wtq/boris)，`php artisan thinker` 指令將會使用到它。系統中也必須先行安裝好 `readline` 和 `pcntl` 兩個 PHP 套件。如果你沒這些套件，從 4.0 之後將會使用到它。

### Eloquent 強化

Eloquent 新增了新的 `hasManyThrough` 關係鏈。想要了解更多，請參見 [Eloquent 文件](/docs/eloquent#has-many-through)。

一個新的 `whereHas` 方法也同時登場，他將允許[檢索基於關係模型的約束](/docs/eloquent#querying-relations)。

### 資料庫讀寫分離

Query Builder 和 Eloquent 目前透過資料庫層，已經可以自動做到讀寫分離。更多的資訊，請參考[文件](/docs/database#read-write-connections)。

### 隊列排序

隊列排序已經被支援，只要在 `queue:listen` 命令後將隊列以逗號分隔送出。

### 失敗隊列作業處理

現在隊列將會自動處理失敗的作業，只要在 `queue:listen` 後加上 `--tries` 即可。更多的失敗作業處理可以參見 [隊列文件](/docs/queues#failed-jobs)。

### 緩存標籤

緩存“區塊”已經被“標籤”取代。緩存標籤允許你將多個“標籤”指向同一個緩存物件，而且可以清空所有被指定某個標籤的所有物件。更多使用緩存標籤資訊請見[緩存文件](/docs/cache#cache-tags)。

### 更具彈性的密碼提醒

密碼提醒引擎已經可以提供更強大的開發彈性，如：認證密碼，顯示狀態訊息等等。使用強化的密碼提醒引擎，更多的資訊[請參閱文件](/docs/security#password-reminders-and-reset)。

### 強化路由引擎

Laravel 4.1 擁有一個完全重新編寫的路由層。API 一樣不變。然而與 4.0 相比，速度快上 100%。整個引擎大幅的簡化，且對於路由表達式的編譯大大減少對 Symfony Routing 的依賴。

### 強化 Session 引擎

此發行版本中，我們亦發佈了全新的 Session 引擎。如同路由增進的部分，新的 Session 曾更加簡化且更快速。我們不再使用 Symfony 的 Session 處理工具，並且使用更簡單、更容易維護的客製化解法。


### Doctrine DBAL

如果你有在你的遷移中使用到 `renameColumn`，之後你必須在 `composer.json` 裡加 `doctrine/dbal` 進相依套件中。此套件不再預設包含在 Laravel 之中。
