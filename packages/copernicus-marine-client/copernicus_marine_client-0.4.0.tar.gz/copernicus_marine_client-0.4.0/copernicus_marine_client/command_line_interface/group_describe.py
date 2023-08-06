import warnings
from json import dumps

import click

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineCatalogue,
    filter_catalogue_with_strings,
    parse_catalogue,
)

warnings.filterwarnings(
    "ignore",
    message="the .identification and"
    + " .serviceidentification properties will merge into .identification"
    + " being a list of properties.  This is currently implemented in"
    + " .identificationinfo.  "
    + "Please see https://github.com/geopython/OWSLib/issues/38 for more "
    + "information",
)
warnings.filterwarnings(
    "ignore",
    message="The .keywords and .keywords2 properties will merge into the"
    + " .keywords property in the future, with .keywords becoming a list of"
    + " MD_Keywords instances. This is currently implemented in .keywords2."
    + " Please see https://github.com/geopython/OWSLib/issues/301 for more "
    + "information",
)
warnings.filterwarnings(
    "ignore",
    message="The .keywords_object attribute will become .keywords proper in "
    + "the next release. .keywords_object is a list of ibstances of the "
    + "Keyword class. See for https://github.com/geopython/OWSLib/pull/765"
    + " more details.",
)


@click.group()
def cli_group_describe() -> None:
    pass


@cli_group_describe.command(
    "describe",
    help="""Parse the Copernicus Marine catalogue, then display a
        JSON-ified version of the corresponding python object.

        The default display contains information on the products, and more data
        can be displayed using the _include-<argument>_ flags (see Usage section).

        The _contains_ option allows the user to specify one or several strings to
        filter through the catalogue display. The search is performed recursively
        on all attributes of the catalogue, and the tokens only need to be
        contained in one of the attributes (i.e. not exact match).

        Example:

        > copernicus-marine describe --contains METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
        --include-datasets

        > copernicus-marine describe -c METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
        """,
)
@click.option(
    "--one-line",
    type=bool,
    is_flag=True,
    default=False,
    help="Output JSON on one line",
)
@click.option(
    "--include-description",
    type=bool,
    is_flag=True,
    default=False,
    help="Include product description in output",
)
@click.option(
    "--include-datasets",
    type=bool,
    is_flag=True,
    default=False,
    help="Include product dataset details in output",
)
@click.option(
    "--include-providers",
    type=bool,
    is_flag=True,
    default=False,
    help="Include product provider details in output",
)
@click.option(
    "--include-keywords",
    type=bool,
    is_flag=True,
    default=False,
    help="Include product keyword details in output",
)
@click.option(
    "--contains",
    "-c",
    type=str,
    multiple=True,
    help="Filter catalogue output. Returns products with attributes "
    "matching a string token",
)
@click.option(
    "--overwrite-cache",
    type=bool,
    is_flag=True,
    default=False,
    help="Force to refresh the catalogue by overwriting the local cache",
)
def describe(
    include_description: bool,
    include_datasets: bool,
    include_providers: bool,
    include_keywords: bool,
    one_line: bool,
    contains: list[str],
    overwrite_cache: bool,
) -> None:
    catalogue: CopernicusMarineCatalogue = parse_catalogue(
        overwrite_cache=overwrite_cache
    )
    if contains:
        catalogue = filter_catalogue_with_strings(catalogue, contains)

    def default_filter(obj):
        attributes = obj.__dict__
        if not include_description:
            attributes.pop("description", None)
        if not include_datasets:
            attributes.pop("datasets", None)
        if not include_providers:
            attributes.pop("providers", None)
        if not include_keywords:
            attributes.pop("keywords", None)
        return obj.__dict__

    json_dump = (
        dumps(catalogue, default=default_filter)
        if one_line
        else dumps(catalogue, default=default_filter, indent=2)
    )
    click.echo(json_dump)


if __name__ == "__main__":
    cli_group_describe()
