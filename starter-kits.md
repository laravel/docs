# 入門套件

- [前言](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [安裝](#laravel-breeze-installation)
    - [Breeze 和 Blade](#breeze-and-blade)
    - [Breeze 和 React / Vue](#breeze-and-inertia)
    - [Breeze 和 Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 前言

為了讓你快速開始建立新的 Laravel 應用程式，我們很高興提供認證（authentication）和應用程式的入門套件。這些套件會自動為應用程式提供註冊和認證使用者的路由（route）、控制器（controller）、視圖（view）的基本架構。

雖然很歡迎你使用這些入門套件，但他們並非必須的。你可以自由建立自己的應用程式，只需要安裝一個乾淨的 Laravel 副本。無論哪種方式，我們知道你會創造出好東西！

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze) 可以迷你、簡單地實現所有 Laravel [認證功能](/docs/{{version}}/authentication)，包含登入（login）、註冊（registration）、密碼重置（password reset）、電子信箱驗證（verifiction）和密碼確認（password confirmation）。Laravel Breeze 的預設視圖層由簡單的 [Blade 模板](/docs/{{version}}/blade) 搭配 [Tailwind CSS](https://tailwindcss.com) 樣式所組成。或者，Breeze 可以成為應用程式使用 Vue / React 和 [Inertia](https://inertiajs.com) 時的基架。

Breeze 提供了一個精彩的起點去開始全新的 Laravel 應用程式，對於想用上 [Laravel Livewire](https://laravel-livewire.com) 將 Blade 模板專案提升到新水平的專案而言，它也是個好選擇。

<img src="https://laravel.com/img/docs/breeze-register.png">

#### Laravel Bootcamp

如果你是 Laravel 新手，可以加入 [Laravel Bootcamp](https://bootcamp.laravel.com)。它可以引導你使用 Breeze 建立你的一個 Laravel 應用程式。這是個體驗 Laravel 和 Breeze 一切的好方法。

<a name="laravel-breeze-installation"></a>
### 安裝

首先，你需要 [建立一個新的 Laravel 應用程式](/docs/{{version}}/installation)，設定你的資料庫，且執行 [資料庫遷移（database migration）](/docs/{{version}}/migrations)。一旦你建立一個新的 Laravel 應用程式，你可以使用 Composer 安裝 Laravel Breeze：

```shell
composer require laravel/breeze --dev
```

一旦 Breeze 被安裝，你可以使用以下文件討論的 Breeze「堆疊（stack）」來建構應用程式。

<a name="breeze-and-blade"></a>
### Breeze 和 Blade

用 Composer 安裝 Laravel Breeze 套件後，你可以執行 Artisan 指令 `breeze:install`。該指令會將認證視圖、路由、控制器和其他資源發布至應用程式。Laravel Breeze 發布所有的程式碼到應用程式，以便你可以完全控制和看見其功能和實作。

預設的 Breeze「堆疊」是使用了簡易 [Blade 模板](/docs/{{version}}/blade) 渲染應用程式端的Blade「堆疊」。Blade 堆疊可以調用 `breeze:install` 指令安裝且毋須附加參數。當 Breeze 的基本架構安裝後，你還可以編譯應用程式前端的資源檔：

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

接下來，你可以將 web 瀏覽器 URL 導航至應用程式的 `/login` 或 `/register`。所有的 Breeze 路由皆定義在 `routes/auth.php` 檔中。

> **Note**  
> 想了解更多關於應用程式 CSS 和 JavaScript 的編譯，可以參考 Laravel 的 [Vite 文件](/docs/{{version}}/vite#running-vite)。

<a name="breeze-and-inertia"></a>
### Breeze & React / Vue

Laravel Breeze 也透過 [Inertia](https://inertiajs.com) 的前端實作提供 React 和 Vue 的基架。Inertia 允許你使用經典的伺服器端路由（server-side routing）和控制器建立現代且一頁式的 React 和 Vue 應用程式。

Inertia 讓你享受 React 和 Vue 前端功能結合生產力極佳的 Laravel 後端和快如閃電的 [Vite](https://vitejs.dev) 編譯。要使用 Inertia 堆疊，請在執行 Artisan 指令 `breeze:install` 時指定 `vue` 或 `react` 為所需的堆疊。Breeze 的基架安裝後，你也可以編譯應用程式前端的資源檔：

```shell
php artisan breeze:install vue

# Or...

php artisan breeze:install react

php artisan migrate
npm install
npm run dev
```

接下來，你可以將 web 瀏覽器 URL 導航至應用程式的 `/login` 或 `/register`。所有的 Breeze 路由皆定義在 `routes/auth.php` 檔中。

<a name="server-side-rendering"></a>
#### 伺服器端渲染

如果你希望 Breeze 為 [Inertia SSR](https://inertiajs.com/server-side-rendering) 提供基架支援，可以在指令 `breeze:install` 後面加上 `ssr` 選項：

```shell
php artisan breeze:install vue --ssr
php artisan breeze:install react --ssr
```

<a name="breeze-and-next"></a>
### Breeze & Next.js / API

Laravel Breeze 還可以建構一個驗證現代 JavaScript 應用程式的驗證 API，例如 [Next](https://nextjs.org) 和 [Nuxt](https://nuxtjs.org) 等。首先，在執行 Artisan 指令 `breeze:install` 時將 `api` 堆疊指定為所需的堆疊：

```shell
php artisan breeze:install api

php artisan migrate
```

在安裝過程中，Breeze 在應用程式的 `.env` 檔內新增一個環境變數 `FRONTEND_URL`。該 URL 必須是 JavaScript 應用程式的 URL。在本地開發時通常會是 `http://localhost:3000`。此外，你應該確保 `APP_URL` 的設定是 `http://localhost:8000`，這是 Artisan 指令 `serve` 預設的 URL。

<a name="next-reference-implementation"></a>
#### Next.js 實作參考

最後，你已經準備好將此後端與你選擇的前端做搭配。Breeze 前端的 Next 實作參考 [可以在 GitHub 上找到](https://github.com/laravel/breeze-next)。該前端由 Laravel 維護，且包含了和 Breeze 提供的傳統 Blade 和 Inertia 堆疊相同的使用者介面。

<a name="laravel-jetstream"></a>
## Laravel Jetstream

雖然 Laravel Breeze 為建立 Laravel 應用程式提供簡單且微小的起點，但 Jetstream 透過更強大的功能和額外的前端技術堆疊來增強該功能。**對於 Laravel 的新手，我們建議學會 Laravel Jetstream 前先學習 Laravel Breeze 該怎麼使用。**

Jetstream 為 Laravel 提供了設計精美的應用程式基架，包含登入（login）、註冊（registration）、電子信箱驗證（email verification）、雙重認證（two-factor authentication）、session 管理，透過 Laravel Sanctum 的 API 支援和可自選的團隊管理。Jetstream 使用 [Tailwind CSS](https://tailwindcss.com) 設計也提供你選擇由 [Livewire](https://laravel-livewire.com) 或 [Inertia](https://inertiajs.com) 驅動的前端基架。

安裝 Laravel Jetstream 的完整文件可以在 [官方 Jetstream 文件](https://jetstream.laravel.com/2.x/introduction.html) 中找到。
