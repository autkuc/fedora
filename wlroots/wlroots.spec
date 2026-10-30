%global abi_ver 0.20

Name:           wlroots
Version:        0.20.2
Release:        %autorelease
Summary:        A modular Wayland compositor library

License:        MIT
URL:            https://gitlab.freedesktop.org/wlroots/wlroots
Source0:        %{url}/-/releases/%{version}/downloads/%{name}-%{version}.tar.gz

Provides:       wlroots-devel = %{version}-%{release}

BuildRequires:  gcc
BuildRequires:  glslang
BuildRequires:  meson >= 1.3.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig

BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm) >= 21.1
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdisplay-info) >= 0.2.0
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(libinput) >= 1.21.0
BuildRequires:  pkgconfig(libliftoff) >= 0.5.0
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(vulkan) >= 1.2.182
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.24.0
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes) >= 1.15
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xkbcommon) >= 1.8.0
BuildRequires:  pkgconfig(xwayland)

%description
wlroots is a modular Wayland compositor library that provides pluggable,
composable, and un-opinionated modules for building Wayland compositors.

%prep
%autosetup -n %{name}-%{version}

%build
%meson \
    -Dexamples=false
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_libdir}/libwlroots-%{abi_ver}.so
%{_includedir}/wlroots-%{abi_ver}/
%{_libdir}/pkgconfig/wlroots-%{abi_ver}.pc

%changelog
%autochangelog
