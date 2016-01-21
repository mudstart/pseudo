from pseudon.code_generator import CodeGenerator, indented


class GolangGenerator(CodeGenerator):
    '''Go generator'''

    templates = {
        'program': '%<code>',
        'function': indented('''
                    func %<name>() {\n
                        %<body>
                    }
                    ''')
    }