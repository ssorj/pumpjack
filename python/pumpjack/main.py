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

from .html import *
from .python import *

import os as _os

from xml.etree.ElementTree import ElementTree

class Pumpjack(object):
    def __init__(self, input_dir):
        self.input_dir = input_dir

        self.model = None

    def load(self):
        input_path = _os.path.join(self.input_dir, "model.xml")
        tree = ElementTree()

        if not _os.path.isfile(input_path):
            msg = "File '{}' is missing"
            raise PumpjackException(msg)

        with open(input_path) as f:
            tree.parse(f)

        elem = tree.getroot()

        self.model = Model(elem)
        self.model.process()
        self.model.process_references()

    def render(self, output_dir, renderer_name):
        assert self.model is not None

        try:
            renderer_class = renderer_classes_by_name[renderer_name]
        except KeyError:
            msg = "Renderer '%s' is unknown" % renderer_name
            raise PumpjackException(msg)

        renderer = renderer_class(output_dir)

        try:
            renderer.render(self.model)
        except IOError as e:
            msg = "Cannot render: %s" % str(e)
            raise PumpjackException(msg)

class PumpjackException(Exception):
    pass
