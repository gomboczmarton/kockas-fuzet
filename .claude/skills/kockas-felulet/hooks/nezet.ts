// A nézet-modell beszerzése. Ez a fájl nem számol és nem dönt: lefuttatja a
// scripts/fuzetallapot.py-t, amely az ellenorzo.py számaiból összerakja a
// felület állapotát (melyik hónap, milyen helyzet), és azt adja tovább. A
// státuszsor (statusLine) ugyanezt a szkriptet használja.

import type { EngineInterface } from 'claude-code'

import type { Allapot } from '../types'

export async function betolt($: EngineInterface): Promise<Allapot> {
  const { exitCode, stdout } = await $.process.run(['python3', 'scripts/fuzetallapot.py'], {
    timeoutMs: 15_000,
  })
  if (exitCode !== 0) throw new Error(`fuzetallapot.py: kilépési kód ${exitCode}`)
  return JSON.parse(stdout) as Allapot
}
