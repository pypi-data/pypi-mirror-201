from constgen.generators.common import Outputer, Constant, Enum, Type
import inflection


class RustOutputer (Outputer):

    def __init__(self, *args, **kwargs):
        super().__init__(comment_mark="//", *args, **kwargs)

    def output_enum(self, enum : Enum):
        separator = ', \n\t'
        self._output.write(f"pub enum {enum.name} {{\n\t{separator.join([val for val in enum.values])}\n}}\n")

    def output_constant(self, constant: Constant):
        name = inflection.underscore(constant.name).upper()
        t = {int: 'i32', float: 'f32', str: '&str'}.get(type(constant.value), type(constant.value).__name__)
        quotes = '"' if t == '&str' else ''
        self._output.write(f'pub const {name}: {t} = {quotes}{constant.value}{quotes};\n')

    def output_type(self, type: Type):
        print(f"WARNING: No type definition support implemented for class: {self.__class__.__name__} - skipping")
