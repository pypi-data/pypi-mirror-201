# Running under FVP

TuxRun allows to run linux kernel under FVP for Morello and AEMvA.

!!! note "Supported devices"
    See the [architecture matrix](devices.md#fvp-devices) for the supported devices.

## Preparing the environment

In order to use TuxRun with FVP, you have to build container images:

* tuxrun fvp image (only for podman)
* AEMvA fvp model
* morello fvp model

Start by cloning the git repository:

```shell
git clone https://gitlab.com/Linaro/tuxrun
cd tuxrun
```

### TuxRun fvp image

Build the TuxRun image

=== "podman"
    ```shell
    cd share/fvp
    make fvp
    ```

=== "docker"
    !!! info "Runtime"
        When using docker runtime, this container is not needed.

### AEMvA fvp model

Build the container containing the AEMvA FVP model:

=== "podman"

    ```shell
    cd share/fvp
    make fvp-aemva
    ```

=== "docker"

    ```shell
    cd share/fvp
    make fvp-aemva RUNTIME=docker
    ```

!!! warning "Container tag"
    The container should be named **fvp:aemva-11.20.15** in order for TuxRun
    to work.


### Morello fvp model

Build the container containing the Morello FVP model:

=== "podman"

    ```shell
    cd share/fvp
    make fvp-morello
    ```

=== "docker"

    ```shell
    cd share/fvp
    make fvp-morello RUNTIME=docker
    ```

!!! warning "Container tag"
    The container should be named **fvp:morello-0.11.34** in order for TuxRun
    to work.

## AEMvA testing

The command line is really similar to the qemu one:

!!! example
    === "podman"
        ```shell
        tuxrun --image tuxrun:fvp \
               --device fvp-aemva \
               --kernel https://example.com/Image \
               --dtb https://example.com/fvp-base-revc.dtb
        ```

    === "docker"
        ```shell
        tuxrun --runtime docker \
               --device fvp-aemva \
               --kernel https://example.com/Image \
               --dtb https://example.com/fvp-base-revc.dtb
        ```

## Boot testing

In order to run a simple boot test on **fvp-morello-busybox**:

!!! example
    === "podman"
        ```shell
        tuxrun --image tuxrun:fvp \
               --device fvp-morello-buxybox \
               --ap-romfw https://example.com/fvp/morello/tf-bl1.bin \
               --mcp-fw https://example.com/fvp/morello/mcp_fw.bin \
               --mcp-romfw https://example.com/fvp/morello/mcp_romfw.bin \
               --rootfs https://example.com/fvp/morello/rootfs.img.xz \
               --scp-fw https://example.com/fvp/morello/scp_fw.bin \
               --scp-romfw https://example.com/fvp/morello/scp_romfw.bin \
               --fip https://example.com/fvp/morello/fip.bin
        ```

    === "docker"
        ```shell
        tuxrun --runtime docker \
               --device fvp-morello-buxybox \
               --ap-romfw https://example.com/fvp/morello/tf-bl1.bin \
               --mcp-fw https://example.com/fvp/morello/mcp_fw.bin \
               --mcp-romfw https://example.com/fvp/morello/mcp_romfw.bin \
               --rootfs https://example.com/fvp/morello/rootfs.img.xz \
               --scp-fw https://example.com/fvp/morello/scp_fw.bin \
               --scp-romfw https://example.com/fvp/morello/scp_romfw.bin \
               --fip https://example.com/fvp/morello/fip.bin
        ```


## Testing on Android

In order to run an Android test on **fvp-morello-android**:

=== "podman"

    ```shell
    tuxrun --image tuxrun:fvp \
           --device fvp-morello-android \
           --ap-romfw https://example.com/fvp/morello/tf-bl1.bin \
           --mcp-fw https://example.com/fvp/morello/mcp_fw.bin \
           --mcp-romfw https://example.com/fvp/morello/mcp_romfw.bin \
           --rootfs https://example.com/fvp/morello/rootfs.img.xz \
           --scp-fw https://example.com/fvp/morello/scp_fw.bin \
           --scp-romfw https://example.com/fvp/morello/scp_romfw.bin \
           --fip https://example.com/fvp/morello/fip.bin \
           --parameters USERDATA=https://example.com/fvp/morello/userdata.tar.xz \
           --tests binder
    ```

=== "docker"

    ```shell
    tuxrun --runtime docker \
           --device fvp-morello-android \
           --ap-romfw https://example.com/fvp/morello/tf-bl1.bin \
           --mcp-fw https://example.com/fvp/morello/mcp_fw.bin \
           --mcp-romfw https://example.com/fvp/morello/mcp_romfw.bin \
           --rootfs https://example.com/fvp/morello/rootfs.img.xz \
           --scp-fw https://example.com/fvp/morello/scp_fw.bin \
           --scp-romfw https://example.com/fvp/morello/scp_romfw.bin \
           --fip https://example.com/fvp/morello/fip.bin \
           --parameters USERDATA=https://example.com/fvp/morello/userdata.tar.xz \
           --tests binder
    ```
