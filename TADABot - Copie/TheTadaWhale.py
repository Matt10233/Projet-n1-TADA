import requests
from datetime import datetime
import json
import time
import tweepy
import matplotlib.pyplot as plt
from requests.exceptions import ConnectTimeout, ReadTimeout


print("launch")
CheckHeure = None

def CalculBenford():
    numbers = []

    with open("MonthTransactions.json", 'r') as file:
        for line in file:
            data = json.loads(line)
            montant = data.get("montant")
            numbers.append(montant)

    print("Montants récupérés depuis le fichier JSON :", numbers)


    #recupere le premier chiffre significatif dune liste de nombres
    
    ChiffresSignifi = []

    for Num in numbers:
        NumStr = str(Num)  
        ChiffreRequis = None
        SupAZero = False
        for Char in NumStr:
            if Char.isdigit() and Char != '0':
                ChiffreRequis = int(Char)
                break  
            elif Char == '.' or Char == ',' :
                SupAZero = True
        ChiffresSignifi.append(ChiffreRequis)

    print("Premiers chiffres significatifs des nombres :", ChiffresSignifi)


    #calcul la frequence dapparition de chaque chiffre 

    FrequencyCount = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    #fréquence apparition des chiffres de 1 a 9
    for digit in ChiffresSignifi:
        if digit is not None:
            FrequencyCount[digit] += 1

    for digit, frequency in FrequencyCount.items():
        print(f"Chiffre {digit} : Fréquence {frequency}")


    #converti la frequence dapparition de chaque chiffres significatif en pourcentage

    #calcul le total des fréquences
    TotalFrequency = sum(FrequencyCount.values())

    pourcentages = []
    frequences = []

    for digit, frequency in FrequencyCount.items():
        if TotalFrequency != 0:
            percentage = (frequency / TotalFrequency) * 100
        else:
            percentage = 0
        pourcentages.append(percentage)
        frequences.append(frequency)
        print(f"Chiffre {digit} : Fréquence {frequency} ({percentage:.2f}%)")


    #genere le tableau

    chiffres = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    #trie par ordre decroissant
    SortedIndices = sorted(range(len(frequences)), key=lambda k: frequences[k], reverse=True)
    chiffres = [chiffres[i] for i in SortedIndices]
    pourcentages = [pourcentages[i] for i in SortedIndices]

    plt.figure(figsize=(10, 6))
    plt.bar(chiffres, pourcentages, color='purple')
    #parametres
    plt.title(f'Loi de Benford TADA\n(Du {DateFormateeDebut} au {DateFormat})')
    plt.xlabel('Chiffres')
    plt.ylabel('Pourcentage')
    plt.xticks(chiffres)
    #print et save le tableau
    plt.grid(axis='y')
    plt.savefig('ImageBenford1.jpg')
    #plt.show()

def Verif10DernieresTransac():
    NbTransacARecup = 10
    ListeMontantsDernieres = []
    Doublon = False

    with open("MonthTransactions.json", "r") as JsonFile:
        lines = JsonFile.readlines()

        if lines:

            if len(lines) <= NbTransacARecup:
                transactions = [json.loads(line) for line in lines]
            else:
                transactions = [json.loads(line) for line in lines[-NbTransacARecup:]]

            for transaction in transactions:
                montant = transaction.get("montantTADA")
                if montant is not None:
                    ListeMontantsDernieres.append(montant)

            print(f"Montants des {NbTransacARecup} dernières transactions : {ListeMontantsDernieres}")

            if Nombre_SAV in ListeMontantsDernieres:
                print("montant deja present dans les 10 dernieres transactions, on passe a la suivante")
                Doublon = True
                return Doublon

        else :
            print("fichier de transactions vide, pas de verif de doublon")

def PostBenfordTweetImages():
    #clés API de twitter
    consumer_key = "xxxxx"
    consumer_secret = "xxxxx"
    access_token = "xxxxx-xxxxx"
    access_secret = "xxxxx"

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_secret)
    api = tweepy.API(auth)
    
    client = tweepy.Client(
        consumer_key = consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_secret)
    
    #upload l'image 1
    MediaId1 = api.media_upload(filename="ImageBenford1.jpg").media_id_string
    print(MediaId1)

    #upload l'image 2
    MediaId2 = api.media_upload(filename="ImageBenford2.jpg").media_id_string
    print(MediaId2)

    client.create_tweet(text=message, media_ids=[MediaId1, MediaId2])
    print("tweeted!")
            
