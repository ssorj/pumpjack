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

        self.type_literals = dict() # XXX

    def render(self, model):
        raise NotImplementedError()

    def get_type_literal(self, node, ref):
        # XXX
        if ref is None:
            return

        if isinstance(ref, Node):
            cls = ref
        else:
            cls = node.resolve_reference(ref)
            
        return self.render_class_name(cls)

    def render_class_name(self, cls):
        return cls.name

    def render_method_name(self, meth):
        return meth.name

    def render_var_name(self, var):
        return var.name

    def render_model(self, out, model):
        raise NotImplementedError()

    def render_module(self, out, module):
        raise NotImplementedError()

    def render_class(self, out, cls):
        raise NotImplementedError()

    def render_constant(self, out, const):
        raise NotImplementedError()

    def render_constructor(self, out, ctor):
        raise NotImplementedError()

    def render_attribute(self, out, attr):
        raise NotImplementedError()

    def render_method(self, out, meth):
        raise NotImplementedError()

    def render_exception(self, out, exc):
        raise NotImplementedError()

class PumpjackWriter(object):
    def __init__(self, out):
        self.out = out

    def write(self, s=None, *args):
        if s is not None:
            self.out.write(s.format(*args))

        self.out.write("\n")

class PumpjackOutput(object):
    def __init__(self, path):
        assert path is not None
        
        self.path = path
        self.file = None

    def __enter__(self):
        assert self.file is None, self.file

        parent, child = _os.path.split(self.path)

        if not _os.path.exists(parent):
            _os.makedirs(parent)
    
        self.file = open(self.path, "w")
        self.file.__enter__()

        return self

    def write(self, s=None, *args):
        if s is not None:
            self.file.write(s.format(*args))

        self.file.write(_os.linesep)
        
    def __exit__(self, type, value, traceback):
        self.file.__exit__(type, value, traceback)
