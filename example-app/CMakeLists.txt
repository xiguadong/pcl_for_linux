cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(pcl_example)

enable_language(C CXX)

# set(CMAKE_CXX_STANDARD 14)


set(PCL_DIR ../install_release/pcl/share/pcl-1.9)
find_package(PCL 1.9 REQUIRED)
include_directories(${PCL_INCLUDE_DIRS})
include_directories(../install_release/include)

link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
# add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)
# add_definitions(-DCMAKE_CXX_VISIBILITY_PRESET="hidden")


# message(INFO ${PCL_LIBRARIES})
add_executable (pcl_example main.cpp)
target_link_libraries (pcl_example ${PCL_LIBRARIES} gomp pcl_io_ply)
set_target_properties(pcl_example PROPERTIES COMPILE_FLAGS -fopenmp)