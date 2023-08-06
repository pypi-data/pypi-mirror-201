#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "sf_compressor::sf_compressor" for configuration "Release"
set_property(TARGET sf_compressor::sf_compressor APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(sf_compressor::sf_compressor PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/sf_compressor.lib"
  )

list(APPEND _cmake_import_check_targets sf_compressor::sf_compressor )
list(APPEND _cmake_import_check_files_for_sf_compressor::sf_compressor "${_IMPORT_PREFIX}/lib/sf_compressor.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
