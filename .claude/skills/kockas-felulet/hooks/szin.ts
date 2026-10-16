// A docs/DESIGN.md palettája két terminál-háttérre. Piros nincs: a túllépés
// információ, nem kudarc, ezért sárga. A főszöveg a téma saját színe (nem
// adunk neki színt), így világos és sötét terminálon is olvasható.

import type { Paletta } from '../types'

export type Szinek = {
  zold: string // rendben / ellenőrizve
  teny: string // a kereten belüli tény (szalag)
  sarga: string // túllépés, döntést kér
  alap: string // a szalag üres része, kihagyott hónap
}

export const SZINEK: Record<Paletta, Szinek> = {
  vilagos: { zold: '#3F6B52', teny: '#8FB39C', sarga: '#C9A642', alap: '#C9C2AE' },
  sotet: { zold: '#8FB39C', teny: '#8FB39C', sarga: '#E8C76A', alap: '#6B675E' },
}

// A téma neve a /config "theme" sora (pl. "light", "dark-daltonized").
export const palettaOf = (tema: unknown): Paletta =>
  typeof tema === 'string' && tema.includes('light') ? 'vilagos' : 'sotet'
