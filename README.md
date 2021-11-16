# How to build rpm package

```sh
./build.sh <SPEC-NAME>
```

Where `<SPEC-NAME>` is the name of .spec file, located in softvisio/rpm repository.

# Manual build

```sh
docker run \
    --rm -it --shm-size=1g \
    -v $PWD:/root/rpmbuild/SPECS \
    "softvisio/rpm:el8"

dnf -y builddep /root/rpmbuild/SPECS/tini.spec

rpmbuild -ba tini.spec
```

# How to remove old RPMs

```sh
./remove.sh repo/.el8-x86_64/pg13-extensions-1-20210526130724.el8.x86_64.rpm
```
