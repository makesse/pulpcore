# Copyright (c) 2010 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0


%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}


# ---- Pulp Platform -----------------------------------------------------------

Name: pulp
Version: 0.0.295
Release: 1%{?dist}
Summary: An application for managing software content
Group: Development/Languages
License: GPLv2
URL: https://fedorahosted.org/pulp/
Source0: https://fedorahosted.org/releases/p/u/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-nose
BuildRequires: rpm-python

%description
Pulp provides replication, access, and accounting for software repositories.

%prep
%setup -q

%build
pushd src
%{__python} setup.py build
popd

%install
rm -rf %{buildroot}
pushd src
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

# Directories
mkdir -p /srv
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/admin
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/admin/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/consumer
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/consumer/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/agent
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/agent/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/pki/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/pki/%{name}/consumer
mkdir -p %{buildroot}/%{_sysconfdir}/gofer/plugins
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
mkdir -p %{buildroot}/%{_usr}/lib/%{name}
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/plugins
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/plugins/distributors
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/plugins/importers
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/plugins/profilers
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/plugins/types
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/admin
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/admin/extensions
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/consumer
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/consumer/extensions
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/agent
mkdir -p %{buildroot}/%{_usr}/lib/%{name}/agent/handlers
mkdir -p %{buildroot}/%{_var}/lib/%{name}
mkdir -p %{buildroot}/%{_var}/lib/%{name}/uploads
mkdir -p %{buildroot}/%{_var}/lib/%{name}/repos
mkdir -p %{buildroot}/%{_var}/lib/%{name}/repos
mkdir -p %{buildroot}/%{_var}/log/%{name}
mkdir -p %{buildroot}/%{_libdir}/gofer/plugins
mkdir -p %{buildroot}/%{_bindir}

