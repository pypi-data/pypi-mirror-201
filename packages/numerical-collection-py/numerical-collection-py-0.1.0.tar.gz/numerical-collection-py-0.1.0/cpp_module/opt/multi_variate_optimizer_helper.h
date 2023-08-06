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
 * \brief Definition of helper functions to bind optimization algorithms
 * multi-variate objective function.
 */
#pragma once

#include <num_collect/opt/concepts/optimizer.h>
#include <pybind11/eigen.h>  // IWYU pragma: keep
#include <pybind11/pybind11.h>

namespace num_collect::opt::multi_variate {

template <num_collect::opt::concepts::optimizer Optimizer>
void bind_common_members(pybind11::class_<Optimizer>& cls) {
    cls.def("iterate", &Optimizer::iterate, R"(
            Iterate once.

            Note:
                Any required initializations (with init functions) are
                assumed to have been done.
        )")
        .def("is_stop_criteria_satisfied", &Optimizer::solve, R"(
            Determine if stopping criteria of the algorithm are satisfied.

            Returns:
                bool: True if stopping criteria of the algorithm are satisfied.
        )")
        .def("solve", &Optimizer::solve, R"(
            Solve the problem.

            Iterate the algorithm until the stopping criteria are satisfied.

            Note:
                Any required initializations (with init functions) are
                assumed to have been done.
        )")
        .def_property_readonly("opt_variable", &Optimizer::opt_variable,
            "Current optimal variable.")
        .def_property_readonly(
            "opt_value", &Optimizer::opt_value, "Current optimal value.")
        .def_property_readonly(
            "iterations", &Optimizer::iterations, "Number of iterations.")
        .def_property_readonly("evaluations", &Optimizer::evaluations,
            "Number of function evaluations.");
}

}  // namespace num_collect::opt::multi_variate
