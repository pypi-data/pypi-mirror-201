"""Pydra tasks for FSL.

>>> from pydra.tasks import fsl
"""

from .bet import BET, RobustFOV
from .eddy import Eddy
from .fast import FAST
from .flirt import (
    FLIRT,
    ApplyXFM,
    ConcatXFM,
    ConvertXFM,
    Img2ImgCoord,
    Img2StdCoord,
    InvertXFM,
    Std2ImgCoord,
)
from .fnirt import FNIRT, ApplyWarp, ConvertWarp, FNIRTFileUtils, InvWarp
from .fugue import FUGUE
from .susan import SUSAN
from .utils import (
    FSLROI,
    FSLInfo,
    FSLMerge,
    FSLReorient2Std,
    FSLSlice,
    FSLSplit,
    fslmaths,
)
