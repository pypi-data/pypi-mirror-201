"""
Module for signal processing related LazyLinearOps (work in progress).
"""
import numpy as np
import scipy as sp
from lazylinop import *


def fft(n, backend='scipy', **kwargs):
    """
    Returns a LazyLinearOp for the DFT of size n.

    Args:
        backend:
             'scipy' (default) or 'pyfaust' for the underlying computation of the DFT.
        kwargs:
            any key-value pair arguments to pass to the scipy of pyfaust dft backend
            (https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html,
            https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600).

    Example:
        >>> #from lazylinop.wip.lsignal import fft
        >>> import numpy as np
        >>> lfft1 = fft(32, norm='ortho')
        >>> lfft2 = fft(32, backend='pyfaust')
        >>> x = np.random.rand(32)
        >>> np.allclose(lfft1 @ x, lfft2 @ x)
        True
        >>> y = lfft1 @ x
        >>> np.allclose(lfft1.H @ y, x)
        True
        >>> np.allclose(lfft2.H @ y, x)
        True

    """
    from scipy.fft import fft, ifft
    if backend == 'scipy':
        lfft = LazyLinearOperator(matmat=lambda x: fft(x, axis=0, **kwargs), rmatmat=lambda
                                  x: ifft(x, axis=0, **kwargs), shape=(n, n))
    elif backend == 'pyfaust':
        from pyfaust import dft
        lfft = aslazylinearoperator(dft(n, **kwargs))
    else:
        raise ValueError('backend '+str(backend)+' is unknown')
    return lfft

def fft2(shape, backend='scipy', **kwargs):
    """Returns a LazyLinearOp for the 2D DFT of size n.

    Args:
        shape:
             the signal shape to apply the fft2 to.
        backend:
             'scipy' (default) or 'pyfaust' for the underlying computation of the 2D DFT.
        kwargs:
             any key-value pair arguments to pass to the scipy or pyfaust dft backend
                (https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft2.html,
                https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600).

    Example:

        >>> #from lazylinop.wip.lsignal import fft2
        >>> import numpy as np
        >>> lfft2_scipy = fft2((32, 32), norm='ortho')
        >>> lfft2_pyfaust = fft2((32, 32), backend='pyfaust')
        >>> x = np.random.rand(32, 32)
        >>> np.allclose(lfft2_scipy @ x.ravel(), lfft2_pyfaust @ x.ravel())
        True
        >>> y = lfft2_scipy @ x.ravel()
        >>> np.allclose(lfft2_scipy.H @ y, x.ravel())
        True
        >>> np.allclose(lfft2_pyfaust.H @ y, x.ravel())
        True

    """
    s = shape[0] * shape[1]
    if backend == 'scipy':
        from scipy.fft import fft2, ifft2
        return LazyLinearOperator(
            (s, s),
            matvec=lambda x: fft2(x.reshape(shape), **kwargs).ravel(),
            rmatvec=lambda x: ifft2(x.reshape(shape), **kwargs).ravel())
    elif backend == 'pyfaust':
        from pyfaust import dft
        K = kron(dft(shape[0], **kwargs), dft(shape[1], **kwargs))
        return LazyLinearOperator((s, s), matvec=lambda x: K @ x,
                                  rmatvec=lambda x: K.H @ x)
    else:
        raise ValueError('backend '+str(backend)+' is unknown')

