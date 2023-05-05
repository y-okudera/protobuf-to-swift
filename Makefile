.PHONY: help
help: ## ヘルプを表示します
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: bootstrap
bootstrap: ## 必要なツールのインストールを実行します
	brew install protobuf go swift-protobuf pipenv
	go install github.com/pseudomuto/protoc-gen-doc/cmd/protoc-gen-doc@latest
	npm install -g yarn

.PHONY: project
project: ## プロジェクトの設定をします
	yarn install
	pipenv install

.PHONY: gen
gen: ## Swiftファイルを生成します
	# 前回生成したファイル、ディレクトリを削除
	make clear

	# *_pb2.py生成
	cd proto; protoc --proto_path=. --python_out=../pb_extractor *.proto model/* service/* view/* google/api/*

	# proto_reader.py生成
	pipenv run python proto_reader_generator/proto_reader_generator.py

	# ./output/RemoteDataSource/Sources/RemoteDataSource/Repository ./output/RemoteDataSource/Sources/RemoteDataSource/Requestディレクトリ生成
	mkdir -p ./output/RemoteDataSource/Sources/RemoteDataSource/Repository ./output/RemoteDataSource/Sources/RemoteDataSource/Request

	# Swift Package生成
	cd ./output/RemoteDataSource; swift package init --name RemoteDataSource --type library
	cp -a ./templates/swift/Foundation ./output/RemoteDataSource/Sources/RemoteDataSource/Foundation
	cp -f ./templates/swift/Package.swift ./output/RemoteDataSource/Package.swift

	# Swiftファイル生成
	pipenv run python pb_extractor/pb_extractor.py

.PHONY: clear
clear: ## make genで生成されるファイル、ディレクトリを削除します
	# *_pb2.py削除
	find ./pb_extractor -type f -name "*_pb2.py" | xargs rm -rf
	find ./pb_extractor -type d -empty -delete

	# proto_reader.py削除
	rm -rf ./pb_extractor/proto_reader.py

	# ./output/RemoteDataSourceディレクトリ削除
	rm -rf ./output/RemoteDataSource
