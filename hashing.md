# Hashing

- [简述](#introduction)
- [基本用法](#basic-usage)

<a name="introduction"></a>
## 简述

在 Laravel `Hash` 内保存的密码使用 Bcrypt 加密方式。
如果您在 Laravel 使用认证控制器，控制器也会帮助未使用 Bcrypt 加密的密码进行 Bcrypt 验证。
同样，在用户注册服务内 Laravel 也提供 `bcrypt` 密码加密的方式保存密码。

<a name="basic-usage"></a>
## 基本用法

####对 A 密码使用Bcrypt 加密

	$password = Hash::make('secret');

你也可直接使用 bcrypt 的 function

	$password = bcrypt('secret');

#### 对加密的 A 密码进行验证

	if (Hash::check('secret', $hashedPassword))
	{
		// The passwords match...
	}

#### 检查 A 密码是否需要重新加密

	if (Hash::needsRehash($hashed))
	{
		$hashed = Hash::make('secret');
	}
