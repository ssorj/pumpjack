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
import re as _re
import xml.etree.ElementTree as _et

class Pumpjack(object):
    def __init__(self, input_dir):
        self.input_dir = input_dir

        self.model = None

    def load(self):
        path = _os.path.join(self.input_dir, "model.xml")

        with open(path) as f:
            content = f.read()

        content = self.merge_content(content, self.input_dir)
        elem = _et.fromstring(content)

        self.model = Model(elem)
        self.model.process()

    def merge_content(self, content, input_dir):
        input_files = _os.listdir(input_dir)
        
        out = list()
        tokens = _re.split(r"(@.+?@)", content)

        for token in tokens:
            if (token[:1], token[-1:]) != ("@", "@"):
                out.append(token)
                continue
            
            file_name = token[1:-1]

            if file_name in input_files:
                file_path = _os.path.join(input_dir, file_name)
                
                with open(file_path, "r") as f:
                    file_content = f.read()
                    
                out.append(self.merge_content(file_content, input_dir))
                continue

            out.append(token)

        return "".join(out)
    
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
