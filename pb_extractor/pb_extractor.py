from message_type_extractor import MessageTypeExtractor as me
from proto_reader import ProtoReader as pr
from service_extractor import ServiceExtractor as se

def main():
    proto_list = pr.readAll()

    for proto in proto_list:
        # サービスの内容を抽出する
        service_contexts = se.extract_services(proto.service)

        # メッセージの内容を抽出する
        me.extract_message_types(proto.message_type, service_contexts)

if __name__ == '__main__':
    main()
