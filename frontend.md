# 前端

- [前言](#introduction)
- [使用 PHP](#using-php)
    - [PHP 和 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [入門套件](#php-starter-kits)
- [使用 Vue / React](#using-vue-react)
    - [Inertia](#inertia)
    - [入門套件](#inertia-starter-kits)
- [綁定資源](#bundling-assets)

<a name="introduction"></a>
## 前言

Laravel 是一款提供建立現代 web 應用程式全部特徵的後端框架，像是 [路由（route）](/docs/{{version}}/routing)、[驗證（validation）](/docs/{{version}}/validation)、[快取（cache）](/docs/{{version}}/cache)、[佇列（queue）](/docs/{{version}}/queues)、[檔案儲存（file storage）](/docs/{{version}}/filesystem)等。然而，我們相信提供給開發者一個美麗的全端經驗很重要，包含建立應用程式前端的強力方法。

使用 Laravel 建立應用程式時，有兩個主要方式可以解決前端開發問題，取決於你決定使用 PHP 或 JavaScript 框架例如 Vue / React 去建立你的前端。我們將在下面討論這兩種選項，方便讓你可以在開發應用程式前端的最佳方法中做出明智的決定。

<a name="using-php"></a>
## 使用 PHP

<a name="php-and-blade"></a>
### PHP 和 Blade

以前，大多數的 PHP 應用程式用簡單的 HTML 模板穿插 PHP 的 `echo` 語法向瀏覽器渲染 HTML，這些呈現的資料是在請求期間從資料庫檢索而來的。

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

在 Laravel，這種渲染 HTML 的類似方法仍然可以使用 [視圖（view）](/docs/{{version}}/views) 和 [Blade](/docs/{{version}}/blade) 實現。Blade 是一種輕量的模板語言，他對顯示資料、迭代資料（iterate over data）等提供了方便且簡短的語法。

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

以這種方式建立應用程式時，表單提交（form submission）和其他互動頁面通常會從伺服器檢索成一整個新的 HTML 文件，且這個頁面會被瀏覽器預先渲染。即使到了現今，許多應用程式也可能非常適合使用單純的 Blade 模板建構其前端。

<a name="growing-expectations"></a>
#### 後續期望

然而，隨著使用者對 web 應用程式的期望趨近成熟，許多開發者發現需要建立更加動態且更多優雅互動的前端。有鑑於此，一些開發者開始選擇使用 JavaScript 框架如 Vue / React 來建立他們的應用程式前端。

而其他人更喜歡堅持使用他們所熟悉的後端語言並開始開發解決方案，允許建構現代 web 應用程式 UI 的同時仍能使用他們選擇的後端語言。例如，在 [Rails](https://rubyonrails.org/) 生態系統中，也帶動了 [Turbo](https://turbo.hotwired.dev/)、[Hotwire](https://hotwired.dev/)、[Stimulus](https://stimulus.hotwired.dev/) 等函式庫的出現。

在 Laravel 的生態系統中，主要使用 PHP 建立現代、動態前端的需求催生出了 [Laravel Livewire](https://laravel-livewire.com) 和 [Alpine.js](https://alpinejs.dev/)。

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://laravel-livewire.com) 是一款由 Laravel 運作前端的框架，就像使用 Vue / React 的 JavaScript 現代框架一樣，都能建立出動態、現代和生動的前端。

使用 Livewire 時，將會各自建立渲染局部 UI 的 Livewire「元件（component）」並公開方法與資料供應用程式前端調用和進行互動。例如，一個簡單的「計數器」元件可能如下所示：

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

然後，與計數器對應的模板可以這樣子寫：

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

如你所見，Livewire 讓你能加入新的 HTML 屬性，像是 `wire:click` 能連接 Laravel 應用程式的前後端。此外，你可以使用簡易的 Blade 表達式呈現元件目前的狀態。

對許多人來說，Livewire 已經使 Laravel 的前端開發徹底改觀，使他們能夠建立現代且動態的 web 應用程式時同時保持 Laravel 的舒適。通常開發者使用 Livewire 時也會用 [Alpine.js](https://alpinejs.dev/) 只將需要的 JavaScript 部分「灑」到前端，例如為了渲染一個對話視窗。

如果你是 Laravel 新手，我們建議熟悉 [視圖（view）](/docs/{{version}}/views) 和 [Blade](/docs/{{version}}/blade) 的基本用法。然後參考官方的 [Laravel Livewire 文件](https://laravel-livewire.com/docs) 去了解如何利用互動式 Livewire 元件（component）將應用程式提升到新的水平。

<a name="php-starter-kits"></a>
### 入門套件

如果你想使用 PHP 和 Livewire 建立前端，你可以斟酌我們的 Breeze 或 Jetstream [入門套件](/docs/{{version}}/starter-kits) 快速啟動應用程式的開發。這兩個入門套件都使用了 [Blade](/docs/{{version}}/blade) 和 [Tailwind](https://tailwindcss.com) 構建應用程式的後端和前端驗證（authentication）流程，以便你可以輕鬆地開始建造下一個新創想法。

<a name="using-vue-react"></a>
## 使用 Vue / React

儘管可以使用 Laravel 和 Livewire 建立現代化的前端，許多開發者仍然更喜歡用像是 Vue / React 的強大 JavaScript 框架。因為它允許開發者透過 NPM 豐富的生態系統去使用 JavaScript 套件和工具。

然而，沒有額外的工具輔助，將 Laravel 和 Vue / React 搭配會令我們需要解決不少複雜的問題，例如 客戶端路由（client-side routing）、資料混合（data hydration）和認證（authentication）。客戶端路由的簡化通常會使用 Vue / React 框架自身的 [Nuxt](https://nuxtjs.org/) 和 [Next](https://nextjs.org/)；然而，將 Laravel 這種後端框架與這些前端框架做搭配，還是會留下資料混合和認證這些待解決的複雜問題。

此外，開發者需要維護兩個獨立的程式碼資料倉儲（code repository），通常需要跨兩個資料倉儲做協調維護、發布和部署。儘管這些問題不是不能克服，但我們認為這不是個有效率且愉快的應用程式開發方式。

<a name="inertia"></a>
### Inertia

值得慶幸的是，Laravel 提供了兩全其美的功能。[Inertia](https://inertiajs.com) 在 Laravel 與 Vue / React 的現代前端之間搭起一座橋梁，允許你用 Vue / React 建立成熟且現代化的前端，同時採用 Laravel 路由和控制器（controller）進行路由、資料混合和認證——全部都在一個程式碼資料倉儲內。透過這個方法，你可以在不削弱任何工具的情況下，同時享受 Laravel 和 Vue / React 的全部功能。

將 Inertia 安裝進 Laravel 應用程式後，你將會像平常一樣編寫路由和控制器。然而，它並不是從控制器回傳 Blade 模板，而是回傳給你一個 Inertia 頁面：

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Inertia\Inertia;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     *
     * @param  int  $id
     * @return \Inertia\Response
     */
    public function show($id)
    {
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 頁面對應到 Vue / React 元件（component），通常會存在應用程式的 `resources/js/Pages` 目錄內。傳給頁面的資料透過方法（method） `Inertia::render` 成為混合頁面元件的「支柱」：

```vue
<script setup>
import Layout from '@/Layouts/Authenticated.vue';
import { Head } from '@inertiajs/inertia-vue3';

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

如你所見，Inertia 允許你在建立前端時使用 Vue / React 的全部功能，同時在 Laravel 驅使的後端和 JavaScript 驅使的前端之間搭起一座輕量的橋樑。

#### 伺服器端渲染

如果你因為應用程式需要伺服器端渲染（server-side rendering）而擔心是否能深入了解 Inertia。免煩惱，Inertia 提供 [伺服器端渲染支援](https://inertiajs.com/server-side-rendering)。而且，當透過 [Laravel Forge](https://forge.laravel.com) 部署應用程式時，Inertia 的伺服器端渲染處理保證是一直輕而易舉地執行中。

<a name="inertia-starter-kits"></a>
### 入門套件

如果你想使用 Inertia 和 Vue 或 React 建立前端，你可以用我們的 Breeze 或 Jetstream [starter kits](/docs/{{version}}/starter-kits#breeze-and-inertia) 來快速啟動應用程式的開發。這些入門套件都會使用 Inertia、Vue / React、 [Tailwind](https://tailwindcss.com)和 [Vite](https://vitejs.dev) 構建應用程式後端和前端認證流程，以便你可以輕鬆地開始建造下一個新創想法。

<a name="bundling-assets"></a>
## 綁定資源

無論你選擇使用 Blade 和 Livewire 或 Vue / React 和  Inertia 開發前端，你可能需要綁定應用程式的 CSS 到產品的預備資源（asset）內。當然，如果你選擇使用 Vue 或 React 建立應用程式的前端，你也會需要綁定你的元件到瀏覽器預備的 JavaScript 資源。

預設情況下，Laravel 使用 [Vite](https://vitejs.dev) 去綁定你的資源。Vite 在本地端開發時提供了快如閃電的建立時間和瞬間的熱模型轉換（Hot Module Replacement, HMR）。在所有新的 Laravel 應用程式含我們使用的 [入門套件](/docs/{{version}}/starter-kits) 中，你會發現我們輕量的 Laravel Vite 外掛中載入了 `vite.config.js` 檔，使其在 Laravel 中使用 Vite 成為樂趣。

起手 Laravel 和 Vite 最快的方法是用上 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) 開始開發應用程式，這是簡易的入門套件，供你快速開始建置提供前端和後端認證結構的應用程式。

> **Note**  
> 關於更多在 Laravel 中使用 Vite 的詳細文件，請參閱我們的 [綁定和編譯資源的專用文件](/docs/{{version}}/vite)。
