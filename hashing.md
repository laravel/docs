# 雜湊

- [簡述](#introduction)
- [基本用法](#basic-usage)

<a name="introduction"></a>
## 簡述

在 Laravel `Hash` 內儲存的密碼使用 Bcrypt 加密方式。
如果您在 Laravel 使用認證控制器，控制器也會幫助未使用 Bcrypt 加密的密碼進行 Bcrypt 驗證。
同樣，在使用者註冊服務內 Laravel 也提供 `bcrypt` 密碼加密的方式儲存密碼。

<a name="basic-usage"></a>
## 基本用法

#### 使用 Bcrypt 加密密碼

	$password = Hash::make('secret');

你也可直接使用 bcrypt 的函數

	$password = bcrypt('secret');

#### 對加密的密碼進行驗證

	if (Hash::check('secret', $hashedPassword))
	{
		// The passwords match...
	}

#### 檢查密碼是否需要重新加密

	if (Hash::needsRehash($hashed))
	{
		$hashed = Hash::make('secret');
	}
