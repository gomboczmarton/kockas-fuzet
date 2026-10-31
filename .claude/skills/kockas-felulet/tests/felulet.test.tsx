// A felület tesztjei. Három dolgot bizonyítanak:
// 1. Szám-eredet: minden számjegy a képernyőn betű szerint az ellenorzo.py
//    kimenetéből jön (a felület nem számol).
// 2. Hangnem: nincs piros, nincs minősítő szó, visszatéréskor nincs hátralék.
// 3. Tartalék: ahol a panel nem jelenik meg, ugyanaz szövegként érkezik.
// A python-futást és a fájlrendszert a teszt adja alulról; a nézet-modell
// a minta-adat valódi --json kimenete (examples/, GROUND-TRUTH.md).

import { describe, expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

const PLUGIN = 'kockas-felulet'

const JULIUS = {
  sema: 'kockas-ellenorzo/1', forras: 'ellenorzo.py', honap: '2026-07', tetelek: 15,
  honapok: { '2026-05': 12, '2026-07': 15 }, allapot: 'dontest_ker', kilepes: 1,
  bevetel: '620000', kiadas: '-234030', atvezetes: '-100000', egyenleg_valtozas: '285970',
  kategoriak: [{ kategoria: 'elelmiszer', osszeg: '-99450' }],
  duplikatum_gyanu: [],
  terv_teny: [
    { kategoria: 'egeszseg', keret: '10000', teny: '8750', elteres: '1250', tullepes: null, allapot: 'keretben' },
    { kategoria: 'elelmiszer', keret: '100000', teny: '99450', elteres: '550', tullepes: null, allapot: 'keretben' },
    { kategoria: 'keszpenz', keret: '40000', teny: '40000', elteres: '0', tullepes: null, allapot: 'keretben' },
    { kategoria: 'szabadido', keret: '10000', teny: '15000', elteres: '-5000', tullepes: '5000', allapot: 'tullepes' },
  ],
  terven_kivul: [],
}

// a scripts/fuzetallapot.py kimenete a három helyzetben
const HAVI = { sema: 'kockas-allapot/1', ma: '2026-07', helyzet: 'havi', frissitve: '14:02', nezet: JULIUS }
const VISSZA = { sema: 'kockas-allapot/1', ma: '2026-10', helyzet: 'visszateres', frissitve: '09:00', nezet: null }
const URES = { sema: 'kockas-allapot/1', ma: '2026-07', helyzet: 'ures', frissitve: '09:00', nezet: null }

const allowedHex = new Set(['#3F6B52', '#8FB39C', '#C9A642', '#E8C76A', '#C9C2AE', '#6B675E'])
const TILTOTT = /sajnos|megint|\bcsak\b|kudarc|hátralék|lemarad|elmarad|késés/i

function alap(on: On, opts: { allapot?: object; placed?: boolean } = {}) {
  const toasts: string[] = []
  // ami a plugin alatt van: a motor helyett a teszt felel ({ value } a $-hívásokra)
  on('session.start', ($, e) => ({ cwd: e.cwd }))
  on('command.register', ($, e) => ({ value: { command: e.name } }))
  on('config.list', () => ({ value: [] }))
  on('ui.toast', ($, e) => {
    toasts.push(e.text)
    return { value: undefined }
  })
  on('ui.open', () => ({ value: opts.placed === false ? { isPlaced: false, reason: 'no-surface' } : { isPlaced: true } }) as never)
  on('process.run', ($, e) => {
    expect(e.argv).toEqual(['python3', 'scripts/fuzetallapot.py'])
    const stdout = JSON.stringify(opts.allapot ?? HAVI)
    return { value: { exitCode: 0, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }
  })
  // a motor saját rajza helyett egy üres sor (ahol a plugin továbbadja)
  on('ui.render', ($, e) => {
    const { Text } = $.ui.resolve(e)
    return <Text>{''}</Text>
  })
  return toasts
}

const BAND = {
  plugin: PLUGIN, component: 'AbovePrompt' as const,
  props: { hasSurvey: false, isWorking: false, maxRows: 8, bodyColumns: 100, scroll: { offset: 0, bodyRows: 8 }, view: {} },
}
const PANE = {
  plugin: PLUGIN, component: 'Pane' as const, requestId: 'fuzetlap',
  props: { title: 'Füzetlap', isFocused: false, bodyColumns: 96, placement: 'dock' as const, scroll: { offset: 0, bodyRows: 30 }, view: {} },
}

const indit = ($: { session: { start: (e: { cwd: string; surface: 'terminal'; isInteractive: boolean }) => Promise<unknown> } }) =>
  $.session.start({ cwd: '/fuzet', surface: 'terminal', isInteractive: true })

// minden szám, ami a nézet-modellben szerepel (előjel nélkül)
const engedett = (n: unknown): Set<string> => {
  const ki = new Set<string>()
  const jar = (v: unknown) => {
    if (typeof v === 'string' && /^-?\d+(\.\d+)?$/.test(v)) ki.add(v.replace(/^-/, ''))
    else if (Array.isArray(v)) v.forEach(jar)
    else if (v && typeof v === 'object') Object.values(v).forEach(jar)
  }
  jar(n)
  return ki
}

// a képernyő számai: dátum, időpont és fájlnév kivéve, tagolás és előjel le
const kepernyoSzamai = (szoveg: string): string[] =>
  (szoveg
    .replace(/\d{4}-\d{2}(-\d{2})?/g, ' ')
    .replace(/\d{1,2}:\d{2}/g, ' ')
    .match(/\d[\d ]*(,\d+)?/g) ?? [])
    .map(s => s.replace(/ /g, '').replace(',', '.'))

describe('füzetsor (prompt fölött)', () => {
  test('havi lap: hónap, pecsét, a döntést kérő kategória a szkript számával', async ($, on) => {
    alap(on)
    await indit($)
    for (const surface of ['terminal', 'desktop'] as const) {
      const ui = await $.ui.mount({ ...BAND, surface })
      const szoveg = (await ui.findAll({ type: 'Text' })).map(t => t.text).join('\n')
      expect(szoveg).toContain('Kockás Füzet')
      expect(szoveg).toContain('2026-07')
      expect(szoveg).toContain('döntést kér')
      expect(szoveg).toContain('szabadido +5 000')
      await ui.unmount()
    }
  })

  test('szám-eredet: minden kiírt szám az ellenorzo.py kimenetéből jön', async ($, on) => {
    alap(on)
    await indit($)
    const szabad = engedett(JULIUS)
    for (const [cel, surface] of [[BAND, 'terminal'], [PANE, 'terminal'], [PANE, 'desktop']] as const) {
      const ui = await $.ui.mount({ ...cel, surface } as never)
      const elemek = await ui.findAll({})
      const szoveg = elemek.map(t => `${t.text} ${String(t.props.alt ?? '')}`).join('\n')
      const szamok = kepernyoSzamai(szoveg)
      // ne lehessen üres rajzzal átmenni: a lapon legalább a szalag-számok ott vannak
      expect(szamok.length).toBeGreaterThan(cel === BAND ? 0 : 6)
      for (const szam of szamok) expect(szabad.has(szam)).toBe(true)
      await ui.unmount()
    }
  })

  test('hangnem: nincs piros, nincs minősítő szó, csak a DESIGN.md színei', async ($, on) => {
    alap(on)
    await indit($)
    for (const cel of [BAND, PANE]) {
      const ui = await $.ui.mount({ ...cel, surface: 'terminal' } as never)
      for (const t of await ui.findAll({ type: 'Text' })) {
        expect(TILTOTT.test(t.text)).toBe(false)
        const c = t.props.color
        if (c !== undefined) expect(allowedHex.has(String(c))).toBe(true)
      }
      await ui.unmount()
    }
  })

  test('visszatérés: a köszöntés jön, nem a kihagyott hónapok', async ($, on) => {
    alap(on, { allapot: VISSZA })
    await indit($)
    const ui = await $.ui.mount({ ...BAND, surface: 'terminal' })
    const szoveg = (await ui.findAll({ type: 'Text' })).map(t => t.text).join('\n')
    expect(szoveg).toContain('jó, hogy itt vagy')
    expect(szoveg).not.toContain('□')
    expect(szoveg).not.toContain('döntést kér')
    expect(kepernyoSzamai(szoveg)).toEqual([])
    await ui.unmount()
  })

  test('üres füzet: a minta kipróbálását ajánlja', async ($, on) => {
    alap(on, { allapot: URES })
    await indit($)
    const ui = await $.ui.mount({ ...BAND, surface: 'terminal' })
    expect(await ui.find({ type: 'Text', text: /mintával/ })).toBeDefined()
    await ui.unmount()
  })
})

describe('Füzetlap', () => {
  test('terminálon szalag-sorok, asztalin és mobilon SVG a számokkal az alt-ban', async ($, on) => {
    alap(on)
    await indit($)
    const term = await $.ui.mount({ ...PANE, surface: 'terminal' })
    expect(await term.find({ type: 'Text', text: /15 000 \/ 10 000/ })).toBeDefined()
    expect(await term.find({ type: 'Text', text: /ellenorzo\.py/ })).toBeDefined()
    await term.unmount()
    for (const surface of ['desktop', 'mobile'] as const) {
      const ui = await $.ui.mount({ ...PANE, surface })
      const svg = await ui.find({ type: 'Svg' })
      expect(svg).toBeDefined()
      expect(String(svg?.props.alt)).toContain('szabadido 15 000 / 10 000, túllépés 5 000')
      await ui.unmount()
    }
  })

  test('/fuzetlap: ahol a panel nem jelenik meg, markdown-tábla a tartalék', async ($, on) => {
    alap(on, { placed: false })
    await indit($)
    const ki = await $.command.run({
      command: 'fuzetlap', args: '', origin: { kind: 'person' } as never,
      presentation: { isFullscreen: false, columns: 100 } as never,
    })
    expect(ki.text ?? '').toContain('| szabadido | 15 000 | 10 000 | +5 000 · döntést kér |')
  })

  test('a kassza módosítása után nyugta-buborék, számok nélkül', async ($, on) => {
    const toasts = alap(on)
    on('tool.call', () => ({ result: {}, text: 'ok' }) as never)
    await indit($)
    await $.tool.call({ tool: 'Edit', file_path: 'penzugy/kassza.csv', old_string: 'a', new_string: 'b' } as never)
    expect(toasts).toEqual(['Ellenőrizve · döntést kér: szabadido'])
  })
})
