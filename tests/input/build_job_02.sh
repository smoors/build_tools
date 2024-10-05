#!/bin/bash -l
#SBATCH --job-name=test-job-gpu
#SBATCH --output="%x-%j.out"
#SBATCH --error="%x-%j.err"
#SBATCH --time=23:59:59
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --gpus-per-node=1
#SBATCH --partition=ampere_gpu

if [ -z $PREFIX_EB ]; then
  echo 'PREFIX_EB is not set!'
  exit 1
fi

# set environment
local_arch="$VSC_ARCH_LOCAL$VSC_ARCH_SUFFIX"
export BUILD_TOOLS_LOAD_DUMMY_MODULES=1
export BUILD_TOOLS_RUN_LMOD_CACHE=
export BUILD_TOOLS_LMOD_CACHE_JOBNAME="lmod_cache_$local_arch"
export LANG=C
export PATH=$PREFIX_EB/easybuild-framework:$PATH
export PYTHONPATH=$PREFIX_EB/easybuild-easyconfigs:$PREFIX_EB/easybuild-easyblocks:$PREFIX_EB/easybuild-framework:$PREFIX_EB/vsc-base/lib

# make build directory
if [ -z $SLURM_JOB_ID ]; then
    export TMPDIR=/tmp/eb-test-build/$USER/
fi
mkdir -p $TMPDIR
mkdir -p /tmp/eb-test-build

# update MODULEPATH for cross-compilations
if [ "zen2-ib" != "$local_arch" ]; then
    export MODULEPATH=${MODULEPATH//$local_arch/zen2-ib}
fi

bwrap eb  --cuda-compute-capabilities=8.0

if [ $? -ne 0 ]; then
    if [ -n "$SLURM_JOB_ID" ]; then
        rm -rf /tmp/eb-test-build
    fi
    exit 1
fi

rsync src dest

scontrol -Q release jobname="$BUILD_TOOLS_LMOD_CACHE_JOBNAME" || :
