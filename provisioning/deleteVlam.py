import boto3

import json
import argparse

thingClient = boto3.client('iot')


def deleteVlam(vlamNaam):
	res = thingClient.list_thing_principals(thingName = vlamNaam)
	certArn = res["principals"][0]
	print(certArn)
	cert_id = certArn.split('/')[1]
	r_detach_thing = thingClient.detach_thing_principal(thingName=vlamNaam,principal=certArn)
	r_upd_cert = thingClient.update_certificate(certificateId=cert_id,newStatus='INACTIVE')
	r_del_cert = thingClient.delete_certificate(certificateId=cert_id,forceDelete=True)
	r_del_thing = thingClient.delete_thing(thingName=vlamNaam)



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--VlamNaam", help="naam van het vlammeke")
	args = parser.parse_args()
	if args.VlamNaam:
		deleteVlam(args.VlamNaam)
