# Felépítési sorrend (eval-first)

Az elv: **előbb a mérce,
aztán a komponens.** Minden lépésnél az a "kész" definíciója, hogy a
minta-adaton a megadott ellenőrzés zölden fut.

## 1. lépés — Alap + mérce (KÉSZ ebben a vázlatban)
- [x] Munkaterület-formátum rögzítése (README: `penzugy/` + `kassza.csv`)
- [x] `examples/minta-kivonat.csv` — szintetikus, ismert végösszegű adat
- [x] `scripts/ellenorzo.py` — kategória-összegek, terv–tény, duplikátum-jelzés
- [x] `templates/csaladi-kassza-sablon.md` — táblázat-spec ellenőrző képletekkel
- [x] `evals/` — 17 automatizált teszt (ground truth, Claude Code-szerkezet,
  hook végponttól végpontig): `bash evals/run.sh`
- Kész-kritérium: `bash evals/run.sh` zölden fut. ✔

## 2. lépés — 0. szint: receptek (KÉSZ vázlatként)
- [x] `prompts/01-kivonat-elemzes.md`, `prompts/02-havi-terv.md`
- Kész-kritérium: a recept a minta-kivonattal egy friss csevegőben értelmes
  eredményt ad (kézi próba, 3 különböző csevegőben).

## 3. lépés — 1. szint: skillek + verifikátor subagent (VÁZ KÉSZ)
- [x] `.claude/skills/kivonat-konyvelo/` — kivonat → kassza.csv, dedup-elvvel
- [x] `.claude/skills/havi-kor/` — terv + zárás
- [x] `.claude/skills/visszateres/` — lemaradás-bepótlás, shame-free
- [x] `.claude/agents/penzugyi-ellenor.md` — csak scriptet futtat, számot sosem becsül
- Kész-kritérium: mindhárom skill a minta-kivonaton végigfut úgy, hogy a
  penzugyi-ellenor zöldet ad; persona-próba: egy "3 hónapot kihagyott"
  forgatókönyv a visszateres skillel, hangnem-ellenőrzéssel (shame-free
  rubrika).

## 4. lépés — 3. szint: parancsok + hookok (VÁZ KÉSZ)
- [x] `.claude/commands/havizaras.md`, `.claude/commands/belefer.md`
- [x] `.claude/settings.json` + `.claude/hooks/` — kassza.csv-írás után auto-ellenőrzés
- Kész-kritérium: /havizaras a minta-munkaterületen elejétől végéig lefut,
  a hook ténylegesen elsüti az ellenorzo.py-t.

## 5. lépés — 2. szint: tematikus szeletek (STUB)
- [ ] `.claude/skills/nyaralas-tervezo/` — stub kész, kidolgozás később
- [ ] Mentor/coaching modul — külső szakértői tudásra épülne, ezért csak
  a megfelelő megállapodások után kerül be (addig szándékosan nincs itt)

## 6. lépés — Nyilvános indulás
- [x] Repo + MIT licenc + README (10 perces első élmény)
- [ ] Telepítő szkript a 3. szinthez
- [ ] Közösségi visszajelzések feldolgozása (issue-k, kérdőív-eredmények)
