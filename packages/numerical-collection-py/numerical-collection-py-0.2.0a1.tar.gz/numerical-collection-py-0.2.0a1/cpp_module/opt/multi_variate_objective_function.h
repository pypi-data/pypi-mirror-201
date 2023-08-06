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
 * \brief Definition of classes of multi-variate objective functions for Python.
 */
#pragma once

#include <Eigen/Core>
#include <memory>

#include <pybind11/eigen.h>  // IWYU pragma: keep
#include <pybind11/pybind11.h>

namespace num_collect::opt::multi_variate {

/*!
 * \brief Base class of multi-variate objective functions in Python.
 */
class py_objective_function_base {
public:
    /*!
     * \brief Evaluate this objective function on a variable.
     *
     * \param[in] var Variable.
     */
    virtual void evaluate_on(const Eigen::VectorXd& var) = 0;

    /*!
     * \brief Get the function value.
     *
     * \return Function value.
     */
    [[nodiscard]] auto value() const -> const double& { return value_; }

    /*!
     * \brief Set the function value.
     *
     * \param[in] value Value.
     */
    void set_value(double value) { value_ = value; }

    py_objective_function_base() = default;

    virtual ~py_objective_function_base() = default;

    py_objective_function_base(const py_objective_function_base&) = delete;
    py_objective_function_base(py_objective_function_base&&) = delete;
    auto operator=(const py_objective_function_base&) = delete;
    auto operator=(py_objective_function_base&&) = delete;

private:
    //! Function value.
    double value_{};
};

/*!
 * \brief Class of "trampoline" in Pybind11 to implement
 * py_objective_function_base in Python.
 */
template <typename Base>
class py_objective_function_trampoline : public Base {
public:
    using Base::Base;

    //! \copydoc num_collect::opt::py_objective_function_base::evaluate_on
    void evaluate_on(const Eigen::VectorXd& var) override {
        PYBIND11_OVERRIDE_PURE(void, Base, evaluate_on, var);
    }
};

/*!
 * \brief Class to wrap py_objective_function_base for use in C++.
 */
class py_objective_function_wrapper {
public:
    //! Type of variables.
    using variable_type = Eigen::VectorXd;

    //! Type of function values.
    using value_type = double;

    /*!
     * \brief Constructor.
     *
     * \param[in] obj_fun Objective function in Python.
     */
    explicit py_objective_function_wrapper(
        std::shared_ptr<py_objective_function_base> obj_fun)
        : obj_fun_(std::move(obj_fun)) {}

    //! \copydoc num_collect::opt::py_objective_function_base::evaluate_on
    void evaluate_on(const Eigen::VectorXd& var) { obj_fun_->evaluate_on(var); }

    //! \copydoc num_collect::opt::py_objective_function_base::value
    [[nodiscard]] auto value() const -> const double& {
        return obj_fun_->value();
    }

protected:
    //! Objective function in Python.
    std::shared_ptr<py_objective_function_base>
        obj_fun_;  // NOLINT(cppcoreguidelines-non-private-member-variables-in-classes)
};

}  // namespace num_collect::opt::multi_variate
