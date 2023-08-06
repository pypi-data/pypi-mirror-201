#!/usr/bin/python3
# -*- coding: utf-8 -*-


import tomli
from pathlib import Path
from dataclasses import dataclass

from slpkg.configs import Configs


@dataclass
class Repositories:
    config = Configs
    color = config.colour()
    bold: str = color['bold']
    red: str = color['red']
    cyan: str = color['cyan']
    endc: str = color['endc']
    bred: str = f'{bold}{red}'

    repositories_file_toml = Path(config.etc_path, 'repositories.toml')

    repos_config = {}
    repositories = {}
    bin_repos_name = []
    bin_enabled_repos = []
    sbo_enabled_repo: bool = True

    sbo_repo_name: str = 'sbo'
    sbo_repo_path: Path = Path(config.lib_path, 'repositories', sbo_repo_name)
    sbo_repo_mirror: str = 'https://slackbuilds.org/slackbuilds/15.0/'
    sbo_repo_slackbuilds: str = 'SLACKBUILDS.TXT'
    sbo_repo_changelog: str = 'ChangeLog.txt'
    sbo_repo_tar_suffix: str = '.tar.gz'
    sbo_repo_tag: str = '_SBo'
    sbo_repo_patch_tag: str = ''

    ponce_repo: bool = False
    ponce_repo_name: str = 'ponce'
    ponce_repo_path: Path = Path(config.lib_path, 'repositories', ponce_repo_name)
    ponce_repo_mirror: str = 'https://cgit.ponce.cc/slackbuilds/plain/'
    ponce_repo_slackbuilds: str = 'SLACKBUILDS.TXT'
    ponce_repo_changelog: str = 'ChangeLog.txt'
    ponce_repo_tag: str = '_SBo'
    ponce_repo_patch_tag: str = ''

    slack_repo: bool = False
    slack_repo_name: str = 'slack'
    slack_repo_path: Path = Path(config.lib_path, 'repositories', slack_repo_name)
    slack_repo_mirror: str = 'https://slackware.uk/slackware/slackware64-15.0/'
    slack_repo_packages: str = 'PACKAGES.TXT'
    slack_repo_checksums: str = 'CHECKSUMS.md5'
    slack_repo_changelog: str = 'ChangeLog.txt'

    slack_extra_repo: bool = False
    slack_extra_repo_name: str = 'slack_extra'
    slack_extra_repo_path: Path = Path(config.lib_path, 'repositories', slack_extra_repo_name)
    slack_extra_repo_mirror: str = 'https://slackware.uk/slackware/slackware64-15.0/'
    slack_extra_packages_mirror: str = 'https://slackware.uk/slackware/slackware64-15.0/extra/'
    slack_extra_repo_packages: str = 'PACKAGES.TXT'
    slack_extra_repo_checksums: str = 'CHECKSUMS.md5'
    slack_extra_repo_changelog: str = 'ChangeLog.txt'

    slack_patches_repo: bool = False
    slack_patches_repo_name: str = 'slack_patches'
    slack_patches_repo_path: Path = Path(config.lib_path, 'repositories', slack_patches_repo_name)
    slack_patches_repo_mirror: str = 'https://slackware.uk/slackware/slackware64-15.0/'
    slack_patches_packages_mirror: str = 'https://slackware.uk/slackware/slackware64-15.0/patches/'
    slack_patches_repo_packages: str = 'PACKAGES.TXT'
    slack_patches_repo_checksums: str = 'CHECKSUMS.md5'
    slack_patches_repo_changelog: str = 'ChangeLog.txt'

    alien_repo: bool = False
    alien_repo_name: str = 'alien'
    alien_repo_path: Path = Path(config.lib_path, 'repositories', alien_repo_name)
    alien_repo_mirror: str = 'https://slackware.nl/people/alien/sbrepos/'
    alien_repo_packages_mirror: str = 'https://slackware.nl/people/alien/sbrepos/15.0/x86_64/'
    alien_repo_packages: str = 'PACKAGES.TXT'
    alien_repo_checksums: str = 'CHECKSUMS.md5'
    alien_repo_changelog: str = 'ChangeLog.txt'

    multilib_repo: bool = False
    multilib_repo_name: str = 'multilib'
    multilib_repo_path: Path = Path(config.lib_path, 'repositories', multilib_repo_name)
    multilib_repo_mirror: str = 'https://slackware.nl/people/alien/multilib/'
    multilib_repo_packages_mirror: str = 'https://slackware.nl/people/alien/multilib/15.0/'
    multilib_repo_packages: str = 'PACKAGES.TXT'
    multilib_repo_checksums: str = 'CHECKSUMS.md5'
    multilib_repo_changelog: str = 'ChangeLog.txt'

    restricted_repo: bool = False
    restricted_repo_name: str = 'restricted'
    restricted_repo_path: Path = Path(config.lib_path, 'repositories', restricted_repo_name)
    restricted_repo_mirror: str = 'https://slackware.nl/people/alien/restricted_sbrepos/'
    restricted_repo_packages_mirror: str = 'https://slackware.nl/people/alien/restricted_sbrepos/15.0/x86_64/'
    restricted_repo_packages: str = 'PACKAGES.TXT'
    restricted_repo_checksums: str = 'CHECKSUMS.md5'
    restricted_repo_changelog: str = 'ChangeLog.txt'

    gnome_repo: bool = False
    gnome_repo_name: str = 'gnome'
    gnome_repo_path: Path = Path(config.lib_path, 'repositories', gnome_repo_name)
    gnome_repo_mirror: str = 'https://reddoglinux.ddns.net/linux/gnome/43.x/x86_64/'
    gnome_repo_packages: str = 'PACKAGES.TXT'
    gnome_repo_checksums: str = 'CHECKSUMS.md5'
    gnome_repo_changelog: str = 'ChangeLog.txt'

    msb_repo: bool = False
    msb_repo_name: str = 'msb'
    msb_repo_path: Path = Path(config.lib_path, 'repositories', msb_repo_name)
    msb_repo_mirror: str = 'https://slackware.uk/msb/'
    msb_repo_packages_mirror: str = 'https://slackware.uk/msb/15.0/1.26/x86_64/'
    msb_repo_packages: str = 'PACKAGES.TXT'
    msb_repo_checksums: str = 'CHECKSUMS.md5'
    msb_repo_changelog: str = 'ChangeLog.txt'

    csb_repo: bool = False
    csb_repo_name: str = 'csb'
    csb_repo_path: Path = Path(config.lib_path, 'repositories', csb_repo_name)
    csb_repo_mirror: str = 'https://slackware.uk/csb/'
    csb_repo_packages_mirror: str = 'https://slackware.uk/csb/15.0/x86_64/'
    csb_repo_packages: str = 'PACKAGES.TXT'
    csb_repo_checksums: str = 'CHECKSUMS.md5'
    csb_repo_changelog: str = 'ChangeLog.txt'

    conraid_repo: bool = False
    conraid_repo_name: str = 'conraid'
    conraid_repo_path: Path = Path(config.lib_path, 'repositories', conraid_repo_name)
    conraid_repo_mirror: str = 'https://reddoglinux.ddns.net/linux/conraid_43.x/x86_64/'
    conraid_repo_packages: str = 'PACKAGES.TXT'
    conraid_repo_checksums: str = 'CHECKSUMS.md5'
    conraid_repo_changelog: str = 'ChangeLog.txt'

    slackonly_repo: bool = False
    slackonly_repo_name: str = 'slackonly'
    slackonly_repo_path: Path = Path(config.lib_path, 'repositories', slackonly_repo_name)
    slackonly_repo_mirror: str = 'https://packages.slackonly.com/pub/packages/15.0-x86_64/'
    slackonly_repo_packages: str = 'PACKAGES.TXT'
    slackonly_repo_checksums: str = 'CHECKSUMS.md5'
    slackonly_repo_changelog: str = 'ChangeLog.txt'

    salixos_repo: bool = False
    salixos_repo_name: str = 'salixos'
    salixos_repo_path: Path = Path(config.lib_path, 'repositories', salixos_repo_name)
    salixos_repo_mirror: str = 'https://download.salixos.org/x86_64/slackware-15.0/'
    salixos_repo_packages: str = 'PACKAGES.TXT'
    salixos_repo_checksums: str = 'CHECKSUMS.md5'
    salixos_repo_changelog: str = 'ChangeLog.txt'

    salixos_extra_repo: bool = False
    salixos_extra_repo_name: str = 'salixos_extra'
    salixos_extra_repo_path: Path = Path(config.lib_path, 'repositories', salixos_extra_repo_name)
    salixos_extra_repo_mirror: str = 'https://download.salixos.org/x86_64/slackware-15.0/'
    salixos_extra_repo_packages_mirror: str = 'https://download.salixos.org/x86_64/slackware-15.0/extra/'
    salixos_extra_repo_packages: str = 'PACKAGES.TXT'
    salixos_extra_repo_checksums: str = 'CHECKSUMS.md5'
    salixos_extra_repo_changelog: str = 'ChangeLog.txt'

    salixos_patches_repo: bool = False
    salixos_patches_repo_name: str = 'salixos_patches'
    salixos_patches_repo_path: Path = Path(config.lib_path, 'repositories', salixos_patches_repo_name)
    salixos_patches_repo_mirror: str = 'https://download.salixos.org/x86_64/slackware-15.0/'
    salixos_patches_repo_packages_mirror: str = 'https://download.salixos.org/x86_64/slackware-15.0/patches/'
    salixos_patches_repo_packages: str = 'PACKAGES.TXT'
    salixos_patches_repo_checksums: str = 'CHECKSUMS.md5'
    salixos_patches_repo_changelog: str = 'ChangeLog.txt'

    slackel_repo: bool = False
    slackel_repo_name: str = 'slackel'
    slackel_repo_path: Path = Path(config.lib_path, 'repositories', slackel_repo_name)
    slackel_repo_mirror: str = 'http://www.slackel.gr/repo/x86_64/current/'
    slackel_repo_packages: str = 'PACKAGES.TXT'
    slackel_repo_checksums: str = 'CHECKSUMS.md5'
    slackel_repo_changelog: str = 'ChangeLog.txt'

    slint_repo: bool = False
    slint_repo_name: str = 'slint'
    slint_repo_path: Path = Path(config.lib_path, 'repositories', slint_repo_name)
    slint_repo_mirror: str = 'https://slackware.uk/slint/x86_64/slint-15.0/'
    slint_repo_packages: str = 'PACKAGES.TXT'
    slint_repo_checksums: str = 'CHECKSUMS.md5'
    slint_repo_changelog: str = 'ChangeLog.txt'

    try:
        if repositories_file_toml.is_file():
            with open(repositories_file_toml, 'rb') as repo:
                repos_config = tomli.load(repo)['REPOSITORIES']

            sbo_repo_name: str = repos_config['SBO_REPO_NAME']
            sbo_repo_mirror: str = repos_config['SBO_REPO_MIRROR']
            sbo_repo_slackbuilds: str = repos_config['SBO_REPO_SLACKBUILDS']
            sbo_repo_changelog: str = repos_config['SBO_REPO_CHANGELOG']
            sbo_repo_tar_suffix: str = repos_config['SBO_REPO_TAR_SUFFIX']
            sbo_repo_tag: str = repos_config['SBO_REPO_TAG']
            sbo_repo_patch_tag: str = repos_config['SBO_REPO_PATCH_TAG']

            ponce_repo: bool = repos_config['PONCE_REPO']
            ponce_repo_name: str = repos_config['PONCE_REPO_NAME']
            ponce_repo_mirror: str = repos_config['PONCE_REPO_MIRROR']
            ponce_repo_slackbuilds: str = repos_config['PONCE_REPO_SLACKBUILDS']
            ponce_repo_changelog: str = repos_config['PONCE_REPO_CHANGELOG']
            ponce_repo_tag: str = repos_config['PONCE_REPO_TAG']
            ponce_repo_patch_tag: str = repos_config['PONCE_REPO_PATCH_TAG']

            slack_repo: bool = repos_config['SLACK_REPO']
            slack_repo_name: str = repos_config['SLACK_REPO_NAME']
            slack_repo_mirror: str = repos_config['SLACK_REPO_MIRROR']
            slack_repo_packages: str = repos_config['SLACK_REPO_PACKAGES']
            slack_repo_checksums: str = repos_config['SLACK_REPO_CHECKSUMS']
            slack_repo_changelog: str = repos_config['SLACK_REPO_CHANGELOG']

            slack_extra_repo: bool = repos_config['SLACK_EXTRA_REPO']
            slack_extra_repo_name: str = repos_config['SLACK_EXTRA_REPO_NAME']
            slack_extra_repo_mirror: str = repos_config['SLACK_EXTRA_REPO_MIRROR']
            slack_extra_repo_packages_mirror: str = repos_config['SLACK_EXTRA_REPO_PACKAGES_MIRROR']
            slack_extra_repo_packages: str = repos_config['SLACK_EXTRA_REPO_PACKAGES']
            slack_extra_repo_checksums: str = repos_config['SLACK_EXTRA_REPO_CHECKSUMS']
            slack_extra_repo_changelog: str = repos_config['SLACK_EXTRA_REPO_CHANGELOG']

            slack_patches_repo: bool = repos_config['SLACK_PATCHES_REPO']
            slack_patches_repo_name: str = repos_config['SLACK_PATCHES_REPO_NAME']
            slack_patches_repo_mirror: str = repos_config['SLACK_PATCHES_REPO_MIRROR']
            slack_patches_repo_packages_mirror: str = repos_config['SLACK_PATCHES_REPO_PACKAGES_MIRROR']
            slack_patches_repo_packages: str = repos_config['SLACK_PATCHES_REPO_PACKAGES']
            slack_patches_repo_checksums: str = repos_config['SLACK_PATCHES_REPO_CHECKSUMS']
            slack_patches_repo_changelog: str = repos_config['SLACK_PATCHES_REPO_CHANGELOG']

            alien_repo: bool = repos_config['ALIEN_REPO']
            alien_repo_name: str = repos_config['ALIEN_REPO_NAME']
            alien_repo_mirror: str = repos_config['ALIEN_REPO_MIRROR']
            alien_repo_packages_mirror: str = repos_config['ALIEN_REPO_PACKAGES_MIRROR']
            alien_repo_packages: str = repos_config['ALIEN_REPO_PACKAGES']
            alien_repo_checksums: str = repos_config['ALIEN_REPO_CHECKSUMS']
            alien_repo_changelog: str = repos_config['ALIEN_REPO_CHANGELOG']

            multilib_repo: bool = repos_config['MULTILIB_REPO']
            multilib_repo_name: str = repos_config['MULTILIB_REPO_NAME']
            multilib_repo_mirror: str = repos_config['MULTILIB_REPO_MIRROR']
            multilib_repo_packages_mirror: str = repos_config['MULTILIB_REPO_PACKAGES_MIRROR']
            multilib_repo_packages: str = repos_config['MULTILIB_REPO_PACKAGES']
            multilib_repo_checksums: str = repos_config['MULTILIB_REPO_CHECKSUMS']
            multilib_repo_changelog: str = repos_config['MULTILIB_REPO_CHANGELOG']

            restricted_repo: bool = repos_config['RESTRICTED_REPO']
            restricted_repo_name: str = repos_config['RESTRICTED_REPO_NAME']
            restricted_repo_mirror: str = repos_config['RESTRICTED_REPO_MIRROR']
            restricted_repo_packages_mirror: str = repos_config['RESTRICTED_REPO_PACKAGES_MIRROR']
            restricted_repo_packages: str = repos_config['RESTRICTED_REPO_PACKAGES']
            restricted_repo_checksums: str = repos_config['RESTRICTED_REPO_CHECKSUMS']
            restricted_repo_changelog: str = repos_config['RESTRICTED_REPO_CHANGELOG']

            gnome_repo: bool = repos_config['GNOME_REPO']
            gnome_repo_name: str = repos_config['GNOME_REPO_NAME']
            gnome_repo_mirror: str = repos_config['GNOME_REPO_MIRROR']
            gnome_repo_packages: str = repos_config['GNOME_REPO_PACKAGES']
            gnome_repo_checksums: str = repos_config['GNOME_REPO_CHECKSUMS']
            gnome_repo_changelog: str = repos_config['GNOME_REPO_CHANGELOG']

            msb_repo: bool = repos_config['MSB_REPO']
            msb_repo_name: str = repos_config['MSB_REPO_NAME']
            msb_repo_mirror: str = repos_config['MSB_REPO_MIRROR']
            msb_repo_packages_mirror: str = repos_config['MSB_REPO_PACKAGES_MIRROR']
            msb_repo_packages: str = repos_config['MSB_REPO_PACKAGES']
            msb_repo_checksums: str = repos_config['MSB_REPO_CHECKSUMS']
            msb_repo_changelog: str = repos_config['MSB_REPO_CHANGELOG']

            csb_repo: bool = repos_config['CSB_REPO']
            csb_repo_name: str = repos_config['CSB_REPO_NAME']
            csb_repo_mirror: str = repos_config['CSB_REPO_MIRROR']
            csb_repo_packages_mirror: str = repos_config['CSB_REPO_PACKAGES_MIRROR']
            csb_repo_packages: str = repos_config['CSB_REPO_PACKAGES']
            csb_repo_checksums: str = repos_config['CSB_REPO_CHECKSUMS']
            csb_repo_changelog: str = repos_config['CSB_REPO_CHANGELOG']

            conraid_repo: bool = repos_config['CONRAID_REPO']
            conraid_repo_name: str = repos_config['CONRAID_REPO_NAME']
            conraid_repo_mirror: str = repos_config['CONRAID_REPO_MIRROR']
            conraid_repo_packages: str = repos_config['CONRAID_REPO_PACKAGES']
            conraid_repo_checksums: str = repos_config['CONRAID_REPO_CHECKSUMS']
            conraid_repo_changelog: str = repos_config['CONRAID_REPO_CHANGELOG']

            slackonly_repo: bool = repos_config['SLACKONLY_REPO']
            slackonly_repo_name: str = repos_config['SLACKONLY_REPO_NAME']
            slackonly_repo_mirror: str = repos_config['SLACKONLY_REPO_MIRROR']
            slackonly_repo_packages: str = repos_config['SLACKONLY_REPO_PACKAGES']
            slackonly_repo_checksums: str = repos_config['SLACKONLY_REPO_CHECKSUMS']
            slackonly_repo_changelog: str = repos_config['SLACKONLY_REPO_CHANGELOG']

            salixos_repo: bool = repos_config['SALIXOS_REPO']
            salixos_repo_name: str = repos_config['SALIXOS_REPO_NAME']
            salixos_repo_mirror: str = repos_config['SALIXOS_REPO_MIRROR']
            salixos_repo_packages: str = repos_config['SALIXOS_REPO_PACKAGES']
            salixos_repo_checksums: str = repos_config['SALIXOS_REPO_CHECKSUMS']
            salixos_repo_changelog: str = repos_config['SALIXOS_REPO_CHANGELOG']

            salixos_extra_repo: bool = repos_config['SALIXOS_EXTRA_REPO']
            salixos_extra_repo_name: str = repos_config['SALIXOS_EXTRA_REPO_NAME']
            salixos_extra_repo_mirror: str = repos_config['SALIXOS_EXTRA_REPO_MIRROR']
            salixos_extra_repo_packages_mirror: str = repos_config['SALIXOS_EXTRA_REPO_PACKAGES_MIRROR']
            salixos_extra_repo_packages: str = repos_config['SALIXOS_EXTRA_REPO_PACKAGES']
            salixos_extra_repo_checksums: str = repos_config['SALIXOS_EXTRA_REPO_CHECKSUMS']
            salixos_extra_repo_changelog: str = repos_config['SALIXOS_EXTRA_REPO_CHANGELOG']

            salixos_patches_repo: bool = repos_config['SALIXOS_PATCHES_REPO']
            salixos_patches_repo_name: str = repos_config['SALIXOS_PATCHES_REPO_NAME']
            salixos_patches_repo_mirror: str = repos_config['SALIXOS_PATCHES_REPO_MIRROR']
            salixos_patches_repo_packages_mirror: str = repos_config['SALIXOS_PATCHES_REPO_PACKAGES_MIRROR']
            salixos_patches_repo_packages: str = repos_config['SALIXOS_PATCHES_REPO_PACKAGES']
            salixos_patches_repo_checksums: str = repos_config['SALIXOS_PATCHES_REPO_CHECKSUMS']
            salixos_patches_repo_changelog: str = repos_config['SALIXOS_PATCHES_REPO_CHANGELOG']

            slackel_repo: bool = repos_config['SLACKEL_REPO']
            slackel_repo_name: str = repos_config['SLACKEL_REPO_NAME']
            slackel_repo_mirror: str = repos_config['SLACKEL_REPO_MIRROR']
            slackel_repo_packages: str = repos_config['SLACKEL_REPO_PACKAGES']
            slackel_repo_checksums: str = repos_config['SLACKEL_REPO_CHECKSUMS']
            slackel_repo_changelog: str = repos_config['SLACKEL_REPO_CHANGELOG']

            slint_repo: bool = repos_config['SLINT_REPO']
            slint_repo_name: str = repos_config['SLINT_REPO_NAME']
            slint_repo_mirror: str = repos_config['SLINT_REPO_MIRROR']
            slint_repo_packages: str = repos_config['SLINT_REPO_PACKAGES']
            slint_repo_checksums: str = repos_config['SLINT_REPO_CHECKSUMS']
            slint_repo_changelog: str = repos_config['SLINT_REPO_CHANGELOG']

    except (tomli.TOMLDecodeError, KeyError) as error:
        raise SystemExit(f'\n{config.prog_name} {bred}Error{endc}: {error}: in the configuration file '
                         f"'{repositories_file_toml}'.\n"
                         f"\nIf you have upgraded the '{config.prog_name}' probably you need to run:\n"
                         f"'mv {repositories_file_toml}.new {repositories_file_toml}'.\n"
                         f"or '{cyan}slpkg_new-configs{endc}' command.\n")

    # Default sbo repository configs.
    repo_tag: str = sbo_repo_tag
    patch_repo_tag: str = sbo_repo_patch_tag
    sbo_enabled_repository: str = sbo_repo_name
    if ponce_repo:
        sbo_enabled_repository: str = ponce_repo_name
        repo_tag: str = ponce_repo_tag
        patch_repo_tag: str = ponce_repo_patch_tag
        sbo_enabled_repo: bool = False

    # List of repositories.
    repositories = {
        sbo_repo_name: [sbo_enabled_repo, sbo_repo_path, sbo_repo_changelog],
        ponce_repo_name: [ponce_repo, ponce_repo_path, ponce_repo_changelog],
        slack_repo_name: [slack_repo, slack_repo_path, slack_repo_changelog],
        slack_extra_repo_name: [slack_extra_repo, slack_extra_repo_path, slack_extra_repo_changelog],
        slack_patches_repo_name: [slack_patches_repo, slack_patches_repo_path, slack_patches_repo_changelog],
        alien_repo_name: [alien_repo, alien_repo_path, alien_repo_changelog],
        multilib_repo_name: [multilib_repo, multilib_repo_path, multilib_repo_changelog],
        restricted_repo_name: [restricted_repo, restricted_repo_path, restricted_repo_changelog],
        gnome_repo_name: [gnome_repo, gnome_repo_path, gnome_repo_changelog],
        msb_repo_name: [msb_repo, msb_repo_path, msb_repo_changelog],
        csb_repo_name: [csb_repo, csb_repo_path, csb_repo_changelog],
        conraid_repo_name: [conraid_repo, conraid_repo_path, conraid_repo_changelog],
        slackonly_repo_name: [slackonly_repo, slackonly_repo_path, slackonly_repo_changelog],
        salixos_repo_name: [salixos_repo, salixos_repo_path, salixos_repo_changelog],
        salixos_extra_repo_name: [salixos_extra_repo, salixos_extra_repo_path, salixos_extra_repo_changelog],
        salixos_patches_repo_name: [salixos_patches_repo, salixos_patches_repo_path,
                                    salixos_patches_repo_changelog],
        slackel_repo_name: [slackel_repo, slackel_repo_path, slackel_repo_changelog],
        slint_repo_name: [slint_repo, slint_repo_path, slint_repo_changelog]
    }

    # All the binary repositories names.
    bin_repos_names = list(repositories.keys())[2:]

    # All the enabled binary repositories names.
    for repo, enabled in repositories.items():
        if repo not in [sbo_repo_name, ponce_repo_name]:
            if enabled[0]:
                bin_enabled_repos.append(repo)
