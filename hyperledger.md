---
layout: post
title: Hyperledger Fabric Energy
date: 07/07/2021
tags: blockchain - cybersecurity
githublink: https://github.com/jouleffect/hyperledger-fabric-energy
githubzip_url: https://github.com/jouleffect/hyperledger-fabric-energy/archive/refs/heads/main.zip
---

[![made-with-javascript](https://img.shields.io/badge/Made%20with-JavaScript-1f425f.svg)](https://www.javascript.com)
[![made-with-bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](https://www.gnu.org/software/bash/)

This project has been realized for the Cybersecurity course, hold at the University of Palermo.<br>
The topic is to simulate, on small scale, the control of electricity balancing, with a web interface, thanks to the blockchain technology inside the system.<br>
The context considered is the energy trading one, wich consists in the exchange of electricity produced by private individuals (prosumers).<br>
Nowadays, using blockchain technology permits the communication between producer and consumer in full safety.<br>
In this simulation the energy supplier has control of the threshold of consumer energy. Once the threshold is exceeded, the producer could send a signal to the device of the consumer, in order to turn the system off, until the the power returns back below the threshold.<br>

## HYPERLEDGER FABRIC

Hyperledger Fabric is an opensource DLT platform (distributed ledger technology), made by Linux-Foundation, in order to develop software applications inside a safe network, because it is based on Blockchain technology. <br>
In this topic, I use a distributed and permissioned network, which is a network of nodes, where each node has the same features and the same persmissions of the others. Therefore, this network is a private and secure network and it ensures privacy, integrity and confidentiality, where only people who authenticate can take part of. This network has a modular architecture, which could be adapted to all demands.<br>

<p align="center">
  <img src="https://user-images.githubusercontent.com/53179989/155743574-6ec5c5aa-16fd-4f2e-850c-818daaf16b0a.png" style="width:500px;">
</p>

The components of Hyperledger Fabric are the following:

- Service Order
- MSP (Membership Service Provider)
- Smart Contracts
- Ledger
- API

## BLOCKCHAIN NETWORK

When a new network is set up, a new channel is configurated according to the rules established between the organizations. This channel is situated inside the Configuration Block. Afterwards, organizations that join the channel should be authenticated by a CA (Certificate Authority). Thus, they will own the permission to join their peers in the service order. Every peer preserves a copy of the ledger of the channel and it is updated with a new Asset block.<br>

* * * 

### How to run the network (configuring the CA):

- Starting the network

<pre><code>
net-start.sh
</code></pre>

Inside the bash script there are two important commands that run the blockchain network, by creating the Docker containers of the organizations and of the service order.<br>

- Generating CA, channels and peers links to the channel

<pre><code>
./network.sh up createChannel -ca
</code></pre>

## SMART-CONTRACT

Once the network is on, we must create a smart-contract (chaincode), defined by the rules established before, in order to be able to make the transitions, by running the commands on the organization peer. In the peer is after signed the output of the transition and it is distributed to the other peers, that allow and confirm it on the ledger, if it is accepted.<br>
In the smart contract we must define the policy of the organizations in the channel. In this topic, the chain code are:

- energycontract.js: the general policy
- energy.js: the policy of the state of Energy (disbursed, interrupted)

The main assets are:

```javascript
async CreateAsset(ctx, id, color, size, owner, power) {
  const asset = {
    ID: id,
    Owner: owner,
    power: power,
  };
  await ctx.stub.putState(id, Buffer.from(JSON.stringify(asset)));
  return JSON.stringify(asset);
}

async Eroga(ctx, id, data, power) {
  let energy = Energy.createInstance(id, data, parseInt(power));
  energy.setErogata();
  if (power > 3000) {
    energy.setInterrotta();
  }
  return energy;
}
```
In this code, if the request power is lower than 3000 W, the state is Active, otherwise the energy is interrupted.<br>
The following command, that uses the lifecycle of the chaincode, distributes the contract in the channel:

<pre><code>
./network.sh deployCC -ccn energy -ccp ${DIR}/organization/produttore/contract -ccl javascript
</code></pre>

The javascript application which interact with the chaincode (app.js), is situated in the consumer and in the producer directory.
Looking at the producer app.js, the most important chaincode is:

```javascript
await contract.evaluateTransaction('eroga', '00001', '07/07/2021', '350');
```

The value of the power in the transaction (350) il lower than 3000, so the energy is still in the disbursed state.

```javascript
*** Result: {
"class": "org.energynet.Energy",
"key": "600:00001",
"currentState": 1,
"energyNumber": "00001",
"data": "07/07/2021",
"potenza": 600
}

*** Result: {
"class": "org.energynet.Energy",
"key": "3200:00001",
"currentState": 2,
"energyNumber": "00001",
"data": "07/07/2021",
"potenza": 3200
}
```

<p align="center">
  <img src="https://user-images.githubusercontent.com/53179989/155750591-919ab96d-d856-4b91-8e7a-b416746d9df8.png" style="width:500px;">
</p>

* * *
