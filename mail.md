# 郵件

- [簡介](#introduction)
- [寄送郵件](#sending-mail)
    - [附件](#attachments)
    - [內部附件](#inline-attachments)
    - [隊列郵件](#queueing-mail)
- [郵件與本機端開發](#mail-and-local-development)
- [事件](#events)

<a name="introduction"></a>
## 簡介

Laravel 基於熱門的 [SwiftMailer](http://swiftmailer.org) 函式庫提供了一個簡潔的 API。Laravel 為 SMTP、Mailgun、Mandrill、Amazon SES、PHP 的 `mail` 函式及 `sendmail` 提供驅動，讓你可以快速地以所選擇的本地或雲端服務開始寄送郵件。

### 驅動前提

基於 API 的驅動，例如 Mailgun 或 Mandrill，通常比 SMTP 伺服器更簡單快速。所有的 API 驅動都需要在應用程式中安裝 Guzzle HTTP 函式庫。你可在 `composer.json` 檔案中加入下面這一行，以便於在專案中安裝 Guzzle：

    "guzzlehttp/guzzle": "~5.3|~6.0"

#### Mailgun 驅動

要使用 Mailgun 驅動，首先必須安裝 Guzzle，之後將 `config/mail.php` 設定檔中的 `driver` 選項設定為 `mailgun`。接下來，確認 `config/services.php` 設定檔包含下列選項：

    'mailgun' => [
        'domain' => 'your-mailgun-domain',
        'secret' => 'your-mailgun-key',
    ],

#### Mandrill 驅動

要使用 Mandrill 驅動，首先必須安裝 Guzzle，之後將 `config/mail.php` 設定檔中的 `driver` 選項設定為 `mandrill`。接下來，確認 `config/services.php` 設定檔包含下列選項：

    'mandrill' => [
        'secret' => 'your-mandrill-key',
    ],

#### SES 驅動

要使用 Amazon SES 驅動，必須安裝 PHP 的 Amazon AWS SDK。你可在 `composer.json` 檔案的 `require` 段落加入下面這一行以安裝此函式庫：

    "aws/aws-sdk-php": "~3.0"

接下來，將 `config/mail.php` 設定檔中的 `driver` 選項設定為 `ses`。然後確認 `config/services.php` 設定檔包含下列選項：

    'ses' => [
        'key' => 'your-ses-key',
        'secret' => 'your-ses-secret',
        'region' => 'ses-region',  // 例如 us-east-1
    ],

<a name="sending-mail"></a>
## 寄送郵件

Laravel 允許你在[視圖](/docs/{{version}}/views)中存放電子郵件訊息。例如，要組織你的電子郵件，你可以在 `resource/views` 目錄中建立 `emails` 目錄：

要寄送訊息，使用 `Mail` [facade](/docs/{{version}}/facades) 的 `send` 方法。`send` 方法接收三個參數。首先是包含郵件訊息的[視圖](/docs/{{version}}/views)名稱。其次是一個要傳遞給該視圖的資料陣列。最後是一個`閉包`回呼用來接收訊息實例，讓你可以自訂收件者、主旨，以及郵件訊息的其他部分：

    <?php

    namespace App\Http\Controllers;

    use Mail;
    use App\User;
    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * 發封電子郵件提醒給使用者。
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function sendEmailReminder(Request $request, $id)
        {
            $user = User::findOrFail($id);

            Mail::send('emails.reminder', ['user' => $user], function ($m) use ($user) {
                $m->from('hello@app.com', 'Your Application');

                $m->to($user->email, $user->name)->subject('Your Reminder!');
            });
        }
    }

在上面的例子中，我們傳了包含 `user` 鍵的陣列，因此可以使用下列的 PHP 程式碼，在郵件視圖中顯示使用者名稱：

    <?php echo $user->name; ?>

> **注意：**`$message` 變數永遠會被傳遞至電子郵件視圖，且允許[內部嵌入附件](#attachments)。因此，你應該避免將 `message` 變數傳至視圖。

#### 建立訊息

如先前討論過的，傳給 `send` 方法的第三個參數是一個`閉包`，讓你可以對電子郵件訊息本體指定不同的選項。使用此閉包，你可以指定訊息的其他屬性，例如副本、密件副本等等：

    Mail::send('emails.welcome', $data, function ($message) {
        $message->from('us@example.com', 'Laravel');

        $message->to('foo@example.com')->cc('bar@example.com');
    });

這是一份在 `$message` 訊息產生器實例中可以使用的方法清單：

    $message->from($address, $name = null);
    $message->sender($address, $name = null);
    $message->to($address, $name = null);
    $message->cc($address, $name = null);
    $message->bcc($address, $name = null);
    $message->replyTo($address, $name = null);
    $message->subject($subject);
    $message->priority($level);
    $message->attach($pathToFile, array $options = []);

    // 以原始 $data 字串附加一個檔案…
    $message->attachData($data, $name, array $options = []);

    // 取得底層的 SwiftMailer 訊息實例…
    $message->getSwiftMessage();

> **注意：**傳遞至 `Mail::send` 閉包的訊息實例繼承了 SwiftMailer 訊息類別，讓你可以呼叫該類別的任何方法來建立你的電子郵件訊息。

#### 寄送純文本

傳給 `send` 方法的視圖，在預設情況下會假定它包含 HTML。然而，藉由傳遞陣列作為 `send` 方法的第一個參數，除了 HTML 視圖之外，你還可以同時指定傳送純文本視圖：

    Mail::send(['html.view', 'text.view'], $data, $callback);

或者，若你只需要寄送純文本電子郵件，可以在陣列中使用 `text` 鍵來指定：

    Mail::send(['text' => 'view'], $data, $callback);

#### 寄送原始字串

若你希望直接發送原始字串，你可以使用 `raw` 方法：

    Mail::raw('Text to e-mail', function ($message) {
        //
    });

<a name="attachments"></a>
### 附件

要在電子郵件中加入附件，在傳遞給閉包的 `$message` 物件上使用 `attach` 方法。`attach` 方法接受檔案的完整路徑作為它的第一個參數：

    Mail::send('emails.welcome', $data, function ($message) {
        //

        $message->attach($pathToFile);
    });

附加檔案至訊息時，你也可以傳遞`陣列`給 `attach` 方法作為第二個參數，以指定顯示名稱和／或 MIME 型別：

    $message->attach($pathToFile, ['as' => $display, 'mime' => $mime]);

<a name="inline-attachments"></a>
### 內部附件

#### 在電子郵件視圖中嵌入圖像

在電子郵件中嵌入內部圖像通常是件很麻煩的事；然而 Laravel 提供一個便利的方法，讓你在電子郵件中附加圖像並取得適當的 CID。要嵌入內部圖像，在電子郵件視圖的 `$message` 變數中使用 `embed` 方法。記得，Laravel 會自動讓你所有的電子郵件視圖都能取得 `$message` 變數：

    <body>
        這是一張圖片：

        <img src="<?php echo $message->embed($pathToFile); ?>">
    </body>

#### 在電子郵件視圖中嵌入原始資料

若你已有希望嵌入電子郵件訊息中的原始資料字串，你可以在 `$message` 變數上使用 `embedData` 方法：

    <body>
        這是一張從原始資料來的圖片：

        <img src="<?php echo $message->embedData($data, $name); ?>">
    </body>

<a name="queueing-mail"></a>
### 隊列郵件

#### 將郵件訊息加入隊列

由於寄送電子郵件訊息會大幅延長應用程式的回應時間，許多開發者選擇將郵件訊息加入隊列並於背景發送。Laravel 使用其內建的[統一的隊列 API](/docs/{{version}}/queues)，讓你輕鬆地完成此工作。要將郵件訊息加入隊列，使用 `Mail` facade 的 `queue` 方法：

    Mail::queue('emails.welcome', $data, function ($message) {
        //
    });

此方法會自動將工作加入隊列，以便在背景發送郵件訊息。當然，在使用此功能之前，你需要[設定你的隊列](/docs/{{version}}/queues)。

#### 延遲的訊息隊列

若你希望延遲遞送已加入隊列的電子郵件訊息，你可以使用 `later` 方法。要著手開始，只要將你想要延遲寄送訊息的秒數，作為第一個參數傳送給此方法：

    Mail::later(5, 'emails.welcome', $data, function ($message) {
        //
    });

#### 加入特定隊列

若你想要指定特定的隊列來加入訊息 ，可使用 `queueOn` 及 `laterOn` 方法：

    Mail::queueOn('queue-name', 'emails.welcome', $data, function ($message) {
        //
    });

    Mail::laterOn('queue-name', 5, 'emails.welcome', $data, function ($message) {
        //
    });

<a name="mail-and-local-development"></a>
## 郵件與本地端開發

當開發需要寄送電子郵件的應用程式時，你有可能不想要實際地送出電子郵件到真正的郵件地址。Laravel 提供了幾種方法以「停止」將電子郵件訊息真正寄出。

#### 日誌驅動

一個解決方案是在本地端開發時使用 `log` 郵件驅動。此驅動會將所有的電子郵件訊息寫入日誌檔案作為檢驗之用。若需要更多根據環境來設定應用程式的資訊，可參考[設定文件](/docs/{{version}}/installation#environment-configuration)。

#### 通用收件者

另一個由 Lavavel 提供的解決方案，是設定一個通用的收件者給框架寄出的所有電子郵件。這樣，應用程式產生的所有電子郵件都會被送到一個特定的地址，而不是寄信時實際指定的收件人地址。這可以透過 `config/mail.php` 設定檔的 `to` 選項來完成：

    'to' => [
        'address' => 'dev@domain.com',
        'name' => 'Dev Example'
    ],

#### Mailtrap

最後，你可以使用像 [Mailtrap](https://mailtrap.io) 這樣的服務以及 `smtp` 驅動來將你的郵件訊息寄到一個「假的」郵箱，而你可以在一個真的郵件客戶端檢視它們。這個方法的好處是讓你可以在 Mailtrap 的訊息檢閱器中實際查看最終的電子郵件。

<a name="events"></a>
## Events

Laravel fires the `mailer.sending` event just before sending mail messages. Remember, this event is fired when the mail is *sent*, not when it is queued. You may register an event listener in your `EventServiceProvider`:

    /**
     * Register any other events for your application.
     *
     * @param  \Illuminate\Contracts\Events\Dispatcher  $events
     * @return void
     */
    public function boot(DispatcherContract $events)
    {
        parent::boot($events);

        $events->listen('mailer.sending', function ($message) {
            //
        });
    }

