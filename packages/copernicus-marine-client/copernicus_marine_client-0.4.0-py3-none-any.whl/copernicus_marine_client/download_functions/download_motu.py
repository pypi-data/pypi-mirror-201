from datetime import datetime
from subprocess import run
from typing import List, Optional, Tuple

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineCatalogue,
    get_product_from_url,
    parse_catalogue,
)


def parse_motu_dataset_url(data_path: str) -> str:
    host = data_path.split("/motu-web/Motu")[0] + "/motu-web/Motu"
    return host


def download_motu(
    dataset_url: str,
    dataset_id: str,
    login: str,
    password: str,
    variables: List[str],
    geographical_subset: Tuple[float, float, float, float],
    temporal_subset: Tuple[datetime, datetime],
    depth_range: Tuple[float, float],
    output_path: str,
    output_file: Optional[str],
    catalogue: Optional[CopernicusMarineCatalogue],
):
    if not catalogue:
        catalogue = parse_catalogue()
    product = get_product_from_url(catalogue, dataset_url)
    product_id = product.product_id
    if not dataset_id:
        dataset_id = product.datasets[0].dataset_id
    if not output_file:
        output_file = "data.nc"
    if not output_path:
        output_path = "."
    options_list = [
        "--motu",
        parse_motu_dataset_url(dataset_url),
        "--service-id",
        product_id + "-TDS",
        "--product-id",
        dataset_id,
        "--out-dir",
        output_path,
        "--out-name",
        output_file,
        "--user",
        login,
        "--pwd",
        password,
    ]

    if geographical_subset:
        options_list.extend(
            [
                "--longitude-min",
                str(geographical_subset[2]),
                "--longitude-max",
                str(geographical_subset[3]),
                "--latitude-min",
                str(geographical_subset[0]),
                "--latitude-max",
                str(geographical_subset[1]),
            ]
        )
    if temporal_subset:
        options_list.extend(
            [
                "--date-min",
                str(temporal_subset[0]),
                "--date-max",
                str(temporal_subset[1]),
            ]
        )
    if depth_range:
        options_list.extend(
            [
                "--depth-min",
                str(depth_range[0]),
                "--depth-max",
                str(depth_range[1]),
            ]
        )
    options_list.extend(
        [flat for var in variables for flat in ["--variable", var]]
    )

    run(
        [
            "motuclient",
        ]
        + options_list
    )
