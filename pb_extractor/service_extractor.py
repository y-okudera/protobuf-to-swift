from google.protobuf import descriptor_pb2
from swift_generator import SwiftGenerator as sg
import pprint


class ServiceExtractor:
    def extract_services(services):
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
            print("---service---")
            pprint.pprint(service)
            method = service.method
            # RPCの取得
            for rpc in method:
                for option in descriptor_pb2.MethodOptions.ListFields(
                    rpc.options
                ):
                    option_key_str = option[0]
                    if option_key_str.full_name == "google.api.http":
                        option_value_str = "{}".format(option[1])
                        split_stg = option_value_str.strip().split(": ")
                        http_method = split_stg[0]
                        path = split_stg[1].replace('"', "")

                template_path = "templates/mustache/api.swift.mustache"
                output_path = "output/api/%sAPI.swift" % rpc.name
                context = {
                    "rpc_name": rpc.name,
                    "http_method": http_method,
                    "input_type": rpc.input_type.replace(".proto.", ""),
                    "output_type": rpc.output_type.replace(".", "_")[
                        1:
                    ].title(),
                    "path": path,
                }

                sg.generate_swift_from_template(
                    template_path, output_path, context
                )
                contexts.append(context)

        print("---service_contexts---")
        pprint.pprint(contexts)
        return contexts
