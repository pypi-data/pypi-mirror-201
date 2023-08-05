"""
  New job class to run Prod6 Divergent simulations
  This is similar to the parallel Prod6 simulations and inherits from it but with a divergent option.
  The divergent angles are hardcoded everywhere and also here.
          OG, Dec 2022
"""

__RCSID__ = "$Id$"

# generic imports
import json
import collections

# DIRAC imports
from DIRAC import gLogger
from CTADIRAC.Interfaces.API.Prod6MCPipeNSBJob import Prod6MCPipeNSBJob


class Prod6MCPipeDivergentJob(Prod6MCPipeNSBJob):
    """Job extension class for Prod6 MC Divergent simulations"""

    def __init__(self, cpu_time=259200):
        """Constructor takes almosst everything from base class

        Keyword arguments:
        cpuTime -- max cpu time allowed for the job
        """
        Prod6MCPipeNSBJob.__init__(self, cpu_time)
        self.catalogs = json.dumps(["DIRACFileCatalog"])
        self.metadata = collections.OrderedDict()

    def set_half_moon(self, half_moon=False):
        """Set if to simulate with half-moon conditions

        Parameters:
        half_moon -- a boolean for simulating with full moon conditions
        """
        if half_moon is True:
            gLogger.info("Set simulations with half-moon conditions")
            self.half_moon = "--with-half-moon"
        else:
            self.half_moon = ""  # We alawys at least run with half moon

    def setupWorkflow(self, debug=False):
        """Override the base class job workflow to adapt to divergent simulations
        All parameters shall have been defined before that method is called.
        """
        # step 1 - debug only
        i_step = 1
        if debug:
            ls_step = self.setExecutable("/bin/ls -alhtr", logFile="LS_Init_Log.txt")
            ls_step["Value"]["name"] = "Step%i_LS_Init" % i_step
            ls_step["Value"]["descr_short"] = "list files in working directory"

            env_step = self.setExecutable("/bin/env", logFile="Env_Log.txt")
            env_step["Value"]["name"] = "Step%i_Env" % i_step
            env_step["Value"]["descr_short"] = "Dump environment"
            i_step += 1

        # step 2 : use new CVMFS repo
        sw_step = self.setExecutable(
            "cta-prod-setup-software",
            arguments="-p %s -v %s -a simulations -g %s"
            % (self.package, self.version, self.compiler),
            logFile="SetupSoftware_Log.txt",
        )
        sw_step["Value"]["name"] = "Step%i_SetupSoftware" % i_step
        sw_step["Value"]["descr_short"] = "Setup software"
        i_step += 1
        # step 3 run corsika+sim_telarray
        prod_exe = "./dirac_prod6_run"
        prod_args = (
            "--start_run %s --run %s --sequential --divergent %s %s %s %s %s %s %s"
            % (
                self.start_run_number,
                self.run_number,
                self.half_moon,
                self.with_sct,
                self.with_magic,
                self.cta_site,
                self.particle,
                self.pointing_dir,
                self.zenith_angle,
            )
        )

        cs_step = self.setExecutable(
            prod_exe, arguments=prod_args, logFile="CorsikaSimtel_Log.txt"
        )
        cs_step["Value"]["name"] = "Step%i_CorsikaSimtel" % i_step
        cs_step["Value"]["descr_short"] = "Run Corsika piped into simtel"
        i_step += 1

        # step 4 - debug only
        if debug:
            ls_step = self.setExecutable("/bin/ls -Ralhtr", logFile="LS_End_Log.txt")
            ls_step["Value"]["name"] = "Step%i_LS_End" % i_step
            ls_step["Value"][
                "descr_short"
            ] = "list files in working directory and sub-directory"
            i_step += 1

        # step 5  verify the number of events in the simtel file and define meta data, upload file on SE and register in catalogs
        self.set_meta_data()
        md_json = json.dumps(self.metadata)

        i_substep = 0
        for div_ang in ["0.0022", "0.0043", "0.008", "0.01135", "0.01453"]:
            data_output_pattern = f"Data/*-div{div_ang}*-dark*.simtel.zst"

            # verify the number of events in the simtel file
            mgv_step = self.setExecutable(
                "dirac_simtel_check",
                arguments=f"'{data_output_pattern}'",
                logFile=f"Verify_n_showers_div{div_ang}_Log.txt",
            )
            mgv_step["Value"]["name"] = f"Step{i_step}.{i_substep}_VerifyNShowers"
            mgv_step["Value"]["descr_short"] = "Verify number of showers"

            i_substep += 1

            # define meta data, upload file on SE and register in catalogs

            # Upload and register data
            file_meta_data = {
                "runNumber": self.run_number,
                "nsb": 1,
                "div_ang": div_ang,
            }  # adding a new meta data field
            file_md_json = json.dumps(file_meta_data)

            dm_step = self.setExecutable(
                "cta-prod-managedata",
                arguments="'%s' '%s' %s '%s' %s %s '%s' Data"
                % (
                    md_json,
                    file_md_json,
                    self.base_path,
                    data_output_pattern,
                    self.package,
                    self.program_category,
                    self.catalogs,
                ),
                logFile=f"DataManagement_div{div_ang}_Log.txt",
            )
            dm_step["Value"]["name"] = f"Step{i_step}.{i_substep}_DataManagement"
            dm_step["Value"][
                "descr_short"
            ] = "Save data files to SE and register them in DFC"

            i_substep += 1

            # Upload and register log_and_hist file
            file_meta_data = {}
            file_md_json = json.dumps(file_meta_data)
            log_file_pattern = f"Data/*-div{div_ang}*-dark*.log_hist.tar"
            log_step = self.setExecutable(
                "cta-prod-managedata",
                arguments="'%s' '%s' %s '%s' %s %s '%s' Log"
                % (
                    md_json,
                    file_md_json,
                    self.base_path,
                    log_file_pattern,
                    self.package,
                    self.program_category,
                    self.catalogs,
                ),
                logFile=f"LogManagement_div{div_ang}_Log.txt",
            )
            log_step["Value"]["name"] = f"Step{i_step}.{i_substep}_LogManagement"
            log_step["Value"]["descr_short"] = "Save log to SE and register them in DFC"

            i_substep += 1

            # Now switching to half moon NSB
            if self.half_moon:
                # Upload and register data - NSB=5 half moon
                file_meta_data = {
                    "runNumber": self.run_number,
                    "nsb": 5,
                    "div_ang": div_ang,
                }
                file_md_json = json.dumps(file_meta_data)
                data_output_pattern = f"Data/*-div{div_ang}*-moon*.simtel.zst"
                # verify the number of events in the simtel file
                mgv_step = self.setExecutable(
                    "dirac_simtel_check",
                    arguments=f"'{data_output_pattern}'",
                    logFile=f"Verify_n_showers_moon_div{div_ang}_Log.txt",
                )
                mgv_step["Value"]["name"] = f"Step{i_step}.{i_substep}_VerifyNShowers"
                mgv_step["Value"]["descr_short"] = "Verify number of showers"

                i_substep += 1

                dm_step = self.setExecutable(
                    "cta-prod-managedata",
                    arguments="'%s' '%s' %s '%s' %s %s '%s' Data"
                    % (
                        md_json,
                        file_md_json,
                        self.base_path,
                        data_output_pattern,
                        self.package,
                        self.program_category,
                        self.catalogs,
                    ),
                    logFile=f"DataManagement_moon_div{div_ang}_Log.txt",
                )
                dm_step["Value"]["name"] = f"Step{i_step}.{i_substep}_DataManagement"
                dm_step["Value"][
                    "descr_short"
                ] = "Save data files to SE and register them in DFC"

                i_substep += 1

                # Upload and register log file - NSB=5
                file_meta_data = {}
                file_md_json = json.dumps(file_meta_data)
                log_file_pattern = f"Data/*-div{div_ang}*-moon*.log_hist.tar"
                log_step = self.setExecutable(
                    "cta-prod-managedata",
                    arguments="'%s' '%s' %s '%s' %s %s '%s' Log"
                    % (
                        md_json,
                        file_md_json,
                        self.base_path,
                        log_file_pattern,
                        self.package,
                        self.program_category,
                        self.catalogs,
                    ),
                    logFile=f"LogManagement_moon_div{div_ang}_Log.txt",
                )
                log_step["Value"]["name"] = f"Step{i_step}.{i_substep}_LogManagement"
                log_step["Value"][
                    "descr_short"
                ] = "Save log to SE and register them in DFC"

                i_substep += 1

        i_step += 1

        # Step 6 - debug only
        if debug:
            ls_step = self.setExecutable("/bin/ls -Ralhtr", logFile="LS_End_Log.txt")
            ls_step["Value"]["name"] = f"Step{i_step}_LSHOME_End"
            ls_step["Value"]["descr_short"] = "list files in Home directory"
            # i_step += 1

        # Number of showers is passed via an environment variable
        self.setExecutionEnv({"NSHOW": f"{self.n_shower}"})
