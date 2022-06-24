cmake_minimum_required(VERSION 3.16)
project(PackageTest CXX)

find_package(serd REQUIRED)

add_executable(example example.cpp)

target_link_libraries(example PUBLIC
        serd::serd
        )

set_target_properties(
        example PROPERTIES
        CXX_STANDARD 11
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF
)
