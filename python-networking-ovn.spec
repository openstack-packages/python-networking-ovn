%global drv_vendor OVN
%global pname networking-ovn
%global sname networking_ovn
%global docpath doc/build/html

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pname}
Version:        XXX
Release:        XXX
Epoch:          1
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pname}
Source0:        https://pypi.python.org/packages/source/n/%{pname}/%{pname}-%{version}.tar.gz

BuildArch:      noarch

# This is required to generate the networking-ovn.ini configuration file
BuildRequires:  openstack-neutron-common

BuildRequires:  python-debtcollector
BuildRequires:  python-mock
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-sphinx

Requires:       python-%{pname}-common = %{epoch}:%{version}-%{release}

# python-openvswitch is not included in openstack-neutron-common.
# Its needed by networking-ovn.
Requires:       python-openvswitch


%description
OVN provides virtual networking for Open vSwitch and is a component of the
Open vSwitch project.

This package contains %{drv_vendor} networking driver which provides
integration between OpenStack Neutron and OVN.



%package -n python-%{pname}-common
Summary:        Python %{pname} common files
Requires:       openstack-neutron-common


%description -n python-%{pname}-common
OVN provides virtual networking for Open vSwitch and is a component of the
Open vSwitch project.

This package contains %{drv_vendor} networking driver common library files
to provide integration between OpenStack Neutron and OVN.



%package -n python-%{pname}-tests
Summary:        Python %{pname} test files
Requires:       python-%{pname} = %{epoch}:%{version}-%{release}
Requires:       python-neutron-tests


%description -n python-%{pname}-tests
OVN provides virtual networking for Open vSwitch and is a component of the
Open vSwitch project.

This package contains %{drv_vendor} networking driver test files.


%prep
%autosetup -n %{pname}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f requirements.txt test-requirements.txt

# Kill egg-info in order to generate new SOURCES.txt
rm -rf {sname}.egg-info


%build
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build
%{__python2} setup.py build_sphinx
rm %{docpath}/.buildinfo

# Generate config file
PYTHONPATH=. oslo-config-generator --namespace networking_ovn --output-file networking-ovn.ini


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python2_sitelib}/bin
rm -rf %{buildroot}%{python2_sitelib}/doc
rm -rf %{buildroot}%{python2_sitelib}/tools


# Move config file to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/plugins/networking-ovn
mv networking-ovn.ini %{buildroot}%{_sysconfdir}/neutron/plugins/networking-ovn
chmod 640 %{buildroot}%{_sysconfdir}/neutron/plugins/*/*.ini


%files
%license LICENSE
%doc %{docpath}
%{_bindir}/neutron-ovn-db-sync-util
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/networking-ovn/*.ini


%files -n python-%{pname}-tests
%license LICENSE
%{python2_sitelib}/%{sname}/tests


%files -n python-%{pname}-common
%license LICENSE
%{python2_sitelib}/%{sname}
%{python2_sitelib}/%{sname}-*.egg-info
%exclude %{python2_sitelib}/%{sname}/tests
