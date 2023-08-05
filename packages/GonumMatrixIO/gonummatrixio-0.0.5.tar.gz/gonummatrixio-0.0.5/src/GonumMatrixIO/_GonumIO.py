import numpy as np

def saveMatrix(matrix: np.ndarray, filepath):
    """
    Save a numpy matrix to a binary file at file path, in a format that gonum can accept.

    Be aware this method will truncate any file it is pointed at!

    :param filepath: (str | Pathlike) the path to the binary save file
    :raises FileNotFoundError: If filepath is not valid
    """

    # My apologies for the magic number. See https://pkg.go.dev/gonum.org/v1/gonum@v0.12.0/mat#Dense.MarshalBinary for details
    meta = np.array([18373144242814977,matrix.shape[0],matrix.shape[1],0,0]).view("float")
    matrixData = matrix.flatten()
    binaryData = np.concatenate([meta, matrixData])
    try:
        binaryData.tofile(filepath)
    except FileNotFoundError:
        raise

def loadMatrix(filepath: str):
    """
    load a matrix from a binary file at file path

    :param filepath: (str | Pathlike) the path to the binary file containing a (gonum) matrix
    :returns: (np.ndarray) The numpy array with data from the matrix saved at filepath
    :raises FileNotFoundError: If filepath does not point to a valid file
    :raises ValueError: If the matrix saved at filepath is invalid
    """

    try:
        metadata = np.fromfile(filepath, dtype="int", count=5)
    except FileNotFoundError:
        raise

    try:
        matrix = np.fromfile(filepath, offset=40)
    except FileNotFoundError:
        raise
    except ValueError:
        raise

    try:
        matrix = matrix.reshape(metadata[1], metadata[2])
    except ValueError:
        raise 

    return matrix

def saveVector(vec: np.ndarray, filepath):
    """
    Save a numpy vector to a binary file at file path, in a format that gonum can accept.

    Be aware this method will truncate any file it is pointed at!

    :param filepath: (str | Pathlike) the path to the binary save file
    :raises FileNotFoundError: If filepath is not valid
    """

    # My apologies for the magic number. See https://pkg.go.dev/gonum.org/v1/gonum@v0.12.0/mat#Dense.MarshalBinary for details
    meta = np.array([18373144242814977,vec.shape[0],vec.shape[1],0,0]).view("float")
    vecData = vec.flatten()
    binaryData = np.concatenate([meta, vecData])
    try:
        binaryData.tofile(filepath)
    except FileNotFoundError:
        raise

def loadVector(filepath):
    """
    load a vector from a binary file at file path

    :param filepath: (str | Pathlike) the path to the binary file containing a (gonum) vector
    :returns: (np.ndarray) The numpy array with data from the vector saved at filepath
    :raises FileNotFoundError: If filepath does not point to a valid file
    :raises ValueError: If the vector saved at filepath is invalid
    """

    try:
        metadata = np.fromfile(filepath, dtype="int", count=5)
    except FileNotFoundError:
        raise

    try:
        vec = np.fromfile(filepath, dtype=np.float64, offset=40)
    except FileNotFoundError:
        raise
    except ValueError:
        raise

    try:
        vec = vec.reshape(metadata[1])
    except ValueError:
        raise 

    return vec