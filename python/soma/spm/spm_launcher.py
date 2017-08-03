# -*- coding: utf-8 -*-
from distutils.spawn import find_executable
from collections import deque
import os
import tempfile
import sys
import subprocess

from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.custom_decorator_pattern import singleton
from soma.spm.spm_main_module import SPM8MainModule, SPM12MainModule


class SPMLauncher():
    @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
    def setSPMScriptPath(self, spm_script_path):
        self.spm_script_path = spm_script_path

    @checkIfArgumentTypeIsAllowed(list, 1)
    def _addBatchListToExecutionQueue(self, batch_list):
        self.current_spm_job_index += 1
        spm_job_key_word = 'matlabbatch{%i}' % self.current_spm_job_index
        self.full_batch_deque.extend(addBatchKeyWordInEachItem(spm_job_key_word, batch_list))

    @checkIfArgumentTypeIsAllowed(list, 1)
    def addSPMCommandToExecutionQueue(self, spm_commands_list):
        self.full_batch_deque.extend(spm_commands_list)

    def _writeSPMScript(self):
        if not os.path.exists(os.path.dirname(self.spm_script_path)):
            os.makedirs(os.path.dirname(self.spm_script_path))
        else:
            pass#folder already exists
        spm_script_file = open(self.spm_script_path, 'w+')
        for batch_row in self.full_batch_deque:
            spm_script_file.write(batch_row + '\n')
        spm_script_file.close()

    def _moveSPMDefaultPathsIfNeeded(self, current_execution_module_deque):
        for module in current_execution_module_deque:
            try:
                module._moveSPMDefaultPathsIfNeeded()
            except Exception, e:
                raise RuntimeError("Move SPM default paths failed :\n%s" % e)

    #TODO : find an other way to re-initialize or destroy singleton function
    def resetExecutionQueue(self):
        """
        for avoid conflict during execution (if we start new module during first
        execution the second batch is added to the first)
        """
        self.current_spm_job_index = 0
        self.full_batch_deque.clear()
        self.execution_module_deque.clear()
#===========================================================================
#
#===========================================================================
class SPM(SPMLauncher):
    def _getMatlabPathFromExecutable(self, matlab_executable):
        matlab_executable_path = find_executable(matlab_executable)
        if matlab_executable_path:
            return matlab_executable_path
        else:
            raise RuntimeError('Matlab executable not found')

    @checkIfArgumentTypeIsAllowed(list, 1)
    def addMatlabCommandBeforeSPMRunning(self, matlab_commands_list):
        self.matlab_commands_before_list.extend(matlab_commands_list)

    @checkIfArgumentTypeIsAllowed(list, 1)
    def addMatlabCommandAfterSPMRunning(self, matlab_commands_list):
        self.matlab_commands_after_list.extend(matlab_commands_list)

    def run(self, use_matlab_options=True):
        if self.spm_script_path is not None:
            self._writeSPMScript()
            matlab_script_path = self._writeMatlabScript()
            current_execution_module_deque = deque(self.execution_module_deque)
            self.resetExecutionQueue()
            output = self._runMatlabScript(use_matlab_options, matlab_script_path)
            try:
                checkIfMatlabFailedBeforSpm(output)
                checkIfSpmHasFailed(output)
                self._moveSPMDefaultPathsIfNeeded(current_execution_module_deque)
            except Exception, e:
                raise RuntimeError("%s\n\nError after SPM finished :\n%s" % (output, e))

            return output
        else:
            raise ValueError("job path and batch path are required")

    def _writeMatlabScript(self):
        #matlab_script_path is created in tmp with little NamedTemporaryFile
        #because matlab namelengthmax is 63
        matlab_script_path = tempfile.NamedTemporaryFile(suffix=".m").name
        workspace_directory = os.path.dirname(self.spm_script_path)

        if not os.path.exists(os.path.dirname(matlab_script_path)):
            os.makedirs(os.path.dirname(matlab_script_path))
        else:
            #folder already exists
            pass
        if self.spm_path is not None:
            matlab_script_file = open(matlab_script_path, 'w+')
            matlab_script_file.write("previous_pwd = pwd;\n")
            matlab_script_file.write("cd('%s');\n" % workspace_directory)
            matlab_script_file.write("addpath('%s');\n" % self.spm_path)
            for matlab_command in self.matlab_commands_before_list:
                matlab_script_file.write(matlab_command + "\n")
            matlab_script_file.write("try\n")
            matlab_script_file.write("  spm('%s');\n"%self.spm_defaults)
            matlab_script_file.write("  jobid = cfg_util('initjob', '%s');\n" % self.spm_script_path)#initialise job
            matlab_script_file.write("  cfg_util('run', jobid);\n")
            matlab_script_file.write("catch\n")
            matlab_script_file.write("  disp('error running SPM');\n")
            matlab_script_file.write("  exit(1);\n")
            matlab_script_file.write("end\n")
            for matlab_command in self.matlab_commands_after_list:
                matlab_script_file.write(matlab_command + "\n")
            matlab_script_file.write("cd(previous_pwd);\n")
            matlab_script_file.write("exit\n")
            matlab_script_file.close()
        else:
            raise ValueError('SPM path not found')#This raise is normally useless!!
        #reset matlab_commands list
        self.matlab_commands_before_list = []
        self.matlab_commands_after_list = []
        return matlab_script_path

    def _runMatlabScript(self, use_matlab_options, matlab_script_path):
        cwd = os.getcwd()
        batch_directory = os.path.dirname(matlab_script_path)
        os.chdir(batch_directory)
        if not use_matlab_options:
            matlab_run_options = ''
        else:
            matlab_run_options = self.matlab_options

        matlab_commmand = ['bv_unenv', self.matlab_executable_path, matlab_run_options, "-r \"run('%s');\"" %matlab_script_path]  # bv_unenv is needed for CentOs 7 (LIB & Pitie)
        print('Running matlab command:', matlab_commmand)
        output = runCommand(matlab_commmand)
        os.chdir(cwd)

        return output

