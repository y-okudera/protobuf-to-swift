import pystache

class SwiftGenerator:
    def generate_swift_from_template(template_path, output_path, context):
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
