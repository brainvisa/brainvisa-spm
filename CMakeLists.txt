cmake_minimum_required( VERSION 2.6 )

find_package( python REQUIRED )
find_package( Sphinx )
find_package( brainvisa-cmake REQUIRED )

find_package( soma-base REQUIRED )
find_package( axon REQUIRED )

BRAINVISA_PROJECT()

BRAINVISA_DEPENDENCY(DEV DEPENDS ${PROJECT_NAME} RUN "= ${BRAINVISA_PACKAGE_VERSION_MAJOR}.${BRAINVISA_PACKAGE_VERSION_MINOR}.${BRAINVISA_PACKAGE_VERSION_PATCH}")
BRAINVISA_DEPENDENCY( RUN DEPENDS python RUN ">= 2.6;<< 3.0" )
math( EXPR result "${soma-base_VERSION_MINOR}+1" )
BRAINVISA_DEPENDENCY( RUN DEPENDS "soma-base" RUN ">= ${soma-base_VERSION};<< ${soma-base_VERSION_MAJOR}.${result}" )
math( EXPR result "${axon_VERSION_MINOR}+1" )
BRAINVISA_DEPENDENCY( RUN DEPENDS "axon" RUN ">= ${axon_VERSION};<< ${axon_VERSION_MAJOR}.${result}" )

BRAINVISA_COPY_PYTHON_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/python"
                                    ${PROJECT_NAME} python )
BRAINVISA_COPY_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/brainvisa"
                            brainvisa
                            ${PROJECT_NAME} )
