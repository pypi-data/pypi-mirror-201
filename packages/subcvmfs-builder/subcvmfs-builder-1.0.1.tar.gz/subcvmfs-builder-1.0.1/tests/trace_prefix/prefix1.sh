export PARROT_CVMFS_REPO="repo1:url=url1,pubkey=pubkey1 repo2:url=url2,pubkey=pubkey2 "
export PARROT_ALLOW_SWITCHING_CVMFS_REPOSITORIES=yes
export HTTP_PROXY="DIRECT"
parrot_run --name-list namelist.txt --env-list envlist.txt