def PostTheTweetWithImages():
    #clés API de twitter
    consumer_key = "xxxxx"
    consumer_secret = "xxxxx"
    access_token = "xxxxx-xxxxx"
    access_secret = "xxxxx"

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_secret)
    api = tweepy.API(auth)
    
    client = tweepy.Client(
        consumer_key = consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_secret)
    
    #upload l'image 1
    MediaID1 = api.media_upload(filename="image1.jpg").media_id_string
    print(MediaID1)

    #upload l'image 2
    MediaID2 = api.media_upload(filename="image2.jpg").media_id_string
    print(MediaID2)

    client.create_tweet(text=message, media_ids=[MediaID1, MediaID2])
    print("tweeted!")

def PostTheTweet():
    #clés API de twitter
    consumer_key = "xxxxx"
    consumer_secret = "xxxxx"
    access_token = "xxxxx-xxxxx"
    access_secret = "xxxxx"

    client = tweepy.Client(
        consumer_key = consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_secret)

    #post le tweet
    response = client.create_tweet(
        text=message)
    
    print("tweeted!")

def EnregistreRecapDaily():
    #dictionnaire pour fichiers .json
    DictioTransac = {
        "TotalVolumeAchat": TotalAchat,
        "TotalVolumeVente": TotalVente,
        "TotalVolume": TotalMontant,
        "TotalTransactionAchat": MontantAchatArrondi,
        "TotalTransactionVente": MontantVenteArrondi,
        "TotalTransaction": TotalTransactions,
        "Date": DateFormat
    }
    
    #enregistre la transaction dans le fichier json journalier
    with open("AllRecaps.json", "a") as JsonFile:
        json.dump(DictioTransac, JsonFile)
        JsonFile.write('\n')
        
    with open("HistoriqueAllRecaps.json", "a") as JsonFile:
        json.dump(DictioTransac, JsonFile)
        JsonFile.write('\n')

    print("Transactions enregistrées avec succes dans AllRecaps.json")
    
def EnregistreTransac():
    #dictionnaire pour fichiers .json
    DictioTransac = {
        "type": statut,
        "montant": PriceValue,
        "montantTADA": Nombre_SAV,
        "prix": price,
        "heure": TimestampLisible,
        "date": DateFormat,
        "lien": Link
    }
    
    #enregistre la transaction dans le fichier json journalier
    with open("transactions.json", "a") as JsonFile:
        json.dump(DictioTransac, JsonFile)
        JsonFile.write('\n')
        
    #enregistre la transaction dans le fichier json mensuel
    with open("MonthTransactions.json", "a") as JsonFile:
        json.dump(DictioTransac, JsonFile)
        JsonFile.write('\n')
        
    #enregistre la transaction dans le fichier json Historique, jamais reinitialiser
    with open("HistoriqueMonthTransactions.json", "a") as JsonFile:
        json.dump(DictioTransac, JsonFile)
        JsonFile.write('\n')

    print("Transactions enregistrées avec succes dans transactions.json et MonthTransactions.json")

def GetPriceTADA():
    global value
    #URL de l'api multiversx du prix du tada
    urltada = f"https://api.multiversx.com/mex/tokens/TADA-5c032c" #(identifiant du TADA : TADA-5c032c)

    urlPrix = urltada

    try:
        #requete a l'api
        response = requests.get(urlPrix, timeout=10)
    except Exception:
        try:
            print("erreur avec l'api")
            time.sleep(5)
            response = requests.get(urlPrix, timeout=10)
        except Exception:
            print(" encore une erreur avec l'api")
            time.sleep(10)
            response = requests.get(urlPrix, timeout=10)

    #code 200 = on a reussi
    if response.status_code == 200:
        #extraire les données
        data = response.json()

        #extraire le prix du TADA
        price = data["price"]
        symbole = data["symbol"]

        # Afficher le prix
        print(f"Le prix actuel de la crypto {symbole} est : {price}") 
        return price
    
    else:
        time.sleep(5)
        print(f"La requete a échoué avec le code : {response.status_code}")
        print("on reessaye")
        response = requests.get(urlPrix, timeout=10)
        if response.status_code == 200:
            data = response.json()
            price = data["price"]
            symbole = data["symbol"]
            print(f"Le prix actuel de la crypto {symbole} est : {price}")
            return price
        else:
            print(f"La requete a de nouveau échoué avec le code : {response.status_code}")

