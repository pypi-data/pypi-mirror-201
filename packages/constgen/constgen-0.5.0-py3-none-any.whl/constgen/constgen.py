import argparse
import yaml
from constgen.config import RootConfig


def process_input(config: RootConfig):
    outputers = [getattr(config.outputs, x) for x in config.outputs.__fields_set__]

    for outputer in outputers:
        outputer.output_header()
        outputer.output_comment("types")
        for gentype in config.types:
            outputer.output_type(gentype)
        outputer.output_comment("constants")
        for constant in config.constants:
            outputer.output_constant(constant)
        outputer.output_comment("enums")
        for enum in config.enums:
            outputer.output_enum(enum)
        outputer.output_footer()
    

def main():
    parser = argparse.ArgumentParser(description='Reconstant - Share constant definitions between programming languages and make your constants constant again.')
    parser.add_argument('input', type=str, help='input file in yaml format')
    args = parser.parse_args()

    with open(args.input, "r") as yaml_input:
        python_obj = yaml.safe_load(yaml_input)
        config = RootConfig.parse_obj(python_obj)
        process_input(config)


if __name__ == "__main__":
    main()
