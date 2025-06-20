from pathlib import Path
import shutil

from brainvisa.processes import *
from soma.spm.spm12.spatial.coregister.reslice_options import ResliceOptions
from soma.spm.spm12.spatial.coregister.estimation_options import EstimationOptions
from soma.spm.spm12.spatial.coregister import EstimateAndReslice
from soma.spm.spm_launcher import SPM12, SPM12Standalone

# ------------------------------------------------------------------------------
configuration = Application().configuration


# ------------------------------------------------------------------------------
def validation():
    try:
        spm = SPM12Standalone(configuration.SPM.spm12_standalone_command,
                              configuration.SPM.spm12_standalone_mcr_path,
                              configuration.SPM.spm12_standalone_path)
    except:
        spm = SPM12(configuration.SPM.spm12_path,
                    configuration.matlab.executable,
                    configuration.matlab.options)
    return spm


# ------------------------------------------------------------------------------

userLevel = 1
name = 'spm12 - Coregister: Estimate & Reslice - generic'

estimation_section = "Estimation options"
reslice_section = "reslice options"

signature = Signature(
    "reference", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']),
    "source", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']),
    "others", ListOf(ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    "objective_function", Choice("Mutual Information",
                                 "Normalised Mutual Information",
                                 "Entropy Correlation Coefficient",
                                 "Normalised Cross Correlation"),
    "separation", ListOf(Float()),
    "tolerances", ListOf(Float()),
    "histogram_smoothing", ListOf(Float()),
    "interpolation", Choice("Nearest neighbour",
                            "Trilinear",
                            "2nd Degree B-Spline",
                            "3rd Degree B-Spline",
                            "4th Degree B-Spline",
                            "5th Degree B-Spline",
                            "6th Degree B-Spline",
                            "7th Degree B-Spline"),
    "wrappping", Choice(("No wrap", [False, False, False]),
                        ("Wrap X", [True, False, False]),
                        ("Wrap Y", [False, True, False]),
                        ("Wrap X & Y", [True, True, False]),
                        ("Wrap Z", [False, False, True]),
                        ("Wrap X & Z", [True, False, True]),
                        ("Wrap Y & Z", [False, True, True]),
                        ("Wrap X, Y & Z", [True, True, True])),
    "masking", Boolean(),
    "custom_outputs", Boolean(),
    "source_warped", WriteDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image"]),
    "others_warped", ListOf(WriteDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
    "filename_prefix", String(),
    "extract_coregister_matrix", Boolean(),
    "coregister_matrix", WriteDiskItem("Transformation matrix", "Transformation matrix"),
    "deformation_in_source", Boolean(),

    'batch_location', WriteDiskItem('Matlab SPM script', 'Matlab script', section='default SPM outputs'),
)


def initialization(self):
    self.setOptional("others")
    self.setDisable("source_warped", "others_warped")

    self.addLink(None, "custom_outputs", self.updateSignatureAboutCustomOutputs)
    self.addLink(None, "filename_prefix", self.checkIfNotEmpty)
    self.addLink(None, "extract_coregister_matrix", self.updateSignatureAboutCoregisterMatrix)

    self.addLink("batch_location", "source", self.updateBatchPath)

    # SPM default initialisation
    self.objective_function = "Normalised Mutual Information"
    self.separation = [4, 2]
    self.tolerances = [0.02, 0.02, 0.02, 0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.001, 0.001, 0.001]
    self.histogram_smoothing = [7, 7]
    self.interpolation = "4th Degree B-Spline"
    self.wrapping = "No wrap"
    self.masking = False
    self.filename_prefix = 'r'
    self.extract_coregister_matrix = False

    self.custom_outputs = False
    self.deformation_in_source = True


def updateSignatureAboutCustomOutputs(self, proc):
    if self.custom_outputs:
        self.setEnable("source_warped")
        self.setEnable("others_warped", mandatory=False)
        self.setDisable("filename_prefix")
    else:
        self.setDisable("source_warped", "others_warped")
        self.setEnable("filename_prefix")
    self.signatureChangeNotifier.notify(self)


def checkIfNotEmpty(self, proc):
    if self.filename_prefix in [None, '']:
        self.filename_prefix = 'r'
    else:
        pass


def updateSignatureAboutCoregisterMatrix(self, proc):
    if self.extract_coregister_matrix:
        self.setEnable("coregister_matrix")
    else:
        self.setDisable("coregister_matrix")
    self.signatureChangeNotifier.notify(self)


def updateBatchPath(self, proc):
    if self.source is not None:
        directory_path = os.path.dirname(self.source.fullPath())
        return os.path.join(directory_path, 'spm12_coregister_ER_job.m')


def execution(self, context):
    if self.deformation_in_source:
        source_diskitem = self.source
        others_diskitem = self.others
    else:
        source_diskitem = context.temporary(self.source.format)
        shutil.copy2(self.source.fullPath(),
                     source_diskitem.fullPath())
        
        others_diskitem = []
        if self.others:
            for other in self.others:
                new_other_path = context.temporary(other.format, suffix=Path(other.fullPath()).name)
                others_diskitem.append(new_other_path)
                shutil.copy2(other.fullPath(), new_other_path.fullPath())
            
    reference_diskitem = self.reference

    if self.others and self.custom_outputs:
        if len(self.others) != len(self.others_warped):
            raise ValueError("others_warped and others length do not match")
        else:
            pass  # all is right
    else:
        pass  # others_warped is useless

    estimation_options = EstimationOptions()
    if self.objective_function == "Mutual Information":
        estimation_options.setObjectiveFunctionToMutualInformation()
    elif self.objective_function == "Normalised Mutual Information":
        estimation_options.setObjectiveFunctionToNormalisedMutualInformation()
    elif self.objective_function == "Entropy Correlation Coefficient":
        estimation_options.setObjectiveFunctionToEntropyCorrelationCoefficient()
    elif self.objective_function == "Normalised Cross Correlation":
        estimation_options.setObjectiveFunctionToNormalisedCrossCorrelation()
    else:
        raise ValueError("Unvalid objective_function")

    estimation_options.setSeparation(self.separation)
    estimation_options.setTolerances(self.tolerances)
    estimation_options.setHistogramSmoothing(self.histogram_smoothing)

    reslice_options = ResliceOptions()
    if self.interpolation == "Nearest neighbour":
        reslice_options.setInterpolationToNearestNeighbour()
    elif self.interpolation == "Trilinear":
        reslice_options.setInterpolationToTrilinear()
    elif self.interpolation == "2nd Degree B-Spline":
        reslice_options.setInterpolationTo2ndDegreeBSpline()
    elif self.interpolation == "3rd Degree B-Spline":
        reslice_options.setInterpolationTo3rdDegreeBSpline()
    elif self.interpolation == "4th Degree B-Spline":
        reslice_options.setInterpolationTo4thDegreeBSpline()
    elif self.interpolation == "5th Degree B-Spline":
        reslice_options.setInterpolationTo5thDegreeBSpline()
    elif self.interpolation == "6th Degree B-Spline":
        reslice_options.setInterpolationTo6thDegreeBSpline()
    elif self.interpolation == "7th Degree B-Spline":
        reslice_options.setInterpolationTo7thDegreeBSpline()
    else:
        raise ValueError("Unvalid interpolation")

    reslice_options.setWrapping(self.wrappping[0], self.wrappping[1], self.wrappping[2])

    if self.masking:
        reslice_options.setMasking()
    else:
        reslice_options.unsetMasking()

    reslice_options.setFilenamePrefix(self.filename_prefix)

    estimate_and_reslice = EstimateAndReslice()
    estimate_and_reslice.setReferenceVolumePath(reference_diskitem.fullPath())
    estimate_and_reslice.setSourceVolumePath(source_diskitem.fullPath())
    if self.others:
        for other_diskitem in others_diskitem:
            estimate_and_reslice.addOtherVolumePath(other_diskitem.fullPath())

    if self.custom_outputs:
        estimate_and_reslice.setSourceWarpedPath(self.source_warped.fullPath())
        if self.others:
            other_output_list = []
            for other_diskitem in self.others_warped:
                other_output_list.append(other_diskitem.fullPath())
            estimate_and_reslice.setOtherVolumesWarpedPathList(other_output_list)
    elif not self.custom_outputs and not self.deformation_in_source:
        source_path = Path(self.source.fullPath())
        source_warped_path = source_path.parent / (self.filename_prefix + source_path.name)
        estimate_and_reslice.setSourceWarpedPath(str(source_warped_path))
        if self.others:
            other_output_list = []
            for other_diskitem in self.others:
                other_path = Path(other_diskitem.fullPath())
                other_warped_path = other_path.parent / (self.filename_prefix + other_path.name)
                other_output_list.append(str(other_warped_path))
            estimate_and_reslice.setOtherVolumesWarpedPathList(other_output_list)

    estimate_and_reslice.replaceEstimationOptions(estimation_options)
    estimate_and_reslice.replaceResliceOptions(reslice_options)

    spm = validation()
    spm.addModuleToExecutionQueue(estimate_and_reslice)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)

    if self.extract_coregister_matrix and self.coregister_matrix is not None:
        # very usefull because spm action doesn't recompute minf, so the transformation in minf files is wrong
        source_diskitem.clearMinf()
        self.extractCoregisterMatrix(source_diskitem.fullPath(), reference_diskitem.fullPath(),
                                     self.coregister_matrix.fullPath())

    if source_diskitem.isTemporary():
        source_diskitem.eraseFiles()

    if reference_diskitem.isTemporary():
        reference_diskitem.eraseFiles()


def extractCoregisterMatrix(self, source_path, reference_path, output_path):
    """ because of 'resetIfNecessary' method, reference_vol have exactly one transformation"""
    source_vol = aims.read(source_path)
    source_aligned_trm = aims.AffineTransformation3d(source_vol.header()['transformations'][1])
    reference_vol = aims.read(reference_path)

    reference_scanner_trm = aims.AffineTransformation3d(reference_vol.header()['transformations'][0])
    reference_trm = reference_scanner_trm.inverse()

    aims.write(reference_trm * source_aligned_trm, output_path)
