.PHONY: help
help: ## ヘルプを表示します
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: bootstrap
bootstrap: ## 必要なツールのインストールを実行します
	brew install protobuf go swift-protobuf pipenv
	go install github.com/pseudomuto/protoc-gen-doc/cmd/protoc-gen-doc@latest
	npm install -g yarn
	pipenv shell

.PHONY: project
project: ## プロジェクトの設定をします
	yarn install
	pipenv install

OUTPUT_PATH := $(shell pipenv run python configs/config.py OUTPUT_PATH)
SWIFT_PACKAGE_NAME := $(shell pipenv run python configs/config.py SWIFT_PACKAGE_NAME)
SWIFT_PACKAGE_PATH := ${OUTPUT_PATH}/${SWIFT_PACKAGE_NAME}

.PHONY: gen-swift-package
gen-swift-package: ## SwiftPackageを生成します
	sh shellscript/generate_swift_package.sh ${SWIFT_PACKAGE_PATH}

.PHONY: clear
clear: ## 生成されたファイル、ディレクトリを削除します
	sh shellscript/clear_generated_files.sh
