"""The main function for the Cyral CLI.
"""

from collections import OrderedDict
import json
import os
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    List,
    TextIO,
    Tuple,
    Union,
)

import click
import yaml
from columnar import columnar

from ._aws import (
    s3_proxy_is_configured,
    configure_s3_proxy_settings,
    update_s3_proxy_endpoint,
    update_aws_creds,
    S3ProxyPluginNotInstalled,
)
from ._pgpass import update_pgpass
from ..sdk.client import Client, DEFAULT_LOCAL_PORT, StoredCredentials
from ..sdk.api import (
    AccessTokenClient,
    AccessInfoClient,
    CABundleClient,
    SidecarClient,
    UserClient,
)


@click.group()
@click.option(
    "--cp-address",
    help="Cyral Control Plane Address",
)
@click.option(
    "--idp", help="Identity Provider to use to authenticate to Cyral"
)
@click.option(
    "--local-port",
    type=int,
    default=DEFAULT_LOCAL_PORT,
    show_default=True,
    help="Local port number for receiving OAuth2 redirects",
)
@click.option(
    "--stored-creds/--no-stored-creds",
    default=True,
    show_default=True,
    help="Use and/or store refresh token in ~/.cyral",
)
@click.option(
    "--offline-access/--no-offline-access",
    default=False,
    show_default=True,
    help="Obtain a (long lived) offline refresh token",
)
@click.option(
    "--realm",
    help="Authentication realm (usually not needed)",
    default="default",
    show_default=True,
)
@click.version_option()
@click.pass_context
def cli(
    ctx,
    cp_address: str,
    idp: str,
    local_port: int,
    stored_creds: bool,
    offline_access: bool,
    realm: str,
) -> None:
    # pylint: disable=too-many-arguments
    """Cyral CLI"""

    if not cp_address:
        print(
            "The Cyral control plane address must be specified using the "
            "--cp-address option."
        )
        sys.exit(1)
    ctx.ensure_object(dict)
    creds_file = None
    if stored_creds:
        creds_file = os.path.join("~", ".cyral", f".{cp_address}.creds")
        creds_file = os.path.expanduser(creds_file)
    creds = StoredCredentials(creds_file)
    cyral_client = Client(
        cp_address,
        stored_creds=creds,
        local_port=local_port,
        offline_access=offline_access,
        idp=idp,
        realm=realm,
    )
    ctx.obj["client"] = cyral_client
    ctx.obj["stored_creds"] = creds


# hidden command to print authorization header for API calls
@cli.command(hidden=True)
@click.pass_context
def auth(ctx) -> None:
    "Print an authorization header for making API calls to the control plane."
    cyral_client = ctx.obj["client"]
    auth_hdr = cyral_client.get_auth_header()
    for key, value in auth_hdr.items():
        print(f"{key}: {value}")


# hidden command to print user information
@cli.command(hidden=True, name="user")
@click.pass_context
def user_info(ctx) -> None:
    "Print information about the current user."
    cyral_client = ctx.obj["client"]
    print(
        json.dumps(
            UserClient(cyral_client).get_current_user(),
            sort_keys=True,
            indent=4,
        )
    )


@cli.group()
def access() -> None:
    """
    Access a data repo.
    """


@access.command(name="token")
@click.pass_context
def access_token(ctx) -> None:
    """Obtain access token for a data repo."""
    cyral_client = ctx.obj["client"]
    access_token_client = AccessTokenClient(cyral_client)
    db_token = access_token_client.get()
    print(db_token)


def _get_repo_selection(max_value: int) -> int:
    while True:
        inp = input("Enter a row number, ENTER for more, or 'q' to quit: ")
        inp = inp.strip()
        if inp == "":
            return 0
        if inp == "q":
            return -1
        try:
            i = int(inp)
            if i < 1 or i > max_value:
                raise ValueError()
            return i
        except ValueError:
            print("Invalid input")


known_repo_types = [
    "auroramysql",
    "aurorapostgres",
    "denodo",
    "dremio",
    "galera",
    "mariadb",
    "mongodb",
    "mysql",
    "oracle",
    "postgresql",
    "redshift",
    "s3",
    "sqlserver",
]


