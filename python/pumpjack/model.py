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

from pencil import *

import os as _os

from collections import defaultdict as _defaultdict

class _Node:
    def __init__(self, element, parent):
        self.element = element

        self.node_type = self.element.tag
        self.name = self.element.attrib["name"]
        
        self.title = None
        self.text = None
        self.links = list()
        self.links_by_relation = _defaultdict(list)
        self.annotations = dict()

        self.hidden = False
        self.internal = False
        self.proposed = False
        self.deprecated = False
        self.experimental = False
        
        self.parent = parent
        self.ancestors = list()
        self.children = list()
        self.children_by_name = dict()

        self.model = None
        self.reference = None
        
        if self.parent:
            if self.name in self.parent.children_by_name:
                raise Exception("Collision! {}".format(self.name))
            
            self.parent.children.append(self)
            self.parent.children_by_name[self.name] = self

            node = self
            reference_items = [self.name]
            
            while node.parent:
                node = node.parent
                self.ancestors.append(node)

                if not isinstance(node, _Group):
                    reference_items.append(node.name)

            self.model = node

            self.reference = "/{}".format("/".join(reversed(reference_items)))
            self.model.nodes_by_reference[self.reference] = self
        
    def __repr__(self):
        return format_repr(self, self.reference)

    @property
    def abstract_path(self):
        raise NotImplementedError()

    @property
    def url(self): 
        site_url="{{{{site_url}}}}" # XXX why doubled?
        elems = [site_url] + list(self.abstract_path)
        return "/".join(elems)

    def output_path(self, output_dir):
        path = _os.path.join(output_dir, *self.abstract_path)

        return "{}.in".format(path)

    def process(self):
        print("Processing {}".format(self))
        
        self.process_properties()
        self.process_text()
        self.process_annotations()

        for child in self.children:
            child.process()
        
    def process_properties(self):
        self.title = self.element.attrib.get("title")

        self.hidden = self.element.attrib.get("hidden", "false") == "true"
        self.internal = self.element.attrib.get("internal", "false") == "true"
        self.proposed = self.element.attrib.get("proposed", "false") == "true"
        self.deprecated = self.element.attrib.get \
                          ("deprecated", "false") == "true"
        self.experimental = self.element.attrib.get \
                            ("experimental", "false") == "true"
        
    def process_text(self):
        text = self.element.text

        if text:
            text = text.strip()

        if text != "":
            self.text = text

    def process_annotations(self):
        for child in self.element.findall("annotation"):
            self.annotations[child.attrib["name"]] = child.text
            
    def process_references(self):
        print("Processing references for {}".format(self))

        for child in self.element.findall("link"):
            relation = child.attrib.get("relation")
            
            if "node" in child.attrib:
                node = self.resolve_reference(child.attrib["node"])
                text = "{} {}".format(init_cap(node.node_type), node.name)
                href = node.url
            else:
                text = child.text
                href = child.attrib["href"]
                
            self.links.append((text, href))
            self.links_by_relation[relation].append((text, href))

        for child in self.children:
            child.process_references()

    def resolve_reference(self, ref):
        # Find nodes by fully qualified paths

        if ref.startswith("/"):
            try:
                return self.model.nodes_by_reference[ref]
            except KeyError:
                raise Exception("Cannot find reference '{}'".format(ref))

        module = self.find_ancestor(_Module)

        if module:
            node = None

            for group in module.groups:
                if ref in group.children_by_name:
                    node = group.children_by_name[ref]
                    break
            else:
                msg = "Cannot find child '{}' on module '{}'"
                raise Exception(msg.format(ref, module.name))

            return node

    def find_ancestor(self, cls):
        for ancestor in self.ancestors:
            if isinstance(ancestor, cls):
                return ancestor

class _Group(_Node):
    def process_references(self):
        super().process_references()

        if self.name in self.model.group_definitions_by_name:
            definition = self.model.group_definitions_by_name[self.name]
        
            if self.title is None:
                self.title = definition.title

            if self.text is None:
                self.text = definition.text
        
class _GroupDefinition(_Node):
    pass

