// C++ Inverse Text Normalization for Russian using OpenFST.
//
// Consumes the grammars exported from the Python package with
// `python -m rus.export` and reproduces the same pipeline:
// tag -> reorder -> verbalize, taking the shortest path at each step.

#ifndef RUS_ITN_RUS_ITN_H_
#define RUS_ITN_RUS_ITN_H_

#include <memory>
#include <string>

#include <fst/fstlib.h>

namespace rus_itn {

class InverseNormalizer {
 public:
  // Loads the tagger and verbalizer grammars from OpenFST binary files
  // (rus_itn_tagger.fst / rus_itn_verbalizer.fst). Returns nullptr and
  // fills *error on failure.
  static std::unique_ptr<InverseNormalizer> FromFiles(
      const std::string& tagger_path, const std::string& verbalizer_path,
      std::string* error = nullptr);

  // Normalizes a UTF-8 sentence, e.g.
  //   "двадцать две тысячи сто один" -> "22101".
  // Returns false (and fills *error) if the input is not valid UTF-8 or the
  // grammar cannot parse it. `output` must not be null.
  bool Normalize(const std::string& text, std::string* output,
                 std::string* error = nullptr) const;

  // Convenience wrapper: returns the input unchanged if it cannot be parsed.
  std::string NormalizeOrPassthrough(const std::string& text) const;

 private:
  InverseNormalizer(std::unique_ptr<fst::StdConstFst> tagger,
                    std::unique_ptr<fst::StdConstFst> verbalizer);

  // ConstFst is immutable and documented by OpenFST as thread-safe.
  std::unique_ptr<fst::StdConstFst> tagger_;
  std::unique_ptr<fst::StdConstFst> verbalizer_;
};

}  // namespace rus_itn

#endif  // RUS_ITN_RUS_ITN_H_
