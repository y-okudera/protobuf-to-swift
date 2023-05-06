# protobuf-to-swift
Python project to generate Swift files from proto2 files with mustache template.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

protobuf-to-swift is a library for generating Swift files from Protocol Buffers. This library is designed to make it easy to generate Swift networking.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Proto Examples](#proto-examples)
- [License](#license)
- [Contributing](#contributing)

## Installation

This library requires Python 3.10 or higher. Install using the following command:

```bash
make bootstrap project
```

## Usage

Store the proto files in the /proto directory and generate Swift files using the following command:

```bash
make gen
```

## Proto Examples

Store the proto files as follows:

```
protobuf-to-swift/
├── proto/
│   ├── google/
│   │   └── ...
│   ├── model/
│   │   └── yourModel.proto
│   ├── service/
│   │   └── yourService.proto
│   ├── view/
│   │   └── yourView.proto
│   └── your.proto
```

At the beginning of the proto file, add import as follows:

```
import "google/api/annotations.proto";
```

Add option (google.api.http) to the rpc definition and define the HTTP method and path.
For example, to set the Login RPC to POST /login, do the following:

```
rpc Login (LoginRequest) returns (Empty) {
  option (google.api.http) = {
    post: "/login"
  };
}
```

## Advanced Usage

- You can customize the output Swift files by editing mustache in templates/mustache.

- By editing the templates/swift/Foundation directory, you can edit Swift files to be included in the Swift Package.

## License

This library is published under the MIT License. For details, see the [LICENSE](LICENSE) file.

## Contributing

We welcome contributions in any form, such as bug reports, feature requests, and pull requests. Details will be provided in CONTRIBUTING.md. (TBD)
