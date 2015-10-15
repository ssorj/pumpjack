#!/usr/bin/python
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

from __future__ import print_function

from format import *

import os as _os

from collections import defaultdict as _defaultdict

class _Node(object):
    def __init__(self, element, parent):
        self.element = element

        self.name = self.element.attrib["name"]
        
        self.title = None
        self.text = None
        self.links = list()
        self.annotations = dict()

        self.parent = parent
        self.ancestors = list()
        self.children = list()
        self.children_by_name = dict()

        if self.parent:
            if self.name in self.parent.children_by_name:
                raise Exception("Collision! {}".format(self.name))
            
            self.parent.children.append(self)
            self.parent.children_by_name[self.name] = self

        node = self

        while node.parent:
            node = node.parent
            self.ancestors.append(node)

        self.model = node

    def __repr__(self):
        return _format_repr(self, self.name)

    @property
    def abstract_path(self):
        raise NotImplementedError()
    
    def get_output_path(self, output_dir):
        path = _os.path.join(output_dir, *self.abstract_path)

        return "{}.in".format(path)

    def get_url(self, site_url="{{{{site_url}}}}"): # XXX why doubled?
        elems = [site_url] + list(self.abstract_path)
        return "/".join(elems)

    def process(self):
        print("Processing {}".format(self))
        
        self.process_properties()
        self.process_text()
        self.process_links()
        self.process_annotations()

        for child in self.children:
            child.process()
        
    def process_properties(self):
        self.title = self.element.attrib.get("title")
        
    def process_text(self):
        text = self.element.text

        if text:
            text = text.strip()

        if text != "":
            self.text = text

    def process_links(self):
        for child in self.element.findall("link"):
            self.links.append((child.text, child.attrib["href"]))

    def process_annotations(self):
        for child in self.element.findall("annotation"):
            self.annotations[child.attrib["name"]] = child.text
            
    def process_references(self):
        print("Processing references for {}".format(self))

        for child in self.children:
            child.process_references()

    def resolve_reference(self, ref):
        if not ref.startswith("@"):
            raise Exception("'{}' doesn't look like a ref".format(ref))

        if ref.startswith("@/"):
            path = ref[2:].split("/")[1:]

            name = None
            node = self.model

            while path:
                name = path.pop(0)

                try:
                    node = node.children_by_name[name]
                except KeyError:
                    msg = "Cannot find child '{}' on node '{}'"
                    raise Exception(msg.format(name, node.name))

            return node
        else:
            module = None

            for ancestor in self.ancestors:
                if isinstance(ancestor, _Module):
                    module = ancestor
                    break

            if module:
                name = ref[1:]
                node = None

                for group in module.groups:
                    if name in group.children_by_name:
                        node = group.children_by_name[name]
                        break
                else:
                    msg = "Cannot find child '{}' on module '{}'"
                    raise Exception(msg.format(name, module.name))

                return node

class _GroupDefinition(_Node):
    pass

class _Module(_Node):
    def __init__(self, element, parent):
        super(_Module, self).__init__(element, parent)

        self.groups = list()

    @property
    def abstract_path(self):
        return (self.name, "index.html")

    def process(self):
        for child in self.element.findall("group"):
            group = _ModuleGroup(child, self)
            self.groups.append(group)

        super(_Module, self).process()

class _ModuleGroup(_Node):
    def __init__(self, element, parent):
        super(_ModuleGroup, self).__init__(element, parent)

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

        super(_ModuleGroup, self).process()

class _Class(_Node):
    def __init__(self, element, parent):
        super(_Class, self).__init__(element, parent)

        self.group = parent
        self.module = self.group.parent

        self.type = None

        self.groups = list()
        self.groups_by_name = dict()

    @property
    def abstract_path(self):
        return (self.module.name, self.name, "index.html")
        
    def process_properties(self):
        super(_Class, self).process_properties()

        self.type = self.element.attrib.get("type")
        
    def process(self):
        for child in self.element.findall("group"):
            group = _ClassGroup(child, self)
            self.groups.append(group)
            self.groups_by_name[group.name] = group

        super(_Class, self).process()

    def process_references(self):
        super(_Class, self).process_references()

        if self.type is not None:
            self.type = self.resolve_reference(self.type)

class _ClassGroup(_Node):
    def __init__(self, element, parent):
        super(_ClassGroup, self).__init__(element, parent)

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

        for child in self.element.findall("constant"):
            const = _Constant(child, self)
            self.constants.append(const)

        super(_ClassGroup, self).process()
        
    def process_references(self):
        super(_ClassGroup, self).process_references()

        if self.name in self.model.group_definitions_by_name:
            definition = self.model.group_definitions_by_name[self.name]
        
            if self.title is None:
                self.title = definition.title

            if self.text is None:
                self.text = definition.text
        
class _ClassMember(_Node):
    def __init__(self, element, parent):
        super(_ClassMember, self).__init__(element, parent)

        self.group = parent
        self.class_ = self.group.parent

    @property
    def abstract_path(self):
        name = "{}.html".format(self.name)

        return (self.class_.module.name, self.class_.name, name)

class _Parameter(_Node):
    def __init__(self, element, parent):
        super(_Parameter, self).__init__(element, parent)

        self.type = self.element.attrib.get("type")
        self.value = self.element.attrib.get("value")
        self.nullable = self.element.attrib.get("nullable", False)

# class _Constant(_Parameter):
#     def __init__(self, element, parent):
#         super(_Constant, self).__init__(element, parent)

class _Property(_ClassMember, _Parameter):
    def __init__(self, element, parent):
        super(_Property, self).__init__(element, parent)

        self.mutable = self.element.attrib.get("mutable", "false") == "true"

class _Method(_ClassMember):
    def __init__(self, element, parent):
        super(_Method, self).__init__(element, parent)

        self.inputs = list()
        self.outputs = list()
        self.error_conditions = list()

    def process(self):
        for child in self.element.findall("input"):
            input = _Parameter(child, self)
            self.inputs.append(input)

        for child in self.element.findall("output"):
            output = _Parameter(child, self)
            self.outputs.append(output)

        for child in self.element.findall("error-condition"):
            cond = _ErrorCondition(child, self)
            self.error_conditions.append(cond)

        super(_Method, self).process()

class _ErrorCondition(_Node):
    def __init__(self, element, parent):
        super(_ErrorCondition, self).__init__(element, parent)
        self.error_ref = self.element.attrib["error"]
        self.error = None

    def process_references(self):
        self.error = self.resolve_reference(self.error_ref)

        super(_ErrorCondition, self).process_references()

class _Error(_Node):
    def __init__(self, element, parent):
        super(_Error, self).__init__(element, parent)

class _Type(_Node):
    def __init__(self, element, parent):
        super(_Type, self).__init__(element, parent)

class Model(_Node):
    def __init__(self, element):
        super(Model, self).__init__(element, None)

        self.modules = list()
        self.types = list()
        self.group_definitions_by_name = dict()

    @property
    def abstract_path(self):
        return ("index.html",)

    def process(self):
        for child in self.element.findall("module"):
            module = _Module(child, self)
            self.modules.append(module)

        for child in self.element.findall("type"):
            type = _Type(child, self)
            self.types.append(type)

        for child in self.element.findall("group-definition"):
            definition = _GroupDefinition(child, self)
            self.group_definitions_by_name[definition.name] = definition

        super(Model, self).process()

def _format_repr(obj, *args):
    cls = obj.__class__.__name__
    strings = [str(x) for x in args]

    return "{}({})".format(cls, ",".join(strings))
