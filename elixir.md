# Laravel Elixir

- [簡介](#introduction)
- [安裝與設置](#installation)
- [執行 Elixir](#running-elixir)
- [使用樣式](#working-with-stylesheets)
    - [Less](#less)
    - [Sass](#sass)
    - [純 CSS](#plain-css)
    - [Source Maps](#css-source-maps)
- [使用腳本](#working-with-scripts)
    - [CoffeeScript](#coffeescript)
    - [Browserify](#browserify)
    - [Babel](#babel)
    - [Scripts](#javascript)
- [複製檔案與目錄](#copying-files-and-directories)
- [版本與暫存清除](#versioning-and-cache-busting)
- [BrowserSync](#browser-sync)
- [呼叫既有的 Gulp 任務](#calling-existing-gulp-tasks)
- [撰寫 Elixir 擴充功能](#writing-elixir-extensions)

<a name="introduction"></a>
## 簡介

Laravel Elixir 提供了簡潔流暢的 API，讓你能夠為你的 Laravel 應用程式定義基本的 [Gulp](http://gulpjs.com) 任務。Elixir 支援許多常見的 CSS 與 JavaScrtip 預處理器，甚至包含了測試工具。使用方法鏈結，Elixir 讓你你流暢的定義你的資源檔管線，例如：

```javascript
elixir(function(mix) {
    mix.sass('app.scss')
       .coffee('app.coffee');
});
```

如果你曾經對於上手 Gulp 及編譯資源檔感到困惑，那麼你將會愛上 Laravel Elixir。但是，當你開發你的應用程式時並不一定需要使用它。你可以自由使用你想用的任何資源檔管線工具，甚至根本不需使用。

<a name="installation"></a>
## 安裝及設置

### 安裝 Node

在開始使用 Elixir 之前，你必須先確定你的機器上有安裝 Node.js。

    node -v

預設情況下，Laravel Homestead 會包含你所需的一切；但是，如果你沒有使用 Vagrant，那麼你可以簡單的瀏覽 [Node 的下載頁面](http://nodejs.org/download/)進行安裝。

### Gulp

接著，你需要全域安裝 [Gulp](http://gulpjs.com) 的 NPM 套件：

    npm install --global gulp

### Laravel Elixir

最後的步驟就是安裝 Elixir！伴隨著新安裝的 Laravel，你會發現根目錄有個名為 `package.json` 的檔案。想像它就如同你的 `composer.json` 檔案，只是它定義的是 Node 的依賴套件，而不是 PHP 的。你可以使用以下的指令安裝依賴套件：

    npm install

如果你是在 Windows 系統上或在 Windows 主機系統上執行 VM 進行開發，你需要在執行 `npm install` 指令時將 `--no-bin-links` 開啟：

    npm install --no-bin-links

<a name="running-elixir"></a>
## 執行 Elixir

Elixir 是建立於 [Gulp](http://gulpjs.com) 之上，所以要執行你的 Elixir 任務，只需要在終端機執行 `gulp` 指令。在指令增加 `--production` 標示會告知 Elixir 壓縮你的 CSS 及 JavaScript 檔案：

    // 執行所有任務...
    gulp

    // 執行所有任務並壓縮所有 CSS 及 JavaScript...
    gulp --production

#### 監控資源檔變更

因為每次變更你的資源檔之後在終端機執行 `gulp` 指令相當不便，因此你可以使用 `gulp watch` 指令。此指令會在你的終端機繼續執行，並監控資源檔的任何變更。當發生變更時，新檔案將會自動被編譯：

    gulp watch

<a name="working-with-stylesheets"></a>
## 使用樣式

專案根目錄的 `gulpfile.js` 包含你所有的 Elixir 任務。Elixir 任務可以被鏈結起來，以定義你的資源檔該如何進行編譯。

<a name="less"></a>
### Less

要將 [Less](http://lesscss.org/) 編譯至 CSS，你可以使用 `less` 方法。`less` 方法會假設你的 Less 檔案被儲存在 `resources/assets/less`。預設情形下，此範例的任務會將編譯後的 CSS 放置於 `public/css/app.css`：

```javascript
elixir(function(mix) {
    mix.less('app.less');
});
```

你可能會想合併多個 Less 檔案至單一的 CSS 檔案。同樣的，產生的 CSS 會被放置於 `public/css/app.css`：

```javascript
elixir(function(mix) {
    mix.less([
        'app.less',
        'controllers.less'
    ]);
});
```

如果你想自定編譯後的 CSS 的輸出位置，你可以傳遞第二個參數至 `less` 方法：

```javascript
elixir(function(mix) {
    mix.less('app.less', 'public/stylesheets');
});

// 指定輸出的檔案名稱...
elixir(function(mix) {
    mix.less('app.less', 'public/stylesheets/style.css');
});
```

<a name="sass"></a>
### Sass

`sass` 方法讓你能編譯 [Sass](http://sass-lang.com/) 至 CSS。你的 Sass 檔案預設會被儲存在 `resources/assets/sass`，你可以像這樣使用此方法：

```javascript
elixir(function(mix) {
    mix.sass('app.scss');
});
```

同樣的，如同 `less` 方法，你可以編譯多個 Sass 檔案至單一的 CSS 檔案，甚至可以自定產生的 CSS 的輸出目錄：

```javascript
elixir(function(mix) {
    mix.sass([
        'app.scss',
        'controllers.scss'
    ], 'public/assets/css');
});
```

<a name="plain-css"></a>
### 純 CSS

如果你只是想將一些純 CSS 樣式合併成單一的檔案，你可以使用 `styles` 方法。傳遞給此方法的路徑相對於 `resources/assets/css` 目錄，而產生的 CSS 會被放置於 `public/css/all.css`：

```javascript
elixir(function(mix) {
    mix.styles([
        'normalize.css',
        'main.css'
    ]);
});
```

當然，你也可以透過傳遞第二個參數至 `styles` 方法，將產生的檔案輸出至自定的位置：

```javascript
elixir(function(mix) {
    mix.styles([
        'normalize.css',
        'main.css'
    ], 'public/assets/css');
});
```

<a name="css-source-maps"></a>
### Source Maps

Source maps 在預設情況下是開啟的。因此，針對每個被編譯的檔案，同目錄內都會伴隨著一個 `*.css.map` 檔案。這個檔案能夠讓你在瀏覽器除錯時，可以追蹤編譯後的樣式選擇器至原始的 Sass 或 Less 位置。

如果你不想為你的 CSS 產生 source maps，你可以使用一個簡單的設定選項關閉它們：

```javascript
elixir.config.sourcemaps = false;

elixir(function(mix) {
    mix.sass('app.scss');
});
```

<a name="working-with-scripts"></a>
## 使用腳本

Elixir 也提供了一些函式來幫助你使用 JavaScript 檔案，像是編譯 ECMAScript 6、編譯 CoffeeScript、Browserify、壓縮、及簡單的串聯純 JavaScript 檔案。

<a name="coffeescript"></a>
### CoffeeScript

`coffee` 方法可以用於編譯 [CoffeeScript](http://coffeescript.org/) 至純 JavaScript。`coffee` 函式接收一個相對於 `resources/assets/coffee` 目錄的 CoffeeScript 檔案字串或陣列，接著在 `public/js` 目錄產生單一的 `app.js` 檔案：

```javascript
elixir(function(mix) {
    mix.coffee(['app.coffee', 'controllers.coffee']);
});
```

<a name="browserify"></a>
### Browserify

Elixir 還附帶了一個 `browserify` 方法，給予你在瀏覽器引入模組及 ECMAScript 6 的所有好處。

此任務假設你的腳本都儲存在 `resources/assets/js`，並會將產生的檔案放置於 `public/js/main.js`：

```javascript
elixir(function(mix) {
    mix.browserify('main.js');
});
```

雖然 Browserify 附帶了 Partialify 及 Babelify 轉換器，但是如果你希望，你可以自由地安裝並增加更多的轉換器：

    npm install aliasify --save-dev

```javascript
elixir.config.js.browserify.transformers.push({
    name: 'aliasify',
    options: {}
});

elixir(function(mix) {
    mix.browserify('main.js');
});
```

<a name="babel"></a>
### Babel

`babel` 方法可被用於編譯 [ECMAScript 6 與 7](https://babeljs.io/docs/learn-es2015/) 至純 JavaScript。此函式接收一個相對於 `resources/assets/js` 目錄的檔案陣列，接著在 `public/js` 目錄產生單一的 `all.js` 檔案：

```javascript
elixir(function(mix) {
    mix.babel([
        'order.js',
        'product.js'
    ]);
});
```

若要選擇不同的輸出位置，只需簡單的指定你希望的路徑作為第二個參數。該方法除了 Babel 的編譯外，特色與功能同等於 `mix.scripts()`。


<a name="javascript"></a>
### Scripts

如果你想將多個 JavaScript 檔案合併至單一檔案，你可以使用 `scripts` 方法。

`scripts` 方法假設所有的路徑都相對於 `resources/assets/js` 目錄，且預設會將產生的 JavaScript 放置於 `public/js/all.js`：

```javascript
elixir(function(mix) {
    mix.scripts([
        'jquery.js',
        'app.js'
    ]);
});
```

如果你想多個腳本的集合合併成不同檔案，你可以使用呼叫多個 `scripts` 方法。給予該方法的第二個參數會為每個串聯決定產生的檔案名稱：

```javascript
elixir(function(mix) {
    mix.scripts(['app.js', 'controllers.js'], 'public/js/app.js')
       .scripts(['forum.js', 'threads.js'], 'public/js/forum.js');
});
```

如果你想合併給定目錄中的所有腳本，你可以使用 `scriptsIn` 方法。產生的 JavaScript 會被放置在 `public/js/all.js`：

```javascript
elixir(function(mix) {
    mix.scriptsIn('public/js/some/directory');
});
```

<a name="copying-files-and-directories"></a>
## 複製檔案與目錄

`copy` 方法可以被用於複製檔案與目錄至新位置。所有操作都相對於專案的根目錄：

```javascript
elixir(function(mix) {
	mix.copy('vendor/foo/bar.css', 'public/css/bar.css');
});

elixir(function(mix) {
	mix.copy('vendor/package/views', 'resources/views');
});
```

<a name="versioning-and-cache-busting"></a>
## 版本與暫存清除

許多的開發者會在它們編譯後的資源檔加上時間戳記或是獨特的 token，強迫瀏覽器載入全新的資源檔以取代提供的舊版本程式碼副本。你可以使用 `version` 方法讓 Elixir 處理它們。

`version` 方法接收一個相對於 `public` 目錄的檔案名稱，接著為你的檔案名稱加上獨特的雜湊值，以防止檔案被快取。舉例來說，產生出來的檔案名稱可能像這樣：`all-16d570a7.css`：

```javascript
elixir(function(mix) {
    mix.version('css/all.css');
});
```

在為檔案產生版本之後，你可以在你的[視圖](/docs/{{version}}/views)中使用 Laravel 的全域 `elixir` PHP 輔助函式來正確載入名稱被雜湊後的檔案。`elixir` 函式會自動判斷被雜湊的檔案名稱：

    <link rel="stylesheet" href="{{ elixir('css/all.css') }}">

#### 為多個檔案產生版本

你可以傳遞一個陣列至 `version` 方法來為多個檔案產生版本：

```javascript
elixir(function(mix) {
    mix.version(['css/all.css', 'js/app.js']);
});
```

一旦該檔案被加上版本，你需要使用 `elixir` 輔助函式來產生被雜湊檔案的正確連結。切記，你只需要傳遞未雜揍檔案的名稱至 `elixir` 輔助函式。此函式使用未雜湊的名稱來判斷該檔案為目前的雜湊版本：

    <link rel="stylesheet" href="{{ elixir('css/all.css') }}">

    <script src="{{ elixir('js/app.js') }}"></script>

<a name="browser-sync"></a>
## BrowserSync

當你對前端資源進行修改後，BrowserSync 會自動重新整理你的網頁瀏覽器。你可以使用 `browserSync` 方法來告知 Elixir，當你執行 `gulp watch` 指令時啟動 BrowserSync 伺服器：

```javascript
elixir(function(mix) {
    mix.browserSync();
});
```

一旦你執行 `gulp watch`，就可以使用連接埠 3000 啟用瀏覽器同步並存取你的網頁應用程式：`http://homestead.app:3000`。如果你在本機開發所使用的域名不是 `homestead.app`，那麼你可以傳遞一個[選項](http://www.browsersync.io/docs/options/)的陣列作為 `browserSync` 方法的第一個參數：

```javascript
elixir(function(mix) {
    mix.browserSync({
    	proxy: 'project.app'
    });
});
```

<a name="calling-existing-gulp-tasks"></a>
## 呼叫既有的 Gulp 任務

如果你需要在 Elixir 呼叫一個既有的 Gulp 任務，你可以使用 `task` 方法。舉個例子，假設你有一個 Gulp 任務，當你呼叫時就會說一些簡單的文字。

```javascript
gulp.task('speak', function() {
    var message = 'Tea...Earl Grey...Hot';

    gulp.src('').pipe(shell('say ' + message));
});
```

如果你希望在 Elixir 呼叫這個任務，使用 `mix.task` 方法並傳遞該任務的名稱作為該方法唯一的參數：

```javascript
elixir(function(mix) {
    mix.task('speak');
});
```

#### 自訂監控器

如果你想註冊一個監控器讓你的自定任務能在每次檔案改變時就執行，只需傳遞一個正規表示式作為 `task` 方法的第二個參數：

```javascript
elixir(function(mix) {
    mix.task('speak', 'app/**/*.php');
});
```

<a name="writing-elixir-extensions"></a>
## 撰寫 Elixir 擴充功能

如果你需要比 Elixir 的 `task` 方法提供的更靈活，你可以建立自定的 Elixir 擴充功能。Elixir 擴充功能允許你傳遞參數至你的自定任務。舉例來說，你可以撰寫一個擴充功能，像是：

```javascript
// 檔案：elixir-extensions.js

var gulp = require('gulp');
var shell = require('gulp-shell');
var Elixir = require('laravel-elixir');

var Task = Elixir.Task;

Elixir.extend('speak', function(message) {

    new Task('speak', function() {
        return gulp.src('').pipe(shell('say ' + message));
    });

});

// mix.speak('Hello World');
```

就是這樣！注意，你的 Gulp 具體的邏輯必須被放置在 `Task` 第二個參數傳遞的建構子函式。你可以將此擴充功能放置在 Gulpfile 的上方，取而代之也可以導出至一個自定任務的檔案。舉個例子，如果你將你的擴充功能放置在 `elixir-extensions.js`，你可以在你的 `Gulpfile` 引入該檔案，像是：

```javascript
// 檔案：Gulpfile.js

var elixir = require('laravel-elixir');

require('./elixir-extensions')

elixir(function(mix) {
    mix.speak('Tea, Earl Grey, Hot');
});
```

#### 自訂監控器

如果你想在執行 `gulp watch` 時能夠重新觸發你的自定任務，你可以註冊一個監控器：

```javascript
new Task('speak', function() {
    return gulp.src('').pipe(shell('say ' + message));
})
.watch('./app/**');
```
