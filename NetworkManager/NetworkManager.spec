Name:           NetworkManager
Epoch:          1
Version:        1.59.1-dev
Release:        %autorelease
Summary:        Network connection manager and user applications (iwd Wi-Fi backend)

License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://networkmanager.dev/
Source0:        https://gitlab.freedesktop.org/NetworkManager/NetworkManager/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz

%global nmplugindir %{_libdir}/%{name}/%{version}-%{release}

BuildRequires:  gcc
BuildRequires:  meson >= 0.59.0
BuildRequires:  ninja-build
BuildRequires:  gettext-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  dbus-devel
BuildRequires:  glib2-devel >= 2.40.0
BuildRequires:  gobject-introspection-devel
BuildRequires:  gnutls-devel >= 2.12
BuildRequires:  readline-devel
BuildRequires:  audit-libs-devel
BuildRequires:  libpsl-devel
BuildRequires:  libcurl-devel
BuildRequires:  libndp-devel
BuildRequires:  newt-devel
BuildRequires:  systemd-devel
BuildRequires:  polkit-devel
BuildRequires:  jansson-devel
BuildRequires:  libbpf-devel
BuildRequires:  libnvme-devel
BuildRequires:  libuuid-devel
BuildRequires:  mobile-broadband-provider-info-devel
BuildRequires:  ModemManager-glib-devel
BuildRequires:  bluez-libs-devel
BuildRequires:  ppp-devel
BuildRequires:  vala
BuildRequires:  bash-completion
BuildRequires:  python3
BuildRequires:  python3-gobject-base
BuildRequires:  libxslt
BuildRequires:  firewalld-filesystem
BuildRequires:  iwd

Requires:       %{name}-libnm%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       iproute
Requires:       iwd
Recommends:     %{name}-wifi%{?_isa} = %{epoch}:%{version}-%{release}
Provides:       networkmanager = %{epoch}:%{version}-%{release}

Provides:       %{name}-bluetooth = %{epoch}:%{version}-%{release}
Provides:       %{name}-wwan = %{epoch}:%{version}-%{release}
Provides:       %{name}-ppp = %{epoch}:%{version}-%{release}

%description
NetworkManager is a system service that manages network devices and
connections. This package is built with native iwd backend support
as the default Wi-Fi manager without wpa_supplicant dependencies.

%package        wifi
Summary:        Wi-Fi support for NetworkManager using iwd
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       iwd
Recommends:     wireless-regdb
Provides:       networkmanager-wifi = %{epoch}:%{version}-%{release}
Obsoletes:      NetworkManager-wifi < %{epoch}:%{version}-%{release}

%description    wifi
This package provides Wi-Fi support for NetworkManager powered by iwd
(Internet Wireless Daemon).

%package        tui
Summary:        Terminal user interface for NetworkManager (nmtui)
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Provides:       networkmanager-tui = %{epoch}:%{version}-%{release}

%description    tui
This package contains nmtui, an interactive curses-based user interface
for NetworkManager.

%package        cloud-setup
Summary:        Cloud network initialization service for NetworkManager
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Provides:       networkmanager-cloud-setup = %{epoch}:%{version}-%{release}

%description    cloud-setup
This package provides automatic network configuration in cloud environments.

%package        libnm
Summary:        NetworkManager client library
Provides:       networkmanager-libnm = %{epoch}:%{version}-%{release}

%description    libnm
This package contains the libnm shared client library used by applications
to interact with NetworkManager.

%package        libnm-devel
Summary:        Development files for libnm
Requires:       %{name}-libnm%{?_isa} = %{epoch}:%{version}-%{release}
Provides:       %{name}-devel = %{epoch}:%{version}-%{release}
Provides:       networkmanager-libnm-devel = %{epoch}:%{version}-%{release}

%description    libnm-devel
This package contains headers and pkg-config files for developing applications
with libnm.

%prep
%autosetup -p1 -n NetworkManager-%{version}

%build
%meson \
    -Ddist_version=%{version}-%{release} \
    -Dcrypto=gnutls \
    -Dsystemd_journal=true \
    -Dsuspend_resume=systemd \
    -Dsession_tracking_consolekit=false \
    -Dpolkit=true \
    -Dpolkit_agent=true \
    -Dpolkit_noauth_group=wheel \
    -Dmodify_system=true \
    -Dselinux=false \
    -Dlibaudit=yes-disabled-by-default \
    -Dwifi=true \
    -Diwd=true \
    -Dconfig_wifi_backend_default=iwd \
    -Dwext=false \
    -Dmodem_manager=true \
    -Dbluez5_dun=true \
    -Dppp=true \
    -Dnmtui=true \
    -Dnm_cloud_setup=true \
    -Dconfig_dns_rc_manager_default=auto \
    -Dconfig_logging_backend_default=journal \
    -Dvapi=true \
    -Dintrospection=true \
    -Ddocs=false \
    -Dtests=no

