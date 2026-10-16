// Rajzolás: tiszta függvények a nézet-modellből fára. A szabály, amit a
// tesztek is ellenőriznek: a GEOMETRIA számolható (milyen hosszú a szalag),
// a KIÍRT SZÁM nem — minden számjegy, ami a képernyőre kerül, betű szerint
// az ellenorzo.py kimenetéből jön. A tagolás és az előjel formázás.

import type { BoxProps, ElementConstructor, RenderElement, TextProps } from 'claude-code'

import type { Allapot, Nezet, TervTeny } from '../types'
import type { Szinek } from './szin'

export type Alap = {
  Box: ElementConstructor<BoxProps>
  Text: ElementConstructor<TextProps>
}

export const FORRAS_SOR = 'Minden szám: scripts/ellenorzo.py · a felület nem számol'

// "-234030" -> "−234 030"; "1250.5" -> "1 250,5". Csak formázás.
export const ft = (s: string): string => {
  const negativ = s.startsWith('-')
  const [egesz = '', tort] = s.replace(/^[-+]/, '').split('.')
  const tagolt = egesz.replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
  return (negativ ? '−' : '') + tagolt + (tort ? `,${tort}` : '')
}

// naptár, nem pénz: a négyzetsor hónapjai
export const elozoHonap = (honap: string): string => {
  const [ev = 0, ho = 1] = honap.split('-').map(Number)
  return ho === 1 ? `${ev - 1}-12` : `${ev}-${String(ho - 1).padStart(2, '0')}`
}

export const honapSor = (ma: string, db = 12): string[] => {
  const sor = [ma]
  while (sor.length < db) sor.unshift(elozoHonap(sor[0] ?? ma))
  return sor
}

// A szalag cellái: [kereten belüli tény, keret feletti rész, maradék keret].
export const szalag = (t: TervTeny, szel: number): [number, number, number] => {
  const keret = Number(t.keret)
  const teny = Math.max(0, Number(t.teny))
  if (!(keret > 0)) return teny > 0 ? [0, szel, 0] : [0, 0, szel]
  const arany = teny / keret
  if (arany <= 1) {
    const tele = Math.round(arany * szel)
    return [tele, 0, szel - tele]
  }
  const bent = Math.max(1, Math.round(szel / arany))
  return [bent, szel - bent, 0]
}

const dontestKer = (n: Nezet): TervTeny[] =>
  (n.terv_teny ?? []).filter(t => t.allapot === 'tullepes')

// ── a prompt fölötti füzetsor ────────────────────────────────────────────

export const fuzetsor = (
  { Box, Text }: Alap,
  a: Allapot,
  sz: Szinek,
  oszlop: number,
): RenderElement => {
  const fej = <Text color={sz.zold} weight="bold">▦ Kockás Füzet</Text>
  if (a.helyzet === 'ures' || a.nezet === null) {
    const szoveg =
      a.helyzet === 'visszateres'
        ? 'jó, hogy itt vagy · ha szeretnéd, együtt rendbe tesszük: „bepótolnám”'
        : 'a füzet még üres · kipróbálnád a mintával? írd: „próbáljuk ki a mintával”'
    return (
      <Box flexDirection="row" gap={2}>
        {fej}
        <Text dimColor wrap="truncate-end">{szoveg}</Text>
      </Box>
    )
  }
  const n = a.nezet
  if (n.allapot === 'hiba') {
    return (
      <Box flexDirection="row" gap={2}>
        {fej}
        <Text color={sz.sarga}>◆ az ellenőrző egy sort nem tudott beolvasni — nézzük meg együtt</Text>
      </Box>
    )
  }
  const honapok = n.honapok ?? {}
  // (a paraméter nem lehet `h`: az a JSX-gyár neve)
  const negyzetek = honapSor(a.ma).map(ho => (
    <Text color={ho === n.honap ? sz.zold : (honapok[ho] ?? 0) > 0 ? sz.teny : sz.alap}>
      {(honapok[ho] ?? 0) > 0 ? '■' : '□'}{' '}
    </Text>
  ))
  const pecset =
    n.allapot === 'rendben'
      ? <Text color={sz.zold}>✓ ellenőrizve {a.frissitve ?? ''}</Text>
      : <Text color={sz.sarga}>◆ döntést kér</Text>
  const tullep = dontestKer(n)
  const dupla = n.duplikatum_gyanu ?? []
  const masodik =
    tullep.length > 0 || dupla.length > 0 ? (
      <Text color={sz.sarga} wrap="truncate-end">
        {[
          ...tullep.map(t => `${t.kategoria} +${ft(t.tullepes ?? '')}`),
          ...dupla.map(d => `duplikátum-gyanú: ${d.leiras} (${d.datum})`),
        ].join(' · ')}
      </Text>
    ) : (
      <Text dimColor>minden kategória kereten belül · /fuzetlap</Text>
    )
  return (
    <Box flexDirection="column">
      <Box flexDirection="row" gap={2}>
        {fej}
        <Text>{n.honap ?? ''}</Text>
        {oszlop >= 72 ? <Text>{negyzetek}</Text> : null}
        {pecset}
      </Box>
      <Box paddingLeft={2}>{masodik}</Box>
    </Box>
  )
}