def convolve2d(signal_shape, kernel, backend='full_scipy'):
    """
    Builds the LazyLinearOp to convolves a kernel and a signal of shape signal_shape in 2D.

    Args:
        signal_shape:
             the shape of the signal this operator will convolves.
        kernel: (numpy array)
             the kernel to convolve.
        backend:
             'pyfaust' or 'scipy' to use lazylinop.fft2(backend='scipy') or 'full_scipy' to use scipy.signal.convolve2d.

    Returns:
        The LazyLinearOp for the 2D convolution.

    Example:
        >>> import numpy as np
        >>> #from lazylinop.wip.lsignal import convolve2d
        >>> from scipy.signal import convolve2d as sconvolve2d
        >>> X =  np.random.rand(64, 64)
        >>> K = np.random.rand(4, 4)
        >>> C1 = convolve2d(X.shape, K, backend='scipy')
        >>> C2 = convolve2d(X.shape, K, backend='pyfaust')
        >>> C3 = convolve2d(X.shape, K, backend='full_scipy')
        >>> np.allclose((C1 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True
        >>> np.allclose((C2 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True
        >>> np.allclose((C3 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True

    """

    import pylops
    signal_shape = np.array(signal_shape)
    if 'full_scipy'== backend:
        from scipy.signal import convolve2d as sconvolve2d, correlate2d
        return \
                LazyLinearOperator(shape=(signal_shape.prod(),signal_shape.prod()),
                                   matvec=lambda x:
                                   sconvolve2d(x.reshape(signal_shape), kernel,
                                              'same').ravel(),
                                   rmatvec=lambda x: correlate2d(x.reshape(signal_shape), kernel,
                                              'same').ravel())
    # Compute the extended shape for input and kernel to overlap
    new_shape = np.array(signal_shape) + np.array(kernel.shape) - 1
    # It must be a power of two
    new_shape = 2 ** (1 + np.int64(np.log2(new_shape)))

    # Input will be centered in the extended shpae
    pad_x = pylops.Pad(
        dims=signal_shape,
        pad=(
            ((new_shape[0] - signal_shape[0])//2, (new_shape[0] - signal_shape[0])//2),
            ((new_shape[1] - signal_shape[1])//2, (new_shape[1] - signal_shape[1])//2)
            )
    )

    # Kernel is spread at corners in the extended shape
    # TODO: Not sure of what I am doing...
    w_topleft = kernel[kernel.shape[0]//2-1:, kernel.shape[0]//2-1:]
    w_topright = kernel[kernel.shape[0]//2-1:, :kernel.shape[0]//2-1]
    w_bottomleft = kernel[:kernel.shape[0]//2-1, kernel.shape[0]//2-1:]
    w_bottomright = kernel[:kernel.shape[0]//2-1, :kernel.shape[0]//2-1]

    w_topright = np.vstack((w_topright, np.zeros((w_topleft.shape[0]-w_topright.shape[0], w_topright.shape[1]))))
    w_bottomleft = np.vstack((np.zeros((w_topleft.shape[0]-w_bottomleft.shape[0], w_bottomleft.shape[1])), w_bottomleft))
    w_bottomright = np.vstack((np.zeros((w_topleft.shape[0]-w_bottomright.shape[0], w_bottomright.shape[1])), w_bottomright))

    W_padded = np.vstack((
        np.hstack((w_topleft, np.zeros((w_topleft.shape[0], new_shape[1]-w_topleft.shape[1]-w_topright.shape[1])), w_topright)),
        np.zeros((new_shape[0]-w_topleft.shape[0]-w_bottomleft.shape[0], new_shape[1])),
        np.hstack((w_bottomleft, np.zeros((w_bottomleft.shape[0], new_shape[1]-w_bottomleft.shape[1]-w_bottomright.shape[1])), w_bottomright))
        )).ravel()
    # TODO: This make lazylinop crash
    #W_padded = scipy.sparse.csc_array(W_padded).reshape((-1, 1))

    #dft2_ = dft2(new_shape)
    if backend == 'pyfaust':
        dft2_ = fft2(new_shape, backend=backend, normed=True, diag_opt=True)
    elif backend == 'scipy':
        dft2_ = fft2(new_shape, backend=backend, norm='ortho')
    else:
        raise ValueError('Unknown backend')
    # For Fourier normalization
    n = new_shape.prod()

    dft2_W = dft2_ @ W_padded

    # TODO: Make it more efficient using sparse or operator?

    return LazyLinearOperator(
        (signal_shape.prod(), signal_shape.prod()),
        matvec=lambda x: pad_x.H @ (1 / np.sqrt(n) * dft2_.H @ (n * dft2_W * (dft2_ @ pad_x @ x))),
                       # pad_x.H is used to reproject from the extended shpae to the original one
        rmatvec=lambda x: (pad_x.H @ (1 / np.sqrt(n) * dft2_.H @ (n * dft2_W * (dft2_ @ pad_x @ x[::-1]) )))[::-1]
         # TODO: something clever for the adjoint?
    )
def _binary_dtype(A_dtype, B_dtype):
    if isinstance(A_dtype, str):
        A_dtype = np.dtype(A_dtype)
    if isinstance(B_dtype, str):
        B_dtype = np.dtype(B_dtype)
    if A_dtype is None:
        return B_dtype
    if B_dtype is None:
        return A_dtype
    if A_dtype is None and B_dtype is None:
        return None
    kinds = [A_dtype.kind, B_dtype.kind]
    if A_dtype.kind == B_dtype.kind:
        dtype = A_dtype if A_dtype.itemsize > B_dtype.itemsize else B_dtype
    elif 'c' in [A_dtype.kind, B_dtype.kind]:
        dtype = 'complex'
    elif 'f' in kinds:
        dtype = 'double'
    else:
        dtype = A_dtype
    return dtype

def _is_power_of_two(n: int) -> bool:
    """return True if integer 'n' is a power of two.
    Parameters
    ----------
    n : int
    Returns
    -------
    bool
    Raises
    ------
    """
    return ((n & (n - 1)) == 0) and n > 0

def pyfaust_convolve(kernel: np.ndarray, mode: str = 'full', boundary: str = 'fill', use_scipy_toeplitz: bool = True, **kwargs):
    """If shape of the signal has been passed return Lazy Linear Operator that corresponds
    to the convolution with the kernel. If signal has been passed return the convolution result.
    The function determines if it is 1D or 2D convolution based on the number of dimensions of the kernel.

    Args:
        kernel: np.ndarray,
             kernel to use for the convolution, shape is (K, ) for 1D and (K, L) for 2D
        mode: str,
             'full' computes convolution (input + padding)
             'valid' computes 'full' mode and extract centered output that does not depend on the padding.
             'same' computes 'full' mode and extract centered output that has the same shape that the input.
             refer to Scipy documentation of scipy.signal.convolve function for more details
        boundary: str,
               refer to Scipy documentation of scipy.signal.convolve2d function
        backend: str,
              'pyfaust' (default) or 'scipy' for the underlying computation of the convolution
        use_scipy_toeplitz: bool,
                         True (default) to use Scipy implementation of Toeplitz matrix
                         False to use pyfaust implementation

        kwargs:
            shape: (tuple)
                 of the signal to convolve with kernel.
            input_array: (np.ndarray)
                 to convolve with kernel, shape is (S, ) or (S, T)

    Returns:
        LazyLinearOperator or np.ndarray

    Raises:
        
        ValueError
            number of dimensions of the signal and/or the kernel is greater than one.
        ValueError
            mode is either 'full' (default), 'valid' or 'same'
        ValueError
            boundary is either 'fill' (default), 'wrap' or 'symm'
        ValueError
            backend is either 'pyfaust' (defualt) or 'scipy'
        ValueError
            'shape' or 'input_array' are expected
        ValueError
            expect 'shape' or 'input_array' not both.

    Examples:
        >>> image = np.random.rand(6, 6)
        >>> kernel = np.random.rand(3, 3)
        >>> c1 = np.real(pyfaust_convolve(kernel, mode='same', shape=image.shape) @ image.flatten()).reshape(image.shape)
        >>> c2 = convolve2d(image, kernel, mode='same', boundary='fill')
        >>> print(np.allclose(c1, c2))
    """
    from pyfaust import toeplitz
    if not mode in ['full', 'valid', 'same']:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'")
    if not boundary in ['fill', 'wrap', 'symm']:
        raise ValueError("boundary is either 'fill' (default), 'wrap' or 'symm'")
    # if not backend in ['pyfaust', 'scipy']:
    #     raise ValueError("backend is either 'pyfaust' (defualt) or 'scipy'")
    if not "shape" in kwargs.keys() and not "input_array" in kwargs.keys():
        raise ValueError("'shape' or 'input_array' are expected")
    if "shape" in kwargs.keys() and "input_array" in kwargs.keys():
        raise ValueError("expect 'shape' or 'input_array' not both.")

    # check if signal/image has been passed to the function
    # check if shape of the signal has been passed to the function
    return_lazylinop = True
    for key, value in kwargs.items():
        if key == "shape":
            return_lazylinop = True
            shape = value
        elif key == "input_array":
            return_lazylinop = False
            if kernel.ndim == 1:
                # signal
                signal = np.copy(value)
                shape = signal.shape
            elif kernel.ndim == 2:
                # image
                image = np.copy(value)
                shape = image.shape
            else:
                pass
        else:
            pass

    # convolution
    if kernel.ndim == 1:
        # 1D convolution
        if shape[0] <= 0 or kernel.ndim != 1:
            raise ValueError("number of dimensions of the signal and/or the kernel is not equal to 1.")
        K = kernel.size
        S = shape[0]
        if return_lazylinop:
            # return lazy linear operator
            if mode == 'valid':
                # compute full mode and extract what we need
                start = (S + K - 1) // 2 - (S - K + 1) // 2
                if use_scipy_toeplitz:
                    return aslazylinearoperator(sp.linalg.toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)))[start:(start + S - K + 1), :S])
                else:
                    return aslazylinearoperator(toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)), diag_opt=True)[start:(start + S - K + 1), :S])
            elif mode == 'same':
                # keep the middle of full mode
                start = (S + K - 1 - S) // 2
                if use_scipy_toeplitz:
                    return aslazylinearoperator(sp.linalg.toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)))[start:(start + S), :S])
                else:
                    return aslazylinearoperator(toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)), diag_opt=True)[start:(start + S), :S])
            else:
                # compute full mode
                if use_scipy_toeplitz:
                    return aslazylinearoperator(sp.linalg.toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1))))
                else:
                    return aslazylinearoperator(toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)), diag_opt=True))
        else:
            # return result of the convolution
            if mode == 'valid':
                # compute full mode and extract what we need
                start = (S + K - 1) // 2 - (S - K + 1) // 2
                if use_scipy_toeplitz:
                    return aslazylinearoperator(sp.linalg.toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)))[start:(start + S - K + 1), :S]) @ signal
                else:
                    return aslazylinearoperator(toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)), diag_opt=True)[start:(start + S - K + 1), :S]) @ signal
            elif mode == 'same':
                # keep the middle of full mode
                start = (S + K - 1 - S) // 2
                if use_scipy_toeplitz:
                    return aslazylinearoperator(sp.linalg.toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)))[start:(start + S), :S]) @ signal
                else:
                    return aslazylinearoperator(toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)), diag_opt=True)[start:(start + S), :S]) @ signal
            else:
                # compute full mode
                if use_scipy_toeplitz:
                    return aslazylinearoperator(sp.linalg.toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)))) @ signal
                else:
                    return aslazylinearoperator(toeplitz(np.pad(kernel, (0, S - 1)), np.pad(np.array([kernel[0]]), (0, S - 1)), diag_opt=True)) @ signal
    elif kernel.ndim == 2:
        # 2D convolution
        if shape[1] <= 0:
            raise ValueError("number of dimensions of the image is not equal to 2.")
        M, N = shape[0], shape[1]
        K, L = kernel.shape
        pad_kernel = np.pad(kernel, ((0, M - 1), (0, N - 1)), mode='constant', constant_values=0)
        # shape of the output image (full mode)
        X, Y = M + K - 1, N + L - 1
        # write 2d convolution as a sum of Kronecker products:
        # convolution(kernel, image) = sum(kron(A_i, B_i), i, 1, M)
        # A_i is a Toeplitz matrix.
        # first column is 0 except for element i that is 1
        # first row is 0
        # B_i is a Toeplitz matrix build from the kernel.
        # first column is the i-th row of the kernel
        # first row is 0
        LO = [None] * K
        r1 = np.zeros(N, dtype=np.int32)
        r2 = np.zeros(N, dtype=kernel.dtype)
        c1 = np.zeros(M + K - 1, dtype=np.int32)
        for i in range(K):
            c1[i] = 1
            LO[i] = kron(sp.linalg.toeplitz(c1, r1), sp.linalg.toeplitz(pad_kernel[i, :], r2), use_pylops=True) if use_scipy_toeplitz else kron(toeplitz(c1, r1, diag_opt=True), toeplitz(pad_kernel[i, :], r2, diag_opt=True), use_pylops=True)
            c1[i] = 0
        # return lazy linear operator or the convolution result
        if return_lazylinop:
            if mode == 'valid':
                # compute full mode and extract what we need
                # number of rows to extract is M - K + 1
                i1 = (X - (M - K + 1)) // 2
                s1 = i1 + M - K + 1
                indices = np.add(np.outer(np.multiply(Y, np.arange(i1, s1)), np.full(M - K + 1, 1)), np.outer(np.full(M - K + 1, 1), np.arange(i1, s1))).flatten()
                return (sum(*LO))[indices, :]
            elif mode == 'same':
                # keep middle of the full mode
                # number of rows to extract is M
                # centered
                i1 = (X - M) // 2
                s1 = i1 + M
                indices = np.add(np.outer(np.multiply(Y, np.arange(i1, s1)), np.full(M, 1)), np.outer(np.full(M, 1), np.arange(i1, s1))).flatten()
                return (sum(*LO))[indices, :]
            else:
                # return full mode
                return sum(*LO)
        else:
            if mode == 'valid':
                # compute full mode result and extract what we need
                # number of rows to extract is M - K + 1
                i1 = (X - (M - K + 1)) // 2# K
                s1 = i1 + M - K + 1# M + 1
                i2 = (Y - (N - L + 1)) // 2# L
                s2 = i2 + N - L + 1# N + 1
                return ((sum(*LO) @ image.flatten()).reshape(X, Y))[i1: s1, i2: s2]
            elif mode == 'same':
                # keep middle of the full mode result
                # number of rows to extract is M
                # centered
                i1 = (X - M) // 2#(K - 1) // 2
                s1 = i1 + M
                i2 = (Y - N) // 2#(L - 1) // 2
                s2 = i2 + N
                return ((sum(*LO) @ image.flatten()).reshape(X, Y))[i1: s1, i2: s2]
            else:
                # compute full mode
                return (sum(*LO) @ image.flatten()).reshape(X, Y)


