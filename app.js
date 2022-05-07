const express = require('express')
const sls = require('serverless-http') 
const { InMemorySigner } = require('@taquito/signer');
const { TezBridgeSigner } = '@taquito/tezbridge-signer';
const {TezosToolkit, MichelCodecPacker } = require('@taquito/taquito');

var  swaggerJSDoc = require("swagger-jsdoc");
var  swaggerUi = require("swagger-ui-express");
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



const swaggerDefinition = {
  openapi: '3.0.0',
  info: {
    title: 'Express API for Tontine smart contract',
    version: '1.0.0',
    description:
      'This is a REST API application made with Express. It retrieves data from Tontine smart contract.',
    license: {
      name: 'Licensed Under MIT',
      url: 'https://spdx.org/licenses/MIT.html',
    },
    contact: {
      name: 'JSONPlaceholder',
      url: 'https://jsonplaceholder.typicode.com',
    },
  },
  servers: [
    {
      url: 'http://localhost:3000',
      description: 'Development server',
    },
  ],
};

const options = {
  swaggerDefinition,
  // Paths to files containing OpenAPI definitions
  apis: ['./app.js'],
};

const swaggerSpec = swaggerJSDoc(options);


app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));




  //*********************************Get Balance**************************************8 */

  /**
 * @swagger
 * /Balance:
 *   get:
 *     summary: Tezos account balance
 *     description: Retrieve tezos account balance
 *     responses:
 *       200:
 *         description: Tezos Balance.
 *         content:
 *           application/json:
 *             schema:
 *               type: string
*/
app.get('/Balance', (req,res) => {
  tezos.tz
  .getBalance(privateKey)
  .then((balance) =>{
    console.log(`Public key balance is: ${balance.toNumber() / 1000000} ꜩ`);
    return res.send((balance.toNumber() / 1000000).toString());
  })
  .catch((error) => {
    // console.log(`Error: ${JSON.stringify(error, null, 2)}`))
    console.log(`Error: verify your infos`);
    return res.status(400);
    }) 
  .finally(()=>{
    res.end();
  })

})




    //////////////////////////////////////////////////////////////////////////////////////////////////////
    ////                           ALL POST FUNCTIONS FOR THE SMART CONTRACT                          ////   
    //////////////////////////////////////////////////////////////////////////////////////////////////////




//*********************************Add Assurer***************************************/

  /**
 * @swagger
 * /addTontine:
 *   post:
 *     summary: Create a Tontine
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               balance:
 *                  type: integer
 *                  description: Set this to 0 as default (Tontine account balance)
 *                  example: 0
 *               descriptif:
 *                  type: string
 *                  description: Tontine account balance
 *                  example: Finance Training Tontine
 *               goal:
 *                  type: integer
 *                  description: Tontine Goal amount 
 *                  example: 24
 *               id:
 *                  type: integer
 *                  description: Tontine key
 *                  example: 1
 *               montantACotiser:
 *                  type: integer
 *                  description: Amount each member has to contribute to the account
 *                  example: 8
 *               nom:
 *                  type: string
 *                  description: Tontine Goal amount 
 *                  example: Tech friends Tontine 
 *               nombreParticipants:
 *                  type: integer
 *                  description: Number of participants
 *                  example: 3
*/
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


/**
 * @swagger
 * /addParticipants:
 *   post:
 *     summary: Add a participant to a Tontine
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               rang:
 *                  type: string
 *                  description: Participant rang
 *                  example: R1
 *               id:
 *                  type: integer
 *                  description: Tontine key
 *                  example: 1
 *               publicKey:
 *                  type: string
 *                  description: public key of participants
 *                  example: tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZhh4
*/
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

 /**
 * @swagger
 * /addCotisations:
 *   post:
 *     summary: Add a contribution to a Tontine
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               amount:
 *                  type: integer
 *                  description: Amount contributed to the Tontine 
 *                  example: 8
 *               id:
 *                  type: integer
 *                  description: Tontine key
 *                  example: 1
 *               publicKey:
 *                  type: string
 *                  description: public key used to contribute 
 *                  example: tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZhh4
 *               round:
 *                  type: integer
 *                  description: Tontine rounds
 *                  example: 1
*/ 
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
 /**
 * @swagger
 * /DemandeRetrait:
 *   post:
 *     summary: demand a withdraw from a Tontine
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               id:
 *                  type: integer
 *                  description: Tontine key
 *                  example: 1
 *               publicKey:
 *                  type: string
 *                  description: public key used to contribute 
 *                  example: tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZhh4
*/ 
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

 /**
 * @swagger
 * /transfer:
 *   post:
 *     summary: Tranfer Tez to a participant after withdraw demand
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               amount:
 *                  type: integer
 *                  description: Amount to be transferred
 *                  example: 24
 *               address:
 *                  type: string
 *                  description: Participant's publickey 
 *                  example: tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZhh4
*/ 
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




const port = process.env.port || 3000;

app.listen(port);

console.log('Smart Contract REST API server started on: ' + port);
module.exports.server = sls(app)
