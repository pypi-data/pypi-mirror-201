'''This Python code is an automatically generated wrapper
for Fortran code made by 'fmodpy'. The original documentation
for the Fortran source code follows.

! Module for matrix multiplication (absolutely crucial for APOS speed).
! Includes routines for orthogonalization, computing the SVD, and
! radializing data matrices with the SVD.
'''

import os
import ctypes
import platform
import numpy

# --------------------------------------------------------------------
#               CONFIGURATION
# 
_verbose = True
_fort_compiler = "gfortran"
_shared_object_name = "axy_matrix_operations." + platform.machine() + ".so"
_this_directory = os.path.dirname(os.path.abspath(__file__))
_path_to_lib = os.path.join(_this_directory, _shared_object_name)
_compile_options = ['-fPIC', '-shared', '-O3', '-lblas', '-llapack']
_ordered_dependencies = ['axy_matrix_operations.f90', 'axy_matrix_operations_c_wrapper.f90']
_symbol_files = []# 
# --------------------------------------------------------------------
#               AUTO-COMPILING
#
# Try to import the prerequisite symbols for the compiled code.
for _ in _symbol_files:
    _ = ctypes.CDLL(os.path.join(_this_directory, _), mode=ctypes.RTLD_GLOBAL)
# Try to import the existing object. If that fails, recompile and then try.
try:
    clib = ctypes.CDLL(_path_to_lib)
except:
    # Remove the shared object if it exists, because it is faulty.
    if os.path.exists(_shared_object_name):
        os.remove(_shared_object_name)
    # Compile a new shared object.
    _command = " ".join([_fort_compiler] + _compile_options + ["-o", _shared_object_name] + _ordered_dependencies)
    if _verbose:
        print("Running system command with arguments")
        print("  ", _command)
    # Run the compilation command.
    import subprocess
    subprocess.run(_command, shell=True, cwd=_this_directory)
    # Import the shared object file as a C library with ctypes.
    clib = ctypes.CDLL(_path_to_lib)
# --------------------------------------------------------------------


