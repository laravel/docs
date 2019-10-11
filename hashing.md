# 雜湊

- [前言](#前言)
- [設定](#設定)
- [基本用法](#基本用法)

## 前言

Laravel 透過 `Hash` [facade](/docs/{{version}}/facades) 提供安全的 Bcrypt 與 Argon2 雜湊來保存使用者密碼。如果你在目前的應用當中使用內建的 `LoginController` 與 `RegisterController` 類別，它將預設使用 Bcrypt 加密進行註冊跟驗證。

> {tip} 由於 Bcrypt 的 "加密係數（word fator）" 可以任意調整，使它成為最好的加密選擇。這代表每一次加密的時間可以隨著硬體設備的升級而加長。

## 設定

您的應用程式預設的雜湊方法被設定在 `config/hashing.php` 檔案。目前支援三種方法: [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt) 、 [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i 與 Argon2id 的變種).

> {note} Argon2i 需要 PHP 7.2.0 或更高的版本、Argon2id 需要 PHP 7.3.0 或更高的版本。

## 基本用法

你可以透過呼叫 `Hash` facade 的 `make` 方法加密一個密碼：

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Hash;

    class UpdatePasswordController extends Controller
    {
        /**
         * Update the password for the user.
         *
         * @param  Request  $request
         * @return Response
         */
        public function update(Request $request)
        {
            // Validate the new password length...

            $request->user()->fill([
                'password' => Hash::make($request->newPassword)
            ])->save();
        }
    }

#### 調整 Bcrypt 的加密係數

如果您使用的是 Bcrypt 演算法，`make` 方法允許你透過 `rounds` 選項來設置加密係數。但對大多數應用程式來說使用預設值是可接受的：

    $hashed = Hash::make('password', [
        'rounds' => 12
    ]);

#### 調整 Argon2 的加密係數

如果您使用的是 Bcrypt 演算法，`make` 方法允許你透過 `memory`、`time` 及 `threads` 選項來設置加密係數。但對大多數應用程式來說使用預設值是可接受的：

    $hashed = Hash::make('password', [
        'memory' => 1024,
        'time' => 2,
        'threads' => 2,
    ]);

> {tip} 關於選項的更多資訊，請參照 [PHP官方手冊](https://secure.php.net/manual/en/function.password-hash.php)。

#### 根據雜湊值驗證密碼

`check` 方法允許你透過一個給定的純字串跟雜湊值進行驗證。如果你目前正使用 [Laravel 內建的](/docs/{{version}}/authentication) `LoginController` ，你可能不需要直接使用該方法，它已經包含在控制器當中並且自動呼叫。

    if (Hash::check('plain-text', $hashedPassword)) {
        // The passwords match...
    }

#### 驗證密碼是否須重新加密

`needsRehash` 函式允許你檢查已加密密碼，它所使用的加密係數是否被變更：

    if (Hash::needsRehash($hashed)) {
        $hashed = Hash::make('plain-text');
    }
