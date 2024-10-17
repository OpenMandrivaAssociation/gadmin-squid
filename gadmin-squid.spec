# if I fix the string literal errors according to the wiki Problems
# page, it crashes on startup - AdamW 2009/01
%define Werror_cflags %nil

Summary:	A GTK+ administation tool for the Squid proxy
Name:		gadmin-squid
Version:	0.1.3
Release:	4
License:	GPLv3+
Group:		System/Configuration/Networking
URL:		https://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gadmin-squid/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
Requires:	squid
Requires:	openssl
Requires:	usermode-consoleonly

%description
Gadmin-Samba is a fast and easy to use GTK+ administration tool for the
Samba server.

%prep
%setup -q

%build
%configure2_5x
%make

%install
%makeinstall_std

install -d %{buildroot}%{_sysconfdir}/%{name}

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

# Mandriva Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
sed -e 's,%{name}.png,%{name},g' \
	-e 's,GADMIN-SQUID,Gadmin-Squid,g'\
	desktop/%name.desktop > %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Prepare usermode entry
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}

%files
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/%{name}.png



%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-2mdv2011.0
+ Revision: 610789
- rebuild

* Wed Apr 07 2010 Funda Wang <fwang@mandriva.org> 0.1.3-1mdv2010.1
+ Revision: 532670
- new version 0.1.3

* Thu Jan 07 2010 Emmanuel Andry <eandry@mandriva.org> 0.1.2-1mdv2010.1
+ Revision: 487290
- New version 0.1.2

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.1.0-2mdv2010.0
+ Revision: 437645
- rebuild

* Sun Jan 04 2009 Adam Williamson <awilliamson@mandriva.org> 0.1.0-1mdv2009.1
+ Revision: 324176
- import gadmin-squid


