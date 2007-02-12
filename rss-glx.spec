# TODO:
# - --with-kdessconfigdir
# - more detailed desc.
#
# Conditional build:
%bcond_without	sound	# without sound
#
%define		rname	rss-glx
Summary:	The Really Slick Screensavers
Summary(pl.UTF-8):	Naprawdę zgrabne wygaszacze ekranu
Name:		rss_glx
Version:	0.7.6
Release:	0.1
Group:		X11/Applications
License:	GPL
Source0:	http://dl.sourceforge.net/rss-glx/%{rname}_%{version}.tar.bz2
# Source0-md5:	c896bd55e9ffdfad69bda4422b42e03b
Source1:	%{name}_install
URL:		http://rss-glx.sourceforge.net/
BuildRequires:	ImageMagick-devel >= 5.5.7
%{?with_sound:BuildRequires:	OpenAL-devel}
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Requires:	OpenGL
Requires:	xscreensaver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1 libGLcore.so.1
%define		_sysconfdir	/etc/X11

%description
GLX screensavers for the X11 windowing system.

%description -l pl.UTF-8
Wygaszacze ekranu oparte o GLX dla systemu X11.

%prep
%setup -qn %{rname}_%{version}

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-configdir=%{_sysconfdir}/xscreensaver \
	%{!?with_sound: --disable-sound}

%{__make} \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/xscreensaver
mv -f $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_libdir}/xscreensaver

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo
echo " To use these savers with xscreensaver, just run"
echo " -> /usr/bin/rss_glx_install <-"
echo

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/xscreensaver/*
%attr(755,root,root) %{_sysconfdir}/xscreensaver/*.xml
%{_mandir}/man1/*
