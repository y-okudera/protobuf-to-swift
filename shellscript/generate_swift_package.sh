#!/bin/sh

SWIFT_PACKAGE_PATH=$1
SWIFT_PACKAGE_NAME=`basename $1`
echo "SWIFT_PACKAGE_PATH: ${SWIFT_PACKAGE_PATH}"
echo "SWIFT_PACKAGE_NAME: ${SWIFT_PACKAGE_NAME}"

WORKING_DIR=${PWD}

API_REPOSITORY_DIR=${SWIFT_PACKAGE_PATH}/Sources/${SWIFT_PACKAGE_NAME}/Repository
API_REPOSITORY_OUTPUT_PATH_FORMAT=${API_REPOSITORY_DIR}/%sAPIRepository.swift
API_REPOSITORY_TEMPLATE_PATH=templates/mustache/swift/api_repository.swift.mustache

API_REQUEST_DIR=${SWIFT_PACKAGE_PATH}/Sources/${SWIFT_PACKAGE_NAME}/Request
API_REQUEST_OUTPUT_PATH_FORMAT=${API_REQUEST_DIR}/%s.swift
API_REQUEST_TEMPLATE_PATH=templates/mustache/swift/request.swift.mustache

# 前回生成したファイル、ディレクトリを削除
make clear

# *_pb2.py生成
cd proto
protoc --proto_path=. --python_out=../protobuf_to_swift *.proto model/* service/* view/* google/api/*

# カレントディレクトリを戻す
cd ${WORKING_DIR}

# proto_reader.py生成
pipenv run python proto_reader_generator/proto_reader_generator.py

# Repository, Requestディレクトリ生成
mkdir -p ${API_REPOSITORY_DIR} ${API_REQUEST_DIR}

# Swift Package生成
cd ${SWIFT_PACKAGE_PATH}
swift package init --name RemoteDataSource --type library

# カレントディレクトリを戻す
cd ${WORKING_DIR}

# 事前に用意したテンプレートのSwiftファイルをSwift Packageに追加する
cp -a ./templates/swift/Foundation ${SWIFT_PACKAGE_PATH}/Sources/${SWIFT_PACKAGE_NAME}/Foundation
cp -f ./templates/swift/Package.swift ${SWIFT_PACKAGE_PATH}/Package.swift

# Swiftファイル生成
pipenv run python protobuf_to_swift/protobuf_to_swift.py \
    ${API_REPOSITORY_OUTPUT_PATH_FORMAT} \
    ${API_REPOSITORY_TEMPLATE_PATH} \
    ${API_REQUEST_OUTPUT_PATH_FORMAT} \
    ${API_REQUEST_TEMPLATE_PATH}
