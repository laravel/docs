# 測試：入門

- [介紹](#introduction)
- [環境](#environment)
- [建立並執行測試](#creating-and-running-tests)

<a name="introduction"></a>
## 介紹

Laravel 在建立時有考慮到測試這件事。事實上，內建已經支援使用 PHPUnit 測試，而且 `phpunit.xml` 檔案也已經幫你設定好應用程式的測試設定。框架還附帶便利的輔助函式方法，可以讓你更直觀的測試應用程式。

預設應用程式的 `tests` 目錄會有兩個子目錄：`Feature` 和 `Unit`。單元測試主要測試非常小且能獨立於你的程式碼部分。實際上，大多數的單元測試可能只專注於單一個方法。功能測試可以測試大部分的程式碼，包含一些物件如何進行互動，甚至是完整的 HTTP 請求到一個 JSON 端點。

`Feature` 和 `Unit` 測試目錄都提供了一個名為 `ExampleTest.php` 的檔案。在安裝新 Laravel 應用程式之後，在命令列上執行 `phpunit` 來執行你的測試。

<a name="environment"></a>
## 環境

透過 `phpunit` 執行測試時，因為在 `phpunit.xml` 檔案定義環境變數，Laravel 會自動將環境設定為 `testing`。Laravel 還會在測試時自動將 Session 和快取設定到 `array` 驅動，也就是說不會保留在測試時的 Session 或快取資料。

你是可以自由的根據需要來定義其他測試環境設定值。`testing` 環境變數可以被設定在 `phpunit.xml` 檔案中，但是要確保在執行測試前有執行 Artisan 指令的 `config:clear` 來清除設定檔的快取！

另外，你可以在專案根目錄建立 `.env.testing` 檔。這個檔案會在運行 PHPUnit 測試或者執行包含 `--env=testing` 選項的 Artisan 指令時，覆蓋原本的 `.env` 設定。

<a name="creating-and-running-tests"></a>
## 建立並執行測試

要建立一個新的測試案例，請使用 Artisan 指令的 `make:test`：

    // 在功能測試目錄建立一個測試...
    php artisan make:test UserTest

    // 在單元測試目錄建立一個測試...
    php artisan make:test UserTest --unit

測試一旦被產生，你可以像是在使用 PHPUnit 來定義測試方法。若要執行測試，只要在終端機執行 `phpunit` 指令：

    <?php

    namespace Tests\Unit;

    use PHPUnit\Framework\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * 一個基礎測試範例。
         *
         * @return void
         */
        public function testBasicTest()
        {
            $this->assertTrue(true);
        }
    }
   
> {note} 如果你在測試類別中定義自己的 `setUp` / `tearDown` 方法，請別忘了呼叫 `parent::setUp()` / `parent::tearDown()`。
