const express = require('express')
const sls = require('serverless-http') 
const { InMemorySigner } = require('@taquito/signer');
const { TezBridgeSigner } = '@taquito/tezbridge-signer';
const {TezosToolkit, MichelCodecPacker } = require('@taquito/taquito');

const bodyParser = require('body-parser')
const app = express()
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const acc = require('./ithacanet.json')

const request = require('request');
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

app.set('views', __dirname);

const tezos = new TezosToolkit('https://ithacanet.smartpy.io');

const contractKey='KT19WAyghvtMaEQzb88AEU6HxdPT8GfRfbJK';


const privateKey ="tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv";
const https = require("https");
tezos.setPackerProvider(new MichelCodecPacker());
tezos.setSignerProvider(InMemorySigner.fromFundraiser(acc.email, acc.password, acc.mnemonic.join(' ')))




// Tezos.contract

  //*********************************Get Balance**************************************8 */

  app.get('/getBalance', (req,res) => {
    const address =req.body.address
    const balance =req.body.balance
    
    tezos.tz
    .getBalance(privateKey)
    .then((balance) => res.send(`Public key balance is: ${balance.toNumber() / 1000000} ꜩ`))
    .catch((error) => res.send(JSON.stringify(error)));

    
})



    //////////////////////////////////////////////////////////////////////////////////////////////////////
    ////                           ALL POST FUNCTIONS FOR THE SMART CONTRACT                          ////   
    //////////////////////////////////////////////////////////////////////////////////////////////////////




//*********************************Add Assurer***************************************/
app.post('/addTontine', (req,res) => {
  tezos.contract
    .at(contractKey)
    .then((contract) => {
      const balance =req.body.balance
      const descriptif =req.body.descriptif
      const goal =req.body.goal
      const id =req.body.id
      const montantACotiser =req.body.montantACotiser
      const nom =req.body.nom
      const nombreParticipants =req.body.nombreParticipants

      console.log("Adding a Tontin with credentials " + balance, descriptif, goal, id, montantACotiser, nom, nombreParticipants);
      return contract.methods.addTontine(balance, descriptif, goal, id, montantACotiser, nom, nombreParticipants).send();
    })
    .then((op) => {
      console.log(`Awaiting for ${op.hash} to be confirmed...`);
      return res.send(op.hash);
    })
  
.catch((error) => {
          // console.log(`Error: ${JSON.stringify(error, null, 2)}`))
          console.log(`Error: verify your infos`);
          return res.status(400);
          })      .finally(()=>{
      res.end();
    })
  
  })



  
//*********************************Add Participant***************************************/
app.post('/addParticipants', (req,res) => {
  console.log("hey")
  tezos.contract
    .at(contractKey)
    .then((contract) => {
      const rang = req.body.rang
      const id = req.body.id
      const publicKey = req.body.publicKey

      console.log("Adding a Participant with credentials ");
      return contract.methods.addParticipants(rang, id, publicKey).send();
    })
    .then((op) => {
      console.log(`Awaiting for ${op.hash} to be confirmed...`);
      return res.send(op.hash);
    })
  
.catch((error) => {
          // console.log(`Error: ${JSON.stringify(error, null, 2)}`))
          console.log(`Error: verify your infos`);
          return res.status(400);
          })      .finally(()=>{
      res.end();
    })
  
  })


  //*********************************Add Cotisation***************************************/
app.post('/addCotisations', (req,res) => {
  console.log("hey")
  tezos.contract
    .at(contractKey)
    .then((contract) => {
      console.log("1")
      const amount = req.body.amount
      const date = new Date();
      const id = req.body.id
      const publicKey = req.body.publicKey
      const round = req.body.round

      var timestamp = date.getTime();

      console.log("Adding a cotisation with credentials ");
      console.log("Amount: "+ amount+" timestamp: "+ timestamp+ " id: "+id+" publicKey: "+publicKey+ " round: "+ round);
      return contract.methods.addCotisations(amount, timestamp.toString(), id, publicKey, round).send();
    })
    .then((op) => {
      console.log(`Awaiting for ${op.hash} to be confirmed...`);
      return res.send(op.hash);
    })
  
.catch((error) => {
          console.log(`Error: verify your infos`);
          return res.status(400);
          })      .finally(()=>{
      res.end();
    })
  
  })


    //*********************************Add Cotisation***************************************/
app.post('/addCotisations', (req,res) => {
  console.log("hey")
  tezos.contract
    .at(contractKey)
    .then((contract) => {
      console.log("1")
      const amount = req.body.amount
      const date = new Date();
      const id = req.body.id
      const publicKey = req.body.publicKey
      const round = req.body.round

      var timestamp = date.getTime();

      console.log("Adding a cotisation with credentials ");
      console.log("Amount: "+ amount+" timestamp: "+ timestamp+ " id: "+id+" publicKey: "+publicKey+ " round: "+ round);
      return contract.methods.addCotisations(amount, timestamp.toString(), id, publicKey, round).send();
    })
    .then((op) => {
      console.log(`Awaiting for ${op.hash} to be confirmed...`);
      return res.send(op.hash);
    })
  
.catch((error) => {
          console.log(`Error: verify your infos`);
          return res.status(400);
          })      .finally(()=>{
      res.end();
    })
  
  })



      //*********************************Demand withdraw***************************************/
app.post('/DemandeRetrait', (req,res) => {
  console.log("hey")
  tezos.contract
    .at(contractKey)
    .then((contract) => {
      console.log("1")
      const id = req.body.id
      const publicKey = req.body.publicKey


      console.log("Adding a cotisation with credentials ");
      console.log(" id: "+id+" publicKey: "+publicKey);
      return contract.methods.DemandeRetrait(id, publicKey).send();
    })
    .then((op) => {
      console.log(`Awaiting for ${op.hash} to be confirmed...`);
      return res.send(op.hash);
    })
  
.catch((error) => {
          console.log(`Error: verify your infos`);
          return res.status(400);
          })     
          .finally(()=>{
      res.end();
    })
  
  })




//Transfer Tez to participants after withdraw demand
app.post('/transfer', (req,res) => {
  const amount = req.body.amount;
  const address = req.body.address;

console.log(`Transfering ${amount} ꜩ to ${address}...`);
tezos.contract
  .transfer({ to: address, amount: amount })
  .then((op) => {
    console.log(`Waiting for ${op.hash} to be confirmed...`);
    // return op.confirmation(1).then(() => op.hash);
    return res.send(op.hash);
  })
  .then((hash) => console.log(`Operation injected: https://ithaca.tzstats.com/${hash}`))
  .catch((error) => console.log(`Error: ${error} ${JSON.stringify(error, null, 2)}`+ error));

}
)



    //////////////////////////////////////////////////////////////////////////////////////////////////////
    ////                           ALL GET FUNCTIONS FOR THE SMART CONTRACT                          ////   
    //////////////////////////////////////////////////////////////////////////////////////////////////////






const port = process.env.port || 3000;

app.listen(port);

console.log('Smart Contract REST API server started on: ' + port);
module.exports.server = sls(app)
