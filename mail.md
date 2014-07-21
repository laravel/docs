# Mail

- [設定](#configuration)
- [基本用法](#basic-usage)
- [內嵌附件](#embedding-inline-attachments)
- [郵件佇列](#queueing-mail)
- [郵件與本地開發](#mail-and-local-development)

<a name="configuration"></a>
## 設定

Laravel 提供一個乾淨簡單的API建構在一個受歡迎的函式庫[SwiftMailer](http://swiftmailer.org)之上，郵件的設定檔案是`app/config/mail.php`，裡面包含了許多設定項目讓你可以更換你的SMTP主機、Port以及相關驗證，還有一個全域的寄件者`from`設定透過這個函式庫，你也可以使用任何你希望的SMTP伺服器。

假如你希望使用PHP`mail`函式來寄發郵件，你可以更變設定檔中的`driver`為`mail`，當然`sendmail`也是可以用的

### 第三方Mail服務API驅動方法


Laravel 當然也包含了Mailgun及Mandrill HTTP APIs的驅動方式，這些APIs通常比SMTP伺服器更簡單快速，這二者的驅動方式必需先在你的應用程式加載及安裝Guzzle 4 HTTP函式庫，你可以新增一行指令在`composer.json`把Guzzle 4加到你的專案。(別忘了composer update)

	"guzzlehttp/guzzle": "~4.0"

#### Mailgun驅動方法

要使用Mailgun請先將`app/config/mail.php`設定檔中的`driver`設定為`mailgun`，接下來新增一個`app/config/services.php`的設定檔(假如這個檔案不在你的專案中)，檢查這個檔案有包含下列項目


	'mailgun' => array(
		'domain' => 'your-mailgun-domain',
		'secret' => 'your-mailgun-key',
	),

#### Mandrill驅動方法

要使用Mandrill請先將`app/config/mail.php`設定檔中的`driver`設定為`mandrill`，接下來新增一個`app/config/services.php`的設定檔(假如這個檔案不在你的專案中)，檢查這個檔案有包含下列項目

	'mandrill' => array(
		'secret' => 'your-mandrill-key',
	),

### Log驅動方法

假如你的`app/config/mail.php`設定檔中的`driver`為`log`時，所有的電子郵件將會寫入你的日誌檔且他們將不會真的被寄出，這主要是讓本機開更有用且快速的發除錯及內容驗證。

<a name="basic-usage"></a>
## 基本用法

The `Mail::send` method may be used to send an e-mail message:
 `Mail::send`方法是用來寄送電子郵件：

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

`send`方法的第一個參數為email內容應該使用哪個view的名稱，第二個參數`$data`為傳遞至view的變數而第三個參數為一個閉包讓你可以允許指定寄送電子郵件的訊息選項。


> **註記:** 一個 `$message` 變數一定會使用一個view作為電子郵件的樣版，且允許使用內嵌附件，所以最好避免傳遞`message`變數 到你的view之中


你也可以指定一個純文字的view新增至一個HTML view

	Mail::send(array('html.view', 'text.view'), $data, $callback);


或是你也可以使用索引 `html` 或 `text` 指定單一類型的view

	Mail::send(array('text' => 'view'), $data, $callback);


你也可以為電子郵件訊息指定其他選項如附加檔案或是任何的副本收件者

	Mail::send('emails.welcome', $data, function($message)
	{
		$message->from('us@example.com', 'Laravel');

		$message->to('foo@example.com')->cc('bar@example.com');

		$message->attach($pathToFile);
	});


當附加檔案到一個電子郵件，你也可以指定一個MIME type及/ 或一個顯示名稱：

	$message->attach($pathToFile, array('as' => $display, 'mime' => $mime));

> **註記:** 在`Mail::send`的閉包中使用SwiftMailer的message擴充實例，允許你可以呼叫任何類別中的方法來建立你的電子郵件

<a name="embedding-inline-attachments"></a>
## 內嵌附件Embedding Inline Attachments

要內嵌一個圖片到你的電子郵件通常是一件很累的工作，然而Laravel 提供一個便利的方式讓你內嵌圖片到你的電子郵件當中，只要設定一個適當的CID

#### 內嵌一個圖片到電子郵件的View中

	<body>
		Here is an image:

		<img src="<?php echo $message->embed($pathToFile); ?>">
	</body>

#### 內嵌一筆資料到電子郵件的View中Embedding Raw Data In An E-Mail View

	<body>
		Here is an image from raw data:

		<img src="<?php echo $message->embedData($data, $name); ?>">
	</body>

注意`$message`這個變數一定會被`Mail`類別傳遞到電子郵件的view當中

<a name="queueing-mail"></a>
## 郵件佇列

#### 加入一個郵件到佇列中

寄送電子郵件會大幅的延長你應用程式的反應時間，許多開發者選擇佇列讓電子郵件在背景(非即時)寄送，Laravel使用內建的[unified queue API](/docs/queues)讓你可以方便的將要寄送的電子郵件加入到佇列之中，簡單的在`Mail`類別之中的`queue`：

	Mail::queue('emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});


你也可以指定你希望的延遲秒數來寄送電子郵件透過使用`later`

	Mail::later(5, 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});


假如你希望指定一個特定的佇列來寄送電子郵件，你可以使用`queueOn` 及 `laterOn` :

	Mail::queueOn('queue-name', 'emails.welcome', $data, function($message)
	{
		$message->to('foo@example.com', 'John Smith')->subject('Welcome!');
	});

<a name="mail-and-local-development"></a>
## 郵件與本地開發


當開發一個應用程式的寄信功能，通常會希望在本地端或是開發環境關閉它，當你要這樣做你可以呼叫`Mail::pretend`或是設定`pretend`選項為`true`在`app/config/mail.php`設定檔裡，當寄送程式在`pretend`模式時，電子郵件將會被寫入你的應用程式日誌中且包含應該被寄到的收件者。

#### 開啟"Pretend"寄送模式

	Mail::pretend();