%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_prefix}/lib/NetworkManager/conf.d
cat << 'EOF' > %{buildroot}%{_prefix}/lib/NetworkManager/conf.d/30-wifi-backend.conf
[device]
wifi.backend=iwd
EOF

mkdir -p %{buildroot}%{_unitdir}/iwd.service.d
cat << 'EOF' > %{buildroot}%{_unitdir}/iwd.service.d/90-networkmanager.conf
[Unit]
After=systemd-udevd.service
Before=NetworkManager.service
EOF

mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/system-connections
mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d
mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/dnsmasq.d
mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/dnsmasq-shared.d
cat << 'EOF' > %{buildroot}%{_sysconfdir}/NetworkManager/NetworkManager.conf
[main]
plugins=keyfile
EOF

mkdir -p %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/no-wait.d
mkdir -p %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/pre-up.d
mkdir -p %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/pre-down.d
mkdir -p %{buildroot}%{_prefix}/lib/NetworkManager/system-connections
mkdir -p %{buildroot}%{_prefix}/lib/NetworkManager/VPN
mkdir -p %{buildroot}%{_localstatedir}/lib/NetworkManager

rm -rf %{buildroot}%{_datadir}/gtk-doc

%find_lang NetworkManager

%post
%systemd_post NetworkManager.service NetworkManager-wait-online.service NetworkManager-dispatcher.service

%preun
%systemd_preun NetworkManager.service NetworkManager-wait-online.service NetworkManager-dispatcher.service

%postun
%systemd_postun_with_restart NetworkManager.service

%files -f NetworkManager.lang
%license COPYING COPYING.LGPL COPYING.GFDL
%doc NEWS AUTHORS README.md CONTRIBUTING.md
%{_bindir}/nm*
%exclude %{_bindir}/nmtui*
%{_sbindir}/NetworkManager
%{_libexecdir}/nm-*
%exclude %{_libexecdir}/nm-cloud-setup
%{_unitdir}/NetworkManager*.service
%{_unitdir}/nm-priv-helper.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/polkit-1/rules.d/*.rules
%{_prefix}/lib/udev/rules.d/*.rules
%{_prefix}/lib/firewalld/zones/nm-shared.xml
%{_datadir}/bash-completion/completions/nmcli
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/conf.d
%dir %{_sysconfdir}/NetworkManager/system-connections
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%dir %{_sysconfdir}/NetworkManager/dnsmasq.d
%dir %{_sysconfdir}/NetworkManager/dnsmasq-shared.d
%config(noreplace) %{_sysconfdir}/NetworkManager/NetworkManager.conf
%dir %{_prefix}/lib/NetworkManager
%dir %{_prefix}/lib/NetworkManager/conf.d
%dir %{_prefix}/lib/NetworkManager/dispatcher.d
%dir %{_prefix}/lib/NetworkManager/dispatcher.d/no-wait.d
%dir %{_prefix}/lib/NetworkManager/dispatcher.d/pre-up.d
%dir %{_prefix}/lib/NetworkManager/dispatcher.d/pre-down.d
%dir %{_prefix}/lib/NetworkManager/system-connections
%dir %{_prefix}/lib/NetworkManager/VPN
%dir %{_localstatedir}/lib/NetworkManager
%dir %{_libdir}/NetworkManager
%dir %{nmplugindir}
%{nmplugindir}/libnm-device-plugin-*.so
%exclude %{nmplugindir}/libnm-device-plugin-wifi.so
%{nmplugindir}/libnm-wwan.so
%{nmplugindir}/libnm-ppp-plugin.so
%{_libdir}/pppd/*/*.so
%{_mandir}/man*/*
%exclude %{_mandir}/man1/nmtui*
%exclude %{_mandir}/man8/nm-cloud-setup*

%files wifi
%{nmplugindir}/libnm-device-plugin-wifi.so
%{_prefix}/lib/NetworkManager/conf.d/30-wifi-backend.conf
%{_unitdir}/iwd.service.d/90-networkmanager.conf

%files tui
%{_bindir}/nmtui*
%{_mandir}/man1/nmtui*

%files cloud-setup
%{_libexecdir}/nm-cloud-setup
%{_unitdir}/nm-cloud-setup.*
%{_mandir}/man8/nm-cloud-setup*
%{_prefix}/lib/NetworkManager/dispatcher.d/*90-nm-cloud-setup.sh
%{_prefix}/lib/NetworkManager/dispatcher.d/*/*90-nm-cloud-setup.sh

%files libnm
%{_libdir}/libnm.so.*
%{_libdir}/girepository-1.0/NM-1.0.typelib

%files libnm-devel
%{_includedir}/libnm/
%{_libdir}/libnm.so
%{_libdir}/pkgconfig/libnm.pc
%{_datadir}/gir-1.0/NM-1.0.gir
%{_datadir}/vala/vapi/libnm.*
%{_datadir}/dbus-1/interfaces/*.xml

%changelog
%autochangelog
