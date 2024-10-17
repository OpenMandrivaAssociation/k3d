Summary:	K-3D open-source 3D modeling, animation, and rendering system
Name:		k3d
Version:	0.8.0.6
Release:	1
License:	GPLv2+
Group:		Graphics
URL:		https://www.k-3d.org
Source0:	https://github.com/K-3D/k3d/archive/refs/tags/k3d-%{version}.tar.gz
Source1:	%{name}.desktop
Patch1:		k3d-0.8.0.1-libdl.patch
Patch2:		k3d-0.8.0.2-gtkmm224.patch
Patch3:		k3d-0.8.0.2-gcc-4.6.diff
Patch4:		k3d-0.8.0.2-lib64.patch
Patch5:		k3d-source-0.8.0.2_libpng15.patch
Patch6:		k3d-0.8.0.2-gcc-4.7.patch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	boost-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gnome-vfs-2.0)
BuildRequires:	pkgconfig(gtkglext-1.0)
BuildRequires:	pkgconfig(gtkmm-2.4)
BuildRequires:	pkgconfig(gtksourceview-2.0)
BuildRequires:	pkgconfig(gts)
BuildRequires:	pkgconfig(ImageMagick)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(uuid)
%ifarch x86_64
BuildRequires:	chrpath
%endif
Requires:	yafray
Requires:	povray
Requires:	aqsis
Conflicts:	k3d-devel < %{version}
Obsoletes:	%{_lib}k3d0 <= %{version}-%{release}

%description
K-3D is the free-as-in-freedom 3D modeling, animation, and rendering 
system for GNU / Linux, Posix, and Win32 operating systems. K-3D features a 
robust, object-oriented plugin architecture, designed to scale to the needs of 
professional artists, and is designed from-the-ground-up to generate 
motion-picture-quality animation using RenderMan-compliant render engines.

%package devel
Summary:	K-3D development headers
Group:		Development/C++
Requires:	%{name} = %{version}-%{release}
Conflicts:	k3d < 0.8.0.2
Obsoletes:	%{_lib}k3d-devel <= %{version}-%{release}
Obsoletes:	%{_lib}k3d-static-devel <= %{version}-%{release}

%description devel
Development libraries needed to develop new k3d plugins.

%prep
%setup -qn %{name}-source-%{version}
%autopatch -p1

%build
%cmake \
    -DK3D_BUILD_GTS_MODULE:BOOL=ON
export LD_LIBRARY_PATH=%{_builddir}/k3d-source-%{version}/build/lib:%{_builddir}/k3d-source-%{version}/build/%{_lib}:$LD_LIBRARY_PATH
%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_datadir}/applications
install -m644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS README
%{_bindir}/%{name}*
%{_libdir}/libk3d*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/plugins
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/documents
%{_datadir}/%{name}/fonts
%{_datadir}/%{name}/geometry
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/logo
%{_datadir}/%{name}/lsystem
%{_datadir}/%{name}/ngui
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/shaders
%{_datadir}/%{name}/textures
%{_datadir}/%{name}/*.k3d
%exclude %{_datadir}/k3d/shaders/*.h
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/*

%files devel
%{_libdir}/libk3d*.so
%{_libdir}/%{name}/include
%{_includedir}/%{name}
%{_datadir}/k3d/shaders/*.h


