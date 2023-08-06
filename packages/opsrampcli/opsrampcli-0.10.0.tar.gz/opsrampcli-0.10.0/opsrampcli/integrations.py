import json

def build_disco_profile(args):
    if args.recurrence == 'NONE':
        return False

    schedule = {}

    if args.recurrence == 'WEEKLY':
        schedule['patternType'] = 'WEEKLY'
        schedule['pattern'] = args.daysofweek.lower()
        schedule['startTime'] = args.starthour
    elif args.recurrence == 'DAILY':
        schedule['patternType'] = 'DAILY'
        schedule['pattern'] = 1
        schedule['startTime'] = args.starthour

    rules = []
    if args.rules:
        ruleitems = args.rules.split(",")
        for rule in ruleitems:
            rules.append({ "filterType": rule})
    else:
        rules.append({ "filterType": "ANY_CLOUD_RESOURCE"})
    discoprofile = [
            {
                "policy": {
                    "name": args.azname,
                    "entityType": "ALL",
                    "matchType": "ANY",
                    "rules": rules,
                    "actions": [
                        {
                        "action": "MANAGE DEVICE"
                        }
                    ]
                },
                "scanNow": True,
                "schedule": schedule,              
            }
        ]
    return discoprofile

def do_add_azure_arm(ops, args):
    obj = {
            "displayName": args.azname,
            "credential": {
                "credentialType": "AZURE",
                "SubscriptionId": args.azsub,
                "AzureType": "ARM",
                "TenantId": args.aztenant,
                "ClientID": args.azclient,
                "SecretKey": args.azsecret
             }
    }
    discoprofile = build_disco_profile(args)
    if discoprofile:
        obj['discoveryProfiles'] = discoprofile
    return ops.add_integration("Azure", obj)

def do_add_azure_asm(ops, args):
    obj = {
            "displayName": args.azname,
            "credential": {
                "credentialType": "AZURE",
                "SubscriptionId": args.azsub,
                "AzureType": "ASM",
                "ManagementCertificate": args.azcert,
                "KeystorePassword": args.azkspw
             }
    }
    discoprofile = build_disco_profile(args)
    if discoprofile:
        obj['discoveryProfiles'] = discoprofile
    return ops.add_integration("Azure", obj)

def do_import_integrations(ops, args):
    intarray = None
    with open(args.file, "r") as file:
        jsonfileobj = json.load(file)
        if type(jsonfileobj) == list:
            intarray = jsonfileobj
        else:
            intarray = [jsonfileobj]
    for intobj in intarray:
        display_name = "Unnamed"
        unique_name = "No unique name"
        if "displayName" in intobj:
            display_name = intobj["displayName"]
        if "integration" in intobj and "name" in intobj["integration"]:
            unique_name = intobj["integration"]["name"]
        for attr in ["integration", "installedBy", "installedTime"]:
            if attr in intobj:
                del intobj[attr]
        try:
            print(f'Importing {display_name} of type {unique_name}...')             
            result = ops.add_integration(unique_name, intobj)
            if "id" in result:
                print(f'Successfully created integration with id {result["id"]}\n')
            else:
                print(f'Integration was not created: {json.dumps(result, indent=2, sort_keys=False)}\n')
        except Exception as e:
            print(e)
