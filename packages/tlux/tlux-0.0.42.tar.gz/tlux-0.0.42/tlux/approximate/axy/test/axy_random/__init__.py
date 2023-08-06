'''This Python code is an automatically generated wrapper
for Fortran code made by 'fmodpy'. The original documentation
for the Fortran source code follows.


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
_shared_object_name = "axy_random." + platform.machine() + ".so"
_this_directory = os.path.dirname(os.path.abspath(__file__))
_path_to_lib = os.path.join(_this_directory, _shared_object_name)
_compile_options = ['-fPIC', '-shared', '-O3']
_ordered_dependencies = ['axy_random.f90', 'axy_random_c_wrapper.f90']
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


class random:
    ''''''

    # Declare 'zero'
    def get_zero(self):
        zero = ctypes.c_long()
        clib.random_get_zero(ctypes.byref(zero))
        return zero.value
    def set_zero(self, zero):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    zero = property(get_zero, set_zero)

    # Declare 'one'
    def get_one(self):
        one = ctypes.c_long()
        clib.random_get_one(ctypes.byref(one))
        return one.value
    def set_one(self, one):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    one = property(get_one, set_one)

    # Declare 'two'
    def get_two(self):
        two = ctypes.c_long()
        clib.random_get_two(ctypes.byref(two))
        return two.value
    def set_two(self, two):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    two = property(get_two, set_two)

    # Declare 'four'
    def get_four(self):
        four = ctypes.c_long()
        clib.random_get_four(ctypes.byref(four))
        return four.value
    def set_four(self, four):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    four = property(get_four, set_four)

    # Declare 'pi'
    def get_pi(self):
        pi = ctypes.c_float()
        clib.random_get_pi(ctypes.byref(pi))
        return pi.value
    def set_pi(self, pi):
        raise(NotImplementedError('Module attributes with PARAMETER status cannot be set.'))
    pi = property(get_pi, set_pi)

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine RANDOM_UNIT_VECTORS
    
    def random_unit_vectors(self, column_vectors):
        '''! Generate randomly distributed vectors on the N-sphere.'''
        
        # Setting up "column_vectors"
        if ((not issubclass(type(column_vectors), numpy.ndarray)) or
            (not numpy.asarray(column_vectors).flags.f_contiguous) or
            (not (column_vectors.dtype == numpy.dtype(ctypes.c_float)))):
            import warnings
            warnings.warn("The provided argument 'column_vectors' was not an f_contiguous NumPy array of type 'ctypes.c_float' (or equivalent). Automatically converting (probably creating a full copy).")
            column_vectors = numpy.asarray(column_vectors, dtype=ctypes.c_float, order='F')
        column_vectors_dim_1 = ctypes.c_long(column_vectors.shape[0])
        column_vectors_dim_2 = ctypes.c_long(column_vectors.shape[1])
    
        # Call C-accessible Fortran wrapper.
        clib.c_random_unit_vectors(ctypes.byref(column_vectors_dim_1), ctypes.byref(column_vectors_dim_2), ctypes.c_void_p(column_vectors.ctypes.data))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return column_vectors

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine INITIALIZE_ITERATOR
    
    def initialize_iterator(self, i_limit, seed=None):
        '''! Given the variables for a linear iterator, initialize it.'''
        
        # Setting up "i_limit"
        if (type(i_limit) is not ctypes.c_long): i_limit = ctypes.c_long(i_limit)
        
        # Setting up "i_next"
        i_next = ctypes.c_long()
        
        # Setting up "i_mult"
        i_mult = ctypes.c_long()
        
        # Setting up "i_step"
        i_step = ctypes.c_long()
        
        # Setting up "i_mod"
        i_mod = ctypes.c_long()
        
        # Setting up "seed"
        seed_present = ctypes.c_bool(True)
        if (seed is None):
            seed_present = ctypes.c_bool(False)
            seed = ctypes.c_long()
        else:
            seed = ctypes.c_long(seed)
        if (type(seed) is not ctypes.c_long): seed = ctypes.c_long(seed)
    
        # Call C-accessible Fortran wrapper.
        clib.c_initialize_iterator(ctypes.byref(i_limit), ctypes.byref(i_next), ctypes.byref(i_mult), ctypes.byref(i_step), ctypes.byref(i_mod), ctypes.byref(seed_present), ctypes.byref(seed))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return i_next.value, i_mult.value, i_step.value, i_mod.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine INDEX_TO_PAIR
    
    def index_to_pair(self, max_value, i):
        '''! Map an integer I in the range [1, MAX_VALUE**2] to a unique pair
