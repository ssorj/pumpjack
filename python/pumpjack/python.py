#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from .render import *

import os as _os

_python_types = {
    "null": "None",
    "boolean": "bool",
    "string": "str",
    "binary": "bytes",
    "double": "float",
    "byte": "int",
    "short": "int",
    "ubyte": "int",
    "ushort": "int",
    "uint": "long",
    "ulong": "long",
    "array": "list",
    "map": "dict",
    "symbol": "str",
    "timestamp": "datetime.datetime",
    "uuid": "uuid.uuid4",
    "duration": "datetime.timedelta",
    "iterator": "object", # Which must implement the iterator protocol
}

class PythonRenderer(Renderer):
    def __init__(self, output_dir):
        super().__init__(output_dir)

    def get_type_name(self, type_):
        try:
            return _python_types[type_.name]
        except KeyError:
            pass

        return self.get_class_name(type_)

    def get_model_name(self, model):
        return model.annotations.get("python-name", model.name)

    def get_module_name(self, module):
        return module.name.replace("-", "_")

    def get_class_name(self, cls):
        return init_cap(_studly_name(cls.name))

    def get_method_name(self, meth):
        if meth.name == "constructor":
            return "__init__"
        
        return meth.name.replace("-", "_")

    def get_parameter_name(self, param):
        return param.name.replace("-", "_")

    def render(self, model):
        self.render_model(None, model)

    def render_model(self, out, model):
        for module in model.modules:
            self.render_module(out, module)

    def render_module(self, out, module):
        model_name = self.get_model_name(module.model)
        module_name = self.get_module_name(module)
        module_file = "{}.py".format(module_name)
        path = _os.path.join(self.output_dir, model_name, module_file)

        with OutputWriter(path) as out:
            out.write("# Module {}", module.name)
            out.write()

            out.write("import _{}_impl.{} as _core", model_name, module_name)
            out.write()

            for group in module.groups:
                out.write("# {}", group.title)
                out.write()
                
                for cls in group.classes:
                    self.render_class(out, cls)
                    out.write()

                for enum in group.enumerations:
                    self.render_enumeration(out, enum)
                    out.write()

            out.write("# End of module {}", module.name)

    def render_class(self, out, cls):
        name = self.get_class_name(cls)
        type = "object"
        
        if cls.type is not None:
            type = self.get_class_name(cls.type)

        text = ""

        if cls.text is not None:
            text = dedent_text(cls.text)
            text = text.replace("\n", "\n    ")
            
        out.write("class {}({}):", name, type)
        out.write("    \"\"\"")
        out.write("    {}", text)

        #for group in cls.groups:
        #    names = [self.get_method_name(x) for x in group.methods]
        #    out.write("    :group {}: {}", group.name, ", ".join(names))

        out.write("    \"\"\"")
        out.write()

        for group in cls.groups:
            for meth in group.methods:
                self.render_method(out, meth)
                out.write()

        out.write("    # End of class {}", name)

    def render_constructor(self, out, ctor):
        print(111)
        
        inputs = list(("self",))
        inputs.extend([x.name for x in ctor.inputs])
        out.write("    def __init__({}):", ", ".join(inputs))

        self.render_method_body(out, ctor)

        for attr in ctor.parent.attributes:
            self.render_attribute(out, attr)

    # XXX
    def render_attribute(self, out, attr):
        name = self.get_parameter_name(attr)
        value = attr.value

        if value is None:
            value = "None"
        elif value.startswith("@"):
            type = self.get_type_name(attr, value)
            value = "{}()".format(type)
        else:
            if attr.type == "string":
                value = "\"{}\"".format(value)

            if attr.type == "boolean":
                value = initcap(value)

        out.write("        self.{} = {}", name, value)

    def render_method(self, out, meth):
        name = self.get_method_name(meth)
        inputs = list(("self",))

        for input in meth.inputs:
            input_name = self.get_parameter_name(input)

            if input.optional:
                inputs.append("{}=None".format(input_name))
            else:
                inputs.append(input_name)

        out.write("    def {}({}):", name, ", ".join(inputs))

        if meth.name == "constructor":
            self.render_constructor_body(out, meth)
        else:
            self.render_method_body(out, meth)

    def render_constructor_body(self, out, ctor):
        self.render_method_docstring(out, ctor)

        cls = ctor.class_
        module_name = "_{}".format(self.get_module_name(cls.module))
        class_name = self.get_class_name(cls)
        args = ", ".join([self.get_parameter_name(x) for x in ctor.inputs])

        out.write()
        out.write("        self._impl = {}.{}({})", module_name, class_name, args)

    def render_method_body(self, out, meth):
        self.render_method_docstring(out, meth)

        method_name = self.get_method_name(meth)
        args = ", ".join([self.get_parameter_name(x) for x in meth.inputs])

        out.write()
        out.write("        return self._impl.{}({})", method_name, args)

    def render_method_docstring(self, out, meth):
        text = ""

        if meth.text is not None:
            text = dedent_text(meth.text)
            text = text.replace("\n", "\n        ")
        
        out.write("        \"\"\"")
        out.write("        {}", text)
        out.write()

        for input in meth.inputs:
            name = self.get_parameter_name(input)

            if input.text:
                out.write("        :param {}: {}", name, input.text)

            literal = self.get_type_name(input.type)
            out.write("        :type {}: {}", name, literal)

        if meth.outputs:
            output = meth.outputs[0]
            name = self.get_parameter_name(output)

            if output.text:
                out.write("        :returns: {}", name, output.text)

            literal = self.get_type_name(output.type)
            out.write("        :rtype: {}", literal)

        # for cond in meth.exception_conditions:
        #     cls = self.get_class_name(cond.exception)
        #     out.write("        @raise {}: {}", cls, cond.doc)

        out.write("        \"\"\"")

    def render_exception(self, out, exc):
        out.write("class {}(Exception):", self.get_class_name(exc))
        out.write("    \"\"\"")
        out.write("    {}", exc.doc)
        out.write("    \"\"\"")

    def render_enumeration(self, out, enum):
        enum_name = self.get_class_name(enum)

        out.write("class {}(object):", enum_name)
        out.write("    pass")
        out.write()

        for value in enum.values:
            name = self.get_parameter_name(value)
            out.write("{}.{} = {}()", enum_name, name, enum_name)

    def render_type(self, out, type):
        out.write("# type {} -> {}", type.name, self.type_literals[type.name])

add_renderer("python", PythonRenderer)

def _studly_name(name):
    assert name

    chars = list()
    prev = None
    curr = None

    for i in range(len(name)):
        curr = name[i]

        if prev == "-":
            curr = curr.upper()

        if curr != "-":
            chars.append(curr)

        prev = curr

    return "".join(chars)