// ── a Füzetlap panel ─────────────────────────────────────────────────────

const osszesito = (n: Nezet): string =>
  [
    `Bevétel ${ft(n.bevetel ?? '0')}`,
    `Kiadás ${ft(n.kiadas ?? '0')}`,
    `Megtakarítás ${ft(n.atvezetes ?? '0')}`,
    `Egyenleg-változás ${elojeles(n.egyenleg_valtozas ?? '0')}`,
  ].join(' · ')

// "+285 970" / "−5 000": az előjel is csak formázás
const elojeles = (s: string): string => (s.startsWith('-') ? ft(s) : `+${ft(s)}`)

const OSSZEG_SZEL = 17 // "100 000 / 100 000"
const ALLAPOT_SZEL = 9 // "keretben" / "+5 000 ◆"

export const fuzetlapTerminal = (
  { Box, Text }: Alap,
  a: Allapot,
  sz: Szinek,
  oszlop: number,
): RenderElement => {
  const n = a.nezet
  if (a.helyzet !== 'havi' || n === null || n.allapot === 'hiba') {
    return <Box><Text dimColor>A Füzetlap a könyvelt hónapot mutatja — még nincs mit.</Text></Box>
  }
  const sorok = n.terv_teny ?? []
  const nevSzel = Math.min(14, Math.max(8, ...sorok.map(t => t.kategoria.length)))
  // a szalag kapja, ami a rögzített oszlopok után marad (a pane belső szélessége)
  const szel = Math.max(6, Math.min(28, oszlop - nevSzel - OSSZEG_SZEL - ALLAPOT_SZEL - 3))
  const rendben = n.allapot === 'rendben'
  return (
    <Box flexDirection="column">
      <Box flexDirection="row" justifyContent="space-between">
        <Text weight="bold" wrap="truncate-end">Füzetlap · {n.honap ?? ''}</Text>
        <Text color={rendben ? sz.zold : sz.sarga} wrap="truncate-end">
          {rendben ? '✓ ellenőrizve' : '◆ döntést kér'} · {a.frissitve ?? ''}
        </Text>
      </Box>
      {sorok.length === 0 ? <Text dimColor>Ehhez a hónaphoz még nincs terv-fájl (penzugy/terv-{n.honap ?? ''}.csv).</Text> : null}
      {sorok.map(t => {
        const [bent, felett, maradek] = szalag(t, szel)
        return (
          <Box flexDirection="row" gap={1}>
            <Box flexShrink={0} width={nevSzel}>
              <Text wrap="truncate-end">{t.kategoria}</Text>
            </Box>
            <Box flexShrink={0} width={szel}>
              <Text>
                <Text color={sz.teny}>{'█'.repeat(bent)}</Text>
                <Text color={sz.sarga}>{'█'.repeat(felett)}</Text>
                <Text color={sz.alap}>{'░'.repeat(maradek)}</Text>
              </Text>
            </Box>
            <Box flexShrink={0} width={OSSZEG_SZEL}>
              <Text wrap="truncate-start">{`${ft(t.teny)} / ${ft(t.keret)}`.padStart(OSSZEG_SZEL)}</Text>
            </Box>
            {t.allapot === 'tullepes'
              ? <Text color={sz.sarga} wrap="truncate-end">+{ft(t.tullepes ?? '')} ◆</Text>
              : <Text dimColor wrap="truncate-end">keretben</Text>}
          </Box>
        )
      })}
      {(n.duplikatum_gyanu ?? []).map(d => (
        <Text color={sz.sarga}>◆ duplikátum-gyanú, nézd meg: {d.datum} | {d.leiras} | {ft(d.osszeg)}</Text>
      ))}
      {(n.terven_kivul ?? []).length > 0
        ? <Text dimColor>Tervben nem szereplő: {(n.terven_kivul ?? []).join(', ')}</Text>
        : null}
      <Box flexDirection="column" marginTop={1}>
        <Text>Bevétel {ft(n.bevetel ?? '0')} · Kiadás {ft(n.kiadas ?? '0')}</Text>
        <Text>Megtakarítás {ft(n.atvezetes ?? '0')} · Egyenleg-változás {elojeles(n.egyenleg_valtozas ?? '0')}</Text>
      </Box>
      <Text dimColor>{FORRAS_SOR}</Text>
    </Box>
  )
}

