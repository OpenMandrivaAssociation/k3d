%define major 0
%define libname %mklibname k3d %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Summary:	K-3D open-source 3D modeling, animation, and rendering system
Name:		k3d
Version:	0.6.7.0
Release:	%mkrel 5
License:	GPLv2+
Group:		Graphics
Url:		http://k3d.sourceforge.net/new/
Source:		http://downloads.sourceforge.net/k3d/%{name}-%{version}-src.tar.bz2
Patch0:		%{name}-desktop.patch
Patch1:		k3d-0.6.6.0-configure-libdir.patch
# move guilib to %{_libdir}/%{name} as we need the .so, and we can't have .so
# symlinks in %{_libdir}
Patch2:		k3d-0.6.6.0-gui-in-pkglibdir.patch
Patch3:		k3d-0.6.7.0-sigc-hide.patch
BuildRequires:	gtkmm2.4-devel >= 2.12.3
BuildRequires:	boost-devel
BuildRequires:	mesa-common-devel
BuildRequires:	libexpat-devel >= 2.0.1
#BuildRequires:	libgts-devel
BuildRequires:	libMagick-devel
BuildRequires:	libgraphviz-devel
BuildRequires:	gtkglext-devel
BuildRequires:	freetype2-devel
BuildRequires:	libOpenEXR-devel
BuildRequires:	libtiff-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	python-devel >= 2.5
#BuildRequires:	superlu
BuildRequires:	librsvg2-devel
%ifarch x86_64
BuildRequires:	chrpath
%endif
Requires:	yafray
Requires:	povray
Requires:	aqsis
Requires:	%{_lib}%{name} = %{version}-%{release}

%description
K-3D is the free-as-in-freedom 3D modeling, animation, and rendering 
system for GNU / Linux, Posix, and Win32 operating systems. K-3D features a 
robust, object-oriented plugin architecture, designed to scale to the needs of 
professional artists, and is designed from-the-ground-up to generate 
motion-picture-quality animation using RenderMan-compliant render engines.

%package -n %{libname}
Summary:	K-3D libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
Libraries that is used for K-3D.

%package -n %{develname}
Summary:	K-3D development headers
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname -d k3d 0

%description -n %{develname}
Development libraries needed to develop new k3d plugins.

%package -n %{staticname}
Summary:	K-3D static libraries
License:	GPL
Group:		Development/C++
Provides:	%{name}-static-devel
Requires:	%{develname} = %{version}-%{release}

%description -n %{staticname}
Static libraries for K-3D.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
aclocal -I m4
autoconf
automake
%configure2_5x \
	--enable-shared \
	--enable-static \
	--without-libxml2 \
	--with-external-boost \
	--with-freetype2 \
	--without-gnome \
	--with-graphviz \
	--without-gts \
	--with-imagemagick \
	--with-jpeg \
	--with-ngui \
	--with-nls \
	--with-openexr \
	--with-png \
	--with-python \
	--without-qt \
	--without-superlu \
	--with-svg-icons \
	--with-tiff
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/%{name}-config

%ifarch x86_64
chrpath -d %{buildroot}%{_libdir}/%{name}/*.so.0.0.0
chrpath -d %{buildroot}%{_libdir}/*.so.0.0.0
chrpath -d %{buildroot}%{_bindir}/k3d-bin
chrpath -d %{buildroot}%{_bindir}/k3d-bug-buddy
chrpath -d %{buildroot}%{_bindir}/k3d-make-module-proxy
chrpath -d %{buildroot}%{_bindir}/k3d-renderframe
chrpath -d %{buildroot}%{_bindir}/k3d-renderjob
chrpath -d %{buildroot}%{_bindir}/k3d-sl2xml
%endif

%find_lang %{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%{update_menus}
%if %mdkversion >= 200700
%{update_desktop_database}
%update_icon_cache hicolor
%endif

%postun
%{clean_menus}
%if %mdkversion >= 200700
%{clean_desktop_database}
%clean_icon_cache hicolor
%endif

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README INSTALL TODO
%doc %{_datadir}/%{name}/documents
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-b*
%attr(755,root,root) %{_bindir}/%{name}-m*
%attr(755,root,root) %{_bindir}/%{name}-r*
%attr(755,root,root) %{_bindir}/%{name}-s*
%attr(755,root,root) %{_bindir}/%{name}-u*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.k3d
%{_datadir}/%{name}/icons/*
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

%files -n %{libname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.%{major}*
%attr(755,root,root) %{_libdir}/%{name}/*.so.%{major}*
%{_libdir}/%{name}/*.so

%files -n %{develname}
%defattr(644,root,root,755)
%multiarch %attr(755,root,root) %{multiarch_bindir}/%{name}-config
%attr(755,root,root) %{_bindir}/%{name}-config
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/%{name}/*.la
%{_includedir}/k3d

%files -n %{staticname}
%defattr(644,root,root,755)
%{_libdir}/*.a
%{_libdir}/%{name}/*.a
