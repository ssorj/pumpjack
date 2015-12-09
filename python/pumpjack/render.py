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

import os as _os

renderer_classes_by_name = dict()
renderer_names_by_class = dict()

def add_renderer(name, cls):
    renderer_classes_by_name[name] = cls
    renderer_names_by_class[cls] = name

class PumpjackRenderer(object):
    def __init__(self, output_dir):
        self.output_dir = output_dir

        self.type_literals = dict()

    def render(self, model):
        renderer_name = renderer_names_by_class[self.__class__]
        output_name = "model.{}.in".format(renderer_name)
        output_path = _os.path.join(self.output_dir, output_name)

        if not _os.path.exists(self.output_dir):
            _os.makedirs(self.output_dir)
        
        with open(output_path, "w") as f:
            out = PumpjackWriter(f)
            self.render_model(out, model)

    def get_type_literal(self, node, ref):
        # XXX
        if ref is None:
            return
        
        if ref.startswith("@"):
            cls = node.resolve_reference(ref)
            return self.render_class_name(cls)
        else:
            return self.type_literals.get(ref, ref) # XXX

    def render_class_name(self, cls):
        return cls.name

    def render_method_name(self, meth):
        return meth.name

    def render_var_name(self, var):
        return var.name

    def render_model(self, out, model):
        raise NotImplemented()

    def render_module(self, out, module):
        raise NotImplemented()

    def render_class(self, out, cls):
        raise NotImplemented()

    def render_constant(self, out, const):
        raise NotImplemented()

    def render_constructor(self, out, ctor):
        raise NotImplemented()

    def render_attribute(self, out, attr):
        raise NotImplemented()

    def render_method(self, out, meth):
        raise NotImplemented()

    def render_exception(self, out, exc):
        raise NotImplemented()

class PumpjackWriter(object):
    def __init__(self, out):
        self.out = out

    def write(self, s=None, *args):
        if s is not None:
            self.out.write(s.format(*args))

        self.out.write("\n")
