# 加密

- [介紹](#introduction)
- [基本用法](#basic-usage)

<a name="introduction"></a>
## 介紹

Laravel 透過 Mcrypt PHP 擴充套件提供功能強大的 AES 加密功能。

<a name="basic-usage"></a>
## 基本用法

#### 加密

	$encrypted = Crypt::encrypt('secret');

> **注意：** 請確保 `config/app.php` 檔案中的 `key` 選項設定了 16, 24, 或 32 字元的隨機字串，否則加密的數值不會安全。

#### 解密

	$decrypted = Crypt::decrypt($encryptedValue);

#### 設定密碼與模式

您也可以使用加密器來設置密碼和模式：

	Crypt::setMode('ctr');

	Crypt::setCipher($cipher);
