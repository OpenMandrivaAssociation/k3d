Summary:	K-3D open-source 3D modeling, animation, and rendering system
Name:		k3d
Version:	0.8.0.2
Release:	%mkrel 1
License:	GPLv2+
Group:		Graphics
URL:		http://www.k-3d.org
Source0:	http://downloads.sourceforge.net/k3d/%{name}-source-%{version}.tar.bz2
Source1:	%{name}.desktop
Patch1:		k3d-0.8.0.1-libdl.patch
Patch2:		k3d-0.8.0.2-gtkmm224.patch
Patch3:		k3d-0.8.0.2-gcc-4.6.diff
Patch4:		k3d-0.8.0.2-lib64.patch
BuildRequires:	gtkmm2.4-devel >= 2.12.3
BuildRequires:	boost-devel
BuildRequires:	mesa-common-devel
BuildRequires:	expat-devel
BuildRequires:	libgts-devel
BuildRequires:	imagemagick-devel
BuildRequires:	graphviz
BuildRequires:	doxygen
BuildRequires:	libext2fs-devel
BuildRequires:	libuuid-devel
BuildRequires:	gtkglext-devel
BuildRequires:	freetype2-devel
BuildRequires:	libOpenEXR-devel
BuildRequires:	libtiff-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	python-devel >= 2.5
BuildRequires:	glew-devel
BuildRequires:	librsvg-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	libgtksourceview-2.0-devel
BuildRequires:	cmake
%ifarch x86_64
BuildRequires:	chrpath
%endif
Requires:	yafray
Requires:	povray
Requires:	aqsis
Conflicts:	k3d-devel < %{version}
Obsoletes:	%{mklibname k3d 0} <= %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
Obsoletes:	%{mklibname k3d -d} <= %{version}-%{release}
Obsoletes:	%{mklibname k3d -d -s} <= %{version}-%{release}

%description devel
Development libraries needed to develop new k3d plugins.

%prep 
%setup -q -n %{name}-source-%{version}
%patch1 -p1 -b .dl
%patch2 -p1 -b .gtkmm
%patch3 -p1 -b .gcc
%patch4 -p1 -b .lib64

%build
%cmake \
    -DK3D_BUILD_GTS_MODULE:BOOL=ON
export LD_LIBRARY_PATH=%{_builddir}/k3d-source-%{version}/build/lib:%{_builddir}/k3d-source-%{version}/build/%{_lib}:$LD_LIBRARY_PATH
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
pushd build
%makeinstall_std
popd

mkdir -p %{buildroot}%{_datadir}/applications
install -m644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_desktop_database}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database}
%clean_icon_cache hicolor
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README
%{_bindir}/%{name}*
%{_libdir}/libk3d*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/plugins
%{_datadir}/%{name}
%exclude %{_datadir}/k3d/shaders/*.h
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop

%files devel
%defattr(-,root,root)
%{_libdir}/libk3d*.so
%{_libdir}/%{name}/include
%{_includedir}/%{name}
%{_datadir}/k3d/shaders/*.h
