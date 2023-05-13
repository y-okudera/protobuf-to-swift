from message_type_extractor import MessageTypeExtractor as me
from proto_reader import ProtoReader as pr
from service_extractor import ServiceExtractor as se
import sys


def main():
    proto_list = pr.readAll()

    for proto in proto_list:
        # サービスの内容を抽出する
        service_contexts = se.extract_services(
            services=proto.service,
            output_path_format=f"{sys.argv[1]}",  # 利用側で%sに値を設定
            template_path=f"{sys.argv[2]}",
        )

        # メッセージの内容を抽出する
        me.extract_message_types(
            message_types=proto.message_type,
            service_contexts=service_contexts,
            output_path_format=f"{sys.argv[3]}",  # 利用側で%sに値を設定
            template_path=f"{sys.argv[4]}",
        )


if __name__ == "__main__":
    main()
