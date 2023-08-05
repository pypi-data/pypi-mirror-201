from constgen.generators.common import Outputer, Constant, Enum, Type
import textwrap
import inflection
import os


class JavaOutputer (Outputer):

    def __init__(self, *args, **kwargs):
        super().__init__(comment_mark="//", comment_indentation=1, *args, **kwargs)

    def output_header(self):
        super().output_header()
        class_name = self._get_class_name()
        self._output.write(textwrap.dedent(f"""\
            public final class {class_name} {{
            """))

    def output_footer(self):
        super().output_footer()
        self._output.write("\n}")

    def _get_class_name(self):
        return os.path.basename(self.path).replace(".java", "")

    def output_enum(self, enum : Enum):
        separator = ', \n\t\t'
        self._output.write(f"\tpublic enum {enum.name} {{\n\t\t{separator.join([val for val in enum.values])}\n\t}}\n")

    def output_constant(self, constant: Constant):
        name = inflection.underscore(constant.name).upper()
        if type(constant.value) == str:
            self._output.write(f'\tpublic static final String {name} = "{constant.value}";\n')
        else:
            self._output.write(f'\tpublic static final {type(constant.value).__name__} {name} = {constant.value};\n')

    def output_type(self, type: Type):
        print(f"WARNING: No type definition support implemented for class: {self.__class__.__name__} - skipping")
