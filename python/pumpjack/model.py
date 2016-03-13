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

from collections import defaultdict as _defaultdict
from pencil import *

import os as _os

class Node:
    def __init__(self, element, parent, name=None):
        self.element = element
        self.parent = parent
        self.name = name

        if self.name is None:
            self.name = self.element.attrib["name"]
        
        self.type_name = self.element.tag

        self.title = None
        self.text = None
        self.hidden = False
        self.internal = False
        self.proposed = False
        self.deprecated = False
        self.experimental = False
        
        self.ancestors = list()
        self.children = list()
        self.children_by_name = dict()
        
        self.links_by_relation = _defaultdict(list)
        self.annotations = dict()

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

                if not isinstance(node, Group):
                    reference_items.append(node.name)

            self.model = node

            self.reference = "/{}".format("/".join(reversed(reference_items)))
            self.model.nodes_by_reference[self.reference] = self
        
    def __repr__(self):
        return format_repr(self, self.reference)

    @property
    def abstract_path(self):
        raise NotImplementedError()

    def process(self):
        print("Processing {}".format(self))
        
        self.process_properties()
        self.process_text()
        self.process_annotations()

        for child in self.children:
            child.process()
        
    def process_properties(self):
        self.title = self.element.attrib.get("title")

        self.special = self.element.attrib.get("special", "false") == "true"
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
                link = self.resolve_reference(child.attrib["node"]) # -> node
            else:
                text = child.text
                href = child.attrib["href"]
                link = (text, href)
                
            self.links_by_relation[relation].append(link)

        if self.model is not None:
            for func in self.model.link_generators:
                func(self)

        for child in self.children:
            child.process_references()

    def resolve_reference(self, ref):
        # Find nodes by fully qualified paths

        if ref.startswith("/"):
            try:
                return self.model.nodes_by_reference[ref]
            except KeyError:
                raise Exception("Cannot find reference '{}'".format(ref))

        node = None
        module = self.find_ancestor(Module)

        # Search the current module
        
        if module:
            node = module.find_member(ref)

        # Search all the modules
            
        if node is None:
            for module in self.model.modules:
                node = module.find_member(ref)

                if node is not None:
                    break

        if node is None:
            msg = "Cannot find member '{}' on module '{}'"
            raise Exception(msg.format(ref, module.name))

        return node

    def find_ancestor(self, cls):
        for ancestor in self.ancestors:
            if isinstance(ancestor, cls):
                return ancestor

class Group(Node):
    def process_references(self):
        super().process_references()

        if self.name in self.model.group_definitions_by_name:
            definition = self.model.group_definitions_by_name[self.name]
        
            if self.title is None:
                self.title = definition.title

            if self.text is None:
                self.text = definition.text
        
class GroupDefinition(Node):
    pass