def pyfaust_oaconvolve(kernel: np.ndarray, mode: str = 'full', **kwargs):
    """This function implements overlap-add method for convolution.
    If shape of the signal has been passed return Lazy Linear Operator
    that corresponds to the convolution with the kernel.
    If signal has been passed return the convolution result.
    The function only considers the first dimension of both kernel and signal.

    Args:
        kernel: np.ndarray
                kernel to use for the convolution, shape is (K, ) for 1D and (K, L) for 2D.
        mode: str,
             'full' computes convolution (input + padding)
             'valid' computes 'full' mode and extract centered output that does not depend on the padding.
             'same' computes 'full' mode and extract centered output that has the same shape that the input.
             refer to Scipy documentation of scipy.signal.convolve function for more details.
        kwargs:
            shape: (tuple)
                of the signal to convolve with kernel.
            input_array: (np.ndarray)
                to convolve with kernel, shape is (S, ).
            block_size: (int)
                size of the block unit (a power of two).

    Return:
        LazyLinearOperator or np.ndarray

    Raises:
        Exception
        kernel number of dimensions < 1.
        ValueError
        mode is either 'full' (default), 'valid' or 'same'
        ValueError
        'shape' or 'input_array' are expected
        ValueError
        expect 'shape' or 'input_array' not both.
        ValueError
        'block_size' argument expects a value that is a power of two.
        ValueError
        'block_size' must be greater than the kernel size.

    Examples:
        >>> signal = np.random.rand(32768)
        >>> kernel = np.random.rand(4)
        >>> c1 = np.real(pyfaust_oaconvolve(kernel, mode='same', input_array=signal))
        >>> c2 = oaconvolve(signal, kernel, mode='same')
        >>> print(np.allclose(c1, c2))
    """
    if not mode in ['full', 'valid', 'same']:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'")
    if not "shape" in kwargs.keys() and not "input_array" in kwargs.keys():
        raise ValueError("'shape' or 'input_array' are expected")
    if "shape" in kwargs.keys() and "input_array" in kwargs.keys():
        raise ValueError("expect 'shape' or 'input_array' not both.")

    # check if signal has been passed to the function
    # check if shape of the signal has been passed to the function
    return_lazylinop, B = True, 2
    for key, value in kwargs.items():
        if key == "shape":
            return_lazylinop = True
            shape = value
        elif key == "input_array":
            return_lazylinop = False
            if value.ndim == 1:
                # signal
                signal1d = np.copy(value)
                shape = signal1d.shape
            elif value.ndim > 1:
                # keep only the first dimension of the signal
                signal1d = np.copy(value[:1])
                shape = signal1d.shape
            else:
                pass
        elif key == "block_size":
            B = value
            if B <= 0 or not _is_power_of_two(B):
                raise ValueError("block_size argument expects a value that is a power of two.")
        else:
            pass

    # keep only the first dimension of the kernel
    if kernel.ndim == 1:
        kernel1d = np.copy(kernel)
    elif kernel.ndim > 1:
        kernel1d = np.copy(kernel[:1])
    else:
        raise Exception("kernel number of dimensions < 1.")

    # size of the kernel
    K = kernel1d.size
    # size of the signal
    S = shape[0]
    # size of the output (full mode)
    O = S + K - 1

    # block size B, number of blocks X=S/B
    if not "block_size" in kwargs.keys():
        # no input for the block size: compute a value
        B = 3 * K
        while B < (4 * K) or not _is_power_of_two(B):
            B += 1
    if B <= K:
        raise ValueError("block_size must be greater than the kernel size.")
    # number of blocks
    R = S % B
    X = (S + R) // B

    # pad kernel
    pkernel = np.pad(kernel1d, ((0, 2 * B - K)))

    # create linear operator LO that will be applied to all the blocks
    # LO = ifft(np.diag(fft(kernel)) @ fft(signal))
    # use Kronecker product between identity matrix and LO to apply to all the blocks
    # use pyfaust_multi_pad to pad each block
    # if the size of the signal is S the size of the result is 2*S
    norm = False
    from pyfaust import dft
    LO = kron(eye(X, n=X, k=0), aslazylinearoperator(dft(2 * B, normed=norm).T.conj()) @ diag(dft(2 * B, normed=norm) @ np.multiply(1.0 if norm else 1.0 / (2 * B), pkernel), k=0) @ aslazylinearoperator(dft(2 * B, normed=norm)) @ pyfaust_multi_pad(B, 1), use_pylops=True)

    # convolution
    if return_lazylinop:
        # return lazy linear operator
        if mode == 'valid':
            # compute full mode and extract what we need
            start = O // 2 - (S - K + 1) // 2
            return (pyfaust_overlap_add(B, X) @ LO)[start:(start + S - K + 1), :]
        elif mode == 'same':
            # keep the middle of full mode (centered)
            start = O // 2 - S // 2
            return (pyfaust_overlap_add(B, X) @ LO)[start:(start + S), :]
        else:
            # compute full mode
            return (pyfaust_overlap_add(B, X) @ LO)[:O, :S]
    else:
        # return result of the convolution
        psignal = np.pad(signal1d, ((0, R)))
        if mode == 'valid':
            # compute full mode and extract what we need
            start = O // 2 - (S - K + 1) // 2
            return (pyfaust_overlap_add(B, X, None) @ LO @ psignal)[start:(start + S - K + 1)]
        elif mode == 'same':
            # keep the middle of full mode (centered)
            start = O // 2 - S // 2
            return (pyfaust_overlap_add(B, X, None) @ LO @ psignal)[start:(start + S)]
        else:
            # compute full mode
            return (pyfaust_overlap_add(B, X, None) @ LO @ psignal)[:O]


