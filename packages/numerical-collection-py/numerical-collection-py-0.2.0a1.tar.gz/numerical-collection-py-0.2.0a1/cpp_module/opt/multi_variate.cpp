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
 * \brief Define bindings of optimization algorithms for multi-variate
 * objective functions.
 */
#include "multi_variate.h"

#include <Eigen/Core>
#include <functional>
#include <memory>

#include <num_collect/opt/adaptive_diagonal_curves.h>
#include <num_collect/opt/dividing_rectangles.h>
#include <num_collect/opt/downhill_simplex.h>
#include <pybind11/cast.h>
#include <pybind11/eigen.h>  // IWYU pragma: keep
#include <pybind11/pybind11.h>

#include "multi_variate_objective_function.h"
#include "multi_variate_optimizer_helper.h"

namespace num_collect::opt::multi_variate {

void bind(pybind11::module& opt_module) {
    auto multi_variate_module = opt_module.def_submodule("multi_variate");

    pybind11::class_<py_objective_function_base,
        std::shared_ptr<py_objective_function_base>,
        py_objective_function_trampoline<py_objective_function_base>>(
        multi_variate_module, "ObjectiveFunctionBase",
        R"(
        Base class of multi-variate objective functions.

        Inherit objective functions from this class and
        implement evaluate_on function.
        )")
        .def(pybind11::init<>())
        .def("evaluate_on", &py_objective_function_base::evaluate_on,
            pybind11::arg("var"),
            R"(
            Evaluate this objective function on a variable.

            Args:
                var (numpy.ndarray): Variable.
            )")
        .def_property("value", &py_objective_function_base::value,
            &py_objective_function_base::set_value, "Function value.");

    using downhill_simplex_type =
        downhill_simplex<py_objective_function_wrapper>;
    bind_common_members(
        pybind11::class_<downhill_simplex_type>(multi_variate_module,
            "DownhillSimplex",
            R"(
            Class of downhill simplex method :cite:`Press2007`.

            Args:
                obj_fun (num_collect.opt.multi_variate.ObjectiveFunctionBase): Objective function.
            )")
            .def(pybind11::init(
                     [](std::shared_ptr<py_objective_function_base> obj_fun) {
                         return std::make_unique<downhill_simplex_type>(
                             py_objective_function_wrapper(std::move(obj_fun)));
                     }),
                pybind11::arg("obj_fun"))
            .def("init", &downhill_simplex_type::init,
                pybind11::arg("init_var"), pybind11::kw_only(),
                pybind11::arg("width") = downhill_simplex_type::default_width,
                R"(
                Initialize the algorithm.

                Args:
                    init_var (numpy.ndarray): Initial variable.
                    width (float, optional): Width of the initial simplex.
                )")
            .def("tol_simplex_size", &downhill_simplex_type::tol_simplex_size,
                pybind11::arg("value"), R"(
                Set tolerance of size of simplex.

                Args:
                    value (float): Value.
                )"));

    using dividing_rectangles_type =
        dividing_rectangles<py_objective_function_wrapper>;
    bind_common_members(
        pybind11::class_<dividing_rectangles_type>(multi_variate_module,
            "DividingRectangles",
            R"(
            Class of dividing rectangles (DIRECT) method :cite:`Jones1993` for optimization.

            Args:
                obj_fun (num_collect.opt.multi_variate.ObjectiveFunctionBase): Objective function.
            )")
            .def(pybind11::init(
                     [](std::shared_ptr<py_objective_function_base> obj_fun) {
                         return std::make_unique<dividing_rectangles_type>(
                             py_objective_function_wrapper(std::move(obj_fun)));
                     }),
                pybind11::arg("obj_fun"))
            .def("init", &dividing_rectangles_type::init,
                pybind11::arg("lower"), pybind11::arg("upper"),
                R"(
                Initialize the algorithm.

                Args:
                    lower (numpy.ndarray): Lower limit of the range of variables.
                    upper (numpy.ndarray): Upper limit of the range of variables.
                )")
            .def("max_evaluations", &dividing_rectangles_type::max_evaluations,
                pybind11::arg("value"),
                R"(
                Set the maximum number of function evaluations.

                Args:
                    value (int): Value.
                )")
            .def("min_rate_imp", &dividing_rectangles_type::min_rate_imp,
                pybind11::arg("value"), R"(
                Set the minimum rate of improvement in the function value required for potentially optimal rectangles.

                Args:
                    value (float): Value.
                )"));

    using adaptive_diagonal_curves_type =
        adaptive_diagonal_curves<py_objective_function_wrapper>;
    bind_common_members(
        pybind11::class_<adaptive_diagonal_curves_type>(multi_variate_module,
            "AdaptiveDiagonalCurves",
            R"(
            Class of adaptive diagonal curves (ADC) method :cite:`Sergeyev2006` for optimization.

            Args:
                obj_fun (num_collect.opt.multi_variate.ObjectiveFunctionBase): Objective function.
            )")
            .def(pybind11::init(
                     [](std::shared_ptr<py_objective_function_base> obj_fun) {
                         return std::make_unique<adaptive_diagonal_curves_type>(
                             py_objective_function_wrapper(std::move(obj_fun)));
                     }),
                pybind11::arg("obj_fun"))
            .def("init", &adaptive_diagonal_curves_type::init,
                pybind11::arg("lower"), pybind11::arg("upper"),
                R"(
                Initialize the algorithm.

                Args:
                    lower (numpy.ndarray): Lower limit of the range of variables.
                    upper (numpy.ndarray): Upper limit of the range of variables.
                )")
            .def("max_evaluations",
                &adaptive_diagonal_curves_type::max_evaluations,
                pybind11::arg("value"),
                R"(
                Set the maximum number of function evaluations.

                Args:
                    value (int): Value.
                )")
            .def("min_rate_imp", &adaptive_diagonal_curves_type::min_rate_imp,
                pybind11::arg("value"), R"(
                Set the minimum rate of improvement in the function value required for potentially optimal rectangles.

                Args:
                    value (float): Value.
                )")
            .def("decrease_rate_bound",
                &adaptive_diagonal_curves_type::decrease_rate_bound,
                pybind11::arg("value"), R"(
                Set the rate of function value used to check whether the function value decreased in the current phase.

                Args:
                    value (float): Value.
                )"));
}

}  // namespace num_collect::opt::multi_variate
