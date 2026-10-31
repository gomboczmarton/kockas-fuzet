// A Kockás Füzet terminál-felülete (Claude Code mod).
//
// Kiegészítés, nem feltétel: a harness e nélkül is teljes (a mod korai
// hozzáférésű, távoli kapcsolóval kikapcsolható). Ezért nem kapu, nem
// számol, és nem ismétli a .claude/settings.json stabil rétegét (statusLine,
// spinnerVerbs): a füzetsort, a Füzetlapot, a nyugtázó buborékot és a
// prompt alatti tippet adja hozzá.

import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Allapot, Paletta } from '../types'
import { betolt } from './nezet'
import {
  fuzetlapMarkdown,
  fuzetlapOsszesito,
  fuzetlapSvg,
  fuzetlapTerminal,
  fuzetsor,
  FORRAS_SOR,
} from './rajz'
import { palettaOf, SZINEK } from './szin'

const PANEL = 'fuzetlap'
const PENZUGYI_FAJL = /(^|\/)penzugy\/(kassza\.csv|terv-\d{4}-\d{2}\.csv)$/

const allapot = atom({ plugin: 'kockas-felulet', key: 'allapot' } as const, null as Allapot | null)
const paletta = atom({ plugin: 'kockas-felulet', key: 'paletta' } as const, 'sotet' as Paletta)

async function frissit($: EngineInterface): Promise<Allapot | null> {
  try {
    const uj = await betolt($)
    await update($, allapot, () => uj)
    return uj
  } catch {
    // nincs python3, vagy a szkript nem futott: a felület csendben marad,
    // a harness szöveges útja ettől még működik
    await update($, allapot, () => null)
    return null
  }
}

const nyugta = (a: Allapot | null): string | undefined => {
  const n = a?.nezet
  if (!n || a?.helyzet !== 'havi') return undefined
  if (n.allapot === 'rendben') return `Ellenőrizve · ${n.honap ?? ''} rendben`
  const nevek = (n.terv_teny ?? []).filter(t => t.allapot === 'tullepes').map(t => t.kategoria)
  const dupla = (n.duplikatum_gyanu ?? []).length > 0 ? ['duplikátum-gyanú'] : []
  return `Ellenőrizve · döntést kér: ${[...nevek, ...dupla].join(', ')}`
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'fuzetlap',
      description: 'A hónap terv–tény lapja szalagokkal (számok: ellenorzo.py)',
    })
    try {
      const sor = (await $.config.list()).find(r => r.key === 'theme')
      await update($, paletta, () => palettaOf(sor?.value))
    } catch {
      // marad a sötét paletta, az világos háttéren is olvasható
    }
    await frissit($)
    return next(e)
  })

  // A kassza vagy egy terv módosult: újra-ellenőrzés és rövid nyugta. A
  // PostToolUse hook ettől függetlenül fut; ez csak megmutatja az eredményt.
  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    const ut = (e as { file_path?: unknown }).file_path
    if (typeof ut === 'string' && PENZUGYI_FAJL.test(ut) && ran.deny === undefined) {
      const szoveg = nyugta(await frissit($))
      if (szoveg !== undefined) $.ui.toast(szoveg)
    }
    return ran
  }).catch(($, e, next) => next(e)) // nem kapu: hibánál a hívás változatlanul megy tovább

  // Minden kör végén friss állapot (pl. ha Bash-sel került be sor).
  on('turn.complete', async ($, e, next) => {
    await frissit($)
    return next(e)
  })

  on('command.run', { command: 'fuzetlap' }, async $ => {
    const a = await frissit($)
    const { isPlaced } = await $.ui.open({ id: PANEL, title: 'Füzetlap' })
    // ahol nincs felület (pl. -p, SDK), ugyanaz szövegként
    return isPlaced ? { text: 'Füzetlap megnyitva.' } : { text: a ? fuzetlapMarkdown(a) : FORRAS_SOR }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const a = await read($, allapot)
    if (a === null) return next(e)
    const sz = SZINEK[await read($, paletta)]
    return fuzetsor($.ui.resolve(e), a, sz, e.props.bodyColumns)
  })

  on('ui.render', { component: 'Pane', requestId: PANEL }, async ($, e) => {
    const a = await read($, allapot)
    const sz = SZINEK[await read($, paletta)]
    if (e.surface === 'terminal') {
      const t = $.ui.resolve(e)
      return a === null
        ? <t.Text dimColor>A Füzetlap az ellenorzo.py kimenetéből rajzol — most nem futott.</t.Text>
        : fuzetlapTerminal(t, a, sz, e.props.bodyColumns)
    }
    // asztali és mobil: SVG-szalagok, alatta az összesítő mono számokkal
    const { Box, Svg, Text } = $.ui.resolve(e)
    if (a === null || a.nezet === null || a.helyzet !== 'havi') {
      return <Text>A Füzetlap a könyvelt hónapot mutatja — még nincs mit.</Text>
    }
    const { source, alt } = fuzetlapSvg(a.nezet)
    return (
      <Box flexDirection="column" gap={1}>
        <Svg source={source} alt={alt} />
        <Text mono>{fuzetlapOsszesito(a.nezet)}</Text>
        <Text size="footnote" dimColor>{FORRAS_SOR}</Text>
      </Box>
    )
  })

  // A kör végi sor magyarul (a motor angol "Baked for 3s" helyett).
  on('ui.render', { component: 'TurnDuration' }, async ($, e) => {
    const { Text } = $.ui.resolve(e)
    const mp = Math.max(1, Math.round(e.props.durationMs / 1000))
    const ido = mp < 60 ? `${mp} mp` : `${Math.floor(mp / 60)} p ${mp % 60} mp`
    return <Text dimColor>▦ {ido}</Text>
  })

  // Tipp a prompt alatt, amíg üres a prompt és nem dolgozik a modell.
  on('ui.render', { component: 'PromptHint' }, async ($, e, next) =>
    e.props.isDraft || e.props.isWorking
      ? next(e)
      : next({ ...e, props: { ...e.props, tail: '/fuzetlap · /belefer' } }),
  )
}
