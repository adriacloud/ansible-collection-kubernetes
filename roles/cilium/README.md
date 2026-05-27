# cilium

This role is responsible for deploying Cilium CNI to a Kubernetes cluster. It utilizes the `helm_deploy` role to handle the orchestration of the Helm release, providing flexibility in how the chart is sourced.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `cilium_version` | `v1.14.8` | The version of Cilium to install. |
| `cilium_helm_release_name` | `cilium` | Name of the Helm release. |
| `cilium_helm_release_namespace` | `kube-system` | Namespace where Cilium will be installed. |
| `cilium_helm_repo_url` | `https://helm.cilium.io/` | The official repository URL. |
| `cilium_helm_values` | `{}` | Dictionary of Helm values to override the default template. |
| `cilium_helm_charts` | (Dynamic) | The list passed to the `helm_deploy` role. |

## Handling Limited Connectivity (Air-gapped)

In environments where the target nodes cannot reach `https://helm.cilium.io/`, you can modify the source of the chart by overriding the `cilium_helm_charts` variable in your inventory or group variables.

### 1. Using a Local Source (Upload from Controller)
If you have the Cilium chart downloaded locally on your Ansible controller, you can tell the role to upload it to the cluster nodes before installing.

```yaml
cilium_helm_charts:
  - name: "{{ cilium_helm_release_name }}"
    namespace: "{{ cilium_helm_release_namespace }}"
    # Path on your local machine
    src: "/home/user/charts/cilium-1.14.8.tgz"
    values: "{{ lookup('ansible.builtin.template', 'values.yml.j2') | from_yaml | combine(cilium_helm_values, recursive=True) }}"
```

### 2. Using an Internal Git Repository
If your organization mirrors charts in a private Git repository, you can source the deployment from there.

```yaml
cilium_helm_charts:
  - name: "{{ cilium_helm_release_name }}"
    namespace: "{{ cilium_helm_release_namespace }}"
    git: "https://git.internal.corp/network/cilium.git"
    git_version: "v1.14.8"
    # Path inside the git repo to the chart folder
    ref: "install/kubernetes/cilium"
    values: "{{ lookup('ansible.builtin.template', 'values.yml.j2') | from_yaml | combine(cilium_helm_values, recursive=True) }}"
```

### 3. Using an Internal Helm Registry
You can point the role to an internal Nexus or Artifactory instance.

```yaml
cilium_helm_repo_url: "https://artifactory.internal.corp/helm-mirrors/"
```

## Configuration

The role uses a base template for values (`values.yml.j2`). To add or override specific Cilium configurations (like enabling Hubble or setting the tunnel mode), use the `cilium_helm_values` variable:

```yaml
cilium_helm_values:
  hubble:
    enabled: true
    relay:
      enabled: true
    ui:
      enabled: true
  ipam:
    mode: "kubernetes"
```

## Dependencies

This role depends on the following roles within the collection:
* `adriacloud.kubernetes.helm_deploy`

## License

Apache-2.0
