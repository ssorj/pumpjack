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
        output_path = _os.path.join(self.output_dir, "index.html.in")

        if not _os.path.exists(self.output_dir):
            _os.makedirs(self.output_dir)

        with open(output_path, "w") as f:
            out = PumpjackWriter(f)
            self.render_model(out, model)
    
    def render_model(self, out, model):
        out.write(html_h(init_cap(model.name)))
        out.write(html_text(model.text))

        items = list()
        
        for link in model.links:
            items.append(html_a(link[0], link[1]))

        out.write(html_ul(items, class_="links two-column"))

        out.write(html_open("section"))
        out.write(html_h("Modules"))

        items = list()
        items.append(("Module", "Content", "Depends on"))

        for module in model.modules:
            name = "{} {}".format(init_cap(module.parent.name), init_cap(module.name))
            link = html_a(name, "{}/index.html".format(module.name))
            summary = first_sentence(module.text)
            requires = module.annotations.get("requires")

            items.append((link, summary, requires))

        out.write(html_table(items))
        out.write(html_close("section"))
        
        for module in model.modules:
            self.render_module(out, module)

    def render_module(self, out, module):
        output_dir = _os.path.join(self.output_dir, module.name)
        output_path = _os.path.join(output_dir, "index.html.in")

        if not _os.path.exists(output_dir):
            _os.makedirs(output_dir)
        
        with open(output_path, "w") as f:
            out = PumpjackWriter(f)

            args = init_cap(module.model.name), init_cap(module.name)
            title = "{} {}".format(*args)

            out.write(html_h(title))
            
            out.write(html_text(module.text))
            #out.write(self.include_file("module.html"))

            if module.classes:
                out.write(html_section_open("Classes"))
                
                for cls in module.classes:
                    self.render_class(out, cls)

                out.write(html_section_close())

            if module.errors:
                out.write(html_section_open("Errors"))
                
                for error in module.errors:
                    self.render_error(out, error)

                out.write(html_section_close())

    def render_class(self, out, cls):
        output_dir = _os.path.join(self.output_dir, cls.parent.name)
        output_name = "{}.html.in".format(cls.name)
        output_path = _os.path.join(output_dir, output_name)

        if not _os.path.exists(output_dir):
            _os.makedirs(output_dir)
        
        with open(output_path, "w") as f:
            out = PumpjackWriter(f)
        
            title = "{}. {}".format(cls.doc_id, cls.name)
            
            out.write(html_section_open(title, "class", toggle_visibility=True))
            out.write(html_text(cls.text))
            out.write(self.include_file("{}.class.html".format(cls.name)))

            if cls.attributes:
                out.write(html_section_open("Attributes", "attributes"))

                for attr in cls.attributes:
                    self.render_attribute(out, attr)

                out.write(html_section_close())

            methods = [x for x in cls.methods if not x.private]

            if methods:
                out.write(html_section_open("Methods", "methods"))

                for meth in methods:
                    self.render_method(out, meth)

                out.write(html_section_close())

            out.write(html_section_close())

    def render_error(self, out, error):
        title = "{}. {}".format(error.doc_id, error.name)

        out.write(html_section_open(title, "error", toggle_visibility=True))
        out.write(html_text(error.text))
        out.write(self.include_file("{}.error.html", error.name))
        out.write(html_section_close())

    def render_attribute(self, out, attr):
        value = ""

        if attr.value is not None:
            value = format_node_value(attr)
            value = "= {}".format(value)
            value = html_span(value, class_="signature")

        title = "{} {}".format(attr.name, value)

        out.write(html_section_open(title, "attribute", toggle_visibility=True))

        items = (
            ("Type", attr.type),
            ("Initial value", attr.value),
            ("Nullable", attr.nullable),
        )

        out.write(html_table(items, False, True, class_="props"))

        out.write(html_text(attr.text))
        out.write(self.include_file("{}.attribute.html".format(attr.name)))
        out.write(html_section_close())

    def render_method(self, out, meth):
        signature = ", ".join([x.name for x in meth.inputs])
        signature = "({})".format(signature)

        if meth.outputs:
            output = meth.outputs[0]
            signature = "{} = {}".format(signature, format_node_value(output))

        signature = html_span(signature, class_="signature")

        title = "{} {}".format(meth.name, signature)

        out.write(html_section_open(title, "method", toggle_visibility=True))

        self.render_method_params(out, meth)

        out.write(html_text(meth.text))
        out.write(self.include_file("{}.method.html".format(meth.name)))
        out.write(html_section_close())

    def render_method_params(self, out, meth):
        items = list()
        
        for input in meth.inputs:
            items.append((input.name, input.type, str(input.nullable)))

        if not items:
            return

        out.write(html_table(items, class_="params"))

    def render_toc(self, out, nodes):
        if not nodes:
            return

        out.write(html_open("table", class_="toc"))
        out.write(html_open("tbody"))

        items = list()
        
        for node in nodes:
            items.append((node.name, first_sentence(node.text)))

        out.write(html_table(items, False, True, class_="props"))

    def render_properties(self, out, node, names):
        items = list()
        
        for name in names:
            items.append((init_cap(name), node.attrib[name]))

        out.write(html_table(items, False, True, class_="props"))

add_renderer("html", HtmlRenderer)

def html_text(text):
    if not text:
        return ""

    text = _re.sub("{", "<a href=\"\">", text) # XXX
    text = _re.sub("}", "</a>", text)

    text = _re.sub("\s*\n\s*\n\s*", " </p>\n\n<p>", text)

    return "<p>{}</p>".format(text)

section_sequence = 0 # XXX Wha?

def html_section_open(heading_text=None,
                      html_class=None,
                      toggle_visibility=False):
    global section_sequence
    section_sequence += 1

    lines = list()

    if heading_text:
        if toggle_visibility:
            attrs = dict()
            attrs["class_"] = "visibility-toggle"
            attrs["target-id"] = str(section_sequence)

            args = heading_text, html_a("&#187", "", **attrs)
            heading_text = "{} {}".format(*args)

        lines.append(html_h(heading_text))

    attrs = list()

    attrs.append("id=\"{}\"".format(section_sequence))

    if html_class:
        attrs.append("class=\"{}\"".format(html_class))

    lines.append("<section {}>".format(" ".join(attrs)))

    return "\n".join(lines)

def html_section_close():
    return "</section>"

def html_prop_table_entry(name, value):
    return "<tr><th>{}</th><td>{}</td></tr>".format(name, value)

def format_node_value(node):
    value = node.value

    if node.type == "string":
        return "'{}'".format(value)

    if node.type[0] == "@":
        return "{} instance".format(node.type[1:])

    return value
