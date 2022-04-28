

import smartpy as sp
class TontineContract(sp.Contract):
    def __init__(self):
        self.init(Tontines = sp.big_map())

    # Defines the addTontine entry point.
    @sp.entry_point
    def addTontine(self, params):
        sp.verify(params.id !=0, "Enter your tontine id")
        sp.if self.data.Tontines.contains(params.id):
            sp.failwith("The id already exist")
        sp.else:    
            # Verifies if mandatory fields have values. 
            sp.verify(params.id != 0)
            # Declare the parameter types.
            sp.set_type(params.id, sp.TInt)
            sp.set_type(params.nom, sp.TString)
            sp.set_type(params.goal, sp.TMutez)
            sp.set_type(params.montantACotiser, sp.TMutez)
            sp.set_type(params.descriptif, sp.TString)
            sp.set_type(params.balance, sp.TMutez)
            sp.set_type(params.nombreParticipants, sp.TNat)
            # Defines a Tontine record, so we can add to a Map.
            Tontine = sp.record(id=params.id,nom=params.nom, goal=params.goal, montantACotiser=params.montantACotiser, descriptif=params.descriptif, balance=params.balance, nombreParticipants=params.nombreParticipants, Participants = sp.list([]), Cotisations = sp.map(), demandeRetrait= sp.map())
            
            # Adds the new Tontin record to a Map (that will reside in the contract's storage).
            self.data.Tontines[params.id] = Tontine   

    @sp.entry_point
    def getTontines(self):
        self.data.Tontines

    @sp.entry_point
    def addCotisations(self, params):
        #vérifier qu’il est membre de cette tontine
        sp.verify(params.id !=0, "Enter your tontine id")
        sp.if self.data.Tontines.contains(params.id):
            # Verifies if mandatory fields have values. 
            sp.verify(params.id != 0)
            sp.verify(params.amount != sp.tez(0))
            sp.verify(params.round != 0)
            
            # Declare the parameter types.
            sp.set_type(params.id, sp.TInt)
            sp.set_type(params.publicKey, sp.TAddress)
            sp.set_type(params.amount, sp.TMutez)
            sp.set_type(params.date, sp.TTimestamp)
            sp.set_type(params.round, sp.TInt)

            #verify that the amount is equivalent to the amount to be paid per member
            ActualAmount =self.data.Tontines[params.id].montantACotiser
            sp.verify(ActualAmount == params.amount, "Impossible to contribute an unspecified amount to the Tontine")
           
            dejaContribuer= self.data.Tontines[params.id].balance
                       
            #Update contributed Amount
            NewMontantCotribuer= dejaContribuer + params.amount
            self.data.Tontines[params.id].balance=NewMontantCotribuer

            #Verify if Amount demanded has been attained 
            Solde =self.data.Tontines[params.id].goal
            sp.verify(Solde >= dejaContribuer,"Amount demanded has not been attained")

            Cotisation = sp.record(id= params.id, publicKey = params.publicKey , amount=params.amount, date=params.date, round=params.round)
            self.data.Tontines[params.id].Cotisations[params.publicKey] = Cotisation
        sp.else: 
            sp.failwith("The Tontine id doesn't exist")

    @sp.entry_point
    def addParticipants(self, params):
        sp.verify(params.id !=0, "Enter your tontine id")
        sp.if self.data.Tontines.contains(params.id):
            # Verifies if mandatory fields have values. 
            sp.verify(params.id != 0)
            sp.verify(params.Rang != "")
            # Declare the parameter types.
            sp.set_type(params.id, sp.TInt)
            sp.set_type(params.publicKey, sp.TAddress)
            sp.set_type(params.Rang, sp.TString)

            # Verify if the number of participants specified in Tontine has been attained
            nombreParticipant = self.data.Tontines[params.id].nombreParticipants
            sizeOfParticipant =sp.len(self.data.Tontines[params.id].Participants)
            sp.verify(sizeOfParticipant < nombreParticipant, "Number of participants already attained")

            Participant = sp.record(id= params.id, publicKey = params.publicKey , Rang=params.Rang)
            self.data.Tontines[params.id].Participants.push(Participant)
        sp.else: 
           sp.failwith("The Tontine id doesn't exist")
       
    
    @sp.entry_point
    def DemandeRetrait(self, params):
        #verify if he is a member of this tontine
        sp.verify(params.id !=0, "Enter your tontine id")
        sp.if self.data.Tontines.contains(params.id):
            # Verifies if mandatory fields have values. 
            sp.verify(params.id != 0)
    
            # Declare the parameter types.  
            sp.set_type(params.id, sp.TInt)
            sp.set_type(params.publicKey, sp.TAddress)

                   
            #verify if the goal amount has been attained before permitting withdraw
            balance =self.data.Tontines[params.id].balance
            Solde =self.data.Tontines[params.id].goal
            sp.verify(Solde == balance, "Impossible to withdraw when amount demanded not attained")

            #Set the balance back to 0 after a withdraw demand
            NewBalance= sp.tez(0)
            self.data.Tontines[params.id].balance=NewBalance

            #Verifier si la meme addresse ne demande pas de retrait plus d'une fois
            sp.verify(~self.data.Tontines[params.id].demandeRetrait.contains(params.publicKey),"Impossible de demander le retrait plus d'une fois")

            Reclamer = sp.record(id= params.id, publicKey = params.publicKey)
            self.data.Tontines[params.id].demandeRetrait[params.publicKey] = Reclamer
        sp.else: 
            sp.failwith("The Tontine id doesn't exist")


    @sp.add_test(name = "TontineContract")
    def test():
        # Instantiate a contract inherited from the Tontine Class.
        myContract = TontineContract()
        
        # Defines a test scenario.
        scenario = sp.test_scenario()
        scenario.h2("Let's have a look at Tontine Smart contract Testing")

        # Adds the contract to the test scenario.
        scenario += myContract

        scenario.h2("Add Tontine")
        #Add Tontine
        scenario += myContract.addTontine(id=1, nom="KJTontine", montantACotiser=sp.tez(45), goal=sp.tez(90), descriptif="Tontine entre amis de confiance", balance=sp.tez(0), nombreParticipants=2 ).run(valid=True)
        scenario += myContract.addTontine(id=2, nom="StockContrib", montantACotiser=sp.tez(12), goal=sp.tez(85), descriptif="Tontine  Familiale", balance=sp.tez(0), nombreParticipants=7).run(valid=True)
        scenario.h2("Attempt to add already existant Tontine error test")
        scenario += myContract.addTontine(id=1, nom="Tontine", montantACotiser=sp.tez(12), goal=sp.tez(67), descriptif="Tontine entre amis", balance=sp.tez(0), nombreParticipants=4).run(valid=False)

        scenario.h2("Add Participant")
        #Add Participants
        scenario += myContract.addParticipants(id=1, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), Rang="2").run(valid=True)
        scenario += myContract.addParticipants(id=1, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), Rang="2").run(valid=True)
        scenario.h2("Attempt to add Participant when number of participants already attained error test")
        scenario += myContract.addParticipants(id=1, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), Rang="2").run(valid=False)
        scenario.h2("Attempt to add Participant to unexistant Tontine error test")
        scenario += myContract.addParticipants(id=3, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), Rang="1").run(valid=False)

        #Add Cotisations
        scenario.h2("Add Cotisations")
        scenario += myContract.addCotisations(id=1, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), amount=sp.tez(45), date=sp.timestamp(12445598),round=2).run(valid=True)
        scenario += myContract.addCotisations(id=1, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), amount=sp.tez(45), date=sp.timestamp(12445598),round=2).run(valid=True)
        scenario.h2("Verify if the amount demanded for the tontine has been attained")
        scenario += myContract.addCotisations(id=1, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), amount=sp.tez(42), date=sp.timestamp(12445598),round=2).run(valid=False)
        scenario.h2("Attempt to add Cotisations to unexistant Tontine error test")
        scenario += myContract.addCotisations(id=3, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), amount=sp.tez(20), date=sp.timestamp(12445598) , round=3).run(valid=False)
        scenario.h2("Attempt to make Cotisations using amount not specified in Tontine error test")
        scenario += myContract.addCotisations(id=2, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv"), amount=sp.tez(34), date=sp.timestamp(12445598),round=1).run(valid= False)

        #Declare withdraw
        scenario.h2("Declare withdraw")
        scenario += myContract.DemandeRetrait(id=1, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv")).run(valid=True)
        scenario.h2("Attempt to demand a withdraw more than once error Test")
        scenario += myContract.DemandeRetrait(id=1, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv")).run(valid=False)
        scenario.h2("Attempt to demand a withdraw when amount demanded not attained error Test")
        scenario += myContract.DemandeRetrait(id=2, publicKey=sp.address("tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv")).run(valid=False)


        #List all Tontine
        scenario.h2("List All Tontine")
        scenario += myContract.getTontines()



   

        
