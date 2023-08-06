#include <pybind11/pybind11.h>

#include "base/bind.h"
#include "logging/bind.h"
#include "opt/bind.h"

namespace num_collect {

static void bind(pybind11::module& module) {
    base::bind(module);
    logging::bind(module);
    opt::bind(module);
}

}  // namespace num_collect

// NOLINTNEXTLINE
PYBIND11_MODULE(num_collect_py_cpp_module, module) {
    pybind11::module::import("numpy");
    num_collect::bind(module);
}
