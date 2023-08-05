"""
  Simple Wrapper on the Job class to run a ctapipe-process job
"""

__RCSID__ = "$Id$"

# generic imports
import json

# DIRAC imports
from CTADIRAC.Interfaces.API.ProcessingJob import ProcessingJob


class CtapipeProcessJob(ProcessingJob):
    """Job extension class for ctapipe stage1 modeling processing"""

    def __init__(self, **kwargs):
        """Constructor"""
        super().__init__(**kwargs)
        self.setName("ctapipe_process")
        self.setType("DL0_Reprocessing")
        self.prog_name = "ctapipe-process"
        # defaults
        self.options = ""
        self.output_data_level = 2

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

        # step 3 run stage1
        proc_step = self.setExecutable(
            "./dirac_ctapipe-process_wrapper",
            arguments=f"{self.options}",
            logFile="ctapipe_process_Log.txt",
        )
        proc_step["Value"]["name"] = "Step%i_ctapipe_process" % i_step
        proc_step["Value"]["descr_short"] = "Run ctapipe process"
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

        # step 5 register Log
        log_file_pattern = "./Data/*.log_and_prov.tgz"
        file_meta_data = {}
        file_meta_data_json = json.dumps(file_meta_data)
        log_step = self.setExecutable(
            "cta-prod-managedata",
            arguments="'%s' '%s' %s '%s' %s %s '%s' Log"
            % (
                meta_data_json,
                file_meta_data_json,
                self.base_path,
                log_file_pattern,
                self.package,
                self.program_category,
                self.catalogs,
            ),
            logFile="LogManagement_Log.txt",
        )
        log_step["Value"]["name"] = f"Step{i_step}_LogManagement"
        log_step["Value"]["descr_short"] = "Save log to SE and register them in DFC"
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
