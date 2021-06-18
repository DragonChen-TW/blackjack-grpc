const PROTO_PATH = '../protobuf/blackjack.proto';

var grpc = require('@grpc/grpc-js');
var protoLoader = require('@grpc/proto-loader');
var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true
    }
);
var blackjack_proto = grpc.loadPackageDefinition(packageDefinition);
const ActionNum = blackjack_proto.Action.type.enumType[0];
var client = new blackjack_proto.BlackJackService('localhost:30051', grpc.credentials.createInsecure());
// 

const express = require('express');

const app = express();
app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.use(express.static('public'));

app.use(express.static(__dirname + '/views'));

app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

p_idx = 0;

app.get('/', (req, res) => {
    res.render('index');
});

app.post('/send', (req, res) => {
    client.SendAction({
        action_num: req.query.action_num, // draw
        p_idx
    }, (err, data) => {
        console.log('action', data);
        res.json(data);
    });
});

app.post('/check', (req, res) => {
    client.CheckStatus({ p_idx }, (err, data) => {
        console.log('check', data);
        res.json(data);
    });
});

app.post('/history', (req, res) => {
    var data = [];
    client.GetHistory({ p_idx })
    .on('data', response => data.push(response))
    .on('end', () => res.json(data));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log('Server running at port %d', PORT);
});