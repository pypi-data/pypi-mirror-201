"""
   Wrapper around the job class to build a workflow element (production step + job)
"""

__RCSID__ = "$Id$"

# generic imports
import json
from copy import deepcopy

# DIRAC imports
import DIRAC
from CTADIRAC.Interfaces.API.MCPipeNSBJob import MCPipeNSBJob
from CTADIRAC.ProductionSystem.Client.WorkflowElement import WorkflowElement


class SimulationElement(WorkflowElement):
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        WorkflowElement.__init__(self, parent_prod_step)
        self.job = MCPipeNSBJob()
        self.job.setOutputSandbox(["*Log.txt"])
        self.prod_step.Type = "MCSimulation"
        self.prod_step.Name = "MCSimulation"
        self.mandatory_keys = {"MCCampaign", "configuration_id", "version"}
        self.constrained_job_keys = {
            "version",
            "catalogs",
            "sct",
            "particle",
            "pointing_dir",
            "moon",
            "magic",
            "div_ang",
        }
        self.file_meta_fields = {"nsb", "div_ang"}

    def set_constrained_job_attribute(self, key, value):
        """Set job attribute with constraints"""
        if key == "catalogs":
            # remove whitespaces between catalogs if there are some and separate between commas
            setattr(self.job, key, json.dumps(value.replace(", ", ",").split(sep=",")))
        elif key == "version":
            if "-sc" not in str(
                value
            ):  # if the version has not already been set by 'sct'
                self.job.version = str(value)
        elif key == "particle":
            self.job.set_particle(value)
        elif key == "pointing_dir":
            self.job.set_pointing_dir(value)
        elif key == "sct":
            self.job.set_sct(value)
        elif key == "moon":
            self.job.set_moon(value.replace(", ", ",").split(sep=","))
        elif key == "magic":
            self.job.set_magic(value)
        elif key == "div_ang":
            self.job.set_div_ang(value)

    def build_input_data(self, workflow_config, workflow_step):
        """Simulation Elements do not have input data"""
        self.prod_step.Inputquery = {}

    def build_job_input_data(self, mode):
        """Simulation Elements do not have input data"""
        pass

    def build_output_data(self):
        """Build output data from the job metadata and the metadata added on the files"""
        self.prod_step.Outputquery = deepcopy(self.job.output_metadata)
        for key, value in self.job.output_file_metadata.items():
            if isinstance(value, list):
                if len(value) > 1:
                    self.prod_step.Outputquery[key] = {"in": value}
                else:
                    self.prod_step.Outputquery[key] = value[0]
            else:
                self.prod_step.Outputquery[key] = value

    #############################################################################
