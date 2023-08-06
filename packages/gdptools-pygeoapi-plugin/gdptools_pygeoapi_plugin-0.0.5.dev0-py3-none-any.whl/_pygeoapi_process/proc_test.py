"""Test pocessing."""
import logging
import time
from typing import Any
from typing import Dict
from typing import Tuple

from pygeoapi.process.base import BaseProcessor

LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "test_processing",
    "title": "Timed processing function for testing",
    "description": "Simple processing function for timed duration",
    "keywords": ["process-testing"],
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
        "process_time": {
            "title": "Processing time in seconds",
            "schema": {"type": "int"},
            "minOccurs": 1,
            "maxOccurs": 1,
        },
    },
    "outputs": {
        "completion_string": {
            "title": "Simple string marking completion",
            "schema": {"type": "object", "contentMediaType": "application/json"},
        }
    },
    "example": {"inputs": {"process_time": "10"}},
}


class GDPTimedProcessTest(BaseProcessor):  # type: ignore
    """Generate weights for grid-to-poly aggregation."""

    def __init__(self, processor_def: dict[str, Any]):
        """Initialize Processor.

        Args:
            processor_def (_type_): _description_
        """
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data: Dict[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
        """Execute calc_weights_catalog web service."""
        LOGGER.info("Loading ")
        process_time = int(data["process_time"])
        LOGGER.info("Starting timed sleep")
        time.sleep(process_time)
        LOGGER.info("Ending timed sleep")

        outputs = {"id": "echo", "value": process_time}
        return "application/json", outputs

    def __repr__(self):  # type: ignore
        """Return representation."""
        return f"<GDPTimedProcessTest> {self.name}"
