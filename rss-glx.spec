# TODO:
# - --with-kdessconfigdir
# - more detailed desc.
#
# Conditional build:
# _without_sound 	- without sound
#
Summary:	The Really Slick Screensavers
Name:		rss_glx
Version:	0.7.4
Release:	0.1
Group:		X11/Applications
License:	GPL
Source0:	http://heanet.dl.sourceforge.net/sourceforge/rss-glx/%{name}-%{version}.tar.bz2
# Source0-md5:	4c3dfd7da7bed6af053febae860a09fc
Source1:	%{name}_install
Patch0:		%{name}-asm_cpu_detect_fix.patch
URL:		http://rss-glx.sourceforge.net/
BuildRequires:	OpenGL-devel
%{!?_without_sound:BuildRequires:	OpenAL-devel}
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Requires:	xscreensaver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreqdep   libGL.so.1 libGLU.so.1 libGLcore.so.1
%define         _sysconfdir     /etc/X11

%description
GLX screensavers for the X11 windowing system.

%description -l pl
Wygaszacze ekranu oparte o GLX dla systemu X11.

%prep
%setup -q
%patch -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
        --with-configdir=%{_sysconfdir}/xscreensaver \
	%{?_without_sound: --disable-sound}

%{__make} CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT%{_libdir}/xscreensaver

cd $RPM_BUILD_ROOT%{_bindir}
for file in *
 do
 mv -f ${file} $RPM_BUILD_ROOT%{_libdir}/xscreensaver/${file}
done
cd -

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
