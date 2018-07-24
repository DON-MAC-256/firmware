# (c) Copyright 2018 by Coinkite Inc. This file is part of Coldcard <coldcardwallet.com>
# and is covered by GPLv3 license found in COPYING.
#
# flow.py - Menu structure
#
from menu import MenuItem

from actions import *
from choosers import *

#
# NOTE: "Always In Title Case"
#
# - try to keep harmless things as first item: so double-tap of OK does no harm

PinChangesMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem('Change Main PIN', f=pin_changer, arg='main'),
    MenuItem('Second Wallet', f=pin_changer, arg='secondary'),
    MenuItem('Duress PIN', f=pin_changer, arg='duress'),
    MenuItem('Brick Me PIN', f=pin_changer, arg='brickme'),
    MenuItem('Login Now', f=login_now, arg=1),
]

SecondaryPinChangesMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem('Second Wallet', f=pin_changer, arg='secondary'),
    MenuItem('Duress PIN', f=pin_changer, arg='duress'),
    MenuItem('Login Now', f=login_now, arg=1),
]

async def which_pin_menu(_1,_2, item):
    from main import pa
    return PinChangesMenu if not pa.is_secondary else SecondaryPinChangesMenu

SettingsMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem('Idle Timeout', chooser=idle_timeout_chooser),
    MenuItem('Blockchain', chooser=chain_chooser),
    MenuItem('Change PIN code', menu=which_pin_menu),
]

SDCardMenu = [
    MenuItem("Verify Backup", f=verify_backup),
    MenuItem("Backup System", f=backup_everything),
    MenuItem("Dump Summary", f=dump_summary),
    MenuItem('Upgrade From SD', f=microsd_upgrade),
    MenuItem("Electrum Wallet", f=electrum_skeleton),
    MenuItem('List Files', f=list_files),
    #MenuItem('Reformat Card', f=wipe_microsd),      # removed: not reliable enuf
]

UpgradeMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem('Show Version', f=show_version),
    MenuItem('From MicroSD', f=microsd_upgrade),
    MenuItem('Bless Firmware', f=bless_flash),
]

DevelopersMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem("Normal USB Mode", f=dev_enable_protocol),
    MenuItem("Enable USB REPL", f=dev_enable_vcp),
    MenuItem("Enable USB Disk", f=dev_enable_disk),
    MenuItem("Wipe Patch Area", f=wipe_filesystem),
    MenuItem('Warm Reset', f=reset_self),
]

AdvancedVirginMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem("View Identity", f=view_ident),
    MenuItem('Upgrade firmware', menu=UpgradeMenu),
    MenuItem('Perform Selftest', f=start_selftest),
    MenuItem("I Am Developer.", menu=maybe_dev_menu),           # security risk?
    MenuItem('Secure Logout', f=logout_now),
]

DebugFunctionsMenu = [
    MenuItem('Debug: assert', f=debug_assert),
    MenuItem('Debug: except', f=debug_except),
    MenuItem('Check: BL FW', f=check_firewall_read),
    MenuItem('Warm Reset', f=reset_self),
    #MenuItem("Perform Selftest", f=start_selftest),
]

DangerZoneMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem("Debug Functions", menu=DebugFunctionsMenu),       # actually harmless
    MenuItem("Destroy Seed", f=clear_seed),
    MenuItem("I Am Developer.", menu=maybe_dev_menu),
    MenuItem("Wipe Patch Area", f=wipe_filesystem),             # needs better label
    MenuItem('Perform Selftest', f=start_selftest),             # little harmful
    MenuItem("Set High-Water", f=set_highwater),
]

BackupStuffMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem("Backup System", f=backup_everything),
    MenuItem("Verify Backup", f=verify_backup),
    MenuItem("Restore Backup", f=restore_everything),   # just a redirect really
    MenuItem("Dump Summary", f=dump_summary),
]

AdvancedNormalMenu = [
    #         xxxxxxxxxxxxxxxx
    MenuItem("View Identity", f=view_ident),
    MenuItem("Upgrade", menu=UpgradeMenu),
    MenuItem("Backup", menu=BackupStuffMenu),
    MenuItem("MicroSD Card", menu=SDCardMenu),
    MenuItem("Danger Zone", menu=DangerZoneMenu),
]

# needs to create main wallet PIN
VirginSystem = [
    #         xxxxxxxxxxxxxxxx
    MenuItem('Choose PIN Code', f=initial_pin_setup),
    MenuItem('Advanced', menu=AdvancedVirginMenu),
    MenuItem('Bag Number', f=show_bag_number),
    MenuItem('Help', f=virgin_help),
]

ImportWallet = [
    MenuItem("24 Words", menu=start_seed_import, arg=24),
    MenuItem("18 Words", menu=start_seed_import, arg=18),
    MenuItem("12 Words", menu=start_seed_import, arg=12),
    MenuItem("Restore Backup", f=restore_everything),
    MenuItem("Import XPRV", f=import_xprv ), 
]

# has PIN, but no secret seed yet
EmptyWallet = [
    #         xxxxxxxxxxxxxxxx
    MenuItem('New Wallet', f=pick_new_wallet),
    MenuItem('Import Existing', menu=ImportWallet),
    MenuItem('Help', f=virgin_help),
    MenuItem('Advanced', menu=AdvancedVirginMenu),
    MenuItem('Settings', menu=SettingsMenu),
]



# In operation, normal system, after a good PIN received.
NormalSystem = [
    #         xxxxxxxxxxxxxxxx
    MenuItem('Ready To Sign', f=ready2sign),
    MenuItem('Secure Logout', f=logout_now),
    MenuItem('Advanced', menu=AdvancedNormalMenu),
    MenuItem('Settings', menu=SettingsMenu),
]

# Shown until unit is put into a numbered bag
FactoryMenu = [
    MenuItem('Bag Me Now'),     # nice to have NOP at top of menu
    MenuItem('DFU Upgrade', f=start_dfu),
    MenuItem('Show Version', f=show_version),
    MenuItem('Ship W/O Bag', f=ship_wo_bag),
    MenuItem("Debug Functions", menu=DebugFunctionsMenu),
    MenuItem("Perform Selftest", f=start_selftest),
]

