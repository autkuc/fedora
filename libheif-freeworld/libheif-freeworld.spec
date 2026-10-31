Name:           libheif-freeworld
Version:        1.23.7
Release:        1%{?dist}
Summary:        H.264, HEVC and VVC support for HEIF and AVIF
License:        LGPL-3.0-or-later AND MIT
URL:            https://github.com/strukturag/libheif
Source0:        %{url}/archive/v%{version}/libheif-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  cmake(vvdec)
BuildRequires:  cmake(vvenc)
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(libde265)
BuildRequires:  pkgconfig(x264)
BuildRequires:  pkgconfig(x265)
BuildRequires:  pkgconfig(zlib)

Requires:       libheif%{_isa} = %{version}
Supplements:    libheif%{_isa}

Provides:       libheif-hevc = %{version}-%{release}
Obsoletes:      libheif-hevc < %{version}-%{release}

%description
Codec plugins adding H.264, HEVC and VVC support to applications using
libheif to read and write HEIF and AVIF images.

%prep
%autosetup -p1 -n libheif-%{version}
rm -rf third-party/

%build
%cmake \
    -GNinja \
    -DBUILD_TESTING=ON \
    -DCMAKE_COMPILE_WARNING_AS_ERROR=OFF \
    -DPLUGIN_DIRECTORY=%{_libdir}/libheif \
    -DWITH_EXAMPLES:BOOL=OFF \
    -DWITH_LIBDE265_PLUGIN:BOOL=ON \
    -DWITH_UNCOMPRESSED_CODEC=ON \
    -DWITH_VVDEC:BOOL=ON \
    -DWITH_VVDEC_PLUGIN:BOOL=ON \
    -DWITH_VVENC:BOOL=ON \
    -DWITH_VVENC_PLUGIN:BOOL=ON \
    -DWITH_X264_PLUGIN:BOOL=ON \
    -DWITH_X265_PLUGIN:BOOL=ON \
    -Wno-dev
%cmake_build

%install
%cmake_install

# Ship only plugins; Fedora's libheif package owns the library and headers.
pushd %{buildroot}
rm -rf .%{_includedir}/libheif
rm -rf .%{_libdir}/cmake/libheif
rm -f  .%{_libdir}/libheif.so*
rm -f  .%{_libdir}/pkgconfig/libheif.pc
popd

%check
%ctest

%files
%license COPYING
%doc README.md
%{_libdir}/libheif/libheif-libde265.so
%{_libdir}/libheif/libheif-vvdec.so
%{_libdir}/libheif/libheif-vvenc.so
%{_libdir}/libheif/libheif-x264.so
%{_libdir}/libheif/libheif-x265.so

%changelog
%autochangelog
