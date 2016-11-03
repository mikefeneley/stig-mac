
import subprocess
from subprocess import call

from mac_system_logger import MacSystemLogger

class MacSystemAuditor:
    """
    Check the system configuartion of the operating system
    to see if any aspect of the setup violates the requirements of the 
    DIA Mac 10.11 STIG.
    """
    def __init__(self, holder_filename = "mac_holder.txt"):
        self.holder_filename = holder_filename

    def audit(self):
        logger = MacSystemLogger()
        result = self.session_lock_enabled()
        logger.session_lock_enabled_errmsg(0)
        result = self.session_lock_time_set()
        logger.session_lock_time_set_errmsg(0)
        result = self.session_login_required()
        logger.session_login_required_errmsg(0)
        result = self.ir_support_disabled()
        logger.ir_support_disabled_errmsg(0)
        result = self.blank_cd_action_disabled()
        logger.blank_cd_action_disabled_errmsg(0)
        result = self.blank_dvd_action_disabled()
        logger.blank_dvd_action_disabled_errmsg(0)
        result = self.music_cd_action_disabled()
        logger.music_cd_action_disabled_errmsg(0)
        result = self.picture_cd_action_disabled()
        logger.picture_cd_action_disabled_errmsg(0)
        result = self.video_dvd_action_disabled()
        logger.video_dvd_action_disabled_errmsg(result)
    def session_lock_enabled(self):
        """
        Check SV-81951r1_rule: The operating system must conceal, via 
        the session lock, information previously visible on the 
        display with a publicly viewable image.

        Finding ID: V-67461

        :returns: bool -- True if criteria is met, False otherwise
        """
        holder_info = open(self.holder_filename, "w")

        p1 = subprocess.Popen(["/usr/sbin/system_profiler", 
            "SPConfigurationProfileDataType"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "moduleName"], 
            stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        holder_info = open(self.holder_filename, "r")

        enabled = False
        for line in holder_info:
        	if "moduleName" in line:
        		enabled = True
        holder_info.close()
        return enabled


    def session_lock_time_set(self):
    	"""
        Check SV-81953r1_rule: The operating system must initiate a session 
        lock after a 15-minute period of inactivity.

        Finding ID: V-67463 CHECK TIME

        :returns: bool -- True if criteria is met, False otherwise
        """
        holder_info = open(self.holder_filename, "w")

        p1 = subprocess.Popen(["/usr/sbin/system_profiler", 
            "SPConfigurationProfileDataType"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "idleTime"], 
            stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        holder_info = open(self.holder_filename, "r")
        time_set = False
        for line in holder_info:
            print(line)
            if "idleTime" in line:
                for s in line.split():
                    s = s.strip(';')
                    if(s.isdigit()):
                        number = int(s)
                        if(number <= 900):
                            time_set = True
        holder_info.close()
        print(time_set)
        return time_set


	   

    def session_login_required(self):
    	"""
        Check SV-81955r1_rule: The operating system must retain the 
        session lock until the user reestablishes access using established 
        identification and authentication procedures.

        Finding ID: V-67465 

        :returns: bool -- True if criteria is met, False otherwise
        """
        holder_info = open(self.holder_filename, "w")

        p1 = subprocess.Popen(["/usr/sbin/system_profiler", 
            "SPConfigurationProfileDataType"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "askForPassword"], 
            stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        holder_info = open(self.holder_filename, "r")

        login_required = False
        for line in holder_info:
            if "askForPassword = 1;" in line:
                login_required = True
        holder_info.close()
        return login_required

    def ir_support_disabled(self):
        """
        Check SV-81989r1_rule: Infrared [IR] support must be disabled.

        Finding ID: V-67499

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")
        call(["/usr/bin/sudo", "/usr/bin/defaults", "read", 
            "/Library/Preferences/com.apple.driver.AppleIRController", 
            "DeviceEnabled"], stdout=holder_info)
        holder_info.close()


        holder_info = open(self.holder_filename, "r")
        disabled = False
        for line in holder_info:
            if "0" in line:
                disabled = True
        holder_info.close()
        return disabled

    def blank_cd_action_disabled(self):
        """
        Check SV-81991r1_rule: Automatic actions must be disabled for blank CDs.

        Finding ID: V-67501

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")

        p1 = subprocess.Popen(["/usr/sbin/system_profiler", 
            "SPConfigurationProfileDataType"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "-A", "2", "'com.apple.digihub.blank.cd.appeared'"], 
            stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        holder_info = open(self.holder_filename, "r")       

        disabled = False
        for line in holder_info:
            if "action = 1" in line:
                disabled = True
        holder_info.close()
        return disabled

    def blank_dvd_action_disabled(self):
        """
        Check SV-81993r1_rule: Automatic actions must be disabled for blank DVDs.

        Finding ID: V-67503

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")

        p1 = subprocess.Popen(["/usr/sbin/system_profiler", 
            "SPConfigurationProfileDataType"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "-A", "2", 
            "'com.apple.digihub.blank.dvd.appeared'"], stdin=p1.stdout,
             stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        holder_info = open(self.holder_filename, "r")       

        disabled = False
        for line in holder_info:
            if "action = 1" in line:
                disabled = True
        holder_info.close()
        return disabled
    
    def music_cd_action_disabled(self):
        """
        Check SV-81995r1_rule: Automatic actions must be disabled for music CDs.

        Finding ID: V-67505

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")

        p1 = subprocess.Popen(["/usr/sbin/system_profiler", 
            "SPConfigurationProfileDataType"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "-A", "2", 
            "'com.apple.digihub.cd.music.appeared'"], stdin=p1.stdout,
             stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        holder_info = open(self.holder_filename, "r")       

        disabled = False
        for line in holder_info:
            if "action = 1" in line:
                disabled = True
        holder_info.close()
        return disabled    
    
    def picture_cd_action_disabled(self):
        """
        Check SV-81997r1_rule: Automatic actions must be disabled for picture CDs.

        Finding ID: V-67507

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")

        p1 = subprocess.Popen(["/usr/sbin/system_profiler", 
            "SPConfigurationProfileDataType"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "-A", "2", 
            "'com.apple.digihub.cd.picture.appeared'"], stdin=p1.stdout,
             stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        holder_info = open(self.holder_filename, "r")       

        disabled = False
        for line in holder_info:
            if "action = 1" in line:
                disabled = True
        holder_info.close()
        return disabled 

    def video_dvd_action_disabled(self):
        """
        Check SV-81999r1_rule: Automatic actions must be disabled for video DVDs.

        Finding ID: V-67509

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")

        p1 = subprocess.Popen(["/usr/sbin/system_profiler", 
            "SPConfigurationProfileDataType"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "-A", "2", 
            "'com.apple.digihub.dvd.video.appeared'"], stdin=p1.stdout,
             stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        holder_info = open(self.holder_filename, "r")       

        disabled = False
        for line in holder_info:
            if "action = 1" in line:
                disabled = True
        holder_info.close()
        return disabled         

    def smb_file_sharing_disabled(self):
        """
        Check SV-82021r1_rule: SMB File Sharing must be disabled unless required.

        Finding ID: V-67531

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")
        p1 = subprocess.Popen(["/usr/bin/sudo", "/bin/launchctl", 
                "print-disabled", "system"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "com.apple.smbd"],
                stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        disabled = False
        for line in holder_info:
            if '"com.apple.smbd" => true' in line:
                disabled = True
        holder_info.close()
        return disabled

    def apple_file_sharing_disabled(self):
        """
        Check SV-82023r1_rule: Apple File (AFP) Sharing must be disabled.

        Finding ID: V-67533

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")
        p1 = subprocess.Popen(["/usr/bin/sudo", "/bin/launchctl", 
                "print-disabled", "system"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "com.apple.AppleFileServer"],
                stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        disabled = False
        for line in holder_info:
            if '"com.apple.AppleFileServer" => true' in line:
                disabled = True
        holder_info.close()
        return disabled

    def nfs_daemon_disabled(self):
        """
        Check SV-82025r1_rule: The NFS daemon must be disabled unless required.

        Finding ID: V-67535

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")
        p1 = subprocess.Popen(["/usr/bin/sudo", "/bin/launchctl", 
                "print-disabled", "system"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "com.apple.nfsd"],
                stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        disabled = False
        for line in holder_info:
            if '"com.apple.nfsd" => true' in line:
                disabled = True
        holder_info.close()
        return disabled

    def nfs_lock_daemon_disabled(self):
        """
        Check SV-82027r1_rule: The NFS lock daemon must be disabled unless required.

        Finding ID: V-67537

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")
        p1 = subprocess.Popen(["/usr/bin/sudo", "/bin/launchctl", 
                "print-disabled", "system"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "com.apple.lockd"],
                stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        disabled = False
        for line in holder_info:
            if '"com.apple.lockd" => true' in line:
                disabled = True
        holder_info.close()
        return disabled

    def nfs_stat_daemon_disabled(self):
        """
        Check SV-82029r1_rule: The NFS stat daemon must be disabled unless required.

        Finding ID: V-67539

        :returns: bool -- True if criteria is met, False otherwise
        """ 
        holder_info = open(self.holder_filename, "w")
        p1 = subprocess.Popen(["/usr/bin/sudo", "/bin/launchctl", 
                "print-disabled", "system"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["/usr/bin/grep", "com.apple.statd.notify"],
                stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output,err = p2.communicate()
        holder_info.write(output)
        holder_info.close()

        disabled = False
        for line in holder_info:
            if '"com.apple.statd.notify" => true' in line:
                disabled = True
        holder_info.close()
        return disabled



    """
    Check RULE:

    Finding ID: ID

    :returns: bool -- True if criteria is met, False otherwise
    """ 
if __name__ == "__main__":
	auditor = MacSystemAuditor()
	auditor.audit()