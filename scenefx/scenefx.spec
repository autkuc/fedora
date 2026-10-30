Name:           scenefx
Version:        0.5
Release:        %autorelease
Summary:        Drop-in replacement for the wlroots scene API with effects

License:        MIT
URL:            https://github.com/wlrfx/scenefx
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

Provides:       scenefx-devel = %{version}-%{release}

BuildRequires:  gcc
BuildRequires:  meson >= 1.3.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(wlroots-0.20) >= 0.20.0
BuildRequires:  pkgconfig(wayland-server) >= 1.24.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(xkbcommon) >= 1.8.0
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(lcms2)

%description
SceneFX is a drop-in replacement for the wlroots scene API that allows
compositors to render surfaces with eye-candy effects like blur, shadows,
rounded corners, and smooth animations.

%prep
%autosetup -n scenefx-%{version}

%build
%meson \
    -Dexamples=false \
    -Drenderers=gles2
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libscenefx-0.5.so
%{_includedir}/scenefx-0.5/
%{_libdir}/pkgconfig/scenefx-0.5.pc

%changelog
%autochangelog