@access.command(name="repo")
@click.pass_context
@click.option(
    "-n",
    "--name",
    "repo_name",
    help="Repo name in Cyral (substring match)",
)
@click.option(
    "--tag",
    "repo_tags",
    multiple=True,
    help="Repo tag (substring match)",
)
@click.option(
    "-t",
    "--type",
    "repo_type",
    help="Repo type",
    type=click.Choice(known_repo_types, case_sensitive=True),
)
@click.option(
    "--repos-per-page",
    "page_size",
    help="Number of repos shown per page",
    type=int,
    default=10,
    show_default=True,
)
@click.option(
    "--output-format",
    "-f",
    help="Output format",
    type=click.Choice(["plain", "json"], case_sensitive=True),
    default="plain",
    show_default=True,
)
def access_repo(
    # pylint: disable=too-many-arguments
    ctx,
    repo_name: Optional[str],
    repo_tags: Optional[List[str]],
    repo_type: Optional[str],
    page_size: int,
    output_format: str,
) -> None:
    """Obtain information to access a data repo"""
    # pylint: disable=too-many-locals
    cyral_client = ctx.obj["client"]
    access_info_client = AccessInfoClient(
        cyral_client,
        repo_name=repo_name,
        repo_tags=repo_tags,
        repo_type=repo_type,
        page_size=page_size,
    )

    count = 0
    # internal data corresponding to rows of output shown to user.
    # note that this is built cumulatively across pages.
    data: List[Tuple[Any, Any]] = []
    headers: List[str] = ["#", "Repo Name", "Type", "Database Account"]
    for repos in iter(access_info_client):
        # build table containing list of repos shown to user
        output_table: List[List[Union[int, str]]] = []
        for repo in repos:
            for db_account in repo["userAccounts"]:
                count += 1
                output_table.append(
                    [
                        count,
                        repo["repoName"],
                        repo["repoType"],
                        db_account["name"],
                    ]
                )
                data.append((repo, db_account))
        if count == 1:
            i = 1  # automatically select the only result.
        else:
            print(columnar(output_table, headers, no_borders=True))
            i = _get_repo_selection(count)
        if i == 0:
            continue
        if i < 0:
            break
        repo = data[i - 1][0]
        db_account = data[i - 1][1]

        # print information for accessing selected repo.
        sidecar_id = repo["accessGatewaySidecarId"]
        binding_id = repo["accessGatewayBindingId"]
        sidecar_client = SidecarClient(
            cyral_client,
        )
        sidecar_info = sidecar_client.get(sidecar_id)
        binding_info = sidecar_client.get_binding(sidecar_id, binding_id)
        uinfo = UserClient(cyral_client).get_current_user()
        password = AccessTokenClient(cyral_client).get()
        port = sidecar_client.port_for_binding(sidecar_id, binding_info)
        output = OrderedDict(
            [
                ("host", f"{SidecarClient.endpoint(sidecar_info)}"),
                (
                    "port",
                    f"{port}",
                ),
                ("username", f"idp:{uinfo['email']}:{db_account['name']}"),
                ("password", f"{password}"),
            ]
        )
        if output_format == "plain":
            print(
                "Use the following information for accessing repo "
                + f"{repo['repoName']}:\n"
            )
            for key, val in output.items():
                print(f"{key.capitalize()}: {val}")
        elif output_format == "json":
            print(json.dumps(output, indent=4))
        break


@access.command(name="s3")
@click.pass_context
@click.option(
    "--aws-profile",
    default="cyral",
    show_default=True,
    help="Name of the AWS profile to configure",
)
@click.option(
    "--autoconfigure/--no-autoconfigure",
    default=False,
    show_default=True,
    help="Autoconfigure (without confirmation) S3 proxy settings",
)
@click.option(
    "--silent/--no-silent",
    default=False,
    show_default=True,
    help="Do not print confirmation messages",
)
def access_s3(
    ctx,
    aws_profile: str,
    autoconfigure: bool,
    silent: bool,
) -> None:
    """Configure AWS profile for accessing S3 via Cyral"""
    # pylint: disable=too-many-locals
    # first get details for the (only) S3 repo accessible to user
    # if it exists.
    cyral_client = ctx.obj["client"]
    access_info_client = AccessInfoClient(
        cyral_client,
        repo_type="s3",
        page_size=1,
    )
    repos: List[Dict[str, Any]] = next(iter(access_info_client), [])
    if not repos:
        print(
            "S3 is not accessible to you via Cyral.",
            file=sys.stderr,
        )
        sys.exit(1)
    s3_repo = repos[0]
    sidecar_id = s3_repo["accessGatewaySidecarId"]
    binding_id = s3_repo["accessGatewayBindingId"]
    sidecar_client = SidecarClient(
        cyral_client,
    )
    sidecar_info = sidecar_client.get(sidecar_id)
    binding_info = sidecar_client.get_binding(sidecar_id, binding_id)
    user_email = UserClient(cyral_client).get_current_user()["email"]
    token = AccessTokenClient(cyral_client).get()
    sidecar_address = (
        f"{SidecarClient.endpoint(sidecar_info)}:"
        + f"{sidecar_client.port_for_binding(sidecar_id, binding_info, True)}"
    )
    ca_bundle = CABundleClient(cyral_client).get()
    if not s3_proxy_is_configured(aws_profile):
        user_input = ""
        if not autoconfigure:
            user_input = input(
                "S3 proxy settings are not correctly configured to work "
                "with Cyral.\nProceed with the configuration first? [y/n] "
            )
        if autoconfigure or str(user_input).lower() == "y":
            try:
                configure_s3_proxy_settings(
                    aws_profile,
                    sidecar_address,
                    ca_bundle,
                )
            except S3ProxyPluginNotInstalled as ex:
                print(ex)
                sys.exit(1)
            if not silent:
                print("Successfully configured S3 proxy settings.")
    else:
        # update profile with latest token and other information.
        update_s3_proxy_endpoint(aws_profile, sidecar_address)
    # update aws creds with access token
    update_aws_creds(token, user_email, aws_profile, silent)


