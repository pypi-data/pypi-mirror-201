from constgen.generators.common import Outputer, Constant, Enum, Type
import textwrap
import inflection


class COutputer (Outputer):

    def __init__(self, *args, **kwargs):
        super().__init__(comment_mark="//", *args, **kwargs)

    def output_header(self):
        super().output_header()
        guard_name = self._get_guard_name()
        self._output.write(textwrap.dedent(f"""\
            #ifndef {guard_name}
            #define {guard_name}
            """))

    def output_footer(self):
        super().output_footer()
        guard_name = self._get_guard_name()
        self._output.write(f"\n#endif /* {guard_name} */")

    def _get_guard_name(self):
        return self.path.replace('/', '_').replace(".", "_").upper()

    def output_enum(self, enum : Enum):
        self._output.write(f"typedef enum {{ {', '.join([val for val in enum.values])} }} {enum.name};\n")

    def output_constant(self, constant: Constant):
        name = inflection.underscore(constant.name).upper()
        if type(constant.value) == str:
            self._output.write(f'const char* {name} = "{constant.value}";\n')
        else:
            self._output.write(f'const {type(constant.value).__name__} {name} = {constant.value};\n')

    def output_type(self, type: Type):
        super().output_type(type, "typedef", ";")
