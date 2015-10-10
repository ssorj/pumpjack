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

from render import *

class PythonRenderer(PumpjackRenderer):
    def __init__(self, output_dir):
        super(PythonRenderer, self).__init__(output_dir)

        self.type_literals["string"] = "str"
        self.type_literals["boolean"] = "bool"
        self.type_literals["integer"] = "int"
        self.type_literals["any"] = "object"
        self.type_literals["class"] = "type"

    def render_class_name(self, cls):
        return init_cap(studly_name(cls.name))

    def render_method_name(self, meth):
        return meth.name.replace("-", "_")

    def render_var_name(self, var):
        return var.name.replace("-", "_")

    def render_model(self, out, model):
        for type in model.types:
            self.render_type(out, type)

        out.write()

        for module in model.modules:
            self.render_module(out, module)

    def render_module(self, out, module):
        out.write("# Module {}", module.name)
        out.write()

        for cls in module.classes:
            self.render_class(out, cls)
            out.write()

        for exc in module.exceptions:
            self.render_exception(out, exc)
            out.write()

        for enum in module.enumerations:
            self.render_enumeration(out, enum)
            out.write()

        out.write("# End of module {}", module.name)

    def render_class(self, out, cls):
        name = self.render_class_name(cls)
        type = self.get_type_literal(cls, cls.type)

        if cls.type is None:
            type = "object"

        out.write("class {}({}):", name, type)
        out.write("    \"\"\"")
        out.write("    {}", cls.doc)
        out.write()

        for group, methods in cls.methods_by_group.iteritems():
            names = [self.render_method_name(x) for x in methods]
            out.write("    @group {}: {}", group, ", ".join(names))

        out.write("    \"\"\"")
        out.write()

        if cls.constants:
            for const in cls.constants:
                self.render_constant(out, const)

            out.write()

        if cls.enumerations:
            for enum in cls.enumerations:
                for const in enum.constants:
                    self.render_constant(out, const)

                out.write()

        if cls.constructor:
            self.render_constructor(out, cls.constructor)
            out.write()

        for meth in cls.methods:
            self.render_method(out, meth)
            out.write()

        out.write("    # End of class {}", name)

    def render_constant(self, out, const):
        name = const.name.upper()
        value = const.value
        out.write("    {} = {}", name, value)

    def render_constructor(self, out, ctor):
        inputs = list(("self",))
        inputs.extend([x.name for x in ctor.inputs])
        out.write("    def __init__({}):", ", ".join(inputs))

        self.render_method_body(out, ctor)

        for attr in ctor.parent.attributes:
            self.render_attribute(out, attr)

    def render_attribute(self, out, attr):
        name = self.render_var_name(attr)
        value = attr.value

        if value is None:
            value = "None"
        elif value.startswith("@"):
            type = self.get_type_literal(attr, value)
            value = "{}()".format(type)
        else:
            if attr.type == "string":
                value = "\"{}\"".format(value)

            if attr.type == "boolean":
                value = initcap(value)

        out.write("        self.{} = {}", name, value)

    def render_method(self, out, meth):
        name = self.render_method_name(meth)
        inputs = list(("self",))

        for input in meth.inputs:
            var = self.render_var_name(input)

            if input.nullable:
                inputs.append("{}=None".format(var))
            else:
                inputs.append(var)

        out.write("    def {}({}):", name, ", ".join(inputs))

        self.render_method_body(out, meth)

    def render_method_body(self, out, meth):
        out.write("        \"\"\"")
        out.write("        {}", meth.doc)
        out.write()

        for input in meth.inputs:
            name = self.render_var_name(input)

            if input.doc:
                out.write("        @param {}: {}", name, input.doc)

            literal = self.get_type_literal(meth, input.type)
            out.write("        @type {}: {}", name, literal)

        if meth.outputs:
            output = meth.outputs[0]
            name = self.render_var_name(output)

            if output.doc:
                out.write("        @return: {}", name, output.doc)

            literal = self.get_type_literal(meth, output.type)
            out.write("        @rtype: {}", literal)

        for cond in meth.exception_conditions:
            cls = self.render_class_name(cond.exception)
            out.write("        @raise {}: {}", cls, cond.doc)

        out.write("        \"\"\"")

    def render_exception(self, out, exc):
        out.write("class {}(Exception):", self.render_class_name(exc))
        out.write("    \"\"\"")
        out.write("    {}", exc.doc)
        out.write("    \"\"\"")

    def render_enumeration(self, out, enum):
        name = self.render_class_name(enum)

        out.write("class {}:", name)
        out.write("    pass")
        out.write()

        for const in enum.constants:
            #prefix = self.render_var_name(enum).upper()
            #out.write("{}_{} = {}()", prefix, self.render_var_name(const).upper(), name)
            out.write("{} = {}()", self.render_var_name(const).upper(), name)

    def render_type(self, out, type):
        out.write("# type {} -> {}", type.name, self.type_literals[type.name])

add_renderer("python", PythonRenderer)
