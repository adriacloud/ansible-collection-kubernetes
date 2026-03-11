# Copyright (c) 2022 VEXXHOST, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleFilterError
from ansible.module_utils.common.collections import is_string



DOCUMENTATION = """
  name: docker_image
  short_description: Parse a Docker image reference
  version_added: 0.13.0
  description:
    - Parse a Docker image and return different parts of the reference
    - This lookup module requires "docker-image-py" to be installed on the
      Ansible controller.
  options:
    _input:
      type: string
      required: true
      description:
          - Docker image reference to parse
    part:
      type: string
      default: 'ref'
      options: [name, ref, tag, domain, path]
      required: true
      description:
        - Part of the Docker image reference to return
    registry:
      type: string
      required: false
      description:
        - Override the registry in the Docker image reference
  author:
    - Mohammed Naser <mnaser@vexxhost.com>
"""

EXAMPLES = """
- name: Generate a Docker image reference
  ansible.builtin.debug:
    msg: "{{ 'docker.io/library/memcached:1.6.3' | adriacloud.kubernetes.docker_image('name') }}"
"""

RETURN = """
  _value:
    description: The part of the Docker image reference
    type: string
"""

DEFAULT_DOMAIN = "docker.io"


def docker_image(value, part="ref", registry=None):
    if not is_string(value):
        raise AnsibleFilterError(
            "Invalid value type (%s) for docker_image (%r)" % (type(value), value)
        )

    if not value:
        raise AnsibleFilterError("Invalid value for docker_image: empty string")

    def _parse(ref_str):
        digest = None
        if "@" in ref_str:
            ref_str, digest = ref_str.rsplit("@", 1)

        tag = None
        last_slash = ref_str.rfind("/")
        last_colon = ref_str.rfind(":")
        if last_colon > last_slash:
            ref_str, tag = ref_str.rsplit(":", 1)

        name = ref_str

        parts = name.split("/")
        if len(parts) > 1 and ("." in parts[0] or ":" in parts[0] or parts[0] == "localhost"):
            domain = parts[0]
            path = "/".join(parts[1:])
        elif len(parts) > 1:
            domain = DEFAULT_DOMAIN
            path = name
        else:
            domain = DEFAULT_DOMAIN
            path = "library/" + name

        if "/" in path:
            prefix = domain + "/" + path.rsplit("/", 1)[0]
        else:
            prefix = domain

        return {
            "ref": name + ((":" + tag) if tag else "") + (("@" + digest) if digest else ""),
            "name": name,
            "tag": tag,
            "digest": digest,
            "domain": domain,
            "path": path,
            "prefix": prefix
        }

    parsed = _parse(value)
    if not registry:
        return parsed.get(part)

    path_val = parsed.get("path") or ""
    ref_name = path_val.split("/")[-1] if path_val else ""
    if ref_name == "skopeo":
        ref_name = "skopeo-stable"

    tag = parsed.get("tag")
    if not tag and not parsed.get("digest"):
        tag = "latest"

    new_ref_string = "{}/{}".format(registry, ref_name)
    if tag:
        new_ref_string = "{}:{}".format(new_ref_string, tag)
    if parsed["digest"]:
        new_ref_string = "{}@{}".format(new_ref_string, parsed["digest"])

    return _parse(new_ref_string).get(part)


class FilterModule(object):
    def filters(self):
        return {"docker_image": docker_image}
