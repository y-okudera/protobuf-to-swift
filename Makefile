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
	rm -rf ./output/api
	rm -rf ./output/request
	mkdir -p ./output/api
	mkdir -p ./output/request
	find ./pb_extractor -type f | grep -v -E 'pb_extractor.py' | xargs rm -rf
	find ./pb_extractor -type d -empty -delete
	cd proto; protoc --proto_path=. --python_out=../pb_extractor accountService.proto model/* service/* google/api/*
	pipenv run python pb_extractor/pb_extractor.py
