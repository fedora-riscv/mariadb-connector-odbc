Name:           mariadb-connector-odbc
Version:        3.0.3
Release:        1%{?dist}
Summary:        The MariaDB Native Client library (ODBC driver)
License:        LGPLv2+
Source:         https://downloads.mariadb.org/f/connector-odbc-%{version}/%{name}-%{version}-ga-src.tar.gz
Url:            https://mariadb.org/en/

BuildRequires:  cmake unixODBC-devel
BuildRequires:  mariadb-connector-c-devel >= 3.0.2

%description
MariaDB Connector/ODBC is a standardized, LGPL licensed database driver using
the industry standard Open Database Connectivity (ODBC) API. It supports ODBC
Standard 3.5, can be used as a drop-in replacement for MySQL Connector/ODBC,
and it supports both Unicode and ANSI modes.

%prep
%setup -q -n %{name}-%{version}-ga-src

%build
%cmake ./ -DMARIADB_LINK_DYNAMIC="%{_libdir}/mariadb/libmariadb.so"

%install
%make_install

rm %{buildroot}%{_datadir}/doc/mariadb_connector_odbc/COPYING
rm %{buildroot}%{_datadir}/doc/mariadb_connector_odbc/README

# Can be removed on F27 EOL
%ldconfig_scriptlets

%files
%license COPYING
%doc     README

# This is unixODBC plugin. It resides directly in {libdir} to be consistent with the rest of unixODBC plugins. Since it is plugin, it doesn´t need to be versioned.
%{_libdir}/libmaodbc.so



%changelog
* Sat Feb 10 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-1
- Rebase to 3.0.3 version
- Use more macros

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Michal Schorm <mschorm@redhat.com> - 3.0.2-1
- Rebase to 3.0.2 version
- Update ldconfig scriptlets
- Remove Group tag

* Thu Sep 07 2017 Augusto Caringi <acaringi@fedoraproject.org> - 3.0.1-2
- Update to top of 3.0 branch from GitHub 860e7f8b754f (version supporting dynamic linking)
- Source tarball composed from upstream GitHub, because the latest version solves the issues
  with dynamic linking.

* Mon Sep 04 2017 Augusto Caringi <acaringi@fedoraproject.org> - 3.0.1-1
- Update to version 3.0.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Michal Schorm <mschorm@redhat.com> - 2.0.14-1
- Update to version 2.0.14 and check, if blockers still apply. They do.
- Upstream issue created

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 19 2016 Michal Schorm <mschorm@redhat.com> - 2.0.12-1
- Initial version for 2.0.12
