# Copyright 2021 VMware, Inc.
# SPDX-License: Apache-2.0
import logging
import os

import salt.exceptions
import saltext.vmware.utils.common as utils_common
import saltext.vmware.utils.connect as utils_connect
import saltext.vmware.utils.vsphere as utils_vsphere

log = logging.getLogger(__name__)

try:
    from pyVmomi import vmodl, vim, VmomiSupport

    HAS_PYVMOMI = True
except ImportError:
    HAS_PYVMOMI = False


__virtualname__ = "vmware_vsphere"

DEFAULT_EXCEPTIONS = (
    vim.fault.InvalidState,
    vim.fault.NotFound,
    vim.fault.HostConfigFault,
    vmodl.fault.InvalidArgument,
    salt.exceptions.VMwareApiError,
    vim.fault.AlreadyExists,
    vim.fault.UserNotFound,
    salt.exceptions.CommandExecutionError,
    vmodl.fault.SystemError,
    TypeError,
)


def __virtual__():
    if not HAS_PYVMOMI:
        return False, "Unable to import pyVmomi module."
    return __virtualname__


def system_info(
    service_instance=None,
    profile=None,
):
    """
    .. versionadded:: 23.4.4.0rc1

    Return system information about a VMware environment.

    service_instance
        Use this vCenter service connection instance instead of creating a new one. (optional).

    profile
        Profile to use (optional)

    .. code-block:: bash

        salt '*' vmware_vsphere.system_info
    """
    log.debug("Running vmware_vsphere.system_info")
    ret = None
    service_instance = service_instance or utils_connect.get_service_instance(
        config=__opts__, profile=profile
    )
    ret = utils_common.get_inventory(service_instance).about.__dict__
    if "apiType" in ret:
        if ret["apiType"] == "HostAgent":
            ret = dictupdate.update(ret, utils_common.get_hardware_grains(service_instance))
    return ret


def list_resourcepools(
    service_instance=None,
    profile=None,
):
    """
    .. versionadded:: 23.4.4.0rc1

    Returns a list of resource pools for the specified host.

    service_instance
        Use this vCenter service connection instance instead of creating a new one. (optional).

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt '*' vmware_vsphere.list_resourcepools
    """
    log.debug("Running vmware_vsphere.list_resourcepools")
    service_instance = service_instance or utils_connect.get_service_instance(
        config=__opts__, profile=profile
    )
    return utils_vsphere.list_resourcepools(service_instance)


def list_networks(
    service_instance=None,
    profile=None,
):
    """
    .. versionadded:: 23.4.4.0rc1

    Returns a list of networks for the specified host.

    service_instance
        Use this vCenter service connection instance instead of creating a new one. (optional).

    profile
        Profile to use (optional)

    CLI Example:

    .. code-block:: bash

        salt '*' vmware_vsphere.list_networks
    """
    log.debug("Running vmware_vsphere.list_networks")
    service_instance = service_instance or utils_connect.get_service_instance(
        config=__opts__, profile=profile
    )
    return utils_vsphere.list_networks(service_instance)
