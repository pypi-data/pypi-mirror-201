#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "matrix_compressor::matrix_compressor" for configuration "Release"
set_property(TARGET matrix_compressor::matrix_compressor APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(matrix_compressor::matrix_compressor PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libmatrix_compressor.a"
  )

list(APPEND _cmake_import_check_targets matrix_compressor::matrix_compressor )
list(APPEND _cmake_import_check_files_for_matrix_compressor::matrix_compressor "${_IMPORT_PREFIX}/lib64/libmatrix_compressor.a" )

# Import target "matrix_compressor::streamvbyte" for configuration "Release"
set_property(TARGET matrix_compressor::streamvbyte APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(matrix_compressor::streamvbyte PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libstreamvbyte.a"
  )

list(APPEND _cmake_import_check_targets matrix_compressor::streamvbyte )
list(APPEND _cmake_import_check_files_for_matrix_compressor::streamvbyte "${_IMPORT_PREFIX}/lib64/libstreamvbyte.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
