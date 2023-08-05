import os
from constgen.generators.common import Outputer, Constant, Enum, Type

class GoOutputer(Outputer):
    def __init__(self, *args, **kwargs):
        super().__init__(comment_mark="//", *args, **kwargs)

    def output_header(self):
        super().output_header()
        self._output.write(f"package {self._get_package_name()}\n")

    def _get_package_name(self):
        file_name = os.path.basename(self.path)
        name, _ = os.path.splitext(file_name)
        return f"generated_{name}"

    def output_enum(self, enum : Enum):
        enum_type = enum.type if enum.type else ''
        starting_value_string = f"+ {enum.start_value}" if enum.start_value else ''
        self._output.write(f"const (\n\t{self._pascalize(enum.values[0])} {enum_type} = iota {starting_value_string}\n")
        for value in enum.values[1:]:
            self._output.write(f"\t{self._pascalize(value)}\n")
        self._output.write(")\n\n")

    @staticmethod
    def _pascalize(value):
        return ''.join(x for x in value.title() if x.isalnum())

    def output_constant(self, constant: Constant):
        name = self._pascalize(constant.name)
        if type(constant.value) == str:
            self._output.write(f'const {name} = "{constant.value}"\n')
        else:
            self._output.write(f'const {name} = {constant.value}\n')

    def output_type(self, type: Type):
        super().output_type(type, "type")

