from __future__ import annotations

import re
from typing import Optional

import IPython
from seeq import spy
from seeq.spy import _common, _login, Session, Status, _datalab
from seeq.spy._errors import *


def upgrade(version: Optional[str] = None, force_restart: bool = False, use_testpypi: bool = False,
            status: Optional[Status] = None, session: Optional[Session] = None):
    """
    Upgrades to the latest version of SPy that is compatible with this version of Seeq Server.

    An internet connection is required since this uses pip to pull the latest version from PyPI. This must be
    invoked from a Jupyter notebook or other IPython-compatible environment.

    Parameters
    ----------
    version : str, optional
        Attempts to upgrade to the provided version exactly as specified. The full SPy version must be
        provided (e.g. 221.13). For Seeq versions prior to R60, You must specify the full "seeq" module
        version (e.g. 58.0.2.184.12).

    force_restart : bool, optional
        If True, forces the kernel to shut down and restart after the upgrade. All in-memory variables and
        imports will be lost.

    use_testpypi : bool, optional
        For Seeq internal testing only.

    status : spy.Status, optional
        If specified, the supplied Status object will be updated as the command progresses. It gets filled
        in with the same information you would see in Jupyter in the blue/green/red table below your code
        while the command is executed.

    session : spy.Session, optional
        If supplied, the Session object (and its Options) will be used to store the login session state.
        This is used to access the server's current version.

    Examples
    --------
    Upgrade to the latest version of SPy compatible with your Seeq server's major version.
    >>> spy.upgrade()

    Upgrade to version '221.13' of SPy.
    >>> spy.upgrade(version='221.13')

    """
    _common.validate_argument_types([
        (version, 'version', str),
        (force_restart, 'force_restart', bool),
        (use_testpypi, 'use_testpypi', bool),
        (status, 'status', Status),
        (session, 'session', Session),
    ])
    status = Status.validate(status)
    session = Session.validate(session)

    if session.client is None:
        raise SPyRuntimeError('Not logged in. Execute spy.login() before calling this function so that the upgrade '
                              'mechanism knows what version of Seeq Server you are interfacing with.')

    sdk_module_major, sdk_module_minor, _ = _login.get_sdk_module_version_tuple()
    seeq_server_major, seeq_server_minor, seeq_server_patch = _login.get_server_version_tuple(session)
    compatible_module_folder = _login.find_compatible_module(session)

    # The old versioning scheme is like 0.49.3 whereas the new scheme is like 50.1.8
    # See https://seeq.atlassian.net/wiki/spaces/SQ/pages/947225963/Seeq+Versioning+Simplification
    using_old_versioning_scheme = (seeq_server_major == 0)

    first_command = None

    if using_old_versioning_scheme:
        install_compatible_sdk = (sdk_module_major != seeq_server_major or sdk_module_minor != seeq_server_minor)
        compatible_sdk_version_specifier = f'{seeq_server_major}.{seeq_server_minor}.{seeq_server_patch}'
    else:
        install_compatible_sdk = (sdk_module_major != seeq_server_major)
        compatible_sdk_version_specifier = f'{seeq_server_major}.{seeq_server_minor}'

    repository_arg = ' --index-url https://test.pypi.org/simple/' if use_testpypi else ''

    def _install_compatible_sdk():
        if not install_compatible_sdk:
            return None

        if compatible_module_folder is not None:
            return 'pip uninstall -y seeq'
        else:
            return f'pip install -U{repository_arg} seeq~={compatible_sdk_version_specifier}'

    if version is not None:
        if 'r' in version.lower():
            version = re.sub(pattern='r', repl='', string=version, flags=re.IGNORECASE)

        match = re.match(r'^(\d+)\..*', version)
        if not match:
            raise SPyValueError(f'version argument "{version}" is not a full version (e.g. 221.13 or 58.0.2.184.12)')

        version_major = int(match.group(1))
        if version_major < _login.SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
            # We're going to the old single-package scheme, where seeq and spy are in the same package and the
            # versioning is something like 58.0.2.184.12. If the currently-installed sdk module is R60 or later, we must
            # uninstall the seeq-spy package so that, when the older seeq package (which includes spy directly) is
            # installed, pip doesn't think that seeq-spy is still installed as well.
            if sdk_module_major >= _login.SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
                first_command = 'pip uninstall -y seeq-spy'

            second_command = f'pip install -U{repository_arg} seeq=={version}'
        else:
            # We're going to the new seeq-spy package scheme.
            if seeq_server_major < _login.SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
                raise SPyValueError(f'version argument "{version}" is incompatible with Seeq Server version '
                                    f'{session.server_version}')

            first_command = _install_compatible_sdk()
            second_command = f'pip install -U{repository_arg} seeq-spy=={version}'
    else:
        if seeq_server_major >= _login.SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
            first_command = _install_compatible_sdk()
            second_command = f'pip install -U{repository_arg} seeq-spy'
        else:
            if sdk_module_major >= _login.SEEQ_SERVER_VERSION_WHERE_SPY_IS_IN_ITS_OWN_PACKAGE:
                first_command = 'pip uninstall -y seeq-spy'
            second_command = f'pip install -U{repository_arg} seeq~={compatible_sdk_version_specifier}'

    pip_commands = [second_command] if first_command is None else [first_command, second_command]
    pip_command = ' && '.join(pip_commands)

    ipython = IPython.get_ipython()
    if not _datalab.is_ipython() or not _datalab.is_ipython_interactive() or not ipython:
        raise SPyValueError(f'spy.upgrade() must be invoked from a Jupyter notebook or other IPython-compatible '
                            f'environment. Unable to run "{pip_command}".')
    restart_message = 'The kernel will automatically be shut down afterward.' if force_restart else \
        'Please restart the kernel once the packages have been upgraded.'
    status.update(f'Running "{pip_command}". {restart_message}', Status.RUNNING)
    ipython.run_cell(pip_command)

    if force_restart:
        if not ipython.kernel:
            raise SPyValueError(f'Unable get IPython kernel to complete restart')
        ipython.kernel.do_shutdown(True)
