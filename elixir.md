# Laravel Elixir

- [簡介](#introduction)
- [安裝](#installation)
- [使用方式](#usage)
- [Gulp](#gulp)
- [功能擴充](#extensions)

<a name="introduction"></a>
## 簡介

Laravel Elixir 提供了簡潔流暢的 API，讓你能夠為你的 Laravel 應用程式定義基本的 [Gulp](http://gulpjs.com) 任務。Elixir 支援許多常見的 CSS 與 JavaScrtip 預處理器，甚至包含了測試工具。

如果你曾經對於使用 Gulp 及編譯資源感到困惑，那麼你絕對會愛上 Laravel Elixir！

<a name="installation"></a>
## 安裝與設定

### 安裝 Node

在開始使用 Elixir 之前，你必須先確定你的開發環境上有安裝 Node.js。

    node -v

預設情況下，Laravel Homestead 會包含你所需的一切；然而，如果你沒有使用 Vagrant，那麼你可以瀏覽 [Node 的下載頁](http://nodejs.org/download/) 進行安裝。別擔心，安裝是很簡單又快速的！

### Gulp

接著你需要全域安裝 [Gulp](http://gulpjs.com) 的 NPM 安裝包，像是這樣：

    npm install --global gulp

### Laravel Elixir

最後的步驟就是安裝 Elixir！伴隨著新安裝的 Laravel，你會發現根目錄有個名為 `package.json` 的檔案。想像它就如同你的 `composer.json` 檔案，只是它定義的是 Node 的依賴，而不是 PHP。你可以使用以下的指令進行安裝依賴的動作：

	npm install

<a name="usage"></a>
## 使用方式

現在你已經安裝好 Elixir，未來任何時候你都能進行編譯及合併檔案！專案根目錄的 `gulpfile.js` 包含你所有的 Elixir 任務。

#### 編譯 Less

```javascript
elixir(function(mix) {
	mix.less("app.less");
});
```

在上述例子中，Elixir 會假設你的 Less 檔案儲存在 `resources/assets/less` 裡。

#### 編譯多個 Less 檔案

```javascript
elixir(function(mix) {
	mix.less([
		'app.less',
		'something-else.less'
	]);
});
```

#### 編譯 Sass

```javascript
elixir(function(mix) {
	mix.sass("app.sass");
});
```

在上述例子中，是假設你的 Sass 檔案儲存在 `resources/assets/sass` 裡。

以預設來說，Elixir 在執行時底層採用的是 LibSass 函式庫來編譯。在一些實例中，Ruby 的版本被證明比前者更加有利，雖然它速度較慢一些，但是它擁有更加豐富的功能。假設你已經安裝了 Ruby 及 Sass 的 gem（`gem install sass`），你可以開啟 Ruby 的模式，如下：

```javascript
elixir(function(mix) {
	mix.rubySass("app.sass");
});
```

#### 編譯並排除 Source Maps

```javascript
elixir.config.sourcemaps = false;

elixir(function(mix) {
	mix.sass("app.scss");
});
```

Source maps 在預設情況下是開啟的。因此，在每個被編譯的檔案，同目錄內都會伴隨著一個 `*.css.map` 檔案。這個檔案能夠讓你在除錯時，能夠追蹤編譯後的樣式表選擇器至原始的 Sass 或 Less 位置。如果你想要關閉此功能，當然，上方的範例程式碼做的就是這件事情。

#### 編譯 CoffeeScript

```javascript
elixir(function(mix) {
	mix.coffee();
});
```

在上述例子中，Elixir 會假設你的 CoffeeScript 檔案儲存在 `resources/assets/coffee` 裡。

#### 編譯所有的 Less 及 CoffeeScript

```javascript
elixir(function(mix) {
    mix.less()
       .coffee();
});
```

#### 觸發 PHPUnit 測試

```javascript
elixir(function(mix) {
	mix.phpUnit();
});
```

#### 觸發 PHPSpec 測試

```javascript
elixir(function(mix) {
	mix.phpSpec();
});
```

#### 合併樣式檔案

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	]);
});
```

傳遞給此方法的檔案路徑均相對於 `resources/assets/css` 目錄。

#### 合併樣式檔案且儲存在自訂的路徑

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	], 'public/build/css/everything.css');
});
```

#### 從特定相對目錄合併樣式檔案

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	], 'public/build/css/everything.css', 'public/css');
});
```

`styles` 與 `scrtips` 方法可以透過傳入第三個參數來決定來源檔案的相對目錄。

#### 合併指定目錄裡所有的樣式檔案

```javascript
elixir(function(mix) {
	mix.stylesIn("public/css");
});
```

#### 合併腳本檔案

```javascript
elixir(function(mix) {
	mix.scripts([
		"jquery.js",
		"app.js"
	]);
});
```

同樣的，傳遞給此方法的檔案路徑均相對於 `resources/assets/js` 目錄

#### 合併指定目錄裡所有的腳本檔案

```javascript
elixir(function(mix) {
	mix.scriptsIn("public/js/some/directory");
});
```

#### 合併多組腳本檔案

```javascript
elixir(function(mix) {
    mix.scripts(['jquery.js', 'main.js'], 'public/js/main.js')
       .scripts(['forum.js', 'threads.js'], 'public/js/forum.js');
});
```

#### 壓縮檔案並加上雜湊的版本號

```javascript
elixir(function(mix) {
	mix.version("css/all.css");
});
```

這個動作會為你的檔案名稱加上獨特的雜湊值，以防止檔案被快取。舉例來說，產生出來的檔案名稱可能像這樣：`all-16d570a7.css`。

接著在你的視圖中，你能夠使用 `elixir()` 函式來正確載入名稱被雜湊後的檔案。舉例如下：

```html
<link rel="stylesheet" href="{{ elixir("css/all.css") }}">
```

程式的作用下，`elixir()` 函式會將參數內的原始檔名轉換成被雜湊後的檔名並載入。是否有如釋重擔的感覺呢？

你也可以傳遞一個陣列給 `version` 方法來把多個檔案加上版本：

```javascript
elixir(function(mix) {
	mix.version(["css/all.css", "js/app.js"]);
});
```

```html
<link rel="stylesheet" href="{{ elixir("css/all.css") }}">
<script src="{{ elixir("js/app.js") }}"></script>
```

#### 複製檔案到新的位置

```javascript
elixir(function(mix) {
	mix.copy('vendor/foo/bar.css', 'public/css/bar.css');
});
```

#### 將整個目錄都複製到新的位置

```javascript
elixir(function(mix) {
	mix.copy('vendor/package/views', 'resources/views');
});
```

#### Trigger Browserify

```javascript
elixir(function(mix) {
	mix.browserify('index.js');
});
```

Want to require modules in the browser? Hoping to use EcmaScript 6 sooner than later? Need a built-in JSX transformer? If so, [Browserify](http://browserify.org/), along with the `browserify` Elixir task, will handle the job nicely.

This task assumes that your scripts are stored in `resources/assets/js`, though you're free to override the default.

#### 方法連接

當然，你能夠串連 Elixir 大部份的方法來建立一連串的任務：

```javascript
elixir(function(mix) {
    mix.less("app.less")
       .coffee()
       .phpUnit()
       .version("css/bootstrap.css");
});
```

<a name="gulp"></a>
## Gulp

現在你已經告訴 Elixir 要執行的任務，接著只需要在命令列執行 Gulp。

#### 執行一次所有註冊的任務

	gulp

#### 監控檔案變更

	gulp watch

#### 只編譯腳本

	gulp scripts

#### 只編譯樣式

	gulp styles

#### 監控測試以及 PHP 類別的變更

	gulp tdd

> **提示：** 所有的任務都會使用開發環境進行，所以壓縮功能不會被執行。如果要使用上線環境，可以使用 `gulp --production`。

<a name="extensions"></a>
## 自訂任務及擴展

有些時候，你可能寫要在掛接自己的 Gulp 任務至 Elixie 中。也許你的功能有點特別，並且想透過 Elixir 來幫你混合或是監看。這當然沒問題！

舉個例子，假設你有一個一般的任務，當你呼叫時就會說一些簡單的文字。

```javascript
gulp.task("speak", function() {
	var message = "Tea...Earl Grey...Hot";

	gulp.src("").pipe(shell("say " + message));
});
```

很容易的。當然，在終端機中，你可以透過呼叫 `gulp speak` 來觸發這個任務。想要將這個任務加入 Elixir ，你只需要使用 `mix.task()` 方法：

```javascript
elixir(function(mix) {
    mix.task('speak');
});
```

就是這樣！現在開始，當你每次執行 Gulp，你自訂的「speak」任務就會和其他 Gulp 任務一起被執行，因為你已經將他們混合在一起了。除此之外你也可以註冊一個監控器，當一個或多個檔案被修改時，就重新觸發你的自訂任務，你只需要傳入一個正規表示式作為第二個參數。

```javascript
elixir(function(mix) {
    mix.task('speak', 'app/**/*.php');
});
```

在加入第二個參數之後，每次只要有 PHP 檔案在「app/」資料夾中被儲存，就會重新觸發「speak」任務。


為了得到更好的靈活性，你可以建立一個完整的 Elixir 擴展。以剛剛的「speak」作為範例，如果你想寫一個擴展，可以這麼做：

```javascript
var gulp = require("gulp");
var shell = require("gulp-shell");
var elixir = require("laravel-elixir");

elixir.extend("speak", function(message) {

	gulp.task("speak", function() {
		gulp.src("").pipe(shell("say " + message));
	});

	return this.queueTask("speak");

 });
```

請注意我們 `擴增（extend）` Elixir 的 API 時所使用的第一個參數名稱，稍後我們需要在 Gulpfile 中參考到它，以及建立 Gulp 任務所使用的回呼函式。

跟前面一樣，如果你想要讓你的自訂任務能被監控，只要在註冊一個監控器就行了。

```javascript
this.registerWatcher("speak", "app/**/*.php");
```

這行程式的意思是指，當符合正規表示式 `app/**/*.php` 的檔案一經修改，就會觸發 `speak` 任務。

很好！接著你可以將這行程式寫在 Gulpfile 的頂端，或者將它放到自訂任務的檔案裡。如果你選擇後者，那麼你必須將它載入至你的 Gulpfile，例如：

```javascript
require("./custom-tasks")
```

大功告成！最後你只需要將他們結合。

```javascript
elixir(function(mix) {
	mix.speak("Tea, Earl Grey, Hot");
});
```

加入之後，每當你觸發 Gulp，Picard 就會要求一些茶。
