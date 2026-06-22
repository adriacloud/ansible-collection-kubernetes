# kubernetes

This role is responsible for bootstrapping and managing a Kubernetes cluster using `kubeadm`. It handles the initialization of the bootstrap control-plane node, uploading control-plane certificates, joining additional control-plane or worker nodes to the cluster, configuring custom CA certificates, and upgrading cluster components.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `kubernetes_version` | `1.36.1` | The version of Kubernetes components to install and upgrade. |
| `kubernetes_bootstrap_node` | First host in `kubernetes_control_plane_group` | The control-plane host selected to bootstrap the cluster. |
| `kubernetes_control_plane_group` | `controllers` | Name of the Ansible inventory group containing all control-plane hosts. |
| `kubernetes_image_repository` | `registry.k8s.io` | Container registry to pull Kubernetes system images from. |
| `kubernetes_non_init_namespace` | `{{ ansible_connection == 'community.docker.docker' }}` | If deployed in a container (docker/LXC), prevents `kube-proxy` from adjusting host conntrack settings. |
| `kubernetes_coredns_node_selector` | `{"openstack-control-plane": "enabled"}` | Node selector mapping applied to the CoreDNS deployment. |
| `kubernetes_allow_custom_ca` | `false` | Whether to upload and configure a custom set of CA certificates. |
| `kubernetes_node_ip` | `{{ kubelet_node_ip }}` | *Deprecated*. Use `kubelet_node_ip` instead. |
| `kubernetes_cri_socket` | `{{ kubelet_cri_socket }}` | *Deprecated*. Use `kubelet_cri_socket` instead. |
| `kubernetes_allow_unsafe_swap` | `false` | *Deprecated*. Use `kubelet_allow_unsafe_swap` instead. |

### Custom CA Variables

When `kubernetes_allow_custom_ca` is set to `true`, the following variables can be configured to provide custom keys and certificates for Kubernetes, etcd, and front-proxy CAs:

* `kubernetes_custom_ca_key`: Private key content for the Kubernetes cluster CA.
* `kubernetes_custom_ca_cert`: Certificate content for the Kubernetes cluster CA.
* `kubernetes_custom_etcd_ca_key`: Private key content for the etcd CA.
* `kubernetes_custom_etcd_ca_cert`: Certificate content for the etcd CA.
* `kubernetes_custom_front_proxy_ca_key`: Private key content for the front-proxy CA.
* `kubernetes_custom_front_proxy_ca_cert`: Certificate content for the front-proxy CA.

### Package Management Variables

These variables control the Python and distribution packages installed on target hosts:

* `kubernetes_pip_packages_base`: List of fundamental Python pip packages required (default: `['kubernetes']`).
* `kubernetes_pip_packages_venv`: Additional Python packages installed when running inside a target virtual environment (default: `['cryptography', 'pyyaml']`).
* `kubernetes_use_venv`: Boolean to specify if the role should utilize an Ansible target virtual environment.
* `kubernetes_pip_packages_install`: Final calculated list of pip packages to install.
* `kubernetes_distro_packages_base`: System packages required by the role (default: `['python3-pip']`).
* `kubernetes_distro_packages_no_venv`: System packages required when not using a virtual environment (default: `['python3-cryptography']`).
* `kubernetes_distro_packages_venv`: System packages required when using a virtual environment, mapped by OS family.
* `kubernetes_distro_packages_install`: Final calculated list of system distribution packages to install.
* `kubernetes_distro_packages_remove`: System packages to remove to avoid conflicts.

## Example Playbook

The following playbook initializes a Kubernetes cluster using the `kubernetes` role:

```yaml
- name: Deploy Kubernetes Cluster
  hosts: all
  roles:
    - role: adriacloud.kubernetes.kubernetes
      vars:
        kubernetes_version: 1.36.1
        kubernetes_control_plane_group: control_plane_nodes
```

## License

Apache-2.0