def GetPrice():
    global value
    # URL de l'API des prix
    urltada = f"https://api.multiversx.com/mex/tokens/TADA-5c032c"
    urlwegld = f"https://api.multiversx.com/mex/tokens/WEGLD-bd4d79"
    usdcurl = f"https://api.multiversx.com/mex/tokens/USDC-c76f1f"
    
    if ReceiverTicker == "WEGLD" :
        urlPrix = urlwegld

    if ReceiverTicker == "USDC" :
        urlPrix = usdcurl

    if ReceiverTicker == "TADA" :
        urlPrix = urltada

    try:
        response = requests.get(urlPrix, timeout=10)
    except Exception:
        try:
            print("erreur avec l'api")
            time.sleep(5)
            response = requests.get(urlPrix, timeout=10)
        except Exception:
            print(" encore une erreur avec l'api")
            time.sleep(10)
            response = requests.get(urlPrix, timeout=10)

    if response.status_code == 200:
        data = response.json()

        price = data["price"]
        symbole = data["symbol"]

        print(f"Le prix actuel de la crypto {ReceiverTicker} ou {symbole} est : {price}")
        
        return price
        
    else:
        time.sleep(5)
        print("recuperation du prix de tada impossible 'api error'")
        print(f"La requete a échoué avec le code : {response.status_code}")
        print("on reessaye")
        response = requests.get(urlPrix, timeout=10)
        if response.status_code == 200:
            data = response.json()
            price = data["price"]
            symbole = data["symbol"]
            print(f"Le prix actuel de la crypto {ReceiverTicker} ou {symbole} est : {price}")
            return price
        else:
            print(f"La requete a échoué avec le code : {response.status_code}")

def SendDiscordErreurs(): #(Partie du code qui interagit avec discord)
    #URL du webhook du salon ou les messages(transactions) de la whalealert seront affichés
    UrlWebhook = "https://discord.com/api/webhooks/XXXXX"
    #payload a envoyer
    payload = {
        "content": message
    }
    #converti le payload en json
    data = json.dumps(payload)

    #envoie de la requête au webhook
    response = requests.post(UrlWebhook, data=data, headers={"Content-Type": "application/json"}, timeout=10)

    #204 = reussi
    if response.status_code == 204:
        print("Message envoyé avec succès sur Discord.")
    else:
        print(f"Echec de l'envoi du message sur discord, Code : {response.status_code}")
             
def SendDiscord(): #(Partie du code qui interagit avec discord)
    #URL du webhook du salon ou les messages(transactions) de la whalealert seront affichés
    UrlWebhook = "https://discord.com/api/webhooks/XXXXX"
    #payload a envoyer
    payload = {
        "content": message
    }
    #converti le payload en json
    data = json.dumps(payload)

    #envoie de la requête au webhook
    response = requests.post(UrlWebhook, data=data, headers={"Content-Type": "application/json"}, timeout=10)

    #204 = reussi
    if response.status_code == 204:
        print("Message envoyé avec succès sur Discord.")
    else:
        print(f"Echec de l'envoi du message sur discord, Code : {response.status_code}")

last_fee = None 
last_fee2 = None
last_fee3 = None
LinkSource = "https://explorer.multiversx.com/transactions/"

