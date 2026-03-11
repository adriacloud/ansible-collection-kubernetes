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

import pytest
from ansible.errors import AnsibleFilterError
from ansible_collections.adriacloud.kubernetes.plugins.filter.docker_image import (
    docker_image,
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0",
            "k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0",
        ),
        ("docker.io/library/haproxy:2.5", "docker.io/library/haproxy:2.5"),
        (
            "k8s.gcr.io/ingress-nginx/controller:v1.1.1@sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",  # noqa E501
            "k8s.gcr.io/ingress-nginx/controller:v1.1.1@sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",  # noqa E501
        ),
    ],
)
def test_docker_image_ref(test_input, expected):
    assert docker_image(test_input, "ref") == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0",
            "k8s.gcr.io/sig-storage/csi-snapshotter",
        ),
        ("docker.io/library/haproxy:2.5", "docker.io/library/haproxy"),
        (
            "k8s.gcr.io/ingress-nginx/controller:v1.1.1@sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",  # noqa E501
            "k8s.gcr.io/ingress-nginx/controller",
        ),
    ],
)
def test_docker_image_name(test_input, expected):
    assert docker_image(test_input, "name") == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0",
            "k8s.gcr.io",
        ),
        ("docker.io/library/haproxy:2.5", "docker.io"),
        (
            "k8s.gcr.io/ingress-nginx/controller:v1.1.1@sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",  # noqa E501
            "k8s.gcr.io",
        ),
    ],
)
def test_docker_image_domain(test_input, expected):
    assert docker_image(test_input, "domain") == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0",
            "sig-storage/csi-snapshotter",
        ),
        ("docker.io/library/haproxy:2.5", "library/haproxy"),
        (
            "k8s.gcr.io/ingress-nginx/controller:v1.1.1@sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",  # noqa E501
            "ingress-nginx/controller",
        ),
    ],
)
def test_docker_image_path(test_input, expected):
    assert docker_image(test_input, "path") == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "registry.k8s.io/kube-apiserver:v1.22.0",
            "registry.k8s.io",
        ),
        (
            "k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0",
            "k8s.gcr.io/sig-storage",
        ),
        ("docker.io/library/haproxy:2.5", "docker.io/library"),
        (
            "k8s.gcr.io/ingress-nginx/controller:v1.1.1@sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",  # noqa E501
            "k8s.gcr.io/ingress-nginx",
        ),
    ],
)
def test_docker_image_prefix(test_input, expected):
    assert docker_image(test_input, "prefix") == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0", "v4.2.0"),
        ("docker.io/library/haproxy:2.5", "2.5"),
        (
            "k8s.gcr.io/ingress-nginx/controller:v1.1.1@sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",  # noqa: E501
            "v1.1.1",
        ),
        ("myregistry/myimage:latest", "latest"),
        ("myregistry/myimage", None),  # No tag
        (
            "docker.io/library/haproxy@sha256:c60346b3dd351211898932c8d21113b3e6b7644543295325f77a24c1de43a63a",
            None,
        ),
        ("haproxy", None),  # No tag
    ],
)
def test_docker_image_tag(test_input, expected):
    assert docker_image(test_input, "tag") == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0", None),  # No digest
        ("docker.io/library/haproxy:2.5", None),  # No digest
        (
            "k8s.gcr.io/ingress-nginx/controller:v1.1.1@sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",  # noqa: E501
            "sha256:0bc88eb15f9e7f84e8e56c14fa5735aaa488b840983f87bd79b1054190e660de",
        ),
        (
            "docker.io/library/haproxy@sha256:c60346b3dd351211898932c8d21113b3e6b7644543295325f77a24c1de43a63a",
            "sha256:c60346b3dd351211898932c8d21113b3e6b7644543295325f77a24c1de43a63a",
        ),
    ],
)
def test_docker_image_digest(test_input, expected):
    assert docker_image(test_input, "digest") == expected


@pytest.mark.parametrize(
    "value,part,registry,expected",
    [
        # Regular image rewrite
        ("ubuntu:20.04", "ref", "my-registry.com", "my-registry.com/ubuntu:20.04"),
        ("ubuntu:20.04", "name", "my-registry.com", "my-registry.com/ubuntu"),
        ("ubuntu:20.04", "domain", "my-registry.com", "my-registry.com"),
        (
            "docker.io/library/ubuntu:20.04",
            "ref",
            "my-registry.com",
            "my-registry.com/ubuntu:20.04",
        ),
        (
            "ubuntu@sha256:c60346b3dd351211898932c8d21113b3e6b7644543295325f77a24c1de43a63a",
            "ref",
            "my-registry.com",
            "my-registry.com/ubuntu@sha256:c60346b3dd351211898932c8d21113b3e6b7644543295325f77a24c1de43a63a",
        ),
        # Special handling for "skopeo"
        ("skopeo", "ref", "my-registry.com", "my-registry.com/skopeo-stable:latest"),
        ("skopeo", "name", "my-registry.com", "my-registry.com/skopeo-stable"),
        ("skopeo:latest", "name", "my-registry.com", "my-registry.com/skopeo-stable"),
    ],
)
def test_docker_image_with_registry(value, part, registry, expected):
    assert docker_image(value, part, registry) == expected


@pytest.mark.parametrize(
    "test_input,part,expected",
    [
        ("k8s.gcr.io/sig-storage/csi-snapshotter:v4.2.0", "invalid_part", None),
        ("docker.io/library/haproxy:2.5", "unknown_part", None),
        ("myimage:latest", "default", None),  # "default" as a part name
        ("myimage:latest", "repo", None),  # 'repo' is not a supported part
        ("myimage:latest", "version", None),  # 'version' is not a supported part
    ],
)
def test_docker_image_unsupported_part(test_input, part, expected):
    assert docker_image(test_input, part) == expected


def test_docker_image_exceptions():
    # Test non-string input
    with pytest.raises(AnsibleFilterError, match="Invalid value type"):
        docker_image(12345, "ref")

    # Test empty string input
    with pytest.raises(AnsibleFilterError):
        docker_image("", "ref")
