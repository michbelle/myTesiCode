laserTTYinfo=['10c4', 'ea60']
# imuTTYinfo=['0403','6001'] # FT232RL
imuTTYinfo=['0403','6014'] # FT232H

def getttyusbconnected(vendorID:str, productID:str)->str:
    import pyudev

    context = pyudev.Context()

    # Iterate over all devices in the system
    for device in context.list_devices(subsystem='tty'):
        # Check if the device has the correct vendor and product ID
        if device.get('ID_VENDOR_ID') == vendorID and device.get('ID_MODEL_ID') == productID:
            return str(device.device_node)
    else:
        raise ValueError('Device not found')

for dev in [laserTTYinfo, imuTTYinfo]:
    print(getttyusbconnected(dev[0],dev[1]))