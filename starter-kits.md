# 入門套件

- [介紹](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [安裝](#laravel-breeze-installation)
    - [Breeze 和 Blade](#breeze-and-blade)
    - [Breeze 和 Livewire](#breeze-and-livewire)
    - [Breeze 和 React / Vue](#breeze-and-inertia)
    - [Breeze 和 Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 介紹

為了讓你在構建新的 Laravel 應用程式時能夠快速上手，我們很高興提供身份驗證和應用入門套件。這些套件會自動為你的應用架設所需的路由、控制器和視圖，以便註冊和驗證應用的使用者。

雖然你可以使用這些入門套件，但它們並非必需。你可以選擇從頭開始建構自己的應用，只需安裝一個全新的 Laravel 副本。無論哪種方式，我們相信你都能構建出色的作品！

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze) 是對所有 Laravel [身份驗證功能](/docs/{{version}}/authentication)的最小、簡單實作，包括登入、註冊、密碼重設、電子郵件驗證和密碼確認。此外，Breeze 還包含一個簡單的“個人資料”頁面，用戶可以在此更新他們的名字、電子郵件地址和密碼。

Laravel Breeze 的預設視圖層由簡單的 [Blade 模板](/docs/{{version}}/blade)和 [Tailwind CSS](https://tailwindcss.com) 組成。此外，Breeze 提供基於 [Livewire](https://livewire.laravel.com) 或 [Inertia](https://inertiajs.com) 的鷹架（scaffolding）選項，可以選擇使用 Vue 或 React 進行基於 Inertia 的鷹架（scaffolding）。

<img src="https://laravel.com/img/docs/breeze-register.png">

#### Laravel Bootcamp

如果你是 Laravel 新手，可以隨時參加 [Laravel Bootcamp](https://bootcamp.laravel.com)。Laravel Bootcamp 將引導你使用 Breeze 構建你的第一個 Laravel 應用程式。這是一個很好的途徑來了解 Laravel 和 Breeze 所提供的一切。

<a name="laravel-breeze-installation"></a>
### 安裝

首先，你應該[創造一個新的 Laravel 應用](/docs/{{version}}/installation)。如果你使用 [Laravel 安裝程式](/docs/{{version}}/installation#creating-a-laravel-project)創造應用，系統會提示你在安裝過程中安裝 Laravel Breeze。否則，你需要按照以下手動安裝說明進行操作。

如果你已經創造了一個沒有入門套件的新 Laravel 應用，可以使用 Composer 手動安裝 Laravel Breeze：

```shell
composer require laravel/breeze --dev
```

Composer 安裝 Laravel Breeze 包後，你應該運行 `breeze:install` Artisan 命令。此命令將身份驗證視圖、路由、控制器和其他資源發佈到你的應用中。Laravel Breeze 會將其所有程式碼發佈到你的應用中，使你能夠完全控制和了解其功能和實作。

`breeze:install` 命令會提示你選擇首選的前端stack和測試框架：

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
### Breeze 和 Blade

預設的 Breeze “stack” 是 Blade stack，它利用簡單的 [Blade 模板](/docs/{{version}}/blade)來渲染你的應用前端。可以在不加任何附加參數的情況下調用 `breeze:install` 命令並選擇 Blade 前端stack來安裝 Blade stack。Breeze 的鷹架（scaffolding）安裝完畢後，你應該編譯應用的前端資源：

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

接下來，你可以在網頁瀏覽器中導航到應用的 `/login` 或 `/register` URLs。Breeze 的所有路由都定義在 `routes/auth.php` 文件中。

> [!NOTE]  
> 欲了解更多關於編譯應用的 CSS 和 JavaScript 的內容，請參閱 Laravel 的 [Vite 文件](/docs/{{version}}/vite#running-vite)。

<a name="breeze-and-livewire"></a>
### Breeze 和 Livewire

Laravel Breeze 也提供 [Livewire](https://livewire.laravel.com) 的鷹架（scaffolding）。Livewire 是一種強大的僅使用 PHP 來打造動態、反應式的前端 UI，。

Livewire 非常適合主要使用 Blade 模板且希望尋求 JavaScript 驅動的 SPA 框架（如 Vue 和 React）替代方案的團隊。

要使用 Livewire stack，你可以在執行 `breeze:install` Artisan 命令時選擇 Livewire 前端stack。Breeze 的鷹架（scaffolding）安裝完畢後，應該運行資料庫遷移：

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
### Breeze 和 React / Vue

Laravel Breeze 還提供通過 [Inertia](https://inertiajs.com) 前端實作的 React 和 Vue 鷹架（scaffolding）。Inertia 允許你使用傳統的服務器端路由和控制器構建現代化的單頁 React 和 Vue 應用。

Inertia 讓你可以享受 React 和 Vue 的前端功能，結合 Laravel 的出色後端生產力和快速的 [Vite](https://vitejs.dev) 編譯。要使用 Inertia stack，你可以在執行 `breeze:install` Artisan 命令時選擇 Vue 或 React 前端stack。

選擇 Vue 或 React 前端stack時，Breeze 安裝程式還會提示你是否需要 [Inertia SSR](https://inertiajs.com/server-side-rendering) 或 TypeScript 支持。Breeze 的鷹架（scaffolding）安裝完畢後，應該也編譯應用的前端資源：

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

接下來，你可以在網頁瀏覽器中導航到應用的 `/login` 或 `/register` URL。Breeze 的所有路由都定義在 `routes/auth.php` 文件中。

<a name="breeze-and-next"></a>
### Breeze 和 Next.js / API

Laravel Breeze 還可以構建一個身份驗證 API，準備好用於現代 JavaScript 應用，如 [Next](https://nextjs.org)、[Nuxt](https://nuxt.com) 和其他應用。要開始，請在執行 `breeze:install` Artisan 命令時選擇 API stack作為所需的stack：

```shell
php artisan breeze:install

php artisan migrate
```

安裝過程中，Breeze 會在應用的 `.env` 文件中添加一個 `FRONTEND_URL` 環境變量。此 URL 應為 JavaScript 應用的 URL。通常在本地開發期間，這將是 `http://localhost:3000`。此外，還應確保 `APP_URL` 設置為 `http://localhost:8000`，這是 `serve` Artisan 命令使用的預設 URL。

<a name="next-reference-implementation"></a>
#### Next.js 參考實作

最後，你準備好將此後端與所選的前端配對。Breeze 前端的 Next 參考實作在 [available on GitHub](https://github.com/laravel/breeze-next)。此前端由 Laravel 維護，並包含與 Breeze 提供的傳統 Blade 和 Inertia stack相同的用戶介面。

<a name="laravel-jetstream"></a>
## Laravel Jetstream

雖然 Laravel Breeze 提供了一個簡單和最小的起點來構建 Laravel 應用，但 Jetstream 透過更強大的功能和更多的前端技術stack來增強這些功能。**對於那些完全新手的 Laravel 開發者，我們建議先學習 Laravel Breeze，然後再進階到 Laravel Jetstream。**

Jetstream 為 Laravel 提供了精美設計的應用鷹架（scaffolding），包括登入、註冊、電子郵件驗證、雙重身份驗證、會話管理、通過 Laravel Sanctum 支持 API 和可選的

團隊管理。Jetstream 使用 [Tailwind CSS](https://tailwindcss.com) 設計，並提供 [Livewire](https://livewire.laravel.com) 或 [Inertia](https://inertiajs.com) 驅動的前端鷹架（scaffolding）選擇。

安裝 Laravel Jetstream 的完整文件可在 [官方 Jetstream 文件](https://jetstream.laravel.com) 中找到。
