import importlib.resources

import power_markets
import intake

with importlib.resources.path(power_markets, "catalog.yaml") as catalog_path:
    cat = intake.open_catalog(catalog_path.resolve().as_uri())