while True:
    try:
        time.sleep(0.5)

        #URL de l'api des transactions
        url = "https://api.elrond.com/tokens/TADA-5c032c/transfers?status=success"

        try:
            response = requests.get(url)
        except Exception:
            try:
                print("erreur avec l'api")
                time.sleep(5)
                response = requests.get(url)
            except Exception:
                print(" encore une erreur avec l'api")
                time.sleep(10)
                response = requests.get(url)

        if response.status_code == 200:
            transactions = response.json()

            if transactions:
                #inverser l'ordre des transactions pour commencer par les plus récentes
                #transactions.reverse()
                #récupérer uniquement les 10 premières(plus recentes) transactions
                First10Transactions = transactions[:10]

                with open('processed_transactions.txt', 'a') as file:
                    for transaction in reversed(First10Transactions):    
                        transactionID = transaction.get("txHash")  # Identifiant de la transaction
                        #print("new transaction")
                        time.sleep(0.1)

                        with open('processed_transactions.txt', 'r') as CheckFile:
                            if transactionID in CheckFile.read():
                                #passer à la prochaine transaction si elle est deja dans le fichier
                                continue

                            file.write(transactionID + '\n')

                            #récup les informations de la transaction
                            FunctionTransac = transaction["function"]
                            ValeurTransac = transaction["action"]["arguments"]["transfers"][0]["value"]
                            ValeurTransacDecimal = int(ValeurTransac) / (10 ** 18)
                            ValeurTransacLisible = round(ValeurTransacDecimal, 2)
                            TickerDeLaValeur = transaction["action"]["arguments"]["transfers"][0]["ticker"]
                            print("----------------------------")
                            print(f" {FunctionTransac} {ValeurTransacLisible} {TickerDeLaValeur}")

                            #verifie le type de transaction
                            if FunctionTransac == "swapTokensFixedInput" or FunctionTransac == "swapTokensFixedOutput":
                                print(FunctionTransac)
                                statut = "Vente"
                                print(f"Statut de la transaction : {statut}")

                                #pour recuperer le bon hash et cree le lien source qui redirige vers la transaction
                                if "originalTxHash" in transaction:
                                    TxIDForLink = transaction["originalTxHash"]
                                else:
                                    TxIDForLink = transaction.get("txHash")

                                SenderValue = transaction["action"]["arguments"]["transfers"][0]["value"]
                                Nombre_SAV = int(SenderValue) / (10 ** 18)
                                NombreSAV = round(Nombre_SAV, 2)
                                TxID = transaction["action"]["arguments"]["transfers"][0]["value"]   
                                print(f"ID (value) de la transaction : {TxID}")
                                
                                #ici si la valeur de la transaction est la meme que la derniere valeur traité alors on passe car il y a tres souvent des doublons
                                if TxID == last_fee:
                                    continue
                                
                                #deuxieme verification qui check si le montant de cette transaction est presente dans les 10 derniere
                                #si c'est le cas il passe a la suivante. (risque de manquer des transactions non doublon dans de rares cas)
                                Verif10DernieresTransac()
                                Doublon = Verif10DernieresTransac()
                                
                                if Doublon is True :
                                    continue
                                    
                                last_fee = TxID

                                sender = transaction["sender"]
                                SenderCourt = sender[:6] + "..." + sender[-3:]
                                timestamp = transaction["timestamp"]

                                SenderTicker = transaction["action"]["arguments"]["transfers"][0]["ticker"]
                                try:
                                    ReceiverTicker = transaction["action"]["arguments"]["transfers"][1]["ticker"]
                                    ReceiverValue = transaction["action"]["arguments"]["transfers"][1]["value"]
                                    ReceiverDecimals = transaction["action"]["arguments"]["transfers"][1]["decimals"]
                                except Exception:
                                    #passer a la transaction suivante
                                    print("erreur pas de receptionniste pour cette transaction, on passe a la suivante")
                                    continue
                                ReceiverValue = int(ReceiverValue) / (10 ** ReceiverDecimals)
                                ReceiverValue = round(ReceiverValue, 2)
                                receiver = transaction["receiver"]
                                ReceiverCourt = receiver[:6] + "..." + receiver[-3:]
                                if "receiverAssets" in transaction:
                                    ReceiverName = transaction["receiverAssets"]["name"]
                                    print(f"sender name : {ReceiverName}")
                                else:
                                    ReceiverName = ReceiverCourt

                                if "senderAssets" in transaction:
                                    SenderName = transaction["senderAssets"]["name"]
                                    print(f"sender name : {SenderName}")
                                else:
                                    SenderName = SenderCourt

                                if TxIDForLink is not None:
                                    Link = LinkSource + TxIDForLink
                                else:
                                    Erreur = "ERROR"
                                    Link = LinkSource + Erreur

                                #converti le timestamp en heure lisible
                                TimestampLisible = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d at %H:%M:%S')
                                DateActuelle = datetime.now().date()
                                DateFormat = datetime.now().strftime("%Y-%m-%d")

                                print("Informations de la transaction :")
                                print("    Sender :", sender)
                                print("    Timestamp (humain) :", TimestampLisible)
                                print("    Nom de l'actif envoyeur :", SenderName)
                                print("    Ticker de l'actif envoyeur :", SenderTicker)
                                print("    Valeur de l'actif envoyeur (sans décimales) :", NombreSAV)
                                print("    Receiver :", receiver)
                                print("    Ticker de l'actif receiver :", ReceiverTicker)
                                print("    Valeur de l'actif receiver (sans décimales) :", ReceiverValue)

                                TransferSenderAddrs = not sender.startswith("erd1qqqq")
                                TransferReceiverAddrs = not receiver.startswith("erd1qqqq")

                                #si le receiver et le sender ont une adresse commancant par erd1qqqq cela signifie que c'est un transfert
                                if TransferSenderAddrs and TransferReceiverAddrs:
                                    GetPriceTADA()
                                    price = GetPriceTADA()
                                    PriceValue = price * NombreSAV
                                    print(PriceValue)
                                    
                                    PriceArrondi = round(price, 2)
                                    PriceArrondi = f"{PriceArrondi:.2f}"
                                    print(PriceArrondi)

                                    KucoinAddrs = "erd1ty4pvmjtl3mnsjvnsxgcpedd08fsn83f05tu0v5j23wnfce9p86snlkdyy"
                                    
                                    if sender == KucoinAddrs :
                                        SenderCourt = "Kucoin"
                                        
                                    if receiver == KucoinAddrs :
                                        ReceiverCourt = "Kucoin"
                                    
                                    message = f"🔄 Transfer of {NombreSAV} {SenderTicker} ({PriceValue}$) made between {SenderCourt} and {ReceiverCourt} on {TimestampLisible}\n['{SenderCourt}' ---> '{ReceiverCourt}']\n\n$TADA price : [{PriceArrondi}$US]\n\nSource : {Link}"
                                    print("Cette transaction est un transfert")
                                    print(message)
                                else:
                                    GetPrice()
                                    price = GetPrice()
                                    value = price * ReceiverValue
                                    ValueArrondi = round(value, 2)
                                    value = f"{ValueArrondi:.2f}"
                                    
                                    GetPriceTADA()
                                    price = GetPriceTADA()
                                    PriceValue = price * NombreSAV
                                    PriceValueArrondi = round(PriceValue, 2)
                                    PriceValueRounded = f"{PriceValueArrondi:.2f}"
                                    print(PriceValueArrondi)
                                    
                                    PriceArrondi = round(price, 4)
                                    PriceArrondi = f"{PriceArrondi:.4f}"
                                    print(PriceArrondi)
                                    

                                    if ReceiverValue == 0 :
                                        message = f"🔴 Sale of {NombreSAV} ${SenderTicker} ({PriceValueArrondi}$) on {TimestampLisible}\n\n$TADA price : [{PriceArrondi}$US]\n\nSource : {Link}"
                                        print("Cette transaction est une vente")
                                        print(message)
                                    else:
                                        message = f"🔴 Sale of {NombreSAV} ${SenderTicker} for {ReceiverValue} {ReceiverTicker} ({value}$) on {TimestampLisible}\n\n$TADA price : [{PriceArrondi}$US]\n\nSource : {Link}"
                                        print("Cette transaction est une vente")
                                        print(message)

                                    EnregistreTransac()

                                #si la valeur de la transaction est superieur a 100$US ca envoie le message sur discord
                                if PriceValue > 100 :
                                    SendDiscord()

                                #si la valeur de la transaction est superieur a 20 000$US ca envoie un tweet
                                #50 tweets max par jours rate limit api free
                                if PriceValue > 20000 :
                                    PostTheTweet()



                            elif FunctionTransac == "ESDTTransfer" :
                                print(FunctionTransac)
                                statut = "Achat"
                                print("Statut de la transaction :", statut)

                                if "originalTxHash" in transaction:
                                    TxIDForLink2 = transaction["originalTxHash"]
                                else:
                                    TxIDForLink2 = transaction.get("txHash")

                                AssetInfo = transaction["action"]["arguments"]["transfers"][0]
                                Nombre_SAV = int(AssetInfo["value"]) / (10 ** AssetInfo["decimals"])
                                NombreSAV = round(Nombre_SAV, 2)
                                TxID2 = transaction["action"]["arguments"]["transfers"][0]["value"]   
                                print("ID (valeur) de la transaction :", TxID2)
                                
                                if TxID2 == last_fee:
                                    continue
                                    
                                #deuxieme verification qui check si le montant de cette transaction est presente dans les 10 derniere
                                #si c'est le cas il passe a la suivante. (risque de manquer des transactions non doublon dans de rares cas)
                                Verif10DernieresTransac()
                                Doublon = Verif10DernieresTransac()
                                
                                if Doublon is True :
                                    continue
                                    
                                last_fee = TxID2

                                receiver = transaction["receiver"]
                                ReceiverCourt = receiver[:6] + "..." + receiver[-3:]
                                sender = transaction["sender"]
                                SenderCourt = sender[:6] + "..." + sender[-3:]
                                timestamp = transaction["timestamp"]
                                ReceiverTicker = AssetInfo["ticker"]
                                if "receiverAssets" in transaction:
                                    ReceiverName = transaction["receiverAssets"]["name"]
                                else:
                                    ReceiverName = ReceiverCourt

                                if "senderAssets" in transaction:
                                    SenderName = transaction["senderAssets"]["name"]
                                else:
                                     SenderName = SenderCourt

                                if TxIDForLink2 is not None:
                                    Link2 = LinkSource + TxIDForLink2
                                else:
                                    Erreur = "ERROR"
                                    Link2 = LinkSource + Erreur

                                TimestampLisible = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d at %H:%M:%S')
                                DateActuelle = datetime.now().date()
                                DateFormat = datetime.now().strftime("%Y-%m-%d")

                                print("Informations de la transaction :")
                                print("    Receiver :", receiver)
                                print("    Sender :", sender)
                                print("    Timestamp (humain) :", TimestampLisible)
                                print("    Ticker :", ReceiverTicker)
                                print("    Valeur :", NombreSAV)
                                print("    Source :", Link2)

                                GetPrice()
                                price = GetPrice()
                                PriceValue = NombreSAV * price
                                print(PriceValue)

                                value = price * NombreSAV
                                ValueArrondi = round(value, 2)
                                value = f"{ValueArrondi:.2f}"
                                
                                PriceArrondi = round(price, 4)
                                PriceArrondi = f"{PriceArrondi:.4f}"
                                print(PriceArrondi)

                                TransferSenderAddrs = not sender.startswith("erd1qqqq")
                                TransferReceiverAddrs = not receiver.startswith("erd1qqqq")

                                if TransferSenderAddrs and TransferReceiverAddrs:
                                    KucoinAddrs = "erd1ty4pvmjtl3mnsjvnsxgcpedd08fsn83f05tu0v5j23wnfce9p86snlkdyy"
                                    
                                    if sender == KucoinAddrs :
                                        SenderCourt = "Kucoin"
                                        
                                    if receiver == KucoinAddrs :
                                        ReceiverCourt = "Kucoin"
                                    
                                    message = f"🔄 Transfer of {NombreSAV} ${ReceiverTicker} ({value}$) made between {SenderCourt} and {ReceiverCourt} on {TimestampLisible}\n['{SenderCourt}' ---> '{ReceiverCourt}']\n\n$TADA price : [{PriceArrondi}$US]\n\nSource : {Link2}"
                                    print("Cette transaction est un transfert")
                                    print(message)
                                else:
                                    message = f"🟢 A purchase of {NombreSAV} ${ReceiverTicker} ({value}$) just took place ! \n(on {TimestampLisible})\n\n$TADA price : [{PriceArrondi}$US]\n\nSource : {Link2}"
                                    print("Cette transaction est un achat")
                                    print(message)
                                    Link = Link2
                                    EnregistreTransac()

                                if PriceValue > 100 :
                                    SendDiscord()

                                if PriceValue > 20000 :
                                    PostTheTweet()

            else:
                print("Aucune transaction trouvée.")
        else:
            print("La requête a échoué avec le code de statut :", response.status_code)

        DateActuelle = datetime.now().date()
        DateFormat = datetime.now().strftime("%Y-%m-%d")

        HeureActuelle = datetime.now().time()

        #code present pour eviter de lancer le recap des transaction plusieurs fois le meme jour
        if HeureActuelle.hour == 00 and 00 <= HeureActuelle.minute <= 10:
            print("Reinitialisation de la variable CheckHeure")
            CheckHeure = None

        if HeureActuelle.hour == 23 and 50 <= HeureActuelle.minute <= 59 and CheckHeure == None:
            print("C'est l'heure de faire le recap des transactions de la journée")
            CheckHeure = True

            TotalAchat = 0
            TotalVente = 0
            MontantAchat = 0
            MontantVente = 0

            with open('transactions.json', 'r') as file:
                for line in file:
                    transaction = json.loads(line)
                    if transaction['type'] == 'Achat':
                        TotalAchat += 1
                        MontantAchat += transaction['montant']
                    elif transaction['type'] == 'Vente':
                        TotalVente += 1
                        MontantVente += transaction['montant']

            TotalTransactions = TotalAchat + TotalVente
            TotalMontant = MontantAchat + MontantVente

            PourcentageAcheteurs = (TotalAchat / TotalTransactions) * 100
            PourcentageVendeurs = (TotalVente / TotalTransactions) * 100

            PourcentageAchats = (MontantAchat / TotalMontant) * 100
            PourcentageVentes = (MontantVente / TotalMontant) * 100
            
            MontantAchat_Arrondi = round(MontantAchat, 2)
            MontantAchatArrondi = f"{MontantAchat_Arrondi:.2f}"

            MontantVente_Arrondi = round(MontantVente, 2)
            MontantVenteArrondi = f"{MontantVente_Arrondi:.2f}"

            message = (
                    f"Summary of $TADA transactions on {DateActuelle} :\n\n"
                    f"🟢 Total number of transactions today : {TotalAchat} ({PourcentageAcheteurs:.2f}%)\n"
                    f"🔴 Total number of sales today : {TotalVente} ({PourcentageVendeurs:.2f}%)\n\n"
                    f"🟢 Purchase volume of the day : {MontantAchatArrondi} ({PourcentageAchats:.2f}%)\n"
                    f"🔴 Sales volume of the day : {MontantVenteArrondi} ({PourcentageVentes:.2f}%)\n\n"
            )

            print(message)
            SendDiscord()

            #Graph des transactions (nombres et pourcentages)
            plt.figure(figsize=(10, 6))
            bars = plt.bar([0, 1], [TotalAchat, TotalVente], color=['green', 'red'])
            plt.xlabel('Transactions')
            plt.ylabel('Number')
            plt.title(f'Number of transactions\n ({DateActuelle})')
            plt.xticks([0, 1], [f'Buying transactions\n ({PourcentageAcheteurs:.2f}%)', f'Sales transactions\n ({PourcentageVendeurs:.2f}%)'])
            plt.savefig('image1.jpg')
            #plt.show()

            #Graph des volumes (montant et pourcentages)
            plt.figure(figsize=(10, 6))
            plt.bar([0, 1], [MontantAchat, MontantVente], color=['green', 'red'])
            plt.xlabel('Purchases/Sales')
            plt.ylabel('Volumes amount $')
            plt.title(f'Transactions volume\n ({DateActuelle})')
            plt.xticks([0, 1], [f'Purchases volume\n ({PourcentageAchats:.2f}%)', f'Sales volume\n ({PourcentageVentes:.2f}%)'])
            plt.savefig('image2.jpg')
            #plt.show()

            EnregistreRecapDaily()
            
            open('transactions.json', 'w').close()

            #poste le message avec les images des graphs sur twitter
            PostTheTweetWithImages()
            
            #check si ca fait un moi pour poster le tableau loi de benford avec les données des transactions
            #si c'est le ca il post un tweet avec le tableau generé et le tableau "temoin"
            #il reinitialise aussi le fichier Json des 30 derniers jours de transactions
            #penser a faire un script qui sauvegarde ces transactions dans un autre fichier ou les enregistrer des le debut dans un fichier json non utilisé
            with open("MonthTransactions.json", "r") as file:
                PremiereTransac = file.readline().strip()
                Donnees = json.loads(PremiereTransac)
                DateTransac = datetime.strptime(Donnees["date"], "%Y-%m-%d")
                DateFormateeDebut = DateTransac.strftime("%Y-%m-%d")
                print(DateFormateeDebut)

            DateActuelle = datetime.now()
            DateFormat = datetime.now().strftime("%Y-%m-%d")

            difference = DateActuelle - DateTransac

            if (DateActuelle.month != DateTransac.month) and (difference.days >= 30):
                print("Ca fait un mois! Génération du tableau des données :")
                CalculBenford()
                message = "Benford tweet test avec images"
                PostBenfordTweetImages()
                open('MonthTransactions.json', 'w').close()
            else:
                print("Ca ne fait pas encore 1 mois.")
            
    except Exception as e:
        message = f"erreur dans le code : {e}"
        print(message)
        #send discord message pour prevenir de l'erreur
        SendDiscordErreurs()
        pass
