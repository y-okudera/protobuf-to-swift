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
	# ./output/api ./output/requestディレクトリ削除、生成
	rm -rf ./output/api ./output/request
	mkdir -p ./output/api ./output/request

	# *_pb2.py削除、生成
	find ./pb_extractor -type f -name "*_pb2.py" | xargs rm -rf
	find ./pb_extractor -type d -empty -delete
	cd proto; protoc --proto_path=. --python_out=../pb_extractor *.proto model/* service/* view/* google/api/*

	# proto_reader.py削除、生成
	rm -rf ./pb_extractor/proto_reader.py
	pipenv run python proto_reader_generator/proto_reader_generator.py

	# Swiftファイル生成
	pipenv run python pb_extractor/pb_extractor.py
