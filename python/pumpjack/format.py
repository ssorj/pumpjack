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

def studly_name(name):
    assert name

    chars = list()
    prev = None
    curr = None

    for i in range(len(name)):
        curr = name[i]

        if prev == "-":
            curr = curr.upper()

        if curr != "-":
            chars.append(curr)

        prev = curr

    return "".join(chars)

def init_cap(s):
    return s[0].upper() + s[1:]

def first_sentence(text):
    if not text:
        return ""

    return re.split('\.\s+', text, 1)[0]

def format_lines(text, max_length):
    assert text

    text = text.strip()

    text = re.sub("\s*\n\s*\n\s*", " [para] ", text)

    words = text.split()
    lines = list()
    line = list()
    length = 0

    for word in words:
        if length + len(word) > max_length or word == "[para]":
            lines.append(" ".join(line))
            line = list()
            length = 0

        if word == "[para]":
            lines.append("")
            continue

        line.append(word)
        length += len(word)

    lines.append(" ".join(line))

    return lines

def format_comment(text, prefix):
    lines = format_lines(text, 66 - len(prefix))
    lines = [prefix + x for x in lines]

    return "\n".join(lines)

class PumpjackWriter(object):
    def __init__(self, out):
        self.out = out

    def write(self, s=None, *args):
        if s is not None:
            self.out.write(s.format(*args))

        self.out.write("\n")
