%global somajor 1

Name:           libheif
Version:        1.23.7
Release:        %autorelease
Summary:        HEIF and AVIF file format decoder and encoder

License:        LGPL-3.0-or-later and MIT
URL:            https://github.com/strukturag/libheif
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        libheif-plugin-helper

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(openjph) >= 0.18.0
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libsharpyuv)
BuildRequires:  pkgconfig(rav1e)
BuildRequires:  pkgconfig(SvtAv1Enc)
%ifnarch %{ix86}
BuildRequires:  pkgconfig(openh264)
%endif

Requires:       python3
Recommends:     %{name}-ffmpeg%{_isa}

%description
libheif is an ISO/IEC 23008-12:2017 HEIF and AVIF (AV1 Image File Format)
file format decoder and encoder.

%package        ffmpeg
Summary:        FFmpeg plugin that enables hardware accelerated decoding of HEIF files
License:        MIT
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libswscale)
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    ffmpeg
The FFmpeg decoding plugin is an alternative decoder for all HEIF codecs and
can make use of hardware decoders.

%package        tools
Summary:        Tools for manipulating HEIF files
License:        MIT
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       shared-mime-info

%description    tools
This package provides tools for manipulating HEIF files.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1
rm -rf third-party/

%build
%cmake \
 -GNinja \
 -DBUILD_SHARED_LIBS=ON \
 -DBUILD_TESTING=OFF \
 -DCMAKE_COMPILE_WARNING_AS_ERROR=OFF \
 -DENABLE_PLUGIN_LOADING=ON \
 -DPLUGIN_DIRECTORY=%{_libdir}/%{name} \
 -DWITH_AOM_DECODER=ON \
 -DWITH_AOM_DECODER_PLUGIN=ON \
 -DWITH_AOM_ENCODER=ON \
 -DWITH_AOM_ENCODER_PLUGIN=ON \
 -DWITH_DAV1D=ON \
 -DWITH_DAV1D_PLUGIN=ON \
 -DWITH_EXAMPLES=ON \
 -DWITH_FFMPEG_DECODER=ON \
 -DWITH_FFMPEG_DECODER_PLUGIN=ON \
 -DWITH_JPEG_DECODER=ON \
 -DWITH_JPEG_DECODER_PLUGIN=ON \
 -DWITH_JPEG_ENCODER=ON \
 -DWITH_JPEG_ENCODER_PLUGIN=ON \
 -DWITH_LIBSHARPYUV=ON \
 -DWITH_OpenJPEG_DECODER=ON \
 -DWITH_OpenJPEG_DECODER_PLUGIN=ON \
 -DWITH_OpenJPEG_ENCODER=ON \
 -DWITH_OpenJPEG_ENCODER_PLUGIN=ON \
 -DWITH_OPENJPH_ENCODER=ON \
 -DWITH_OPENJPH_ENCODER_PLUGIN=ON \
 -DWITH_RAV1E=ON \
 -DWITH_RAV1E_PLUGIN=ON \
 -DWITH_SvtEnc=ON \
 -DWITH_SvtEnc_PLUGIN=ON \
%ifnarch %{ix86}
 -DWITH_OpenH264_DECODER=ON \
 -DWITH_OpenH264_DECODER_PLUGIN=ON \
%endif
 -DWITH_UNCOMPRESSED_CODEC=ON \
 -DWITH_GDK_PIXBUF=OFF \
 -Wno-dev

%cmake_build

%install
%cmake_install

install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_libexecdir}/%{name}/libheif-plugin-helper

%post
if [ $1 -ge 1 ]; then
    %{_libexecdir}/%{name}/libheif-plugin-helper || :
fi

%postun
if [ $1 -eq 0 ]; then
    rm -f %{_libdir}/%{name}/libheif-*.so %{_libdir}/%{name}/.abi.hash || :
fi

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.%{somajor}{,.*}
%dir %{_libdir}/%{name}
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/libheif-plugin-helper
%{_libdir}/%{name}/%{name}-aomdec.so
%{_libdir}/%{name}/%{name}-aomenc.so
%{_libdir}/%{name}/%{name}-dav1d.so
%{_libdir}/%{name}/%{name}-j2kdec.so
%{_libdir}/%{name}/%{name}-j2kenc.so
%{_libdir}/%{name}/%{name}-jpegdec.so
%{_libdir}/%{name}/%{name}-jpegenc.so
%{_libdir}/%{name}/%{name}-jphenc.so
%{_libdir}/%{name}/%{name}-rav1e.so
%{_libdir}/%{name}/%{name}-svtenc.so
%ifnarch %{ix86}
%{_libdir}/%{name}/%{name}-openh264dec.so
%endif

%files ffmpeg
%{_libdir}/%{name}/%{name}-ffmpegdec.so

%files tools
%{_bindir}/heif-*
%{_mandir}/man1/heif-*
%{_datadir}/thumbnailers/heif.thumbnailer

%files devel
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%changelog
%autochangelog