class Module(Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.groups = list()
        self.classes = list()
        self.enumerations = list()

    @property
    def abstract_path(self):
        return (self.name,)

    def process(self):
        for child in self.element.findall("group"):
            group = ModuleMemberGroup(child, self)
            self.groups.append(group)

        super().process()

    def find_member(self, ref):
        assert not ref.startswith("/")
        
        for group in self.groups:
            if ref in group.children_by_name:
                return group.children_by_name[ref]

class ModuleMemberGroup(Group):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.module = parent
        
        self.classes = list()
        self.enumerations = list()

    def process(self):
        for child in self.element.findall("class"):
            cls = Class(child, self)
            self.classes.append(cls)
            self.module.classes.append(cls)

        for child in self.element.findall("enumeration"):
            enum = Enumeration(child, self)
            self.enumerations.append(enum)
            self.module.enumerations.append(enum)

        super().process()

class ModuleMember(Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

    @property
    def abstract_path(self):
        return (self.module.name, self.name)

class Class(ModuleMember):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.group = parent
        self.module = self.group.parent

        self.type = None

        self.groups = list()
        self.groups_by_name = dict()

        self.properties = list()
        self.methods = list()

    def process_properties(self):
        super().process_properties()

        self.type = self.element.attrib.get("type")
        
    def process(self):
        for child in self.element.findall("group"):
            group = ClassMemberGroup(child, self)
            self.groups.append(group)
            self.groups_by_name[group.name] = group

        # Create a default constructor

        # XXX
            
        super().process()

    def process_references(self):
        super().process_references()

        if self.type is not None:
            self.type = self.resolve_reference(self.type)

class ClassMemberGroup(Group):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.class_ = parent

        self.properties = list()
        self.methods = list()

    def process(self):
        for child in self.element.findall("property"):
            prop = Property(child, self)
            self.properties.append(prop)
            self.class_.properties.append(prop)

        for child in self.element.findall("method"):
            meth = Method(child, self)
            self.methods.append(meth)
            self.class_.methods.append(meth)

        super().process()
        
class ClassMember(Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.group = parent
        self.class_ = self.group.parent

    @property
    def abstract_path(self):
        return (self.class_.module.name, self.class_.name, self.name)

class Parameter(Node):
    def __init__(self, element, parent):
        type_name = element.attrib.get("type")
        name = element.attrib.get("name", type_name)
        
        super().__init__(element, parent, name)

        self.type = self.element.attrib.get("type")
        self.key_type = self.element.attrib.get("key-type")
        self.item_type = self.element.attrib.get("item-type")
        self.value = self.element.attrib.get("value")
        self.nullable = self.element.attrib.get("nullable", "false") == "true"

    def process_properties(self):
        super().process_properties()

        if self.value is None and not self.nullable:
            self.value = "[instance]"
        
    def process_references(self):
        super().process_references()

        if self.type is not None:
            self.type = self.resolve_reference(self.type)

        if self.key_type is not None:
            self.key_type = self.resolve_reference(self.key_type)

        if self.item_type is not None:
            self.item_type = self.resolve_reference(self.item_type)

class Property(ClassMember, Parameter):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.mutable = self.element.attrib.get("mutable", "false") == "true"

class Method(ClassMember):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.inputs = list()
        self.outputs = list()
        self.error_conditions = list()

    def process(self):
        for child in self.element.findall("input"):
            input = MethodInput(child, self)
            self.inputs.append(input)

        for child in self.element.findall("output"):
            output = Parameter(child, self)
            self.outputs.append(output)

        for child in self.element.findall("error-condition"):
            cond = ErrorCondition(child, self)
            self.error_conditions.append(cond)

        super().process()

class MethodInput(Parameter):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.optional = self.element.attrib.get("optional", "false") == "true"
                
class Enumeration(ModuleMember):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.group = parent
        self.module = self.group.parent

        self.values = list()

    def process(self):
        for child in self.element.findall("value"):
            value = EnumerationValue(child, self)
            self.values.append(value)
        
        super().process()

class EnumerationValue(Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.enumeration = self.parent
    
class ErrorCondition(Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)
        self.error_ref = self.element.attrib["error"]
        self.error = None

    def process_references(self):
        self.error = self.resolve_reference(self.error_ref)

        super().process_references()

class Error(Node):
    def __init__(self, element, parent):
        super().__init__(element, parent)

class Model(Node):
    def __init__(self, element):
        super().__init__(element, None)

        self.modules = list()
        self.group_definitions_by_name = dict()
        self.link_generators = list()

        self.nodes_by_reference = dict()
        
    @property
    def abstract_path(self):
        return ()

    def process(self):
        for child in self.element.findall("module"):
            module = Module(child, self)
            self.modules.append(module)

        for child in self.element.findall("group-definition"):
            definition = GroupDefinition(child, self)
            self.group_definitions_by_name[definition.name] = definition

        for child in self.element.findall("link-generator"):
            func_name = child.attrib["function"]
            func = globals()[func_name]

            self.link_generators.append(func)

        super().process()

from .linkgenerators import *
