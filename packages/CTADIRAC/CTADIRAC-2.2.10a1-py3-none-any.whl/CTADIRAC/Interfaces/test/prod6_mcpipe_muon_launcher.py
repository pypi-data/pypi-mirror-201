""" Launcher script to launch a Prod6MCPipeMuonJob
    on the WMS or create a Transformation
"""

from DIRAC.Core.Base import Script
Script.setUsageMessage('\n'.join([__doc__.split('\n')[1],
                                  'Usage:',
                                  'python %s.py <mode> <telescope> <pointing> <zenith> <n showers> with-half-moon degraded-mirror-ref' % Script.scriptName,
                                  'Arguments:',
                                  '  mode: WMS for testing, TS for production',
                                  '  telescope: one of LST, MST-FlashCam, MST-NectarCam, SST, SCT',
                                  '  pointing: North or South',
                                  '  zenith: 20, 40 or 60',
                                  '  n shower: 100 for testing',
                                  '  with-half-moon: simulate half-moon conditions (optional argument)',
                                  '  degraded-mirror-ref: simulate with degraded mirror reflectivity (optional argument)',
                                  '\ne.g: python %s.py WMS LST North 20 100 with-half-moon degraded-mirror-ref' % Script.scriptName,
                                  ]))

Script.parseCommandLine()

import DIRAC
from DIRAC.TransformationSystem.Client.Transformation import Transformation
from CTADIRAC.Interfaces.API.Prod6MCPipeMuonJob import Prod6MCPipeMuonJob
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.Interfaces.API.Dirac import Dirac


def submit_transformation(job, trans_name):
  """ Create a transformation executing the job workflow
  """
  DIRAC.gLogger.notice('submit_trans : %s' % trans_name)

  # Initialize JOB_ID
  job.workflow.addParameter(Parameter("JOB_ID", "000000", "string", "", "",
                                      True, False, "Temporary fix"))

  trans = Transformation()
  trans.setTransformationName(trans_name)  # this must be unique
  trans.setType("MCSimulation")
  trans.setDescription("Prod6 MC Pipe TS")
  trans.setLongDescription("Prod6 simulation pipeline")  # mandatory
  trans.setBody(job.workflow.toXML())
  result = trans.addTransformation()  # transformation is created here
  if not result['OK']:
    return result
  trans.setStatus("Active")
  trans.setAgentType("Automatic")
  trans_id = trans.getTransformationID()
  return trans_id


def submit_wms(job):
  """ Submit the job to the WMS
  @todo launch job locally
  """
  dirac = Dirac()
  job.setJobGroup('Prod6MCPipeMuonJob')
  result = dirac.submitJob(job)
  if result['OK']:
    Script.gLogger.notice('Submitted job: ', result['Value'])
  return result


def run_simulation(args):
  """ Simple wrapper to create a Prod6MCPipeMuonJob and setup parameters
      from positional arguments given on the command line.

      Parameters:
      args -- mode (trans_name)
  """
  DIRAC.gLogger.notice('run_mc_pipeline')
  # get arguments
  mode = args[0]

  # job setup
  job = Prod6MCPipeMuonJob()
  job.version = '2022-08-03-sc'
  job.compiler = 'gcc83_matchcpu'
  # override for testing
  job.setName('Prod6_MC_Pipeline')
  # parameters from command line
  job.set_site('Paranal')
  job.set_particle('muon')
  job.set_telescope(args[1])
  job.set_pointing_dir(args[2])
  job.zenith_angle = args[3]
  job.n_shower = args[4]
  if len(args) > 5:
    if args[5] == 'with-half-moon':
      job.set_half_moon(True)
    if args[5] == 'degraded-mirror-ref':
      job.set_degraded_mirror_reflectivity(True)
    if len(args) > 6:
      if args[6] == 'with-half-moon':
        job.set_half_moon(True)
      if args[6] == 'degraded-mirror-ref':
        job.set_degraded_mirror_reflectivity(True)


  # input
  # job.setInputSandbox(['dirac_prod6_run'])

  # output
  job.setOutputSandbox(['*Log.txt'])

  # specific configuration
  if mode == 'WMS':
    # put here your user directory under the Dirac File Catalog
    job.base_path = '/vo.cta.in2p3.fr/user/o/ogueta/prod6_test/'
    # adjust start_run_number and run_number for testing, both can be 0
    job.start_run_number = '0'
    job.run_number = '1'
    job.setupWorkflow(debug=True)
    # submit to the WMS for debug, choose a destination site
    # job.setDestination('LCG.DESY-ZEUTHEN.de')
    job.setDestination('LCG.PIC.es')
    # job.setDestination('ARC.CSCS.ch')
    result = submit_wms(job)
  elif mode == 'TS':
    # put here your user directory under the Dirac File Catalog
    # job.base_path = '/vo.cta.in2p3.fr/MC/PRODTest/test/'
    job.start_run_number = '0'
    job.run_number = '@{JOB_ID}'  # dynamic
    job.setupWorkflow(debug=False)
    # extra tag in case you have to run different tests, can be empty
    tag = '_v3'
    # Change below the name of transformation, in particular the user name
    # this name must be unique accross the whole system
    trans_name = 'Prod6_%s_%s_%s_%s%s' %\
        (job.particle, job.telescope, job.pointing_dir, job.zenith_angle, tag)
    result = submit_transformation(job, trans_name)
  else:
    DIRAC.gLogger.error('1st argument should be the job mode: WMS or TS,\n\
                             not %s' % mode)
    return None

  return result


#########################################################
if __name__ == '__main__':

  arguments = Script.getPositionalArgs()
  if len(arguments) < 5:
    Script.showHelp()
  try:
    result = run_simulation(arguments)
    if not result['OK']:
      DIRAC.gLogger.error(result['Message'])
      DIRAC.exit(-1)
    else:
      DIRAC.gLogger.notice('Done')
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit(-1)