#===========================================================================
#===============================================================================
# # SPM8 (Matlab needed)
#===============================================================================
#===========================================================================
@singleton
class SPM8(SPM):
    def __init__(self, spm_path, matlab_executable, matlab_options='', spm_defaults='PET'):
        self.current_spm_job_index = 0
        self.full_batch_deque = deque()
        self.execution_module_deque = deque()

        self.spm_path = spm_path
        self.matlab_executable_path = self._getMatlabPathFromExecutable(matlab_executable)
        self.matlab_options = matlab_options
        self.spm_defaults = spm_defaults

        self.spm_script_path = None
        self.matlab_commands_before_list = []
        self.matlab_commands_after_list = []

        self._checkSPM8Availability()

    def _checkSPM8Availability(self):
        checkIfExists(self.matlab_executable_path, 'matlab_executable_path')
        checkIfExists(self.spm_path, 'spm8_path')

    @checkIfArgumentTypeIsAllowed(SPM8MainModule, 1)
    def addModuleToExecutionQueue(self, spm_module):
        self.execution_module_deque.append(spm_module)
        batch_list = spm_module.getStringListForBatch()
        self._addBatchListToExecutionQueue(batch_list)

#===========================================================================
# SPM12 (Matlab needed)
#===========================================================================
@singleton
class SPM12(SPM):
    def __init__(self, spm_path, matlab_executable, matlab_options='', spm_defaults='PET'):
        self.current_spm_job_index = 0
        self.full_batch_deque = deque()
        self.execution_module_deque = deque()

        self.spm_path = spm_path
        self.matlab_executable_path = self._getMatlabPathFromExecutable(matlab_executable)
        self.matlab_options = matlab_options
        self.spm_defaults = spm_defaults

        self.spm_script_path = None
        self.matlab_commands_before_list = []
        self.matlab_commands_after_list = []

        self._checkSPM12Availability()

    def _checkSPM12Availability(self):
        checkIfExists(self.matlab_executable_path, 'matlab_executable_path')
        checkIfExists(self.spm_path, 'spm12_path')

    @checkIfArgumentTypeIsAllowed(SPM12MainModule, 1)
    def addModuleToExecutionQueue(self, spm_module):
        self.execution_module_deque.append(spm_module)
        batch_list = spm_module.getStringListForBatch()
        self._addBatchListToExecutionQueue(batch_list)

#===========================================================================
#
#===========================================================================
class SPMStandalone(SPMLauncher):
    def run(self, initcfg=True):
        if self.spm_script_path is not None:
            self.full_batch_deque.appendleft("spm('defaults', '%s');" % self.spm_defaults)
            if initcfg:
                self.full_batch_deque.appendleft("spm_jobman('initcfg');")
            self._writeSPMScript()
            cwd = os.getcwd()
            job_directory = os.path.dirname(self.spm_script_path)
            os.chdir(job_directory)
            standalone_command = [self.standalone_command, self.standalone_mcr_path, 'run', self.spm_script_path]
            current_execution_module_deque = deque(self.execution_module_deque)
            self.resetExecutionQueue()
            print('running SPM standalone command:', standalone_command)
            output = runCommand(standalone_command)
            os.chdir(cwd)
            try:
                checkIfSpmHasFailed(output)
                self._moveSPMDefaultPathsIfNeeded(current_execution_module_deque)
            except Exception, e:
                raise RuntimeError("%s\n\nError after SPM finished :\n%s" % (output, e))

            return output
        else:
            raise ValueError("job path is required")

