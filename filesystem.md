# 檔案系統 / 雲端儲存

- [簡介](#introduction)
- [設定檔](#configuration)
- [基本用法](#basic-usage)

<a name="introduction"></a>
## 簡介

Laravel 有很棒的檔案系統抽象層，是基於 Frank de Jonge 的 [Flysystem](https://github.com/thephpleague/flysystem) 套件。 Laravel 整合的 Flysystem 提供了簡單的介面，可以操作本地端空間、 Amazon S3 、 Rackspace Cloud Storage 。更好的是，它可以非常簡單的切換不同儲存方式，但仍使用相同的 API 操作！

<a name="configuration"></a>
## 設定檔

檔案系統的設定檔放在 `config/filesystems.php` 。在這個檔案內你可以設定所有的「硬碟」。每個硬碟代表一種儲存方式和地點。預設的設定檔內已經包含了所有儲存方式的範例。所以只要修改儲存設定和認證即可！

在使用 S3 或 Rackspace 之前，你必須先用 Composer 安裝相對應的套件：

- Amazon S3: `league/flysystem-aws-s3-v2 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

當然，你可以加入任意數量的硬碟設定檔，甚至設定多個硬碟都使用同一種儲存方式。

使用本地端空間時，要注意所有的操作路徑都是相對於設定檔裡 `local` 的 `root` ，預設的路徑是 `storage/app` 。因此下列的操作將會儲存一個檔案在 `storage/app/file.txt` ：

	Storage::disk('local')->put('file.txt', 'Contents');

<a name="basic-usage"></a>
## 基本用法

可以用 `Storage` facade 操作所有寫在設定檔裡的硬碟。或者是，你也可以將 `Illuminate\Contracts\Filesystem\Factory` 型別暗示寫到任何類別裡，經由 [IoC container](/docs/5.0/container) 解析。

#### 取得一個特定硬碟

	$disk = Storage::disk('s3');

	$disk = Storage::disk('local');

#### 確認檔案是否存在

	$exists = Storage::disk('s3')->exists('file.jpg');

#### 使用預設硬碟呼叫方法

	if (Storage::exists('file.jpg'))
	{
		//
	}

#### 取得檔案內容

	$contents = Storage::get('file.jpg');

#### 設定檔案內容

	Storage::put('file.jpg', $contents);

#### 附加內容到檔案結尾

	Storage::prepend('file.log', 'Prepended Text');

#### 加入內容到檔案開頭

	Storage::append('file.log', 'Appended Text');

#### 刪除檔案

	Storage::delete('file.jpg');

	Storage::delete(['file1.jpg', 'file2.jpg']);

#### 複製檔案到新的路徑

	Storage::copy('old/file1.jpg', 'new/file1.jpg');

#### 移動檔案到新的路徑

	Storage::move('old/file1.jpg', 'new/file1.jpg');

#### 取得檔案大小

	$size = Storage::size('file1.jpg');

#### 取得最近修改時間 (UNIX)

	$time = Storage::lastModified('file1.jpg');

#### 取得目錄下所有檔案

	$files = Storage::files($directory);

	// Recursive...
	$files = Storage::allFiles($directory);

#### 取得目錄下所有子目錄

	$directories = Storage::directories($directory);

	// Recursive...
	$directories = Storage::allDirectories($directory);

#### 建立目錄

	Storage::makeDirectory($directory);

#### 刪除目錄

	Storage::deleteDirectory($directory);
