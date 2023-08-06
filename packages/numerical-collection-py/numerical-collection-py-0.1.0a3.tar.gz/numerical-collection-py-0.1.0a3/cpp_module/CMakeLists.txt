pybind11_add_module(
    num_collect_py_cpp_module
    # base
    base/bind.cpp
    # logging
    logging/sinks.cpp
    logging/config.cpp
    logging/bind.cpp
    # opt
    opt/multi_variate.cpp
    opt/bind.cpp
    # main
    main.cpp)
target_link_libraries(num_collect_py_cpp_module
                      PRIVATE num_collect::num_collect)
set_target_properties(
    num_collect_py_cpp_module
    PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${NUM_COLLECT_PY_CPP_MODULE_OUT_DIR}
               RUNTIME_OUTPUT_DIRECTORY ${NUM_COLLECT_PY_CPP_MODULE_OUT_DIR}
               ARCHIVE_OUTPUT_DIRECTORY ${NUM_COLLECT_PY_CPP_MODULE_OUT_DIR})

if(NUM_COLLECT_PY_UPDATE_STUB)
    add_custom_target(
        num_collect_py_cpp_module_stub ALL
        COMMAND ${POETRY_EXECUTABLE} run python scripts/update_stub.py
        DEPENDS num_collect_py_cpp_module
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/..
        COMMENT "Update stub file for num_collect_py_cpp_module.")
endif()
