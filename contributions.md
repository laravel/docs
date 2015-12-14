# 貢獻導引

- [錯誤回報](#bug-reports)
- [核心開發討論](#core-development-discussion)
- [選擇分支](#which-branch)
- [安全漏洞](#security-vulnerabilities)
- [程式碼風格](#coding-style)
    - [程式碼風格修復器](#code-style-fixer)

<a name="bug-reports"></a>
## 錯誤回報

為了鼓勵積極協作，Laravel 強烈地鼓勵 pull request，而不只是回報錯誤。「錯誤回報」也可以用包含一個失敗測試的 pull request 形式發送。

然而，如果你建立錯誤回報，你的問題應該包含標題和清楚的問題描述。你也應該盡可能地提供相關的資訊和示範問題的程式碼範例。錯誤回報的目的是讓自己和其他人可以簡單地重現錯誤並開發修復程式。

請記住，我們希望建立錯誤回報可以讓其他也有相同問題的人可以與你協作解決問題。不要期望錯誤回報後會自動地看到任何動靜或其他人會馬上修復它。建立錯誤回報用於幫助自己和其他人開始修復問題。

Laravel 原始碼託管在 Github 上面，並且每個 Laravel 的專案都有自己的儲存庫：

- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Cashier](https://github.com/laravel/cashier)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Website](https://github.com/laravel/laravel.com)
- [Laravel Art](https://github.com/laravel/art)

<a name="core-development-discussion"></a>
## 核心開發討論

有關錯誤、新功能和現有功能的實作討論會在 [LaraChat](http://larachat.co) Slack 團隊的 `#internals` 頻道中進行。Laravel 的維護者 Taylor Otwell 在工作日的 8am 到 5pm（ UTC-06:00 或 America/Chicago ）通常會出現在頻道，其他時間則是零星地出現在頻道。

<a name="which-branch"></a>
## 選擇分支

**所有的**錯誤修復應該發送到最新的穩定分支。除非它們修復的功能只存在下一版的釋出中，不然錯誤修復**永遠不**應該發送到 `master` 分支。

**次要的**且與現行的 Laravel 釋出版本**完全向下相容**的功能可以發送到最新的穩定分支。

**主要的**新功能應該都發送到 `master` 分支，它包含下一版的 Laravel 釋出內容。

如果不確定你的功能是主要的還是次要的，請在 [LaraChat](http://larachat.co) Slack 團隊的 `#internals` 頻道詢問 Taylor Otwell。

<a name="security-vulnerabilities"></a>
## 安全漏洞

如果你發現 Laravel 的安全漏洞，請寄電子郵件到 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a> 給 Taylor Otwell。所有的安全漏洞，將會及時予以處理。

<a name="coding-style"></a>
## 編碼風格

Laravel 遵守 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 編碼規範和 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 自動載入規範。

### DocBlocks

`@param` tags should **not be aligned** and arguments should be separated by **2 spaces**.

Here's an example block:

    /**
     * Register a binding with the container.
     *
     * @param  string|array  $abstract
     * @param  \Closure|string|null  $concrete
     * @param  bool  $shared
     * @return void
     */
    public function bind($abstract, $concrete = null, $shared = false)
    {
        //
    }

<a name="code-style-fixer"></a>
### Code Style Fixer

You may use the [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) to fix your code style before committing.

To get started, [install the tool globally](https://github.com/FriendsOfPHP/PHP-CS-Fixer#globally-manual) and check the code style by issuing the following terminal command from your project's root directory:

```sh
php-cs-fixer fix
```
