# Laravel Valet

- [介紹](#introduction)
    - [Valet 與 Homestead](#valet-or-homestead)
- [安裝](#installation)
    - [升級](#upgrading)
- [啟動專案](#serving-sites)
    - [「Park」指令](#the-park-command)
    - [「Link」指令](#the-link-command)
    - [使用 TLS 保護](#securing-sites)
- [共享網站](#sharing-sites)
- [Site Specific Environment Variables](#site-specific-environment-variables)
- [自訂 Valet 驅動](#custom-valet-drivers)
    - [本機驅動](#local-drivers)
- [其它 Valet 指令](#other-valet-commands)

<a name="introduction"></a>
## 介紹

Valet 是專屬於 MacOS 的 Laravel 開發環境。既不用 Vagrant，也不用 `/etc/hosts` 檔案，就能夠使用本機終端機來公開並共享你的網站。_沒錯！我們也很喜歡。_

Laravel Valet 設定 MacOS 在啟動伺服器時會在背景執行 [Nginx](https://www.nginx.com/)。然後，使用 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)，Valet 會將所有本機伺服器上安裝的專案全都代理到 `*.test` 網域上。

換句話說，這個極快的 Laravel 開發環境只會用到 7 MB 的記憶體。Valet 並非能完全取代 Vagrant 或 Homestead，但如果你想要靈活、極快、或更輕盈的開發環境，這會是一個很好的選擇。

Valet 預設就支援以下這些內容，當然，實際支援的內容還有更多：

<style>
    #valet-support > ul {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        line-height: 1.9;
    }
</style>

<div id="valet-support" markdown="1">
- [Laravel](https://laravel.com)
- [Lumen](https://lumen.laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [Concrete5](https://www.concrete5.org/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- Static HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)
</div>

對了，你可以使用[自訂驅動](#custom-valet-drivers)來擴展 Valet。

<a name="valet-or-homestead"></a>
### Valet 與 Homestead

就如你所知的那樣，Laravel 提供了另一個開發環境，也就是 [Homestead](/docs/{{version}}/homestead)。Homestead 和 Valet 不同的地方在於他們主要客群想使用什麼方式來建立開發環境。Homestead 提供一個完整的 Ubuntu 虛擬機，並自動化 Nginx 設定。如果你想要完全虛擬化的 Linux  開發環境或者在 Windows / Linux 系統環境上開發，Homestead 會是一個很好的選擇。

Valet 只支援 MacOS，並且會要求你在本機環境上直接安裝 PHP 和資料庫伺服器。你可以使用 [Homebrew](http://brew.sh/) 的 `brew install php72` 和 `brew install mysql` 指令來輕鬆的安裝。Valet 提供了一個極快的本機開發環境，且只會佔用到極小的資源，所以這對於只會用到 PHP 和 MySQL 而不需要完整的虛擬開發環境的開發者而言真的很好！

不論是 Valet 還是 Homestead 都是設定 Laravel 開發環境的最佳選項。請根據你與團隊的喜好與需求來做選擇。

<a name="installation"></a>
## 安裝

**Valet 的基本要求是 macOS 系統並安裝 [Homebrew](http://brew.sh/)。在安裝之前，你應該確認沒有像是 Apache 或 Nginx 的程式有占用到本機的 80 Port**

<div class="content-list" markdown="1">
- 使用 `brew update` 來安裝或更新 [Homebrew](http://brew.sh/) 的最新的版本。
- 使用 Homebrew 的 `brew install php` 指令來安裝 PHP 7.3
- 安裝 [Composer](https://getcomposer.org).
- 使用 Composer 的 `composer global require laravel/valet` 指令來安裝 Valet。並確認 `~/.composer/vendor/bin` 目錄有在你系統的 「PATH」。
- 執行 `valet install` 指令。這指令會為你設定並安裝 Valet 和 DnsMasq，並於系統啟動時自動註冊守護行程。
</div>

Valet 一旦安裝好了，就可以在終端機上使用像是 `ping foobar.test` 指令來測試任何 `*.test` 網域的連線狀態。如果有成功安裝 Valet ，你應該會看到這個網域回應 `127.0.0.1`。

Valet 會在每次被啟動時自動開啟他的守護行程。一旦完成了第一次的 Valet 安裝，就不需要再執行 `valet start` 或 `valet install` 指令了。

#### 使用其它的網域

By default, Valet serves your projects using the `.test` TLD. If you'd like to use another domain, you can do so using the `valet tld tld-name` command.

For example, if you'd like to use `.app` instead of `.test`, run `valet tld app` and Valet will start serving your projects at `*.app` automatically.

#### Database

If you need a database, try MySQL by running `brew install mysql@5.7` on your command line. Once MySQL has been installed, you may start it using the `brew services start mysql@5.7` command. You can then connect to the database at `127.0.0.1` using the `root` username and an empty string for the password.

#### PHP Versions

Valet allows you to switch PHP versions using the `valet use php@version` command. Valet will install the specified PHP version via Brew if it is not already installed:

    valet use php@7.2

    valet use php

<a name="upgrading"></a>
### Upgrading

You may update your Valet installation using the `composer global update` command in your terminal. After upgrading, it is good practice to run the `valet install` command so Valet can make additional upgrades to your configuration files if necessary.

#### Upgrading To Valet 2.0

Valet 2.0 transitions Valet's underlying web server from Caddy to Nginx. Before upgrading to this version you should run the following commands to stop and uninstall the existing Caddy daemon:

    valet stop
    valet uninstall

Next, you should upgrade to the latest version of Valet. Depending on how you installed Valet, this is typically done through Git or Composer. If you installed Valet via Composer, you should use the following command to update to the latest major version:

    composer global require laravel/valet

Once the fresh Valet source code has been downloaded, you should run the `install` command:

    valet install
    valet restart

After upgrading, it may be necessary to re-park or re-link your sites.

<a name="serving-sites"></a>
## Serving Sites

Once Valet is installed, you're ready to start serving sites. Valet provides two commands to help you serve your Laravel sites: `park` and `link`.

<a name="the-park-command"></a>
**The `park` Command**

<div class="content-list" markdown="1">
- Create a new directory on your Mac by running something like `mkdir ~/Sites`. Next, `cd ~/Sites` and run `valet park`. This command will register your current working directory as a path that Valet should search for sites.
- Next, create a new Laravel site within this directory: `laravel new blog`.
- Open `http://blog.test` in your browser.
</div>

**That's all there is to it.** Now, any Laravel project you create within your "parked" directory will automatically be served using the `http://folder-name.test` convention.

<a name="the-link-command"></a>
**`link` 指令**

The `link` command may also be used to serve your Laravel sites. This command is useful if you want to serve a single site in a directory and not the entire directory.

<div class="content-list" markdown="1">
- To use the command, navigate to one of your projects and run `valet link app-name` in your terminal. Valet will create a symbolic link in `~/.config/valet/Sites` which points to your current working directory.
- After running the `link` command, you can access the site in your browser at `http://app-name.test`.
</div>

To see a listing of all of your linked directories, run the `valet links` command. You may use `valet unlink app-name` to destroy the symbolic link.

> {tip} You can use `valet link` to serve the same project from multiple (sub)domains. To add a subdomain or another domain to your project run `valet link subdomain.app-name` from the project folder.

<a name="securing-sites"></a>
**使用 TLS 保護**

預設的 Valet 只會啟動未加密的 HTTP。然而，如果你想要使用 HTTP/2 的加密 TLS 來啟動專案，請使用 `secure` 指令。例如，如果你的專案被啟動在 Valet 上的 `laravel.test` 網域，你你應該執行以下指令來保護它：

    valet secure laravel

若要「解除」專案的安全協定，並恢復到未加密的 HTTP，請使用 `unsecure` 指令。就像使用 `secure` 指令一樣，這個指令接受你想要解除的主機名稱：

    valet unsecure laravel

<a name="sharing-sites"></a>
## 共享專案

Valet 甚至包括與世界分享你的本機網站的指令。一旦安裝了 Valet，就不需要安裝額外的軟體。

若要共享專案，請導航到終端機中的專案目錄，並執行 `valet share` 指令。會將可被公開存取的 URL 放入剪貼簿中，並準備貼到瀏覽器。就這樣。

若要停止共享專案，請點擊 `Control + C` 來終止共享。

<a name="site-specific-environment-variables"></a>
## Site Specific Environment Variables

Some applications using other frameworks may depend on server environment variables but do not provide a way for those variables to be configured within your project. Valet allows you to configure site specific environment variables by adding a `.valet-env.php` file within the root of your project. These variables will be added to the `$_SERVER` global array:

    <?php

    return [
        'WEBSITE_NAME' => 'My Blog',
    ];

<a name="custom-valet-drivers"></a>
## 自訂 Valet 驅動

你能夠撰寫屬於自己的 Valet「驅動」來啟動 Valet 不支援的其他框架或 CMS 的 PHP 應用程式。當你安裝 Valet 的時候，會建立一個包含 `SampleValetDriver.php`  檔案的 `~/.valet/Drivers` 目錄。這個檔案包含一個簡易的驅動實作來示範如何撰寫自訂驅動。撰寫一個驅動只需要你實作三種方法：`serves`、`isStaticFile` 和 `frontControllerPath`。

這三種方法都接受 `$sitePath`、`$siteName` 和 `$uri` 的值作為它們的參數。`$sitePath` 會是在本機上的專案完整路徑，像是 `/Users/Lisa/Sites/my-project`。`$siteName` 會是網域（`my-project`）的「主機」或專案名稱的部分。`$uri` 則是傳入請求的 URI (`/foo/bar`)。

你一旦完成了自訂 Valet 驅動，請使用 `FrameworkValetDriver.php` 慣例命名方式將它放置於 `~/.valet/Drivers` 目錄中。例如，如果你正在為 WordPress 撰寫自訂的 Valet 驅動，你的檔名應該會是 `WordPressValetDriver.php`。

讓我們來看看自訂 Valet 驅動應該實作的每種方法的簡單實作。

#### `serves` 方法

如果你的驅動會去處理傳入請求，`serves` 方法會回傳 `true`。反之，該方法則回傳 `false`。因此，在這個方法中，你應該嘗試確認給定的 `$sitePath` 是否有你想要啟動的類型專案。

例如，讓我們假設正在撰寫 `WordPressValetDriver`。我們的 `serve` 方法看起來會像是這樣：

    /**
     * 檢查是否需要該驅動。
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return bool
     */
    public function serves($sitePath, $siteName, $uri)
    {
        return is_dir($sitePath.'/wp-admin');
    }

#### `isStaticFile` 方法

`isStaticFile` 會去檢查傳入的請求是不是「靜態」檔案，像是圖像或樣式表。如果該檔案為靜態，該方法會回傳硬碟上的靜態檔案的完整路徑。如果傳入請求不是靜態檔案，該方法會回傳 `false`：

    /**
     * 檢查傳入的請求是否為靜態檔案。
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return string|false
     */
    public function isStaticFile($sitePath, $siteName, $uri)
    {
        if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
            return $staticFilePath;
        }

        return false;
    }

> {note} `isStaticFile` 方法只會在 `serves` 方法回傳 `true` 的時候傳入請求，並且該請求的 URL 不是 `/` 時呼叫該方法。

#### `frontControllerPath` 方法

`frontControllerPath` 方法會回傳符合條件的完整路徑到應用程式的「前端控制器」，這通常是你的「index.php」或相同性質的檔案：

    /**
     * 取得符合條件的完整路徑到應用程式的前端控制器。
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return string
     */
    public function frontControllerPath($sitePath, $siteName, $uri)
    {
        return $sitePath.'/public/index.php';
    }

<a name="local-drivers"></a>
### 本機驅動

如果你想要為專為一個應用程式定義一個自訂的 Valet 驅動，請在應用程式的根目錄中建立  `LocalValetDriver.php`。你自訂的驅動會去繼承底層的 `ValetDriver` 類別或指定繼承現有的驅動，像是 `LaravelValetDriver`：

    class LocalValetDriver extends LaravelValetDriver
    {
        /**
         * 檢查該驅動是否有被需要。
         *
         * @param  string  $sitePath
         * @param  string  $siteName
         * @param  string  $uri
         * @return bool
         */
        public function serves($sitePath, $siteName, $uri)
        {
            return true;
        }

        /**
         * 取得應用程式的前端控制器完整路徑。
         *
         * @param  string  $sitePath
         * @param  string  $siteName
         * @param  string  $uri
         * @return string
         */
        public function frontControllerPath($sitePath, $siteName, $uri)
        {
            return $sitePath.'/public_html/index.php';
        }
    }

<a name="other-valet-commands"></a>
## 其它 Valet 指令

指令  | 說明
------------- | -------------
`valet forget` | 從被「Park」標記的目錄中執行這個指令，可以移除對它的標記。
`valet log` | View a list of logs which are written by Valet's services.
`valet paths` | 查看所有被「Park」標記的路徑。
`valet restart` | 重新啟動 Valet 的守護行程。
`valet start` | 啟動 Valet 的守護行程。
`valet stop` | 暫停 Valet 的守護行程。
`valet trust` | Add sudoers files for Brew and Valet to allow Valet commands to be run without prompting for passwords.
`valet uninstall` | 完整的移除 Valet 守護行程。
