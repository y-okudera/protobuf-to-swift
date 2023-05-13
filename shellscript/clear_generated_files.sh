#!/bin/sh

# *_pb2.py削除
find ./protobuf_to_swift -type f -name "*_pb2.py" | xargs rm -rf
find ./protobuf_to_swift -type d -empty -delete

# proto_reader.py削除
rm -rf ./protobuf_to_swift/proto_reader.py

# ./outputディレクトリ削除
rm -rf ./output
mkdir ./output
touch ./output/.gitkeep