class matrix_operations:
    ''''''

    # Declare 'pi'
    def get_pi(self):
        pi = ctypes.c_float()
        clib.matrix_operations_get_pi(ctypes.byref(pi))
        return pi.value
    def set_pi(self, pi):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    pi = property(get_pi, set_pi)

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine GEMM
    
    def gemm(self, op_a, op_b, out_rows, out_cols, inner_dim, ab_mult, a, a_rows, b, b_rows, c_mult, c, c_rows):
        '''! Convenience wrapper routine for calling matrix multiply.
!
! TODO: For very large data, automatically batch the operations to reduce
!       the size of the temporary space that is needed.'''
        
        # Setting up "op_a"
        if (type(op_a) is not ctypes.c_char): op_a = ctypes.c_char(op_a)
        
        # Setting up "op_b"
        if (type(op_b) is not ctypes.c_char): op_b = ctypes.c_char(op_b)
        
        # Setting up "out_rows"
        if (type(out_rows) is not ctypes.c_int): out_rows = ctypes.c_int(out_rows)
        
        # Setting up "out_cols"
        if (type(out_cols) is not ctypes.c_int): out_cols = ctypes.c_int(out_cols)
        
        # Setting up "inner_dim"
        if (type(inner_dim) is not ctypes.c_int): inner_dim = ctypes.c_int(inner_dim)
        
        # Setting up "ab_mult"
        if (type(ab_mult) is not ctypes.c_float): ab_mult = ctypes.c_float(ab_mult)
        
        # Setting up "a"
        if ((not issubclass(type(a), numpy.ndarray)) or
            (not numpy.asarray(a).flags.f_contiguous) or
            (not (a.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a = numpy.asarray(a, dtype=ctypes.c_float, order='F')
        a_dim_1 = ctypes.c_long(a.shape[0])
        a_dim_2 = ctypes.c_long(a.shape[1])
        
        # Setting up "a_rows"
        if (type(a_rows) is not ctypes.c_int): a_rows = ctypes.c_int(a_rows)
        
        # Setting up "b"
        if ((not issubclass(type(b), numpy.ndarray)) or
            (not numpy.asarray(b).flags.f_contiguous) or
            (not (b.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'b' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            b = numpy.asarray(b, dtype=ctypes.c_float, order='F')
        b_dim_1 = ctypes.c_long(b.shape[0])
        b_dim_2 = ctypes.c_long(b.shape[1])
        
        # Setting up "b_rows"
        if (type(b_rows) is not ctypes.c_int): b_rows = ctypes.c_int(b_rows)
        
        # Setting up "c_mult"
        if (type(c_mult) is not ctypes.c_float): c_mult = ctypes.c_float(c_mult)
        
        # Setting up "c"
        if ((not issubclass(type(c), numpy.ndarray)) or
            (not numpy.asarray(c).flags.f_contiguous) or
            (not (c.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'c' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            c = numpy.asarray(c, dtype=ctypes.c_float, order='F')
        c_dim_1 = ctypes.c_long(c.shape[0])
        c_dim_2 = ctypes.c_long(c.shape[1])
        
        # Setting up "c_rows"
        if (type(c_rows) is not ctypes.c_int): c_rows = ctypes.c_int(c_rows)
    
        # Call C-accessible Fortran wrapper.
        clib.c_gemm(ctypes.byref(op_a), ctypes.byref(op_b), ctypes.byref(out_rows), ctypes.byref(out_cols), ctypes.byref(inner_dim), ctypes.byref(ab_mult), ctypes.byref(a_dim_1), ctypes.byref(a_dim_2), ctypes.c_void_p(a.ctypes.data), ctypes.byref(a_rows), ctypes.byref(b_dim_1), ctypes.byref(b_dim_2), ctypes.c_void_p(b.ctypes.data), ctypes.byref(b_rows), ctypes.byref(c_mult), ctypes.byref(c_dim_1), ctypes.byref(c_dim_2), ctypes.c_void_p(c.ctypes.data), ctypes.byref(c_rows))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return c

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine SYRK
    
    def syrk(self, uplo, trans, n, k, alpha, a, lda, beta, c, ldc):
        '''! Convenience wrapper routine for calling symmetric matrix multiplication.'''
        
        # Setting up "uplo"
        if (type(uplo) is not ctypes.c_char): uplo = ctypes.c_char(uplo)
        
        # Setting up "trans"
        if (type(trans) is not ctypes.c_char): trans = ctypes.c_char(trans)
        
        # Setting up "n"
        if (type(n) is not ctypes.c_int): n = ctypes.c_int(n)
        
        # Setting up "k"
        if (type(k) is not ctypes.c_int): k = ctypes.c_int(k)
        
        # Setting up "alpha"
        if (type(alpha) is not ctypes.c_float): alpha = ctypes.c_float(alpha)
        
        # Setting up "a"
        if ((not issubclass(type(a), numpy.ndarray)) or
            (not numpy.asarray(a).flags.f_contiguous) or
            (not (a.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a = numpy.asarray(a, dtype=ctypes.c_float, order='F')
        a_dim_1 = ctypes.c_long(a.shape[0])
        a_dim_2 = ctypes.c_long(a.shape[1])
        
        # Setting up "lda"
        if (type(lda) is not ctypes.c_int): lda = ctypes.c_int(lda)
        
        # Setting up "beta"
        if (type(beta) is not ctypes.c_float): beta = ctypes.c_float(beta)
        
        # Setting up "c"
        if ((not issubclass(type(c), numpy.ndarray)) or
            (not numpy.asarray(c).flags.f_contiguous) or
            (not (c.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'c' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            c = numpy.asarray(c, dtype=ctypes.c_float, order='F')
        c_dim_1 = ctypes.c_long(c.shape[0])
        c_dim_2 = ctypes.c_long(c.shape[1])
        
        # Setting up "ldc"
        if (type(ldc) is not ctypes.c_int): ldc = ctypes.c_int(ldc)
    
        # Call C-accessible Fortran wrapper.
        clib.c_syrk(ctypes.byref(uplo), ctypes.byref(trans), ctypes.byref(n), ctypes.byref(k), ctypes.byref(alpha), ctypes.byref(a_dim_1), ctypes.byref(a_dim_2), ctypes.c_void_p(a.ctypes.data), ctypes.byref(lda), ctypes.byref(beta), ctypes.byref(c_dim_1), ctypes.byref(c_dim_2), ctypes.c_void_p(c.ctypes.data), ctypes.byref(ldc))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return c

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine ORTHOGONALIZE
    
    def orthogonalize(self, a, lengths, rank=None, order=None, multipliers=None):
        '''! Orthogonalize and normalize column vectors of A with pivoting.'''
        
        # Setting up "a"
        if ((not issubclass(type(a), numpy.ndarray)) or
            (not numpy.asarray(a).flags.f_contiguous) or
            (not (a.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a = numpy.asarray(a, dtype=ctypes.c_float, order='F')
        a_dim_1 = ctypes.c_long(a.shape[0])
        a_dim_2 = ctypes.c_long(a.shape[1])
        
        # Setting up "lengths"
        if ((not issubclass(type(lengths), numpy.ndarray)) or
            (not numpy.asarray(lengths).flags.f_contiguous) or
            (not (lengths.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'lengths' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            lengths = numpy.asarray(lengths, dtype=ctypes.c_float, order='F')
        lengths_dim_1 = ctypes.c_long(lengths.shape[0])
        
        # Setting up "rank"
        rank_present = ctypes.c_bool(True)
        if (rank is None):
            rank_present = ctypes.c_bool(False)
            rank = ctypes.c_int()
        else:
            rank = ctypes.c_int(rank)
        
        # Setting up "order"
        order_present = ctypes.c_bool(True)
        if (order is None):
            order_present = ctypes.c_bool(False)
            order = numpy.zeros(shape=(1), dtype=ctypes.c_int, order='F')
        elif (type(order) == bool) and (order):
            order = numpy.zeros(shape=(1), dtype=ctypes.c_int, order='F')
        elif ((not issubclass(type(order), numpy.ndarray)) or
              (not numpy.asarray(order).flags.f_contiguous) or
              (not (order.dtype == numpy.dtype(ctypes.c_int)))):
            import warnings
            warnings.warn("The provided argument 'order' was not an f_contiguous NumPy array of type 'ctypes.c_int' (or equivalent). Automatically converting (probably creating a full copy).")
            order = numpy.asarray(order, dtype=ctypes.c_int, order='F')
        if (order_present):
            order_dim_1 = ctypes.c_long(order.shape[0])
        else:
            order_dim_1 = ctypes.c_long()
        
        # Setting up "multipliers"
        multipliers_present = ctypes.c_bool(True)
        if (multipliers is None):
            multipliers_present = ctypes.c_bool(False)
            multipliers = numpy.zeros(shape=(1,1), dtype=ctypes.c_float, order='F')
        elif (type(multipliers) == bool) and (multipliers):
            multipliers = numpy.zeros(shape=(1,1), dtype=ctypes.c_float, order='F')
        elif ((not issubclass(type(multipliers), numpy.ndarray)) or
              (not numpy.asarray(multipliers).flags.f_contiguous) or
              (not (multipliers.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'multipliers' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            multipliers = numpy.asarray(multipliers, dtype=ctypes.c_float, order='F')
        if (multipliers_present):
            multipliers_dim_1 = ctypes.c_long(multipliers.shape[0])
            multipliers_dim_2 = ctypes.c_long(multipliers.shape[1])
        else:
            multipliers_dim_1 = ctypes.c_long()
            multipliers_dim_2 = ctypes.c_long()
    
        # Call C-accessible Fortran wrapper.
        clib.c_orthogonalize(ctypes.byref(a_dim_1), ctypes.byref(a_dim_2), ctypes.c_void_p(a.ctypes.data), ctypes.byref(lengths_dim_1), ctypes.c_void_p(lengths.ctypes.data), ctypes.byref(rank_present), ctypes.byref(rank), ctypes.byref(order_present), ctypes.byref(order_dim_1), ctypes.c_void_p(order.ctypes.data), ctypes.byref(multipliers_present), ctypes.byref(multipliers_dim_1), ctypes.byref(multipliers_dim_2), ctypes.c_void_p(multipliers.ctypes.data))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return a, lengths, (rank.value if rank_present else None), (order if order_present else None), (multipliers if multipliers_present else None)

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine SVD
    
    def svd(self, a, s, vt, rank=None, steps=None, bias=None):
        '''! Compute the singular values and right singular vectors for matrix A.
!
! TODO: Add an INFO flag that can be used to raise errors.
! TODO: Move allocation to be allowed as input.'''
        
        # Setting up "a"
        if ((not issubclass(type(a), numpy.ndarray)) or
            (not numpy.asarray(a).flags.f_contiguous) or
            (not (a.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a = numpy.asarray(a, dtype=ctypes.c_float, order='F')
        a_dim_1 = ctypes.c_long(a.shape[0])
        a_dim_2 = ctypes.c_long(a.shape[1])
        
        # Setting up "s"
        if ((not issubclass(type(s), numpy.ndarray)) or
            (not numpy.asarray(s).flags.f_contiguous) or
            (not (s.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 's' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            s = numpy.asarray(s, dtype=ctypes.c_float, order='F')
        s_dim_1 = ctypes.c_long(s.shape[0])
        
        # Setting up "vt"
        if ((not issubclass(type(vt), numpy.ndarray)) or
            (not numpy.asarray(vt).flags.f_contiguous) or
            (not (vt.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'vt' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            vt = numpy.asarray(vt, dtype=ctypes.c_float, order='F')
        vt_dim_1 = ctypes.c_long(vt.shape[0])
        vt_dim_2 = ctypes.c_long(vt.shape[1])
        
        # Setting up "rank"
        rank_present = ctypes.c_bool(True)
        if (rank is None):
            rank_present = ctypes.c_bool(False)
            rank = ctypes.c_int()
        else:
            rank = ctypes.c_int(rank)
        
        # Setting up "steps"
        steps_present = ctypes.c_bool(True)
        if (steps is None):
            steps_present = ctypes.c_bool(False)
            steps = ctypes.c_int()
        else:
            steps = ctypes.c_int(steps)
        if (type(steps) is not ctypes.c_int): steps = ctypes.c_int(steps)
        
        # Setting up "bias"
        bias_present = ctypes.c_bool(True)
        if (bias is None):
            bias_present = ctypes.c_bool(False)
            bias = ctypes.c_float()
        else:
            bias = ctypes.c_float(bias)
        if (type(bias) is not ctypes.c_float): bias = ctypes.c_float(bias)
    
        # Call C-accessible Fortran wrapper.
        clib.c_svd(ctypes.byref(a_dim_1), ctypes.byref(a_dim_2), ctypes.c_void_p(a.ctypes.data), ctypes.byref(s_dim_1), ctypes.c_void_p(s.ctypes.data), ctypes.byref(vt_dim_1), ctypes.byref(vt_dim_2), ctypes.c_void_p(vt.ctypes.data), ctypes.byref(rank_present), ctypes.byref(rank), ctypes.byref(steps_present), ctypes.byref(steps), ctypes.byref(bias_present), ctypes.byref(bias))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return s, vt, (rank.value if rank_present else None)

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine RADIALIZE
    
    def radialize(self, x, shift, vecs, inverse=None, maxbound=None, max_to_flatten=None, max_to_square=None, svd_steps=None):
        '''! If there are at least as many data points as dimension, then
! compute the principal components and rescale the data by
! projecting onto those and rescaling so that each component has
! identical singular values (this makes the data more "radially
! symmetric").
!
!   X -- The real data matrix, column vectors (a "point" is a column).
!
!   SHIFT -- The real vector that is added to X in order to center it about the origin.
!
!   VECS -- The approximate principal components of the data, these are the orthogonal
!           column vectors about which the data in X is rotated. Notably, they are NOT
!           necessarily unit length, because they are rescaled to achieve the desired
!           properties in X (which property is determined by MAXBOUND setting).
!
!   INVERSE -- Optional output, the inverse of VECS.
!
!   MAX_TO_FLATTEN -- Optional input, the integer maximum number of components to flatten
!                     (rescale by their singular value) while the rest simply get divided
!                     by the first (maximum) singular value.
!
!   MAXBOUND -- Optional input, TRUE to normalize by the firs (maximum) singular value,
!               dfeaults to FALSE, to normalize so that the 2-norm of the data matrix is 1.
!
!   MAX_TO_SQUARE -- Optional, the integer maximum number of points (second component of X)
!                    that will be considered for the routine (to bound compute for large data).
!
!   SVD_STEPS -- Optional input, the integer number of power-iterations to take when estimating
!                the principal components of the data with the SVD of the covariance matrix.'''
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
        
        # Setting up "shift"
        if ((not issubclass(type(shift), numpy.ndarray)) or
            (not numpy.asarray(shift).flags.f_contiguous) or
            (not (shift.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'shift' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            shift = numpy.asarray(shift, dtype=ctypes.c_float, order='F')
        shift_dim_1 = ctypes.c_long(shift.shape[0])
        
        # Setting up "vecs"
        if ((not issubclass(type(vecs), numpy.ndarray)) or
            (not numpy.asarray(vecs).flags.f_contiguous) or
            (not (vecs.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'vecs' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            vecs = numpy.asarray(vecs, dtype=ctypes.c_float, order='F')
        vecs_dim_1 = ctypes.c_long(vecs.shape[0])
        vecs_dim_2 = ctypes.c_long(vecs.shape[1])
        
        # Setting up "inverse"
        inverse_present = ctypes.c_bool(True)
        if (inverse is None):
            inverse_present = ctypes.c_bool(False)
            inverse = numpy.zeros(shape=(1,1), dtype=ctypes.c_float, order='F')
        elif (type(inverse) == bool) and (inverse):
            inverse = numpy.zeros(shape=(1,1), dtype=ctypes.c_float, order='F')
        elif ((not issubclass(type(inverse), numpy.ndarray)) or
              (not numpy.asarray(inverse).flags.f_contiguous) or
              (not (inverse.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'inverse' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            inverse = numpy.asarray(inverse, dtype=ctypes.c_float, order='F')
        if (inverse_present):
            inverse_dim_1 = ctypes.c_long(inverse.shape[0])
            inverse_dim_2 = ctypes.c_long(inverse.shape[1])
        else:
            inverse_dim_1 = ctypes.c_long()
            inverse_dim_2 = ctypes.c_long()
        
        # Setting up "maxbound"
        maxbound_present = ctypes.c_bool(True)
        if (maxbound is None):
            maxbound_present = ctypes.c_bool(False)
            maxbound = ctypes.c_int()
        else:
            maxbound = ctypes.c_int(maxbound)
        if (type(maxbound) is not ctypes.c_int): maxbound = ctypes.c_int(maxbound)
        
        # Setting up "max_to_flatten"
        max_to_flatten_present = ctypes.c_bool(True)
        if (max_to_flatten is None):
            max_to_flatten_present = ctypes.c_bool(False)
            max_to_flatten = ctypes.c_int()
        else:
            max_to_flatten = ctypes.c_int(max_to_flatten)
        if (type(max_to_flatten) is not ctypes.c_int): max_to_flatten = ctypes.c_int(max_to_flatten)
        
        # Setting up "max_to_square"
        max_to_square_present = ctypes.c_bool(True)
        if (max_to_square is None):
            max_to_square_present = ctypes.c_bool(False)
            max_to_square = ctypes.c_long()
        else:
            max_to_square = ctypes.c_long(max_to_square)
        if (type(max_to_square) is not ctypes.c_long): max_to_square = ctypes.c_long(max_to_square)
        
        # Setting up "svd_steps"
        svd_steps_present = ctypes.c_bool(True)
        if (svd_steps is None):
            svd_steps_present = ctypes.c_bool(False)
            svd_steps = ctypes.c_int()
        else:
            svd_steps = ctypes.c_int(svd_steps)
        if (type(svd_steps) is not ctypes.c_int): svd_steps = ctypes.c_int(svd_steps)
    
        # Call C-accessible Fortran wrapper.
        clib.c_radialize(ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data), ctypes.byref(shift_dim_1), ctypes.c_void_p(shift.ctypes.data), ctypes.byref(vecs_dim_1), ctypes.byref(vecs_dim_2), ctypes.c_void_p(vecs.ctypes.data), ctypes.byref(inverse_present), ctypes.byref(inverse_dim_1), ctypes.byref(inverse_dim_2), ctypes.c_void_p(inverse.ctypes.data), ctypes.byref(maxbound_present), ctypes.byref(maxbound), ctypes.byref(max_to_flatten_present), ctypes.byref(max_to_flatten), ctypes.byref(max_to_square_present), ctypes.byref(max_to_square), ctypes.byref(svd_steps_present), ctypes.byref(svd_steps))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return x, shift, vecs, (inverse if inverse_present else None)

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine LEAST_SQUARES
    
    def least_squares(self, trans, a, b, x):
        '''! Perform least squares with LAPACK.
!
!   A is column vectors (of points) if TRANS='T', and row vectors
!     (of points) if TRANS='N'.
!   B must be COLUMN VECTORS of fit output (1 row = 1 point).
!   X always has a first dimension that is nonpoint axis size of A,
!     and the second dimension is determined by B's columns (or rank),
!     and if X is smaller then B is reduced to its principal components.'''
        
        # Setting up "trans"
        if (type(trans) is not ctypes.c_char): trans = ctypes.c_char(trans)
        
        # Setting up "a"
        if ((not issubclass(type(a), numpy.ndarray)) or
            (not numpy.asarray(a).flags.f_contiguous) or
            (not (a.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'a' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            a = numpy.asarray(a, dtype=ctypes.c_float, order='F')
        a_dim_1 = ctypes.c_long(a.shape[0])
        a_dim_2 = ctypes.c_long(a.shape[1])
        
        # Setting up "b"
        if ((not issubclass(type(b), numpy.ndarray)) or
            (not numpy.asarray(b).flags.f_contiguous) or
            (not (b.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'b' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            b = numpy.asarray(b, dtype=ctypes.c_float, order='F')
        b_dim_1 = ctypes.c_long(b.shape[0])
        b_dim_2 = ctypes.c_long(b.shape[1])
        
        # Setting up "x"
        if ((not issubclass(type(x), numpy.ndarray)) or
            (not numpy.asarray(x).flags.f_contiguous) or
            (not (x.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'x' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            x = numpy.asarray(x, dtype=ctypes.c_float, order='F')
        x_dim_1 = ctypes.c_long(x.shape[0])
        x_dim_2 = ctypes.c_long(x.shape[1])
    
        # Call C-accessible Fortran wrapper.
        clib.c_least_squares(ctypes.byref(trans), ctypes.byref(a_dim_1), ctypes.byref(a_dim_2), ctypes.c_void_p(a.ctypes.data), ctypes.byref(b_dim_1), ctypes.byref(b_dim_2), ctypes.c_void_p(b.ctypes.data), ctypes.byref(x_dim_1), ctypes.byref(x_dim_2), ctypes.c_void_p(x.ctypes.data))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return a, b, x

matrix_operations = matrix_operations()

