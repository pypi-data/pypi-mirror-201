/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace transform {
::llvm::StringRef stringifyFailurePropagationMode(FailurePropagationMode val) {
  switch (val) {
    case FailurePropagationMode::Propagate: return "propagate";
    case FailurePropagationMode::Suppress: return "suppress";
  }
  return "";
}

::std::optional<FailurePropagationMode> symbolizeFailurePropagationMode(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<FailurePropagationMode>>(str)
      .Case("propagate", FailurePropagationMode::Propagate)
      .Case("suppress", FailurePropagationMode::Suppress)
      .Default(::std::nullopt);
}
::std::optional<FailurePropagationMode> symbolizeFailurePropagationMode(uint32_t value) {
  switch (value) {
  case 1: return FailurePropagationMode::Propagate;
  case 2: return FailurePropagationMode::Suppress;
  default: return ::std::nullopt;
  }
}

bool FailurePropagationModeAttr::classof(::mlir::Attribute attr) {
  return (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(32)))) && (((attr.cast<::mlir::IntegerAttr>().getInt() == 1)) || ((attr.cast<::mlir::IntegerAttr>().getInt() == 2)));
}
FailurePropagationModeAttr FailurePropagationModeAttr::get(::mlir::MLIRContext *context, FailurePropagationMode val) {
  ::mlir::IntegerType intType = ::mlir::IntegerType::get(context, 32);
  ::mlir::IntegerAttr baseAttr = ::mlir::IntegerAttr::get(intType, static_cast<uint32_t>(val));
  return baseAttr.cast<FailurePropagationModeAttr>();
}
FailurePropagationMode FailurePropagationModeAttr::getValue() const {
  return static_cast<FailurePropagationMode>(::mlir::IntegerAttr::getInt());
}
} // namespace transform
} // namespace mlir

