# $Id: c3-4.0.spec,v 1.2 2003/06/24 20:24:50 zbml1 Exp $

%define   name        c3
%define   ver         4.0
%define   rel         1
%define   prefix      /opt/c3-4
%define   profiled    /etc/profile.d

Summary: Cluster Command and Control (C3) - command line tool suite  
Name: %{name}
Version: %{ver}
Release: %{rel}
Copyright: freely distributable
Group: Application/System
Source0: %{name}-%{ver}.tar.gz
Packager: Thomas Naughton <naughtont@ornl.gov>
URL: http://www.csm.ornl.gov/torc/C3/
AutoReqProv: no
Requires: rsync
Requires: perl
Requires: /usr/bin/python2
BuildRoot: %{_tmppath}/%{name}-%{ver}-root

%description
The Cluster Command and Control (C3) tool suite offers a command line
interface for system and user administration tasks on a cluster. 




%package ckillnode
Summary: Cluster Command and Control (C3) - ckillnode
Group: Application/System

%description ckillnode
The Cluster Command and Control (C3) - 'ckillnode' command used 
on client nodes in conjunction with 'ckill' from headnode.  

NOTE: Only needed on client nodes.



%package profiled
Summary: Cluster Command and Control (C3) - profile.d scripts
Group: Application/System
Requires: c3 >= 4

%description profiled
The Cluster Command and Control (C3) tool suite offers a command line
interface for system and user administration tasks on a cluster. 

Scripts for PATHing information placed in the '/etc/profile.d/' area.



#---------------------------------------------------------------------
# Prep install section
#---------------------------------------------------------------------

%prep

# Get rid of any previously built stuff that might cause problems.
# (only worried about things in RPM-land '/usr/src/redhat/' here)
%__rm -rf $RPM_BUILD_ROOT

# Actually do the untar/gzip stuff
%setup -n %{name}-%{ver}



#---------------------------------------------------------------------
# Build section
#---------------------------------------------------------------------

%build

# Copy the build distribution to target install dir.  The files must
# exist in the desired location (path) when RPM checks the filelist. This
# is greatly simplified by using the BuildRoot (chroot sort of thing) method.
%__mkdir -p $RPM_BUILD_ROOT/%{prefix}
%__mkdir -p $RPM_BUILD_ROOT/%{profiled}

%__cp -Rf $RPM_BUILD_DIR/%{name}-%{ver}/* \
	  $RPM_BUILD_ROOT/%{prefix}

%__cp -Rf $RPM_BUILD_DIR/%{name}-%{ver}/c3.sh \
	  $RPM_BUILD_ROOT/%{profiled}

%__cp -Rf $RPM_BUILD_DIR/%{name}-%{ver}/c3.csh \
	  $RPM_BUILD_ROOT/%{profiled}


#---------------------------------------------------------------------
# Clean section
#---------------------------------------------------------------------

%clean
# Get rid of any tmp files in RPM land, ie. '/usr/src/redhat/BUILD/...'
%__rm -rf $RPM_BUILD_DIR/%{name}-%{ver}
%__rm -rf $RPM_BUILD_ROOT



#---------------------------------------------------------------------
# Pre-un(install) section
#---------------------------------------------------------------------
%preun
%__rm -f %{prefix}/*.pyc



#---------------------------------------------------------------------
# Post-un(install) section
#---------------------------------------------------------------------
%postun



#---------------------------------------------------------------------
# Files section
#
#  List all files that will make it to the target machine here.  Note,
#  that listing the entire dir, gets all the files withing.  The %doc
#  files are treated special and copied into the system doc area (eg. share).
#---------------------------------------------------------------------

%files
%defattr(-,root,root)
%doc INSTALL KNOWN_BUGS README CHANGELOG
%{prefix}


%files ckillnode
%defattr(-,root,root)
%{prefix}/ckillnode


%files profiled
%defattr(-,root,root)
%{profiled}


#---------------------------------------------------------------------
# ChangeLog section
#---------------------------------------------------------------------
%changelog
* Wed Dec 04 2002  01:36:38AM    Thomas Naughton  <naughtont@ornl.gov>
- (3.1-3) Overhaul the RPM spec stuffo.  
  Consolidate 'c3, -profiled, -ckillnode' RPMs into a single SPEC file.
- Fix path for ckillnode, change to also be '/opt/c3-3'.
- Additionally, this is using the newer version of 'ckillnode' that was
  in the 3.1.1 tarball.

* Wed May 29 2002  11:15:18AM    Thomas Naughton  <naughtont@ornl.gov>
- (3.1-2) Changed the pre-reqs to be '/usr/bin/python2' to work better 
  w/ OSCAR and non-RedHat based systems that don't use the "Python" (1.x) 
  and "Python2" (2.x) RPM naming for co-existence.

* Thu May 16 2002  21:00:32PM    modified by:  tjn <naughtont@ornl.gov>
- Upgraded to c3-3.1                  (BRANCH-TAG=branch-c3-3-1, rel=1)
- LAM/MPI rocks (http://www.lam-mpi.org/)  THANKS JEFF!  :)
  Jeff Squyres fixed things up to use BuildRoot, which fixed lots! 
- Added the %preun to get rid of the *.pyc files (pre-compiled bytecode).
- Moved the 'profile.d' stuff to a seperate RPM "c3-profiled".  This 
  cleans things up here and also allows for use of switcher only w/o 
  the profile.d/ scripts (partially OSCAR related).
- Fixed the '-U' & '-e' errors for similarly named files.
- Cleaning things up, everything stays in '/opt/c3-3' (ie. %{prefix} )
  including the Man pages, Brian moved mans to the more std man/manN/ form.
- Removed the postun stuff that breaks stuff!  Bad tjn...
- Misc clean ups and added *many* more comments.
- Generate these as noarch.
- Generate these w/ Python2 deps

* Tue May 14 2002  10:25:23AM    modified by:  tjn <naughtont@ornl.gov>
- Adding this to a CVS repository...not changing the rel# (2.7.2-4)

* Mon Apr 01 2002  10:21:34AM    modified by:  tjn <naughtont@ornl.gov>
- Using RPM provided macros for cat, cp & rm until I upgrade the entire RPM
  see also: /usr/lib/rpm/macros
- Also removed echo to STDOUT, assume users can edit c3.conf and created
  a 'c3-ckillnode-2.7.2-X' RPM for use on client nodes.
- On a related note, I created a c3-ckillnode RPM for use on clients.

* Thu Dec 13 2001  09:35:50AM    modified by:  tjn <naughtont@ornl.org>
- Changed the c3.conf stuff to only create a new if one doesn't exist.

* Wed Dec 12 2001  11:18:02AM    modified by:  tjn <naughtont@ornl.org>
- removed some of the extra stuff printed upon 'rpm -ivh' & added 'Requires:'.

* Tue Dec 11 2001  13:28:32PM    modified by:  tjn <naughtont@ornl.org>
- fixed problem related to only c3.1 man page being install.

* Fri Aug 24 2001  10:25:55AM    modified by:  tjn <naughtont@ornl.gov>
- changed the name for the Source1 & Source2 to be specific to version

* Tue Jul 31 2001  14:06:02PM    modified by:  tjn <naughtont@ornl.gov>
- check for exiting defs on the /etc/profile.d/  files
  (this also required me to change the echo of the contents to actual a copy!)

* Tue Jun 19 2001 Thomas Naughton <naughtontiii@ornl.gov>
- Creation of initial c3-2.7.2 rpm
