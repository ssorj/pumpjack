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

    def get_property_name(self, prop):
        return prop.name.replace("-", "_")
    
    def get_method_name(self, meth):
        if meth.name == "constructor":
            return "__init__"
        
        return meth.name.replace("-", "_")

    def get_parameter_name(self, param):
        return param.name.replace("-", "_")

    def render(self, model):
        self.render_model(None, model)

    def render_model(self, out, model):
        model_name = self.get_model_name(model)
        path = _os.path.join(self.output_dir, model_name, "__init__.py")

        with OutputWriter(path) as out:
            out.write("# Model {}", model.name)
        
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

            self.render_module_imports(out, module)

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

    def render_module_imports(self, out, module):
        model_name = self.get_model_name(module.model)
        module_name = self.get_module_name(module)
        
        out.write("import _{}_impl.{} as _{}", model_name, module_name, module_name)
        out.write()

    def render_class(self, out, cls):
        name = self.get_class_name(cls)
        type_ = "object"
        
        if cls.type is not None:
            type_ = self.get_class_name(cls.type)

        out.write("class {}({}):", name, type_)
        
        self.render_class_docstring(out, cls)

        if not cls.properties and not cls.methods:
            out.write("    pass")
            return

        self.render_constructor(out, cls)

        for prop in cls.properties:
            self.render_property(out, prop)
            out.write()
        
        for meth in cls.methods:
            if meth is cls.constructor:
                continue
            
            self.render_method(out, meth)
            out.write()

        out.write("    # End of class {}", name)

    def render_class_docstring(self, out, cls):
        text = ""

        if cls.text is not None:
            text = dedent_text(cls.text)
            text = text.replace("\n", "\n    ")
            
        out.write("    \"\"\"")
        out.write("    {}", text)

        #for group in cls.groups:
        #    names = [self.get_method_name(x) for x in group.methods]
        #    out.write("    :group {}: {}", group.name, ", ".join(names))

        out.write("    \"\"\"")
        out.write()

    def render_constructor(self, out, cls):
        if cls.constructor is None:
            self.render_default_constructor(out, cls)
        else:
            self.render_method(out, cls.constructor)
            out.write()

    def render_default_constructor(self, out, cls):
        module_name = self.get_module_name(cls.module)
        class_name = self.get_class_name(cls)
        
        out.write("    def __init__(self):")
        out.write("        self._impl = _{}.{}()", module_name, class_name)
        out.write()

    def render_property(self, out, prop):
        name = self.get_parameter_name(prop)

        out.write("    @property")
        out.write("    def {}(self):", name)

        self.render_property_docstring(out, prop)
        self.render_property_getter_body(out, prop)

        if prop.mutable:
            out.write()
            out.write("    @{}.setter", name)
            out.write("    def {}(self, value):", name)

            self.render_property_setter_body(out, prop)

    def render_property_docstring(self, out, prop):
        text = ""

        if prop.text is not None:
            text = dedent_text(prop.text)
            text = text.replace("\n", "\n        ")
        
        out.write("        \"\"\"")
        out.write("        {}", text)
        out.write("        \"\"\"")
        out.write()
        
    def render_property_getter_body(self, out, prop):
        name = self.get_parameter_name(prop)
        out.write("        return self._impl.{}", name)

    def render_property_setter_body(self, out, prop):
        name = self.get_parameter_name(prop)
        out.write("        self._impl.{} = value", name)

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

class PythonImplRenderer(PythonRenderer):
    def get_property_value(self, prop):
        if prop.value is None:
            if prop.type.name == "map":
                return "map()"

            if prop.type.name in ("array", "list"):
                return "list()"
            
            return "None"

        # XXX Don't use magic strings for these

        if prop.value == "[discovered]":
            if prop.type.name == "map":
                return "map() # Discovered"

            if prop.type.name in ("array", "list"):
                return "list() # Discovered"
            
            return "None # Discovered"

        if prop.value == "[instance]":
            type_name = self.get_type_name(prop.type)
            return "{}()".format(type_name)

        if prop.value == "[generated]":
            name = self.get_property_name(prop)
            return "self._generate_{}()".format(name)

        if type(prop.type) is Enumeration:
            enum_name = self.get_class_name(prop.type)
            name = prop.value.replace("-", "_")

            return "{}.{}".format(enum_name, name)
        
        if prop.type.name == "boolean":
            if prop.value == "true":
                return "True"
            else:
                return "False"

        if prop.type.name == "string":
            return "\"{}\"".format(prop.value)

        return prop.value
    
    def render_module_imports(self, out, module):
        pass
    
    def render_class_docstring(self, out, cls):
        pass

    def render_property_docstring(self, out, prop):
        pass

    def render_property_getter_body(self, out, prop):
        name = self.get_parameter_name(prop)
        out.write("        return self._{}", name)

    def render_property_setter_body(self, out, prop):
        name = self.get_parameter_name(prop)
        out.write("        self._{} = value", name)

    def render_method_docstring(self, out, meth):
        pass

    def render_method_body(self, out, meth):
        self.render_not_implemented(out, meth)

    def render_constructor_body(self, out, ctor):
        #if not ctor.class_.properties and not ctor.inputs:
        #    out.write("        pass")
        #    return

        if ctor.class_.type is None:
            out.write("        super().__init__()")
            out.write()
        else:
            super_ctor = ctor.class_.type.constructor

            if super_ctor is not None:
                args = ", ".join([self.get_parameter_name(x) for x in super_ctor.inputs])
                out.write("        super().__init__()")
                out.write()
        
        for prop in ctor.class_.properties:
            name = self.get_property_name(prop)
            value = self.get_property_value(prop)
                
            out.write("        self._{} = {}", name, value)

        if ctor.inputs:
            property_names = {x.name for x in ctor.class_.properties}

            for input in ctor.inputs:
                name = self.get_parameter_name(input)

                out.write()
                
                if input.optional:
                    if input.name not in property_names:
                        out.write("        self._{} = None", name)
                        out.write()
                        
                    out.write("        if {} is not None:", name)
                    out.write("            self._{} = {}", name, name)
                else:
                    out.write("        self._{} = {}", name, name)

    def render_not_implemented(self, out, node):
        out.write("        raise NotImplementedError()")

    def render_default_constructor(self, out, cls):
        module_name = self.get_module_name(cls.module)
        class_name = self.get_class_name(cls)
        
        out.write("    def __init__(self):")
        out.write("        super().__init__()")

        if cls.properties:
            out.write()
            
            for prop in cls.properties:
                name = self.get_property_name(prop)
                value = self.get_property_value(prop)
            
                out.write("        self._{} = {}", name, value)

        out.write()

add_renderer("python", PythonRenderer)
add_renderer("python-impl", PythonImplRenderer)

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
