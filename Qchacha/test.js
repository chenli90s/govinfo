const { Chromeless } = require('chromeless')

async function run() {
  const chromeless = new Chromeless()

  const screenshot = await chromeless
    .goto('https://www.baidu.com')
    .type('chromeless', 'input[name="wd"]')
    .press(13)
    .wait('#wrapper_wrapper')
    .screenshot()

  console.log(screenshot) // prints local file path or S3 url

  await chromeless.end()
}

run().catch(console.error.bind(console))


function see() {
    res = m3CC.m3Y()
    console.log(res)
    while(typeof res == 'object'){
      res = res[1]
    }
    console.log(res)
}