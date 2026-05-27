# helm_deploy

This role is responsible for deploying Helm charts to a Kubernetes cluster. It supports multiple sources for charts, including native Helm repositories, Git repositories, and local directories uploaded from the Ansible controller.

All tasks are delegated to a specific host (usually a control-plane node) that has access to the cluster and the Helm binary.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `helm_deploy_host_group` | `controllers` | The inventory group containing the host where Helm commands will be executed. |
| `helm_deploy_host` | First host in `helm_deploy_host_group` | The specific host used for delegation. |
| `helm_deploy_python_interpreter` | `/usr/bin/python3` | The Python interpreter path used for Kubernetes modules on the target host. |
| `helm_deploy_git_clone_path` | `/var/lib/downloads` | The base directory on the target host where Git repositories are cloned. |
| `helm_deploy_charts` | `[]` | A list of dictionaries defining the charts to be deployed. |

### Chart Definition Parameters

Each item in the `helm_deploy_charts` list can contain the following keys:

* `name`: (Required) Name of the Helm release.
* `namespace`: (Required) Kubernetes namespace for the release.
* `state`: `present` or `absent` (default: `present`).
* `version`: Version of the chart to install.
* `values`: A dictionary of Helm values.
* `kubeconfig`: Path to the kubeconfig file (default: `/etc/kubernetes/admin.conf`).
* `verify`: Boolean to toggle SSL/TLS verification (default: `true`).

#### Source-specific parameters:
* `repo_url`: URL of a native Helm repository.
* `repo_name`: Custom name for the Helm repository.
* `git`: URL of a Git repository containing the chart.
* `git_version`: Branch, tag, or commit SHA to clone (default: `HEAD`).
* `src`: Local path on the Ansible controller to be uploaded to the target.
* `ref`: Relative path to the chart within the Git repository or uploaded source.

## Examples

### 1. Install from a Native Helm Repository
This is the standard way to install charts using `helm repo add`.

```yaml
helm_deploy_charts:
  - name: cert-manager
    namespace: cert-manager
    repo_url: "https://charts.jetstack.io"
    repo_name: jetstack
    version: "v1.11.5"
    values:
      installCRDs: true
```

### 2. Install from a Git Repository
The role will clone the repository to the `helm_deploy_git_clone_path` and install the chart from the specified reference.

```yaml
helm_deploy_charts:
  - name: cilium
    namespace: kube-system
    git: "https://github.com/cilium/cilium.git"
    git_version: "v1.14.8"
    ref: "install/kubernetes/cilium"
    values:
      debug:
        enabled: true
```

### 3. Upload from Ansible Controller (`src`)
Use this when the chart source is located on your local machine (Ansible controller). The role will upload it to the target host before deployment.

```yaml
helm_deploy_charts:
  - name: my-custom-app
    namespace: default
    src: "/home/user/my-charts/custom-app-1.0.0.tgz"
    values:
      replicaCount: 3
```

### 4. Mixed Sources
You can define multiple charts from different sources in a single execution.

```yaml
helm_deploy_charts:
  - name: prometheus
    namespace: monitoring
    repo_url: "https://prometheus-community.github.io/helm-charts"
    values:
      alertmanager:
        enabled: false
  - name: backend-api
    namespace: prod
    git: "git@github.com:my-org/charts.git"
    ref: "stable/backend-api"
```

## License
Apache-2.0
