# adriacloud\.kubernetes Release Notes

**Topics**

- <a href="#v26-4-0">v26\.4\.0</a>
    - <a href="#major-changes">Major Changes</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
- <a href="#v26-3-0">v26\.3\.0</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#deprecated-features">Deprecated Features</a>
    - <a href="#bugfixes">Bugfixes</a>

<a id="v26-4-0"></a>
## v26\.4\.0

<a id="major-changes"></a>
### Major Changes

* Dependecy on <em class="title-reference">vexxhost\.containers</em> has been completely removed
* Minimal version of <em class="title-reference">comminuty\.general</em> collection required is 7\.0\.0
* Role <em class="title-reference">vexxhost\.containers\.containerd</em> has been replaced with <em class="title-reference">adriacloud\.kubernetes\.containerd</em>\, which is included explicitly in tasks and can accept a list of artifacts for download\.
* Role <em class="title-reference">vexxhost\.containers\.download\_artifact</em> has been replaced with <em class="title-reference">adriacloud\.kubernetes\.download\_artifacts</em>\, which is included explicitly in tasks and can accept a list of artifacts for download\.
* The <em class="title-reference">kubelet</em> role has incorporated logic for CRI and CNI deployment and configuration\. Please\, use variables <em class="title-reference">kubelet\_crictl\_version</em> and <em class="title-reference">kubelet\_cni\_plugins\_version</em> to define desired versions of tools\. If set to an empty string or null values\, deployment of tools will be skipped\.

<a id="minor-changes"></a>
### Minor Changes

* Added role <em class="title-reference">adriacloud\.kubernetes\.containerd</em> which aims to replace the <em class="title-reference">vexxhost\.containers\.containerd</em> role in the future\. While it maintains simmilar set of features\, it has a series of significant differences\. The role does not mandate a list of supported runc/containerd versions\, and any valid version set could be used freely\.
* Added role <em class="title-reference">adriacloud\.kubernetes\.defaults</em> which is going to carry re\-usable variables\, not avoid repeating ourselves\. Role consists solely from defaults file\, and will be included/loaded from other roles in the collection\.
* Added role <em class="title-reference">adriacloud\.kubernetes\.download\_artifacts</em> which aims to replace the <em class="title-reference">vexxhost\.containers\.download\_artifact</em> role in the future\. Main difference is that the new role accepts a list of arguments to download\, instead requiring to call the role include in a loop\. It maintains all same features as the original one\. Though\, in order to use proxy connection\, operators are expected to define <em class="title-reference">environment</em> on the playbook level\, or for the <em class="title-reference">include\_role</em>\.
* Added variable <em class="title-reference">defaults\_containerd\_socket</em> with default value of <em class="title-reference">/run/containerd/containerd\.sock</em>\. It is used in both <em class="title-reference">containerd</em> and <em class="title-reference">kubelet</em> roles\.
* Collection no longer requires presence of <em class="title-reference">docker\-image\-py</em> Python package for the ansible controller\. The filter <em class="title-reference">adriacloud\.kubernetes\.docker\_image</em> now implements the same logic internally\.
* Helm diff plugin installation can be disabled with <em class="title-reference">adriacloud\.kubernetes\.helm</em> role by setting <em class="title-reference">helm\_diff\_version</em> to an empty string\.
* Introduced a new helm\_deploy role\, which takes care of installing and deploying helm charts to the deployed k8s cluster\.
* Introduced variable <em class="title-reference">upload\_helm\_chart\_list</em> which allows to accept a list of helm charts to be copied by the role\. By default\, the variable is populated from <em class="title-reference">upload\_helm\_chart\_src</em> and <em class="title-reference">upload\_helm\_chart\_dest</em> for backwards compatability\.
* Reduced amount of external dependenices\, specifically on helper roles from <em class="title-reference">vexxhost\.containers</em> like <em class="title-reference">vexxhost\.containers\.package</em> and <em class="title-reference">vexxhost\.containers\.directory</em>\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* Role for <code>flux</code> deployment has been removed from the collection\. It was not required for a kubernetes deployment\, and goal of this collection is to perform a functional kubernetes cluster deployment\, while management tools for these kubernetes clusters are left out of the collection scope\.

<a id="v26-3-0"></a>
## v26\.3\.0

<a id="minor-changes-1"></a>
### Minor Changes

* Added support for CAPO versions 0\.13\.4 and 0\.14\.1
* Added support for HELM versions v3\.19\.5 and v3\.20\.0
* Added support for ansible\-core 2\.19 and later\.
* Added support for clusterctl versions 1\.10\.10\, 1\.11\.6\, 1\.12\.3
* Added support for kubernetes versions 1\.34\.5 and 1\.35\.2

<a id="deprecated-features"></a>
### Deprecated Features

* Collection no longer cleans\-up components\, if they were installed from system packages\.
* Support for Debian 12 has been deprecated

<a id="bugfixes"></a>
### Bugfixes

* Ensured\, that proper python interpreter is used\, when ansible\_collection\_kubernetes\_target\_venv is defined\.
