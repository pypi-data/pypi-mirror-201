"""Calc_weights_catalog_proceess."""
import json
import logging
from typing import Any
from typing import Dict
from typing import Tuple

import geopandas as gpd
from gdptools import ODAPCatData
from gdptools import WeightGen
from pygeoapi.process.base import BaseProcessor

LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "calc_weights_catalog",
    "title": "Calculate weights for area-weighted aggregation",
    "description": "Calculate weights for OpenDAP endpoint and user-defined Features",
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
            "title": "param_json fragment for openDAP catalog",
            "description": (
                "The parameter json fragment associated with the ",
                "openDAP endpoint of user interest",
            ),
            "schema": {"type": "string"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        "grid_dict": {
            "title": "grid_json_string",
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
            "title": "shape_crs_string",
            "schema": {
                "type": "string",
            },
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
        "wght_gen_proj": {
            "title": "Projection string (epsg code or proj string)",
            "schema": {"type": "string"},
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
        "weights": {
            "title": "Comma separated weights, id, i, j, weight",
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
            "wght_gen_proj": "6931",
            "start_date": "1980-01-01",
            "end_date": "1980-12-31",
        }
    },
}


class GDPCalcWeightsCatalogProcessor(BaseProcessor):  # type: ignore
    """Generate weights for grid-to-poly aggregation."""

    def __init__(self, processor_def: dict[str, Any]):
        """Initialize Processor.

        Args:
            processor_def (_type_): _description_
        """
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
        """Execute calc_weights_catalog web service."""
        param_dict = json.loads(str(data["param_dict"]))
        grid_dict = json.loads(str(data["grid_dict"]))
        shpfile_feat = json.loads(str(data["shape_file"]))
        shp_crs = str(data["shape_crs"])
        shp_poly_idx = str(data["shape_poly_idx"])
        wght_gen_proj = str(data["wght_gen_proj"])
        start_date = str(data["start_date"])
        end_date = str(data["end_date"])
        period = [start_date, end_date]

        shp_file = gpd.GeoDataFrame.from_features(shpfile_feat)
        shp_file.set_crs(shp_crs, inplace=True)

        LOGGER.info(f"param_dict: {param_dict}  type: {type(param_dict)}\n")
        LOGGER.info(f"grid_dict: {grid_dict} type: {type(grid_dict)}\n")
        LOGGER.info(f"shp_file: {shp_file.head()} type: {type(shp_file)}\n")
        LOGGER.info(f"shp_poly_idx: {shp_poly_idx} type: {type(shp_poly_idx)}\n")
        LOGGER.info(f"wght_gen_proj: {wght_gen_proj} type: {type(wght_gen_proj)}\n")

        user_data = ODAPCatData(
            param_dict=param_dict,
            grid_dict=grid_dict,
            f_feature=shp_file,
            id_feature=shp_poly_idx,
            period=period,
        )
        wght_gen = WeightGen(
            user_data=user_data, method="serial", output_file="", weight_gen_crs=6931
        )

        wghts = wght_gen.calculate_weights(intersections=True)
        # cp = CatParams(**(json.loads(pjson)))
        # cg = CatGrids(**(json.loads(gjson)))
        # wght = calc_weights_catalog2(
        #     params_json=cp,
        #     grid_json=cg,
        #     shp_file=shp_file,
        #     shp_poly_idx=shp_poly_idx,
        #     wght_gen_proj=wght_gen_proj,
        # )
        wghts.reset_index(inplace=True)
        return "application/json", json.loads(wghts.to_json())

    def __repr__(self):  # type: ignore
        """Return representation."""
        return f"<GDPCalcWeightsCatalogProcessor> {self.name}"
