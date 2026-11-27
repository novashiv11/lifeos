/* LifeOS v6 home "Yaad": one job, remind on time. Late → Is hafte → Baad mein → Bina date, ✓ per row, one Jarvis button. */
(()=>{
const css=`
.td-sec{display:block}.td-list{display:grid;gap:8px;margin:8px 0 0}
.td-row{display:flex;gap:10px;align-items:center;padding:12px 12px 12px 14px;border:1px solid var(--line);border-radius:18px;background:var(--card);min-width:0}
.td-row.hot{border-color:var(--late);box-shadow:inset 3px 0 0 var(--late)}
.td-main{flex:1;min-width:0;display:grid;gap:2px;text-align:left;background:none;border:0;padding:0;color:inherit;font:inherit}
.td-main b{font:600 15px var(--body);overflow-wrap:anywhere}.td-main small{color:var(--muted);font:12px var(--mono)}
.td-ok{flex:none;width:40px;height:40px;border-radius:12px;background:var(--chip);font-size:18px}
.td-empty{color:var(--muted);padding:6px 2px}
.td-tag{margin:0 0 4px;color:var(--muted);font-size:14px}
.td-late{color:var(--late)}
.td-ask{width:100%;margin-top:18px;padding:14px;border-radius:18px;border:1.5px solid var(--accent);background:none;color:var(--accent);font:700 16px var(--body)}`;
document.head.insertAdjacentHTML("beforeend",`<style>${css}</style>`);

const ICON={task:"✅",recurring:"🔁",deadline:"⏳",case:"⚖️",job:"🔧"};
const open=all=>all.filter(i=>!i.done&&!i.deleted_at);
const when=(it,today)=>{const n=daysLeft(it,today);return n<0?`${-n} din late`:n===0?"Aaj":n===1?"Kal":n<=7?`${n} din mein`:fmt(it.due)};
const fmt=d=>new Date(d+"T12:00").toLocaleDateString("en-IE",{day:"numeric",month:"short",year:d.slice(0,4)===R2.todayIso().slice(0,4)?undefined:"numeric"});
const LATER_MAX=5;
// Yaad (v6 home): one job, remind on time. Sections: Late → Is hafte → Baad mein (first 5) → Bina date.
function sections(all,today){
  const v=open(all).map(R2.view).filter(r=>ICON[r.type]), byDue=(a,b)=>a.due.localeCompare(b.due);
  const dated=v.filter(r=>r.due).sort(byDue), n=r=>daysLeft(r,today);
  return {late:dated.filter(r=>n(r)<0||(r.type==="case"&&n(r)===0)), week:dated.filter(r=>n(r)>=0&&n(r)<=7&&!(r.type==="case"&&n(r)===0)),
    later:dated.filter(r=>n(r)>7), nodate:v.filter(r=>!r.due)};
}
function sub(r,today){
  if(r.type==="case"&&r.waiting_on==="them"&&daysLeft(r,today)<=0)return `${r.seller||"Unka"} reply nahi aaya · ✓ jab chase karo`;
  const w=r.due?when(r,today):"Date nahi";
  return r.type==="recurring"?`${w} · repeat`:r.due&&daysLeft(r,today)>7&&windowOpen(r,today)?`${w} · abhi shuru karo`:w;
}
function row(r,today,hot){
  const act=r.type==="case"?`<button class="td-ok" data-td-chased="${r.id}" aria-label="I chased ${esc(r.title)}">✓</button>`
    :`<button class="td-ok" data-td-done="${r.id}" aria-label="Done: ${esc(r.title)}">✓</button>`;
  return `<div class="td-row${hot?" hot":""}"><div class="td-main"><b>${esc(r.title)}</b><small>${esc(sub(r,today))}</small></div>${act}</div>`;
}
function render2(all,today){
  const S=sections(all,today), part=(h,rows,hot,more)=>rows.length?`<section class="td-sec"><h2${hot?' class="td-late"':""}>${h}</h2><div class="td-list">${rows.map(r=>row(r,today,hot)).join("")}</div>${more||""}</section>`:"";
  const extra=S.later.length-LATER_MAX;
  const up=!R2.migrated&&items.size?`<button class="go" style="width:100%;padding:12px;margin-bottom:12px" data-v="migrate">⬆️ Upgrade to v4: records sort ho jayenge (1 min)</button>`:"";
  const empty=!S.late.length&&!S.week.length&&!S.later.length&&!S.nodate.length;
  return `${up}<p class="td-tag">Likh do, time pe yaad dilaunga. Jaise: "car tax 15 dec" · "rent monthly 1st"</p>
    ${empty?`<p class="td-empty">Abhi kuch yaad nahi dilana 🌿</p>`:""}
    ${part("Late",S.late,true)}${part("Is hafte",S.week)}
    ${part("Baad mein",S.later.slice(0,LATER_MAX),false,extra>0?`<button class="linkbtn" data-v="all">+${extra} aur ›</button>`:"")}${part("Bina date",S.nodate)}
    ${empty?"":`<button class="td-ask" data-askclaude="Meri list dekho. Kya pehle karun, aur kya bhool raha hoon?">Jarvis se help lo ↗</button>`}`;
}
document.addEventListener("click",async e=>{const b=e.target.closest&&e.target.closest("button");if(!b)return;
  if(b.dataset.tdDone){await complete(+b.dataset.tdDone);return}
  if(b.dataset.tdChased){const c=items.get(+b.dataset.tdChased);if(!c)return;const d=R2.addWorkingDays(todayDate(),5),nd=iso(d);
    await R2.update(c.id,{timeline:[...(c.timeline||[]),{at:R2.todayIso(),channel:"chase",by:"me",i_said:"Chased"}],waiting_on:"them",next_action:"Chase if no reply",next_action_date:nd},`Chased ✓ · next ${nd}`);return}
});

window.EXTRA_VIEWS=window.EXTRA_VIEWS||{};
EXTRA_VIEWS.now={title:"Yaad",render:render2,mount(){},_test:{sections}};
})();
