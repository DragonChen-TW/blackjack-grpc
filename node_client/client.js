const PROTO_PATH = "../protobuf/blackjack.proto";

const grpc = require("grpc");
const protoLoader = require("@grpc/proto-loader");

var packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    arrays: true
});

const BlackJackService = grpc.loadPackageDefinition(packageDefinition).BlackJackService;
const client = new BlackJackService(
    "localhost:30051",
    grpc.credentials.createInsecure()
);

module.exports = client;