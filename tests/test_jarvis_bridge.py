"""Coming back from Jarvis in Claude: one tap pastes the reply; our own prompt on the clipboard is never saved."""
import unittest
from urllib.parse import unquote

from tests.test_e2e import PhoneBase

STUB = "window.__opened=[]; window.open=(u)=>{window.__opened.push(u);return null}; navigator.clipboard.writeText=async()=>{}; 0"
NUDGES = """new Promise(ok => { const r = indexedDB.open('lifeos', 1);
  r.onsuccess = () => { const q = r.result.transaction('kv').objectStore('kv').get('nudges');
  q.onsuccess = () => ok(JSON.parse(q.result || '[]')); }; })"""


class ReturnFromClaudeTest(PhoneBase):
    def test_paste_nudge_ignores_own_prompt_then_reads_reply(self):
        self.pg.evaluate(STUB + "; window.__clip=''; navigator.clipboard.readText=async()=>window.__clip; 0")
        self.tab("jarvis")
        self.pg.fill("#aq", "kya pending hai?")
        self.pg.press("#aq", "Enter")
        self.tab("home")
        self.pg.wait_for_selector("#pasteNudge")
        self.pg.evaluate("window.__clip = lastPrompt; 0")  # Claude reply not copied yet: our own prompt is on the clipboard
        self.pg.click("#pasteNudge")
        self.assertIn("reply copy karo", self.pg.inner_text("#toast"))
        self.assertIsNone(self.pg.evaluate("pasteResult"))
        self.pg.evaluate("window.__clip = 'Sure!\\nLIFEOS\\n+ dentist 3 nov 10am\\ndone #99'; 0")
        self.pg.click("#pasteNudge")
        self.pg.click("[data-paste=apply]")
        self.pg.wait_for_function("items.size >= 1")
        self.assertEqual(self.pg.query_selector_all("#pasteNudge"), [])
        self.assertIn("dentist 3 nov 10am", self.items())



if __name__ == "__main__":
    unittest.main()
