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

import collections as _collections
import markdown2 as _markdown2
import os as _os
import re as _re

_markdown_extras = {
    "header-ids": True,
}

_markdown = _markdown2.Markdown(extras=_markdown_extras)

class HtmlRenderer(Renderer):
    def __init__(self, output_dir):
        super().__init__(output_dir)

    def get_node_path(self, node, prefix):
        elems = [prefix]
        elems.extend(node.abstract_path)
    
        if type(node) in (Model, Module, Class):
            elems.append("index")

        return "{}.html".format("/".join(elems))
        
    def get_node_output_path(self, node):
        return "{}.in".format(self.get_node_path(node, self.output_dir))

    def get_node_href(self, node):
        site_url = "{{{{site_url}}}}" # XXX why doubled?
        return self.get_node_path(node, site_url)

    def get_node_flags(self, node):
        flags = list()

        if node.internal:
            flags.append(html_span("internal", class_="flag"))
            
        if node.proposed:
            flags.append(html_span("proposed", class_="flag"))

        if node.deprecated:
            flags.append(html_span("deprecated", class_="flag"))
            
        if node.experimental:
            flags.append(html_span("experimental", class_="flag"))

        return " ".join(flags)

    def get_node_name(self, node):
        name = node.name

        if isinstance(node, ClassMember):
            name = "{}.{}".format(node.class_.name, node.name)

        return name

    def get_node_link(self, node):
        class_ = None
        
        if node.special:
            class_ = "special"

        name = self.get_node_name(node)
        href = self.get_node_href(node)

        return html_a(name, href)

    def get_node_table_link(self, node):
        class_ = None
        
        if node.special:
            class_ = "special"

        href = self.get_node_href(node)
        flags = self.get_node_flags(node)
        link = html_a(node.name, href, class_=class_, id=node.name)

        return "{} {}".format(link, flags)

    def get_node_summary(self, node):
        return first_sentence(node.text)

    def get_parameter_type(self, param):
        type = self.get_node_link(param.type)
        key_type = None
        item_type = None

        if param.key_type is not None:
            key_type = self.get_node_link(param.key_type)

        if param.item_type is not None:
            item_type = self.get_node_link(param.item_type)

        if key_type is not None:
            type = "{} of {} &#8658; {}".format(type, key_type, item_type)
        elif item_type is not None:
            type = "{} of {}".format(type, item_type)

        return type

    def get_parameter_value(self, param):
        return _special_value(param.value)
    
    def get_method_input(self, input):
        name = input.name
        href = self.get_node_href(input.type)

        if input.optional:
            name = "[{}]".format(name)
            name = html_span(name, _class="optional")
        
        return html_a(name, href)
    
    def render(self, model):
        path = self.get_node_output_path(model)

        with OutputWriter(path) as out:
            self.render_model(out, model)

    def render_node_title(self, out, node):
        out.write(html_h(node.title, id=node.name))
        
    def render_node_heading(self, out, node):
        assert isinstance(node, Node), node

        name = self.get_node_name(node)
        name = html_span(name, class_="name")
        
        type_ = init_cap(node.type_name)
        flags = self.get_node_flags(node)
        text = "{} {} {}".format(type_, name, flags)

        out.write(html_h(text, class_="pumpjack", id=node.name))

    def render_node_doc(self, out, node):
        if node.text is not None:
            text = dedent_text(node.text)
            text = _markdown.convert(text)
        
            out.write(text)
            
        self.render_node_links_for_relation(out, node, None, "Related")
        self.render_node_links_for_relation(out, node, "impl", "Implementations")
        self.render_node_links_for_relation(out, node, "amqp", "AMQP")

    def render_node_links_for_relation(self, out, node, relation, label):
        links = list()
        
        for link in node.links_by_relation[relation]:
            if isinstance(link, Node):
                name = self.get_node_name(link)
                text = "{} {}".format(init_cap(link.type_name), name)
                href = self.get_node_href(link)
                link = text, href

            links.append(html_a(link[0], link[1]))

        if not links:
            return

        links = html_p("{}: {}".format(label, ", ".join(links)))
        
        out.write(links)

    def render_model(self, out, model):
        print("Rendering {}".format(model))

        self.render_node_title(out, model)
        self.render_node_doc(out, model)
        
        out.write(html_open("section"))
        out.write(html_h("Modules"))

        items = list()
        items.append(("Module", "Content", "Depends on"))

        for module in model.modules:
            link = self.get_node_table_link(module)
            summary = self.get_node_summary(module)
            requires = module.annotations.get("requires")
            
            items.append((link, summary, requires))

        out.write(html_table(items, class_="pumpjack modules"))
        out.write(html_close("section"))
        
        for module in model.modules:
            self.render_module(out, module)

    def render_module(self, out, module):
        path = self.get_node_output_path(module)
        
        print("Rendering {} to {}".format(module, path))

        with OutputWriter(path) as out:
            self.render_node_heading(out, module)
            self.render_node_doc(out, module)

            for group in module.groups:
                self.render_class_group(out, group)

            for group in module.groups:
                for cls in group.classes:
                    self.render_class(out, cls)

                for enum in group.enumerations:
                    self.render_enumeration(out, enum)

    def render_class_group(self, out, group):
        out.write(html_open("section"))
        
        self.render_node_title(out, group)
        self.render_node_doc(out, group)

        items = list()
        items.append(("Class", "Summary"))
                        
        for cls in group.classes:
            link = self.get_node_table_link(cls)
            summary = first_sentence(cls.text)

            if cls.hidden or cls.internal:
                continue

            items.append((link, summary))

        out.write(html_table(items, class_="pumpjack classes"))
        out.write(html_close("section"))

    def render_class(self, out, cls):
        path = self.get_node_output_path(cls)
        
        print("Rendering {} to {}".format(cls, path))

        groups = _collections.OrderedDict()
        basic_group = None

        for c in cls.classes:
            for group in c.groups:
                if group.name == "basic":
                    basic_group = group
                    continue
                
                groups[group.name] = group

        groups = list(groups.values())

        if basic_group is not None:
            groups.insert(0, basic_group)

        with OutputWriter(path) as out:
            self.render_node_heading(out, cls)
            self.render_node_doc(out, cls)

            for group in groups:
                self.render_class_member_group(out, cls, group)

            for group in cls.groups:
                for prop in group.properties:
                    self.render_property(out, prop)

                for meth in group.methods:
                    self.render_method(out, meth)

    def render_class_member_group(self, out, cls, group):
        if group.hidden or group.internal:
            return
        
        id = group.title.lower().replace(" ", "-")
        
        out.write(html_open("section"))

        self.render_node_title(out, group)
        self.render_node_doc(out, group)

        if group.virtual_properties:
            items = list()
            items.append(("Property", "Summary", "Type", "Default value",
                          "Mutable", "Nullable"))

            for prop in group.virtual_properties:
                if prop.hidden or prop.internal:
                    continue
                
                link = self.get_node_table_link(prop)
                summary = self.get_node_summary(prop)
                type = self.get_parameter_type(prop)
                value = self.get_parameter_value(prop)
                mutable = _boolean_tick_box(prop.mutable)
                nullable = _boolean_tick_box(prop.nullable)

                items.append((link, summary, type, value, mutable, nullable))

            out.write(html_table(items, class_="pumpjack properties"))

        if group.virtual_methods:
            items = list()
            items.append(("Method", "Summary", "Inputs", "Outputs"))
                            
            for meth in group.virtual_methods:
                if meth.hidden or meth.internal:
                    continue
                
                link = self.get_node_table_link(meth)
                summary = self.get_node_summary(meth)

                inputs = list()
                outputs = list()

                if meth.inputs:
                    for input in meth.inputs:
                        inputs.append(self.get_method_input(input))

                if meth.outputs:
                    for output in meth.outputs:
                        outputs.append(self.get_parameter_type(output))
                            
                inputs = ", ".join(inputs)
                outputs = ", ".join(outputs)

                items.append((link, summary, inputs, outputs))

            out.write(html_table(items, class_="pumpjack methods"))

        out.write(html_close("section"))

    def render_property(self, out, prop):
        path = self.get_node_output_path(prop)
        
        print("Rendering {} to {}".format(prop, path))

        with OutputWriter(path) as out:
            self.render_node_heading(out, prop)
            self.render_node_doc(out, prop)

            items = (
                ("Type", self.get_parameter_type(prop)),
                ("Default value", self.get_parameter_value(prop)),
                ("Mutable", _boolean_text(prop.mutable)),
                ("Nullable", _boolean_text(prop.nullable)),
            )

            out.write(html_table(items, False, True, class_="props"))
            
            if type(prop.type) is Enumeration:
                text = "Enumeration {}".format(prop.type.name)

                out.write(html_elem("h2", text))
                
                self.render_enumeration_table(out, prop.type)

    def render_method(self, out, meth):
        path = self.get_node_output_path(meth)
        
        print("Rendering {} to {}".format(meth, path))

        with OutputWriter(path) as out:
            self.render_node_heading(out, meth)
            self.render_node_doc(out, meth)

            if meth.inputs:
                self.render_method_inputs(out, meth)

            if meth.outputs:
                self.render_method_outputs(out, meth)

    def render_method_inputs(self, out, meth):
        items = list()
        items.append(("Input", "Type", "Default value", "Nullable", "Optional"))
        
        for input in meth.inputs:
            name = input.name
            type = self.get_parameter_type(input)
            value = self.get_parameter_value(input)
            nullable = _boolean_tick_box(input.nullable)
            optional = _boolean_tick_box(input.optional)
            
            items.append((name, type, value, nullable, optional))

        out.write(html_table(items, class_="parameters"))

    def render_method_outputs(self, out, meth):
        items = list()
        items.append(("Output", "Type", "Nullable"))
        
        for output in meth.outputs:
            name = output.name
            type = self.get_parameter_type(output)
            nullable = _boolean_tick_box(output.nullable)
            
            items.append((name, type, nullable))

        out.write(html_table(items, class_="parameters"))

    def render_enumeration(self, out, enum):
        path = self.get_node_output_path(enum)

        print("Rendering {} to {}".format(enum, path))

        with OutputWriter(path) as out:
            self.render_node_heading(out, enum)
            self.render_node_doc(out, enum)

            self.render_enumeration_table(out, enum)

    def render_enumeration_table(self, out, enum):
        items = list()
        items.append(("Name", "Summary"))
        
        for value in enum.values:
            name = value.name
            summary = self.get_node_summary(value)

            items.append((name, summary))

        out.write(html_table(items))
                    
add_renderer("html", HtmlRenderer)

def _special_value(value):
    if value is not None and value.startswith("[") and value.endswith("]"):
        value = html_span(value[1:-1], class_="special")

    return value

def _boolean_tick_box(value):
    if isinstance(value, str):
        value = value == "true"
    
    return "&#x2612;" if value else "&#x2610;"

def _boolean_text(value):
    if isinstance(value, str):
        value = value == "true"
    
    return "Yes" if value else "No"