#==============================================================================
# SPM8 Standalone
#==============================================================================
@singleton
class SPM8Standalone(SPMStandalone):
    def __init__(self, command, mcr_path, path, spm_defaults='PET'):
        self.current_spm_job_index = 0
        self.full_batch_deque = deque()
        self.execution_module_deque = deque()

        self.standalone_command = command
        self.standalone_mcr_path = mcr_path
        self.standalone_path = path
        self.spm_defaults = spm_defaults

        self.spm_script_path = None

        self._checkSPM8StandaloneAvailability()

    def _checkSPM8StandaloneAvailability(self):
        checkIfExists(self.standalone_command, 'spm8_standalone_command')
        checkIfExists(self.standalone_mcr_path, 'spm8_standalone_mcr_path')
        checkIfExists(self.standalone_path, 'spm8_standalone_path')

    @checkIfArgumentTypeIsAllowed(SPM8MainModule, 1)
    def addModuleToExecutionQueue(self, spm_module):
        self.execution_module_deque.append(spm_module)
        batch_list = spm_module.getStringListForBatch()
        self._addBatchListToExecutionQueue(batch_list)


#==============================================================================
# SPM12 Standalone
#==============================================================================
@singleton
class SPM12Standalone(SPMStandalone):
    def __init__(self, command, mcr_path, path, spm_defaults='PET'):
        self.current_spm_job_index = 0
        self.full_batch_deque = deque()
        self.execution_module_deque = deque()

        self.standalone_command = command
        self.standalone_mcr_path = mcr_path
        self.standalone_path = path
        self.spm_defaults = spm_defaults

        self.spm_script_path = None

        self._checkSPM12StandaloneAvailability()

    def _checkSPM12StandaloneAvailability(self):
        checkIfExists(self.standalone_command, 'spm12_standalone_command')
        checkIfExists(self.standalone_mcr_path, 'spm12_standalone_mcr_path')
        checkIfExists(self.standalone_path, 'spm12_standalone_path')

    @checkIfArgumentTypeIsAllowed(SPM12MainModule, 1)
    def addModuleToExecutionQueue(self, spm_module):
        self.execution_module_deque.append(spm_module)
        batch_list = spm_module.getStringListForBatch()
        self._addBatchListToExecutionQueue(batch_list)


def spm8(spm8_standalone_command=None,
         spm8_standalone_mcr_path=None,
         spm8_standalone_path=None,
         spm8_path=None,
         matlab_executable=None,
         matlab_options=None):
    spm8 = None
    try:
        spm8 = SPM8Standalone(spm8_standalone_command,
                              spm8_standalone_mcr_path,
                              spm8_standalone_path)
    except:
        try:
            spm8 = SPM8(spm8_path,
                        matlab_executable,
                        matlab_options)
        except:
            raise RuntimeError('SPM8 is not available or configuration '
                               'is incomplete')

    return spm8


def spm12(spm12_standalone_command=None,
          spm12_standalone_mcr_path=None,
          spm12_standalone_path=None,
          spm12_path=None,
          matlab_executable=None,
          matlab_options=None):
    spm12 = None
    try:
        spm12 = SPM12Standalone(spm12_standalone_command,
                                spm12_standalone_mcr_path,
                                spm12_standalone_path)
    except:
        try:
            spm12 = SPM12(spm12_path,
                          matlab_executable,
                          matlab_options)
        except:
            raise RuntimeError('SPM12 is not available or configuration '
                               'is incomplete')

    return spm12

#===========================================================================
#===========================================================================
# #
#===========================================================================
#===========================================================================


def checkIfExists(path, configuration_name):
    if not os.path.exists(path):
        raise ValueError(configuration_name + ' does not exist')
    else:
        pass


def checkIfMatlabFailedBeforSpm(output):
    """check if output terminal contains "spm" """
    if "License checkout failed" in output.lower():
        raise RuntimeError("Matlab execution failed : License checkout failed")
    elif not "spm" in output.lower():
        raise RuntimeError("Matlab execution failed")


def checkIfSpmHasFailed(output):
    """check if output terminal contains "Execution failed" """
    common_spm_errors = ["Error reading information on",
                         "Cant open image file",
                         "Error while evaluating uicontrol Callback",
                         "Index exceeds matrix dimensions"]
    for common_spm_error in common_spm_errors:
        if common_spm_error in output:
            raise RuntimeError("SPM execution failed : %s" % common_spm_error)


def runCommand(command_list):
    #Popen run spm in background
    process = subprocess.Popen(command_list,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    # Poll process for new output until finished
    output_lines = []
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        output_lines.append(nextline)
        sys.stdout.write(nextline)
        sys.stdout.flush()

    return ''.join(output_lines)
