"""
  Simple Wrapper on the Job class to run ctapipe merge
"""

__RCSID__ = "$Id$"

# generic imports
import json

# DIRAC imports
from CTADIRAC.Interfaces.API.ProcessingJob import ProcessingJob


class CtapipeMergeJob(ProcessingJob):
    """Job extension class for ctapipe merging"""

    def __init__(self, **kwargs):
        """Constructor"""
        super().__init__(**kwargs)
        self.setType("Merging")
        self.setName("ctapipe_merge")
        self.prog_name = "ctapipe-merge"
        # defaults
        self.output_data_level = 2
        self.output_extension = "merged.DL2.h5"
        self.options = ""

    def set_output_metadata(self, metadata):
        """Set meta data

        Parameters:
        metadata -- metadata dictionary from the telescope simulation
        """
        # # Set directory meta data
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
        # There can be multiple stages of merging
        # For each stage of merging we add +1
        try:
            merged = metadata["merged"]["="]
        except BaseException:
            merged = metadata["merged"]
        self.output_metadata["merged"] = merged + 1
        self.output_metadata["MCCampaign"] = self.MCCampaign

    def set_executable_sequence(self, debug=False):
        """Setup job workflow by defining the sequence of all executables
        All parameters shall have been defined before that method is called.
        """
        i_step = 0
        # step 1 -- debug
        if debug:
            ls_step = self.setExecutable("/bin/ls -alhtr", logFile="LS_Init_Log.txt")
            ls_step["Value"]["name"] = "Step%i_LS_Init" % i_step
            ls_step["Value"]["descr_short"] = "list files in working directory"
            i_step += 1

            env_step = self.setExecutable("/bin/env", logFile="Env_Log.txt")
            env_step["Value"]["name"] = "Step%i_Env" % i_step
            env_step["Value"]["descr_short"] = "Dump environment"
            i_step += 1

        # step 2
        sw_step = self.setExecutable(
            "cta-prod-setup-software",
            arguments="-p %s -v %s -a stage1 -g %s"
            % (self.package, self.version, self.compiler),
            logFile="SetupSoftware_Log.txt",
        )
        sw_step["Value"]["name"] = "Step%i_SetupSoftware" % i_step
        sw_step["Value"]["descr_short"] = "Setup software"
        i_step += 1

        # step 3 run merge
        merge_step = self.setExecutable(
            "./dirac_ctapipe-merge_wrapper",
            arguments=f"--out_ext {self.output_extension} {self.options}",
            logFile="ctapipe_merge_Log.txt",
        )
        merge_step["Value"]["name"] = "Step%i_ctapipe_merge" % i_step
        merge_step["Value"]["descr_short"] = "Run ctapipe merge"
        i_step += 1

        # step 4 set meta data and register Data
        meta_data_json = json.dumps(self.output_metadata)
        file_meta_data_json = json.dumps(self.output_file_metadata)

        # register Data
        data_output_pattern = "./Data/*.h5"  # %self.output_data_level
        dm_step = self.setExecutable(
            "cta-prod-managedata",
            arguments="'%s' '%s' %s '%s' %s %s '%s' Data"
            % (
                meta_data_json,
                file_meta_data_json,
                self.base_path,
                data_output_pattern,
                self.package,
                self.program_category,
                self.catalogs,
            ),
            logFile="DataManagement_Log.txt",
        )
        dm_step["Value"]["name"] = f"Step{i_step}_DataManagement"
        dm_step["Value"][
            "descr_short"
        ] = "Save data files to SE and register them in DFC"
        i_step += 1

        # step 6 failover step
        failover_step = self.setExecutable(
            "/bin/ls -l", modulesList=["Script", "FailoverRequest"]
        )
        failover_step["Value"]["name"] = f"Step{i_step}_Failover"
        failover_step["Value"]["descr_short"] = "Tag files as unused if job failed"
        i_step += 1

        # Step 7 - debug only
        if debug:
            ls_step = self.setExecutable("/bin/ls -Ralhtr", logFile="LS_End_Log.txt")
            ls_step["Value"]["name"] = f"Step{i_step}_LSHOME_End"
            ls_step["Value"]["descr_short"] = "list files in Home directory"
            i_step += 1
