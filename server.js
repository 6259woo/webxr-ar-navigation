const express = require('express');
const path = require('path');
const http = require('http');
const ngrok = require('ngrok');

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// HTTP 서버 + ngrok 연동
const server = http.createServer(app).listen(port, async () => {
    console.log(`HTTP 서버 실행 중. 접속: http://localhost:${port}`);

    try {
        const url = await ngrok.connect({
        addr: port,
        proto: 'http'
        });
        console.log(`Ngrok 작동! 주소: ${url}`);
    } catch (err) {
        console.error('ngrok 연결 실패:', err);
    }
});