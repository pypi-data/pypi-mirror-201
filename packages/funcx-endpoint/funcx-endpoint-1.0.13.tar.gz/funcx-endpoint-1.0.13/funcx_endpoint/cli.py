from __future__ import annotations

import importlib.util
import json
import logging
import pathlib
import sys

import click
from click import ClickException

from funcx.sdk.login_manager import LoginManager
from funcx.sdk.login_manager.whoami import print_whoami_info

from .endpoint.endpoint import Endpoint
from .endpoint.endpoint_manager import EndpointManager
from .endpoint.utils.config import Config
from .logging_config import setup_logging

log = logging.getLogger(__name__)


class CommandState:
    def __init__(self):
        self.endpoint_config_dir: str = str(pathlib.Path.home() / ".funcx")
        self.debug = False
        self.no_color = False
        self.log_to_console = False
        self.endpoint_uuid = None
        self.die_with_parent = False

    @classmethod
    def ensure(cls) -> CommandState:
        return click.get_current_context().ensure_object(CommandState)


def init_endpoint_configuration_dir(funcx_conf_dir: pathlib.Path):
    if not funcx_conf_dir.exists():
        log.info(
            "No existing configuration found at %s. Initializing...", funcx_conf_dir
        )
        try:
            funcx_conf_dir.mkdir(mode=0o700, exist_ok=True)
        except Exception as exc:
            e = click.ClickException(
                f"{exc}\n\nUnable to create configuration directory"
            )
            raise e from exc

    elif not funcx_conf_dir.is_dir():
        raise click.ClickException(
            f"File already exists: {funcx_conf_dir}\n\n"
            "Refusing to initialize funcX configuration directory: path already exists"
        )


def get_config_dir() -> pathlib.Path:
    state = CommandState.ensure()
    return pathlib.Path(state.endpoint_config_dir)


def get_cli_endpoint() -> Endpoint:
    # this getter creates an Endpoint object from the CommandState
    # it takes its various configurable values from the current CommandState
    # as a result, any number of CLI options may be used to tweak the CommandState
    # via callbacks, and the Endpoint will only be constructed within commands which
    # access the Endpoint via this getter
    funcx_dir = get_config_dir()
    init_endpoint_configuration_dir(funcx_dir)

    state = CommandState.ensure()
    endpoint = Endpoint(debug=state.debug)

    return endpoint


def set_param_to_config(ctx, param, value):
    state = CommandState.ensure()
    setattr(state, param.name, value)
    return state


def log_flag_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    state = set_param_to_config(ctx, param, value)
    setup_logging(debug=state.debug, no_color=state.no_color)


def common_options(f):
    f = click.option(
        "--debug",
        is_flag=True,
        expose_value=False,
        callback=log_flag_callback,
        is_eager=True,
        help="Emit extra information generally only helpful for developers",
    )(f)
    f = click.option(
        "--log-to-console",
        is_flag=True,
        expose_value=False,
        is_eager=True,
        callback=log_flag_callback,
        help="Emit log lines to console as well as log",
    )(f)
    f = click.option(
        "--no-color",
        is_flag=True,
        expose_value=False,
        is_eager=True,
        callback=log_flag_callback,
        help="Do not colorize the (console) log lines",
    )(f)

    f = click.help_option("-h", "--help")(f)
    return f


def start_options(f):
    f = click.option(
        "--endpoint-uuid",
        default=None,
        callback=set_param_to_config,
        help="The UUID to register with the Globus Compute services",
    )(f)
    f = click.option(
        "--die-with-parent",
        is_flag=True,
        hidden=True,
        callback=set_param_to_config,
        help="Shutdown if parent process goes away",
    )(f)
    return f


def name_arg(f):
    return click.argument("name", required=False, default="default")(f)


def config_dir_callback(ctx, param, value):
    if value is None or ctx.resilient_parsing:
        return
    state = CommandState.ensure()
    state.endpoint_config_dir = value


@click.group("funcx-endpoint")
@click.option(
    "-c",
    "--config-dir",
    default=None,
    help="override default config dir",
    callback=config_dir_callback,
    expose_value=False,
)
def app():
    # the main command group body runs on every command, so the block below will always
    # execute
    setup_logging()  # Until we parse the CLI flags, just setup default logging


@app.command("version")
@common_options
def version_command():
    """Show the version of funcx-endpoint"""
    import funcx_endpoint

    click.echo(f"FuncX endpoint version: {funcx_endpoint.__version__}")


