
import smartpy as sp
class KovamiSmartContract(sp.Contract):
    def __init__(self):
        self.init(Assures = sp.big_map(), conseillerWallets = sp.big_map(), KovamiWallet=sp.map())

    # Defines the addAssures entry point.
    @sp.entry_point
    def addAssure(self, params):
        sp.verify(params.email !="", "Enter your email address")
        sp.if self.data.Assures.contains(params.email):
            sp.failwith("The email already exist")
        sp.else:    
            # Verifies if mandatory fields have values. 
            sp.verify(params.email != "")
            # Declare the parameter types.
            sp.set_type(params.email, sp.TString)

            # Defines an assureur record, so we can add to a Map.
            Assure = sp.record(email=params.email, Souscription = sp.list([]))
            
            # Adds the new Assures record to a Map (that will reside in the contract's storage).
            self.data.Assures[params.email] = Assure   

    @sp.entry_point
    def getAssures(self):
        self.data.Assures

    @sp.entry_point
    def addSouscription(self, params):
        
        # Verifies if mandatory fields have values. 
        sp.verify(params.email != "")
        # Declare the parameter types.
        sp.set_type(params.emailSouscripteur, sp.TString)
        sp.set_type(params.email, sp.TString)
        sp.set_type(params.amount, sp.TInt)
        sp.set_type(params.dateEmission, sp.TString)
        sp.set_type(params.dateEcheance, sp.TString)
        sp.set_type(params.categorieDuvehicule, sp.TString)
        sp.set_type(params.puissance, sp.TInt)
        sp.set_type(params.zone, sp.TString)
        sp.set_type(params.immatriculation, sp.TString)
        sp.set_type(params.numeroAttestation, sp.TString)
        sp.set_type(params.numeroCarteRose, sp.TString)
        sp.set_type(params.fc, sp.TInt)
        sp.set_type(params.dta, sp.TInt)
        sp.set_type(params.acc, sp.TInt)
        sp.set_type(params.pna, sp.TInt)
        sp.set_type(params.pttc, sp.TInt)
        sp.set_type(params.mode, sp.TString)

        sp.verify(params.email !="", "Enter your email address")
        sp.if self.data.Assures.contains(params.email):
            Souscripteur = sp.record(email= params.emailSouscripteur, amount = params.amount , mode=params.mode, dateUpdate=sp.timestamp_from_utc_now(),
            dateEmission=params.dateEmission, dateEcheance=params.dateEcheance, categorieDuvehicule=params.categorieDuvehicule,
            puissance=params.puissance, zone=params.zone, immatriculation=params.immatriculation, numeroAttestation=params.numeroAttestation,
            numeroCarteRose=params.numeroCarteRose, fc=params.fc, dta=params.dta, acc=params.acc, pna=params.pna, pttc=params.pttc
            )
            self.data.Assures[params.email].Souscription.push(Souscripteur)
          
        sp.else:
            Assure = sp.record(email=params.email, Souscription = sp.list())
            self.data.Assures[params.email] = Assure

            Souscripteur = sp.record(email= params.emailSouscripteur, amount = params.amount , mode=params.mode, dateUpdate=sp.timestamp_from_utc_now(),
            dateEmission=params.dateEmission, dateEcheance=params.dateEcheance, categorieDuvehicule=params.categorieDuvehicule,
            puissance=params.puissance, zone=params.zone, immatriculation=params.immatriculation, numeroAttestation=params.numeroAttestation,
            numeroCarteRose=params.numeroCarteRose, fc=params.fc, dta=params.dta, acc=params.acc, pna=params.pna, pttc=params.pttc
            )
            self.data.Assures[params.email].Souscription.push(Souscripteur)
          

    @sp.entry_point
    def kovamiWallet(self, params):
        sp.verify(params.ophash !="", "Enter ophash")
        sp.if self.data.KovamiWallet.contains(params.senderAddress):
            sp.failwith("The kovami Address already exist")
        sp.else: 
            # sp.verify(params.kovamiAddress != "")
            sp.set_type(params.senderAddress, sp.TString)
            sp.set_type(params.ophash, sp.TString)
            sp.set_type(params.reason, sp.TString)
            userWallet = sp.record(senderAddress=params.senderAddress , ophash=params.ophash, reason=params.reason )
            self.data.KovamiWallet[params.ophash] = userWallet   

    @sp.entry_point
    def conseillerWallet(self, params): 
        sp.verify(params.ophash !="", "Enter ophash")
        sp.if self.data.conseillerWallets.contains(params.ophash):
            sp.failwith("The conseiller Address already exist")
        sp.else:
            sp.set_type(params.walletAddress, sp.TString)
            sp.set_type(params.ophash, sp.TString)
            sp.set_type(params.reason, sp.TString)
            Wallet = sp.record(walletAddress=params.walletAddress, ophash=params.ophash, reason=params.reason)
            self.data.conseillerWallets[params.ophash] = Wallet   

    # @sp.entry_point
    # def paiementSouscription(self, params):
    #     sp.verify(params.walletAddress != "")
    #     sp.set_type(params.walletAddress, sp.TString)
    #     sp.set_type(params.Amount, sp.TInt)
    #     sp.set_type(params.reason, sp.TString)
    #     sp.set_type(params.sender, sp.TString)

    #     balance=self.data.KovamiWallet[params.walletAddress].walletBalance
    #     newbalance = balance + params.Amount
    #     self.data.KovamiWallet[params.walletAddress].walletBalance = newbalance
        
    #     paiementSouscription = sp.record(amountSent=params.Amount, dateUpdate=sp.timestamp_from_utc_now(), reason=params.reason, sender=params.sender)
    #     self.data.KovamiWallet[params.walletAddress].paiementSouscription.push(paiementSouscription)
 
    


    @sp.add_test(name = "KovamiSmartContract")
    def test():
        # Instantiate a contract inherited from the Customer Class.
        myCustomersContract = KovamiSmartContract()
        
        # Defines a test scenario.
        scenario = sp.test_scenario()
        scenario.h2("Let's have a look at Kovami Smart contract Testing")


        # Adds the contract to the test scenario.
        scenario += myCustomersContract

        scenario.h2("Ajout Assure")
        
        #Add Assureur
        scenario += myCustomersContract.addAssure(email="jane@gmail.com").run(valid=True)
        scenario += myCustomersContract.addAssure(email="kelly@gmail.com").run(valid=True)
        scenario.h2("Add already existant Assurer error test")
        scenario += myCustomersContract.addAssure(email="kelly@gmail.com").run(valid=False)

        
        #Create souscription
        scenario.h2("Let's Souscribe to an assurance")
        scenario += myCustomersContract.addSouscription(
        email= "jane@gmail.com", amount = 250000 , mode="Tez", dateUpdate=sp.timestamp_from_utc_now(),
        dateEmission="30/04/2022", dateEcheance="30/07/2022", categorieDuvehicule="Rav4",
        puissance=12, zone="Douala", immatriculation="HUTG7IB", numeroAttestation="NO246",
        numeroCarteRose="CR4356", fc=500, dta=45000, acc=1000, pna=150000, pttc=200000, emailSouscripteur="jane@gmail.com"
        )

        scenario += myCustomersContract.addSouscription(
        email= "jane@gmail.com", amount = 150000 , mode="Tez", dateUpdate=sp.timestamp_from_utc_now(),
        dateEmission="01/04/2022", dateEcheance="01/05/2022", categorieDuvehicule="BMW",
        puissance=60, zone="Yaounde", immatriculation="JI37F9", numeroAttestation="NO198",
        numeroCarteRose="CR4356", fc=1000, dta=35000, acc=1000, pna=80000, pttc=140000, emailSouscripteur="jane@gmail.com"
        )

        scenario += myCustomersContract.addSouscription(
        email= "kevin@gmail.com", amount = 150000 , mode="Tez", dateUpdate=sp.timestamp_from_utc_now(),
        dateEmission="01/04/2022", dateEcheance="01/05/2022", categorieDuvehicule="BMW",
        puissance=60, zone="Yaounde", immatriculation="JI37F9", numeroAttestation="NO198",
        numeroCarteRose="CR4356", fc=1000, dta=35000, acc=1000, pna=80000, pttc=140000, emailSouscripteur="rakeal@gmail.com"
        )

        #List all assureur
        scenario.h2("List Assures")
        scenario += myCustomersContract.getAssures()

        scenario.h2("Add conseillerWallet")
        scenario += myCustomersContract.conseillerWallet( walletAddress="tz1M6x9Y4cAGWpmkJjrSopTLfTLAUVmCZoLv",ophash="opjhgdyuegvhbhefsdwefrer", reason="Commission")

        scenario.h2("Add kovamiWallet")
        scenario += myCustomersContract.kovamiWallet(senderAddress="tz1d72He7paiNsd4BQpZZqQjwmvkEgWVtZ57", ophash="opjghyut76hbhefsdwefrer", reason="Paiement Souscription")


        
