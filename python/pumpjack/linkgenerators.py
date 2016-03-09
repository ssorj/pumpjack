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

from .model import *

_amqp_type_link = "https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-{}"
    
def gen_amqp_type_link(node):
    if type(node) is not Class:
        return

    if node.module.name != "types":
        return

    if node.name in ("message-id", "duration", "iterator", "object"):
        return

    link = "Type definition", _amqp_type_link.format(node.name)

    node.links_by_relation["amqp"].append(link)

_cpp_module_link = "http://qpid.apache.org/releases/qpid-proton-0.12.0/proton/cpp/api/namespace{}.html"
_cpp_class_link = "http://qpid.apache.org/releases/qpid-proton-0.12.0/proton/cpp/api/class{}_1_1{}.html"
_cpp_error_link = "http://qpid.apache.org/releases/qpid-proton-0.12.0/proton/cpp/api/struct{}_1_1{}.html"

_cpp_namespaces_by_module = {
    "core": "proton",
    "types": "proton",
    "codec": "proton_1_1codec",
    "io": "proton_1_1io",
}

def gen_cpp_class_link(node):
    if type(node) is not Class:
        return

    namespace = _cpp_namespaces_by_module[node.module.name]
    name = node.name.replace("-", "__")
    href = _cpp_class_link.format(namespace, name)

    if node.name == "proton-error":
        href = _cpp_error_link.format(namespace, "error")
    elif node.name.endswith("-error"):
        href = _cpp_error_link.format(namespace, name)

    link = "C++", href

    node.links_by_relation["impl"].append(link)

def gen_cpp_module_link(node):
    if type(node) is not Module:
        return

    namespace = _cpp_namespaces_by_module[node.name]
    href = _cpp_module_link.format(namespace)
    link = "C++", href
        
    node.links_by_relation["impl"].append(link)
    
_c_group_link = "http://qpid.apache.org/releases/qpid-proton-master/proton/c/api/group__{}.html"

_c_groups_by_module = {
    "core": "engine",
    "types": "types",
    "codec": "data",
    "io": "selectable",
}

def gen_c_class_link(node):
    if type(node) is not Class:
        return

    if node.module.name is not "core":
        return

    if node.name.endswith("-options"):
        return

    if node.name.endswith("-error"):
        return
    
    if node.name in ("endpoint", "handler", "acceptor"):
        return

    name = node.name.replace("-", "__")
    href = _c_group_link.format(name)
    link = "C", href

    node.links_by_relation["impl"].append(link)

def gen_c_module_link(node):
    if type(node) is not Module:
        return

    name = _c_groups_by_module[node.name]
    href = _c_group_link.format(name)
    link = "C", href

    node.links_by_relation["impl"].append(link)