@app.command(name="configure", help="Configure an endpoint")
@click.option("--endpoint-config", default=None, help="a template config to use")
@click.option(
    "--multi-tenant",
    is_flag=True,
    default=False,
    hidden=True,
    help="Configure endpoint as multi-tenant capable",
)
@name_arg
@common_options
def configure_endpoint(
    *,
    name: str,
    endpoint_config: str | None,
    multi_tenant: bool,
):
    """Configure an endpoint

    Drops a config.py template into the funcx configs directory.
    The template usually goes to ~/.funcx/<ENDPOINT_NAME>/config.py
    """
    funcx_dir = get_config_dir()
    ep_dir = funcx_dir / name
    Endpoint.configure_endpoint(ep_dir, endpoint_config, multi_tenant)


@app.command(name="start", help="Start an endpoint by name")
@name_arg
@start_options
@common_options
def start_endpoint(*, name: str, **_kwargs):
    """Start an endpoint

    This function will do:
    1. Connect to the broker service, and register itself
    2. Get connection info from broker service
    3. Start the interchange as a daemon

    |                      Broker service       |
    |               -----2----> Forwarder       |
    |    /register <-----3----+   ^             |
    +-----^-----------------------+-------------+
          |     |                 |
          1     4                 6
          |     v                 |
    +-----+-----+-----+           v
    |      Start      |---5---> EndpointInterchange
    |     Endpoint    |         daemon
    +-----------------+
    """
    state = CommandState.ensure()
    _do_start_endpoint(
        name=name,
        endpoint_uuid=state.endpoint_uuid,
        die_with_parent=state.die_with_parent,
    )


@app.command(name="logout", help="Logout from all endpoints")
@click.option(
    "--force",
    is_flag=True,
    help="Revokes tokens even with currently running endpoints",
)
def logout_endpoints(force: bool):
    success, msg = _do_logout_endpoints(force=force)
    if not success:
        # Raising ClickException is apparently the way to do sys.exit(1)
        #     and return a non-zero value to the command line
        # See https://click.palletsprojects.com/en/8.1.x/exceptions/
        if not isinstance(msg, str) or msg is None:
            # Generic unsuccessful if no reason was given
            msg = "Logout unsuccessful"
        raise ClickException(msg)


@app.command("whoami", help="Show the currently logged-in identity")
@click.option(
    "--linked-identities",
    is_flag=True,
    default=False,
    help="Also show identities linked to the currently logged-in primary identity.",
)
def whoami(linked_identities: bool) -> None:
    try:
        print_whoami_info(linked_identities)
    except ValueError as ve:
        raise ClickException(str(ve))


def _do_logout_endpoints(
    force: bool, running_endpoints: dict | None = None
) -> tuple[bool, str | None]:
    """
    Logout from all endpoints and remove cached authentication credentials

    Returns True, None if logout was successful and tokens were found and revoked
    Returns False, error_msg if token revocation was not done
    """
    if running_endpoints is None:
        funcx_dir = get_config_dir()
        running_endpoints = Endpoint.get_running_endpoints(funcx_dir)
    tokens_revoked = False
    error_msg = None
    if running_endpoints and not force:
        running_list = ", ".join(running_endpoints.keys())
        log.info(
            "The following endpoints are currently running: "
            + running_list
            + "\nPlease use logout --force to proceed"
        )
        error_msg = "Not logging out with running endpoints without --force"
    else:
        tokens_revoked = LoginManager().logout()
        if tokens_revoked:
            log.info("Logout succeeded and all cached credentials were revoked")
        else:
            error_msg = "No cached tokens were found, already logged out?"
            log.info(error_msg)
    return tokens_revoked, error_msg


