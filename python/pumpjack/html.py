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

import collections as _collections
import markdown2 as _markdown2
import os as _os
import re as _re

class HtmlRenderer(PumpjackRenderer):
    def __init__(self, output_dir):
        super(HtmlRenderer, self).__init__(output_dir)

    def render(self, model):
        output_path = model.get_output_path(self.output_dir)
        
        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            self.render_model(out, model)
    
    def render_model(self, out, model):
        print("Rendering {}".format(model))

        out.write(html_h(init_cap(model.title)))
        out.write(_html_node_text(model))
        out.write(_html_node_links(model))
        
        out.write(html_open("section"))
        out.write(html_h("Modules"))

        items = list()
        items.append(("Module", "Content", "Depends on"))

        for module in model.modules:
            link = _html_node_link(module)
            summary = _html_node_summary(module)
            requires = module.annotations.get("requires")

            items.append((link, summary, requires))

        out.write(html_table(items, class_="pumpjack modules"))
        out.write(html_close("section"))
        
        for module in model.modules:
            self.render_module(out, module)

    def render_module(self, out, module):
        output_path = module.get_output_path(self.output_dir)
        
        print("Rendering {} to {}".format(module, output_path))
        
        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            out.write(_html_node_title(module))
            out.write(_html_node_text(module))
            out.write(_html_node_links(module))

            for group in module.groups:
                self.render_module_group(out, group)

            for group in module.groups:
                for cls in group.classes:
                    self.render_class(out, cls)

    def render_module_group(self, out, group):
        out.write(html_open("section"))
        out.write(html_h(group.title))
        out.write(_html_node_text(group))
        out.write(_html_node_links(group))

        items = list()
        items.append(("Class", "Summary"))
                        
        for cls in group.classes:
            link = _html_node_link(cls)
            summary = first_sentence(cls.text)

            if cls.hidden:
                continue

            items.append((link, summary))

        out.write(html_table(items, class_="pumpjack classes"))

        out.write(html_close("section"))

    def render_class(self, out, cls):
        output_path = cls.get_output_path(self.output_dir)
        
        print("Rendering {} to {}".format(cls, output_path))

        classes = _get_classes(cls)
        groups = _collections.OrderedDict()

        for c in classes:
            for group in c.groups:
                groups[group.name] = group

        if "basic" in groups:
            basic_group = groups["basic"]
            del groups["basic"]
            groups = [basic_group] + groups.values()
                
        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            out.write(_html_node_title(cls))
            out.write(_html_node_text(cls))
            out.write(_html_node_links(cls))

            for group in groups:
                self.render_class_group(out, cls, group)

            for group in cls.groups:
                for prop in group.properties:
                    self.render_property(out, prop)

                for meth in group.methods:
                    self.render_method(out, meth)

    def render_class_group(self, out, cls, group):
        out.write(html_open("section"))

        out.write(html_h(group.title))
        out.write(_html_node_text(group))
        out.write(_html_node_links(group))

        classes = _get_classes(cls)
        
        properties = list()
        methods = list()

        for c in reversed(classes):
            try:
                group = c.groups_by_name[group.name]
            except KeyError:
                continue
            
            properties.extend(group.properties)
            methods.extend(group.methods)

        if properties:
            items = list()
            items.append(("Property", "Summary", "Type", "Default value",
                          "Mutable", "Nullable"))

            for prop in properties:
                link = _html_node_link(prop)
                summary = _html_node_summary(prop)
                type = _html_parameter_type(prop)
                value = _html_parameter_value(prop)
                mutable = _html_boolean(prop.mutable)
                nullable = _html_boolean(prop.nullable)

                if value and value.startswith("[") and value.endswith("]"):
                    value = html_span(value[1:-1], class_="special")
                
                items.append((link, summary, type, value, mutable, nullable))

            out.write(html_table(items, class_="pumpjack properties"))

        if methods:
            items = list()
            items.append(("Method", "Summary", "Inputs", "Outputs"))
                            
            for meth in methods:
                link = _html_node_link(meth)
                summary = _html_node_summary(meth)

                inputs = list()
                outputs = list()

                if meth.inputs:
                    for input in meth.inputs:
                        inputs.append(_html_input(input))

                if meth.outputs:
                    for output in meth.outputs:
                        outputs.append(_html_parameter_type(output))
                            
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
                
            out.write(_html_node_title(prop))
            out.write(_html_node_text(prop))

            items = (
                ("Type", _html_parameter_type(prop)),
                ("Default value", _html_parameter_value(prop)),
                ("Mutable", prop.mutable),
                ("Nullable", prop.nullable),
            )

            out.write(html_table(items, False, True, class_="props"))

    def render_method(self, out, meth):
        output_path = meth.get_output_path(self.output_dir)
        
        print("Rendering {} to {}".format(meth, output_path))

        with _open_output(output_path) as f:
            out = PumpjackWriter(f)

            out.write(_html_node_title(meth))
            out.write(_html_node_text(meth))
            out.write(_html_node_links(meth))

            if meth.inputs:
                self.render_method_inputs(out, meth)

            if meth.outputs:
                self.render_method_outputs(out, meth)

    def render_method_inputs(self, out, meth):
        items = list()
        items.append(("Input", "Type", "Default value", "Nullable"))
        
        for input in meth.inputs:
            name = input.name
            type = _html_parameter_type(input)
            value = _html_parameter_value(input)
            nullable = _html_boolean(input.nullable)
            
            items.append((name, type, value, nullable))

        out.write(html_table(items, class_="parameters"))

    def render_method_outputs(self, out, meth):
        items = list()
        items.append(("Output", "Type", "Nullable"))
        
        for output in meth.outputs:
            name = output.name
            type = _html_parameter_type(output)
            nullable = _html_boolean(output.nullable)
            
            items.append((name, type, nullable))

        out.write(html_table(items, class_="parameters"))

