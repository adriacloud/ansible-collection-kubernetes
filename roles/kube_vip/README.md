# `kube_vip`

This role is responsible for deploying and configuring `kube-vip` to provide a highly available virtual IP (VIP) and/or load balancer for the Kubernetes control plane. It supports both ARP (Layer 2) and BGP modes.

All tasks are executed on the control-plane hosts to generate and upload the static pod manifest for `kube-vip`.

## Role Variables

### General Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `kube_vip_enabled` | `{{ kube_vip_interface is defined and kube_vip_address is defined }}` | Toggle whether the `kube_vip` configuration is uploaded. |
| `kube_vip_control_plane_group` | `{{ kubernetes_control_plane_group \| default('controllers') }}` | The Ansible group representing all control plane nodes. |
| `kube_vip_image` | `ghcr.io/kube-vip/kube-vip:v1.1.2` | The container image to use for the `kube-vip` pod. |
| `kube_vip_port` | `6443` | Port used to connect to the Kubernetes API server. |
| `kube_vip_kubeconfig_path` | `/etc/kubernetes/admin.conf` | Path to the kubeconfig file on the host. |

### VIP Networking

| Variable | Default | Description |
|----------|---------|-------------|
| `kube_vip_interface` | `{{ keepalived_interface \| default(kubernetes_keepalived_interface) }}` | Network interface to bind the Virtual IP to. |
| `kube_vip_address` | `{{ keepalived_vip \| default(kubernetes_keepalived_vip) }}` | The Virtual IP (VIP) address for the control plane. |
| `kube_vip_cidr` | `32` | Subnet mask CIDR for the Virtual IP address. |
| `kube_vip_ddns` | `false` | Enable/disable DDNS. |

### Control Plane Load Balancer (HAProxy Replacement)

| Variable | Default | Description |
|----------|---------|-------------|
| `kube_vip_lb_enable` | `false` | Toggle to enable/disable the internal load balancer. |
| `kube_vip_lb_port` | `6443` | Local port of the internal load balancer. |

### Leader Election

| Variable | Default | Description |
|----------|---------|-------------|
| `kube_vip_leaderelection` | `true` | Toggle leader election for the control plane VIP. |
| `kube_vip_leasename` | `plndr-cp-lock` | Lease resource name for control plane HA. |
| `kube_vip_leaseduration` | `15` | Lease duration in seconds. |
| `kube_vip_renewdeadline` | `10` | Renew deadline duration in seconds. |
| `kube_vip_retryperiod` | `2` | Retry period duration in seconds. |

### Service Load Balancer

| Variable | Default | Description |
|----------|---------|-------------|
| `kube_vip_svc_enable` | `true` | Toggle leader election / service load balancer for Kubernetes services. |
| `kube_vip_svc_leasename` | `plndr-svcs-lock` | Lease resource name for service HA. |

### VIP Mode

| Variable | Default | Description |
|----------|---------|-------------|
| `kube_vip_mode` | `arp` | Mode to run the VIP. Valid options are `arp` (Layer 2) or `bgp`. |

#### BGP Mode Configurations

If `kube_vip_mode` is set to `bgp`, the following variables should be defined to configure peer routing:

* `kube_vip_bgp_peers`: Comma-separated BGP peer configurations (e.g., `192.168.0.10:65000::false,192.168.0.11:65000::false`).
* `kube_vip_bgp_peeras`: AS number of the BGP peer (e.g., `"65000"`).
* `kube_vip_bgp_as`: Local AS number (e.g., `"65000"`).
* `kube_vip_bgp_routerid`: Router ID for the BGP session (typically the node IP).
* `kube_vip_bgp_routerinterface`: Interface used for BGP routing.
* `kube_vip_bgp_peeraddress`: IP address of a single BGP peer.
* `kube_vip_bgp_peerpass`: Password for BGP authentication.
* `kube_vip_bgp_sourceip`: Source IP for BGP session connection.

### Metrics

| Variable | Default | Description |
|----------|---------|-------------|
| `kube_vip_prometheus_server` | `:2112` | Address and port for the Prometheus metrics exporter. |

## Examples

### 1. Standard ARP Mode Deployment
Configure `kube-vip` using Layer 2 ARP:

```yaml
- name: Configure kube-vip
  hosts: controllers
  roles:
    - role: adriacloud.kubernetes.kube_vip
      vars:
        kube_vip_mode: arp
        kubernetes_keepalived_interface: eth0
        kubernetes_keepalived_vip: 192.168.10.100
```

### 2. BGP Peer Deployment
Configure `kube-vip` to peer with a local BGP router:

```yaml
- name: Configure kube-vip (BGP)
  hosts: controllers
  roles:
    - role: adriacloud.kubernetes.kube_vip
      vars:
        kube_vip_mode: bgp
        kube_vip_bgp_as: "65000"
        kube_vip_bgp_peeras: "65000"
        kube_vip_bgp_peers: "192.168.0.10:65000::false"
        kubernetes_keepalived_vip: 192.168.10.100
```

## License

Apache-2.0
