/*
 * Copyright 2023 MusicScience37 (Kenta Kabashima)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
/*!
 * \file
 * \brief Define bindings of log sinks.
 */
#include "sinks.h"

#include <memory>

#include <num_collect/logging/sinks/log_sink_base.h>
#include <pybind11/attr.h>
#include <pybind11/chrono.h>  // IWYU pragma: keep
#include <pybind11/gil.h>
#include <pybind11/pybind11.h>

#include "num_collect/util/source_info_view.h"

namespace num_collect::logging::sinks {

auto py_log_sink_base::to_cpp_log_sink() -> std::shared_ptr<log_sink_base> {
    return std::make_shared<py_log_sink_wrapper>(this->shared_from_this());
}

void bind(const pybind11::module& module) {
    pybind11::class_<py_log_sink_base, std::shared_ptr<py_log_sink_base>,
        py_log_sink_trampoline>(
        module, "LogSinkBase", "Interface of log sinks.")
        .def(pybind11::init<>())
        .def("write", &py_log_sink_base::write,
            pybind11::call_guard<pybind11::gil_scoped_release>(),
            pybind11::arg("time"), pybind11::arg("tag"), pybind11::arg("level"),
            pybind11::arg("file_path"), pybind11::arg("line"),
            pybind11::arg("column"), pybind11::arg("function_name"),
            pybind11::arg("body"), R"(
            Write a log.

            Args:
                time (datetime.datetime): Time.
                tag (str): Tag.
                level (LogLevel): Log level.
                file_path (str): File path.
                line (int): Line number in the file.
                column (int): Column number in the line.
                function_name (str): Function name.
                body (str): Log body.
            )");
}

}  // namespace num_collect::logging::sinks
