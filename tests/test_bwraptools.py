#
# Copyright 2017-2024 Vrije Universiteit Brussel
# All rights reserved.
#
# This file is part of build_tools (https://github.com/vub-hpc/build_tools),
# originally created by the HPC team of Vrije Universiteit Brussel (https://hpc.vub.be),
# with support of Vrije Universiteit Brussel (https://www.vub.be),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# the Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
##
"""
Unit tests for build_tools.bwraptools

@author: Samuel Moors (Vrije Universiteit Brussel)
"""

from build_tools import bwraptools

job_options = {
    'eb_installpath': '/apps/brussel/$VSC_OS_LOCAL/skylake',
}


def test_bwrap_prefix(mock_realpath_apps_brussel):
    prefix = bwraptools.bwrap_prefix(job_options, 'HPL', 'skylake')
    ref_prefix = 'mkdir -p /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/software/HPL && mkdir -p /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL && bwrap --bind / / --bind /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/software/HPL /vscmnt/brussel_pixiu_apps/_apps_brussel/$VSC_OS_LOCAL/skylake/software/HPL --bind /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL /vscmnt/brussel_pixiu_apps/_apps_brussel/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL --dev /dev --bind /dev/log /dev/log'  # noqa: E501

    assert prefix == ref_prefix


def test_rsync_copy():
    rsync_cmds = bwraptools.rsync_copy(job_options, 'HPL', '2.3-foss-2022a', 'skylake')
    ref_rsync_cmds = """\
dest_subdir=$(</apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL/modules_subdir.txt)
dest_mod_file="/apps/brussel/$VSC_OS_LOCAL/skylake/modules/$dest_subdir/all/HPL/2.3-foss-2022a.lua"
echo "bwrap install dir: /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/software/HPL/2.3-foss-2022a/"
echo "destination install dir: /apps/brussel/$VSC_OS_LOCAL/skylake/software/HPL/2.3-foss-2022a/"
echo "bwrap module file: /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL/2.3-foss-2022a.lua"
echo "destination module file: $dest_mod_file"
test -d /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/software/HPL/2.3-foss-2022a/ || { echo "ERROR: bwrap install dir does not exist"; exit 1; }
test "$(ls -A /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/software/HPL/2.3-foss-2022a/)" || { echo "ERROR: bwrap install dir empty"; exit 1; }
test -s /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL/2.3-foss-2022a.lua || { echo "ERROR: bwrap module file does not exist or empty"; exit 1; }
rsync -a --link-dest=/apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/software/HPL/2.3-foss-2022a/ /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/software/HPL/2.3-foss-2022a/ /apps/brussel/$VSC_OS_LOCAL/skylake/software/HPL/2.3-foss-2022a/ || { echo "ERROR: failed to copy bwrap install dir"; exit 1; }
rsync -a --link-dest=/apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL/2.3-foss-2022a.lua "$dest_mod_file" || { echo "ERROR: failed to copy bwrap module file"; exit 1; }
rm -rf /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/software/HPL/2.3-foss-2022a/ /apps/brussel/bwrap/$VSC_OS_LOCAL/skylake/modules/bwrap/all/HPL/2.3-foss-2022a.lua"""  # noqa: E501

    assert rsync_cmds == ref_rsync_cmds
