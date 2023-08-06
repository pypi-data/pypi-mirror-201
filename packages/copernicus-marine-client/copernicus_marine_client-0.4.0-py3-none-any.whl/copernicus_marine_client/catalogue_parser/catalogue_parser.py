from copy import deepcopy
from dataclasses import dataclass
from io import StringIO
from itertools import groupby
from multiprocessing.pool import ThreadPool
from typing import List, Tuple
from xml.dom import minidom

import requests
from cachier import cachier
from numpy import arange
from owslib.csw import CatalogueServiceWeb
from owslib.iso import CI_OnlineResource, CI_ResponsibleParty, MD_Metadata


@dataclass
class CopernicusMarineDatasetService:
    protocol: str
    uri: str


@dataclass
class CopernicusMarineProductDataset:
    dataset_id: str
    services: List[CopernicusMarineDatasetService]


@dataclass
class CopernicusMarineProductProvider:
    name: str
    roles: List[str]
    url: str
    email: str


@dataclass
class CopernicusMarineProduct:
    title: str
    product_id: str
    thumbnail: str
    description: str
    providers: List[CopernicusMarineProductProvider]
    created: str
    bbox: List[float]
    temporal_extent: List[str]
    keywords: List[str]
    datasets: List[CopernicusMarineProductDataset]


@dataclass
class CopernicusMarineCatalogue:
    products: List[CopernicusMarineProduct]
    timestamp: str


ENDPOINT = (
    "https://cmems-catalog-ro.cls.fr"
    + "/geonetwork/srv/eng/csw-MYOCEAN-CORE-PRODUCTS"
)
COUNT_ENDPOINT = (
    ENDPOINT
    + "?SERVICE=CSW&REQUEST=GetRecords&VERSION=2.0.2&resultType=hits"
    + "&outputFormat=application/xml"
)
TIMESTAMP_ENDPOINT = (
    ENDPOINT
    + "?SERVICE=CSW&REQUEST=GetRecords&VERSION=2.0.2&resultType=results"
    + "&ElementSetName=full&maxRecords=1&outputSchema=http://www.isotc211.org/2005/gmd"
)
OPENDAP_KEY = "WWW:OPENDAP"
MOTU_KEY = "MYO:MOTU-SUB"
FTP_KEY = "WWW:FTP"


def count_products() -> int:
    """
    Retrieve max number of datasets in csw from csw node
    """
    xml_file = requests.get(COUNT_ENDPOINT, allow_redirects=True)
    csw_header = minidom.parse(StringIO(xml_file.text))
    root = csw_header.documentElement
    search_results = root.getElementsByTagName("csw:SearchResults")[0]
    nproduct_tot = search_results.getAttribute("numberOfRecordsMatched")
    return int(nproduct_tot)


def get_catalogue_timestamp(args=[], kwds={}) -> str:
    """
    Retrieve timestamp of remote catalogue creation
    """
    xml_file = requests.get(TIMESTAMP_ENDPOINT, allow_redirects=True)
    csw_header = minidom.parse(StringIO(xml_file.text))
    root = csw_header.documentElement
    search_results = root.getElementsByTagName("csw:SearchResults")[0]
    dateStamp = search_results.getElementsByTagName("gmd:dateStamp")[0]
    DateTime = dateStamp.getElementsByTagName("gco:DateTime")[0]
    return str(DateTime.firstChild.data)


def parse_catalogue(
    overwrite_cache: bool = False,
) -> CopernicusMarineCatalogue:
    return _parse_catalogue(overwrite_cache=overwrite_cache)


@cachier(hash_params=get_catalogue_timestamp)
def _parse_catalogue() -> CopernicusMarineCatalogue:
    def get_csw_records(slicing_tuple: Tuple[int, int]) -> List[MD_Metadata]:
        """
        Launch csw requests in parallel and gather all results in list
        """
        ndatasets, start_position = slicing_tuple
        csw = CatalogueServiceWeb(ENDPOINT, timeout=60)
        csw.getrecords2(
            esn="full",
            outputschema="http://www.isotc211.org/2005/gmd",
            startposition=start_position,
            maxrecords=ndatasets,
        )
        csw_records: List[MD_Metadata] = csw.records.values()
        return csw_records

    pool = ThreadPool()
    nproduct_per_page, nproduct_tot = 10, count_products()
    start_positions = arange(1, nproduct_tot, nproduct_per_page, dtype=int)
    results = pool.map(
        get_csw_records,
        zip([nproduct_per_page] * len(start_positions), start_positions),
    )
    products: List[CopernicusMarineProduct] = [
        product
        for csw_records in results
        for product in list(map(record_to_product, csw_records))
    ]
    return CopernicusMarineCatalogue(
        products=sorted(products, key=lambda product: product.title),
        timestamp=get_catalogue_timestamp(),
    )


def record_to_product(csw_record: MD_Metadata) -> CopernicusMarineProduct:
    return CopernicusMarineProduct(
        title=csw_record.identification.title,
        product_id=csw_record.identification.alternatetitle,
        thumbnail=csw_record.identification.graphicoverview[0],
        description="".join(csw_record.identification.abstract),
        providers=get_providers(csw_record),
        created=get_created(csw_record),
        bbox=get_bounding_box(csw_record),
        temporal_extent=get_temporal_extent(csw_record),
        keywords=get_keywords(csw_record),
        datasets=record_datasets(csw_record.distribution.online),
    )


def get_created(csw_record: MD_Metadata) -> str:
    return csw_record.identification.date[0].date


def get_bounding_box(csw_record: MD_Metadata) -> List[float]:
    return [
        csw_record.identification.extent.boundingBox.minx,
        csw_record.identification.extent.boundingBox.miny,
        csw_record.identification.extent.boundingBox.maxx,
        csw_record.identification.extent.boundingBox.maxy,
    ]


