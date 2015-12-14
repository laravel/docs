# Blade 模板

- [簡介](#introduction)
- [模板繼承](#template-inheritance)
    - [定義頁面佈局](#defining-a-layout)
    - [繼承頁面佈局](#extending-a-layout)
- [顯示資料](#displaying-data)
- [控制結構](#control-structures)
- [服務注入](#service-injection)
- [擴充 Blade](#extending-blade)

<a name="introduction"></a>
## 簡介

Blade 是 Laravel 所提供的簡單且強大的模板引擎。相較於其它知名的 PHP 模板引擎，Blade 並不會限制你必須在視圖中使用 PHP 程式碼。所有 Blade 視圖會被編譯成一般的 PHP 程式碼並快取直到它們被更動為止，這代表著基本上 Blade 不會對你的應用程式產生負擔。Blade 視圖檔案使用 `.blade.php` 做為副檔名，且通常儲存於 `resources/views` 資料夾。

<a name="template-inheritance"></a>
## 模板繼承

<a name="defining-a-layout"></a>
### 定義頁面佈局

使用 Blade 模板的兩個主要優點為_模板繼承_與_區塊_。讓我們先看一個簡單的範例來上手。首先，我們確認一下「主要的」頁面佈局。由於大多數的網頁應用程式在不同頁面都保持著相同的佈局方式，這便於定義這個佈局為單一的 Blade 視圖：

    <!-- 檔案儲存於 resources/views/layouts/master.blade.php -->

    <html>
        <head>
            <title>應用程式名稱 - @yield('title')</title>
        </head>
        <body>
            @section('sidebar')
                這是主要的側邊欄。
            @show

            <div class="container">
                @yield('content')
            </div>
        </body>
    </html>

如你所見，這個檔案包含了傳統的 HTML 語法。不過，請注意 `@section` 與 `@yield` 指令。正如其名，`@section` 指令定義一個內容區塊，而 `@yield` 指令被用來顯示給定區塊的內容。

現在，我們已經定義了這個應用程式的佈局，讓我們來定義一個繼承此佈局的子頁面。

<a name="extending-a-layout"></a>
### 繼承頁面佈局

當正在定義子頁面時，你可以使用 Blade 的 `@extends` 指令指定子頁面應該「繼承」哪一個佈局。當視圖 `@extends` Blade 的佈局之後，即可使用 `@section` 指令將內容注入於佈局的區塊中。切記，如上述範例所見，這些區塊的內容都會使用 `@yield` 顯示在佈局中：

    <!-- 儲存於 resources/views/child.blade.php -->

    @extends('layouts.master')

    @section('title', '頁面標題')

    @section('sidebar')
        @@parent

        <p>這邊會附加在主要的側邊欄。</p>
    @endsection

    @section('content')
        <p>這是我的主要內容。</p>
    @endsection

在這個範例中，`sidebar` 區塊利用了 `@@parent` 指令增加（而不是覆蓋）內容至佈局的側邊欄。`@@parent` 指令會在視圖輸出時被置換成佈局的內容。

當然，就像一般的 PHP 視圖，可以在路由中使用全域的 `view` 輔助函式回傳 Blade 視圖：

    Route::get('blade', function () {
        return view('child');
    });

<a name="displaying-data"></a>
## 顯示資料

你可以使用「大」括號包住變數以顯示傳遞至 Blade 視圖的資料。舉例而言，就像以下的路由設定：

    Route::get('greeting', function () {
        return view('welcome', ['name' => 'Samantha']);
    });

你可以像這樣顯示 `name` 變數的內容：

    Hello, {{ $name }}.

當然，也不是一定只能顯示傳遞至視圖的變數內容。你也可以顯示 PHP 函式的結果。實際上，你可以放置任何你需要的 PHP 程式碼到 Blade 顯示語法裡面：

    目前的 UNIX 時間戳記為 {{ time() }}。

> **注意：**Blade 的 `{{ }}` 語法已經自動以 PHP 既有的 `htmlentites` 函式防禦 XSS 攻擊。

#### Blade 與 JavaScript 框架

由於許多 JavaScript 框架也使用「大」括號在瀏覽器中顯示給定的表達式，你可以使用 `@` 符號來告知 Blade 渲染引擎該表達式應該維持原樣。舉個例子：

    <h1>Laravel</h1>

    Hello, @{{ name }}.

在這個範例中，`@` 符號會被 Blade 移除。而且，Blade 引擎會保留 `{{ name }}` 表達式，如此一來便可讓其它 JavaScript 框架所應用。

#### 當資料存在時印出

有時候你想要印出一個變數，但你並不確定這個變數是否已被設定。我們可以用像這樣的冗長 PHP 程式碼表達：

    {{ isset($name) ? $name : 'Default' }}

不過，Blade 提供了較方便的縮寫來替代寫三元運算子表示式：

    {{ $name or 'Default' }}

在這個範例中，如果 `$name` 變數存在，它的值將會被顯示出來。但是，如果這個變數不存在，便會顯示 `Default`。

#### 顯示未跳脫的資料

在預設情況下，Blade 模板中的 `{{ }}` 表達式將會自動套用 PHP 的 `htmlentities` 函式，以避免 XSS 攻擊。如果你不希望你的資料被跳脫，可以使用下列的語法：

    Hello, {!! $name !!}.

> **注意：**要非常小心處理任何應用程式使用者提供的字串。請總是使用雙大括號語法來跳脫內容中的 HTML 元素。

<a name="control-structures"></a>
## 控制結構

除了模板繼承與顯示資料功能以外，Blade 也提供了方便的縮寫給一般的 PHP 控制敘述，像是條件陳述式和迴圈。這些縮寫提供了乾淨、簡潔的方式來使用 PHP 的控制結構，同時還保留對應在 PHP 中熟悉且同樣的語法。

#### If 陳述式

你可以使用 `@if`、`@elseif`、`@else` 及 `@endif` 指令建構 `if` 陳述式。這些指令的功能等同於在 PHP 中的語法：

    @if (count($records) === 1)
        我有一條記錄！
    @elseif (count($records) > 1)
        我有多條記錄！
    @else
        我沒有任何記錄！
    @endif

為了方便，Blade 也提供了 `@unless` 指令：

    @unless (Auth::check())
        你尚未登入。
    @endunless

#### 迴圈

除了條件陳述式外，Blade 也提供了簡易指令使用 PHP 支援的迴圈結構。再次提及，這每個指令函式等同於他們 PHP 中的語法：

    @for ($i = 0; $i < 10; $i++)
        目前的值為 {{ $i }}
    @endfor

    @foreach ($users as $user)
        <p>此使用者為 {{ $user->id }}</p>
    @endforeach

    @forelse ($users as $user)
        <li>{{ $user->name }}</li>
    @empty
        <p>沒有使用者</p>
    @endforelse

    @while (true)
        <p>我永遠都在跑迴圈。</p>
    @endwhile

#### 引入子視圖

Blade 的 `@include` 指令，允使你簡單地從一個已存在的視圖引入 Blade 視圖。所有在父視圖的可用變數在被引入的視圖中都是可用的。

    <div>
        @include('shared.errors')

        <form>
            <!-- 表單內容 -->
        </form>
    </div>

儘管被引入的視圖會繼承父視圖中的所有資料，你也可以傳遞額外資料的陣列至被引入的頁面：

    @include('view.name', ['some' => 'data'])

> **注意：**你必須在 Blade 視圖中避免使用 `__DIR__` 及 `__FILE__` 常數，因為他們會引用視圖被快取的位置。

#### 為集合渲染視圖

你可以使用 Blade 的 `@each` 指令將迴圈及引入結合成一行：

    @each('view.name', $jobs, 'job')

第一個參數為對陣列或集合的每個元素渲染的局部視圖。第二個參數為你要迭代的陣列或集合，而第三個參數為迭代時被分配至視圖中的變數名稱。所以，舉例來說，如果你迭代一個 `jobs` 陣列，通常你會希望在局部視圖中透過 `job` 變數存取每一個 job。

你也可以傳遞第四個參數至 `@each` 指令。此參數為當給定的陣列為空時，將會被渲染的視圖。

    @each('view.name', $jobs, 'job', 'view.empty')

#### 註解

Blade 也允許在頁面中定義註解。然而，有異於 HTML 的註解，Blade 的註解並不會被包含在應用程式回傳的 HTML 內：

    {{-- 此註解將不會出現在渲染後的 HTML --}}

<a name="service-injection"></a>
## 服務注入

`@inject` 指令可以取出 Laravel [服務容器](/docs/{{version}}/container)中的服務。傳遞給 `@inject` 的第一個參數為置放該服務的變數名稱，而第二個參數為你想要解析的服務的類別或是介面的名稱：

    @inject('metrics', 'App\Services\MetricsService')

    <div>
        每月收入：{{ $metrics->monthlyRevenue() }}。
    </div>

<a name="extending-blade"></a>
## 擴充 Blade

Blade 甚至允許你定義客製化的指令。你可以使用 `directive` 方法註冊指令。當 Blade 編譯器遇到該指令時，它將會帶參數呼叫提供的回呼函式。

以下範例建立一個把給定的 `$var` 格式化的 `@datetime($var)` 指令：

    <?php

    namespace App\Providers;

    use Blade;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 執行服務註冊後的啟動程序。
         *
         * @return void
         */
        public function boot()
        {
            Blade::directive('datetime', function($expression) {
                return "<?php echo with{$expression}->format('m/d/Y H:i'); ?>";
            });
        }

        /**
         * 在容器註冊綁定。
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

如你所見，Laravel 的 `with` 輔助函式被用在這個指令中。`with` 輔助函式會簡單地回傳給定的物件或值，並允許使用便利的方法鏈結。最後此指令產生的 PHP 會是：

    <?php echo with($var)->format('m/d/Y H:i'); ?>


