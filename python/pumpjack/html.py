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

import os as _os
import re as _re

class HtmlRenderer(PumpjackRenderer):
    def __init__(self, output_dir):
        super(HtmlRenderer, self).__init__(output_dir)

    def include_file(self, path):
        #return "" # XXX

        path = _os.path.join(self.output_dir, path)

        if not _os.path.exists(path):
            return ""

        with open(path, "r") as file:
            out = file.read()

        if out is None:
            return ""

        return out

    def render(self, model):
        output_path = model.get_output_path(self.output_dir)
        
        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            self.render_model(out, model)
    
    def render_model(self, out, model):
        print("Rendering {}".format(model))

        out.write(html_h(init_cap(model.title)))
        out.write(html_text(model.text))

        items = list()
        
        for link in model.links:
            items.append(html_a(link[0], link[1]))

        out.write(html_ul(items, class_="pumpjack links"))

        out.write(html_open("section"))
        out.write(html_h("Modules"))

        items = list()
        items.append(("Module", "Content", "Depends on"))

        for module in model.modules:
            name = "{}.{}".format(module.model.name, module.name)
            link = html_a(name, module.get_url())
            summary = first_sentence(module.text)
            requires = module.annotations.get("requires")

            items.append((link, summary, requires))

        out.write(html_table(items))
        out.write(html_close("section"))
        
        for module in model.modules:
            self.render_module(out, module)

    def render_module(self, out, module):
        output_path = module.get_output_path(self.output_dir)
        
        print("Rendering {} to {}".format(module, output_path))
        
        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            title = "Module '{}.{}'".format(module.model.name, module.name)

            out.write(html_h(title))
            
            out.write(html_text(module.text))
            #out.write(self.include_file("module.html"))

            for group in module.groups:
                self.render_module_group(out, group)

            for group in module.groups:
                for cls in group.classes:
                    self.render_class(out, cls)

    def render_module_group(self, out, group):
        out.write(html_open("section"))
        out.write(html_h(group.title))

        items = list()
        items.append(("Class", "Summary"))
                        
        for cls in group.classes:
            link = html_a(cls.name, cls.get_url())
            summary = first_sentence(cls.text)

            items.append((link, summary))

        out.write(html_table(items, class_="pumpjack classes"))

        out.write(html_close("section"))

    def render_class(self, out, cls):
        output_path = cls.get_output_path(self.output_dir)
        
        print("Rendering {} to {}".format(cls, output_path))

        classes = _get_classes(cls)
        group_names = set()
        groups = list()

        for c in classes:
            for group in c.groups:
                if group.name not in group_names:
                    group_names.add(group.name)
                    groups.append(group)

        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            title = "Class '{}'".format(cls.name)
            
            out.write(html_h(title))
            out.write(html_text(cls.text))

            items = list()
            
            for link in cls.links:
                items.append(html_a(link[0], link[1]))

            out.write(html_ul(items, class_="pumpjack links"))
            
            #out.write(self.include_file("{}.class.html".format(cls.name)))

            for group in groups:
                self.render_class_group(out, group)

            for group in cls.groups:
                for attr in group.properties:
                    self.render_property(out, attr)

                for meth in group.methods:
                    self.render_method(out, meth)

                # XXX the rest

    def render_class_group(self, out, group):
        out.write(html_open("section"))

        out.write(html_h(group.title))
        out.write(html_text(group.text))

        classes = _get_classes(group.class_)
        
        properties = list()
        methods = list()

        for cls in reversed(classes):
            try:
                group = cls.groups_by_name[group.name]
            except KeyError:
                continue
            
            properties.extend(group.properties)
            methods.extend(group.methods)

        if properties:
            items = list()
            items.append(("Property", "Summary", "Type", "Initial value",
                          "Mutable", "Nullable"))

            for prop in properties:
                link = html_a(prop.name, prop.get_url())
                summary = first_sentence(prop.text)
                type = html_ref(prop, prop.type)
                value = prop.value
                mutable = html_bool(prop.mutable)
                nullable = html_bool(prop.mutable)

                if value and value.startswith("[") and value.endswith("]"):
                    value = html_span(value[1:-1], class_="special")
                
                items.append((link, summary, type, value, mutable, nullable))

            out.write(html_table(items, class_="pumpjack properties"))

        if methods:
            items = list()
            items.append(("Method", "Summary", "Inputs", "Outputs"))
                            
            for meth in methods:
                link = html_a(meth.name, meth.get_url())
                summary = first_sentence(meth.text)

                inputs = list()
                outputs = list()

                if meth.inputs:
                    for input in meth.inputs:
                        if input.type.startswith("@"):
                            inputs.append(html_ref(input, input.type))
                        else:
                            inputs.append(input.name)

                if meth.outputs:
                    for output in meth.outputs:
                        if output.type.startswith("@"):
                            outputs.append(html_ref(output, output.type))
                        else:
                            outputs.append(output.name)
                            
                inputs = ", ".join(inputs)
                outputs = ", ".join(outputs)

                items.append((link, summary, inputs, outputs))

            out.write(html_table(items, class_="pumpjack methods"))

        out.write(html_close("section"))

    def render_property(self, out, prop):
        output_path = prop.get_output_path(self.output_dir)
        
        print("Rendering {} to {}".format(prop, output_path))

        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            value = ""

            if prop.value is not None:
                value = format_node_value(prop)
                value = "= {}".format(value)
                value = html_span(value, class_="signature")

            title = "Property '{}'".format(prop.name)
                
            out.write(html_h(title))

            items = (
                ("Type", prop.type),
                ("Initial value", prop.value),
                ("Mutable", prop.mutable),
                ("Nullable", prop.nullable),
            )

            out.write(html_table(items, False, True, class_="props"))
            out.write(html_text(prop.text))
            #out.write(self.include_file("{}.property.html".format(prop.name)))

    def render_method(self, out, meth):
        output_path = meth.get_output_path(self.output_dir)
        
        print("Rendering {} to {}".format(meth, output_path))

        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            # signature = ", ".join([x.name for x in meth.inputs])
            # signature = "({})".format(signature)

            # if meth.outputs:
            #     output = meth.outputs[0]
            #     signature = "{} = {}".format(signature, format_node_value(output))

            # signature = html_span(signature, class_="signature")

            title = "Method '{}'".format(meth.name)

            out.write(html_h(title))

            out.write(html_text(meth.text))

            if meth.inputs:
                self.render_method_inputs(out, meth)

            if meth.outputs:
                self.render_method_outputs(out, meth)

            #out.write(self.include_file("{}.method.html".format(meth.name)))

    def render_method_inputs(self, out, meth):
        items = list()
        items.append(("Input", "Type", "Nullable"))
        
        for input in meth.inputs:
            name = input.name
            type = html_ref(input, input.type)
            nullable = html_bool(input.nullable)
            
            items.append((name, type, nullable))

        out.write(html_table(items, class_="parameters"))

    def render_method_outputs(self, out, meth):
        items = list()
        items.append(("Output", "Type", "Nullable"))
        
        for output in meth.outputs:
            name = output.name
            type = html_ref(output, output.type)
            nullable = html_bool(output.nullable)
            
            items.append((name, type, nullable))

        out.write(html_table(items, class_="parameters"))

add_renderer("html", HtmlRenderer)

def html_ref(node, ref):
    if ref is not None and ref.startswith("@"):
        node = node.resolve_reference(ref)

        if node is not None:
            return html_a(node.name, node.get_url())
    else:
        return ref

def html_bool(value):
    return "&#x2612;" if value else "&#x2610;"    
    
def html_text(text):
    if not text:
        return ""

    text = _re.sub("{", "<a href=\"\">", text) # XXX
    text = _re.sub("}", "</a>", text)

    text = _re.sub("\s*\n\s*\n\s*", " </p>\n\n<p>", text)

    return "<p>{}</p>".format(text)

def format_node_value(node):
    value = node.value

    if node.type == "string":
        return "'{}'".format(value)

    if node.type[0] == "@":
        return "{} instance".format(node.type[1:])

    return value

def _open_output(path):
    parent, child = _os.path.split(path)

    if not _os.path.exists(parent):
        _os.makedirs(parent)
    
    return open(path, "w")

def _get_classes(cls):
    classes = list()
    current = cls

    while current is not None:
        classes.append(current)
        current = current.type

    return classes

