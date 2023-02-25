#include <tensorflow/compiler/xla/hlo/ir/hlo_module.h>

int main(int argc, char** argv) {
  xla::HloModule hlo_module =
      xla::HloModule("test_hlo_module", xla::HloModuleConfig());
  return 0;
}
