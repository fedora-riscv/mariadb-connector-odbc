# !! CRITICAL BLOCKING ISSUES !!
# https://jira.mariadb.org/browse/ODBC-98
# https://bugzilla.redhat.com/show_bug.cgi?id=1397869
# https://bugzilla.redhat.com/show_bug.cgi?id=1381548

# THE PACKAGE CANNOT BE USED UNTIL THEY ARE SOLVED BY UPSTREAM

Name:           mariadb-connector-odbc
Version:        2.0.14
Release:        2%{?dist}
Summary:        The MariaDB Native Client library (ODBC driver)
Group:          Applications/Databases
License:        LGPLv2+
Source:         http://mirror.hosting90.cz/mariadb/connector-odbc-%{version}/source/mariadb-connector-odbc-%{version}-ga-src.tar.gz
Url:            https://mariadb.org/en/
BuildRequires:  cmake unixODBC-devel
BuildRequires:  mariadb-connector-c-devel >= 2.3.2

# Set Cmake to build against dynamic library with parameter "-DMARIADB_DYNAMIC_LIB=..."
Patch:          CMakeLists.txt.patch

%description
MariaDB Connector/ODBC is a standardized, LGPL licensed database driver using
the industry standard Open Database Connectivity (ODBC) API. It supports ODBC
Standard 3.5, can be used as a drop-in replacement for MySQL Connector/ODBC,
and it supports both Unicode and ANSI modes.

%prep
%setup -q -n mariadb-connector-odbc-%{version}-ga-src
%patch -p1 -b .backup

%build
%cmake ./ -DMARIADB_DYNAMIC_LIB="%{_libdir}/mariadb/libmariadb.so"

%install
%make_install DESTDIR=$RPM_BUILD_ROOT

rm /$RPM_BUILD_ROOT/usr/share/doc/mariadb_connector_odbc/COPYING
rm /$RPM_BUILD_ROOT/usr/share/doc/mariadb_connector_odbc/README

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%doc     README
%{_libdir}/libmaodbc.so
# This is unixODBC plugin. It resides directly in {libdir} to be consistent with the rest of unixODBC plugins. Since it is plugin, it doesn´t need to be versioned.



%changelog
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Michal Schorm <mschorm@redhat.com> - 2.0.14-1
- Update to version 2.0.14 and check, if blockers still apply. They do.
- Upstream issue created

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 19 2016 Michal Schorm <mschorm@redhat.com> - 2.0.12-1
- Initial version for 2.0.12
