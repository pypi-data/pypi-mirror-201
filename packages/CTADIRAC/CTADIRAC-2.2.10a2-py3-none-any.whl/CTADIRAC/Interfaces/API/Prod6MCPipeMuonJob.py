"""
  New job class to run Prod6 single-telescope muon simulations
"""

__RCSID__ = "$Id$"

# generic imports
import json
import collections
import numpy as np

# DIRAC imports
import DIRAC
from DIRAC.Interfaces.API.Job import Job
from CTADIRAC.Core.Utilities.tool_box import DATA_LEVEL_METADATA_ID


class Prod6MCPipeMuonJob(Job):
    """Job extension class for Prod5 MC NSB simulations,
    takes care of running corsika piped into simtel
    2 output files are created for Dark and Moon NSB
    """

    def __init__(self, cpu_time=259200):
        """Constructor takes almosst everything from base class

        Keyword arguments:
        cpuTime -- max cpu time allowed for the job
        """
        Job.__init__(self)
        self.setCPUTime(cpu_time)
        self.setName("Prod6MC_Generation")
        self.setType("MCSimulation")
        self.package = "corsika_simtelarray"
        self.version = "2022-08-03-sc"
        self.compiler = "gcc83_matchcpu"
        self.program_category = "tel_sim"
        self.prog_name = "sim_telarray"
        self.configuration_id = 15
        self.output_data_level = DATA_LEVEL_METADATA_ID["R1"]
        self.base_path = "/vo.cta.in2p3.fr/MC/PROD6/"
        self.catalogs = json.dumps(["DIRACFileCatalog", "TSCatalog"])
        self.metadata = collections.OrderedDict()

    def set_site(self, site):
        """Set the site to simulate

        Parameters:
        site -- a string for the site name (LaPalma)
        """
        if site in ["Paranal", "LaPalma"]:
            DIRAC.gLogger.info(f"Set Corsika site to: {site}")
            self.cta_site = site
        else:
            DIRAC.gLogger.error(f"Site is unknown: {site}")
            DIRAC.exit(-1)

    def set_telescope(self, telescope):
        """Set the telescope to simulate

        Parameters:
        telescope -- a string for the telescope name
        """
        if telescope in ["LST", "MST-FlashCam", "MST-NectarCam", "SST", "SCT"]:
            DIRAC.gLogger.info(f"Set telescope to: {telescope}")
            self.telescope = telescope
        else:
            DIRAC.gLogger.error(f"Telescope {telescope} is unknown, aborting")
            DIRAC.exit(-1)

    def set_particle(self, particle):
        """Set the corsika primary particle

        Parameters:
        particle -- a string for the particle type/name
        """
        if particle in ["muon"]:
            DIRAC.gLogger.info(f"Set Corsika particle to: {particle}")
            self.particle = particle
        else:
            DIRAC.gLogger.error(
                "This script can only perform muon simulations, not %s simulations"
                % particle
            )
            DIRAC.exit(-1)

    def set_pointing_dir(self, pointing):
        """Set the pointing direction, North or South

        Parameters:
        pointing -- a string for the pointing direction
        """
        if pointing in ["North", "South", "East", "West"]:
            DIRAC.gLogger.info(f"Set Pointing dir to: {pointing}")
            self.pointing_dir = pointing
        else:
            DIRAC.gLogger.error(f"Unknown pointing direction: {pointing}")
            DIRAC.exit(-1)

    def set_half_moon(self, half_moon=False):
        """Set if to simulate with full-moon conditions

        Parameters:
        half_moon -- a boolean for simulating with half-moon conditions
        """
        if half_moon is True:
            DIRAC.gLogger.info("Set simulations with half-moon conditions")
            self.half_moon = "--with-half-moon"
        else:
            self.half_moon = ""

    def set_degraded_mirror_reflectivity(self, degraded_mirror_reflectivity=False):
        """Set the values of degraded mirror reflectivity to simulate

        Parameters:
        degraded_mirror_reflectivity -- a boolean to set if to simulate a degraded mirror reflectivity (0.3 to 1.0 in steps of 0.05)
        """
        if degraded_mirror_reflectivity:
            DIRAC.gLogger.info("Set simulations with degraded mirror reflectivities")
            self.degraded_values = np.arange(0.3, 1.05, 0.05)
            self.degraded_mirror = "--degraded-mirror-ref"
        else:
            DIRAC.gLogger.info("Set simulations without degraded mirror reflectivities")
            self.degraded_values = [1]  # No degraded mirror reflectivity
            self.degraded_mirror = ""

    def set_meta_data(self):
        """define the common meta data of the application"""
        # The order of the metadata dictionary is important,
        # since it's used to build the directory structure
        self.metadata["array_layout"] = "Single-telescope"
        self.metadata["site"] = self.cta_site
        self.metadata["particle"] = self.particle
        # for air shower simulation means North=0 and South=180
        # but here piped into tel_sim so North=180 and South=0
        if self.pointing_dir == "North":
            self.metadata["phiP"] = 180
        if self.pointing_dir == "South":
            self.metadata["phiP"] = 0
        self.metadata["thetaP"] = float(self.zenith_angle)
        self.metadata[self.program_category + "_prog"] = self.prog_name
        self.metadata[self.program_category + "_prog_version"] = "".join(
            self.version.rsplit("-sc", 1)
        )
        self.metadata["data_level"] = self.output_data_level
        self.metadata["configuration_id"] = self.configuration_id
        if self.telescope == "SCT":
            self.metadata["sct"] = "True"
        else:
            self.metadata["sct"] = "False"

    def setupWorkflow(self, debug=False):
        """Override the base class job workflow to adapt to NSB test simulations
        All parameters shall have been defined before that method is called.
        """
        # step 1 - debug only
        i_step = 1
        if debug:
            ls_step = self.setExecutable("/bin/ls -alhtr", logFile="LS_Init_Log.txt")
            ls_step["Value"]["name"] = "Step%i_LS_Init" % i_step
            ls_step["Value"]["descr_short"] = "list files in working directory"
            i_step += 1

            env_step = self.setExecutable("/bin/env", logFile="Env_Log.txt")
            env_step["Value"]["name"] = "Step%i_Env" % i_step
            env_step["Value"]["descr_short"] = "Dump environment"
            i_step += 1

        # step 2 : use new CVMFS repo
        sw_step = self.setExecutable(
            "cta-prod-setup-software",
            arguments="-p %s -v %s -a simulations -g %s -r /cvmfs/sw.cta-observatory.org/software"
            % (self.package, self.version, self.compiler),
            logFile="SetupSoftware_Log.txt",
        )
        sw_step["Value"]["name"] = "Step%i_SetupSoftware" % i_step
        sw_step["Value"]["descr_short"] = "Setup software"
        i_step += 1

        # step 3 run corsika+sim_telarray
        prod_exe = "./dirac_prod6_muon_run"
        prod_args = "--start_run {} --run {} {} {} {} {} {} {} {}".format(
            self.start_run_number,
            self.run_number,
            self.half_moon,
            self.degraded_mirror,
            self.telescope,
            self.cta_site,
            self.particle,
            self.pointing_dir,
            self.zenith_angle,
        )

        cs_step = self.setExecutable(
            prod_exe, arguments=prod_args, logFile="CorsikaSimtel_Log.txt"
        )
        cs_step["Value"]["name"] = "Step%i_CorsikaSimtel" % i_step
        cs_step["Value"]["descr_short"] = "Run Corsika piped into simtel"
        i_step += 1

        # step 4 - define meta data, upload file on SE and register in catalogs
        self.set_meta_data()
        md_json = json.dumps(self.metadata)

        i_step += 1
        i_substep = 0
        for degraded in self.degraded_values:
            data_output_pattern = f"Data/*dark-ref-degraded-{degraded:.2f}.simtel.zst"

            # step 5 verify the number of events in the simtel file
            mgv_step = self.setExecutable(
                "dirac_simtel_check",
                arguments=f"'{data_output_pattern}'",
                logFile="Verify_n_showers_Log.txt",
            )
            mgv_step["Value"]["name"] = f"Step{i_step}.{i_substep}_VerifyNShowers"
            mgv_step["Value"]["descr_short"] = "Verify number of showers"

            # Upload and register data - NSB=1 dark
            file_meta_data = {"runNumber": self.run_number, "nsb": 1}
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
                logFile=f"DataManagement_dark_ref_degraded_{degraded:.2f}Log.txt",
            )
            dm_step["Value"]["name"] = f"Step{i_step}.{i_substep}_DataManagement"
            dm_step["Value"][
                "descr_short"
            ] = "Save data files to SE and register them in DFC"
            i_substep += 1

            # Upload and register log and histo file - NSB=1
            file_meta_data = {}
            file_md_json = json.dumps(file_meta_data)
            log_file_pattern = f"Data/*dark-ref-degraded-{degraded:.2f}.log_hist.tar"
            log_step = self.setExecutable(
                "cta-prod-managedata",
                arguments="'%s' '%s' '%s' %s '%s' %s %s '%s' Log"
                % (
                    md_json,
                    md_field_json,
                    file_md_json,
                    self.base_path,
                    log_file_pattern,
                    self.package,
                    self.program_category,
                    self.catalogs,
                ),
                logFile=f"LogManagement_dark_ref_degraded_{degraded:.2f}Log.txt",
            )
            log_step["Value"]["name"] = f"Step{i_step}.{i_substep}_LogManagement"
            log_step["Value"]["descr_short"] = "Save log to SE and register them in DFC"
            i_substep += 1

            if self.half_moon == "--with-half-moon":
                # Now switching to half moon NSB
                # Upload and register data - NSB=5 half moon
                file_meta_data = {"runNumber": self.run_number, "nsb": 5}
                file_md_json = json.dumps(file_meta_data)
                data_output_pattern = "Data/*moon-ref-degraded-%.2f.simtel.zst" % (
                    degraded
                )

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
                    logFile=f"DataManagement_moon_ref_degraded_{degraded:.2f}Log.txt",
                )
                dm_step["Value"]["name"] = f"Step{i_step}.{i_substep}_DataManagement"
                dm_step["Value"][
                    "descr_short"
                ] = "Save data files to SE and register them in DFC"
                i_substep += 1

                # Upload and register log file - NSB=5
                file_meta_data = {}
                file_md_json = json.dumps(file_meta_data)
                log_file_pattern = "Data/*moon-ref-degraded-%.2f.log_hist.tar" % (
                    degraded
                )
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
                    logFile=f"LogManagement_moon_ref_degraded_{degraded:.2f}Log.txt",
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
            i_step += 1

        # Number of showers is passed via an environment variable
        self.setExecutionEnv(
            {
                "NSHOW": f"{self.n_shower}",
                "CORSIKA_MULTIPLEX_SEQUENTIAL": "1",  # Set CORSIKA multipipe to run in sequential mode (better for single-slot/cpu grid jobs)
            }
        )