@access.command(name="pg")
@click.pass_context
@click.option(
    "--silent/--no-silent",
    default=False,
    show_default=True,
    help="Do not print confirmation messages",
)
def access_pg(
    ctx,
    silent: bool,
) -> None:
    """Configure access to postgres databases via Cyral in .pgpass file."""
    cyral_client = ctx.obj["client"]
    access_info_client = AccessInfoClient(
        cyral_client,
        repo_type="postgresql",
        page_size=20,
    )
    sidecar_client = SidecarClient(cyral_client)
    sidecar_ids: Dict[str, None] = {}
    for repos in iter(access_info_client):
        for repo in repos:
            sidecar_ids[repo["accessGatewaySidecarId"]] = None
    endpoints: List[str] = []
    for sidecar_id in sidecar_ids:
        sidecar_info = sidecar_client.get(sidecar_id)
        endpoint = SidecarClient.endpoint(sidecar_info)
        if endpoint:
            endpoints.append(endpoint)
    if not endpoints:
        print(
            "Did not find any sidecar endpoints for postgres repos, "
            "skipping write to PGPASS file",
            file=sys.stderr,
        )
        return
    token = AccessTokenClient(cyral_client).get()
    update_pgpass(token, endpoints)
    if not silent:
        num = len(endpoints)
        print(f"Updated PGPASS file with {num} sidecar endpoint(s).")


@cli.group(
    name="sidecar",
)
@click.pass_context
@click.option(
    "--id",
    "sidecar_id",
    help="the id of the sidecar",
    type=click.types.STRING,
)
@click.option(
    "--name",
    "sidecar_name",
    help="the name of the sidecar",
    type=click.types.STRING,
)
def sidecar_group(
    ctx: click.Context, sidecar_id: str, sidecar_name: str
) -> None:
    """sidecar related commands"""
    cyral_client: Client = ctx.obj["client"]
    ctx.obj["sidecar_client"] = SidecarClient(
        cyral_client,
    )
    ctx.obj["sidecar_id"] = sidecar_id
    ctx.obj["sidecar_name"] = sidecar_name


@sidecar_group.command(
    name="get",
)
@click.pass_context
@click.option(
    "--output-format",
    help="output format",
    show_default=True,
    type=click.Choice(["yaml", "json", "table"]),
    show_choices=True,
    default="table",
)
def sidecar_get(ctx: click.Context, output_format: str):
    """get information about sidecars in the control plane"""

    sidecar_id: str = ctx.obj["sidecar_id"]
    sidecar_name: str = ctx.obj["sidecar_name"]
    if sidecar_name and sidecar_id:
        print(
            "At most one of --sidecar-id"
            + " and --sidecar-name can be specified.",
            file=sys.stderr,
        )
        sys.exit(1)

    sidecar_client: SidecarClient = ctx.obj["sidecar_client"]
    if sidecar_id or sidecar_name:
        if sidecar_id:
            # an exception (http status 500 - unfortunately indistinguishable
            # from other possible errors) gets raised if a sidecar
            # with given id does not exist.
            data = sidecar_client.get(sidecar_id)
        else:
            sidecars = sidecar_client.list_sidecars()
            filtered_sidecars = [
                side
                for side in sidecars
                if side["sidecar"]["name"] == sidecar_name
            ]
            if len(filtered_sidecars) == 0:
                print(
                    f"Sidecar with name {sidecar_name} not found",
                    file=sys.stderr,
                )
                sys.exit(1)

            sidecar_id = filtered_sidecars[0]["id"]
            data = filtered_sidecars[0]["sidecar"]

        def columnize_single_sidecar(
            data: Any,
        ) -> Tuple[List[List[str]], List[str]]:
            rows = []
            rows.append(
                [
                    sidecar_id,
                    data["name"],
                    SidecarClient.endpoint(data),
                ]
            )

            header = ["id", "name", "endpoint"]
            return rows, header

        format_output(output_format, data, columnize_single_sidecar)
    else:
        sidecars = sidecar_client.list_sidecars()

        def columnize_all_sidecars(
            data: Any,
        ) -> Tuple[List[List[str]], List[str]]:
            rows = []
            for sidecar in data:
                rows.append(
                    [
                        sidecar["id"],
                        sidecar["sidecar"]["name"],
                        SidecarClient.endpoint(sidecar["sidecar"]),
                    ]
                )

            header = ["id", "name", "endpoint"]
            return rows, header

        format_output(output_format, sidecars, columnize_all_sidecars)