class _Module(_Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.groups = list()

    @property
    def abstract_path(self):
        return (self.name, "index.html")

    def process(self):
        for child in self.element.findall("group"):
            group = _ModuleGroup(child, self)
            self.groups.append(group)

        super(_Module, self).process()

class _ModuleGroup(_Group):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.module = parent
        
        self.classes = list()
        self.enumerations = list()

    def process(self):
        for child in self.element.findall("class"):
            cls = _Class(child, self)
            self.classes.append(cls)

        for child in self.element.findall("enumeration"):
            enum = _Enumeration(child, self)
            self.enumerations.append(enum)

        super().process()

class _Type(_Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

class _Class(_Type):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.group = parent
        self.module = self.group.parent

        self.type = None

        self.groups = list()
        self.groups_by_name = dict()

    @property
    def abstract_path(self):
        return (self.module.name, self.name, "index.html")
        
    def process_properties(self):
        super().process_properties()

        self.type = self.element.attrib.get("type")
        
    def process(self):
        for child in self.element.findall("group"):
            group = _ClassGroup(child, self)
            self.groups.append(group)
            self.groups_by_name[group.name] = group

        super().process()

    def process_references(self):
        super().process_references()

        if self.type is not None:
            self.type = self.resolve_reference(self.type)

        annotations = self.module.annotations
        
        if "class-link-function" in annotations:
            text_template = annotations["class-link-text-template"]
            href_template = annotations["class-link-href-template"]
            func = globals()[annotations["class-link-function"]]
            
            link = func(self, text_template, href_template)

            if link is not None:
                self.links.append(link)

class _ClassGroup(_Group):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.class_ = parent

        self.properties = list()
        self.methods = list()
        self.constants = list()

    def process(self):
        for child in self.element.findall("property"):
            attr = _Property(child, self)
            self.properties.append(attr)

        for child in self.element.findall("method"):
            meth = _Method(child, self)
            self.methods.append(meth)

        super().process()
        
class _ClassMember(_Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.group = parent
        self.class_ = self.group.parent

    @property
    def abstract_path(self):
        name = "{}.html".format(self.name)
        return (self.class_.module.name, self.class_.name, name)

class _Parameter(_Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.type = self.element.attrib.get("type")
        self.key_type = self.element.attrib.get("key-type")
        self.item_type = self.element.attrib.get("item-type")
        self.value = self.element.attrib.get("value")
        self.nullable = self.element.attrib.get("nullable", "false") == "true"

    def process_properties(self):
        super().process_properties()

        if self.value is None:
            if self.nullable:
                self.value = "null"
            else:
                self.value = "[instance]"
        
    def process_references(self):
        super().process_references()

        if self.type is not None:
            self.type = self.resolve_reference(self.type)

        if self.key_type is not None:
            self.key_type = self.resolve_reference(self.key_type)

        if self.item_type is not None:
            self.item_type = self.resolve_reference(self.item_type)

class _Property(_ClassMember, _Parameter):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.mutable = self.element.attrib.get("mutable", "false") == "true"

class _Input(_Parameter):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.optional = self.element.attrib.get("optional", "false") == "true"
                
class _Method(_ClassMember):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.inputs = list()
        self.outputs = list()
        self.error_conditions = list()

    def process(self):
        for child in self.element.findall("input"):
            input = _Input(child, self)
            self.inputs.append(input)

        for child in self.element.findall("output"):
            output = _Parameter(child, self)
            self.outputs.append(output)

        for child in self.element.findall("error-condition"):
            cond = _ErrorCondition(child, self)
            self.error_conditions.append(cond)

        super().process()

class _Enumeration(_Type):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.group = parent
        self.module = self.group.parent

        self.values = list()

    @property
    def abstract_path(self):
        name = "{}.html".format(self.name)
        return (self.module.name, name)

    def process(self):
        for child in self.element.findall("value"):
            value = _Value(child, self)
            self.values.append(value)
        
        super().process()

class _Value(_Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.enumeration = self.parent
    
class _ErrorCondition(_Node):
    def __init__(self, element, parent):
        super(_ErrorCondition, self).__init__(element, parent)
        self.error_ref = self.element.attrib["error"]
        self.error = None

    def process_references(self):
        self.error = self.resolve_reference(self.error_ref)

        super().process_references()

class _Error(_Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

class Model(_Node):
    def __init__(self, element):
        super().__init__(element, None)

        self.modules = list()
        self.group_definitions_by_name = dict()

        self.nodes_by_reference = dict()
        
    @property
    def abstract_path(self):
        return ("index.html",)

    def process(self):
        for child in self.element.findall("module"):
            module = _Module(child, self)
            self.modules.append(module)

        for child in self.element.findall("group-definition"):
            definition = _GroupDefinition(child, self)
            self.group_definitions_by_name[definition.name] = definition

        super().process()

def _gen_amqp_type_link(class_, text_template, href_template):
    if not class_.name.startswith("amqp-"):
        return
    
    text = text_template
    href = href_template.format(class_.name[5:])

    return text, href
