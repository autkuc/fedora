Name:           durdraw
Version:        0.31.1
Release:        %autorelease
Summary:        ASCII and ANSI art editor for the terminal

License:        BSD-3-Clause
URL:            https://github.com/durdraw/durdraw
Source0:        https://github.com/durdraw/durdraw/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%pyproject_buildrequires

%description
Durdraw is a terminal editor for ASCII, Unicode, and ANSI art, with
support for animation, colors, and custom themes.

%prep
%autosetup -n durdraw-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

install -Dpm0644 durdraw.1 \
    %{buildroot}%{_mandir}/man1/durdraw.1
install -Dpm0644 durview.1 \
    %{buildroot}%{_mandir}/man1/durview.1
install -Dpm0644 durfetch.1 \
    %{buildroot}%{_mandir}/man1/durfetch.1

%check
python3 -m compileall -q durdraw

%files
%license LICENSE
%doc README.md
%{_bindir}/durdraw
%{_bindir}/durview
%{_bindir}/durfetch
%{python3_sitelib}/durdraw/
%{python3_sitelib}/durdraw-*.dist-info/
%{_mandir}/man1/durdraw.1*
%{_mandir}/man1/durview.1*
%{_mandir}/man1/durfetch.1*

%changelog
%autochangelog
