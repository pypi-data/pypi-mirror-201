"""
  New job class to run Prod6 for Paranal and La Palma
"""

__RCSID__ = "$Id$"

# generic imports
import json
import collections
import itertools


# DIRAC imports
import DIRAC
from DIRAC.Interfaces.API.Job import Job
from CTADIRAC.Core.Utilities.tool_box import DATA_LEVEL_METADATA_ID


class MCPipeNSBJob(Job):
    """Job extension class for Prod5 MC NSB simulations,
    takes care of running corsika piped into simtel
    2 output files are created for Dark and Moon NSB
    """

    def __init__(self, cpu_time=259200):
        """Constructor takes almosst everything from base class

        Keyword arguments:
        cpuTime -- max cpu time allowed for the job
        """
        super().__init__()
        self.setCPUTime(cpu_time)
        self.setName("MC_Generation")
        self.setType("MCSimulation")
        self.package = "corsika_simtelarray"
        self.version = "2022-08-03"
        self.compiler = "gcc83_matchcpu"
        self.program_category = "tel_sim"
        self.prog_name = "sim_telarray"
        self.start_run_number = "0"
        self.run_number = "@{JOB_ID}"  # dynamic
        self.configuration_id = 15
        self.output_data_level = DATA_LEVEL_METADATA_ID["R1"]
        self.base_path = "/vo.cta.in2p3.fr/MC/PROD6/"
        self.catalogs = json.dumps(["DIRACFileCatalog", "TSCatalog"])
        self.output_metadata = collections.OrderedDict()
        self.output_file_metadata = collections.OrderedDict()
        self.sct = ""
        self.magic = ""
        self.moon = ""
        self.array_layout = "Prod6-Hyperarray"
        self.div_ang = ""

    def set_site(self, site):
        """Set the site to simulate

        Parameters:
        site -- a string for the site name (LaPalma)
        """
        if site in ["Paranal", "LaPalma"]:
            DIRAC.gLogger.info(f"Set Corsika site to: {site}")
            self.site = site
        else:
            DIRAC.gLogger.error(f"Site is unknown: {site}")
            DIRAC.exit(-1)

    def set_particle(self, particle):
        """Set the corsika primary particle

        Parameters:
        particle -- a string for the particle type/name
        """
        if particle in ["gamma", "gamma-diffuse", "electron", "proton", "helium"]:
            DIRAC.gLogger.info(f"Set Corsika particle to: {particle}")
            self.particle = particle
        else:
            DIRAC.gLogger.error(f"Corsika does not know particle type: {particle}")
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

    def set_moon(self, moon=["dark", "half", "full"]):
        """Set to simulate with various moon conditions

        Parameters:
        moon -- a list of moon conditions for simulation
        """
        if moon == ["dark"]:
            DIRAC.gLogger.info("Set simulations with dark conditions")
            self.moon = ""
            self.output_file_metadata["nsb"] = [1]
        elif moon == ["dark", "half"]:
            DIRAC.gLogger.info("Set simulations with half-moon conditions")
            self.moon = "--with-half-moon"
            self.output_file_metadata["nsb"] = [1, 5]

        elif moon == ["dark", "half", "full"]:
            DIRAC.gLogger.info("Set simulations with full-moon conditions")
            self.moon = "--with-full-moon"
            self.output_file_metadata["nsb"] = [1, 5, 19]
        else:
            DIRAC.gLogger.error(
                "Unknown moon option: %s. Options for simulation step are: \n [dark] \n [dark, half] \n [dark, half, "
                "full] " % str(moon).replace("'", "")
            )
            DIRAC.exit(-1)

    def set_div_ang(self, div_ang=None):
        div_default = [
            "0.0022",
            "0.0043",
            "0.008",
            "0.01135",
            "0.01453",
        ]  # Default divergent angles
        if div_ang is not None:
            if str(div_ang).replace(", ", ",").split(sep=",") != div_default:
                DIRAC.gLogger.error(
                    "Unknown div_ang option: %s. Option for simulation step is: %s"
                    % (div_ang, ", ".join(str(x) for x in div_default))
                )
                DIRAC.exit(-1)
            else:
                self.div_ang = div_default
                self.output_file_metadata["div_ang"] = div_default

    def set_magic(self, with_magic=False):
        """Set to simulate with MAGIC

        Parameters:
        with_magic -- a boolean for simulating with MAGIC
        """
        if with_magic is True:
            DIRAC.gLogger.info("Set simulations with MAGIC telescopes")
            self.magic = "--with-magic"

    def set_sct(self, with_sct=None):
        """Set to include SCTs in simulations

        Parameters:
        with_sct -- a string to include SCTs
        """
        if with_sct is not None:
            if with_sct.lower() == "all":
                DIRAC.gLogger.info("Set to include SCTs for all MST positions")
                self.sct = "--with-all-scts"
            elif with_sct.lower() == "non-alpha":
                DIRAC.gLogger.info("Set to include SCTs for non-Alpha MST positions")
                self.sct = "--with-sct"
            self.version = self.version + "-sc"

    def set_output_metadata(self):
        """define the common meta data of the application"""
        # The order of the metadata dictionary is important,
        # since it's used to build the directory structure
        self.output_metadata["array_layout"] = self.array_layout
        self.output_metadata["site"] = self.site
        self.output_metadata["particle"] = self.particle
        # for air shower simulation means North=0 and South=180
        # but here piped into tel_sim so North=180 and South=0
        if self.pointing_dir == "North":
            self.output_metadata["phiP"] = 180
        if self.pointing_dir == "South":
            self.output_metadata["phiP"] = 0
        self.output_metadata["thetaP"] = float(self.zenith_angle)
        if self.sct:
            self.output_metadata["sct"] = "True"
        else:
            self.output_metadata["sct"] = "False"
        self.output_metadata[self.program_category + "_prog"] = self.prog_name
        self.output_metadata[self.program_category + "_prog_version"] = "".join(
            self.version.rsplit("-sc", 1)
        )
        self.output_metadata["data_level"] = self.output_data_level
        self.output_metadata["configuration_id"] = self.configuration_id
        self.output_metadata["merged"] = 0
        self.output_metadata["MCCampaign"] = self.MCCampaign

    def set_executable_sequence(self, debug=False):
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

        # step 2 - use new CVMFS repo
        sw_step = self.setExecutable(
            "cta-prod-setup-software",
            arguments="-p %s -v %s -a simulations -g %s"
            % (self.package, self.version, self.compiler),
            logFile="SetupSoftware_Log.txt",
        )
        sw_step["Value"]["name"] = "Step%i_SetupSoftware" % i_step
        sw_step["Value"]["descr_short"] = "Setup software"
        i_step += 1

        # step 3 - run corsika+sim_telarray
        prod_exe = "./dirac_prod_run"
        if self.div_ang:
            prod_args = (
                "--start_run %s --run %s --sequential --divergent %s %s %s %s %s %s %s"
                % (
                    self.start_run_number,
                    self.run_number,
                    self.moon,
                    self.sct,
                    self.magic,
                    self.site,
                    self.particle,
                    self.pointing_dir,
                    self.zenith_angle,
                )
            )

        else:
            prod_args = "--start_run {} --run {} {} {} {} {} {} {} {}".format(
                self.start_run_number,
                self.run_number,
                self.moon,
                self.sct,
                self.magic,
                self.site,
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

        # step 4 - debug only
        if debug:
            ls_step = self.setExecutable("/bin/ls -Ralhtr", logFile="LS_End_Log.txt")
            ls_step["Value"]["name"] = "Step%i_LS_End" % i_step
            ls_step["Value"][
                "descr_short"
            ] = "list files in working directory and sub-directory"
            i_step += 1

        # step 5 - data management
        md_json = json.dumps(self.output_metadata)

        keys = self.output_file_metadata.keys()

        for element in itertools.product(*self.output_file_metadata.values()):
            i_substep = 1
            combination = dict(zip(keys, element))

            # build file meta data
            file_meta_data = {
                "runNumber": self.run_number,
            }
            for key, value in combination.items():
                file_meta_data[key] = value

            file_md_json = json.dumps(file_meta_data)

            if combination["nsb"] == 1:
                moon_str = "dark"
            if combination["nsb"] == 5:
                moon_str = "moon"
            if combination["nsb"] == 19:
                moon_str = "fullmoon"

            if combination.get("div_ang"):
                div = f"div{combination['div_ang']}"
                div_str = div + "_"
            else:
                div = ""
                div_str = ""

            data_output_pattern = f"Data/*-{div}*-{moon_str}*.simtel.zst"

            # substep 1 - verify the number of events in the simtel file
            mgv_step = self.setExecutable(
                "dirac_simtel_check",
                arguments=f"'{data_output_pattern}'",
                logFile=f"Verify_n_showers_{moon_str}_{div_str}Log.txt",
            )
            mgv_step["Value"]["name"] = f"Step{i_step}.{i_substep}_VerifyNShowers"
            mgv_step["Value"]["descr_short"] = "Verify number of showers"

            i_substep += 1

            # substep 2 - upload data file on SE and register in catalog
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
                logFile=f"DataManagement_{moon_str}_{div_str}Log.txt",
            )
            dm_step["Value"]["name"] = f"Step{i_step}.{i_substep}_DataManagement"
            dm_step["Value"][
                "descr_short"
            ] = "Save data files to SE and register them in DFC"
            i_step += 1

            # substep 3 - upload log and histo file on SE and register in catalog
            file_meta_data = {}
            file_md_json = json.dumps(file_meta_data)
            log_file_pattern = f"Data/*-{div}*-{moon_str}*.log_hist.tar"
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
                logFile=f"LogManagement_{moon_str}_{div_str}Log.txt",
            )
            log_step["Value"]["name"] = f"Step{i_step}.{i_substep}_LogManagement"
            log_step["Value"]["descr_short"] = "Save log to SE and register them in DFC"
            i_step += 1

        # Last step - debug only
        if debug:
            ls_step = self.setExecutable("/bin/ls -Ralhtr", logFile="LS_End_Log.txt")
            ls_step["Value"]["name"] = f"Step{i_step}_LSHOME_End"
            ls_step["Value"]["descr_short"] = "list files in Home directory"
            i_step += 1

        # Number of showers is passed via an environment variable
        self.setExecutionEnv({"NSHOW": f"{self.n_shower}"})
