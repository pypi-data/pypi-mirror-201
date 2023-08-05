from constgen.generators import COutputer, Python2Outputer, Python3Outputer, JavaOutputer,\
    JavascriptOutputer, RustOutputer, VueMixinOutputer, GoOutputer, Constant, Enum, Type
from pydantic import BaseModel
from typing import List


class AllOutputs (BaseModel):
    python: Python3Outputer = None
    python2: Python2Outputer = None
    javascript: JavascriptOutputer = None
    vue: VueMixinOutputer = None
    c: COutputer = None
    java: JavaOutputer = None
    rust: RustOutputer = None
    go: GoOutputer = None


class RootConfig (BaseModel):
    enums: List[Enum] = []
    constants: List[Constant] = []
    outputs: AllOutputs
    types: List[Type] = []