@sidecar_group.group(name="set")
@click.pass_context
def sidecar_set_group(ctx: click.Context):
    """set different sidecar options"""

    sidecar_client: SidecarClient = ctx.obj["sidecar_client"]
    sidecar_name: str = ctx.obj["sidecar_name"]
    sidecar_id: str = ctx.obj["sidecar_id"]

    if (sidecar_name and sidecar_id) or not (sidecar_name or sidecar_id):
        print(
            "Exactly one of --sidecar-id"
            + " and --sidecar-name must be specified.",
            file=sys.stderr,
        )
        sys.exit(1)

    sidecar = None
    if sidecar_name:
        sidecars = sidecar_client.list_sidecars()
        for side in sidecars:
            if side["sidecar"]["name"] == sidecar_name:
                sidecar = side["sidecar"]
                sidecar_id = side["id"]
                break
    else:
        sidecar = sidecar_client.get(sidecar_id)
    if not sidecar:
        sidecar_spec = (
            f"name {sidecar_name}" if sidecar_name else f"id {sidecar_id}"
        )
        print(
            f"error finding the sidecar with {sidecar_spec}", file=sys.stderr
        )
        sys.exit(1)
    ctx.obj["sidecar"] = sidecar
    ctx.obj["sidecar_id"] = sidecar_id


@sidecar_set_group.command(name="log-level")
@click.pass_context
@click.option(
    "--level",
    type=str,
    help="the log level for a sidecar service. It can be of the form <level> "
    + "(log level applicable to all services) or <service>:<level> (log level "
    + "for a specific service). <level> can be one of fatal, error, warn, "
    + "info, debug, or trace. The list of services may vary depending on the "
    + "sidecar version and configuration. This option can be specified "
    + "multiple times, the last log level specified for a service is the one "
    + "that is set.",
    multiple=True,
)
def sidecar_set_log_level(ctx: click.Context, level: Tuple[str]):
    """
    set the log level for a sidecar service

    # EXAMPLES:

    ## set the level for all services

    cyral sidecar set log-level --level debug

    ## set the level for a single service

    cyral sidecar set log-level --level dispatcher:warn

    ## set the level for multiple services

    cyral sidecar set log-level --level dispatcher:warn --level pg-wire:debug
    """

    if len(level) <= 0:
        print(
            "At least one '--level' option must be specified.", file=sys.stderr
        )
        sys.exit(1)

    sidecar_client: SidecarClient = ctx.obj["sidecar_client"]
    sidecar: Dict[str, Any] = ctx.obj["sidecar"]
    sidecar_id: str = ctx.obj["sidecar_id"]

    valid_log_level_list = [lvl.value for lvl in SidecarClient.LogLevel]

    levels: Dict[str, SidecarClient.LogLevel] = {}
    for lvl in level:
        split_level = lvl.split(":")
        if len(split_level) == 1:
            level_for_all = split_level[0]
            for service in sidecar["services"]:
                try:
                    levels[service] = SidecarClient.LogLevel(level_for_all)
                except ValueError:
                    print(
                        f"Invalid log level '{level_for_all}', valid log "
                        + f"levels are {valid_log_level_list}.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
        else:
            service = split_level[0]
            if service not in sidecar["services"]:
                print(f"Service '{service}' does not exist", file=sys.stderr)
                sys.exit(1)

            current_level = split_level[1]
            try:
                levels[service] = SidecarClient.LogLevel(current_level)
            except ValueError:
                print(
                    f"Invalid log level '{current_level}', valid log "
                    + f"levels are {valid_log_level_list}."
                )
                sys.exit(1)

    sidecar_client.set_log_level(sidecar_id, **levels)


def format_output(
    output_format: str,
    data: Any,
    columnize: Callable[[Any], Tuple[List[List[str]], List[str]]],
    stream: TextIO = sys.stdout,
):
    """
    format_output formats output and prints it depending on the specified
    format
    """
    if output_format == "json":
        print(json.dumps(data, indent=4), file=stream)
    elif output_format == "yaml":
        yaml.dump(data, stream)
    else:
        columns, rows = columnize(data)
        print(columnar(columns, rows, no_borders=True), file=stream)


def main():
    """entrypoint for the Cyral CLI"""
    # pylint: disable=no-value-for-parameter
    cli(obj={}, auto_envvar_prefix="CYRAL")


if __name__ == "__main__":
    main()
