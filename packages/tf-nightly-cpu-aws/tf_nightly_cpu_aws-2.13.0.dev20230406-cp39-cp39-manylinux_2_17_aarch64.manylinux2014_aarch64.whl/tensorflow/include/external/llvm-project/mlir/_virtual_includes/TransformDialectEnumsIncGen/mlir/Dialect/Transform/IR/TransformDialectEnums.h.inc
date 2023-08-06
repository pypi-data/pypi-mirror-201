/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Declarations                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace transform {
// Silenceable error propagation policy
enum class FailurePropagationMode : uint32_t {
  Propagate = 1,
  Suppress = 2,
};

::std::optional<FailurePropagationMode> symbolizeFailurePropagationMode(uint32_t);
::llvm::StringRef stringifyFailurePropagationMode(FailurePropagationMode);
::std::optional<FailurePropagationMode> symbolizeFailurePropagationMode(::llvm::StringRef);
inline constexpr unsigned getMaxEnumValForFailurePropagationMode() {
  return 2;
}


inline ::llvm::StringRef stringifyEnum(FailurePropagationMode enumValue) {
  return stringifyFailurePropagationMode(enumValue);
}

template <typename EnumType>
::std::optional<EnumType> symbolizeEnum(::llvm::StringRef);

template <>
inline ::std::optional<FailurePropagationMode> symbolizeEnum<FailurePropagationMode>(::llvm::StringRef str) {
  return symbolizeFailurePropagationMode(str);
}

class FailurePropagationModeAttr : public ::mlir::IntegerAttr {
public:
  using ValueType = FailurePropagationMode;
  using ::mlir::IntegerAttr::IntegerAttr;
  static bool classof(::mlir::Attribute attr);
  static FailurePropagationModeAttr get(::mlir::MLIRContext *context, FailurePropagationMode val);
  FailurePropagationMode getValue() const;
};
} // namespace transform
} // namespace mlir

namespace mlir {
template <typename T, typename>
struct FieldParser;

template<>
struct FieldParser<::mlir::transform::FailurePropagationMode, ::mlir::transform::FailurePropagationMode> {
  template <typename ParserT>
  static FailureOr<::mlir::transform::FailurePropagationMode> parse(ParserT &parser) {
    // Parse the keyword/string containing the enum.
    std::string enumKeyword;
    auto loc = parser.getCurrentLocation();
    if (failed(parser.parseOptionalKeywordOrString(&enumKeyword)))
      return parser.emitError(loc, "expected keyword for Silenceable error propagation policy");

    // Symbolize the keyword.
    if (::std::optional<::mlir::transform::FailurePropagationMode> attr = ::mlir::transform::symbolizeEnum<::mlir::transform::FailurePropagationMode>(enumKeyword))
      return *attr;
    return parser.emitError(loc, "invalid Silenceable error propagation policy specification: ") << enumKeyword;
  }
};
} // namespace mlir

namespace llvm {
inline ::llvm::raw_ostream &operator<<(::llvm::raw_ostream &p, ::mlir::transform::FailurePropagationMode value) {
  auto valueStr = stringifyEnum(value);
  return p << valueStr;
}
} // namespace llvm

namespace llvm {
template<> struct DenseMapInfo<::mlir::transform::FailurePropagationMode> {
  using StorageInfo = ::llvm::DenseMapInfo<uint32_t>;

  static inline ::mlir::transform::FailurePropagationMode getEmptyKey() {
    return static_cast<::mlir::transform::FailurePropagationMode>(StorageInfo::getEmptyKey());
  }

  static inline ::mlir::transform::FailurePropagationMode getTombstoneKey() {
    return static_cast<::mlir::transform::FailurePropagationMode>(StorageInfo::getTombstoneKey());
  }

  static unsigned getHashValue(const ::mlir::transform::FailurePropagationMode &val) {
    return StorageInfo::getHashValue(static_cast<uint32_t>(val));
  }

  static bool isEqual(const ::mlir::transform::FailurePropagationMode &lhs, const ::mlir::transform::FailurePropagationMode &rhs) {
    return lhs == rhs;
  }
};
}

