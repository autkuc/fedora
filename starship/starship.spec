Name:           starship
Version:        1.27.0
Release:        %autorelease
Summary:        The minimal, blazing-fast, and infinitely customizable prompt for any shell

License:        ISC
URL:            https://starship.rs
Source0:        https://github.com/starship/starship/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  cargo-rpm-macros
BuildRequires:  gcc

%description
Starship is the minimal, blazing-fast, and infinitely customizable prompt
for any shell! It is designed to show only the information you need while
being fast, reliable, and easily configurable.

%prep
%autosetup -n starship-%{version} -p1

%build
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
export CARGO_PROFILE_RELEASE_DEBUG=2
cargo build --release --locked

%install
install -D -p -m 0755 target/release/starship %{buildroot}%{_bindir}/starship

install -d %{buildroot}%{_datadir}/bash-completion/completions
%{buildroot}%{_bindir}/starship completions bash > %{buildroot}%{_datadir}/bash-completion/completions/starship || :

install -d %{buildroot}%{_datadir}/fish/vendor_completions.d
%{buildroot}%{_bindir}/starship completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/starship.fish || :

install -d %{buildroot}%{_datadir}/zsh/site-functions
%{buildroot}%{_bindir}/starship completions zsh > %{buildroot}%{_datadir}/zsh/site-functions/_starship || :

%check
%{buildroot}%{_bindir}/starship --version

%files
%license LICENSE
%doc README.md
%{_bindir}/starship
%{_datadir}/bash-completion/completions/starship
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/starship.fish
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_starship

%changelog
%autochangelog
