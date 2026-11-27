"""v4 core: reviewed migration (classic → typed), soft delete + Trash + undo, Home is tested in test_home_feed."""
import json
import unittest

from tests.test_e2e import PhoneBase

V1 = [  # generic fixture, nothing personal
    {"id": 1, "text": "Rent every month on the 20th", "domain": "home", "due": "2026-11-20", "repeat": {"every": 1, "unit": "month"}},
    {"id": 2, "text": "Residence card expires (date unknown)", "domain": "document", "due": None},
    {"id": 3, "text": "BrandX speaker refund: faulty, wants same colour", "domain": "shopping", "due": None},
    {"id": 4, "text": "Max 5 lines, Hinglish", "domain": "journal", "due": None},
    {"id": 5, "text": "Side project A; side project B; side project C ideas list", "domain": "idea", "due": None},
    {"id": 6, "text": "Call the plumber", "domain": "home", "due": None},
]


class MigrationTest(PhoneBase):
    def load_v1(self):
        items = [dict(i, created="2026-10-01T09:00:00", done=False, tags=[], tracking=[], metrics=[]) for i in V1]
        self.pg.evaluate(f"localStorage.removeItem('lifeos.v2'); localStorage.setItem('lifeos.items.v1', {json.dumps(json.dumps(items))}); 0")
        self.pg.reload()
        self.pg.wait_for_function("typeof items !== 'undefined' && backend && items.size === 6")

    def test_review_split_skip_and_approve(self):
        self.load_v1()
        self.assertFalse(self.pg.evaluate("R2.migrated"))
        self.pg.evaluate("view='migrate'; render(); 0")
        types = self.pg.eval_on_selector_all("[data-mg-type]", "s => s.map(x => x.value)")
        self.assertEqual(types, ["recurring", "deadline", "case", "fact", "journal", "task"])
        self.assertIn("date unknown → Needs info", self.pg.inner_text("[data-mg='1']"))
        self.assertIn("→ settings", self.pg.inner_text("[data-mg='3']"))
        self.assertIn("mixed? split it", self.pg.inner_text("[data-mg='4']"))
        # split the mixed idea into two, skip the plumber
        self.pg.fill("[data-mg-title='4']", "Side project A")
        self.pg.click("[data-mg-split='4']")
        self.pg.fill("[data-mg-title='5']", "Side project B")
        self.pg.select_option("[data-mg-type='5']", "project")
        self.pg.click("[data-mg-skip='6']")
        self.pg.evaluate("window.backupNow = () => {}; 0")
        self.pg.click("[data-mg-approve]")
        self.pg.wait_for_function("R2.migrated")
        recs = self.pg.evaluate("[...items.values()].map(r => [r.title, r.type, r.area])")
        self.assertIn(["Rent every month on the 20th", "recurring", "home"], recs)
        self.assertIn(["BrandX speaker refund: faulty, wants same colour", "case", "shopping"], recs)
        self.assertIn(["Side project B", "project", "ideas"], recs)
        self.assertNotIn("Call the plumber", [r[0] for r in recs])
        self.assertNotIn("Max 5 lines, Hinglish", [r[0] for r in recs])  # became settings
        self.assertEqual(self.pg.evaluate("[settings.max_lines, settings.language]"), [5, "hinglish"])
        dl = self.pg.evaluate("[...items.values()].find(r => r.type === 'deadline')")
        self.assertFalse(dl["date_known"])
        self.assertEqual(self.pg.evaluate("[...items.values()].find(r => r.type === 'case').seller"), "BrandX speaker")
        self.assertEqual(len(json.loads(self.pg.evaluate("localStorage.getItem('lifeos.items.v1')"))), 6)  # old data untouched
        self.pg.reload()
        self.pg.wait_for_function("typeof items !== 'undefined' && backend && R2.migrated")
        self.assertEqual(self.pg.evaluate("items.size"), 5)
        self.pg.evaluate("view='now'; render(); 0")
        self.assertIn("BINA DATE", self.pg.inner_text("#view"))  # unknown date stays visible on Home

    def test_upgrade_banner_on_today(self):
        self.load_v1()
        self.pg.evaluate("view='now'; render(); 0")
        self.assertIn("Upgrade to v4", self.pg.inner_text("#view"))


class TrashAndTodayTest(PhoneBase):
    def test_delete_undo_trash_restore_purge(self):
        self.assertTrue(self.pg.evaluate("R2.migrated"))  # a fresh phone starts on v4
        self.add("Call the plumber", "Buy bin bags")
        self.pg.wait_for_function("items.size === 2")
        self.pg.evaluate("change([...items.keys()][0], null, 'Deleted'); 0")
        self.pg.wait_for_function("items.size === 1 && R2.trash.size === 1")
        self.pg.click("#toastUndo")
        self.pg.wait_for_function("items.size === 2 && R2.trash.size === 0")
        self.pg.evaluate("change([...items.keys()][0], null, 'Deleted'); 0")
        self.tab("all")
        self.assertIn("Trash (1)", self.pg.inner_text("#trash"))
        self.pg.click("[data-tr-restore]")
        self.pg.wait_for_function("items.size === 2 && R2.trash.size === 0")
        # 31-day-old trash is purged on the next load
        self.pg.evaluate("change([...items.keys()][0], null, 'Deleted'); 0")
        self.pg.evaluate("[...R2.trash.values()][0].deleted_at = '2020-01-01T00:00:00'; R2.save(); 0")
        self.pg.reload()
        self.pg.wait_for_function("typeof items !== 'undefined' && backend && R2.migrated")
        self.assertEqual(self.pg.evaluate("R2.trash.size"), 0)

if __name__ == "__main__":
    unittest.main()
