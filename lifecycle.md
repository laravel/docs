# 請求的生命週期

- [簡介](#introduction)
- [生命週期概要](#lifecycle-overview)
- [聚焦於服務提供者](#focus-on-service-providers)

<a name="introduction"></a>
## 簡介

使用「真實世界」中的任何工具時，若能瞭解它是如何運作的，你會更具信心。開發應用程式並無二致。當你明白你的開發工具運作的方式，使用它們時，會感到更舒適、更有信心。

這份文件的目的在給予你一個優良且高階的概述，關於 Laravel 框架是如何「運作」的。當你愈瞭解整個框架，這些事情便不再那麼令人感到「神奇」，而你在建立應用程式時也會更具信心。

若你目前還無法瞭解所有的術語，不要灰心！只要試著對現在提到的東西有個基本掌握，你的知識將會隨著你探索這份文件其他章節的同時跟著成長。

<a name="lifecycle-overview"></a>
## 生命週期概要

### 首要之事

`public/index.php` 這個檔案是對 Laravel 應用程式所有請求的進入點。所有的請求都透過你的網頁伺服器（Apache / Nginx）的設定導向這個檔案。`index.php` 這個檔案並沒有太多的程式碼。更確切地說，它只是個起始點，用來載入框架其他的部分。

`index.php` 此檔案會載入由 Composer 產生的自動載入器定義，並擷取由 `bootstrap/app.php` 指令稿所產生的 Laravel 應用程式實例。Laravel 自身的第一個動作就是創建一個應用程式／[服務容器](/docs/{{version}}/container)的實例。

### HTTP / 終端核心

接下來，進入應用程式的請求的會被送往 HTTP 核心或終端核心，視該請求的種類而定。這兩種核心是所有請求流向的中心位置。現在開始，我們只將焦點放在 HTTP 核心，它位於 `app/Http/Kernel.php`。

HTTP 核心擴展了 `Illuminate\Foundation\Http\Kernel` 類別，它定義了一個 `bootstrappers` 陣列，在請求被執行前會先行運作。這些啟動器設定了錯誤處理、日誌記錄、[偵測應用程式環境](/docs/{{version}}/installation#environment-configuration)，並執行其他在請求被實際處理前，需要完成的工作。

HTTP 核心也定義了一份 HTTP [中介層](/docs/{{version}}/middleware)清單，所有的請求在被應用程式處理之前都必須經過它們。這些中介層處理 [HTTP session](/docs/{{version}}/session) 的讀寫、[驗證 CSRF 標記](/docs/{{version}}/routing#csrf-protection)、決定應用程式是否處於維護模式，以及其他更多工作。

HTTP 核心 `handle` 方法的方法簽章相當簡單：接收一個 `Request` 並回傳一個 `Response`。把核心想像成一個大的黑盒子，代表你完整的應用程式。餵給它 HTTP 請求，它就會傳回 HTTP 回應。

#### 服務提供者

最重要的核心啟動載入行為之一，是載入你的應用程式的[服務提供者](/docs/{{version}}/providers)。應用程式的所有服務提供者，都在 `config/app.php` 此設定檔的 `providers` 陣列中被設定。首先，所有提供者的 `register` 方法會被呼叫，一旦所有提供者都被註冊之後，`boot` 方法就會被呼叫。

服務提供者負責在啟動時載入所有的框架各式元件，例如資料庫、隊列、驗證、以及路由元件。服務提供者啟動載入並設定框架提供的各種功能，是整個 Laravel 啟動載入過程中最重要的面向。

#### 請求分派

一旦應用程式被啟動且所有的服務提供者都被註冊之後，`Request` 將被移轉給路由器進行分派。路由器會將請求分派給路由或控制器，並執行任何特定路由的中介層。

<a name="focus-on-service-providers"></a>
## 聚焦於服務提供者

服務提供者是啟動 Laravel 應用程式的真正關鍵。應用程式的實例被建立、服務提供者被註冊、請求被移轉至已啟動的應用程式。真的就是這麼簡單！

確實掌握 Laravel 應用程式如何建立並透過服務提供者啟動，這是很有價值的。當然，你的應用程式預設的服務提供者存放在 `app/Providers` 此一目錄下。

預設情況下，`AppServiceProvider` 幾乎是空的。要加入你應用程式自己的啟動及服務容器繫結，此提供者是一個很好的地方。當然，對大型應用程式而言，你可能希望建立若干個服務提供者，每一個都具備更精細的啟動類型。