def get_temporal_extent(csw_record: MD_Metadata) -> List[str]:
    return [
        csw_record.identification.temporalextent_start,
        csw_record.identification.temporalextent_end,
    ]


def get_keywords(csw_record: MD_Metadata) -> List[str]:
    return list(
        map(
            lambda keyword: keyword.thesaurus["title"],
            csw_record.identification.keywords2,
        )
    )


def get_providers(
    csw_record: MD_Metadata,
) -> List[CopernicusMarineProductProvider]:
    def to_provider(
        responsible_party: CI_ResponsibleParty,
    ) -> CopernicusMarineProductProvider:
        return CopernicusMarineProductProvider(
            name=responsible_party.organization,
            roles=[responsible_party.role],
            url=responsible_party.onlineresource,
            email=responsible_party.email,
        )

    return list(map(to_provider, csw_record.identification.contact))


def record_datasets(
    online_resources: List[CI_OnlineResource],
) -> List[CopernicusMarineProductDataset]:
    online_resources_by_name = groupby(
        (
            online_resource
            for online_resource in online_resources
            if online_resource.name
        ),
        lambda online_resource: online_resource.name,
    )

    def to_service(
        online_resource: CI_OnlineResource,
    ) -> CopernicusMarineDatasetService:
        return CopernicusMarineDatasetService(
            protocol=online_resource.protocol, uri=online_resource.url
        )

    def to_dataset(
        item: Tuple[str, CI_OnlineResource]
    ) -> CopernicusMarineProductDataset:
        return CopernicusMarineProductDataset(
            dataset_id=item[0],
            services=sorted(
                map(to_service, item[1]), key=lambda service: service.protocol
            ),
        )

    return sorted(
        map(to_dataset, online_resources_by_name),
        key=lambda dataset: dataset.dataset_id,
    )


def get_dataset_from_id(
    catalogue: CopernicusMarineCatalogue, dataset_id: str
) -> CopernicusMarineProductDataset:
    for product in catalogue.products:
        for dataset in product.datasets:
            if dataset_id == dataset.dataset_id:
                return dataset
    raise KeyError(
        f"The requested dataset '{dataset_id}' was not found in the catalogue, "
        "you can use 'copernicus-marine describe --include-datasets "
        "-c <search_token>' to find the dataset id"
    )


def get_product_from_url(
    catalogue: CopernicusMarineCatalogue, dataset_url: str
) -> CopernicusMarineProduct:
    """
    Return the product object, with its dataset list filtered
    """
    return filter_catalogue_with_strings(catalogue, [dataset_url]).products[0]


def get_protocol_from_url(dataset_url) -> str:
    if dataset_url.startswith("ftp://"):
        protocol = "WWW:FTP"
    elif "/motu-web/Motu" in dataset_url:
        protocol = "MYO:MOTU-SUB"
    elif "/wms/" in dataset_url:
        protocol = "OGC:WMS:getCapabilities"
    elif "/thredds/dodsC/" in dataset_url:
        protocol = "WWW:OPENDAP"
    else:
        raise ValueError(f"No protocol matching url: {dataset_url}")
    return protocol


def get_protocol_url_from_id(
    dataset_id: str, PROTOCOL_KEYS_ORDER: List[str]
) -> Tuple[str, str]:
    catalogue = parse_catalogue()
    dataset_urls = (
        get_dataset_url_from_id(catalogue, dataset_id, protocol)
        for protocol in PROTOCOL_KEYS_ORDER
    )
    try:
        dataset_url = next(filter(lambda dataset: dataset, dataset_urls))
        protocol = get_protocol_from_url(dataset_url)
    except StopIteration:
        raise KeyError(
            f"Dataset {dataset_id} does not have a valid protocol "
            f"for subset function. Available protocols: {PROTOCOL_KEYS_ORDER}"
        )
    return protocol, dataset_url


def get_service_url(
    dataset: CopernicusMarineProductDataset, protocol: str
) -> str:
    service_urls = iter(
        [
            service.uri
            for service in dataset.services
            if service.protocol == protocol
        ]
    )
    return next(service_urls, "")


def get_dataset_url_from_id(
    catalogue: CopernicusMarineCatalogue, dataset_id: str, protocol: str
) -> str:
    dataset = get_dataset_from_id(catalogue, dataset_id)
    return get_service_url(dataset, protocol)


def filter_catalogue_with_strings(
    catalogue: CopernicusMarineCatalogue, tokens: list[str]
) -> CopernicusMarineCatalogue:
    filtered_catalogue = deepcopy(catalogue)
    return find_match_object(filtered_catalogue, tokens)


def find_match_object(obj, tokens):
    if any(
        token in val
        for val in obj.__dict__.values()
        if val
        for token in tokens
    ):
        return obj
    else:
        match_dict, is_match = {}, False
        for key, val in obj.__dict__.items():
            if isinstance(val, list):
                match_list = find_match_list(val, tokens)
                if match_list:
                    is_match = True
                    match_dict[key] = match_list
                else:
                    match_dict[key] = val
            elif hasattr(val, "__dict__"):
                match_object = find_match_object(val, tokens)
                is_match = True if match_object else False
                match_dict[key] = val
            else:
                match_dict[key] = val
        if is_match:
            obj.__dict__ = match_dict
            return obj
        else:
            return None


def find_match_list(search_list, tokens):
    match_list = []
    for element in search_list:
        if hasattr(element, "__dict__"):
            match_list.append(find_match_object(element, tokens))
        elif any(token in element for token in tokens if element):
            match_list.append(element)
        else:
            pass
    match_list = [match for match in match_list if match]
    return match_list
