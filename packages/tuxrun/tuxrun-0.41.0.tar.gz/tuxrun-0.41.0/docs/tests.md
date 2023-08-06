# Tests

TuxRun support some tests, each tests is supported on some but not all architectures.

!!! tip "Listing tests"
    You can list the supported tests with:
    ```shell
    tuxrun --list-tests
    ```

## FVP AEMvA device

The following tests are supported by the default root filesystem.

Device    | Tests                                                                     | Parameters                                     |
----------|---------------------------------------------------------------------------|------------------------------------------------|
fvp-aemva | command                                                                   |                                                |
fvp-aemva | kselftest-(arm64, gpio, ipc, ir, kcmp, kexec, *...)                       | KSELFTEST, SKIPFILE, SHARD_NUMBER, SHARD_INDEX |
fvp-aemva | kunit\*                                                                   |                                                |
fvp-aemva | ltp-(fcntl-locktests, fs_bind, fs_perms_simple, fsx, nptl, smoke)         | SKIPFILE, SHARD_NUMBER, SHARD_INDEX            |
fvp-aemva | perf                                                                      |                                                |
fvp-aemva | rcutorture                                                                |                                                |
fvp-aemva | v4l2                                                                      |                                                |

The following tests are not supported by the default root filesystem. You should
provide a custom root filesystem.

Device    | Tests                                                                                                                                                 | Parameters                          |
----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
fvp-aemva | libgpiod                                                                                                                                              |                                     |
fvp-aemva | libhugetlbfs                                                                                                                                          |                                     |
fvp-aemva | ltp-(cap_bounds, commands, containers, controllers, crypto, cve, filecaps, fs, hugetlb, io, ipc, math, mm, pty, sched, securebits, syscalls, tracing) | SKIPFILE, SHARD_NUMBER, SHARD_INDEX |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters KSELFTEST=http://.../kselftest.tar.xz`

!!! info "kselftest parameters"
    The `CPUPOWER` and `KSELFTEST` parameters are not mandatory. If kselftest
    is present on the filesystem (in `/opt/kselftests/default-in-kernel/`) then the
    parameter is not required.

!!! info "Running a commands"
    When running a commands test passing a `--parameters command-name=custom-test-name`

!!! info "ltp parameter"
    The `SKIPFILE` parameter is not mandatory but allows to specify a skipfile
    present on the root filesystem.

!!! info "kselftest and ltp sharding"
    In order to run kselftest and/or ltp with sharding, define `SHARD_NUMBER`
    to the number of shards and `SHARD_INDEX` to the shard to run. The list of
    kselftest or ltp tests will be sharded by`SHARD_NUMBER` and only the
    `SHARD_INDEX` part will be ran.

!!! warning "KUnit config"
    In order to run KUnit tests, the kernel should be compiled with
    ```
    CONFIG_KUNIT=m
    CONFIG_KUNIT_ALL_TESTS=m
    ```
    The **modules.tar.xz** should be given with `--modules https://.../modules.tar.xz`.


## FVP Modello devices

Device              | Tests          | Parameters                       |
--------------------|----------------|----------------------------------|
fvp-morello-android | binder         |                                  |
fvp-morello-android | bionic         | GTEST_FILTER\* BIONIC_TEST_TYPE\*|
fvp-morello-android | boottest       |                                  |
fvp-morello-android | boringssl      | SYSTEM_URL                       |
fvp-morello-android | compartment    | USERDATA                         |
fvp-morello-android | device-tree    |                                  |
fvp-morello-android | dvfs           |                                  |
fvp-morello-android | libjpeg-turbo  | LIBJPEG_TURBO_URL, SYSTEM_URL    |
fvp-morello-android | libpdfium      | PDFIUM_URL, SYSTEM_URL           |
fvp-morello-android | libpng         | PNG_URL, SYSTEM_URL              |
fvp-morello-android | lldb           | LLDB_URL, TC_URL                 |
fvp-morello-android | logd           | USERDATA                         |
fvp-morello-android | libpcre        |                                  |
fvp-morello-android | multicore      |                                  |
fvp-morello-android | smc91x         |                                  |
fvp-morello-android | virtio_net     |                                  |
fvp-morello-android | zlib           | SYSTEM_URL                       |
fvp-morello-busybox | purecap        |                                  |
fvp-morello-busybox | smc91x         |                                  |
fvp-morello-busybox | virtio_net     |                                  |
fvp-morello-busybox | virtiop9       |                                  |
fvp-morello-debian  | debian-purecap |                                  |
fvp-morello-oe      | fwts           |                                  |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters USERDATA=http://.../userdata.tar.xz`

