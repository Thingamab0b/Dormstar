import bluetooth
target_name='HC-06'
target_add='98:DA:60:02:6B:36'
port=1
device_list=bluetooth.discover_devices(lookup_names=True)


for (device_add,device_name) in device_list:
    if target_name==device_name and target_add==device_add:
        print('Found!')
        try:
            s=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            s.connect((target_add,port))
            print('Connected')
            s.send(bytes('/x00/x00/x00'))
        except bluetooth.btcommon.BluetoothError as err:
            pass
        