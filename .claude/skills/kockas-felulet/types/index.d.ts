// A felület állapot-szerződése. A nézet-modell az ellenorzo.py --json
// kimenete változtatás nélkül: minden összeg szöveg, ahogy a Decimal kiírja.

export type TervTeny = {
  kategoria: string
  keret: string
  teny: string
  elteres: string
  tullepes: string | null
  allapot: 'keretben' | 'tullepes'
}

export type Nezet = {
  sema: string
  forras: string
  honap: string | null
  tetelek?: number
  honapok?: Record<string, number>
  allapot: 'rendben' | 'dontest_ker' | 'nincs_adat' | 'hiba'
  kilepes: number
  uzenet?: string
  bevetel?: string
  kiadas?: string
  atvezetes?: string
  egyenleg_valtozas?: string
  kategoriak?: { kategoria: string; osszeg: string }[]
  duplikatum_gyanu?: { datum: string; leiras: string; osszeg: string }[]
  terv_teny?: TervTeny[]
  terven_kivul?: string[]
}

// Mit mutat a felület: üres füzet, visszatérés kihagyás után (a hátralék
// ilyenkor nem kerül elő), vagy a havi lap.
export type Helyzet = 'ures' | 'visszateres' | 'havi'

// A scripts/fuzetallapot.py kimenete változtatás nélkül.
export type Allapot = {
  sema?: string
  helyzet: Helyzet
  nezet: Nezet | null
  // a mostani naptári hónap (ÉÉÉÉ-HH), a négyzetsor jobb széle
  ma: string
  // mikor futott az ellenőrző (ÓÓ:PP), a pecsét alá
  frissitve: string | null
}

export type Paletta = 'vilagos' | 'sotet'

declare module 'claude-code' {
  interface PluginState {
    'kockas-felulet': { allapot: Allapot | null; paletta: Paletta }
  }
}
