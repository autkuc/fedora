%global modulename bubblewrap
%global selinuxtype targeted

Name:           bubblewrap-selinux
Version:        1.0.11
Release:        1
Summary:        SELinux policy for bubblewrap
License:        GPL-2.0-or-later
URL:            https://codeberg.org/HastD/bubblewrap-restricted
Source0:        bubblewrap.fc
Source1:        bubblewrap.if
Source2:        bubblewrap.te

BuildRequires:  flatpak-selinux
BuildRequires:  make
BuildRequires:  selinux-policy-devel

Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
Recommends:     bubblewrap
BuildArch:      noarch
%{?selinux_requires_min}

%description
SELinux policy module for bubblewrap (https://github.com/containers/bubblewrap).

This is a port of the bubblewrap policy in SELinux Refpolicy to Fedora's
SELinux policy.

%prep
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} .

%build
make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp

%install
install -Dp -m 0644 -t %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype} %{modulename}.pp.bz2
install -Dp -m 0644 -t %{buildroot}%{_datadir}/selinux/devel/include/distributed %{modulename}.if

%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%postun
if [ "$1" -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
    %selinux_relabel_post -s %{selinuxtype}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{modulename}.if
%ghost %verify(not md5 size mode mtime) %{_selinux_store_path}/%{selinuxtype}/active/modules/200/%{modulename}

%changelog
* Tue Nov 24 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.11-1
- Avoid granting unnecessary permissions alongside entrypoint

* Thu Nov 05 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.10-1
- Allow no-new-privileges domain transition for confined users

* Tue Nov 03 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.9-1
- Allow bwrap to resolve symlinks

* Thu Oct 29 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.8-1
- Allow noatsecure transition from bubblewrap back to userdomain

* Wed Oct 28 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.7-1
- Allow cap_dac_read_search in bwrap userns

* Tue Oct 27 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.6-1
- Allow bwrap to execute files in flatpak directories
- Allow bwrap to read socket metadata

* Tue Sep 29 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.5-1
- Allow bwrap to read device node file attributes

* Mon Sep 28 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.4-1
- Allow bwrap to read file metadata

* Sun Sep 27 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.3-1
- Allow thumb_t to execute bwrap

* Fri Sep 25 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.2-1
- Add domain transition when bubblewrap executes lib_t
- Fix policy gaps with home directory content

* Tue Sep 22 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.1-1
- Allow no-new-privileges transition from unconfined to bubblewrap domain

* Sat Sep 19 2026 Daniel Hast <hast.daniel@protonmail.com> - 1.0.0-1
- Initial release
