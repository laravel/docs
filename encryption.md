# 加密

- [介绍](#introduction)
- [基本用法](#basic-usage)

<a name="introduction"></a>
## 介绍

Laravel 透过 Mcrypt PHP 扩充套件提供功能强大的 AES 加密功能。

<a name="basic-usage"></a>
## 基本用法

#### 加密

	$encrypted = Crypt::encrypt('secret');

> **注意：** 请确保 `config/app.php` 文件中的 `key` 选项设置了 16, 24, 或 32 字符的随机字串，否则加密的数值不会安全。

#### 解密

	$decrypted = Crypt::decrypt($encryptedValue);

#### 设置密码与模式

您也可以使用加密器来设置密码和模式：

	Crypt::setMode('ctr');

	Crypt::setCipher($cipher);
