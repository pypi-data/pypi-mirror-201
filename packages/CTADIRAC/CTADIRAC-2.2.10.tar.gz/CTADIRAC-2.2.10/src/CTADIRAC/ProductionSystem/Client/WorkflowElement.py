"""
   Wrapper around the job class to build a workflow element (production step + job)
"""

__RCSID__ = "$Id$"

# generic imports
import json
from copy import deepcopy


# DIRAC imports
import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.ProductionSystem.Client.ProductionStep import ProductionStep
from CTADIRAC.Core.Utilities.tool_box import get_dataset_MQ
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient


class WorkflowElement:
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        self.job = Job()
        self.prod_step = ProductionStep()
        self.prod_step.ParentStep = parent_prod_step
        self.fc = FileCatalogClient()
        self.mandatory_keys = {""}
        self.constrained_job_keys = {""}
        self.constrained_input_keys = {""}
        self.file_meta_fields = {""}

    def set_constrained_job_attribute(self, key, value):
        """Set job attribute with constraints"""
        setattr(self.job, key, value)

    def set_constrained_input_query(self, key, value):
        """Set input meta query with constraints"""
        self.prod_step.Inputquery[key] = value

    def build_job_attributes_from_job_config(self, workflow_step):
        """Build job attributes with job_config values"""
        for key, value in workflow_step["job_config"].items():
            if value is not None:
                if key in self.constrained_job_keys:
                    self.set_constrained_job_attribute(key, value)
                elif key in self.file_meta_fields:
                    self.job.output_file_metadata[key] = value
                else:
                    setattr(self.job, key, value)
            elif key in self.mandatory_keys:
                DIRAC.gLogger.error("%s is mandatory" % key)
                DIRAC.exit(-1)

    def build_job_attributes_from_common(self, workflow_config):
        """Build job attributes concerning the whole production"""
        for key, value in workflow_config["Common"].items():
            if value is not None:
                setattr(self.job, key, value)
            elif key in self.mandatory_keys:
                DIRAC.gLogger.error("%s is mandatory" % key)
                DIRAC.exit(-1)

    def build_job_attributes_from_input(self):
        """Set job attributes from input meta query"""
        for key, value in self.prod_step.Inputquery.items():
            if key in self.file_meta_fields:
                try:
                    self.job.output_file_metadata[key] = value["="]
                except BaseException:
                    self.job.output_file_metadata[key] = value
            else:
                try:
                    setattr(self.job, key, value["="])
                except BaseException:
                    setattr(self.job, key, value)

    def build_job_attributes(self, workflow_config, workflow_step):
        """Set job attributes"""
        self.build_job_attributes_from_input()
        self.build_job_attributes_from_common(workflow_config)
        self.build_job_attributes_from_job_config(workflow_step)

    def build_input_data(self, workflow_config, workflow_step):
        """Build input data"""
        self.prod_step.Inputquery = {}
        if self.prod_step.ParentStep:
            self.prod_step.Inputquery = self.prod_step.ParentStep.Outputquery
        else:
            if workflow_step["input_meta_query"].get("dataset"):
                self.prod_step.Inputquery = get_dataset_MQ(
                    workflow_step["input_meta_query"]["dataset"]
                )

        # refine parent MQ by adding extra specification if needed
        for key, value in workflow_step["input_meta_query"].items():
            if value is not None:
                if key in self.constrained_input_keys:
                    self.set_constrained_input_query(key, value)
                elif (key != "dataset") and (key != "parentID"):
                    self.prod_step.Inputquery[key] = value

    def build_job_input_data(self, mode):
        """Limit the nb of input data to process (for testing purpose)"""
        res = self.fc.findFilesByMetadata(dict(self.prod_step.Inputquery))
        if not res["OK"]:
            DIRAC.gLogger.error(res["Message"])
            DIRAC.exit(-1)
        input_data_limit = self.job.input_limit
        input_data = res["Value"][:input_data_limit]
        if mode.lower() in ["wms", "local"]:
            self.job.setInputData(input_data)
        if not input_data and mode.lower() == "wms":
            DIRAC.gLogger.error("No job submitted: job must have input data")
            DIRAC.exit(-1)
        if mode.lower() == "ps" and self.job.input_limit:
            f = open("test_input_data.list", "w")
            for lfn in input_data:
                f.write(lfn + "\n")
            f.close()
            DIRAC.gLogger.notice("\t\tInput limit found: %d files dumped to test_input_data.list" % len(input_data))
            self.prod_step.Inputquery = {}

    def build_element_config(self):
        """Set job and production step attributes specific to the configuration"""
        self.job.set_executable_sequence(debug=False)
        self.prod_step.Body = self.job.workflow.toXML()

    def build_job_output_data(self, workflow_step):
        """Build job output meta data"""
        self.job.set_output_metadata()

    def build_output_data(self):
        """Build output data from the job metadata and the metadata added on the files"""
        self.prod_step.Outputquery = deepcopy(self.job.output_metadata)
        for key, value in self.job.output_file_metadata.items():
            self.prod_step.Outputquery[key] = value


#############################################################################
