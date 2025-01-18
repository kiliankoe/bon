from escpos.printer import Usb

# TODO: Consider reading VendorID and ProductID from a configuration file or environment variables
# TODO: Figure out how to set a valid media width pixel field for centering media
printer = Usb(0x04b8, 0x0e28, profile="TM-T88III")
