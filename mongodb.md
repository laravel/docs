# MongoDB

- [Introduction](#introduction)
- [Installation](#installation)
    - [Starting a MongoDB server](#starting-a-mongodb-server)
    - [MongoDB Driver](#mongodb-driver)
    - [Install the Laravel MongoDB package](#install-the-laravel-mongodb-package)
- [Configuration](#configuration)
- [Features](#features)

<a name="introduction"></a>
## Introduction

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb) is one of the most popular NoSQL document-oriented database, used for its high write load (useful for analytics or IoT) and high availability (easy to set replica sets with automatic failover). It can also shard the database easily for horizontal scalability and has a powerful query language for doing aggregation, text search or geospatial queries. Instead of storing data in tables of rows or columns like SQL databases, each record in a MongoDB database is a document described in BSON, a binary representation of the data. Applications can then retrieve this information in a JSON format. It supports a wide variety of data types, including documents, arrays, embedded documents, and binary data.

Before using MongoDB with Laravel, we recommend installing and using the `mongodb/laravel-mongodb` package via Composer. While MongoDB is natively supported by PHP through the MongoDB driver, the [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) package provides a richer integration with Eloquent and other Laravel features.

```shell
composer require mongodb/laravel-mongodb
```

<a name="installation"></a>
## Installation

<a name="starting-a-mongodb-server"></a>
#### Starting a MongoDB server

The MongoDB Community Server can be used to create a Laravel application. It is available for installation in Windows, macOS, Linux, or as Docker container. Read how to [Install MongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/).

The connection string for the MongoDB server can be set in the `.env` file:

```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=laravel_app
```

For hosting MongoDB in the cloud, consider using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
To access a MongoDB Atlas cluster locally from your application, you will need to [add your own IP address in the cluster's network settings](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) to the project's IP Access List.

The connection string for MongoDB Atlas can be set in the `.env` file:

```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority
MONGODB_DATABASE=laravel_app
```

<a name="mongodb-driver"></a>
#### MongoDB Driver

To connect to a MongoDB database, the `mongodb` PHP extension is required. This extension can be installed using PECL:

```shell
pecl install mongodb
```

Read the [MongoDB PHP extension installation instructions](https://www.php.net/manual/en/mongodb.installation.php) for more information.

<a name="install-the-laravel-mongodb-package"></a>
#### Install the Laravel MongoDB package

Use Composer to install the Laravel MongoDB package:

```shell
composer require mongodb/laravel-mongodb
```

> [!NOTE]  
> This installation of the package will fail if the `mongodb` PHP extension is not installed. The PHP configuration can differ between the CLI and the web server, so ensure the extension is enabled in both configurations.

<a name="configuration"></a>
## Configuration

You may configure your MongoDB connection via the `config/database.php` configuration file.
Within this file, you can add a `mongodb` connection using the `mongodb` driver:

```php
'connections' => [
    'mongodb' => [
        'driver' => 'mongodb',
        'dsn' => env('MONGODB_URI', 'mongodb://localhost:27017'),
        'database' => env('MONGODB_DATABASE', 'laravel_app'),
    ],
],
```

<a name="features"></a>
## Features

Once your configuration is complete, you can use the `mongodb` connection in your application:

- [Using Eloquent](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/), models can be stored in MongoDB collections. In addition to the standard Eloquent features, the Laravel MongoDB package provides additional features such as embedded relationships. The package also provides direct access to the MongoDB driver, which can be used to execute operations such as raw queries and aggregation pipelines.
- [Write complex queries](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) using the query builder.
- [Using the Cache](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/), the `mongodb` cache driver is optimized to use MongoDB features such as TTL indexes to automatically clear expired cache entries.
- Using the Session with Laravel's `cache` and the `mongodb` cache driver. 
- [Using the Queue](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/) with the `mongodb` queue driver.
- [Storing files in GridFS](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/gridfs/), by way of the [GridFS Adapter for Flysystem](https://flysystem.thephpleague.com/docs/adapter/gridfs/).
- Most third party packages using a database connection or Eloquent can be used with MongoDB.

Refer to the [**Quick Start**](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/) guide to connect a Laravel application to MongoDB, and perform read/write operations on the data.
