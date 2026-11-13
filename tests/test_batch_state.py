import unittest

from amazon_android.batch_state import BatchDraft
from amazon_android.core import ToolError


class BatchDraftTests(unittest.TestCase):
    def test_changing_batch_sizes_does_not_carry_counts(self):
        draft = BatchDraft()
        for size in (3, 5, 4):
            draft.replace("proxy", size)
            draft.replace("account", size)
            self.assertEqual(draft.count, size)
            draft.validate(size)
            old_id = draft.batch_id
            draft = draft.new()
            self.assertNotEqual(old_id, draft.batch_id)
            self.assertEqual((draft.proxy_count, draft.account_count), (0, 0))

    def test_mismatched_rows_block_run(self):
        draft = BatchDraft()
        draft.replace("proxy", 5)
        draft.replace("account", 3)
        with self.assertRaises(ToolError):
            draft.validate(5)
        draft.replace("account", 5)
        draft.validate(5)

    def test_account_rows_remain_visible_before_matching_proxies_are_pasted(self):
        draft = BatchDraft()
        draft.replace("account", 12)
        self.assertEqual(draft.count, 12)
        draft.replace("proxy", 4)
        self.assertEqual(draft.count, 12)
        with self.assertRaises(ToolError):
            draft.validate(12)

    def test_locked_batch_cannot_be_replaced(self):
        draft = BatchDraft()
        draft.locked = True
        with self.assertRaises(ToolError):
            draft.replace("proxy", 3)


if __name__ == "__main__":
    unittest.main()
