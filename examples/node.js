
// https://www.npmjs.com/package/node-json-rpc
// npm install node-json-rpc
var rpc = require('node-json-rpc');

var client = new rpc.Client({
      port: 8080,
      host: '127.0.0.1',
      path: '/',
});

client.call({
    "jsonrpc": "2.0",
    "method": "add",
    "params": {
      a: 1,
      b: 3
    },
    "id": 0
  },
  function(err, res) {
    if (err) {
      console.log("Error add");
      console.log(err);
    } else {
      console.log("Success add");
      console.log(res);
    }
  }
);