def read_config(endpoint_dir: pathlib.Path) -> Config:
    endpoint_name = endpoint_dir.name

    try:
        conf_path = endpoint_dir / "config.py"
        spec = importlib.util.spec_from_file_location("config", conf_path)
        if not (spec and spec.loader):
            raise Exception(f"Unable to import configuration (no spec): {conf_path}")
        config = importlib.util.module_from_spec(spec)
        if not config:
            raise Exception(f"Unable to import configuration (no config): {conf_path}")
        spec.loader.exec_module(config)
        return config.config

    except FileNotFoundError as err:
        if not endpoint_dir.exists():
            configure_command = "funcx-endpoint configure"
            if endpoint_name != "default":
                configure_command += f" {endpoint_name}"
            msg = (
                f"{err}"
                f"\n\nEndpoint '{endpoint_name}' is not configured!"
                "\n1. Please create a configuration template with:"
                f"\n\t{configure_command}"
                "\n2. Update the configuration"
                "\n3. Start the endpoint\n"
            )
            raise ClickException(msg) from err
        msg = (
            f"{err}"
            "\n\nUnable to find required configuration file; has the configuration"
            "\ndirectory been corrupted?"
        )
        raise ClickException(msg) from err

    except AttributeError as err:
        msg = (
            f"{err}"
            "\n\nFailed to find expected data structure in configuration file."
            "\nHas the configuration file been corrupted or modified incorrectly?\n"
        )
        raise ClickException(msg) from err

    except Exception:
        log.exception(
            "funcX v0.2.0 made several non-backwards compatible changes to the config. "
            "Your config might be out of date. "
            "Refer to "
            "https://funcx.readthedocs.io/en/latest/endpoints.html#configuring-funcx"
        )
        raise


def _do_start_endpoint(
    *,
    name: str,
    endpoint_uuid: str | None,
    die_with_parent: bool = False,
):
    state = CommandState.ensure()
    ep_dir = get_config_dir() / name
    if ep_dir.is_dir():
        setup_logging(
            logfile=ep_dir / "endpoint.log",
            debug=state.debug,
            console_enabled=state.log_to_console,
            no_color=state.no_color,
        )

    reg_info = {}
    if sys.stdin and not (sys.stdin.closed or sys.stdin.isatty()):
        try:
            stdin_data = json.loads(sys.stdin.read())
            if not isinstance(stdin_data, dict):
                type_name = stdin_data.__class__.__name__
                raise ValueError(
                    "Expecting JSON dictionary with endpoint registration info; got"
                    f" {type_name} instead"
                )
            reg_info = stdin_data
        except Exception as e:
            exc_type = e.__class__.__name__
            log.debug("Invalid registration info on stdin -- (%s) %s", exc_type, e)

    ep_config = read_config(ep_dir)
    if ep_config.multi_tenant:
        epm = EndpointManager(ep_dir, endpoint_uuid, ep_config)
        epm.start()
    else:
        get_cli_endpoint().start_endpoint(
            ep_dir,
            endpoint_uuid,
            ep_config,
            state.log_to_console,
            state.no_color,
            reg_info,
            die_with_parent,
        )


@app.command("stop")
@name_arg
@click.option(
    "--remote",
    is_flag=True,
    help="send stop signal to all endpoints with this UUID, local or elsewhere",
)
@common_options
def stop_endpoint(*, name: str, remote: bool):
    """Stops an endpoint using the pidfile"""
    _do_stop_endpoint(name=name, remote=remote)


def _do_stop_endpoint(*, name: str, remote: bool = False) -> None:
    ep_dir = get_config_dir() / name
    Endpoint.stop_endpoint(ep_dir, read_config(ep_dir), remote=remote)


@app.command("restart")
@name_arg
@common_options
@start_options
def restart_endpoint(*, name: str, **_kwargs):
    """Restarts an endpoint"""
    state = CommandState.ensure()
    _do_stop_endpoint(name=name)
    _do_start_endpoint(
        name=name,
        endpoint_uuid=state.endpoint_uuid,
        die_with_parent=state.die_with_parent,
    )


@app.command("list")
@common_options
def list_endpoints():
    """List all available endpoints"""
    funcx_dir = get_config_dir()
    Endpoint.print_endpoint_table(funcx_dir)


@app.command("delete")
@name_arg
@click.option(
    "--force",
    default=False,
    is_flag=True,
    help="Deletes the local endpoint even if the web service returns an error.",
)
@click.option(
    "--yes", default=False, is_flag=True, help="Do not ask for confirmation to delete."
)
@common_options
def delete_endpoint(*, name: str, force: bool, yes: bool):
    """Deletes an endpoint and its config."""
    if not yes:
        click.confirm(
            f"Are you sure you want to delete the endpoint <{name}>?", abort=True
        )

    ep_dir = get_config_dir() / name
    Endpoint.delete_endpoint(ep_dir, read_config(ep_dir), force)


def cli_run():
    """Entry point for setuptools to point to"""
    app()


if __name__ == "__main__":
    app()
