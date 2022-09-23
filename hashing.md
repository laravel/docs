# 雜湊

- [簡介](#introduction)
- [設定](#configuration)
- [基本用法](#basic-usage)
    - [雜湊密碼](#hashing-passwords)
    - [驗證密碼是否符合雜湊](#verifying-that-a-password-matches-a-hash)
    - [判斷是否需要重新雜湊密碼](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
## 簡介

Laravel 的 `Hash` [facade](/docs/{{version}}/facades)提供了安全的 Brcypt 和 Argon2 雜湊，用以來儲存使用者的密碼。若使用 [Laravel 專案入門套件](/docs/{{version}}/starter-kits)，則會預設 Brcypt 來註冊與登入。

Brcypt 是雜湊密碼的一個不錯選擇，因為他的「加密係數」（Work Factor）是可以調整的，這代表，隨著硬體功能的提升，我們也能調整雜湊所需的時間。在雜湊密碼時，慢即是好。若演算法需要更多時間來在雜湊密馬，惡意使用者要產生「彩虹表」的時間也就更長。彩虹表就是包含所有可能的字串雜湊值的表， 可以被用來暴力破解密碼。

<a name="configuration"></a>
## 組態設定（Configuration）

專案中預設的雜湊驅動（Driver）設定在專案中的 `config/hashing.php` 設定檔中。目前有支援多個驅動（Driver）： [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt) &nbsp; 和 &nbsp; [Argon2](https://en.wikipedia.org/wiki/Argon2)（Argon2i 與 Argon2id 變形）

<a name="basic-usage"></a>
## 基本用法

<a name="hashing-passwords"></a>
### 雜湊密碼

可以使用 `Hash` facade 的 `make`  方法了來雜湊密碼：

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Hash;

    class PasswordController extends Controller
    {
        /**
         * Update the password for the user.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function update(Request $request)
        {
            // Validate the new password length...

            $request->user()->fill([
                'password' => Hash::make($request->newPassword)
            ])->save();
        }
    }

<a name="adjusting-the-bcrypt-work-factor"></a>
#### 調整 Bcrypt 的加密係數（Work Factor）

如果使用 Bcrypt 的演算法，可使用 `rounds` 選項來在 `make` 方法中控制 Bcrypt 的加密係數（Work Factor）。不過， Laravel 所控制的預設加密係數（Work Factor）對於大多數專案來說應是可以接受的值：

    $hashed = Hash::make('password', [
        'rounds' => 12,
    ]);

<a name="adjusting-the-argon2-work-factor"></a>
#### 調整 Argon2 的加密係數（Work Factor）

如果使用 Argon2 的演算法，可使用 `memory` 、 `time`、 和 `threads` 選項在 `make` 方法中控制 Argon2 的加密係數（Work Factor）。不過， Laravel 所控制的預設加密係數（Work Factor）對大多數專案來說應是可以接受的值：

    $hashed = Hash::make('password', [
        'memory' => 1024,
        'time' => 2,
        'threads' => 2,
    ]);

> **注意**  
> 有關這些選項的詳細資訊，請參照 [PHP 官方文件中的 Argon 雜湊說明](https://secure.php.net/manual/en/function.password-hash.php)

<a name="verifying-that-a-password-matches-a-hash"></a>
### 驗證密碼是否符合雜湊

`Hash` facade 的 `check` 方法可以用來驗證給定的純文字字串是否對應給定的雜湊： 

    if (Hash::check('plain-text', $hashedPassword)) {
        // The passwords match...
    }

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 判斷是否需要重新雜湊密碼

`Hash` facade 的 `needsRehash` 方法可以用來判斷自從該密碼被雜湊以來 Hash 程式的雜湊密碼（Work Factor）是否有經過更改。有的專案會在網站的身份驗證過程中做這項檢查：

    if (Hash::needsRehash($hashed)) {
        $hashed = Hash::make('plain-text');
    }
