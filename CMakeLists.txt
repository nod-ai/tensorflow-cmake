cmake_minimum_required(VERSION 3.15)
project(tensorflow)

include(ExternalProject)
include(CMakePackageConfigHelpers)

find_package(Python3 REQUIRED)

set(CMAKE_CXX_STANDARD 17 CACHE STRING "The C++ standard for building and linking the library (e.g., 17).")
set(TF_VERSION "" CACHE STRING "TensorFlow Version. Defaults to ${TF_DEFAULT_VERSION}.")
if("${TF_VERSION}" STREQUAL "")
    message(FATAL_ERROR "TF_VERSION must be set. E.g. 2.11.0.")
endif()
set(TF_TAG "v${TF_VERSION}")
set(TF_URL
    "https://github.com/tensorflow/tensorflow/archive/${TF_TAG}.tar.gz"
    CACHE
    STRING
    "URL to TensorFlow source code. Directory or archive. Can be a local path."
)

if(NOT IS_DIRECTORY "${TF_URL}")
    set(DOWNLOAD_ARGS
        URL "${TF_URL}"
        DOWNLOAD_DIR "tensorflow"
        USES_TERMINAL_DOWNLOAD TRUE
        DOWNLOAD_EXTRACT_TIMESTAMP TRUE
    )
    set(TF_SRC "${CMAKE_CURRENT_BINARY_DIR}/tensorflow_extern_proj/tensorflow")
else()
    set(TF_SRC "${TF_URL}")
endif()
set(TF_BIN "${TF_SRC}")

ExternalProject_Add(
    tensorflow_extern_proj
    ${DOWNLOAD_ARGS}
    SOURCE_DIR "${TF_SRC}"
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ""
    BUILD_COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/configure.py"
        "--tf_src=${TF_SRC}"
    COMMAND
        "${Python3_EXECUTABLE}"
        "${CMAKE_CURRENT_SOURCE_DIR}/build.py"
        "--tf_src=${TF_SRC}"
    USES_TERMINAL_BUILD TRUE
    INSTALL_COMMAND ""
    BUILD_ALWAYS TRUE
)

set(SRC_DIR "${CMAKE_CURRENT_LIST_DIR}")
configure_file("install.cmake.in" "install.cmake" @ONLY)

install(
    SCRIPT "${CMAKE_CURRENT_BINARY_DIR}/install.cmake"
)

add_library(tensorflow_cc INTERFACE)
target_include_directories(
  tensorflow_cc INTERFACE
  $<INSTALL_INTERFACE:include>
  $<INSTALL_INTERFACE:include/src>
)
target_link_libraries(
  tensorflow_cc INTERFACE
  "${CMAKE_INSTALL_PREFIX}/lib/libtensorflow_cc.so.${TF_VERSION}"
  "${CMAKE_INSTALL_PREFIX}/lib/libtensorflow_framework.so.${TF_VERSION}"
)
target_compile_features(tensorflow_cc INTERFACE "cxx_std_${CMAKE_CXX_STANDARD}")
set_target_properties(
  tensorflow_cc PROPERTIES EXPORT_NAME TensorflowCC
)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/TensorflowCCConfigVersion.cmake"
    VERSION ${TF_VERSION}
    COMPATIBILITY SameMinorVersion
)
set(CMAKECFG_INSTALL_DIR lib/cmake/TensorflowCC)
configure_package_config_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/TensorflowCCConfig.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/TensorflowCCConfig.cmake"
  INSTALL_DESTINATION "${CMAKECFG_INSTALL_DIR}"
  NO_SET_AND_CHECK_MACRO # TensorflowCC only uses interface libraries
  NO_CHECK_REQUIRED_COMPONENTS_MACRO # TensorflowCC does not have components
)
install(
  TARGETS tensorflow_cc
  EXPORT TensorflowCCTargets
)
install(
  EXPORT TensorflowCCTargets
  FILE TensorflowCCTargets.cmake
  NAMESPACE TensorflowCC::
  DESTINATION "${CMAKECFG_INSTALL_DIR}"
)
install(
  FILES
    "${CMAKE_CURRENT_BINARY_DIR}/TensorflowCCConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/TensorflowCCConfigVersion.cmake"
  DESTINATION "${CMAKECFG_INSTALL_DIR}"
)
