import logging
from pathlib import Path
import pynini

from pl_itn.src.tag import tag
from pl_itn.src.parse import parse_tokens
from pl_itn.src.permute import generate_permutations
from pl_itn.src.verbalize import verbalize
from pl_itn.src.restore_whitespace import restore_whitespaces
from pl_itn.src.restore_uppercase import restore_uppercase
from pl_itn.src.utils import pre_process, post_process

logger = logging.getLogger(__name__)

package_root = Path(__file__).parents[1]


class Normalizer:
    def __init__(
        self,
        tagger_fst_path: Path = package_root / "grammars/tagger.fst",
        verbalizer_fst_path: Path = package_root / "grammars/verbalizer.fst",
        debug_mode: bool = False,
    ):
        self._tagger_fst = pynini.Fst.read(str(tagger_fst_path))
        self._verbalizer_fst = pynini.Fst.read(str(verbalizer_fst_path))
        self.debug_mode = debug_mode

    @property
    def tagger_fst(self):
        return self._tagger_fst

    @property
    def verbalizer_fst(self):
        return self._verbalizer_fst

    def normalize(self, text: str) -> str:
        logger.debug(f"input: {text}")

        preprocessed_text = pre_process(text)

        if not preprocessed_text:
            logger.info("Empty input string")
            return text

        logger.debug(f"pre_process(): {preprocessed_text}")

        try:
            tagged_text = tag(self.tagger_fst, preprocessed_text)
            logger.debug(f"tag(): {tagged_text}")

            tokens = parse_tokens(tagged_text)
            logger.debug(f"parse(): {tokens}")

            tags_reordered = generate_permutations(tokens)
            logger.debug(f"generate_permutations(): {tags_reordered}")

            verbalized_text = verbalize(self.verbalizer_fst, tags_reordered)
            logger.debug(f"verbalize(): {verbalized_text}")

            postprocessed_text = post_process(verbalized_text)
            logger.debug(f"post_process(): {postprocessed_text}")

            uppercase_restored = restore_uppercase(text, postprocessed_text)
            logger.debug(f"restore_uppercase(): {uppercase_restored}")

            whitespaces_restored = restore_whitespaces(text, uppercase_restored, tokens)
            logger.debug(f"restore_whitespaces(): {whitespaces_restored}")

            return whitespaces_restored

        except ValueError as e:
            logger.error(e)
            if self.debug_mode:
                raise
            else:
                return text
