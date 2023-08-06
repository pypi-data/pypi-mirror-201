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
#include "bind.h"

#include <num_collect/logging/log_level.h>
#include <pybind11/attr.h>
#include <pybind11/pybind11.h>

#include "config.h"
#include "sinks.h"

namespace num_collect::logging {

void bind(pybind11::module& module) {
    pybind11::enum_<log_level>(module, "LogLevel", "Enumeration of log levels.",
        pybind11::arithmetic())
        .value("trace", log_level::trace, "For internal trace logs.")
        .value("debug", log_level::debug,
            "For debug information. (Meant for use in user code, not in "
            "algorithms.)")
        .value("iteration", log_level::iteration, "For logs of iterations.")
        .value("iteration_label", log_level::iteration_label,
            "For labels of iteration logs.")
        .value("summary", log_level::summary, "For summary of calculations.")
        .value("info", log_level::info,
            "For some information. (Meant for use in user code, not in "
            "algorithms.)")
        .value("warning", log_level::warning, "For warnings.")
        .value("error", log_level::error, "For errors.")
        .value("critical", log_level::critical, "For critical errors.")
        .value("off", log_level::off,
            "Turn off output (only for output log level).");

    sinks::bind(module);
    config::bind(module);
}

}  // namespace num_collect::logging
