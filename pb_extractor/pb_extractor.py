import accountService_pb2 as pb2
from google.protobuf import descriptor_pb2
import humps
import pystache

def __generate_swift_from_template(template_path, output_path, context):
    """
    Swiftファイルを生成する
    Parameters
    ----------
    template_path : str
        テンプレートファイルのpath
    output_path : str
        出力先のpath
    context : dictionary
        テンプレートに割り当てる値
    """
    with open(template_path, 'r') as file:
        template = file.read()

    renderer = pystache.Renderer()
    rendered_content = renderer.render(template, context)

    with open(output_path, 'w') as file:
        file.write(rendered_content)

def __extract_services(services):
    """
    サービスを抽出する
    Parameters
    ----------
    services : RepeatedCompositeFieldContainer[global___ServiceDescriptorProto]
        services
    """

    # サービスごとに処理
    contexts = []
    for service in services:
        method = service.method
        # RPCの取得
        for rpc in method:
            for option in descriptor_pb2.MethodOptions.ListFields(rpc.options):
                option_key_str = option[0]
                if (option_key_str.full_name == "google.api.http"):
                    option_value_str = "{}".format(option[1])
                    split_stg = option_value_str.strip().split(': ')
                    http_method = split_stg[0]
                    path = split_stg[1].replace('"', '')

            print('---rpc---')
            print('rpc名: %s' % rpc.name)
            print('input_type: %s' % rpc.input_type)
            print('output_type: %s' % rpc.output_type)
            print('http_method: %s' % http_method)
            print('path: %s' % path)
            print('')

            template_path = "templates/mustache/api.swift.mustache"
            output_path = "output/api/%sAPI.swift" % rpc.name
            context = {
                "rpc_name": rpc.name,
                "http_method": http_method,
                "input_type": rpc.input_type.replace('.proto.', ''),
                "output_type": rpc.output_type.replace('.', '_')[1:].title(),
                "path": path
            }
            __generate_swift_from_template(template_path, output_path, context)
            contexts.append(context)

    print("service_contexts: {}".format(contexts))
    print('')
    return contexts

def __extract_message_types(message_types, service_contexts):
    """
    メッセージを抽出する
    Parameters
    ----------
    message_types : RepeatedCompositeFieldContainer[global___DescriptorProto]
        message_types
    """

    # メッセージごとに処理
    for message_type in message_types:
        print("---message_type---")
        print("message名: %s" % message_type.name)
        fields = {}
        for f in message_type.field:
            print(" ---field---")
            print(" field名: %s" % f.name)

            if (f.label == 1):
                print("  LABEL_OPTIONAL")
                label = "?"
            if (f.label == 2):
                print("  LABEL_REQUIRED")
                label = ""
            if (f.label == 3):
                print("  LABEL_REPEATED")
                # TODO:

            if (f.type == 1):
                print("  TYPE_DOUBLE")
                type = "Double"
            if (f.type == 2):
                print("  TYPE_FLOAT")
                type = "Float"
            if (f.type == 3):
                print("  TYPE_INT64")
                type = "Int64"
            if (f.type == 4):
                print("  TYPE_UINT64")
                type = "UInt64"
            if (f.type == 5):
                print("  TYPE_INT32")
                type = "Int32"
            if (f.type == 6):
                print("  TYPE_FIXED64")
                type = "UInt64"
            if (f.type == 7):
                print("  TYPE_FIXED32")
                type = "UInt32"
            if (f.type == 8):
                print("  TYPE_BOOL")
                type = "Bool"
            if (f.type == 9):
                print("  TYPE_STRING")
                type = "String"
            if (f.type == 10):
                print("  TYPE_GROUP")
                # TODO:
            if (f.type == 11):
                print("  TYPE_MESSAGE")
                # TODO:
            if (f.type == 12):
                print("  TYPE_BYTES")
                type = "Data"
            if (f.type == 13):
                print("  TYPE_UINT32")
                type = "UInt32"
            if (f.type == 14):
                print("  TYPE_ENUM")
                # TODO:
            if (f.type == 15):
                print("  TYPE_SFIXED32")
                type = "Int32"
            if (f.type == 16):
                print("  TYPE_SFIXED64")
                type = "Int64"
            if (f.type == 17):
                print("  TYPE_SINT32")
                type = "Int32"
            if (f.type == 18):
                print("  TYPE_SINT64")
                type = "Int64"
            fields[f.name] = type + label
            print('')

        print('message_fields: {}'.format(fields))

        service_context = list(filter(lambda item : item['input_type'] == message_type.name, service_contexts))[0]
        print("対象のservice_context: {}".format(service_context))

        properties = []
        for k, v in humps.camelize(fields).items():
            properties.append({"name": k, "type": v})

        template_path = "templates/mustache/request.swift.mustache"
        output_path = "output/request/%s.swift" % message_type.name
        context = {
            "message": message_type.name,
            "output_type": service_context["output_type"],
            "http_method": service_context["http_method"],
            "path": service_context["path"],
            "properties": properties
        }
        print("message_context: {}".format(context))
        __generate_swift_from_template(template_path, output_path, context)

def main():
    # ファイルの読み込み
    proto = descriptor_pb2.FileDescriptorProto.FromString(
        pb2.DESCRIPTOR.serialized_pb
    )

    # サービスの内容を抽出する
    service_contexts = __extract_services(proto.service)

    # メッセージの内容を抽出する
    message_types = proto.message_type
    __extract_message_types(message_types, service_contexts)

if __name__ == '__main__':
    main()
