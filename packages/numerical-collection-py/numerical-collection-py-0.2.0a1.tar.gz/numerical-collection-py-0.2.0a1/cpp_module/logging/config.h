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
#pragma once

#include <pybind11/pybind11.h>

namespace num_collect::logging::config {

/*!
 * \brief Define bindings of log configurations.
 *
 * \param[in] module
 */
void bind(pybind11::module& module);

}  // namespace num_collect::logging::config
