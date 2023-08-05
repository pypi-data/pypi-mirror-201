import arklog
from spendpoint.endpoint import SparqlEndpoint
from spendpoint import __version__
from spendpoint.service import outlier_service, example_service, conversion_service

arklog.set_config_logging()

functions = {
    "https://ontology.rys.app/dt/function/outlier": outlier_service,
    "https://ontology.rys.app/dt/function/example": example_service,
    "https://ontology.rys.app/dt/function/conversion": conversion_service,
}

app = SparqlEndpoint(
    version = __version__,
    functions = functions,
    title = "SPARQL endpoint for storage and services",
    description = "\n".join((
        "SPARQL endpoint.",
        f"Supports {len(functions)} custom services:",
        *(f" - {service_uri}" for service_uri, fc in functions.items()))
    )
)
