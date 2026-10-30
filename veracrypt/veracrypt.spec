Name:           veracrypt
Version:        1.26.30
Release:        1%{?dist}
Summary:        Disk encryption software

License:        Apache-2.0 AND TrueCrypt-3.0
URL:            https://github.com/veracrypt/VeraCrypt
Source0:        https://github.com/veracrypt/VeraCrypt/releases/download/VeraCrypt_%{version}/VeraCrypt_%{version}_Source.tar.bz2

ExclusiveArch:  x86_64

Provides:       veracrypt-cli = %{version}-%{release}
Provides:       veracrypt-gui = %{version}-%{release}
Provides:       veracrypt-nogui = %{version}-%{release}
Provides:       truecrypt = 7.1a-1

Obsoletes:      veracrypt-cli < %{version}-%{release}
Obsoletes:      veracrypt-gui < %{version}-%{release}
Obsoletes:      veracrypt-nogui < %{version}-%{release}
Obsoletes:      truecrypt <= 7.1a-1

Conflicts:      truecrypt
Conflicts:      truecrypt-gui
Conflicts:      truecrypt-console

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  yasm
BuildRequires:  pkgconfig
BuildRequires:  openssl-devel
BuildRequires:  device-mapper-devel
BuildRequires:  fuse-devel
BuildRequires:  pcsc-lite-devel
BuildRequires:  wxGTK-devel
BuildRequires:  desktop-file-utils

Requires:       cryptsetup
Requires:       hicolor-icon-theme

%description
VeraCrypt is a free open-source disk encryption software based on TrueCrypt.
It supports both graphical and command-line interfaces.

%prep
%autosetup -c -n %{name}-%{version}

%build
cd src
%make_build \
    WX_CONFIG=wx-config \
    NOSTRIP=1 \
    NOTEST=1 \
    TC_EXTRA_CFLAGS="%{optflags}" \
    TC_EXTRA_CXXFLAGS="%{optflags}" \
    TC_EXTRA_LFLAGS="%{build_ldflags}"

%install
install -D -p -m 0755 src/Main/veracrypt %{buildroot}%{_bindir}/veracrypt
install -D -p -m 0755 src/Setup/Linux/mount.veracrypt %{buildroot}%{_sbindir}/mount.veracrypt
install -D -p -m 0644 src/Setup/Linux/veracrypt.desktop %{buildroot}%{_datadir}/applications/veracrypt.desktop
install -D -p -m 0644 src/Setup/Linux/veracrypt.xml %{buildroot}%{_datadir}/mime/packages/veracrypt.xml
install -D -p -m 0644 src/Resources/Icons/VeraCrypt.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/veracrypt.svg
install -D -p -m 0644 src/Resources/Icons/VeraCrypt-256x256.xpm %{buildroot}%{_datadir}/pixmaps/veracrypt.xpm
install -D -p -m 0644 src/Resources/Icons/VeraCrypt-16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/veracrypt.png
install -D -p -m 0644 src/Resources/Icons/VeraCrypt-48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/veracrypt.png
install -D -p -m 0644 src/Resources/Icons/VeraCrypt-128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/veracrypt.png
install -D -p -m 0644 src/Resources/Icons/VeraCrypt-256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/veracrypt.png
install -d %{buildroot}%{_datadir}/veracrypt/languages
install -p -m 0644 Translations/*.xml %{buildroot}%{_datadir}/veracrypt/languages/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/veracrypt.desktop
%{buildroot}%{_bindir}/veracrypt --text --test

%files
%license License.txt
%doc README.md
%{_bindir}/veracrypt
%{_sbindir}/mount.veracrypt
%{_datadir}/applications/veracrypt.desktop
%{_datadir}/mime/packages/veracrypt.xml
%{_datadir}/pixmaps/veracrypt.xpm
%{_datadir}/icons/hicolor/*/apps/veracrypt.*
%{_datadir}/veracrypt/

%changelog
%autochangelog
