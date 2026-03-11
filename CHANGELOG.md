# adriacloud\.kubernetes Release Notes

**Topics**

- <a href="#v26-3-0">v26\.3\.0</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#deprecated-features">Deprecated Features</a>
    - <a href="#bugfixes">Bugfixes</a>

<a id="v26-3-0"></a>
## v26\.3\.0

<a id="minor-changes"></a>
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
