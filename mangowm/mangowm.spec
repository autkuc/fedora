Name:           mangowm
Version:        0.18.5
Release:        %autorelease
Summary:        Lightweight tiling Wayland compositor with smooth animations

License:        GPL-3.0-or-later
URL:            https://github.com/mangowm/mango
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/mango-%{version}.tar.gz

Provides:       mangowm = %{version}-%{release}
Obsoletes:      mangowm < %{version}-%{release}

Obsoletes:      mango < %{version}-%{release}

Provides:       mangowc = %{version}-%{release}
Obsoletes:      mangowc < %{version}-%{release}

Provides:       mmsg = %{version}-%{release}
Provides:       mango-tools = %{version}-%{release}
Obsoletes:      mango-tools < %{version}-%{release}

Provides:       wayland-compositor

Conflicts:      mangowm-git
Conflicts:      mango-git
Conflicts:      mangowc-git
Conflicts:      mangowm-wlonly

BuildRequires:  gcc
BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig
BuildRequires:  cjson-devel
BuildRequires:  scenefx
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.32
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.23.1
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput) >= 1.27.1
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-randr)

Recommends:     xorg-x11-server-Xwayland

%description
Mango is a lightweight, feature-rich Wayland compositor inspired by dwl,
built on top of wlroots and scenefx. It features built-in smooth window
animations, drop shadows, corner rounding, blur, flexible tiling layouts
(Master-Stack, Monocle, Scroller, Grid), an IPC client (mmsg), and
hot-reloadable configuration.

%prep
%autosetup -n mango-%{version}

%build
%meson -Dxwayland=enabled
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}%{_datadir}/wayland-sessions/mango.desktop || :

%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/mango
%config(noreplace) %{_sysconfdir}/mango/config.conf
%config(noreplace) %{_sysconfdir}/mango/config.toml
%{_bindir}/mango
%{_bindir}/mmsg
%{_bindir}/mangonag
%{_datadir}/wayland-sessions/mango.desktop
%dir %{_datadir}/xdg-desktop-portal
%{_datadir}/xdg-desktop-portal/mango-portals.conf
%{_userunitdir}/mango-session.target
%{_mandir}/man1/mmsg.1*
%{_mandir}/man1/mangonag.1*

%changelog
%autochangelog
