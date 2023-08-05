from constgen.generators.common import Outputer, Constant, Enum, Type
import inflection


class Python2Outputer (Outputer):

    def output_enum(self, constant : Constant):
        super().output_enum(constant, prefix=f"{inflection.underscore(constant.name).upper()}_")

    def output_type(self, type: Type):
        print(f"WARNING: No type definition support implemented for class: {self.__class__.__name__} - skipping")


class Python3Outputer (Outputer):

    def output_header(self):
        super().output_header()
        self._output.write("from enum import Enum\n")

    def output_enum(self, enum : Enum):
        self._output.write(f"class {enum.name}(Enum):\n")
        super().output_enum(enum, prefix=f"\t")
        self._output.write(f"\n")

    def output_type(self, type: Type):
        print(f"WARNING: No type definition support implemented for class: {self.__class__.__name__} - skipping")
