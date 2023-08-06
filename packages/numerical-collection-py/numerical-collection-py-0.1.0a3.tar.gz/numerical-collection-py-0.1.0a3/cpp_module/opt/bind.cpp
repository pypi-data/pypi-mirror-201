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
 * \brief Define bindings of optimization algorithms.
 */
#include "bind.h"

#include <pybind11/pybind11.h>

#include "multi_variate.h"

namespace num_collect::opt {

void bind(pybind11::module& module) {
    auto opt_module = module.def_submodule("opt");
    multi_variate::bind(opt_module);
}

}  // namespace num_collect::opt
