// Böngészős próba a Füzetlap MCP App nézetéhez: egy minimális "gazda" (host)
// sandboxolt iframe-be tölti a nézetet, végigviszi az MCP Apps kézfogást
// (ui/initialize → ui/notifications/initialized → ui/notifications/tool-result),
// és minden üzenetet mindkét irányban rögzít, hogy a hívó a hivatalos
// @modelcontextprotocol/ext-apps sémával ellenőrizhesse.
//
// Használat: NODE_PATH=$(npm root -g) node gazda_proba.cjs <nezet.html> <tool-result.json> <kimenet-mappa>
// Kimenet: <mappa>/uzenetek.json, <mappa>/szoveg-{light,dark}.txt, <mappa>/fuzetlap-{light,dark}.png

const fs = require('fs')
const path = require('path')
const { chromium } = require('playwright')

const [nezetUt, eredmenyUt, ki] = process.argv.slice(2)
const nezet = fs.readFileSync(nezetUt, 'utf8')
const eredmeny = JSON.parse(fs.readFileSync(eredmenyUt, 'utf8'))
fs.mkdirSync(ki, { recursive: true })

const gazdaOldal = tema => `<!doctype html><html><body style="margin:0;background:#888">
<iframe id="app" sandbox="allow-scripts" style="width:640px;height:420px;border:0;background:white"></iframe>
<script>
  window.__uzenetek = []
  const app = document.getElementById('app')
  const valaszol = m => { window.__uzenetek.push({ irany: 'gazda->nezet', m }); app.contentWindow.postMessage(m, '*') }
  window.addEventListener('message', ev => {
    if (ev.source !== app.contentWindow) return
    const m = ev.data
    window.__uzenetek.push({ irany: 'nezet->gazda', m })
    if (m.method === 'ui/initialize') {
      valaszol({ jsonrpc: '2.0', id: m.id, result: {
        protocolVersion: '2026-01-26',
        hostInfo: { name: 'kockas-proba-gazda', version: '0.1.0' },
        hostCapabilities: {},
        hostContext: { theme: '${tema}', displayMode: 'inline', locale: 'hu-HU' } } })
    }
    if (m.method === 'ui/notifications/initialized') {
      valaszol({ jsonrpc: '2.0', method: 'ui/notifications/tool-result', params: window.__eredmeny })
    }
    if (m.method === 'ui/notifications/size-changed') window.__meret = m.params
  })
</script></body></html>`

;(async () => {
  const bongeszo = await chromium.launch()
  const osszes = []
  for (const tema of ['light', 'dark']) {
    const oldal = await bongeszo.newPage({ viewport: { width: 660, height: 440 } })
    await oldal.setContent(gazdaOldal(tema))
    await oldal.evaluate(e => { window.__eredmeny = e }, eredmeny)
    await oldal.evaluate(h => { document.getElementById('app').srcdoc = h }, nezet)
    await oldal.waitForFunction(() => window.__meret !== undefined, null, { timeout: 10000 })
    const keret = oldal.frames().find(f => f !== oldal.mainFrame())
    const szoveg = await keret.evaluate(() => document.getElementById('lap').innerText)
    fs.writeFileSync(path.join(ki, `szoveg-${tema}.txt`), szoveg)
    await oldal.locator('#app').screenshot({ path: path.join(ki, `fuzetlap-${tema}.png`) })
    osszes.push(...(await oldal.evaluate(() => window.__uzenetek)).map(u => ({ tema, ...u })))
    await oldal.close()
  }
  fs.writeFileSync(path.join(ki, 'uzenetek.json'), JSON.stringify(osszes, null, 1))
  await bongeszo.close()
  console.log(`${osszes.length} üzenet, ${ki}`)
})().catch(h => { console.error(h); process.exit(1) })
