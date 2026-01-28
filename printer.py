from escpos.printer import Usb

# TODO: Consider reading VendorID and ProductID from a configuration file or environment variables
printer = Usb(0x04b8, 0x0e28, profile="TM-T88III")
printer.profile.profile_data["media"]["width"]["pixels"] = 576
