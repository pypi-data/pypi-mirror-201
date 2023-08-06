from datetime import datetime
from typing import List, Optional, Tuple

import click
from opendap_downloader.opendap_downloader import (
    download_dataset as download_opendap,
)

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    MOTU_KEY,
    OPENDAP_KEY,
    get_dataset_url_from_id,
    get_protocol_from_url,
    parse_catalogue,
)
from copernicus_marine_client.download_functions.download_motu import (
    download_motu,
)

PROTOCOL_KEYS_ORDER = [OPENDAP_KEY]


class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + " option is mutually exclusive with "
            + ", ".join(self.not_required_if)
            + "."
        ).strip()
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '"
                        + str(self.name)
                        + "' is mutually exclusive with "
                        + str(mutex_opt)
                        + "."
                    )
                else:
                    self.prompt = None
        return super().handle_parse_result(ctx, opts, args)


@click.group()
def cli_group_subset() -> None:
    pass


@cli_group_subset.command(
    "subset",
    help="""Downloads subsets of datasets as NetCDF files taking into account the
server data query limit. A 'dataset-id' (can be found via the
'copernicus-marine describe' command) is required.

Example:

  copernicus-marine subset
--dataset-id METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
--variable analysed_sst --variable sea_ice_fraction
--temporal-subset 2021-01-01 2021-01-02
--geographical-subset 0.0 0.1 0.0 0.1

  copernicus-marine subset -i METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v analysed_sst
  -v sea_ice_fraction -t 2021-01-01 2021-01-02 -g 0.0 0.1 0.0 0.1
""",
)
@click.option(
    "--dataset-url",
    "-u",
    type=str,
    cls=Mutex,
    not_required_if=[
        "dataset_id",
    ],
    help="The full dataset URL",
)
@click.option(
    "--dataset-id",
    "-i",
    type=str,
    cls=Mutex,
    not_required_if=[
        "dataset_url",
    ],
    help="The dataset id",
)
@click.option(
    "--login",
    prompt=True,
    hide_input=False,
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=str,
    help="Specify dataset variables",
    multiple=True,
)
@click.option(
    "--geographical-subset",
    "-g",
    type=(
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-180, max=180),
        click.FloatRange(min=-180, max=180),
    ),
    help="The geographical subset as "
    + "minimal latitude, maximal latitude, "
    + "minimal longitude and maximal longitude",
)
@click.option(
    "--temporal-subset",
    "-t",
    type=(
        click.DateTime(
            ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
        ),
        click.DateTime(
            ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
        ),
    ),
    help="The temporal subset as start datetime and end datetime",
)
@click.option(
    "--depth-range",
    "-d",
    type=(click.FloatRange(min=0), click.FloatRange(min=0)),
    help="The depth range in meters, if depth is a dataset coordinate",
)
@click.option(
    "--output-path",
    "-o",
    type=click.Path(),
    required=True,
    help="The destination path for the downloaded files."
    + " Default is the current directory",
    default="",
)
@click.option(
    "--output-file",
    "-f",
    type=click.Path(),
    help="Concatenate the downloaded data in the given file name"
    + " (under the output path)",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    help="Specify the download size limit (in MB) of the Opendap server if it "
    "can't be provided by the message error",
)
@click.option(
    "--confirmation",
    is_flag=True,
    help="Print dataset metadata and ask for confirmation before download",
)
@click.option(
    "--force-protocol",
    type=click.Choice([OPENDAP_KEY, MOTU_KEY]),
    help="Force download through one of the available protocols",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Flag to specify NOT to send the request to external server. "
    "Returns the request instead",
)
def subset(
    dataset_url: str,
    dataset_id: str,
    login: str,
    password: str,
    variables: List[str],
    geographical_subset: Tuple[float, float, float, float],
    temporal_subset: Tuple[datetime, datetime],
    depth_range: Tuple[float, float],
    output_path: str,
    confirmation: bool,
    output_file: Optional[str],
    limit: Optional[int] = None,
    force_protocol: Optional[str] = None,
    dry_run: Optional[bool] = False,
):
    subset_function(
        dataset_url,
        dataset_id,
        login,
        password,
        variables,
        geographical_subset,
        temporal_subset,
        depth_range,
        output_path,
        confirmation,
        output_file,
        limit,
        force_protocol,
        dry_run,
    )


def subset_function(
    dataset_url: str,
    dataset_id: str,
    login: str,
    password: str,
    variables: List[str],
    geographical_subset: Tuple[float, float, float, float],
    temporal_subset: Tuple[datetime, datetime],
    depth_range: Tuple[float, float],
    output_path: str,
    confirmation: bool,
    output_file: Optional[str],
    limit: Optional[int] = None,
    force_protocol: Optional[str] = None,
    dry_run: Optional[bool] = False,
):
    possible_protocols = (
        PROTOCOL_KEYS_ORDER if not force_protocol else [force_protocol]
    )
    if force_protocol:
        click.echo(f"You forced selection of protocol: {force_protocol}")
    if not dataset_url:
        if not dataset_id:
            raise SyntaxError(
                "Must specify at least one of 'dataset_url' or 'dataset_id'"
            )
        catalogue = parse_catalogue()
        protocol_keys_iterator = iter(possible_protocols)
        while not dataset_url:
            try:
                protocol = next(protocol_keys_iterator)
            except StopIteration:
                raise KeyError(
                    f"Dataset {dataset_id} does not have a valid protocol "
                    f"for subset function. Available protocols: {possible_protocols}"
                )
            dataset_url = get_dataset_url_from_id(
                catalogue, dataset_id, protocol
            )
    else:
        protocol = get_protocol_from_url(dataset_url)
        catalogue = None
    if protocol == OPENDAP_KEY:
        click.echo("download through OPeNDAP")
        if dry_run:
            print(
                "download_opendap("
                + ", ".join(
                    [
                        f"{login}",
                        "HIDING_PASSWORD",
                        f"{dataset_url}",
                        f"{output_path}",
                        f"{output_file}",
                        f"{variables}",
                        f"{geographical_subset}",
                        f"{temporal_subset}",
                        f"{depth_range}",
                        f"{limit}",
                        f"{confirmation}",
                    ]
                )
                + ")"
            )
            return
        download_opendap(
            login,
            password,
            dataset_url,
            output_path,
            output_file,
            variables,
            geographical_subset,
            temporal_subset,
            depth_range,
            limit,
            confirmation,
        )
    elif protocol == MOTU_KEY:
        click.echo("download through MOTU")
        if dry_run:
            print(
                "download_motu("
                + ", ".join(
                    [
                        f"{dataset_url}",
                        f"{dataset_id}",
                        f"{login}",
                        "HIDING_PASSWORD",
                        f"{variables}",
                        f"{geographical_subset}",
                        f"{temporal_subset}",
                        f"{depth_range}",
                        f"{output_path}",
                        f"{output_file}",
                        "NOT_PRINTING_CATALOGUE",
                    ]
                )
                + ")"
            )
            return
        download_motu(
            dataset_url,
            dataset_id,
            login,
            password,
            variables,
            geographical_subset,
            temporal_subset,
            depth_range,
            output_path,
            output_file,
            catalogue=catalogue,
        )
    elif not protocol:
        raise KeyError(
            f"The requested dataset '{dataset_id}' does not have "
            f"{possible_protocols} url available"
        )
    else:
        raise KeyError(f"Protocol {protocol} not handled by subset command")


if __name__ == "__main__":
    subset()
