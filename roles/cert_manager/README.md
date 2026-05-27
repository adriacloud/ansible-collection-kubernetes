# cert-manager

This role is responsible for deploying `cert-manager` using Helm against a Kubernetes cluster. It utilizes the `helm_deploy` role to handle the orchestration of the Helm release, providing flexibility in how the chart is sourced.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `cert_manager_helm_release_name` | `cert-manager` | Name of the Helm release. |
| `cert_manager_helm_release_namespace` | `cert-manager` | Namespace where cert-manager will be installed. |
| `cert_manager_helm_repo_url` | `https://charts.jetstack.io` | The official repository URL. |
| `cert_manager_tools_version` | `v1.11.5` | The version of the cert-manager chart to install. |
| `cert_manager_helm_values` | `{}` | Dictionary of Helm values to override the defaults. |
| `cert_manager_helm_charts` | (Dynamic) | The list passed to the `helm_deploy` role. |
| `cert_manager_node_selector` | `{}` | Node selector for cert-manager components. |

## Handling Limited Connectivity (Air-gapped)

In environments where the target nodes cannot reach the official Jetstack Helm repository, you can modify the source of the chart by overriding the `cert_manager_helm_charts` variable.

### 1. Using a Local Source (Upload from Controller)
If you have the cert-manager chart downloaded locally on your Ansible controller, you can tell the role to upload it to the cluster nodes before installing.

```yaml
cert_manager_helm_charts:
  - name: "{{ cert_manager_helm_release_name }}"
    namespace: "{{ cert_manager_helm_release_namespace }}"
    # Path on your local machine
    src: "/home/user/charts/cert-manager-v1.11.5.tgz"
    values: "{{ _cert_manager_helm_values | combine(cert_manager_helm_values, recursive=True) }}"
```

### 2. Using an Internal Git Repository
If your organization mirrors charts in a private Git repository, you can source the deployment from there.

```yaml
cert_manager_helm_charts:
  - name: "{{ cert_manager_helm_release_name }}"
    namespace: "{{ cert_manager_helm_release_namespace }}"
    git: "https://git.internal.corp/kubernetes/cert-manager.git"
    git_version: "v1.11.5"
    # Path inside the git repo to the chart folder
    ref: "deploy/charts/cert-manager"
    values: "{{ _cert_manager_helm_values | combine(cert_manager_helm_values, recursive=True) }}"
```

### 3. Using an Internal Helm Registry
You can point the role to an internal Nexus or Artifactory instance by updating the repository URL.

```yaml
cert_manager_helm_repo_url: "https://artifactory.internal.corp/helm-mirrors/"
```

## Configuration

To add or override specific cert-manager configurations (like enabling CRD installation or configuring resource limits), use the `cert_manager_helm_values` variable:

```yaml
cert_manager_helm_values:
  installCRDs: true
  global:
    leaderElection:
      namespace: "cert-manager"
  prometheus:
    enabled: true
```

## Dependencies

This role depends on the following roles within the collection:
* `adriacloud.kubernetes.helm_deploy`

## License

Apache-2.0
