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
 * \brief Bindings of log sinks.
 */
#pragma once

#include <memory>
#include <utility>

#include <num_collect/logging/sinks/log_sink_base.h>
#include <num_collect/util/source_info_view.h>
#include <pybind11/pybind11.h>

namespace num_collect::logging::sinks {

/*!
 * \brief Interface of log sinks for Python.
 */
class py_log_sink_base : public std::enable_shared_from_this<py_log_sink_base> {
public:
    /*!
     * \brief Write a log.
     *
     * \param[in] time Time.
     * \param[in] tag Tag.
     * \param[in] level Log level.
     * \param[in] file_path File path.
     * \param[in] line Line number in the file.
     * \param[in] column Column number in the line.
     * \param[in] function_name Function name.
     * \param[in] body Log body.
     */
    virtual void write(std::chrono::system_clock::time_point time,
        std::string_view tag, log_level level, std::string_view file_path,
        index_type line, index_type column, std::string_view function_name,
        std::string_view body) = 0;

    /*!
     * \brief Convert to a log sink for C++.
     *
     * \return Log sink.
     */
    [[nodiscard]] virtual auto to_cpp_log_sink()
        -> std::shared_ptr<log_sink_base>;

    py_log_sink_base(const py_log_sink_base&) = delete;
    py_log_sink_base(py_log_sink_base&&) = delete;
    auto operator=(const py_log_sink_base&) -> py_log_sink_base& = delete;
    auto operator=(py_log_sink_base&&) -> py_log_sink_base& = delete;

    /*!
     * \brief Destructor.
     */
    virtual ~py_log_sink_base() noexcept = default;

protected:
    /*!
     * \brief Constructor.
     */
    py_log_sink_base() noexcept = default;
};

/*!
 * \brief Class of "trampoline" in Pybind11 to implement py_log_sink_base in
 * Python.
 */
class py_log_sink_trampoline : public py_log_sink_base {
public:
    //! Constructor.
    py_log_sink_trampoline() = default;

    //! \copydoc num_collect::logging::sinks::py_log_sink_base::write
    void write(std::chrono::system_clock::time_point time, std::string_view tag,
        log_level level, std::string_view file_path, index_type line,
        index_type column, std::string_view function_name,
        std::string_view body) override {
        PYBIND11_OVERRIDE_PURE(void, py_log_sink_base, write, time, tag, level,
            file_path, line, column, function_name, body);
    }
};

/*!
 * \brief Class to wrap log sinks in C++ for Python.
 */
class cpp_log_sink_wrapper final : public py_log_sink_base {
public:
    /*!
     * \brief Constructor.
     *
     * \param[in] log_sink Log sink in C++.
     */
    explicit cpp_log_sink_wrapper(std::shared_ptr<log_sink_base> log_sink)
        : log_sink_(std::move(log_sink)) {}

    //! \copydoc num_collect::logging::sinks::py_log_sink_base::write
    void write(std::chrono::system_clock::time_point time, std::string_view tag,
        log_level level, std::string_view file_path, index_type line,
        index_type column, std::string_view function_name,
        std::string_view body) override {
        log_sink_->write(time, tag, level,
            util::source_info_view(file_path, line, column, function_name),
            body);
    }

    //! \copydoc num_collect::logging::sinks::py_log_sink_base::to_cpp_log_sink
    [[nodiscard]] auto to_cpp_log_sink()
        -> std::shared_ptr<log_sink_base> override {
        return log_sink_;
    }

private:
    //! Log sink in C++.
    std::shared_ptr<log_sink_base> log_sink_;
};

/*!
 * \brief Class to wrap log sinks in Python for C++.
 */
class py_log_sink_wrapper final : public log_sink_base {
public:
    /*!
     * \brief Constructor.
     *
     * \param[in] log_sink Log sink in Python.
     */
    explicit py_log_sink_wrapper(std::shared_ptr<py_log_sink_base> log_sink)
        : log_sink_(std::move(log_sink)) {}

    /*!
     * \brief Write a log.
     *
     * \param[in] time Time.
     * \param[in] tag Tag.
     * \param[in] level Log level.
     * \param[in] source Information of the source code.
     * \param[in] body Log body.
     */
    void write(std::chrono::system_clock::time_point time, std::string_view tag,
        log_level level, util::source_info_view source,
        std::string_view body) noexcept override {
        try {
            log_sink_->write(time, tag, level, source.file_path(),
                source.line(), source.column(), source.function_name(), body);
        } catch (...) {
            // Nothing can be done here.
        }
    }

private:
    //! Log sink in Python.
    std::shared_ptr<py_log_sink_base> log_sink_;
};

/*!
 * \brief Define bindings of log sinks.
 *
 * \param[in] module Python module.
 */
void bind(const pybind11::module& module);

}  // namespace num_collect::logging::sinks
