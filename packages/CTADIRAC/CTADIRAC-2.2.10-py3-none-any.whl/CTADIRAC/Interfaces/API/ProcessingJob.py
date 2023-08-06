"""
  Simple Wrapper on the Job class to handle ctapipe processing applications
"""

__RCSID__ = "$Id$"

# generic imports
import json
import collections

# DIRAC imports
from DIRAC.Interfaces.API.Job import Job


class ProcessingJob(Job):
    """Job extension class for ctapipe processing"""

    def __init__(self, cpuTime=432000):
        """Constructor

        Keyword arguments:
        cpuTime -- max cpu time allowed for the job
        """
        super().__init__()
        self.setCPUTime(cpuTime)
        # defaults
        self.setName("ctapipe")
        self.package = "ctapipe"
        self.version = "v0.10.0"
        self.compiler = "gcc48_default"
        self.program_category = "analysis"
        self.output_metadata = collections.OrderedDict()
        self.output_file_metadata = collections.OrderedDict()
        self.catalogs = json.dumps(["DIRACFileCatalog", "TSCatalog"])
        # to be redefined in the derived classes
        self.prog_name = "ctapipe-process"
        self.configuration_id = 1
        self.output_data_level = 1
        self.MCCampaign = "ProdTest"

    def set_output_metadata(self, metadata):
        """Set output metadata

        Parameters:
        metadata -- metadata dictionary from telescope simulation
        """
        # # Set directory meta data
        self.output_metadata = collections.OrderedDict()
        self.output_metadata["array_layout"] = metadata["array_layout"]
        self.output_metadata["site"] = metadata["site"]
        self.output_metadata["particle"] = metadata["particle"]
        try:
            phiP = metadata["phiP"]["="]
        except BaseException:
            phiP = metadata["phiP"]
        self.output_metadata["phiP"] = phiP
        try:
            thetaP = metadata["thetaP"]["="]
        except BaseException:
            thetaP = metadata["thetaP"]
        self.output_metadata["thetaP"] = thetaP
        if metadata.get("sct"):
            self.output_metadata["sct"] = metadata["sct"]
        self.output_metadata[self.program_category + "_prog"] = self.prog_name
        self.output_metadata[self.program_category + "_prog_version"] = self.version
        self.output_metadata["data_level"] = self.output_data_level
        self.output_metadata["configuration_id"] = self.configuration_id
        self.output_metadata["merged"] = 0
        self.output_metadata["MCCampaign"] = self.MCCampaign
