# Connecting to AWS
import boto3

import json
# Create random name for things
import random
import string
import argparse
import geocoder

# Parameters for Thing
thingArn = ''
thingId = ''
thingName = ''
defaultPolicyName = 'cdjhvlamt-policy'
print(thingName)
thingClient = boto3.client('iot')

###################################################


def createThing(eigenaar, adres):
    global thingClient
    global thingName
    thingName = 'cdjhvlamt-' + eigenaar
    g = geocoder.osm(adres)

    
    print(thingName)
    thingResponse = thingClient.create_thing(
        thingName=thingName,
        thingTypeName = "CDJHVlam",
        attributePayload={
        "attributes": {
            "eigenaar": eigenaar,
            "lat": str(g.json['lat']),
            "lng": str(g.json['lng']),
            "adres": adres.replace(" ", '_')
        }
    },
    )
    data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'thingArn':
            thingArn = data['thingArn']
        elif element == 'thingId':
            thingId = data['thingId']
    createCertificate()


def createCertificate():
    global thingClient
    certResponse = thingClient.create_keys_and_certificate(
        setAsActive=True
    )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'certificateArn':
            certificateArn = data['certificateArn']
        elif element == 'keyPair':
            PublicKey = data['keyPair']['PublicKey']
            PrivateKey = data['keyPair']['PrivateKey']
        elif element == 'certificatePem':
            certificatePem = data['certificatePem']
        elif element == 'certificateId':
            certificateId = data['certificateId']

    with open('public.key', 'w') as outfile:
        outfile.write(PublicKey)
    with open('private.key', 'w') as outfile:
        outfile.write(PrivateKey)
    with open('cert.pem', 'w') as outfile:
        outfile.write(certificatePem)

    response = thingClient.attach_policy(
        policyName=defaultPolicyName,
        target=certificateArn
    )
    response = thingClient.attach_thing_principal(
        thingName=thingName,
        principal=certificateArn
    )


# createThing()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--Eigenaar", help = "Van wie is dit vlammetje?")
    parser.add_argument("-a", "--Adres", help = "Waar woon je?")
    args = parser.parse_args()
    if args.Eigenaar:
        print("Eigenaar van dit vlammetje: % s" % args.Eigenaar)
    if args.Adres:
        print("Adres van dit vlammetje: % s" % args.Adres)
    createThing(args.Eigenaar, args.Adres)


