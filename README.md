# Ansible collection for Kubernetes
[![Molecule](https://github.com/adriacloud/ansible-collection-kubernetes/actions/workflows/molecule.yml/badge.svg)](https://github.com/adriacloud/ansible-collection-kubernetes/actions/workflows/molecule.yml)
[![Unit Tests](https://github.com/adriacloud/ansible-collection-kubernetes/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/adriacloud/ansible-collection-kubernetes/actions/workflows/unit-tests.yml)



This is a forked version of [`vexxhost.kubernetes`](https://github.com/vexxhost/ansible-collection-kubernetes)
collection which is intended to be agnostic from Atmosphere implementation
and contain playbooks and roles to deploy a generic Kubernetes cluster using Ansible.

## Contributing

All contributions to the repository are warmly welcome. For testing we heavily rely on `tox`.
Before submitting a change, please make sure you have at least have executed following environments:

```console
tox -e linters
tox -e molecule-cluster-api
```

These two environments cover most of the cases and should be enough for most of the changes.
In case you made a change to some of the embedded plugins or filters, please also execute
the following environment:

```console
tox -e ansible-test
```

## Documentation

For documentation on collection, please check [docs](docs/README.md)

## Changelog

To check the collection changelog, please refer to [CHANGELOG.md](CHANGELOG.md)

## License

This collection is licensed under the terms of the [Apache 2.0 License](LICENSE.txt).