# Configuration
cp -R etc/pulp/* %{buildroot}/%{_sysconfdir}/%{name}

# Apache Configuration
cp etc/httpd/conf.d/pulp.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/

# Pulp Web Services
cp -R srv %{buildroot}

# PKI
cp etc/pki/pulp/* %{buildroot}/%{_sysconfdir}/pki/%{name}

# Agent
cp etc/gofer/plugins/pulp.conf %{buildroot}/%{_sysconfdir}/gofer/plugins
cp -R src/pulp/agent/gofer/pulp.py %{buildroot}/%{_libdir}/gofer/plugins

# Tools
cp bin/* %{buildroot}/%{_bindir}

# Init (init.d)
cp etc/rc.d/init.d/* %{buildroot}/%{_sysconfdir}/rc.d/init.d/

# Remove egg info
rm -rf %{buildroot}/%{python_sitelib}/*.egg-info

%clean
rm -rf %{buildroot}


# ---- Server ------------------------------------------------------------------

%package server
Summary: The pulp platform server
Requires: %{name}-common = %{version}
Requires: pymongo >= 1.9
Requires: python-setuptools
Requires: python-webpy
Requires: python-simplejson >= 2.0.9
Requires: python-oauth2 >= 1.5.170-2.pulp
Requires: python-httplib2
Requires: python-isodate >= 0.4.4-3.pulp
Requires: python-BeautifulSoup
Requires: grinder >= 0.1.3-1
Requires: httpd
Requires: mod_ssl
Requires: openssl
Requires: python-ldap
Requires: python-gofer >= 0.69
Requires: crontabs
Requires: acl
Requires: mod_wsgi >= 3.3-3.pulp
Requires: mongodb
Requires: mongodb-server
Requires: qpid-cpp-server
# RHEL5
%if 0%{?rhel} == 5
Requires: m2crypto
Requires: python-uuid
Requires: python-ssl
Requires: python-ctypes
Requires: python-hashlib
Requires: createrepo = 0.9.8-3
Requires: mkisofs
# RHEL6 & FEDORA
%else
Requires: m2crypto >= 0.21.1.pulp-7
Requires: genisoimage
%endif
# RHEL6 ONLY
%if 0%{?rhel} == 6
Requires: python-ctypes
Requires: python-hashlib
Requires: nss >= 3.12.9
Requires: curl => 7.19.7
%endif

%description server
Pulp provides replication, access, and accounting for software repositories.

%files server
%defattr(-,root,root,-)
%{python_sitelib}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/server.conf
%config(noreplace) %{_sysconfdir}/%{name}/logging/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/pki/%{name}
%{_sysconfdir}/rc.d/init.d/pulp-server
%{_bindir}/pulp-migrate
%defattr(-,apache,apache,-)
/srv/%{name}/webservices.wsgi
%{_var}/lib/%{name}/
%doc


# ---- Common ------------------------------------------------------------------

%package -n python-pulp-common
Summary: Pulp common python packages
Group: Development/Languages

%description -n python-pulp-common
A collection of components that are common between the pulp server and client.

%files -n python-pulp-common
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/__init__.*
%{python_sitelib}/%{name}/common/
%defattr(-,apache,apache,-)
%doc


# ---- Client Bindings ---------------------------------------------------------

%package -n python-pulp-bindings
Summary: Pulp REST bindings for python
Group: Development/Languages

%description -n python-pulp-bindings
The Pulp REST API bindings for python.

%files -n python-pulp-bindings
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/bindings/
%doc


# ---- Client Extension Framework -----------------------------------------------------

%package -n python-pulp-client-lib
Summary: Pulp client extensions framework
Group: Development/Languages
Requires: python-%{name}-common = %{version}
Requires: python-okaara >= 1.0.12

%description -n python-pulp-client-lib
A framework for loading Pulp client extensions.

%files -n python-pulp-client-lib
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/client/
%doc


# ---- Agent Handler Framework -------------------------------------------------

%package -n python-pulp-agent-lib
Summary: Pulp agent handler framework
Group: Development/Languages
Requires: python-%{name}-common = %{version}

%description -n python-pulp-agent-lib
A framework for loading agent handlers that provide support
for content, bind and system specific operations.

%files -n python-pulp-agent-lib
%defattr(-,root,root,-)
%{python_sitelib}/%{name}/agent/*.py
%{python_sitelib}/%{name}/agent/lib/
%dir %{_sysconfdir}/%{name}/agent
%dir %{_sysconfdir}/%{name}/agent/conf.d
%dir %{_usr}/lib/%{name}/agent
%doc


# ---- Admin Client (CLI) ------------------------------------------------------

%package admin-client
Summary: Admin tool to administer the pulp server
Requires: python-%{name}-common = %{version}
Requires: python-%{name}-bindings = %{version}
Requires: python-%{name}-client-lib = %{version}
Obsoletes: pulp-client <= 0.218

%description admin-client
A tool used to administer the pulp server, such as repo creation and
synching, and to kick off remote actions on consumers.

%files admin-client
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/admin
%dir %{_sysconfdir}/%{name}/admin/conf.d
%dir %{_usr}/lib/%{name}/admin/extensions/
%config(noreplace) %{_sysconfdir}/%{name}/admin/admin.conf
%{_bindir}/%{name}-admin
%doc


# ---- Consumer Client (CLI) ---------------------------------------------------

%package consumer-client
Summary: Consumer tool to administer the pulp consumer.
Requires: python-%{name}-common = %{version}
Requires: python-%{name}-bindings = %{version}
Requires: python-%{name}-client-lib = %{version}

%description consumer-client
A tool used to administer a pulp consumer.

%files consumer-client
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/consumer
%dir %{_sysconfdir}/%{name}/consumer/conf.d
%dir %{_usr}/lib/%{name}/consumer/extensions/
%config(noreplace) %{_sysconfdir}/%{name}/consumer/consumer.conf
%{_bindir}/%{name}-consumer
%doc


# ---- Agent -------------------------------------------------------------------

%package agent
Summary: The Pulp agent
Requires: python-%{name}-bindings = %{version}
Requires: python-%{name}-agent-lib = %{version}

%description agent
The pulp agent, used to provide remote command & control and
scheduled actions such as reporting installed content profiles
on a defined interval.

%files agent
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/agent/agent.conf
%{_sysconfdir}/gofer/plugins/pulp.conf
%{_libdir}/gofer/plugins/pulp.*
%doc



%changelog
* Fri Jun 08 2012 Jeff Ortel <jortel@redhat.com> 0.0.295-1
- bump to gofer 0.69. (jortel@redhat.com)
- Add support for linking rpms units referenced with in a errata
  (pkilambi@redhat.com)
- Automatic commit of package [gofer] minor release [0.69-1].
  (jortel@redhat.com)
- Copying comps_util.py from pulp.server to pulp.yum_plugin so YumImporter may
  use this (jmatthews@redhat.com)
- YumImporter: test data for a simple repo with no comps (jmatthews@redhat.com)
- Added a warning in pulp-dev for when a dir exists but we expected it to be a
  symlink (jmatthews@redhat.com)
- Added unit copy extension to the RPM (jason.dobies@redhat.com)
- YumImporter/YumDistributor update unit tests to configure logger and redirect
  output from console to log file (jmatthews@redhat.com)
* Mon Jun 04 2012 Jeff Ortel <jortel@redhat.com> 0.0.294-1
- updated copyright information (jason.connor@gmail.com)
- Hide the auth ca cert, just show if one is present (jason.dobies@redhat.com)
- Changed triggers for consistency across the UI (jason.dobies@redhat.com)
- consumer cli extension for bind, unbind and minor re-structuring of
  consumerid function (skarmark@redhat.com)
- Changing order of consumer history result and removing unwanted _id
  (skarmark@redhat.com)
- removing consumer id validation from consumer history querying to allow
  querying for unregistered consumer as well (skarmark@redhat.com)
- Fixing unbind client extension error (skarmark@redhat.com)
- Update .gitignore to ignore test coverage output files (jmatthews@redhat.com)
- YumImporter:  Change 'fileName' to 'filename' for drpm (jmatthews@redhat.com)
- added deprecated notice to doctring (jason.connor@gmail.com)
- Fixed async response handling (jason.dobies@redhat.com)
- YumDistributor:  Added check to see if createrepo pid is running before
  canceling (jmatthews@redhat.com)
- YumDistributor: continue to debug errors from running with jenkins
  (jmatthews@redhat.com)
- Python 2.4 compatibility change for determining if Iterable
  (jmatthews@redhat.com)
- YumDistributor, debugging intermittent test failure when run from jenkins
  (jmatthews@redhat.com)
- YumImporter:  removed filename from srpm unit key (jmatthews@redhat.com)
- Fix for rhel5 unit tests, collections.Iterable doesn't exist
  (jmatthews@redhat.com)
- Fixed to use correct link call (jason.dobies@redhat.com)
- Revert "idempotent misspelled" (jason.connor@gmail.com)
- Revert "removed not_implemented() controllers" (jason.connor@gmail.com)
- Revert "removed unnecessary quotes around controller class names"
  (jason.connor@gmail.com)
- Revert "added _href fields to resources in repositories collection"
  (jason.connor@gmail.com)
- Revert "added _href field to new created repository" (jason.connor@gmail.com)
- Revert "added _href for repo resources" (jason.connor@gmail.com)
- added _href for repo resources (jason.connor@gmail.com)
- added _href field to new created repository (jason.connor@gmail.com)
- added _href fields to resources in repositories collection
  (jason.connor@gmail.com)
- changed sync overrides to a keyword argument (jason.connor@gmail.com)
- removed unnecessary quotes around controller class names
  (jason.connor@gmail.com)
- removed not_implemented() controllers (jason.connor@gmail.com)
- idempotent misspelled (jason.connor@gmail.com)
- changed task lookups to use new task_queue factory instead of accessing it
  via the coordinator (jason.connor@gmail.com)
- 827221 - Added individual resource GET methods and hrefs to resources
  (jason.dobies@redhat.com)
- 827220 - Removed old error_handler directives (jason.dobies@redhat.com)
- YumDistributor:  cancel_publish implementation and unit tests
  (jmatthews@redhat.com)
- Test data for simulating a long running createrepo process
  (jmatthews@redhat.com)
- added cleanup of mocked-out factory functions (jason.connor@gmail.com)
- fixed consumer controller entry (jason.connor@gmail.com)
- Delete the upload request if its rejected (jason.dobies@redhat.com)
- fix relativepath of the rpm during upload (pkilambi@redhat.com)
- Updated user guide for 1.1 (jason.dobies@redhat.com)
- utilized new factory access to move complete lifecycle callback out of
  scheduler class to a stand-alone function (jason.connor@gmail.com)
- changed tests to reflect changes in scheduler (jason.connor@gmail.com)
- remoced collection instance from scheduler as well (jason.connor@gmail.com)
- while I was at it I eliminated the task resource collection as state as well
  and instead use the get_collection factory method that is a part of every
  Model class (jason.connor@gmail.com)
- changed unit tests to reflect changes in coordinator (jason.connor@gmail.com)
- changed initialization of scheduler and coordinator to reflect changes in
  constructors (jason.connor@gmail.com)
- removed task queue as internal state and instead access it through the
  dispatch factory (jason.connor@gmail.com)
- added task queue factory function and updated the return types of the factory
  functions while I was at it (jason.connor@gmail.com)
- updated unittests to reflect changes in scheduler (jason.connor@gmail.com)
- removed the coordinator as state and instead use the factory to access it
  (jason.connor@gmail.com)
- removed unused imports (jason.connor@gmail.com)
- removed unused import (jason.connor@gmail.com)
- moved all imports into initialization methods to avoid circulary imports this
  will allow the different modules of the dispatch package to access each other
  via the factory in order keep the amount of state (read: references to each
  other) to a minimum (jason.connor@gmail.com)
- added super setup/teardown of old mocked async to keep clean happy
  (jason.connor@gmail.com)
- cleaned up imports and future proofed json_util import
  (jason.connor@gmail.com)
- moved exception handling into loop for better reporting
  (jason.connor@gmail.com)
- change mkdir to makedirs for better parental supervision
  (jason.connor@gmail.com)
- Added handling for async responses when importing units
  (jason.dobies@redhat.com)
- Added UG for repo tasks (jason.dobies@redhat.com)
- Added UG section for describing postponed and rejected tasks
  (jason.dobies@redhat.com)
- Fixed incongruences in the sync user guide (jason.dobies@redhat.com)
- Added user guide entry for repo publish (jason.dobies@redhat.com)
- User guide for package upload (jason.dobies@redhat.com)
- remove filename from rpm unit key (pkilambi@redhat.com)
- Cleanup for the consumer packages section of the user guide
  (jason.dobies@redhat.com)
- Corrected handling/display for operations postponed by the coordinator
  (jason.dobies@redhat.com)
- Refactored out bool conversion so it can be used directly
  (jason.dobies@redhat.com)
- Added publish schedule support to the RPM CLI extensions
  (jason.dobies@redhat.com)
- Added direct publish support (jason.dobies@redhat.com)
- Added enabled/disabled support for all RPM extensions
  (jason.dobies@redhat.com)

* Fri May 25 2012 Jeff Ortel <jortel@redhat.com> 0.0.293-1
- Fix .spec for moving agent handlers. (jortel@redhat.com)
- Add comments with Config usage and examples. (jortel@redhat.com)

* Fri May 25 2012 Jeff Ortel <jortel@redhat.com> 0.0.292-1
- Better section filtering in gc_config. (jortel@redhat.com)
- YumImporter:  Added cancel sync (jmatthews@redhat.com)
- Implement upload_unit in yum importer (pkilambi@redhat.com)
- Final code clean up and tweaks (jason.dobies@redhat.com)
- Removed delete call from import, it doesn't belong there
  (jason.dobies@redhat.com)
- Don't return the report, it will be stuffed into history instead
  (jason.dobies@redhat.com)
- Added upload extension to the RPM (jason.dobies@redhat.com)
- Added filename to unit key temporarily (jason.dobies@redhat.com)
- Wrong call to import the unit (jason.dobies@redhat.com)
- Default the relative URL to repo ID for feedless repos
  (jason.dobies@redhat.com)
- Turned on the import step (jason.dobies@redhat.com)
- admin consumer bind and unbind extension (skarmark@redhat.com)
- Fix agent unregistered(), delete of consumer cert. (jortel@redhat.com)
- Rename (distributor) handler role to: (bind). (jortel@redhat.com)
- Move GC agent handlers to: /etc/pulp/agent & /usr/lib/pulp/agent.
  (jortel@redhat.com)
- Fix epydoc typos. (jortel@redhat.com)
- Initial working version of the upload CLI (jason.dobies@redhat.com)
- Remove default {} from report signatures; fix epydoc. (jortel@redhat.com)
- Add linux system handler to git. (jortel@redhat.com)
- Add a ton of missing GC packages and tests. (jortel@redhat.com)
- Fixing syntax error at the end of params in the api doc (skarmark@redhat.com)
- GC agent: add (system) role and refactor reboot(). (jortel@redhat.com)
- Fix title for consistency (jason.dobies@redhat.com)
- Another minor rendering fix for consumer history api doc (3rd time's the
  charm) (skarmark@redhat.com)
- Minor rendering fix for consumer history api doc (skarmark@redhat.com)
- updated docstring (jason.connor@gmail.com)
- Fixing title of consumer history api doc (skarmark@redhat.com)
- In GC agent, add initial mapping for package group installs.
  (jortel@redhat.com)
- Update epydocs. (jortel@redhat.com)
- Refactor Handler interface for clarity.  Fix bind handler using
  ConsumerConfig. (jortel@redhat.com)

* Thu May 24 2012 Jeff Ortel <jortel@redhat.com> 0.0.291-1
- yum_importer proxy fix to force config values to be in ascii
  (jmatthews@redhat.com)
- minor fix in consumer history retrieval (skarmark@redhat.com)
- converting consumer history query call to GET from POST (skarmark@redhat.com)
- added skeleton Profiler loading support (jason.connor@gmail.com)
- added skeleton Profiler class (jason.connor@gmail.com)
- Added sample response for retrieving a single consumer api
  (skarmark@redhat.com)
- Removing importer retrieval doc pasted by mistake in consumer docs
  (skarmark@redhat.com)
- For consistency, use repo-id in all cases (jason.dobies@redhat.com)
- updating display_name argument coming from client extension to display-name
  and updating argument to MissingResource exception (skarmark@redhat.com)
- removing (optional) from cli arguments (skarmark@redhat.com)
- Add the repo to the upload_unit API (jason.dobies@redhat.com)
- Fixing minor errors in consumer extensions and correcting rendering methods
  for failure cases (skarmark@redhat.com)
- Remove unused files from gc_client/. (jortel@redhat.com)
- Factor out references to: credentials/config in: gc_client/consumer and
  gc_client/lib. (jortel@redhat.com)
- Added call report example (jason.dobies@redhat.com)
- Added client upload manager and unit tests (jason.dobies@redhat.com)
- added tags to delete operations (jason.connor@gmail.com)
- changed field names and provided sample request (jason.connor@gmail.com)
- remove unicode indicators from sample response (jason.connor@gmail.com)
- changed content_type to content_type_id and content_id to unit_id for
  consistency across apis (jason.connor@gmail.com)
- moved key checking to manager (jason.connor@gmail.com)
- updated copyright (jason.connor@gmail.com)
- changed new schedules to always have their "first run" in the future
  (jason.connor@gmail.com)
- moved schedule validation out of db model (jason.connor@gmail.com)
- much more comprehensive parameter validation in for additions and updates
  (jason.connor@gmail.com)
- added unsupported value exception class (jason.connor@gmail.com)
- Using consumer config loaded by launcher instead of using hardcoded config in
  ConsumerBundle and ConsumerConfig classes (skarmark@redhat.com)
- move heartbeat and registration detection to GC agent (jortel@redhat.com)
- Add rpm admin consumer extension unit test. (jortel@redhat.com)
- Add package install UG pages. (jortel@redhat.com)
- combining all consumer history record and query invalid values together to
  raise an exception with a list of all invalid values instead of separate
  exceptions for each invalid value (skarmark@redhat.com)
- Changing consumer history query extension arguments from '_' to '-' according
  to v2 coding standard; updating input to MissingResource exceptions
  (skarmark@redhat.com)
- support veriety of input on construction. (jortel@redhat.com)
- Fixed incorrect lookup for display-name in update (jason.dobies@redhat.com)
- adding new fields to publish report (pkilambi@redhat.com)
- Display remaining runs for a schedule (jason.dobies@redhat.com)
- Added middleware support for arg parsing exception (jason.dobies@redhat.com)
- Add strict vs. non-strict flag on config graph. (jortel@redhat.com)
- Add dict-like configuration object and updated validation.
  (jortel@redhat.com)
- Added repo sync schedule user guide documentation (jason.dobies@redhat.com)
- Load content handlers on gofer plugin loading. (jortel@redhat.com)
- validation placeholders (jason.connor@gmail.com)
- couple of tweaks (jason.connor@gmail.com)
- orphan rest api docs (jason.connor@gmail.com)
- added schedule validation for updates (jason.connor@gmail.com)
- moved scheduler constants back into scheduler module and absolutely no one
  else uses them... (jason.connor@gmail.com)
- added missing coordinator reponses for updated and delete sync/publish
  schedules (jason.connor@gmail.com)
- bz 798281 add status call to service pulp-cds (whayutin@redhat.com)
- 821041 - packagegroup install of custom groups seems to be failing
  (jmatthews@redhat.com)
- Flushed out date/time conventions in the user guide (jason.dobies@redhat.com)
- Added cleaner message when no schedules are present (jason.dobies@redhat.com)
- mod auth token prototype (pkilambi@redhat.com)
- Added generic schedule commands and repo sync schedule usage of them
  (jason.dobies@redhat.com)
- re-captured isodate parsing and raising InvalidValue error instead for proper
  handling in the middleware (jason.connor@gmail.com)
- re-introduced v1 task queue feature of caching completed tasks
  (jason.connor@gmail.com)
- added orphan manager unittests (jason.connor@gmail.com)

* Fri May 18 2012 Jeff Ortel <jortel@redhat.com> 0.0.290-1
- Fix broken GC package install CLI. (jortel@redhat.com)
- Utilities for handling CLI argument conventions (jason.dobies@redhat.com)
- removing checks to support no pulishing (pkilambi@redhat.com)
- GC bind: hook up handler and repolib. (jortel@redhat.com)
- Upgraded okaara to 1.0.18 (jason.dobies@redhat.com)
- Updated base command class to use okaara's option description prefixing
  (jason.dobies@redhat.com)
- temp disablement of task archival task until race condition can be resolved
  (jason.connor@gmail.com)
- Disable all tasks view by default (enabled in .conf)
  (jason.dobies@redhat.com)
- orphan manager unit tests (jason.connor@gmail.com)
- fixed missing .items() while iterating over dictionary
  (jason.connor@gmail.com)
- removed unused options argument to collection constructor which just went
  away in pymongo 2.2 anyway (jason.connor@gmail.com)
- place running tasks before waiting tasks when returning all tasks to maintain
  a closer representation of the enqueue time total ordering on the task set
  (jason.connor@gmail.com)
- added archive to all delete requests (jason.connor@gmail.com)
- added auth_required decorators to all orphan controllers
  (jason.connor@gmail.com)
- added mac special dir to ignore (jason.connor@gmail.com)
- moved archival test to task queue tests (jason.connor@gmail.com)
- removed archival from task tests (jason.connor@gmail.com)
- moved call archival from task into task queue to prevent race condition in
  task queries (jason.connor@gmail.com)
- converted to _id for unit ids (jason.connor@gmail.com)
- initial implementation of delete orphans action (jason.connor@gmail.com)
- utilizing changed field names (jason.connor@gmail.com)
- changed fields to more managable content_type and content_id
  (jason.connor@gmail.com)
- initial implementation of orphan collections and resources
  (jason.connor@gmail.com)
- added get_orphan method (jason.connor@gmail.com)
- added orphan manager to factory (jason.connor@gmail.com)
- added comment (jason.connor@gmail.com)
- Add yum repo (bind) handler; more bind plumbing. (jortel@redhat.com)
- Update mock distributor bind payload. (jortel@redhat.com)
- Updated bind (GET) to include distributor payload. (jortel@redhat.com)
- updating payload info (pkilambi@redhat.com)
- Last docs tweak for today, I swear (jason.dobies@redhat.com)
- Added background functionality to repo sync run (jason.dobies@redhat.com)
- fix for updating the state when a distribution symlink step fails
  (pkilambi@redhat.com)
- Consumer history manager layer, controller and adminclient extension
  (skarmark@redhat.com)
- Added a status call to the repo to see if it is synccing
  (jason.dobies@redhat.com)
- Added ability to resume tracking an in progress sync and refactored extension
  to separate sync running and scheduling commands (jason.dobies@redhat.com)
- Fixed tags lookup from query parameters (jason.dobies@redhat.com)
- Tasks extension unit tests and code cleanup (jason.dobies@redhat.com)
- Update GC content handler framework to support bind(). (jortel@redhat.com)
- Implementation of task list, details, and delete commands
  (jason.dobies@redhat.com)
- Flushed out client-side task API (jason.dobies@redhat.com)
- Refactored response object structure in client API (jason.dobies@redhat.com)
- Updated 404 exception handling to handle new data dict format
  (jason.dobies@redhat.com)
- moved log file to get full path into message (jason.connor@gmail.com)
- implementation of orphan manager (jason.connor@gmail.com)
- fixed some spelling errors (jason.connor@gmail.com)
- Move GC agent lib under (lib); Add pulp bindings to agent.
  (jortel@redhat.com)
- Update RPM handler and gofer plugin for GC agent move to gc_client.
  (jortel@redhat.com)
- Update pulp.spec for GC agent moved to gc_client. (jortel@redhat.com)
- Move GC agent under gc_client. (jortel@redhat.com)
- Add bindings query by consumer/repo in API; Add binding query to GC client
  API. (jortel@redhat.com)
- adding host_urls and renaming few keys in payload (pkilambi@redhat.com)
- minor changes to payload structure (pkilambi@redhat.com)
- implement the consumer payload in distributor (pkilambi@redhat.com)
- Fix GC agent & rpm handler reboot logic; support update ALL.
  (jortel@redhat.com)
- Ported v1 protected repositories into the v2 documentation
  (jason.dobies@redhat.com)
* Fri May 11 2012 Jeff Ortel <jortel@redhat.com> 0.0.289-1
- Updated to correct importer/distributor config values
  (jason.dobies@redhat.com)
- Corrected _ to - in the user guide (jason.dobies@redhat.com)
- Unit tests for unit copy (jason.dobies@redhat.com)
- Added gt, gte, lt, lte, after, and before functionality to unit copy
  (jason.dobies@redhat.com)
- Added unit copy API to client bindings (jason.dobies@redhat.com)
- fix test districutor to use mock (pkilambi@redhat.com)
- fix tests to use a mock object (pkilambi@redhat.com)
- Initial implementation of the unit copy extension (jason.dobies@redhat.com)
- Protected Repos: - support for writing consumer cert to specific location
  based on repo_auth.conf - update protected_repo_listings file - implement
  distributor_remove hook to clean up on repo delete (pkilambi@redhat.com)
- Renamed underscore CLI flags to use the hyphens convention
  (jason.dobies@redhat.com)
- added cross references for asynchronous call reports and the task dispatch
  api (jason.connor@gmail.com)
- initial placeholder for orphan manager (jason.connor@gmail.com)
- added dispatch to index (jason.connor@gmail.com)
- start of dispatch apis (jason.connor@gmail.com)

* Tue May 08 2012 Jeff Ortel <jortel@redhat.com> 0.0.288-1
- 819589 - casting all kwarg keys to str (jason.connor@gmail.com)
- removed cast to timedelta from isodate.Duration (jason.connor@gmail.com)
- Consumer 'rpm' extension replaces generic 'content' extension when installed.
  (jortel@redhat.com)
- some json v python corrections and start of new section on iso8601
  (jason.connor@gmail.com)
- Add --no-commit to GC content extension. (jortel@redhat.com)
- Changed handling of http/https flags so they are only defaulted in create
  (jason.dobies@redhat.com)
- changed _do_request to allow multiple polls to be sent to task url
  (jason.connor@gmail.com)
- changed aynchronous support to only set success or failure if the task is
  actually running changed asynchronous support to guaruntee only 1 call into
  coordinator changed asynchronous support to allow multiple calls into
  controllers per unittest so long as set_success or set_failure is called
  before each asynchronous controller is called (jason.connor@gmail.com)
- Unit metadata is optional for unit import (jason.dobies@redhat.com)
- Create the necessary directories for content uploads
  (jason.dobies@redhat.com)
- convert the ssl certs queried from mongo to utf8 before passing to m2crypto
  (pkilambi@redhat.com)
- GC agent; enable authorization. (jortel@redhat.com)
- CallRequest(asynchronous=True); Simulate agent reply in GC consumer
  controller unit test. (jortel@redhat.com)
- make --importkeys a flag. (jortel@redhat.com)
- removed generic scheduled tag and added schedule resource tag
  (jason.connor@gmail.com)

* Thu May 03 2012 Jeff Ortel <jortel@redhat.com> 0.0.287-2
- move gc_client to client-lib. (jortel@redhat.com)

* Thu May 03 2012 Jeff Ortel <jortel@redhat.com> 0.0.287-1
- Support -n alias for GC content install CLI. (jortel@redhat.com)
- Add support for str|list|tuple tracebacks. (jortel@redhat.com)
- Enhanced gc & rpm content install CLI. (jortel@redhat.com)
- Better error handling in generic content install CLI. (jortel@redhat.com)
- Refactor admin cli to split generic content unit vs. rpm install.
  (jortel@redhat.com)
- YumImporter:  Fix for rhel5 issue with itertools.chain.from_iterable
  (jmatthews@redhat.com)
- Added REST APIs for content upload (jason.dobies@redhat.com)
- publish added to index (jason.connor@gmail.com)
- publish api documentation (jason.connor@gmail.com)
- corrected a number of typos (jason.connor@gmail.com)
- fixes to sync doc (jconnor@redhat.com)
- no longer recording duplicate reasons for postponed and rejected
  (jconnor@redhat.com)
- updated tags to use new resource_tag generation (jconnor@redhat.com)
- replaced spaces in resource types with underscores (jconnor@redhat.com)
- removed leading underscores for scheduled call object fields
  (jconnor@redhat.com)
- removed superfluous part of child path for sync/publish schedules
  (jconnor@redhat.com)
- fixed typo in docstring (jconnor@redhat.com)
- Render content install,update,uninstall results. (jortel@redhat.com)
- YumDistributor:  Update to remove http/https link if no longer set to True in
  config (jmatthews@redhat.com)
- convert the cert strings to utf-8 before passing to grinder; also fixed
  default sslverify value if not specified (pkilambi@redhat.com)
- Differentiate association owner for uploaded v. syncced units
  (jason.dobies@redhat.com)
- YumImporter:  First pass at handling sync of a protected repo
  (jmatthews@redhat.com)
- Added distribution support for repo units display (jason.dobies@redhat.com)
- Docs cleanup (jason.dobies@redhat.com)
- YumDistributor:  Fix for unicode relative_url validation
  (jmatthews@redhat.com)
- forgot to use $set, so I was completely overwriting the fields instead of
  just setting a sub-set of them (jason.connor@gmail.com)
- fixed too short underline (jason.connor@gmail.com)
- repo sync documentation (jason.connor@gmail.com)
- fixed up scheduled call serialization (jason.connor@gmail.com)
- added sync to index (jason.connor@gmail.com)
- changed all scheduled sync and publish controllers to use new serialization
  (jason.connor@gmail.com)
- added specific serialization for scheduled sync and publish
  (jason.connor@gmail.com)
- fixed comment typo (jason.connor@gmail.com)
- added more fields to call report (jason.connor@gmail.com)
- removed assumptions and generalized scheduled call object
  (jason.connor@gmail.com)
- added iso8601 interval to gloassary (jason.connor@gmail.com)
- added call report to glossary (jason.connor@gmail.com)
- Added publish progress support to sync status. (jason.dobies@redhat.com)
- Adding multiple content unit install support (skarmark@redhat.com)
- Ensure report contains 'details' on exceptoin as well. (jortel@redhat.com)
- Refactored out the progress report rendering (jason.dobies@redhat.com)
- client extension for a consumer content unit install (skarmark@redhat.com)
- Docs cleanup (jason.dobies@redhat.com)
- including http/https publish progress info in report (pkilambi@redhat.com)
- Implementation of v2 storage of uploaded files (jason.dobies@redhat.com)
- YumDistributor:  Implementation of 'http' publishing option
  (jmatthews@redhat.com)
- Added 'keys()' method to return a set of all keys available from the
  underlying dicts (jmatthews@redhat.com)
- YumImporter:  Made feed_url optional and ensure we invoke progress report for
  NOT_STARTED as first step (jmatthews@redhat.com)
- Client bindings for consumer content unit install (skarmark@redhat.com)
- updating doc strings to  include progress callback description
  (pkilambi@redhat.com)
- default progress arg to None (pkilambi@redhat.com)
- first pass at changes to support Yum Distributor publish progress reporting
  (pkilambi@redhat.com)
- Base unit addition/linking conduit (jason.dobies@redhat.com)
- Refactored out base unit add conduit support to better scope the upload
  conduit (jason.dobies@redhat.com)
- Adding consumer credential support from v1 to v2 (skarmark@redhat.com)
- Added ability to store consumer cert bundle for v2 consumers
  (skarmark@redhat.com)
- schedule creation using configured create_weight (jconnor@redhat.com)
- converted all tags to use new generic tags functions (jconnor@redhat.com)
- adding tag generating functions to common (jconnor@redhat.com)
- changed scheduled sync/publish to use controller (jason.connor@gmail.com)
- re-implementation of sync and publish schedule controllers using schedule
  manager (jason.connor@gmail.com)
- added schedule_manager to managers factory (jason.connor@gmail.com)
- fixed override config keyword argument publish schedule update fixed schedule
  update keyword arguments (jason.connor@gmail.com)
- added return of schedule_id to publish create (jason.connor@gmail.com)
- fixed schedule update keyword arguments fixed repo importer manager
  constructor arguments (jason.connor@gmail.com)
- converting _id to string in schedule report (jason.connor@gmail.com)
- removed _id that needed more processing, added failure_threshold
  (jason.connor@gmail.com)
- fixed check for schedule (jason.connor@gmail.com)
- added required flag for dict validation (jconnor@redhat.com)
- add/remove/list publish schedule functionality (jconnor@redhat.com)
- add/remove/list sync schedule functionality (jconnor@redhat.com)
- finished implementation of scheduled sync/publish cud operations
  (jconnor@redhat.com)
- removed old import (jconnor@redhat.com)
- schedule managers skeletons (jconnor@redhat.com)
- sync schedule method place holders (jconnor@redhat.com)
- sync schedule collection list (jconnor@redhat.com)
- Add TODO: in consumer controller. (jortel@redhat.com)
- Initial add of repo sync 'schedule' subsection. (jortel@redhat.com)
- Added importer API for upload and manager to call into it
  (jason.dobies@redhat.com)
- Updated epydocs. (jortel@redhat.com)
- YumImporter:  implementation for import_units (jmatthews@redhat.com)
- YumDistributor:  Reduce logging output (jmatthews@redhat.com)
- Correct API docs. (jortel@redhat.com)