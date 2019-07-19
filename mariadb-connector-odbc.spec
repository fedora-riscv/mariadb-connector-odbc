# For deep debugging we need to build binaries with extra debug info
%bcond_with     debug

Name:           mariadb-connector-odbc
Version:        3.1.1
Release:        4%{?with_debug:.debug}%{?dist}
Summary:        The MariaDB Native Client library (ODBC driver)
License:        LGPLv2+
Source:         https://downloads.mariadb.org/f/connector-odbc-%{version}/%{name}-%{version}-ga-src.tar.gz
Url:            https://mariadb.org/en/
# Online documentation can be found at: https://mariadb.com/kb/en/library/mariadb-connector-odbc/

BuildRequires:  cmake unixODBC-devel gcc-c++
BuildRequires:  mariadb-connector-c-devel >= 3.0.6

Patch1:         libraries_include_path.patch
# Reported upstream JIRA: ODBC-258
Patch2:         cmake_docdir_licensedir_configurable.patch

%description
MariaDB Connector/ODBC is a standardized, LGPL licensed database driver using
the industry standard Open Database Connectivity (ODBC) API. It supports ODBC
Standard 3.5, can be used as a drop-in replacement for MySQL Connector/ODBC,
and it supports both Unicode and ANSI modes.

%prep
%setup -q -n %{name}-%{version}-ga-src
%patch1 -p1
%patch2 -p1

%build
%{set_build_flags}

# Override all optimization flags when making a debug build
%{?with_debug: CFLAGS="$CFLAGS -O0 -g"}
CXXFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS

%cmake -DMARIADB_LINK_DYNAMIC="%{_libdir}/libmariadb.so" \
       -DBUILD_SHARED_LIBS="ON" \
       -DCMAKE_BUILD_TYPE="%{?with_debug:Debug}%{!?with_tokudb:RelWithDebInfo}" \
       -DCMAKE_INSTALL_PREFIX="%{_usr}" \
       -DINCLUDE_INSTALL_DIR="%{_includedir}" \
       -DINSTALL_LIB_SUFFIX="%{_lib}" \
       -DSHARE_INSTALL_PREFIX="%{_datadir}" \
       -DSYSCONF_INSTALL_DIR="%{_sysconfdir}" \
       -DINSTALL_DOC_DIR="%{_defaultdocdir}/%{name}" \
       -DINSTALL_LICENSE_DIR="%{_defaultlicensedir}/%{name}" \
       .

#cmake -LAH
cmake -L .

%install
%make_install

# Can be commented out thanks to Patch2.
# Can be dropped if upstream accept the patch (https://jira.mariadb.org/browse/ODBC-258)
  # The %%doc and %%license files are installed to the wrong location by default
  # rm %{buildroot}%{_datadir}/doc/mariadb_connector_odbc/{README,COPYING}

%files
%license COPYING
%doc     README

# This is unixODBC plugin. It resides directly in %%{_libdir} to be consistent with the rest of unixODBC plugins. Since it is plugin, it doesn´t need to be versioned.
%{_libdir}/libmaodbc.so



%changelog
* Fri Jul 19 2019 Michal Schorm <mschorm@redhat.com> - 3.1.1-4
- Use macro for setting the compiler flags

* Wed Jun 05 2019 Michal Schorm <mschorm@redhat.com> - 3.1.1-3
- Added debug build switch
- Added patch2: configurable doc and license dirs paths

* Wed Jun 05 2019 Michal Schorm <mschorm@redhat.com> - 3.1.1-2
- Patch solution found

* Tue Jun 04 2019 Michal Schorm <mschorm@redhat.com> - 3.1.1-1
- Rebase to 3.1.1

* Tue Jun 04 2019 Michal Schorm <mschorm@redhat.com> - 3.0.9-1
- Rebase to 3.0.9

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 3.0.8-2
- Append curdir to CMake invokation. (#1668512)

* Sun Jan 06 2019 Michal Schorm <mschorm@redhat.com> - 3.0.8-1
- Rebase to 3.0.8

* Tue Nov 20 2018 Michal Schorm <mschorm@redhat.com> - 3.0.7-1
- Rebase to 3.0.7

* Fri Aug 03 2018 Michal Schorm <mschorm@redhat.com> - 3.0.6-1
- Rebase to 3.0.6
- Raise the minimal version of the connector-c required, because of a fixed bug
  which affected connector-odbc builds

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

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
