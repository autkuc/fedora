Name:           durdraw
Version:        0.31.1
Release:        %autorelease
Summary:        ASCII and ANSI art editor for the terminal

License:        BSD-3-Clause
URL:            https://github.com/durdraw/durdraw
Source0:        https://github.com/durdraw/durdraw/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%description
Durdraw is a terminal editor for ASCII, Unicode, and ANSI art, with
support for animation, colors, and custom themes.

%prep
%autosetup -n durdraw-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l durdraw

install -Dpm0644 durdraw.1 \
    %{buildroot}%{_mandir}/man1/durdraw.1
install -Dpm0644 durview.1 \
    %{buildroot}%{_mandir}/man1/durview.1
install -Dpm0644 durfetch.1 \
    %{buildroot}%{_mandir}/man1/durfetch.1

%check
python3 -m compileall -q durdraw

%files -f %{pyproject_files}
%doc README.md
%{_bindir}/durdraw
%{_bindir}/durfetch
%{_bindir}/durview
%{_mandir}/man1/durdraw.1*
%{_mandir}/man1/durfetch.1*
%{_mandir}/man1/durview.1*

%changelog
%autochangelog
