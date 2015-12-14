# 檔案系統與雲端儲存

- [簡介](#introduction)
- [設定](#configuration)
- [基本用法](#basic-usage)
    - [取得磁碟實體](#obtaining-disk-instances)
    - [提取檔案](#retrieving-files)
    - [儲存檔案](#storing-files)
    - [刪除檔案](#deleting-files)
    - [目錄](#directories)
- [自訂檔案系統](#custom-filesystems)

<a name="introduction"></a>
## 簡介

Laravel 強大的檔案抽象層得力於 Frank de Jonge 的 [Flysystem](https://github.com/thephpleague/flysystem) 套件。Laravel 的 flysystem 整合以各種驅動（driver）提供本地端磁碟系統、Amazon S3、以及 Rackspace 雲端儲存。並且能像使用 API 一般，輕易的切換這些儲存方式來面對各式系統。

<a name="configuration"></a>
## 設定

檔案系統設定檔位於 `config/filesystems.php`。該檔案能讓你設定所有的「磁碟（disk）」。每個磁碟代表一種獨特的儲存驅動以及儲存位置。各種支援驅動範例已包含在其中，僅需要簡單的根據你的偏好配置及憑證設定進行變更即可。

當然，你可以設定多組磁碟，甚至使用相同驅動。

#### 本地端驅動

當使用 `local` 驅動，所有的操作是相對於設定檔中的 `root` 目錄設定進行。該目錄預設是 `storage/app`。因此下列方法將把檔案儲存在 `storage/app/file.txt`：

    Storage::disk('local')->put('file.txt', 'Contents');

#### 其他驅動的預先需求

在使用 S3 或 Rackspace 驅動之前，你需要透過 Composer 安裝適當套件：

- Amazon S3: `league/flysystem-aws-s3-v3 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

<a name="basic-usage"></a>
## 基本用法

<a name="obtaining-disk-instances"></a>
### 獲得磁碟實體

`Storage` facade 用於對任何已設定的磁碟進行互動。舉例來說，你可以使用 facade 的 `put` 方法將一張頭像儲存到預設磁碟。當使用 `Storage` facade 呼叫任一方法而未先呼叫 `disk` 方法，預設磁碟將自動傳遞給該方法。

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

面對使用多個磁碟時，你可以透過 `Storage` facade 的 `disk` 方法存取特定磁碟。當然，你也可以使用方法鏈結（chain methods）對磁碟使用各種執行方法。

    $disk = Storage::disk('s3');

    $contents = Storage::disk('local')->get('file.jpg')

<a name="retrieving-files"></a>
### 提取檔案

`get` 方法提取給定檔案的內容，該檔案的原始字串內容將透過該方法取得：

    $contents = Storage::get('file.jpg');

`has` 方法可以用於判定給定的檔案是否存於磁碟上：

    $exists = Storage::disk('s3')->has('file.jpg');

#### 檔案資訊

`size` 方法取得檔案的大小並以 bytes 顯示：

    $size = Storage::size('file1.jpg');

`lastModified` 方法回傳檔案的最後修改時間並以 UNIX 時間戳記顯示：

    $time = Storage::lastModified('file1.jpg');

<a name="storing-files"></a>
### 儲存檔案

`put` 方法儲存單一檔案於磁碟上。你能同時傳遞 PHP 的 `resource` 給 `put` 方法，它將使用檔案系統底層的 stream 支援。強烈建議使用 stream 處理大型檔案。

    Storage::put('file.jpg', $contents);

    Storage::put('file.jpg', $resource);

`copy` 方法用於複製一個存在的檔案到磁碟的新位置。

    Storage::copy('old/file1.jpg', 'new/file1.jpg');

`move` 方法被用於重新命名或是移動一個存在的檔案到新位置。

    Storage::move('old/file1.jpg', 'new/file1.jpg');

#### 插入到檔案

`prepend` 及 `append` 方法允許你輕易的插入內容到一個檔案的開頭或結尾：

    Storage::prepend('file.log', 'Prepended Text');

    Storage::append('file.log', 'Appended Text');

<a name="deleting-files"></a>
### 刪除檔案

`delete` 方法接受一個檔案名稱或檔案名稱陣列，用以移除磁碟上的檔案：

    Storage::delete('file.jpg');

    Storage::delete(['file1.jpg', 'file2.jpg']);

<a name="directories"></a>
### 目錄

#### 取得單一目錄內所有檔案

`files` 方法回傳給定目錄下的檔案陣列。如果你希望回傳包含給定目錄下所有子目錄的檔案，你可以使用 `allFiles` 方法。

    $files = Storage::files($directory);

    $files = Storage::allFiles($directory);

#### 取得單一目錄內所有目錄

`directories` 方法回傳給定目錄下的目錄陣列。另外，你也可以使用 `allDirectories` 方法取得給定目錄下子目錄以及子目錄所包含的目錄。

    $directories = Storage::directories($directory);

    // Recursive...
    $directories = Storage::allDirectories($directory);

#### 建立目錄

`makeDirectory` 方法將建立給定的目錄，包括任何所需的子目錄。

    Storage::makeDirectory($directory);

#### 刪除目錄

最後，`deleteDirectory` 方法能移除磁碟上的單一目錄以及所包含的全部檔案。

    Storage::deleteDirectory($directory);

<a name="custom-filesystems"></a>
## 自訂檔案系統

Laravel 整合的 Flysystem 提供許多預設的驅動；然而 Flysystem 本身提供了不僅僅這些，還包括其他儲存系統的接口（adapter）。你能在 Laravel 的應用當中通過建立新的驅動使用這些額外的接口。

為了建構一個自訂的磁碟系統，你將需要建立一個像是 `DropboxServiceProvider` 的 [服務提供者](/docs/{{version}}/providers)。並在該提供者的 `boot` 方法使用 `Storage` facade 的 `extend` 方法自訂你的驅動。

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

`extend` 方法的第一個參數是你的驅動名稱，第二個參數則是一個接受 `$app` 及 `$config` 變數的閉包。該閉包必須回傳 `League\Flysystem\Filesystem` 實例。`$config` 變數包含了定義在 `config/filesystems.php` 對指定磁碟的設定。

當你透過建立服務提供者註冊該擴展，你便能在 `config/filesystem.php` 設定檔中使用 `dropbox` 驅動。
