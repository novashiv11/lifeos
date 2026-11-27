"""Home = "Yaad": one reminder list (Late → Is hafte → Baad mein → Bina date), ✓ per row, one Jarvis button."""
import unittest

from tests.test_e2e import PhoneBase


class HomeFeedTest(PhoneBase):
    def setUp(self):
        super().setUp()
        self.pg.evaluate("localStorage.setItem('lifeos.settings', '{}'); 0")  # fresh user → v4 home
        self.pg.reload()
        self.pg.wait_for_function("typeof items !== 'undefined' && backend && R2.migrated")

    def sections(self):
        return self.pg.evaluate("""[...document.querySelectorAll('#view h2')].map(h => [h.innerText.toLowerCase(),
          [...h.nextElementSibling.querySelectorAll('.td-row')].map(r => r.innerText)])""")

    def test_yaad_sections(self):
        self.assertEqual(self.pg.get_attribute("body", "data-view"), "now")
        self.assertEqual(self.pg.inner_text("#title"), "Yaad")
        self.assertIn("Abhi kuch yaad nahi", self.pg.inner_text("#view"))
        self.pg.evaluate("""(async()=>{const t=R2.todayIso();
          await R2.create('task',{title:'Car tax',due_date:R2.addDays(t,-2)});
          await R2.create('case',{title:'BrandX: speaker',seller:'BrandX',next_action:'Chase if no reply',next_action_date:R2.addDays(t,-1),waiting_on:'them'});
          await R2.create('task',{title:'Dentist',due_date:R2.addDays(t,1)});
          for(let k=0;k<7;k++)await R2.create('deadline',{title:'later '+k,date:R2.addDays(t,30+k),date_known:true});
          await R2.create('task',{title:'Buy lamp'});
          await R2.create('journal',{title:'a note'});
          render()})(); 0""")
        self.pg.wait_for_function("items.size === 12")
        s = dict(self.sections())
        self.assertEqual([r.split("\n")[0] for r in s["late"]], ["Car tax", "BrandX: speaker"])
        self.assertIn("2 din late", s["late"][0])
        self.assertIn("BrandX reply nahi aaya", s["late"][1])
        self.assertEqual([r.split("\n")[0] for r in s["is hafte"]], ["Dentist"])
        self.assertIn("Kal", s["is hafte"][0])
        self.assertEqual(len(s["baad mein"]), 5)                           # long tail capped
        self.assertIn("+2 aur", self.pg.inner_text("#view"))
        self.assertEqual([r.split("\n")[0] for r in s["bina date"]], ["Buy lamp"])
        view = self.pg.inner_text("#view")
        self.assertNotIn("a note", view)                                    # notes are not reminders
        self.assertNotIn("Bank file", view)                                 # money and 🌱 left home
        self.assertNotIn("🌱", view)
        self.assertTrue(self.pg.is_visible("#view [data-askclaude]"))
        self.assertEqual(self.pg.evaluate("document.documentElement.scrollWidth"), 390)

    def test_tick_removes_row(self):
        self.pg.evaluate("R2.create('task',{title:'Dentist',due_date:R2.addDays(R2.todayIso(),1)}); 0")
        self.pg.wait_for_function("items.size === 1")
        self.pg.click("#view .td-row button.td-ok")
        self.pg.wait_for_function("[...items.values()][0].done")
        self.assertNotIn("Dentist", self.pg.inner_text("#view"))

    def test_question_from_home_answers_from_the_list(self):
        self.add("passport expires 2027-03-14")
        self.pg.wait_for_function("items.size === 1")
        self.pg.fill("#q", "passport ka kya scene hai?")
        self.pg.press("#q", "Enter")
        self.assertIn("passport expires 2027-03-14", self.pg.inner_text("#answer"))
        self.assertTrue(self.pg.is_visible("#answer [data-askclaude]"))   # "Ask Jarvis ↗" for more
        self.assertEqual(self.pg.evaluate("items.size"), 1)

    def test_no_leftover_daily_jarvis_nudge(self):
        """The daily Jarvis update was removed in v5.0: no notification for it may be planned."""
        self.pg.wait_for_timeout(300)
        nudges = self.pg.evaluate("""new Promise(ok => { const r = indexedDB.open('lifeos', 1);
          r.onsuccess = () => { const q = r.result.transaction('kv').objectStore('kv').get('nudges');
          q.onsuccess = () => ok(JSON.parse(q.result || '[]')); }; })""")
        self.assertEqual([n for n in nudges if n["kind"] == "daily"], [])

    def test_chase_card_marks_chased_and_moves_on(self):
        """A case card on Home has no screen to open any more: ✓ = chased, next chase in 5 working days."""
        self.pg.evaluate("""(async()=>{const t=R2.todayIso();
          await R2.create('case',{title:'BrandX: speaker',seller:'BrandX',next_action:'Chase if no reply',next_action_date:R2.addDays(t,-2),waiting_on:'them'});render()})(); 0""")
        self.pg.wait_for_function("items.size === 1")
        self.pg.click("#view .td-row button.td-ok")
        self.pg.wait_for_function("[...items.values()][0].next_action_date > R2.todayIso()")
        c = self.pg.evaluate("[...items.values()][0]")
        self.assertFalse(c["done"])
        self.assertEqual(len(c["timeline"]), 1)


if __name__ == "__main__":
    unittest.main()
