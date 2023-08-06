"""
   Wrapper around the job class to build a workflow element (production step + job)
"""

__RCSID__ = "$Id$"

# generic imports
from copy import deepcopy
import json

# DIRAC imports
from CTADIRAC.Interfaces.API.CtapipeProcessJob import CtapipeProcessJob
from CTADIRAC.ProductionSystem.Client.WorkflowElement import WorkflowElement


class CtapipeProcessingElement(WorkflowElement):
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        WorkflowElement.__init__(self, parent_prod_step)
        self.job = CtapipeProcessJob(cpuTime=259200.0)
        self.job.setOutputSandbox(["*Log.txt"])
        self.job.input_limit = None
        self.prod_step.Type = "DataReprocessing"
        self.prod_step.Name = "CtapipeProcessing"
        self.mandatory_keys = {"MCCampaign", "configuration_id", "version"}
        self.constrained_job_keys = {"catalogs", "moon", "group_size"}
        self.constrained_input_keys = {
            "pointing_dir",
            "zenith_angle",
            "moon",
            "sct",
            "div_ang",
        }
        self.file_meta_fields = {"nsb", "div_ang", "split"}

    def set_constrained_job_attribute(self, key, value):
        """Set job attribute with constraints"""
        if key == "catalogs":
            # remove whitespaces between catalogs if there are some and separate between commas
            setattr(self.job, key, json.dumps(value.replace(", ", ",").split(sep=",")))
        elif key == "group_size":
            setattr(self.job, key, value)
            self.prod_step.GroupSize = self.job.group_size
        elif key == "moon":
            if value == "dark":
                self.job.output_file_metadata["nsb"] = 1
            elif value == "half":
                self.job.output_file_metadata["nsb"] = 5
            elif value == "full":
                self.job.output_file_metadata["nsb"] = 19

    def set_constrained_input_query(self, key, value):
        """Set input meta query with constraints"""
        if key == "pointing_dir":
            if value == "North":
                self.prod_step.Inputquery["phiP"] = 180
            elif value == "South":
                self.prod_step.Inputquery["phiP"] = 0
        elif key == "zenith_angle":
            self.prod_step.Inputquery["thetaP"] = float(value)
        elif key == "sct":
            self.prod_step.Inputquery["sct"] = str(value)
        elif key == "moon":
            if value == "dark":
                self.prod_step.Inputquery["nsb"] = 1
            elif value == "half":
                self.prod_step.Inputquery["nsb"] = 5
            elif value == "full":
                self.prod_step.Inputquery["nsb"] = 19
        elif key == "div_ang":
            self.prod_step.Inputquery["div_ang"] = str(value)

    def build_job_output_data(self, workflow_step):
        """Build job output meta data"""
        metadata = deepcopy(self.prod_step.Inputquery)
        for key, value in workflow_step["job_config"].items():
            metadata[key] = value
        self.job.set_output_metadata(metadata)

    #############################################################################
