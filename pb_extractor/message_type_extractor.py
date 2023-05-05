from swift_generator import SwiftGenerator as sg
import pprint
import re


class MessageTypeExtractor:
    def extract_message_types(message_types, service_contexts):
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
            pprint.pprint(message_type)

            enum_list = []
            for e in message_type.enum_type:
                values = list(
                    map(
                        lambda v: {
                            "value": re.sub(
                                "_(.)",
                                lambda x: x.group(1).upper(),
                                v.name.lower(),
                            )
                        },
                        e.value,
                    )
                )
                enum_list.append({"enum_name": e.name, "enum_values": values})

            print("---enum_list---")
            pprint.pprint(enum_list)

            properties = []
            for f in message_type.field:
                if f.label == 1:
                    label = "?"
                if f.label == 2:
                    label = ""
                if f.label == 3:
                    print("  LABEL_REPEATED")
                    # TODO:

                if f.type == 1:
                    type = "Double"
                if f.type == 2:
                    type = "Float"
                if f.type == 3:
                    type = "Int64"
                if f.type == 4:
                    type = "UInt64"
                if f.type == 5:
                    type = "Int32"
                if f.type == 6:
                    type = "UInt64"
                if f.type == 7:
                    type = "UInt32"
                if f.type == 8:
                    type = "Bool"
                if f.type == 9:
                    type = "String"
                if f.type == 10:
                    print("  TYPE_GROUP")
                    # TODO:
                if f.type == 11:
                    print("  TYPE_MESSAGE")
                    # TODO:
                if f.type == 12:
                    type = "Data"
                if f.type == 13:
                    type = "UInt32"
                if f.type == 14:
                    # e.g. ".proto.FooRequest.Bar" -> "FooRequest.Bar"
                    type = f.type_name.replace(".proto.", "")
                if f.type == 15:
                    type = "Int32"
                if f.type == 16:
                    type = "Int64"
                if f.type == 17:
                    type = "Int32"
                if f.type == 18:
                    type = "Int64"

                camel_case_name = re.sub(
                    "_(.)", lambda x: x.group(1).upper(), f.name
                )

                if f == message_type.field[-1]:
                    properties.append(
                        {
                            "name": camel_case_name,
                            "type": type + label,
                        }
                    )
                else:
                    properties.append(
                        {
                            "name": camel_case_name,
                            "type": type + label,
                            "comma": True,
                        }
                    )

            service_context = list(
                filter(
                    lambda item: item["input_type"] == message_type.name,
                    service_contexts,
                )
            )[0]

            template_path = "templates/mustache/request.swift.mustache"
            output_path = (
                "output/RemoteDataSource/Sources/RemoteDataSource/Request/%s.swift"
                % message_type.name
            )
            context = {
                "message": message_type.name,
                "output_type": service_context["output_type"],
                "http_method": service_context["http_method"],
                "path": service_context["path"],
                "properties": properties,
                "enum_list": enum_list,
            }

            sg.generate_swift_from_template(
                template_path, output_path, context
            )

            print("---message_context---")
            pprint.pprint(context)
