Summary:	K-3D open-source 3D modeling, animation, and rendering system
Name:		k3d
Version:	0.7.3.0
Release:	%mkrel 1
License:	GPLv2+
Group:		Graphics
Url:		http://www.k-3d.org
Source0:	http://downloads.sourceforge.net/k3d/%{name}-source-%{version}.tar.bz2
Source1:	%{name}.desktop
Patch0:		%{name}-source-0.7.3.0-libdir-output-path.patch
BuildRequires:	gtkmm2.4-devel >= 2.12.3
BuildRequires:	boost-devel
BuildRequires:	mesa-common-devel
BuildRequires:	libexpat-devel >= 2.0.1
BuildRequires:	libgts-devel
BuildRequires:	imagemagick-devel
BuildRequires:	graphviz
BuildRequires:	doxygen
BuildRequires:	libext2fs-devel
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
BuildRequires:	cmake
%ifarch x86_64
BuildRequires:	chrpath
%endif
Requires:	yafray
Requires:	povray
Requires:	aqsis
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

%description devel
Development libraries needed to develop new k3d plugins.

%prep 
%setup -q -n %{name}-source-%{version}
%if %{_lib} != lib 
%patch0 -p1
%endif

%build
%cmake \
    -DK3D_IMAGEMAGICK_INCLUDE_DIR="%{_includedir}/ImageMagick" \
    -DK3D_BUILD_GTS_MODULE:BOOL=ON

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
pushd build
%makeinstall_std

#ifarch x86_64
#chrpath -d %{buildroot}%{_libdir}/%{name}/*.so.0.0.0
#chrpath -d %{buildroot}%{_libdir}/*.so.0.0.0
#chrpath -d %{buildroot}%{_bindir}/k3d-bin
#chrpath -d %{buildroot}%{_bindir}/k3d-bug-buddy
#chrpath -d %{buildroot}%{_bindir}/k3d-make-module-proxy
#chrpath -d %{buildroot}%{_bindir}/k3d-renderframe
#chrpath -d %{buildroot}%{_bindir}/k3d-renderjob
#chrpath -d %{buildroot}%{_bindir}/k3d-sl2xml
#endif

popd

mkdir -p %{buildroot}%{_datadir}/applications
install -m644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%{update_menus}
%{update_desktop_database}
%update_icon_cache hicolor

%postun
%{clean_menus}
%{clean_desktop_database}
%clean_icon_cache hicolor

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README INSTALL
%dir %{_datadir}/%{name}
%{_bindir}/%{name}*
%{_libdir}/%{name}/plugins
%{_libdir}/%{name}/uiplugins
%{_datadir}/%{name}/*.k3d
%{_datadir}/%{name}/icons/*
%{_datadir}/%{name}/documents
%{_datadir}/%{name}/ngui/*
%{_datadir}/%{name}/scripts/*
%{_datadir}/%{name}/shaders/*
%{_datadir}/%{name}/lsystem/*
%{_datadir}/%{name}/textures/*
%{_datadir}/%{name}/qtui/*
%{_datadir}/%{name}/fonts/*.ttf
%{_datadir}/%{name}/logo/*.svg
%{_datadir}/%{name}/tutorials/*
%{_datadir}/%{name}/locale/*
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop

%files devel
%defattr(-,root,root)
%{_libdir}/libk3dsdk*.so
%{_libdir}/%{name}/include
%{_includedir}/%{name}
