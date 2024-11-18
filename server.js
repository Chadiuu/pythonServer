const express = require('express');
const net = require('net');

const app = express();
const PORT = 3000; 
const allowedIP = '192.168.10.6';

app.use(express.json());
app.use((req, res, next) => {
  const clientIP = req.ip.replace('::ffff:', '');
  if (clientIP !== allowedIP) {
    console.log(`Unauthorized access attempt from IP: ${clientIP}`);
    res.status(403).send('Access Denied');
    return;
  }
  next();
});
app.post('/send-message', (req, res) => {
  const { message } = req.body;

  const pythonHost = '127.0.0.1'; 
  const pythonPort = 65432;       

  const client = new net.Socket();
  client.connect(pythonPort, pythonHost, () => {
    console.log(`Connected to Python server. Sending message: ${message}`);
    client.write(message);
  });

  client.on('data', (data) => {
    console.log(`Response from Python: ${data}`);
    client.destroy(); 
    res.send(`Python server responded: ${data}`);
  });

  client.on('error', (err) => {
    console.error(`Error: ${err.message}`);
    res.status(500).send('Error communicating with Python server');
  });

  client.on('close', () => {
    console.log('Connection to Python server closed');
  });
});


app.use(express.static('public'));


app.listen(PORT,'0.0.0.0',() => {
  console.log(`Node.js server running on http://localhost:${PORT}`);
});
