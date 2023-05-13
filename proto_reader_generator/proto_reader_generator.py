import os
import pystache


def main():
    template_path = "templates/mustache/python/proto_reader.py.mustache"
    output_path = "protobuf_to_swift/proto_reader.py"

    pb2_files = []

    # ファイル名取得
    for f in os.listdir("protobuf_to_swift"):
        if f.endswith("_pb2.py"):
            pb2_files.append({"name": f[:-3]})
    context = {"pb2_files": pb2_files}

    with open(template_path, "r") as file:
        template = file.read()

    renderer = pystache.Renderer()
    rendered_content = renderer.render(template, context)

    with open(output_path, "w") as file:
        file.write(rendered_content)


if __name__ == "__main__":
    main()