!  of integers PAIR1 and PAIR2 with both in the range [1, MAX_VALUE].'''
        
        # Setting up "max_value"
        if (type(max_value) is not ctypes.c_long): max_value = ctypes.c_long(max_value)
        
        # Setting up "i"
        if (type(i) is not ctypes.c_long): i = ctypes.c_long(i)
        
        # Setting up "pair1"
        pair1 = ctypes.c_long()
        
        # Setting up "pair2"
        pair2 = ctypes.c_long()
    
        # Call C-accessible Fortran wrapper.
        clib.c_index_to_pair(ctypes.byref(max_value), ctypes.byref(i), ctypes.byref(pair1), ctypes.byref(pair2))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return pair1.value, pair2.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine PAIR_TO_INDEX
    
    def pair_to_index(self, max_value, pair1, pair2):
        '''! Map a pair of integers PAIR1 and PAIR2 in the range [1, MAX_VALUE]
!  to an integer I in the range [1, MAX_VALUE**2].'''
        
        # Setting up "max_value"
        if (type(max_value) is not ctypes.c_long): max_value = ctypes.c_long(max_value)
        
        # Setting up "pair1"
        if (type(pair1) is not ctypes.c_long): pair1 = ctypes.c_long(pair1)
        
        # Setting up "pair2"
        if (type(pair2) is not ctypes.c_long): pair2 = ctypes.c_long(pair2)
        
        # Setting up "i"
        i = ctypes.c_long()
    
        # Call C-accessible Fortran wrapper.
        clib.c_pair_to_index(ctypes.byref(max_value), ctypes.byref(pair1), ctypes.byref(pair2), ctypes.byref(i))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return i.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine RANDOM_INTEGER
    
    def random_integer(self, max_value=None):
        '''! Define a function for generating random integers.
! Optional MAX_VALUE is a noninclusive upper bound for the value generated.'''
        
        # Setting up "max_value"
        max_value_present = ctypes.c_bool(True)
        if (max_value is None):
            max_value_present = ctypes.c_bool(False)
            max_value = ctypes.c_long()
        else:
            max_value = ctypes.c_long(max_value)
        if (type(max_value) is not ctypes.c_long): max_value = ctypes.c_long(max_value)
        
        # Setting up "random_int"
        random_int = ctypes.c_long()
    
        # Call C-accessible Fortran wrapper.
        clib.c_random_integer(ctypes.byref(max_value_present), ctypes.byref(max_value), ctypes.byref(random_int))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return random_int.value

    
    # ----------------------------------------------
    # Wrapper for the Fortran subroutine GET_NEXT_INDEX
    
    def get_next_index(self, i_limit, i_next, i_mult, i_step, i_mod, reshuffle=None):
        '''! Get the next index in the model point iterator.'''
        
        # Setting up "i_limit"
        if (type(i_limit) is not ctypes.c_long): i_limit = ctypes.c_long(i_limit)
        
        # Setting up "i_next"
        if (type(i_next) is not ctypes.c_long): i_next = ctypes.c_long(i_next)
        
        # Setting up "i_mult"
        if (type(i_mult) is not ctypes.c_long): i_mult = ctypes.c_long(i_mult)
        
        # Setting up "i_step"
        if (type(i_step) is not ctypes.c_long): i_step = ctypes.c_long(i_step)
        
        # Setting up "i_mod"
        if (type(i_mod) is not ctypes.c_long): i_mod = ctypes.c_long(i_mod)
        
        # Setting up "reshuffle"
        reshuffle_present = ctypes.c_bool(True)
        if (reshuffle is None):
            reshuffle_present = ctypes.c_bool(False)
            reshuffle = ctypes.c_bool()
        else:
            reshuffle = ctypes.c_bool(reshuffle)
        if (type(reshuffle) is not ctypes.c_bool): reshuffle = ctypes.c_bool(reshuffle)
        
        # Setting up "next_i"
        next_i = ctypes.c_long()
    
        # Call C-accessible Fortran wrapper.
        clib.c_get_next_index(ctypes.byref(i_limit), ctypes.byref(i_next), ctypes.byref(i_mult), ctypes.byref(i_step), ctypes.byref(i_mod), ctypes.byref(reshuffle_present), ctypes.byref(reshuffle), ctypes.byref(next_i))
    
        # Return final results, 'INTENT(OUT)' arguments only.
        return i_next.value, i_mult.value, i_step.value, i_mod.value, next_i.value

random = random()

