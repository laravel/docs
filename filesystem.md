# 檔案系統與雲端儲存

- [簡介](#introduction)
- [設定](#configuration)
- [基本用法](#basic-usage)
    - [取得磁碟實體](#obtaining-disk-instances)
    - [檔案提取](#retrieving-files)
    - [檔案儲存](#storing-files)
    - [檔案刪除](#deleting-files)
    - [目錄](#directories)
- [自訂檔案系統](#custom-filesystems)

<a name="introduction"></a>
## 簡介

感謝 Frank de Jonge 的 [Flysystem](https://github.com/thephpleague/flysystem) 套件，使得 Laravel 能提供強大的檔案抽象層。Laravel 整合的 Flysystem 以各種驅動（driver）提供本地端磁碟系統、Amazon S3、以及 Rackspace 雲端儲存。並且能像使用 API 一般，輕易的切換這些儲存方式來面對各種系統。
Laravel provides a powerful filesystem abstraction thanks to the wonderful [Flysystem](https://github.com/thephpleague/flysystem) PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple to use drivers for working with local filesystems, Amazon S3, and Rackspace Cloud Storage. Even better, it's amazingly simple to switch between these storage options as the API remains the same for each system.

<a name="configuration"></a>
## 設定

檔案系統設定檔位於 `config/filesystems.php`。該檔案能讓你設定所有的「磁碟（disk）」。每一個磁碟代表一種獨特的儲存驅動以及儲存位置。各種支援驅動範例已包含在檔案中。僅需要簡單的根據你的偏好配置及憑證設定進行變更即可。
The filesystem configuration file is located at `config/filesystems.php`. Within this file you may configure all of your "disks". Each disk represents a particular storage driver and storage location. Example configurations for each supported driver is included in the configuration file. So, simply modify the configuration to reflect your storage preferences and credentials.

當然，你可以設定多組磁碟，甚至使用相同驅動。
Of course, you may configure as many disks as you like, and may even have multiple disks that use the same driver.

#### 本地端驅動

當使用 `local` 驅動，所有的操作是相對於設定檔中的 `root` 目錄設定進行。該目錄預設是 `storage/app` 目錄。因此下列的方法將把檔案儲存在 `storage/app/file.txt`：
When using the `local` driver, note that all file operations are relative to the `root` directory defined in your configuration file. By default, this value is set to the `storage/app` directory. Therefore, the following method would store a file in `storage/app/file.txt`:

    Storage::disk('local')->put('file.txt', 'Contents');

#### 其他驅動的預先需求

在使用 S3 或 Rackspace 驅動之前，你需要透過 Composer 安裝適當套件：
Before using the S3 or Rackspace drivers, you will need to install the appropriate package via Composer:

- Amazon S3: `league/flysystem-aws-s3-v3 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

<a name="basic-usage"></a>
## 基本用法

<a name="obtaining-disk-instances"></a>
### 獲得磁碟實體

`Storage` facade 用於跟任何已設定的磁碟進行互動。舉例來說，你可以使用 facade 的 `put` 方法將一張頭像儲存到預設磁碟。而當使用 `Storage` facade 呼叫任一方法而未先呼叫 `disk` 方法，預設磁碟將自動傳遞給該方法。
The `Storage` facade may be used to interact with any of your configured disks. For example, you may use the `put` method on the facade to store an avatar on the default disk. If you call methods on the `Storage` facade without first calling the `disk` method, the method call will automatically be passed to the default disk:

    <?php

    namespace App\Http\Controllers;

    use Storage;
    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Update the avatar for the given user.
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function updateAvatar(Request $request, $id)
        {
            $user = User::findOrFail($id);

            Storage::put(
                'avatars/'.$user->id,
                file_get_contents($request->file('avatar')->getRealPath())
            );
        }
    }

當使用多個磁碟，你可以透過使用 `Storage` facade 的 `disk` 方法存取特定磁碟。當然，你也可以使用方法鏈結（chain methods）對磁碟使用各種執行方法。
When using multiple disks, you may access a particular disk using the `disk` method on the `Storage` facade. Of course, you may continue to chain methods to execute methods on the disk:

    $disk = Storage::disk('s3');

    $contents = Storage::disk('local')->get('file.jpg')

<a name="retrieving-files"></a>
### 檔案提取

`get` 方法提取給定檔案的內容，該檔案的原始字串內容將透過該方法取得：
The `get` method may be used to retrieve the contents of a given file. The raw string contents of the file will be returned by the method:

    $contents = Storage::get('file.jpg');

`exists` 方法判定給定的檔案是否存於磁碟上：
The `exists` method may be used to determine if a given file exists on the disk:

    $exists = Storage::disk('s3')->exists('file.jpg');

#### 檔案資訊

`size` 方法取得檔案的大小並以 bytes 顯示：
The `size` method may be used to get the size of the file in bytes:

    $size = Storage::size('file1.jpg');

`lastModified` 方法回傳檔案的最後修改時間並以 UNIX 時間戳記顯示：
The `lastModified` method returns the UNIX timestamp of the last time the file was modified:

    $time = Storage::lastModified('file1.jpg');

<a name="storing-files"></a>
### 檔案儲存

`put` 方法儲存單一檔案於磁碟上。你能同時傳遞 PHP 的 `resource` 給 `put` 方法，它將使用檔案系統底層的 stream 支援。強烈建議使用 stream 處理大型檔案。
The `put` method may be used to store a file on disk. You may also pass a PHP `resource` to the `put` method, which will use Flysystem's underlying stream support. Using streams is greatly recommended when dealing with large files:

    Storage::put('file.jpg', $contents);

    Storage::put('file.jpg', $resource);

`copy` 方法複製一個存在的檔案到目前磁碟的新位置。
The `copy` method may be used to move an existing file to a new location on the disk:

    Storage::copy('old/file1.jpg', 'new/file1.jpg');
    
`move` 方法移動一個存在的檔案到新位置。
The `move` method may be used to move an existing file to a new location:

    Storage::move('old/file1.jpg', 'new/file1.jpg');

#### 插入到檔案

`prepend` 及 `append` 方法允許你輕易的插入內容到一個檔案的開頭或結尾：
The `prepend` and `append` methods allow you to easily insert content at the beginning or end of a file:

    Storage::prepend('file.log', 'Prepended Text');

    Storage::append('file.log', 'Appended Text');

<a name="deleting-files"></a>
### 檔案刪除

`delete` 方法接受一個檔案名稱或者一個檔案名稱陣列，用以移除磁碟上的檔案：
The `delete` method accepts a single filename or an array of files to remove from the disk:

    Storage::delete('file.jpg');

    Storage::delete(['file1.jpg', 'file2.jpg']);

<a name="directories"></a>
### 目錄

#### 取得單一目錄內所有檔案

`files` 方法回傳所有給定目錄下的檔案陣列。如果你希望回傳包含給定目錄下所有子目錄的檔案，你可以使用 `allFiles` 方法。
The `files` method returns an array of all of the files in a given directory. If you would like to retrieve a list of all files within a given directory including all sub-directories, you may use the `allFiles` method:

    $files = Storage::files($directory);

    $files = Storage::allFiles($directory);

#### 取得單一目錄內所有目錄

`directories` 方法回傳所有給定目錄下的目錄陣列。另外，你也可以使用 `allDirectories` 方法取得給定目錄下子目錄以及子目錄所包含的目錄。
The `directories` method returns an array of all the directories within a given directory. Additionally, you may use the `allDirectories` method to get a list of all directories within a given directory and all of its sub-directories:

    $directories = Storage::directories($directory);

    // Recursive...
    $directories = Storage::allDirectories($directory);

#### 建立目錄

`makeDirectory` 方法將建立給定的目錄，包括任何所需的子目錄。
The `makeDirectory` method will create the given directory, including any needed sub-directories:

    Storage::makeDirectory($directory);

#### 刪除目錄

最後，`deleteDirectory` 方法能移除磁碟上的單一目錄以及所包含的全部檔案。
Finally, the `deleteDirectory` may be used to remove a directory, including all of its files, from the disk:

    Storage::deleteDirectory($directory);

<a name="custom-filesystems"></a>
## 自訂檔案系統

Laravel 整合的 Flysystem 提供許多預設的驅動；然而 Flysystem 本身提供了不僅僅這些，還包括其他儲存系統的接口（adapter）。你能在 Laravel 的應用當中通過建立新的驅動使用這些額外的接口。
Laravel's Flysystem integration provides drivers for several "drivers" out of the box; however, Flysystem is not limited to these and has adapters for many other storage systems. You can create a custom driver if you want to use one of these additional adapters in your Laravel application.

為了建構一個自訂的磁碟系統，你將需要建立一個像是 `DropboxServiceProvider` 的 [服務提供者](/docs/{{version}}/providers)。並在該提供者的 `boot` 方法使用 `Storage` facade 的 `extend` 方法自訂你的驅動。
In order to set up the custom filesystem you will need to create a [service provider](/docs/{{version}}/providers) such as `DropboxServiceProvider`. In the provider's `boot` method, you may use the `Storage` facade's `extend` method to define the custom driver:

    <?php

    namespace App\Providers;

    use Storage;
    use League\Flysystem\Filesystem;
    use Dropbox\Client as DropboxClient;
    use Illuminate\Support\ServiceProvider;
    use League\Flysystem\Dropbox\DropboxAdapter;

    class DropboxServiceProvider extends ServiceProvider
    {
        /**
         * Perform post-registration booting of services.
         *
         * @return void
         */
        public function boot()
        {
            Storage::extend('dropbox', function($app, $config) {
                $client = new DropboxClient(
                    $config['accessToken'], $config['clientIdentifier']
                );

                return new Filesystem(new DropboxAdapter($client));
            });
        }

        /**
         * Register bindings in the container.
         *
         * @return void
         */
        public function register()
        {
            //
        }
    }

`extend` 方法的第一個參數是你的驅動名稱，第二個參數則是一個接受 `$app` 及 `$config` 變數的閉包。該閉包必須回傳 `League\Flysystem\Filesystem` 的實體。`$config` 變數包含了定義在 `config/filesystems.php` 對指定磁碟的設定。
The first argument of the `extend` method is the name of the driver and the second is a Closure that receives the `$app` and `$config` variables. The resolver Closure must return an instance of `League\Flysystem\Filesystem`. The `$config` variable contains the values defined in `config/filesystems.php` for the specified disk.

當你透過建立服務提供者註冊該擴展，你便能在 `config/filesystem.php` 設定檔中使用 `dropbox` 驅動。
Once you have created the service provider to register the extension, you may use the `dropbox` driver in your `config/filesystem.php` configuration file.