def pyfaust_multi_pad(L: int, X: int) -> LazyLinearOp:
    """return a lazy linear operator mp to pad each block of a signal of length L * X.
    if you apply this operator to a vector of length L * X the output will be of length 2 * L * X.
    the operator looks like:
    mp = (1 0 0 0 ... 0)
    (0 0 0 0 ... 0)
    (0 1 0 0 ... 0)
    (0 0 0 0 ... 0)
    (0 0 1 0 ... 0)
    (.           .)
    (.           .)
    (.           .)
    (.           1)
    (0 0 0 0 ... 0)

     Args:
         L: int
             block size
         X: int
             number of blocks

     Returns:
        LazyLinearOp


    Examples:
        >>> signal = np.full(5, 1.0)
        >>> print(signal)
        >>> [1. 1. 1. 1. 1.]
        >>> print(signal.shape)
        >>> (5,)
        >>> print(pyfaust_multi_pad(1, 5) @ signal)
        >>> [1. 0. 1. 0. 1. 0. 1. 0. 1. 0.]
        >>> print((pyfaust_multi_pad(1, 5) @ signal).shape)
        >>> (10,)
    """
    mp = np.zeros((2 * X, X))
    for x in np.arange(0, 2 * X, 2):
        mp[x, x // 2] = 1
    return kron(mp, eye(L, n=L, k=0), use_pylops=True)


def pyfaust_overlap_add(L: int, X: int, signal = None):
    """return overlap-add linear operator.
    if signal is a numpy array return the result of the matrix-vector product.
    overlap-add linear operator is given by:
    (I 0 0 0 0 0 ... 0)
    (0 I I 0 0 0 ... 0)
    (0 0 0 I I 0 ... 0)
    .                .
    .                .
    .                .
    (0 0 0 0 0 0 ... I)
    where I (shape is (L, L)) is the identity matrix.
    The overlap-add linear operator adds last L samples from previous
    block with first L samples from current block.

    Args:
        L: int
            block size
        X: int
            number of blocks
        signal: np.ndarray,
            if signal is numpy array apply overlap-add linear operator (default is None).
            function only considers first dimension of the signal argument.

    Returns:
        aslazylinearoperator or np.ndarray

    Raises:
        ValueError
            L is strictly positive.
        ValueError
            X is strictly positive.
        ValueError
            number of columns of the linear operator is not equal to the size of the signal.

    Examples:
        >>> signal = np.full(16, 1.0)
        >>> oa1 = pyfaust_overlap_add(2, 4, None) @ signal
        >>> oa2 = pyfaust_overlap_add(2, 4, signal)
        >>> np.allclose(oa1, oa2)
    """
    if L <= 0:
        raise ValueError("L is strictly positive.")
    if X <= 0:
        raise ValueError("X is strictly positive.")
    if (2 * X * L) != signal.size:
        raise ValueError("number of columns of the linear operator is not equal to the size of the signal.")
    oa = np.full((X + 1, 2 * X), 0.0)
    oa[0, 0] = 1
    for x in range(1, X + 1 - 1):
        oa[x, 2 * (x - 1) + 1] = 1
        oa[x, 2 * (x - 1) + 2] = 1
    oa[X + 1 - 1, 2 * (X - 1) + 1] = 1
    if type(signal) is np.ndarray:
        return aslazylinearoperator(kron(oa, eye(L, n=L, k=0), use_pylops=True)) @ signal
    else:
        return aslazylinearoperator(kron(oa, eye(L, n=L, k=0), use_pylops=True))