!!! tip "Default parameters"
    **GTEST_FILTER** is optional and defaults to
    ```
    string_nofortify.*-string_nofortify.strlcat_overread:string_nofortify.bcopy:string_nofortify.memmove
    ```
    **BIONIC_TEST_TYPE** is optional and defaults to `static`. Valid values are `dynamic` and `static`.

## QEMU devices

The following tests are supported by the default root filesystem.

Device  | Tests                                                                     | Parameters                                               |
--------|---------------------------------------------------------------------------|----------------------------------------------------------|
qemu-\* | command                                                                   |                                                          |
qemu-\* | kselftest-(arm64, gpio, ipc, ir, kcmp, kexec, *...)                       | CPUPOWER, KSELFTEST, SKIPFILE, SHARD_NUMBER, SHARD_INDEX |
qemu-\* | kunit\*                                                                   |                                                          |
qemu-\* | ltp-(fcntl-locktests, fs_bind, fs_perms_simple, fsx, nptl, smoke)         | SKIPFILE, SHARD_NUMBER, SHARD_INDEX                      |
qemu-\* | perf                                                                      |                                                          |
qemu-\* | rcutorture                                                                |                                                          |
qemu-\* | v4l2                                                                      |                                                          |

The following tests are not supported by the default root filesystem. You should
provide a custom root filesystem.

Device  | Tests                                                                                                                                                 | Parameters                          |
--------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
qemu-\* | libgpiod                                                                                                                                              |                                     |
qemu-\* | libhugetlbfs                                                                                                                                          |                                     |
qemu-\* | ltp-(cap_bounds, commands, containers, controllers, crypto, cve, filecaps, fs, hugetlb, io, ipc, math, mm, pty, sched, securebits, syscalls, tracing) | SKIPFILE, SHARD_NUMBER, SHARD_INDEX |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters KSELFTEST=http://.../kselftest.tar.xz`

!!! info "kselftest parameters"
    The `CPUPOWER` and `KSELFTEST` parameters are not mandatory. If kselftest
    is present on the filesystem (in `/opt/kselftests/default-in-kernel/`) then the
    parameter is not required.

!!! info "Running a commands"
    When running a commands test passing a `--parameters command-name=custom-test-name`

!!! info "ltp parameter"
    The `SKIPFILE` parameter is not mandatory but allows to specify a skipfile
    present on the root filesystem.

!!! info "kselftest and ltp sharding"
    In order to run kselftest and/or ltp with sharding, define `SHARD_NUMBER`
    to the number of shards and `SHARD_INDEX` to the shard to run. The list of
    kselftest or ltp tests will be sharded by`SHARD_NUMBER` and only the
    `SHARD_INDEX` part will be ran.

!!! info "kselftest-arm64"
    Kselftest-arm64 are tests that can run on a qemu-arm64 machine.

!!! warning "KUnit config"
    In order to run KUnit tests, the kernel should be compiled with
    ```
    CONFIG_KUNIT=m
    CONFIG_KUNIT_ALL_TESTS=m
    ```
    The **modules.tar.xz** should be given with `--modules https://.../modules.tar.xz`.
