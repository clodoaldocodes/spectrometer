HOST, PORT = '192.168.50.139', 9999
client = seabreeze_server.client.Client(HOST, PORT)

# Prints out currently plugged-in devices
print(
    "Available Devices:\n",
    "\n".join(["%d : %s" % (i,dev)\
                for i,dev in enumerate(client.list_devices())
             ])
)

# Select the first spectrometer
client.select_spectrometer(0)

# Set integration time to 10 ms
client.set_integration_time_micros(10*1000)

# Get wavelengths and intensities
wls = client.get_wavelengths()
i = client.get_intensities()