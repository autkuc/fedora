# upstream: bitwarden-desktop
%global debug_package %{nil}
%global _build_id_links none

%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude ^(libffmpeg|libEGL|libGLESv2|libvk_swiftshader)\\.so.*$

Name:           bitwarden
Version:        2026.11.0
Release:        %autorelease
Summary:        A secure and free password manager for all of your devices

License:        GPL-3.0-only
URL:            https://github.com/bitwarden/clients
Source0:        %{url}/archive/refs/tags/desktop-v%{version}.tar.gz#/%{name}-%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  nodejs24
BuildRequires:  nodejs24-npm
BuildRequires:  nodejs24-devel
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  git-core
BuildRequires:  pkgconf-pkg-config
BuildRequires:  dbus-devel
BuildRequires:  glib2-devel
BuildRequires:  libsecret-devel
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme
Requires:       polkit

%description
Bitwarden is a free and open-source password management solution for
individuals, teams, and business organizations. This package builds the
Bitwarden desktop application and its native Rust modules from source.

%prep
%autosetup -n clients-desktop-v%{version} -p1

%build
mkdir -p .node24-bin
ln -sf %{_bindir}/node-24 .node24-bin/node
ln -sf %{_bindir}/npm-24 .node24-bin/npm
ln -sf %{_bindir}/npx-24 .node24-bin/npx
export PATH="$PWD/.node24-bin:$PATH"

export HUSKY=0
export npm_config_cache="%{_builddir}/.npm"
export CARGO_HOME="%{_builddir}/.cargo"
export ELECTRON_CACHE="%{_builddir}/.cache/electron"

npm ci
npm run build-native --workspace=@bitwarden/desktop -- --release
npm run build:oss --workspace=@bitwarden/desktop
npm run pack:dir --workspace=@bitwarden/desktop

%install
%ifarch x86_64
UNPACKED_DIR="apps/desktop/dist/linux-unpacked"
%endif
%ifarch aarch64
UNPACKED_DIR="apps/desktop/dist/linux-arm64-unpacked"
%endif

install -d %{buildroot}%{_libdir}/%{name}
cp -a "${UNPACKED_DIR}/." %{buildroot}%{_libdir}/%{name}/
chmod 0755 %{buildroot}%{_libdir}/%{name}/chrome-sandbox 2>/dev/null || :

install -d %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/bitwarden %{buildroot}%{_bindir}/bitwarden

install -D -p -m 0644 apps/desktop/resources/com.bitwarden.desktop.desktop \
    %{buildroot}%{_datadir}/applications/com.bitwarden.desktop.desktop

install -D -p -m 0644 apps/desktop/resources/com.bitwarden.desktop.policy \
    %{buildroot}%{_datadir}/polkit-1/actions/com.bitwarden.desktop.policy

for size in 16x16 32x32 64x64 128x128 256x256 512x512 1024x1024; do
    install -D -p -m 0644 "apps/desktop/resources/icons/${size}.png" \
        "%{buildroot}%{_datadir}/icons/hicolor/${size}/apps/com.bitwarden.desktop.png"
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.bitwarden.desktop.desktop

%files
%license LICENSE.txt LICENSE_GPL.txt
%doc README.md
%{_bindir}/bitwarden
%{_libdir}/%{name}/
%{_datadir}/applications/com.bitwarden.desktop.desktop
%{_datadir}/polkit-1/actions/com.bitwarden.desktop.policy
%{_datadir}/icons/hicolor/*/apps/com.bitwarden.desktop.png

%changelog
%autochangelog
