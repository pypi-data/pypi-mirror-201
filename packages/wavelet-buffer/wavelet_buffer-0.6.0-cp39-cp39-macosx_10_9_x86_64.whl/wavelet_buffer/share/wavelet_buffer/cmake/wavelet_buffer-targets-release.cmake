#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "wavelet_buffer::wavelet_buffer" for configuration "Release"
set_property(TARGET wavelet_buffer::wavelet_buffer APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(wavelet_buffer::wavelet_buffer PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libwavelet_buffer.a"
  )

list(APPEND _cmake_import_check_targets wavelet_buffer::wavelet_buffer )
list(APPEND _cmake_import_check_files_for_wavelet_buffer::wavelet_buffer "${_IMPORT_PREFIX}/lib/libwavelet_buffer.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