// Asztali és mobil felületen ugyanaz a lap SVG-ként, a DESIGN.md szerint:
// saját papír-háttér 24 px-es ráccsal, serif a szó, mono a gép száma.
const esc = (s: string): string =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

export const fuzetlapSvg = (n: Nezet): { source: string; alt: string } => {
  const sorok = n.terv_teny ?? []
  const W = 640
  const sorMag = 32
  const H = 56 + sorok.length * sorMag + 24
  const szalagX = 150
  const szalagW = 260
  const racs: string[] = []
  for (let x = 0; x <= W; x += 24) racs.push(`<line x1="${x}" y1="0" x2="${x}" y2="${H}"/>`)
  for (let y = 0; y <= H; y += 24) racs.push(`<line x1="0" y1="${y}" x2="${W}" y2="${y}"/>`)
  const sorSvg = sorok.map((t, i) => {
    const y = 56 + i * sorMag
    const [bent, felett, maradek] = szalag(t, szalagW)
    const szoveg =
      t.allapot === 'tullepes' ? `+${ft(t.tullepes ?? '')} · döntést kér` : 'keretben'
    return [
      `<text x="16" y="${y + 15}" font-family="Georgia, serif" font-size="14" fill="#23231F">${esc(t.kategoria)}</text>`,
      `<rect x="${szalagX}" y="${y + 3}" width="${bent}" height="14" fill="#8FB39C"/>`,
      `<rect x="${szalagX + bent}" y="${y + 3}" width="${felett}" height="14" fill="#E8C76A"/>`,
      `<rect x="${szalagX + bent + felett}" y="${y + 3}" width="${maradek}" height="14" fill="#F2EFE6" stroke="#CFC8B5"/>`,
      `<text x="${szalagX + szalagW + 12}" y="${y + 15}" font-family="ui-monospace, Menlo, monospace" font-size="12" fill="#4A4740">${esc(`${ft(t.teny)} / ${ft(t.keret)}`)}</text>`,
      `<text x="${W - 16}" y="${y + 15}" text-anchor="end" font-family="ui-monospace, Menlo, monospace" font-size="11" fill="${t.allapot === 'tullepes' ? '#C9A642' : '#6B675E'}">${esc(szoveg)}</text>`,
    ].join('')
  })
  const source =
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">` +
    `<rect width="${W}" height="${H}" fill="#FDFCF8"/>` +
    `<g stroke="#E3EBF0" stroke-width="1">${racs.join('')}</g>` +
    `<text x="16" y="32" font-family="Georgia, serif" font-size="20" fill="#23231F">Füzetlap · ${esc(n.honap ?? '')}</text>` +
    `<text x="${W - 16}" y="32" text-anchor="end" font-family="ui-monospace, Menlo, monospace" font-size="11" fill="${n.allapot === 'rendben' ? '#3F6B52' : '#C9A642'}">${n.allapot === 'rendben' ? '✓ ellenőrizve' : '◆ döntést kér'} · ellenorzo.py</text>` +
    sorSvg.join('') +
    `</svg>`
  const alt =
    `Füzetlap ${n.honap ?? ''}: ` +
    sorok
      .map(t =>
        `${t.kategoria} ${ft(t.teny)} / ${ft(t.keret)}` +
        (t.allapot === 'tullepes' ? `, túllépés ${ft(t.tullepes ?? '')}` : ', keretben'))
      .join('; ')
  return { source, alt }
}

export const fuzetlapOsszesito = osszesito

// Szöveges tartalék oda, ahol a panel nem jelenik meg (pl. nincs felület):
// ugyanazok a számok markdown-táblában.
export const fuzetlapMarkdown = (a: Allapot): string => {
  const n = a.nezet
  if (a.helyzet !== 'havi' || n === null) return 'A Füzetlap a könyvelt hónapot mutatja — még nincs mit.'
  const sorok = (n.terv_teny ?? []).map(t =>
    `| ${t.kategoria} | ${ft(t.teny)} | ${ft(t.keret)} | ${t.allapot === 'tullepes' ? `+${ft(t.tullepes ?? '')} · döntést kér` : 'keretben'} |`)
  return [
    `**Füzetlap · ${n.honap ?? ''}**`,
    '',
    '| kategória | tény | keret | |',
    '|---|---:|---:|---|',
    ...sorok,
    '',
    osszesito(n),
    '',
    `_${FORRAS_SOR}_`,
  ].join('\n')
}
