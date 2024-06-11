# 前端

- [介紹](#introduction)
- [使用 PHP](#using-php)
    - [PHP 和 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [入門套件](#php-starter-kits)
- [使用 Vue / React](#using-vue-react)
    - [Inertia](#inertia)
    - [入門套件](#inertia-starter-kits)
- [打包資源](#bundling-assets)

<a name="introduction"></a>
## 介紹

Laravel 是一個後端框架，提供了構建現代 Web 應用所需的所有功能，如[routing](/docs/{{version}}/routing)、[validation](/docs/{{version}}/validation)、[caching](/docs/{{version}}/cache)、[queues](/docs/{{version}}/queues)、[file storage](/docs/{{version}}/filesystem) 等。然而，我們認為為開發者提供一個美好的全端體驗非常重要，包括構建應用前端的強大方法。

在使用 Laravel 構建應用時，有兩種主要方式來處理前端開發，而選擇哪種方式取決於你是希望通過使用 PHP 還是使用 JavaScript 框架（如 Vue 和 React）來構建前端。我們將在下面討論這兩種選項，以便你可以做出關於應用前端開發最佳方法的明智決定。

<a name="using-php"></a>
## 使用 PHP

<a name="php-and-blade"></a>
### PHP 和 Blade

過去，大多數 PHP 應用使用簡單的 HTML 模板與 PHP `echo` 語句混合在一起來渲染 HTML 到瀏覽器，這些語句會在請求期間從資料庫檢索數據並渲染：

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

在 Laravel 中，可以使用[視圖](/docs/{{version}}/views)和[Blade](/docs/{{version}}/blade)來實現這種渲染 HTML 的方法。Blade 是一種非常輕量級的模板語言，提供了方便、簡短的語法來顯示數據、迭代數據等：

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

以這種方式構建應用時，表單提交和其他頁面互動通常會從服務器接收一個全新的 HTML 文檔，並由瀏覽器重新渲染整個頁面。即使在今天，許多應用可能仍然非常適合使用簡單的 Blade 模板構建其前端。

<a name="growing-expectations"></a>
#### 期望的增長

然而，隨著用戶對 Web 應用期望的提高，許多開發者發現需要構建更具動態性和精緻感的前端。鑑於此，一些開發者選擇開始使用 JavaScript 框架（如 Vue 和 React）構建應用的前端。

其他人則更願意堅持使用他們熟悉的後端語言，並開發出一些解決方案，允許在主要使用後端語言的情況下構建現代 Web 應用 UI。例如，在[Rails](https://rubyonrails.org/)生態系統中，這促使了像[Turbo](https://turbo.hotwired.dev/)、[Hotwire](https://hotwired.dev/)和[Stimulus](https://stimulus.hotwired.dev/)這樣的函式庫的創建。

在 Laravel 生態系統中，主要使用 PHP 創建現代動態前端的需求導致了[Laravel Livewire](https://livewire.laravel.com)和[Alpine.js](https://alpinejs.dev/)的創建。

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com) 是一個構建 Laravel 驅動的前端框架，使其看起來動態、現代和充滿活力，就像使用現代 JavaScript 框架（如 Vue 和 React）構建的前端一樣。

使用 Livewire 時，你將創建 Livewire "元件"，這些元件渲染 UI 的一個獨立部分，並expose方法和數據，可以從應用的前端調用和互動。例如，一個簡單的"計數器"元件可能如下所示：

```php
<?php

namespace App\Http\Livewire;

use Livewire\Component;

class Counter extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
```

計數器的對應模板會這樣編寫：

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

如你所見，Livewire 允許你編寫新的 HTML 屬性，如 `wire:click`，這些屬性將 Laravel 應用的前端和後端連接起來。此外，你可以使用簡單的 Blade 表達式渲染元件的當前狀態。

對於許多人來說，Livewire 徹底改變了使用 Laravel 進行前端開發的方式，使他們能夠在熟悉的 Laravel 環境中構建現代動態 Web 應用。通常，使用 Livewire 的開發者還會利用[Alpine.js](https://alpinejs.dev/)來在前端"撒一些" JavaScript，只在需要的地方使用，例如用於渲染對話框。

如果你是 Laravel 新手，我們建議先熟悉[視圖](/docs/{{version}}/views)和[Blade](/docs/{{version}}/blade)的基本用法。然後，查閱官方的[Laravel Livewire 文檔](https://livewire.laravel.com/docs)，學習如何通過互動的 Livewire 元件將應用提升到新的水平。

<a name="php-starter-kits"></a>
### 入門套件

如果你希望使用 PHP 和 Livewire 構建前端，可以利用我們的 Breeze 或 Jetstream[入門套件](/docs/{{version}}/starter-kits)來快速啟動應用的開發。這兩個入門套件都會使用[Blade](/docs/{{version}}/blade)和[Tailwind](https://tailwindcss.com)搭建應用的後端和前端認證流程，使你能夠立即開始構建你的下個大創意。

<a name="using-vue-react"></a>
## 使用 Vue / React

雖然可以使用 Laravel 和 Livewire 構建現代前端，但許多開發者仍然更喜歡利用 JavaScript 框架（如 Vue 或 React）的強大功能。這使得開發者能夠利用 NPM 上豐富的 JavaScript packages和工具生態系統。

然而，如果沒有額外的工具，將 Laravel 與 Vue 或 React 配對將使我們需要解決各種複雜的問題，如客戶端路由、數據加載和認證。客戶端路由通常可以通過使用意見明確的 Vue / React 框架（如[Nuxt](https://nuxt.com/)和[Next](https://nextjs.org/)）來簡化；然而，當將後端框架如 Laravel 與這些前端框架配對時，數據加載和認證仍然是複雜而繁瑣的問題。

此外，開發者需要維護兩個單獨的程式庫，通常需要協調維護、發布和部署這兩個程式庫。雖然這些問題不是不可克服的，但我們不認為這是一種高效或愉快的開發方式。

<a name="inertia"></a>
### Inertia

幸運的是，Laravel 提供了兩全其美的解決方案。[Inertia](https://inertiajs.com) 在 Laravel 應用和現代 Vue 或 React 前端之間架起了一座橋樑，允許你在使用 Vue 或 React 構建完整的現代前端的同時，利用 Laravel 路由和控制器進行路由、數據加載和認證——所有這些都在一個程式庫中。通過這種方式，你可以享受 Laravel 和 Vue / React 的全部功能，而不會削弱任何一個工具的能力。

將 Inertia 安裝到 Laravel 應用後，你將像平常一樣編寫路由和控制器。然而，你將不會從控制器返回 Blade 模板，而是

返回 Inertia 頁面：

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

class UserController extends Controller
{
    /**
     * 顯示給定用戶的個人資料。
     */
    public function show(string $id): Response
    {
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 頁面對應於一個 Vue 或 React 元件，通常存儲在應用的 `resources/js/Pages` 目錄中。通過 `Inertia::render` 方法傳遞給頁面的數據將用於加載頁面元件的"props"：

```vue
<script setup>
import Layout from '@/Layouts/Authenticated.vue';
import { Head } from '@inertiajs/vue3';

const props = defineProps(['user']);
</script>

<template>
    <Head title="User Profile" />

    <Layout>
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Profile
            </h2>
        </template>

        <div class="py-12">
            Hello, {{ user.name }}
        </div>
    </Layout>
</template>
```

如你所見，Inertia 允許你在構建前端時充分利用 Vue 或 React 的功能，同時在 Laravel 驅動的後端和 JavaScript 驅動的前端之間提供了一個輕量級的橋樑。

#### 服務器端渲染

如果你擔心使用 Inertia 因為你的應用需要服務器端渲染，別擔心。Inertia 提供[服務器端渲染支持](https://inertiajs.com/server-side-rendering)。而且，當通過[Laravel Forge](https://forge.laravel.com)部署應用時，確保 Inertia 的服務器端渲染過程總是輕而易舉地運行。

<a name="inertia-starter-kits"></a>
### 入門套件

如果你希望使用 Inertia 和 Vue / React 構建前端，可以利用我們的 Breeze 或 Jetstream [入門套件](/docs/{{version}}/starter-kits#breeze-and-inertia)來快速啟動應用的開發。這兩個入門套件都會使用 Inertia、Vue / React、[Tailwind](https://tailwindcss.com) 和 [Vite](https://vitejs.dev) 搭建應用的後端和前端認證流程，使你能夠開始構建你的下個大創意。

<a name="bundling-assets"></a>
## 打包資源

無論你選擇使用 Blade 和 Livewire 還是 Vue / React 和 Inertia 開發前端，你可能都需要將應用的 CSS 打包成正式環境就緒的資源。當然，如果你選擇用 Vue 或 React 構建應用的前端，你還需要將元件打包成瀏覽器就緒的 JavaScript 資源。

預設情況下，Laravel 使用 [Vite](https://vitejs.dev) 打包你的資源。Vite 提供閃電般快速的構建時間和本地開發期間近乎即時的熱模組替換（HMR）。在所有新的 Laravel 應用中，包括使用我們的[入門套件](/docs/{{version}}/starter-kits)的應用，你會發現一個 `vite.config.js` 文件，其中加載了我們的輕量級 Laravel Vite 插件，使 Vite 與 Laravel 應用的使用變得愉快。

快速開始使用 Laravel 和 Vite 的最快方式是使用 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze)開始你的應用開發，我們最簡單的入門套件，通過提供前端和後端認證腳手架來快速啟動你的應用。

> [!NOTE]  
> 欲了解更多關於在 Laravel 中使用 Vite 的詳細文檔，請參見我們[專門的資源打包和編譯文檔](/docs/{{version}}/vite)。