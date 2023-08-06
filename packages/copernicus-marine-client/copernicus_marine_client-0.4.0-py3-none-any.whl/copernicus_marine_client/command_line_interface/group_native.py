from typing import Optional

import click

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    FTP_KEY,
    get_protocol_from_url,
    get_protocol_url_from_id,
)
from copernicus_marine_client.download_functions.download_ftp import (
    create_filenames_out,
    download_ftp,
    download_header,
)

PROTOCOL_KEYS_ORDER = [FTP_KEY]


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
def cli_group_native() -> None:
    pass


@cli_group_native.command(
    "native",
    help="""Downloads native data files based on
    dataset_id or datafiles url path.
    The function fetches the files recursively if a folder path is passed as url.
    When provided a dataset id,
    all the files in the corresponding folder will be downloaded.

    By default for any download request, a summary of the request result is
    displayed to the user and a confirmation is asked.
    This can be turned down.
Example:

  copernicus-marine native -nd -o data_folder --dataset-id
  cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m

  copernicus-marine native -nd -o data_folder --dataset-url
  ftp://my.cmems-du.eu/Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m
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
    help="Path to the data files",
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
    "--no-directories",
    "-nd",
    is_flag=True,
    help="Option to not recreate folder hierarchy" + " in ouput directory.",
    default=False,
)
@click.option(
    "--show-outputnames",
    is_flag=True,
    help="Option to display the names of the"
    + " output files before download.",
    default=False,
)
@click.option(
    "--output-path",
    "-o",
    type=click.Path(),
    required=True,
    help="The destination path for the downloaded files."
    + " Default is the current directory",
    default=".",
)
@click.option(
    "--no-confirmation",
    is_flag=True,
    default=False,
    help="Ask for confirmation before download, after header display",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Flag to specify NOT to send the request to external server. "
    "Returns the request instead",
)
def native(
    dataset_url: str,
    dataset_id: str,
    login: str,
    password: str,
    no_directories: bool,
    show_outputnames: bool,
    output_path: str,
    no_confirmation: bool,
    dry_run: Optional[bool] = False,
):
    native_function(
        dataset_url,
        dataset_id,
        login,
        password,
        no_directories,
        show_outputnames,
        output_path,
        no_confirmation,
        dry_run,
    )


def native_function(
    dataset_url: str,
    dataset_id: str,
    login: str,
    password: str,
    no_directories: bool,
    show_outputnames: bool,
    output_path: str,
    no_confirmation: bool,
    dry_run: Optional[bool] = False,
):
    if not dataset_url:
        if not dataset_id:
            raise SyntaxError(
                "Must specify at least one of 'dataset_url' or 'dataset_id'"
            )
        protocol, dataset_url = get_protocol_url_from_id(
            dataset_id, PROTOCOL_KEYS_ORDER
        )
    else:
        protocol = get_protocol_from_url(dataset_url)
    if protocol == FTP_KEY:
        if dry_run:
            print(
                "download_ftp("
                + ", ".join(
                    [
                        f"{login}",
                        "HIDE_PASSWORD",
                        f"{no_directories}",
                        f"{output_path}",
                        "HOST(REQUIRE_LOGIN)",
                        "FILENAME_IN(REQUIRE_LOGIN)",
                        "FILENAME_OUT(REQUIRE_LOGIN)",
                    ]
                )
            )
            return

        message, host, filenames_in = download_header(
            [dataset_url], login, password
        )
        filenames_out = create_filenames_out(
            filenames_in, output_path, no_directories
        )
        print(message)
        if show_outputnames:
            click.echo("Output filenames:")
            [click.echo(filename_out) for filename_out in filenames_out]
        if not no_confirmation:
            click.confirm("Do you want to continue?", abort=True)
        download_summary = download_ftp(
            login,
            password,
            no_directories,
            output_path,
            host,
            filenames_in,
            filenames_out,
        )
        click.echo(download_summary)
    else:
        raise TypeError(f"Protocol type not handled: {protocol}")
