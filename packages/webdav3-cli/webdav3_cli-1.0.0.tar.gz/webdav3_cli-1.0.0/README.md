# webdav3-cli

Simple command-line interface for interacting with a WebDAV server.

This was tested and developed against the WebDAV interface for a [Redmine](https://www.redmine.org/) server.

## Usage

### Configuring

You can configure a set of default values for the optional arguments using the `config` command 

#### Examples:
`webdav3 config set hostname="http://client.openjaus.net/dmsf/webdav/openjaus4-sdk-cpp"`

`webdav3 config set user={username}`

`webdav3 config set pass={password}`


### Uploading files

Files can be uploaded to the WebDAV server using the `upload` command

#### Examples:
`webdav3 upload {local_path} {remote_path} --hostname {server address} --root "/dmsf/webdav" --user {username} --pass {password}`

`webdav3 upload {local_path} {remote_path}`
