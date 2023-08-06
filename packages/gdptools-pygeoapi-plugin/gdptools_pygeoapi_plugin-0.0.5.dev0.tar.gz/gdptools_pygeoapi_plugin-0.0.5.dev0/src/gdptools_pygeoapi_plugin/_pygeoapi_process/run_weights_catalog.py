"""Calc_weights_catalog_proceess."""
import json
import logging
import tempfile
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Tuple

import geopandas as gpd
import pandas as pd
from gdptools import AggGen
from gdptools import ODAPCatData
from pygeoapi.process.base import BaseProcessor

LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "run_weights_catalog",
    "title": "run area-weighted aggregation",
    "description": """Run area-weighted aggredation using  OpenDAP endpoint and
        user-defined Features""",
    "keywords": ["area-weighted intersections"],
    "links": [
        {
            "type": "text/html",
            "rel": "canonical",
            "title": "information",
            "href": "https://example.org/process",
            "hreflang": "en-CA",
        }
    ],
    "inputs": {
        "param_dict": {
            "title": "param_dict",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "grid_dict": {
            "title": "grid_dict",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "weights": {
            "title": "weights_json_string",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_file": {
            "title": "shape_file_json_string",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_crs": {
            "title": "shape_file_crs_string",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "shape_poly_idx": {
            "title": "shape_poly_idx_string",
            "schema": {
                "type": "string",
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "start_date": {
            "title": "Beginning date to pull from openDAP endpoint",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "end_date": {
            "title": "Ending date to pull from openDAP endpoint",
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
    },
    "outputs": {
        "aggregated_json": {
            "title": "json records file of aggregated values",
            "schema": {"type": "object", "contentMediaType": "application/json"},
        }
    },
    "example": {
        "inputs": {
            "param_dict": (
                '{"aet": {"id": "terraclim", "grid_id": 116.0, "URL":'
                ' "http://thredds.northwestknowledge.net:8080/thredds/dodsC/'
                'agg_terraclimate_aet_1958_CurrentYear_GLOBE.nc", "tiled": "", '
                '"variable": "aet", "varname": "aet", "long_name": '
                '"water_evaporation_amount", "T_name": "time", "duration": '
                '"1958-01-01/2020-12-01", "interval": "1 months", "nT": 756.0, '
                '"units": "mm", "model": NaN, "ensemble": NaN, "scenario": "total"}, '
                '"pet": {"id": "terraclim", "grid_id": 116.0, "URL": '
                '"http://thredds.northwestknowledge.net:8080/thredds/dodsC/'
                'agg_terraclimate_pet_1958_CurrentYear_GLOBE.nc", "tiled": "", '
                '"variable": "pet", "varname": "pet", "long_name": '
                '"water_potential_evaporation_amount", "T_name": "time", "duration": '
                '"1958-01-01/2020-12-01", "interval": "1 months", "nT": 756.0, "units":'
                '  "mm", "model": NaN, "ensemble": NaN, "scenario": "total"}, '
                '"PDSI": {"id": "terraclim", "grid_id": 116.0, "URL": '
                '"http://thredds.northwestknowledge.net:8080/thredds/dodsC/'
                'agg_terraclimate_PDSI_1958_CurrentYear_GLOBE.nc", "tiled": "", '
                '"variable": "PDSI", "varname": "PDSI", "long_name": '
                '"palmer_drought_severity_index", "T_name": "time", "duration": '
                '"1958-01-01/2020-12-01", "interval": "1 months", "nT": 756.0, '
                '"units": "unitless", "model": NaN, "ensemble": NaN, "scenario": '
                '"total"}}'
            ),
            "grid_dict": (
                '{"aet": {"grid_id": 116.0, "X_name": "lon", "Y_name": "lat", '
                '"X1": -179.9792, "Xn": 179.9792, "Y1": 89.9792, "Yn": -89.9792, '
                '"resX": 0.0417, "resY": 0.0417, "ncols": 8640, "nrows": 4320, "proj": '
                '"+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs", '
                '"toptobottom": 0.0, "tile": NaN, "grid.id": NaN}, '
                '"pet": {"grid_id": 116.0, "X_name": "lon", "Y_name": "lat", '
                '"X1": -179.9792, "Xn": 179.9792, "Y1": 89.9792, "Yn": -89.9792, '
                '"resX": 0.0417, "resY": 0.0417, "ncols": 8640, "nrows": 4320, "proj": '
                '"+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs", '
                '"toptobottom": 0.0, "tile": NaN, "grid.id": NaN}, '
                '"PDSI": {"grid_id": 116.0, "X_name": "lon", "Y_name": "lat", '
                '"X1": -179.9792, "Xn": 179.9792, "Y1": 89.9792, "Yn": -89.9792, '
                '"resX": 0.0417, "resY": 0.0417, "ncols": 8640, "nrows": 4320, "proj": '
                '"+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs", '
                '"toptobottom": 0.0, "tile": NaN, "grid.id": NaN}}'
            ),
            "weights": (
                '{"i":{"0":2,"1":1,"2":2,"3":1},'
                '"index":{"0":0,"1":1,"2":2,"3":3},'
                '"j":{"0":3,"1":3,"2":2,"3":2},'
                '"poly_idx":{"0":"1","1":"1","2":"1","3":"1"},'
                '"wght":{'
                '"0":0.138616567,"1":0.001795472,"2":0.7689606915,"3":0.0906272694}}'
            ),
            "shape_file": (
                '{"type": "FeatureCollection", "features": ['
                '{"id": "0", "type": "Feature", "properties": {'
                '"id": 1, "poly_idx": "1"}, "geometry": {'
                '"type": "Polygon", "coordinates": [['
                "[-70.60141212297273, 41.9262774500321], "
                "[-70.57199544021768, 41.91303994279233], "
                "[-70.5867037815952, 41.87626908934851], "
                "[-70.61906213262577, 41.889506596588284], "
                "[-70.60141212297273, 41.9262774500321]"
                "]]}}]}"
            ),
            "shape_crs": "4326",
            "shape_poly_idx": "poly_idx",
            "start_date": "1980-01-01",
            "end_date": "1980-12-31",
        }
    },
}


class GDPRunWeightsCatalogProcessor(BaseProcessor):  # type: ignore
    """Run area-weighted grid-to-poly aggregation."""

    def __init__(self, processor_def: dict[str, Any]):
        """Initialize Processor.

        Args:
            processor_def (_type_): _description_
        """
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
        """Execute run_weights_catalog web service."""
        param_dict = json.loads(str(data["param_dict"]))
        grid_dict = json.loads(str(data["grid_dict"]))
        wghts = json.loads(str(data["weights"]))
        shpfile_feat = json.loads(str(data["shape_file"]))
        shp_crs = str(data["shape_crs"])
        shp_poly_idx = str(data["shape_poly_idx"])
        start_date = str(data["start_date"])
        end_date = str(data["end_date"])
        period = [start_date, end_date]

        weights = pd.DataFrame.from_dict(wghts)
        shp_file = gpd.GeoDataFrame.from_features(shpfile_feat)
        shp_file.set_crs(shp_crs, inplace=True)

        LOGGER.info(f"param_dict: {param_dict}  type: {type(param_dict)}\n")
        LOGGER.info(f"grid_dict: {grid_dict} type: {type(grid_dict)}\n")
        LOGGER.info(f"weights: {weights} type: {type(weights)}\n")
        LOGGER.info(f"shp_file: {shp_file.head()} type: {type(shp_file)}\n")
        LOGGER.info(f"shp_poly_idx: {shp_poly_idx} type: {type(shp_poly_idx)}\n")
        LOGGER.info(f"start_date: {start_date} type: {type(start_date)}\n")
        LOGGER.info(f"end_date: {end_date} type: {type(end_date)}\n")

        user_data = ODAPCatData(
            param_dict=param_dict,
            grid_dict=grid_dict,
            f_feature=shp_file,
            id_feature=shp_poly_idx,
            period=period,
        )
        tempdir = tempfile.TemporaryDirectory()
        agg_gen = AggGen(
            user_data=user_data,
            stat_method="masked_average",
            agg_engine="serial",
            agg_writer="json",
            out_path=tempdir.name,
            file_prefix="temp_outfile",
            weights=weights,
        )
        ngdf, nvals = agg_gen.calculate_agg()

        ofile = Path(tempdir.name) / "temp_outfile.json"

        df = pd.read_json(ofile)
        return "application/json", df.to_json(orient="records", date_format="iso")

    def __repr__(self):  # type: ignore
        """Return representation."""
        return f"<GDPCalcWeightsCatalogProcessor> {self.name}"
