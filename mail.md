# Mail

- [設定](#configuration)
- [基本用法](#basic-usage)
- [內嵌附件](#embedding-inline-attachments)
- [郵件佇列](#queueing-mail)
- [郵件與本地開發](#mail-and-local-development)

<a name="configuration"></a>
## 設定

Laravel 利用一個熱門的函式庫 [SwiftMailer](http://swiftmailer.org) 來建立一個乾淨簡單的 API。郵件設定檔為 `app/config/mail.php`，裏面有些選項，可以讓你更改你的 SMTP 連接埠、憑證以及可以為透過此函式庫寄出的所有信件，設定一個全域的寄件者 `from`。你可以使用任何的 SMTP 伺服器。如果你想要使用 PHP 內建的 `mail` 函式來寄送郵件，你可以將設定檔中的 `driver` 改為 `mail` 即可。`sendmail` 的驅動一樣可以使用。


### 第三方郵件服務 API 驅動

Laravel 也包含了 Mailgun 和 Mandrill 服務的 HTTP API 的驅動方式。這些 API 比使用 SMTP 伺服器更簡單快速。這些驅動都需要在你的應用程式裡預先安裝 Guzzle 4 HTTP 函式庫。你可以透過在你的 `composer.json` 檔中增加一行如下，來將 Guzzle 4 安裝到你的專案中：

	"guzzlehttp/guzzle": "~4.0"

#### Mailgun 驅動

使用 Mailgun 驅動前，先在 `app/config/mail.php` 設定檔中將 `driver` 設定為 `mailgun`。再來，如果你的專案中沒有 `app/config/services.php` 請先建立他。並確定它包含了如下的內容：

	'mailgun' => array(
		'domain' => 'your-mailgun-domain',
		'secret' => 'your-mailgun-key',
	),

#### Mandrill 驅動

使用 Mandrill 驅動前，先在 `app/config/mail.php` 設定檔中將 `driver` 設定為 `mandrill`。再來，如果你的專案中沒有 `app/config/services.php` 請先建立他。並確定它包含了如下的內容：

	'mandrill' => array(
		'secret' => 'your-mandrill-key',
	),

### Log 驅動

如果你的 `app/config/mail.php` 設定檔的 `driver` 被設定為 `log` 時，所有的郵件將會被寫進日誌中，且並不會真的被寄出。這主要用在快速本地除錯和內容驗證上。

<a name="basic-usage"></a>
## 基本用法

 `Mail::send` 方法是用來寄送電子郵件：

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

`send` 方法的第一個參數為郵件內容的視圖名稱，第二個參數 `$data` 為傳遞至視圖的變數，而第三個參數為一個閉包讓你可以指定更多寄送電子郵件的訊息選項。


> **注意:** 變數預設被傳遞進郵件的視圖中，且允許內嵌復健。所以最好避免傳遞名為 `message` 的變數至你的視圖中造成重疊。

除了使用 HTML 視圖外，你也可以指定一個純文字的視圖：

	Mail::send(array('html.view', 'text.view'), $data, $callback);


或者你也可以指定視圖類別為 `html` 或 `text`：

	Mail::send(array('text' => 'view'), $data, $callback);


你也可以為電子郵件訊息指定其他選項如附加檔案或是任何的副本收件者：

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');

		$message->attach($pathToFile);
	});


當附加檔案到一個電子郵件，你也可以指定一個 MIME type 及/或 一個顯示名稱：

	$message->attach($pathToFile, array('as' => $display, 'mime' => $mime));

> **注意:** 在 `Mail::send` 的閉包中使用 SwiftMailer 的 message 擴充實例，允許你可以呼叫任何類別中的方法來建立你的電子郵件。

<a name="embedding-inline-attachments"></a>
## 內嵌附件

內嵌圖片到郵件中通常是一件很麻煩的事，然而Laravel 提供一個便利的方式讓你內嵌圖片到你的電子郵件當中且接收相對應的 CID。

#### 內嵌圖片到電子郵件的視圖中

	<body>
		Here is an image:

		<img src="<?php echo $message->embed($pathToFile); ?>">
	</body>

#### 內嵌資料到電子郵件的視圖中

	<body>
		Here is an image from raw data:

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

注意 `$message` 這個變數一定會被 `Mail` 類別傳遞到電子郵件的視圖當中。

<a name="queueing-mail"></a>
## 郵件佇列

#### 加入一個郵件到佇列中

寄送電子郵件會大幅的延長你應用程式的反應時間，許多開發者選擇讓電子郵件放進隊列中，並在背景(非即時)寄送。Laravel 使用內建的 [unified queue API](/docs/queues) 讓你可以方便的將要寄送的電子郵件加入到隊列之中，只要使用 `Mail` 類別的 `queue` 方法：

	Mail::queue('emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

你也可以透過使用 `later` 方法來指定寄送電子郵件的延遲秒數：

	Mail::later(5, 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

假如你想要指定一個特別的隊列或管道來發送郵件，你可以使用 `queueOn` 和 `laterOn` 方法：

	Mail::queueOn('queue-name', 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

<a name="mail-and-local-development"></a>
## 郵件與本地開發

在開發應用程式的寄信功能時，通常會希望在本地或是開發環境中關閉寄送功能。你可以呼叫 `Mail::pretend` 方法，或是在 `app/config/mail.php` 設定檔的 `pretend` 為 `true` 可以達到。當在 `pretend` 模式開啟下，郵件將會被寫到你的應用程式日誌中取代實際寄出信件。


#### 開啟 "Pretend" 寄送模式

	Mail::pretend();
