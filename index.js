
const express = require('express')
const app = express()
const port = 4545
app.use('/node_modules', express.static('node_modules'))
app.use('/static', express.static('public'))
app.get('/', function (req, res) {
    res.redirect("/static")
  })
app.listen(port, () => console.log(`Example app listening on port ${port}!`))


