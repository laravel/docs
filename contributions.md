# 貢獻導引

- [錯誤回報](#bug-reports)
- [核心開發討論](#core-development-discussion)
- [選擇分支](#which-branch)
- [安全缺陷](#security-vulnerabilities)
- [編碼風格](#coding-style)

<a name="bug-reports"></a>
## 錯誤回報

為了鼓勵積極合作，Laravel 強烈地鼓勵 pull request，而不只是回報錯誤。「錯誤回報」也可以用包含一個失敗的單元測試的 pull request 形式發送。

然而，如果你建立錯誤回報，你的問題應該包含標題和清楚的問題描述。你也應該盡可能地提供相關的資訊和示範問題的程式碼範例。錯誤回報的目的是讓自己和其他人可以簡單地重現錯誤並開發修復程式。

請記住，我們希望建立錯誤回報可以讓其他也有相同問題的人可以與你合作解決問題。不要期望錯誤回報後會自動地看到任何動靜或其他人會馬上修復它。建立錯誤回報用於幫助自己和其他人開始修復問題上。

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

有關錯誤、新功能和現有功能的實作討論會在 `#laravel-dev` IRC 頻道（ Freenode ）裡面。Laravel 的維護者 Taylor Otwell 在工作日的 8am 到 5pm（ UTC-06:00 或 America/Chicago ）通常會出現在頻道，其他時間則是零星地出現在頻道。

`#laravel-dev` IRC 頻道開放給所有人。不論是參與討論或是只是想觀看討論都歡迎加入頻道！

<a name="which-branch"></a>
## 選擇分支

**所有的**錯誤修復應該發送到最新的穩定分支。除非它們修復的功能只存在下一版的釋出中，不然錯誤修復**永遠不** 應該發送到 `master` 分支。

**次要的**且與現行的 Laravel 釋出版本**完全向下相容**的功能可以發送到最新的穩定分支。

**主要的**新功能應該總是發送到 `master` 分支，它包含下一版的 Laravel 釋出內容。

如果你不確定你的功能是主要的還是次要的，請在 `#laravel-dev` IRC 頻道（ Freenode ）詢問 Taylor Otwell。

<a name="security-vulnerabilities"></a>
## 安全缺陷

如果你發現 Laravel 的安全漏洞，請寄電子郵件到 <a href="mailto:taylorotwell@gmail.com">taylorotwell@gmail.com</a> 給 Taylor Otwell。所有的安全漏洞，將會及時予以處理。

<a name="coding-style"></a>
## 編碼風格

Laravel 遵循 [PSR-0](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-0.md) 和 [PSR-1](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-1-basic-coding-standard.md) 編碼規範。除了這些規範以外，以下編碼規範也應該遵守：

- 類別的命名空間宣告必須跟 `<?php` 在同一行。
- 類別的起始 `{` 必須跟類別名稱在同一行。
- 函式跟控制結構必須使用 Allman style braces。
- 用 tab 縮排，用空白對齊。
