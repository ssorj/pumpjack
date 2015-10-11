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
        
    def process(self):
        print("Processing {}".format(self))
        
        self.process_attributes()
        self.process_text()
        self.process_links()
        self.process_annotations()

        for child in self.children:
            child.process()
        
    def process_attributes(self):
        self.title = self.element.attrib.get("title")
        
    def process_text(self):
        self.text = self.element.text

        if self.text:
            self.text = self.text.strip()

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
            node = None

            for ancestor in self.ancestors:
                if isinstance(ancestor, _Module):
                    node = ancestor
                    break

            if node:
                name = ref[1:]

                try:
                    return node.children_by_name[name]
                except KeyError:
                    msg = "Cannot find child '{}' on node '{}'"
                    raise Exception(msg.format(name, node.name))

class _Module(_Node):
    def __init__(self, element, parent):
        super(_Module, self).__init__(element, parent)

        self.model = parent

        self.groups = list()

    def process(self):
        for child in self.element.findall("group"):
            group = _ModuleGroup(child, self)
            self.groups.append(group)

        super(_Module, self).process()

class _ModuleGroup(_Node):
    def __init__(self, element, parent):
        super(_ModuleGroup, self).__init__(element, parent)

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

        self.module = parent.parent

        self.constructor = None

        self.type = self.element.attrib.get("type")

        self.attributes = list()
        self.methods = list()
        self.constants = list()
        self.enumerations = list()

        self.html_id = "C{}".format(self.parent.children.index(self) + 1)

    def process(self):
        for child in self.element.findall("attribute"):
            attr = _Attribute(child, self)
            self.attributes.append(attr)

        child = self.element.find("constructor")

        if child is not None:
            self.constructor = _Method(child, self)
            self.methods.append(self.constructor)

        for child in self.element.findall("method"):
            meth = _Method(child, self)
            self.methods.append(meth)

        for child in self.element.findall("constant"):
            const = _Constant(child, self)
            self.constants.append(const)

        for child in self.element.findall("enumeration"):
            enum = _Enumeration(child, self)
            self.enumerations.append(enum)

        super(_Class, self).process()
        
class _Enumeration(_Node):
    def __init__(self, element, parent):
        super(_Enumeration, self).__init__(element, parent)

        self.module = parent.parent

        self.constants = list()
        self.constants_by_group = _defaultdict(list)

    def process(self):
        for child in self.element.findall("constant"):
            const = _Constant(child, self)
            self.constants.append(const)
            self.constants_by_group[const.group].append(const)

        super(_Enumeration, self).process()

class _Parameter(_Node):
    def __init__(self, element, parent):
        super(_Parameter, self).__init__(element, parent)

        self.type = self.element.attrib.get("type")
        self.value = self.element.attrib.get("value")
        self.nullable = self.element.attrib.get("nullable", False)

class _Constant(_Parameter):
    def __init__(self, element, parent):
        super(_Constant, self).__init__(element, parent)

class _Attribute(_Parameter):
    def __init__(self, element, parent):
        super(_Attribute, self).__init__(element, parent)

        self.writeable = True
        self.readable = True

        writeable = self.element.attrib.get("writeable")
        readable = self.element.attrib.get("readable")

        if writeable == "false":
            self.writeable = False

        if readable == "false":
            self.readable = False

        args = self.parent.html_id, self.parent.children.index(self) + 1
        self.html_id = "{}.{}".format(*args)

class _Method(_Node):
    def __init__(self, element, parent):
        super(_Method, self).__init__(element, parent)

        self.inputs = list()
        self.outputs = list()
        self.error_conditions = list()

        args = self.parent.html_id, self.parent.children.index(self)
        self.html_id = "{}.{}".format(*args)

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

        self.html_id = "E{}".format(self.parent.children.index(self))

class _Type(_Node):
    def __init__(self, element, parent):
        super(_Type, self).__init__(element, parent)

class Model(_Node):
    def __init__(self, element):
        super(Model, self).__init__(element, None)

        self.modules = list()
        self.types = list()

    def process(self):
        for child in self.element.findall("module"):
            module = _Module(child, self)
            self.modules.append(module)

        for child in self.element.findall("type"):
            type = _Type(child, self)
            self.types.append(type)

        super(Model, self).process()

def _format_repr(obj, *args):
    cls = obj.__class__.__name__
    strings = [str(x) for x in args]
    return "{}({})".format(cls, ",".join(strings))
