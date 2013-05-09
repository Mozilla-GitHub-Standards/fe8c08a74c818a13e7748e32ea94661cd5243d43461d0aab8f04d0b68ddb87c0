%define name python26-syncwhoami
%define pythonname SyncWhoami
%define version 1.0
%define unmangled_version %{version}
%define release 2

Summary: Sync User Account Details Server
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{pythonname}-%{unmangled_version}.tar.gz
License: MPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{pythonname}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Ryan Kelly <rfkelly@mozilla.com>
Requires: nginx gunicorn logstash-metlog >= 0.8.3 openldap-devel python26 python26-setuptools python26-webob python26-paste python26-pastedeploy python26-services >= 2.13 python26-sqlalchemy python26-simplejson python26-routes python26-ldap python26-cef python26-gevent
Url: https://github.com/mozilla-services/server-whoami

%description
===========
Sync Whoami
===========

Simple server for retrieving user account details.


%prep
%setup -n %{pythonname}-%{unmangled_version} -n %{pythonname}-%{unmangled_version}

%build
python2.6 setup.py build

%install
python2.6 setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
# This works around a problem with rpmbuild, where it pre-gnerates .pyo
# files that aren't included in the INSTALLED_FILES list by bdist_rpm.
cat INSTALLED_FILES | grep '.pyc$' | sed 's/.pyc$/.pyo/' >> INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES

%defattr(-,root,root)
