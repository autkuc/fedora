%global commit      390bd2bb4b70e71c2acccb4a7309a490ba187664
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapdate    20261128

Name:           prgm
Version:        0.1.0~%{snapdate}git%{shortcommit}
Release:        %autorelease
Summary:        Minimal project workspace manager

License:        Apache-2.0
URL:            https://github.com/autkuc/prgm
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build

%description
prgm is a minimal, fast project workspace manager intended for basic file
tracking. It manages project directories inside named instances or filesystem
roots and is extendable via shared-object plugins.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, header files, and man pages for
developing applications and plugins that use libprgm.

%prep
%autosetup -n %{name}-%{commit}

%build
%meson
%meson_build

%install
%meson_install
install -d %{buildroot}%{_libdir}/prgm/plugins

%check
if python3 -c 'import os, tempfile; d = tempfile.mkdtemp(dir="/tmp"); os.setxattr(d, "user.test", b"1"); os.rmdir(d)' 2>/dev/null; then
    %meson_test
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/prgm
%{_libdir}/libprgm.so.1
%{_libdir}/libprgm.so.0.1.0
%dir %{_libdir}/prgm
%dir %{_libdir}/prgm/plugins
%{_mandir}/man1/prgm.1*

%files devel
%{_includedir}/prgm.h
%{_includedir}/meta.h
%{_libdir}/libprgm.so
%{_libdir}/pkgconfig/prgm.pc
%{_mandir}/man3/libprgm.3*

%changelog
%autochangelog