add_renderer("html", HtmlRenderer)

def _html_node_title(node):
    type = init_cap(node.node_type)
    name = html_span(node.name, class_="name")
    title = "{} {}".format(type, name)

    return html_h(title, class_="pumpjack")

def _html_node_link(node):
    return html_a(_html_special(node.name), node.get_url())

def _html_node_summary(node):
    return first_sentence(node.text)

_markdown_extras = {}
_markdown = _markdown2.Markdown(extras=_markdown_extras)

def _html_node_text(node):
    if not node.text:
        return ""

    text = _dedent_text(node.text)
    
    return _markdown.convert(text)

def _html_node_links(node):
    items = list()
    
    for link in node.links:
        items.append(html_a(link[0], link[1]))

    return html_ul(items, class_="pumpjack links")

def _html_parameter_type(param):
    type = _html_reference(param, param.type)

    if param.item_type is not None:
        type = "{} of {}".format(type, _html_reference(param, param.item_type))

    return type

def _html_input(input):
    if input.type in input.model.type_names:
        return input.name

    return _html_parameter_type(input)

def _html_parameter_value(param):
    return _html_special(param.value)

def _html_reference(node, ref):
    if ref is not None and ref.startswith("@"):
        node = node.resolve_reference(ref)

        if node is not None:
            return html_a(node.name, node.get_url())

    return ref

def _html_special(value):
    if value is not None and value.startswith("[") and value.endswith("]"):
        value = html_span(value[1:-1], class_="special")

    return value

def _html_boolean(value):
    if isinstance(value, basestring):
        value = value == "true"
    
    return "&#x2612;" if value else "&#x2610;"

def _dedent_text(text):
    if text[0] == "\n":
        text = text[1:]

    lines = text.splitlines(True)

    if len(lines) == 1:
        return text

    for line in lines[1:]:
        if line == "\n":
            continue
        
        for i, c in enumerate(line):
            if not c == ' ':
                break

        trim_index = i

        break

    out = [lines[0]]
    out += [l if l == "\n" else l[trim_index:] for l in lines[1:]]
    
    return "".join(out)

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
