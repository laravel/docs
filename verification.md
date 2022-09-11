# 電子郵件驗證

- [簡介](#introduction)
    - [模型的準備](#model-preparation)
    - [資料庫的準備](#database-preparation)
- [路由](#verification-routing)
    - [電子郵件驗證說明](#the-email-verification-notice)
    - [電子郵件驗證的處理程式](#the-email-verification-handler)
    - [重新傳送電子郵件驗證](#resending-the-verification-email)
    - [受保護的路由](#protecting-routes)
- [自定](#customization)
- [事件](#events)

<a name="introduction"></a>
## 簡介

許多網路應用程式都要求使用者先驗證電子郵件位址後才能繼續使用。與其迫使您為您創建的每個應用程式重新實作此功能，Laravel 提供了方便的內建服務來傳送和驗證電子郵件驗證的請求。

> **Note**   
> 想要快速入門嗎？ 請在全新的 Laravel 應用程式內安裝一個 [Laravel 應用程式入門套件](/docs/{{version}}/starter-kits) 。這些入門套件會幫你搞定整個驗證系統的基本架構，包含電子郵件驗證的支援。
<a name="model-preparation"></a>
### 模型的準備

在開始之前，請先確定 `App\Models\User` 有實作 `Illuminate\Contracts\Auth\MustVerifyEmail` contract:

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        use Notifiable;

        // ...
    }

當這個介面被添加到您的模型中，新註冊的用戶將會自動收到一封包含電子郵件驗證連結的電子郵件。如您所見，透過檢查您的應用程式的`App\Providers\EventServiceProvider`，Laravel 已經包含一個 `SendEmailVerificationNotification` [監聽器](/docs/{{version}}/events)附加到 `Illuminate\Auth\Events\Registered` 事件，此事件監聽器會將電子郵件驗證連結發送給用戶。

如果您在應用程式中自行實作註冊，而不是使用[Laravel 應用程式入門套件](/docs/{{version}}/starter-kits)，請確保有在使用者成功註冊後分派`Illuminate\Auth\Events\Registered` 事件:

    use Illuminate\Auth\Events\Registered;

    event(new Registered($user));

<a name="database-preparation"></a>
### 資料庫的準備

接下來，您的 `users` 資料表中應包含一個 `email_verified_at` 欄位來儲存使用者驗證其電子郵件位址的日期時間。預設情況下，Laravel 框架中包含的 `users` 資料表遷移已經包含此欄位，因此，您所需要做的就是進行資料庫遷移：

```shell
php artisan migrate
```

<a name="verification-routing"></a>
## 路由

為了正確實作電子郵件驗證，需要定義三個路由。首先，需要一個路由來向用戶顯示一個通知，他們應該點擊 Laravel 在註冊後發送給他們的驗證電子郵件中的電子郵件驗證連結。

其次，需要一個路由來處理用戶點擊電子郵件中的電子郵件驗證連結時產生的請求。

最後，如果用戶不小心丟失了第一個驗證連結，則需要重新發送驗證連結的路由。

<a name="the-email-verification-notice"></a>
### 電子郵件驗證說明

如前所述，要定義一個路由能夠返回一個視圖指示用戶在註冊後點擊 Laravel 透過電子郵件發送給他們的電子郵件驗證連結。當用戶嘗試訪問應用程式的其他部分而不先驗證其電子郵件地址時，將會向用戶顯示此視圖。請記住，只要您的 `App\Models\User` 模型實現了 `MustVerifyEmail` 介面，連結就會自動透過電子郵件發送給用戶:

    Route::get('/email/verify', function () {
        return view('auth.verify-email');
    })->middleware('auth')->name('verification.notice');

返回電子郵件驗證通知的路由應命名為 `verification.notice`。為路由命名為此名稱很重要，因為如果用戶沒有驗證他們的電子郵件地址，[Laravel 中內建的](#protecting-routes) `verified` 中介層將會自動重新導向到該路由名稱。

> **Note**  
> 自行實作電子郵件驗證時，需要自己定義驗證通知視圖的內容。如果您想要包含所有必要的身份驗證和驗證視圖的基本架構，請查看[Laravel 應用程式入門套件](/docs/{{version}}/starter-kits)。
<a name="the-email-verification-handler"></a>
### 電子郵件驗證的處理程式

接下來，我們需要定義一個路由來處理當用戶點擊透過電子郵件發送給他們的電子郵件驗證連結時生成的請求。這個路由要被命名為 `verification.verify` 且被分配給 `auth` 和 `signed` 中介層:

    use Illuminate\Foundation\Auth\EmailVerificationRequest;

    Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
        $request->fulfill();

        return redirect('/home');
    })->middleware(['auth', 'signed'])->name('verification.verify');

在繼續之前，讓我們仔細看看這個路由。首先，您會注意到我們使用的是 `EmailVerificationRequest` 請求型態，而不是典型的 `Illuminate\Http\Request` 執行個體。`EmailVerificationRequest` 是個被包含在 Laravel 的[表單請求](/docs/{{version}}/validation#form-request-validation)。此請求將自動負責驗證請求的 `id` 和 `hash` 參數.

接下來，我們可以直接在請求上呼叫 `fulfill` 方法。此方法會對經過身份驗證的用戶呼叫 `markEmailAsVerified` 方法並分派 `Illuminate\Auth\Events\Verified` 事件。`markEmailAsVerified` 方法可通過 `Illuminate\Foundation\Auth\User` 基底類別用於預設的 `App\Models\User` 模型。當用戶的電子郵件地址被驗證後，您可以將他們重新導向到任何您想要的位置。

<a name="resending-the-verification-email"></a>
### 重新傳送電子郵件驗證

有時，用戶可能會放錯或不小心刪除電子郵件地址驗證電子郵件。為了因應這種情況，您可能希望定義一個路由允許用戶請求重新發送驗證電子郵件。您可以通過在[驗證通知視圖](#the-email-verification-notice)中放置一個簡單的表單提交按鈕來向此路由發出請求:

    use Illuminate\Http\Request;

    Route::post('/email/verification-notification', function (Request $request) {
        $request->user()->sendEmailVerificationNotification();

        return back()->with('message', 'Verification link sent!');
    })->middleware(['auth', 'throttle:6,1'])->name('verification.send');

<a name="protecting-routes"></a>
### 受保護的路由

[路由中介層](/docs/{{version}}/middleware)可用於僅允許經過驗證的用戶訪問給定路由。 Laravel 附帶了一個 `verified` 中介層，它引用了 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 類別。由於此中介層已註冊在應用程式的 HTTP 內核中，因此您要做的僅僅是將中介層附加到路由定義中:

    Route::get('/profile', function () {
        // Only verified users may access this route...
    })->middleware('verified');

如果未經驗證的用戶嘗試訪問已分配此中介層的路由，他們將自動被重新導向到 `verification.notice` [命名路由](/docs/{{version}}/routing#named-routes)中。

<a name="customization"></a>
## 自定

<a name="verification-email-customization"></a>
#### 自訂電子郵件驗證

雖然預設的電子郵件驗證通知應該能夠滿足大多數應用程式的要求，但 Laravel 允許您自定電子郵件驗證郵件訊息。

首先，傳遞閉包給由 `Illuminate\Auth\Notifications\VerifyEmail` 通知所提供的 `toMailUsing` 方法。該閉包會收到收到該通知的模型執行個體以及用戶必須訪問以驗證其電子郵件地址的簽名電子郵件驗證 URL 且閉包會返回一個 `Illuminate\Notifications\Messages\MailMessage` 的執行個體。通常，您應該從應用程式的 `App\Providers\AuthServiceProvider` 類別中的 `boot` 方法呼叫 `toMailUsing` 方法:

    use Illuminate\Auth\Notifications\VerifyEmail;
    use Illuminate\Notifications\Messages\MailMessage;

    /**
     * Register any authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        // ...

        VerifyEmail::toMailUsing(function ($notifiable, $url) {
            return (new MailMessage)
                ->subject('Verify Email Address')
                ->line('Click the button below to verify your email address.')
                ->action('Verify Email Address', $url);
        });
    }

> **Note**  
> 要了解更多有關郵件通知的資訊，請參閱[郵件通知說明文件](/docs/{{version}}/notifications#mail-notifications)。
<a name="events"></a>
## 事件

使用 [Laravel 應用程式入門套件](/docs/{{version}}/starter-kits)時，Laravel 在電子郵件驗證過程中分派[多個事件](/docs/{{version}}/events)。如果您正在為您的應用程式手動處理電子郵件驗證，您可能會希望在驗證完成後手動分派這些事件。您可以在應用程式的 `EventServiceProvider` 中將監聽器附加到這些事件:

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Auth\Events\Verified' => [
            'App\Listeners\LogVerifiedUser',
        ],
    ];
