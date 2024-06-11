# Request Lifecycle

- [介紹](#introduction)
- [生命周期概述](#lifecycle-overview)
    - [第一步](#first-steps)
    - [HTTP / Console 核心](#http-console-kernels)
    - [服務提供者](#service-providers)
    - [路由](#routing)
    - [完成](#finishing-up)
- [專注於服務提供者](#focus-on-service-providers)

<a name="introduction"></a>
## 介紹

在使用任何“真實世界”的工具時，如果了解該工具的工作原理，你會感到更加自信。應用程式開發也不例外。當你了解開發工具的功能時，使用它們會感到更舒適和自信。

本文件的目標是為你提供一個關於 Laravel 框架工作方式的高級概述。通過更好地了解整體框架，一切都會顯得不那麼“神奇”，你也會更有信心地建構應用程式。如果你不能立即理解所有術語，不要氣餒！只需嘗試基本掌握發生了什麼，隨著你探索文件的其他部分，你的知識會逐漸增長。

<a name="lifecycle-overview"></a>
## 生命週期概述

<a name="first-steps"></a>
### 第一步

所有請求進入 Laravel 應用程式的入口點是 `public/index.php` 文件。所有請求都是由你的 Web 伺服器（Apache / Nginx）配置指向這個文件的。`index.php` 文件本身程式碼不多。它是載入框架其他部分的起點。

`index.php` 文件載入 Composer 生成的自動載入器（autoloader）定義，然後從 `bootstrap/app.php` 獲取 Laravel 應用程式實例。Laravel 本身採取的第一個動作是建立應用程式實例 / [服務容器](/docs/{{version}}/container)。

<a name="http-console-kernels"></a>
### HTTP / Console 核心

接下來，根據進入應用程式的請求類型，將傳入的請求發送到 HTTP 核心或控制台核心，使用應用程式實例的 `handleRequest` 或 `handleCommand` 方法。這兩個核心是所有請求流經的中心位置。目前，讓我們先專注在 HTTP 核心，它是 `Illuminate\Foundation\Http\Kernel` 的實例。

HTTP 核心定義了一個 `bootstrappers` 陣列，在請求執行前會運行這些陣列。這些 bootstrappers 配置錯誤處理、配置記錄（logging）、[檢測應用程式環境](/docs/{{version}}/configuration#environment-configuration)，以及執行其他在實際處理請求之前需要完成的任務。通常，這些類別處理內部的 Laravel 配置，你不需要擔心。

HTTP 核心還負責將請求傳遞給應用程式的中介層堆疊。這些中介層處理讀取和寫入 [HTTP session](/docs/{{version}}/session)、確定應用程式是否處於維護模式、[驗證 CSRF 標記](/docs/{{version}}/csrf)等。我們很快會詳細討論這些。

HTTP 核心的 `handle` 方法的方法簽名非常簡單：它接收一個 `Request` 並返回一個 `Response`。可以把核心看作是代表整個應用程式的一個大黑盒子。向它提供 HTTP 請求，它會返回 HTTP 回應。

<a name="service-providers"></a>
### 服務提供者

最重要的核心引導（bootstrapping）動作之一是載入應用程式的 [服務提供者](/docs/{{version}}/providers)。服務提供者負責引導框架的所有元件，如資料庫、佇列、確認和路由元件。

Laravel 將遍歷這個提供者列表並實例化每一個。實例化提供者後，將呼叫所有提供者的 `register` 方法。然後，當所有提供者都註冊完畢後，將呼叫每個提供者的 `boot` 方法。這樣服務提供者就可以依賴於每個被註冊的容器綁定，且在 `boot` 方法被執行時即可使用。

Laravel 提供的幾乎所有主要功能都是由服務提供者引導和配置的。由於它們引導和配置了框架提供的許多功能，服務提供者是整個 Laravel 引導過程中最重要的部分。

雖然框架內部使用了數十個服務提供者，但你也可以選擇建立自己的服務提供者。你可以在 `bootstrap/providers.php` 文件中找到應用程式使用的用戶定義或第三方服務提供者列表。

<a name="routing"></a>
### 路由

一旦應用程式已被引導且所有服務提供者已註冊，`Request` 將被交給路由器進行分派。路由器將請求分派到路由或控制器，以及運行任何特定路由的中介層。

中介層提供了一種方便的機制來過濾或檢查進入應用程式的 HTTP 請求。例如，Laravel 包含一個中介層來驗證應用程式的用戶是否已經認證。如果用戶未經認證，中介層將重新導向用戶到登錄頁面。然而，如果用戶已經認證，中介層將允許請求進一步進入應用程式。一些中介層被分配給應用程式中的所有路由，例如 `PreventRequestsDuringMaintenance`，而有些則只分配給特定的路由或路由群組。你可以通過閱讀完整的 [中介層文件](/docs/{{version}}/middleware)來了解更多關於中介層的內容。

如果請求通過了所有符合路由分配的中介層，則將執行路由或控制器方法，並且路由或控制器方法返回的回應將通過路由的中介層鏈發送回去。

<a name="finishing-up"></a>
### 完成

一旦路由或控制器方法返回回應，回應將返回通過路由的中介層，給應用程式機會修改或檢查傳出的回應。

最後，當回應返回通過中介層時，HTTP 核心的 `handle` 方法將回應對象返回給應用程式實例的 `handleRequest`，此方法呼叫返回回應的 `send` 方法。`send` 方法將回應內容發送到用戶的網頁瀏覽器。我們已經完成了整個 Laravel 請求生命周期的旅程！

<a name="focus-on-service-providers"></a>
## 專注於服務提供者

服務提供者是真正啟動 Laravel 應用程式的關鍵。建立應用程式實例，註冊服務提供者，然後將請求交給引導（bootstrapping）的應用程式。真的是這麼簡單！

牢牢掌握通過服務提供者建構和引導 Laravel 應用程式的方式非常有價值。應用程式的用戶定義服務提供者儲存在 `app/Providers` 目錄中。

預設情況下，`AppServiceProvider` 是相當空的。這個提供者是一個很好的地方來添加應用程式自己的引導（bootstrapping）和服務容器綁定。對於大型應用程式，你可能希望建立多個服務提供者，每個提供者對應於應用程式使用的特定服務進行更細化的引導（bootstrapping）。
