.. contents:: Table of Contents:


About
-----

Slpkg is a software package manager that installs, updates and removes packages on `Slackware <http://www.slackware.com/>`_-based systems.
It automatically calculates dependencies and figures out what things need to happen to install packages. 
Slpkg makes it easier to manage groups of machines without the need for manual updates.

Slpkg works in accordance with the standards of the `SlackBuilds.org <https://www.slackbuilds.org>`_ organization to build packages. 
It also uses the Slackware Linux instructions for installing, upgrading or removing packages.

.. image:: https://gitlab.com/dslackw/images/raw/master/slpkg/slpkg_package.png
    :target: https://gitlab.com/dslackw/slpkg


Requirements
------------

.. code-block:: bash

    SQLAlchemy >= 1.4.46
    pythondialog >= 3.5.3
    progress >= 1.6

Install
-------

Install from the official third-party `SBo repository <https://slackbuilds.org/repository/15.0/system/slpkg/>`_ or directly from source:

.. code-block:: bash

    $ tar xvf slpkg-4.7.2.tar.gz
    $ cd slpkg-4.7.2
    $ ./install.sh

Screenshots
-----------

.. image:: https://gitlab.com/dslackw/images/raw/master/slpkg/slpkg_install.png
    :target: https://gitlab.com/dslackw/slpkg

.. image:: https://gitlab.com/dslackw/images/raw/master/slpkg/slpkg_remove.png
    :target: https://gitlab.com/dslackw/slpkg

.. image:: https://gitlab.com/dslackw/images/raw/master/slpkg/slpkg_dependees.png
    :target: https://gitlab.com/dslackw/slpkg


Usage
-----

.. code-block:: bash

    $ slpkg --help
      USAGE: slpkg [OPTIONS] [COMMAND] [FILELIST|PACKAGES...]

      DESCRIPTION:
        Package manager utility for Slackware.

      COMMANDS:
        -u, update                    Update the package lists.
        -U, upgrade                   Upgrade all the packages.
        -c, check-updates             Check for news on ChangeLog.txt.
        -I, repo-info                 Prints the repositories information.
        -g, configs                   Edit the configuration file.
        -L, clean-logs                Clean dependencies log tracking.
        -T, clean-data                Clean all the repositories data
        -D, clean-tmp                 Deletes all the downloaded sources.
        -b, build [packages...]       Build only the packages.
        -i, install [packages...]     Build and install the packages.
        -d, download [packages...]    Download only the scripts and sources.
        -R, remove [packages...]      Remove installed packages.
        -f, find [packages...]        Find installed packages.
        -w, view [packages...]        View packages from the repository.
        -s, search [packages...]      Search packages from the repository.
        -e, dependees [packages...]   Show which packages depend.
        -t, tracking [packages...]    Tracking the packages dependencies.

      OPTIONS:
        -y, --yes                     Answer Yes to all questions.
        -j, --jobs                    Set it for multicore systems.
        -o, --resolve-off             Turns off dependency resolving.
        -r, --reinstall               Upgrade packages of the same version.
        -k, --skip-installed          Skip installed packages.
        -E, --full-reverse            Full reverse dependency.
        -S, --search                  Search packages from the repository.
        -n, --no-silent               Disable silent mode.
        -p, --pkg-version             Print the repository package version.
        -G, --generate-only           Generates only the SLACKBUILDS.TXT file.
        -P, --parallel                Download files in parallel.
        -B, --bin-repo=[REPO]         Set a binary repository.
        -z, --directory=[PATH]        Download files to a specific path.

        -h, --help                    Show this message and exit.
        -v, --version                 Print version and exit.

   If you need more information try to use slpkg manpage.
   Extra help for the commands, use: 'slpkg help [command]'.
   Edit the config file in the /etc/slpkg/slpkg.toml or 'slpkg configs'.



Configuration files
-------------------

.. code-block:: bash

    /etc/slpkg/slpkg.toml
        General configuration of slpkg

    /etc/slpkg/repositories.toml
        Repositories configurations

    /etc/slpkg/blacklist.toml
        Blacklist of packages


Repositories
------------

The supported repositories, please read the repositories configuration file.

- `Slackbuilds <https://slackbuilds.org/>`_ repository.
- `Ponce <https://cgit.ponce.cc/slackbuilds/>`_ repository.
- `Slackware <https://slackware.uk/slackware/slackware64-15.0/>`__ repository.
- `Slackware extra <https://slackware.uk/slackware/slackware64-15.0/extra/>`__ repository.
- `Slackware patches <https://slackware.uk/slackware/slackware64-15.0/patches/>`__ repository.
- `Alien <http://slackware.uk/people/alien/sbrepos/15.0/x86_64/>`_ repository.
- `Multilib <https://slackware.nl/people/alien/multilib/15.0/>`_ repository.
- `Restricted <https://slackware.nl/people/alien/restricted_sbrepos/15.0/x86_64/>`_ repository.
- `Gnome <https://reddoglinux.ddns.net/linux/gnome/41.x/x86_64/>`_ repository.
- `Msb <https://slackware.uk/msb/15.0/1.26/x86_64/>`_ repository.
- `Csb <https://slackware.uk/csb/15.0/x86_64/>`_ repository.
- `Conraid <https://slack.conraid.net/repository/slackware64-current/>`_ repository.
- `Slackonly <https://packages.slackonly.com/pub/packages/15.0-x86_64/>`_ repository.
- `Salix OS <https://download.salixos.org/x86_64/slackware-15.0/>`_ repository.
- `Salix OS extra <https://download.salixos.org/x86_64/slackware-15.0/extra/>`_ repository.
- `Salix OS patches <https://download.salixos.org/x86_64/slackware-15.0/patches/>`_ repository.
- `Slackel OS <http://www.slackel.gr/repo/x86_64/current/>`_ repository.
- `Slint OS <https://slackware.uk/slint/x86_64/slint-15.0/>`_ repository.

Donate
------

If you feel satisfied with this project and want to thanks me make a donation.

.. image:: https://gitlab.com/dslackw/images/raw/master/donate/paypaldonate.png
   :target: https://www.paypal.me/dslackw


Copyright
---------

- Copyright 2014-2023 © Dimitris Zlatanidis.
- Slackware® is a Registered Trademark of Patrick Volkerding. 
- Linux is a Registered Trademark of Linus Torvalds.
