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
 * \brief Bindings of log configurations.
 */
#include "config.h"

#include <memory>

#include <num_collect/logging/load_logging_config.h>
#include <num_collect/logging/log_config.h>
#include <num_collect/logging/log_tag_config.h>
#include <num_collect/logging/log_tag_view.h>

#include "sinks.h"

namespace num_collect::logging::config {

void bind(pybind11::module& module) {
// NOLINTNEXTLINE(cppcoreguidelines-macro-usage): false positive
#define DEF_LOG_TAG_CONFIG_PROPERTY(TYPE, CPP_NAME, PY_NAME, DOC) \
    def_property(PY_NAME,                                         \
        pybind11::overload_cast<>(                                \
            &log_tag_config::CPP_NAME, pybind11::const_),         \
        pybind11::overload_cast<TYPE>(&log_tag_config::CPP_NAME), DOC)

    pybind11::class_<log_tag_config>(
        module, "LogTagConfig", "Class to hold configurations for log tags.")
        .def(pybind11::init<>())
        .def_property(
            "sink",
            [](const log_tag_config& self)
                -> std::shared_ptr<sinks::py_log_sink_base> {
                return std::make_shared<sinks::cpp_log_sink_wrapper>(
                    self.sink());
            },
            [](log_tag_config& self,
                const std::shared_ptr<sinks::py_log_sink_base>& val) {
                self.sink(val->to_cpp_log_sink());
            },
            "Log sink.")
        .DEF_LOG_TAG_CONFIG_PROPERTY(log_level, output_log_level,
            "output_log_level", "Minimum log level to output.")
        .DEF_LOG_TAG_CONFIG_PROPERTY(log_level,
            output_log_level_in_child_iterations,
            "output_log_level_in_child_iterations",
            "Minimum log level to output in child iterations.")
        .DEF_LOG_TAG_CONFIG_PROPERTY(index_type, iteration_output_period,
            "iteration_output_period", "Period to write iteration logs.")
        .DEF_LOG_TAG_CONFIG_PROPERTY(index_type, iteration_label_period,
            "iteration_label_period",
            "Period to write labels of iteration logs.");

#undef DEF_LOG_TAG_CONFIG_PROPERTY

    pybind11::class_<log_config>(
        module, "LogConfig", "Class of configurations of logs.")
        .def_static(
            "get_default_tag_config",
            []() { return log_config::instance().get_default_tag_config(); },
            pybind11::call_guard<pybind11::gil_scoped_release>(), R"(
            Get the default configuration of log tags.

            Returns:
                LogTagConfig: Default configuration of log tags.
            )")
        .def_static(
            "set_default_tag_config",
            [](const log_tag_config& config) {
                log_config::instance().set_default_tag_config(config);
            },
            pybind11::call_guard<pybind11::gil_scoped_release>(),
            pybind11::arg("config"),
            R"(
            Set the default configuration of log tags.

            Args:
                config (LogTagConfig): Configuration.
            )")
        .def_static(
            "get_config_of",
            [](std::string_view tag) {
                return log_config::instance().get_config_of(log_tag_view(tag));
            },
            pybind11::call_guard<pybind11::gil_scoped_release>(),
            pybind11::arg("tag"),
            R"(
            Get the configuration of a tag.

            Args:
                tag (str): Tag.

            Returns:
                LogTagConfig: Configuration.
            )")
        .def_static(
            "set_config_of",
            [](std::string_view tag, const log_tag_config& config) {
                log_config::instance().set_config_of(log_tag_view(tag), config);
            },
            pybind11::call_guard<pybind11::gil_scoped_release>(),
            pybind11::arg("tag"), pybind11::arg("config"),
            R"(
            Set the configuration of a tag.

            Args:
                tag (str): Tag.
                config (LogTagConfig): Configuration.
            )");

    module.def("load_logging_config_file", &load_logging_config_file,
        pybind11::call_guard<pybind11::gil_scoped_release>(),
        pybind11::arg("file_path"), R"(
        Parse and apply configurations of logging from a file.

        Args:
            file_path (str): File path.
        )");
}

}  // namespace num_collect::logging::config
