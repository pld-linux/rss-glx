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
Version:	0.8.1
Release:	1
Group:		X11/Applications
License:	GPL
Source0:	http://dl.sourceforge.net/rss-glx/%{rname}_%{version}.tar.bz2
# Source0-md5:	a2bdf0e10ee4e89c8975f313c5c0ba6f
Source1:	%{name}_install
URL:		http://rss-glx.sourceforge.net/
BuildRequires:	ImageMagick-devel >= 5.5.7
%{?with_sound:BuildRequires:	OpenAL-devel}
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Requires:	OpenGL
Requires:	xscreensaver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1 libGLcore.so.1
%define		_sysconfdir	/etc/X11
%define		_themedir	/usr/share/applications/screensavers

%description
GLX screensavers for the X11 windowing system.

%description -l pl.UTF-8
Wygaszacze ekranu oparte o GLX dla systemu X11.

%package -n gnome-screensaver-theme-rss-glx
Summary:	GNOME Screensaver themes for the Really Slick Screensavers
Summary(pl.UTF-8):	Tematy wygaszacza ekranu GNOME dla naprawdę zgrabnych wygaszaczy ekranu
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description -n gnome-screensaver-theme-rss-glx
GLX screensaver themes for GNOME Screensaver.

%description -n gnome-screensaver-theme-rss-glx -l pl.UTF-8
Tematy oparte o GLX dla wygaszacza ekranu GNOME.

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
install -d $RPM_BUILD_ROOT%{_themedir}
mv -f $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_libdir}/xscreensaver

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

generate_fix_desktop_files_links () {
	local line name trycmd cmd desc
	while read line;
	do
		eval $(echo "$line" | awk -F§ '{print "name=\"" $1 "\"; cmd=\"" $2 "\"; desc=\"" $3 "\""}')
		trycmd="${cmd%%%% *}"
		cat << EOF > $RPM_BUILD_ROOT%{_themedir}/rss-glx-${cmd}.desktop

[Desktop Entry]
Encoding=UTF-8
Name=${name}
Comment=${desc}
TryExec=rss-glx-${trycmd}
Exec=rss-glx-${cmd} -r
StartupNotify=false
Terminal=false
Type=Application
Categories=Screensaver
EOF
	done
}
cat << EOF | generate_fix_desktop_files_links
BioF§biof§This is an attempt to recreate some of the work of William Latham.
Busy Spheres§busyspheres§Spheres made of dancing particles.
Colorfire§colorfire§Burning colors.
Cyclone§cyclone§A cyclone made of particles.
Euphoria§euphoria§Psychedelic shapes.
Fieldlines§fieldlines§A simulation of the electric field lines between charged particles.
Flocks§flocks§Flocks of birds.
Flux§flux§If you know anything about strange attractors, you might recognize the patterns created by this screensaver.
Helios§helios§Throw together some attraction/repulsion particle effects and some smooth implicit surfaces and this is what you get.
Hufo's Smoke§hufo_smoke§Smoke effect.
Hufo's Tunnel§hufo_tunnel§Inside a tunnel.
Hyperspace§hyperspace§Hyperspace.
Lattice§lattice§Fly through an endless world of linked rings.
MatrixView§matrixview§The Matrix.
Plasma§plasma§Probably the second most psychedelic screensaver in existence.
Skyrocket (silent)§skyrocket -v 0§The most full-blown fireworks screensaver ever. It has bright lights, smoke trails, clouds that are illuminated by the explosions, sound effects, and plenty of other eye candy. Silent version.
Skyrocket§skyrocket§The most full-blown fireworks screensaver ever. It has bright lights, smoke trails, clouds that are illuminated by the explosions, sound effects, and plenty of other eye candy. With sound.
Solarwinds§solarwinds§This is a very mesmerizing particle effects saver.
SpirographX§spirographx§Spirograph-like screensaver.
Sundancer2§sundancer2§Rotating stack of quads.
EOF

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

%files -n gnome-screensaver-theme-rss-glx
%defattr(644,root,root,755)
%{_themedir}/*.desktop
