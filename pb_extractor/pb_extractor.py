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

            output_type = rpc.output_type.replace('.', '_')[1:].title()

            http_method = ""
            path = ""
            lines = "{}".format(rpc).splitlines()
            for i, m in enumerate(lines):
                if ('[google.api.http]' in m):
                    ls = lines[i+1].strip().replace('"', '').split(': ')
                    http_method = ls[0]
                    path = ls[1]
            print('RPC名: %s' % rpc.name)
            print('input_type: %s' % rpc.input_type)
            print('output_type: %s' % output_type)
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
        print("Message %s" % message_type.name)
        print("Fields")
        fields = {}
        for f in message_type.field:
            print(" %s" % f.name)

            lbl = f.label
            o = ""
            if (lbl == 1):
                print("  LABEL_OPTIONAL")
                o = "?"
            if (lbl == 2):
                print("  LABEL_REQUIRED")
                o = ""
            if (lbl == 3):
                print("  LABEL_REPEATED")
                # TODO:

            type = f.type
            t = ""
            if (type == 1):
                print("  TYPE_DOUBLE")
                t = "Double"
            if (type == 2):
                print("  TYPE_FLOAT")
                t = "Float"
            if (type == 3):
                print("  TYPE_INT64")
                t = "Int64"
            if (type == 4):
                print("  TYPE_UINT64")
                t = "UInt64"
            if (type == 5):
                print("  TYPE_INT32")
                t = "Int32"
            if (type == 6):
                print("  TYPE_FIXED64")
                t = "UInt64"
            if (type == 7):
                print("  TYPE_FIXED32")
                t = "UInt32"
            if (type == 8):
                print("  TYPE_BOOL")
                t = "Bool"
            if (type == 9):
                print("  TYPE_STRING")
                t = "String"
            if (type == 10):
                print("  TYPE_GROUP")
                # TODO:
            if (type == 11):
                print("  TYPE_MESSAGE")
                # TODO:
            if (type == 12):
                print("  TYPE_BYTES")
                t = "Data"
            if (type == 13):
                print("  TYPE_UINT32")
                t = "UInt32"
            if (type == 14):
                print("  TYPE_ENUM")
                # TODO:
            if (type == 15):
                print("  TYPE_SFIXED32")
                t = "Int32"
            if (type == 16):
                print("  TYPE_SFIXED64")
                t = "Int64"
            if (type == 17):
                print("  TYPE_SINT32")
                t = "Int32"
            if (type == 18):
                print("  TYPE_SINT64")
                t = "Int64"
            fields[f.name] = t + o

        print('')
        print(fields)

        service_context = list(filter(lambda item : item['input_type'] == message_type.name, service_contexts))[0]
        print(service_context)
        template_path = "templates/mustache/request.swift.mustache"
        output_path = "output/request/%s.swift" % message_type.name
        properties = []
        for k, v in humps.camelize(fields).items():
            properties.append({"name": k, "type": v})
        context = {
            "message": message_type.name,
            "output_type": service_context["output_type"],
            "http_method": service_context["http_method"],
            "path": service_context["path"],
            "properties": properties
        }
        print(context)
        __generate_swift_from_template(template_path, output_path, context)

def main():
    # ファイルの読み込み
    proto = descriptor_pb2.FileDescriptorProto.FromString(
        pb2.DESCRIPTOR.serialized_pb
    )

    # サービスの内容を抽出する
    service_contexts = __extract_services(proto.service)
    print("service_contexts: {}".format(service_contexts))

    # メッセージの内容を抽出する
    message_types = proto.message_type
    __extract_message_types(message_types, service_contexts)

if __name__ == '__main__':
    main()
