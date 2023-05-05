// swift-tools-version: 5.7
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "RemoteDataSource",
    platforms: [
        .iOS(.v14),
    ],
    products: [
        .library(
            name: "RemoteDataSource",
            targets: ["RemoteDataSource"]
        ),
    ],
    dependencies: [
        .package(url: "https://github.com/ishkawa/APIKit", exact: "5.4.0"),
        .package(url: "https://github.com/apple/swift-protobuf", exact: "1.21.0"),
    ],
    targets: [
        .target(
            name: "RemoteDataSource",
            dependencies: [
                .product(name: "APIKit", package: "APIKit"),
                .product(name: "SwiftProtobuf", package: "swift-protobuf"),
            ]
        ),
        .testTarget(
            name: "RemoteDataSourceTests",
            dependencies: ["RemoteDataSource"]
        ),
    ]
)
