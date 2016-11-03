class MacSystemLogger:
    """
    MacSystemLogger writes error messages to the mac network log file
    for Mac network rule in the Mac STIG that is violated
    """
    def __init__(self, filename="MacSystemLog.txt"):
        self.filename = filename
        self.log = open(filename, 'w')
        self.log.write("#########################\n\n")
        self.log.write("Mac System Audit Findings\n\n")

    def __del__(self):
        self.log.write("#########################\n\n")
        self.log.close()

    def get_filename(self):
        return self.filename

    def session_lock_enabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81951r1_rule: ")
            self.log.write("The operating system must conceal, via the session lock, information previously visible on the display with a publicly viewable image.\n\n")
            self.log.write("To fix: ")
            self.log.write(" This setting is enforced using the Login Window Policy configuration profile.\n\n\n")

    def session_lock_time_set_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81953r1_rule: ")
            self.log.write("The operating system must initiate a session lock after a 15-minute period of inactivity.\n\n")
            self.log.write("To fix: ")
            self.log.write(" This setting is enforced using the Login Window Policy configuration profile.\n\n\n")

    def session_login_required_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81955r1_rule: ")
            self.log.write("The operating system must retain the session lock until the user reestablishes access using established identification and authentication procedures.\n\n")
            self.log.write("To fix: ")
            self.log.write(" This setting is enforced using the Login Window Policy configuration profile.\n\n\n")

    def ir_support_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81989r1_rule: ")
            self.log.write("Infrared [IR] support must be disabled.\n\n")
            self.log.write("To fix: ")
            self.log.write("To disable IR, run the following command: /usr/bin/sudo /usr/bin/defaults write /Library/Preferences/com.apple.driver.AppleIRController DeviceEnabled -bool FALSE \n\n\n")

    def blank_cd_action_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81991r1_rule: ")
            self.log.write("Automatic actions must be disabled for blank CDs.\n\n")
            self.log.write("To fix: ")
            self.log.write("This setting is enforced using the Custom Policy configuration profile. \n\n\n")

    def blank_dvd_action_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81993r1_rule: ")
            self.log.write("Automatic actions must be disabled for blank DVDs.\n\n")
            self.log.write("To fix: ")
            self.log.write("This setting is enforced using the Custom Policy configuration profile. \n\n\n")

    def music_cd_action_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81995r1_rule: ")
            self.log.write("Automatic actions must be disabled for music CDs.\n\n")
            self.log.write("To fix: ")
            self.log.write("This setting is enforced using the Custom Policy configuration profile. \n\n\n")

    def picture_cd_action_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81997r1_rule: ")
            self.log.write("Automatic actions must be disabled for picture CDs.\n\n")
            self.log.write("To fix: ")
            self.log.write("This setting is enforced using the Custom Policy configuration profile. \n\n\n")

    def video_dvd_action_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-81999r1_rule: ")
            self.log.write("Automatic actions must be disabled for video DVDs.\n\n")
            self.log.write("To fix: ")
            self.log.write("This setting is enforced using the Custom Policy configuration profile. \n\n\n")

    def smb_file_sharing_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-82021r1_rule: ")
            self.log.write("SMB File Sharing must be disabled unless required.\n\n")
            self.log.write("To fix: ")
            self.log.write("To disable the SMB File Sharing service, run the following command: /usr/bin/sudo /bin/launchctl disable system/com.apple.smbd\n\n\n")

    def apple_file_sharing_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-82023r1_rule: ")
            self.log.write("Apple File (AFP) Sharing must be disabled unless required.\n\n")
            self.log.write("To fix: ")
            self.log.write("To disable the Apple File (AFP) Sharing service, run the following command: /usr/bin/sudo /bin/launchctl disable system/com.apple.AppleFileServer\n\n\n")

    def nfs_daemon_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-82025r1_rule: ")
            self.log.write("The NFS daemon must be disabled unless required.\n\n")
            self.log.write("To fix: ")
            self.log.write("To check if the NFS daemon is disabled, use the following command: /usr/bin/sudo /bin/launchctl print-disabled system | /usr/bin/grep com.apple.nfsd\n\n\n")

    def nfs_lock_daemon_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-82027r1_rule: ")
            self.log.write("SThe NFS lock daemon must be disabled unless required.\n\n")
            self.log.write("To fix: ")
            self.log.write("To check if the NFS lock daemon is disabled, use the following command: /usr/bin/sudo /bin/launchctl print-disabled system | /usr/bin/grep com.apple.lockd\n\n\n")

    def nfs_stat_daemon_disabled_errmsg(self, result):
        if result == 0:
            self.log.write("Check SV-82029r1_rule: ")
            self.log.write("The NFS stat daemon must be disabled unless required.\n\n")
            self.log.write("To fix: ")
            self.log.write("To disable the NFS stat daemon, run the following command: /usr/bin/sudo /bin/launchctl disable system/com.apple.statd.notify\n\n\n")

	