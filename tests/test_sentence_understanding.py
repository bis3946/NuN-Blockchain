import unittest

from nun_sue.sentence_understanding import understand_sentence


class SentenceUnderstandingTests(unittest.TestCase):
    def test_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            understand_sentence("   ")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            understand_sentence(None)  # type: ignore[arg-type]

    def test_rejects_oversized_input(self):
        with self.assertRaises(ValueError):
            understand_sentence("x" * 10001)

    def test_preserves_original_and_normalizes_whitespace(self):
        result = understand_sentence("  Molim   te provjeri status. ", language="hr")
        self.assertEqual(result.original_text, "  Molim   te provjeri status. ")
        self.assertEqual(result.normalized_text, "Molim te provjeri status.")

    def test_question_is_classified(self):
        result = understand_sentence("Where is the module?", language="en")
        self.assertEqual(result.intent, "question")
        self.assertFalse(result.needs_clarification)

    def test_simple_croatian_request_is_review_only(self):
        result = understand_sentence("Molim te provjeri status.", language="hr")
        self.assertEqual(result.intent, "request")
        self.assertEqual(result.route, "request_review")
        self.assertFalse(result.action_allowed)

    def test_ambiguous_input_requires_clarification(self):
        result = understand_sentence("blue sapphire", language="en")
        self.assertTrue(result.needs_clarification)
        self.assertEqual(result.route, "clarification")

    def test_unknown_language_is_rejected(self):
        with self.assertRaises(ValueError):
            understand_sentence("Hello", language="xx")

    def test_output_contract_is_serializable(self):
        result = understand_sentence("What is NuN?", language="en").to_dict()
        self.assertIn("policy_reason", result)
        self.assertFalse(result["action_allowed"])


if __name__ == "__main__":
    unittest.main()
