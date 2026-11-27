# upstream: ente-auth
%global debug_package %{nil}
%global _build_id_links none

%global __provides_exclude_from ^%{_datadir}/enteauth/.*$
%global __requires_exclude ^(libflutter_linux_gtk\\.so|libflutter_rust_bridge.*\\.so)$

Name:           ente-auth
Version:        4.4.27
Release:        %autorelease
Summary:        2FA app with end-to-end encrypted backup and sync

License:        AGPL-3.0-only
URL:            https://github.com/ente-io/ente
Source0:        %{url}/archive/refs/tags/auth-v%{version}.tar.gz#/ente-auth-%{version}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  git-core
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gtk3-devel
BuildRequires:  glib2-devel
BuildRequires:  libsecret-devel
BuildRequires:  sqlite-devel
BuildRequires:  libayatana-appindicator3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       gtk3
Requires:       glib2
Requires:       libsecret
Requires:       sqlite-libs
Requires:       libayatana-appindicator3
Requires:       polkit
Requires:       hicolor-icon-theme

Provides:       enteauth = %{version}-%{release}

%description
Ente Auth is an open-source, end-to-end encrypted 2FA authenticator app.
It provides automatic cloud backups and multi-device synchronization
without compromising privacy or security.

%prep
%autosetup -n ente-auth-v%{version} -p1

%build
# Download official Flutter SDK toolchain for Linux desktop build
export FLUTTER_VERSION="3.47.8"
export FLUTTER_ROOT="%{_builddir}/flutter"
export PUB_CACHE="%{_builddir}/.pub-cache"
export CARGO_HOME="%{_builddir}/.cargo"

if [ ! -d "${FLUTTER_ROOT}" ]; then
    mkdir -p "${FLUTTER_ROOT}"
    curl -fsSL --retry 3 "https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz" | tar -xJ --strip-components=1 -C "${FLUTTER_ROOT}"
fi

export PATH="${FLUTTER_ROOT}/bin:${CARGO_HOME}/bin:$PATH"

# Build Rust bridge codegen & bindings
cd rust
cargo build --release --bin codegen
./target/release/codegen frb auth
cd ..

# Build Linux desktop bundle with Flutter
cd mobile/apps/auth
flutter config --no-analytics
flutter config --enable-linux-desktop
flutter pub get
flutter build linux --release --verbose

%install
cd mobile/apps/auth

# Install bundle to /usr/share/enteauth
install -d %{buildroot}%{_datadir}/enteauth
cp -a build/linux/x64/release/bundle/* %{buildroot}%{_datadir}/enteauth/

# Create binary symlink in /usr/bin
install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/enteauth/enteauth %{buildroot}%{_bindir}/enteauth

# Desktop application entry
install -D -p -m 0644 linux/packaging/enteauth.desktop \
    %{buildroot}%{_datadir}/applications/enteauth.desktop

# AppStream metadata
install -D -p -m 0644 linux/packaging/enteauth.appdata.xml \
    %{buildroot}%{_metainfodir}/enteauth.appdata.xml

# Application icon
install -D -p -m 0644 assets/generation-icons/icon-windows-linux.png \
    %{buildroot}%{_datadir}/pixmaps/io.ente.auth.png

# Polkit policy for biometric/system authentication
install -D -p -m 0644 assets/polkit/com.ente.auth.policy \
    %{buildroot}%{_datadir}/polkit-1/actions/com.ente.auth.policy

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/enteauth.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/enteauth.appdata.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/enteauth
%{_datadir}/enteauth/
%{_datadir}/applications/enteauth.desktop
%{_metainfodir}/enteauth.appdata.xml
%{_datadir}/pixmaps/io.ente.auth.png
%{_datadir}/polkit-1/actions/com.ente.auth.policy

%changelog
%autochangelog
