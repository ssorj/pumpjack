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

_amqp_type_href = "https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-{}"
    
def gen_amqp_type_link(node):
    if type(node) is not Class:
        return

    if node.module.name != "types":
        return

    if node.name in ("message-id", "duration", "iterator", "object"):
        return

    link = "Type definition", _amqp_type_href.format(node.name)

    node.links_by_relation["amqp"].append(link)

_cpp_module_href = "https://qpid.apache.org/releases/qpid-proton-master/proton/cpp/api/namespace{}.html"
_cpp_class_href = "https://qpid.apache.org/releases/qpid-proton-master/proton/cpp/api/class{}_1_1{}.html"
_cpp_error_href = "https://qpid.apache.org/releases/qpid-proton-master/proton/cpp/api/struct{}_1_1{}.html"

_cpp_namespaces_by_module = {
    "core": "proton",
    "types": "proton",
    "codec": "proton_1_1codec",
    "io": "proton_1_1io",
}

def gen_cpp_module_link(node):
    if type(node) is not Module:
        return

    namespace = _cpp_namespaces_by_module[node.name]
    href = _cpp_module_href.format(namespace)
    link = "C++", href
        
    node.links_by_relation["impl"].append(link)
    
def gen_cpp_class_link(node):
    if type(node) is not Class:
        return

    if node.name == "endpoint-options":
        return

    namespace = _cpp_namespaces_by_module[node.module.name]
    name = node.name.replace("-", "__")
    href = _cpp_class_href.format(namespace, name)

    if node.name == "proton-error":
        href = _cpp_error_href.format(namespace, "error")
    elif node.name.endswith("-error"):
        href = _cpp_error_href.format(namespace, name)

    link = "C++", href

    node.links_by_relation["impl"].append(link)

_c_group_href = "https://qpid.apache.org/releases/qpid-proton-master/proton/c/api/group__{}.html"

_c_groups_by_module = {
    "core": "engine",
    "types": "types",
    "codec": "data",
    "io": None,
}

def gen_c_module_link(node):
    if type(node) is not Module:
        return

    name = _c_groups_by_module[node.name]

    if name is None:
        return
    
    href = _c_group_href.format(name)
    link = "C", href

    node.links_by_relation["impl"].append(link)

def gen_c_class_link(node):
    if type(node) is not Class:
        return

    if node.module.name != "core":
        return

    if node.name.endswith("-options"):
        return

    if node.name.endswith("-error"):
        return
    
    if node.name in ("endpoint", "handler", "acceptor"):
        return

    name = node.name.replace("-", "__")
    href = _c_group_href.format(name)
    link = "C", href

    node.links_by_relation["impl"].append(link)

_java_module_href = "https://qpid.apache.org/releases/qpid-proton-master/proton/java/api/{}/package-summary.html"
_java_class_href = "https://qpid.apache.org/releases/qpid-proton-master/proton/java/api/{}/{}.html"

_java_packages_by_module = {
    "core": "org/apache/qpid/proton/engine",
    "types": "org/apache/qpid/proton/amqp",
    "codec": "org/apache/qpid/proton/codec",
    "io": None,
}

def gen_java_module_link(node):
    if type(node) is not Module:
        return

    package = _java_packages_by_module[node.name]

    if package is None:
        return

    href = _java_module_href.format(package)
    link = "Java", href

    node.links_by_relation["impl"].append(link)

def gen_java_class_link(node):
    if type(node) is not Class:
        return

    if node.name.endswith("-options"):
        return

    if node.name in ("container", "acceptor", "conversion-error"):
        return

    package = _java_packages_by_module[node.module.name]

    if package is None:
        return

    if node.name == "message":
        package = "org/apache/qpid/proton/message"

    name = init_cap(node.name)

    if node.name == "condition":
        package = "org/apache/qpid/proton/amqp/transport"
        name = "ErrorCondition"

    if node.name.endswith("-error"):
        package = "org/apache/qpid/proton"
        name = "{}Exception".format(init_cap(node.name.split("-")[0]))
    
    href = _java_class_href.format(package, name)
    link = "Java", href

    node.links_by_relation["impl"].append(link)

_python_module_href = "https://qpid.apache.org/releases/qpid-proton-master/proton/python/api/{}-module.html"
_python_class_href = "https://qpid.apache.org/releases/qpid-proton-master/proton/python/api/{}.{}-class.html"

_python_packages_by_module = {
    "core": "proton",
    "types": "proton",
    "codec": "proton",
    "io": None,
}

def gen_python_module_link(node):
    if type(node) is not Module:
        return

    package = _python_packages_by_module[node.name]

    if package is None:
        return

    href = _python_module_href.format(package)
    link = "Python", href

    node.links_by_relation["impl"].append(link)

def gen_python_class_link(node):
    if type(node) is not Class:
        return

    if node.name.endswith("-options"):
        return

    if node.name in ("conversion-error"):
        return

    package = _python_packages_by_module[node.module.name]

    if package is None:
        return

    if node.name in ("container", "acceptor"):
        package = "proton.reactor"

    name = init_cap(node.name)

    if node.name in ("ssl", "sasl"):
        name = node.name.upper()

    if node.name.endswith("-error"):
        name = "{}Exception".format(init_cap(node.name.split("-")[0]))

    if node.name == "timeout-error":
        name = "Timeout"
        
    href = _python_class_href.format(package, name)
    link = "Python", href

    node.links_by_relation["impl"].append(link)
