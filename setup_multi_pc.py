"""
Multi-PC Setup Installer
- One-command setup for multiple computers
- Configures GitHub sync
- Sets up Task Scheduler (Windows) or Cron (Mac/Linux)
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from dotenv import load_dotenv

def run_command(cmd, description=""):
    """Run command and report status"""
    if description:
        print(f"\n📝 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            if description:
                print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}")
            print(f"   Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

class MultiPCSetup:
    def __init__(self):
        self.os_type = platform.system()
        self.repo_path = Path.cwd()
        
    def setup_git_config(self):
        """Configure Git for this PC"""
        print("\n" + "="*70)
        print("🔧 STEP 1: GitHub Configuration")
        print("="*70)
        
        pc_name = input("\nPC Name (e.g., 'home-pc-1', 'office-pc-2'): ").strip()
        
        run_command(f'git config --local user.name "{pc_name}"', "Set Git username")
        run_command(f'git config --local user.email "scraper-{pc_name}@local"', "Set Git email")
        
        # Store PC name in .env
        env_file = Path('.env')
        if env_file.exists():
            content = env_file.read_text()
            if 'PC_NAME=' not in content:
                with open(env_file, 'a') as f:
                    f.write(f"\nPC_NAME={pc_name}\n")
        
        print(f"✅ Git configured for: {pc_name}")
        return pc_name

    def setup_dependencies(self):
        """Install Python dependencies"""
        print("\n" + "="*70)
        print("🔧 STEP 2: Install Dependencies")
        print("="*70)
        
        # Check Python version
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        print(f"✓ Python: {result.stdout.strip()}")
        
        # Install requirements
        if not run_command('pip install -r requirements.txt', "Installing Python packages"):
            print("⚠️ Some packages may have failed. Continuing...")
        
        # Install Playwright
        if not run_command('playwright install chromium', "Installing Playwright Chromium"):
            print("⚠️ Playwright installation may have issues. Trying alternate method...")
            run_command('python -m playwright install chromium', "Installing via Python module")
        
        # Install spaCy model
        if not run_command('python -m spacy download en_core_web_sm', "Installing spaCy model"):
            print("⚠️ spaCy download may have failed. Not critical.")
        
        print("\n✅ Dependencies installed")

    def setup_scheduler(self, pc_name):
        """Setup automatic scheduling"""
        print("\n" + "="*70)
        print("🔧 STEP 3: Setup Auto-Scheduling")
        print("="*70)
        
        if self.os_type == "Windows":
            self.setup_windows_scheduler(pc_name)
        elif self.os_type == "Darwin":
            self.setup_mac_scheduler(pc_name)
        elif self.os_type == "Linux":
            self.setup_linux_scheduler(pc_name)
        else:
            print(f"❓ Unknown OS: {self.os_type}")
            print("Please manually run: python local_scraper_scheduler.py")

    def setup_windows_scheduler(self, pc_name):
        """Setup Windows Task Scheduler"""
        print("\n📅 Setting up Windows Task Scheduler...")
        
        # Get Python executable path
        python_exe = sys.executable
        script_path = self.repo_path / "local_scraper_scheduler.py"
        
        # Create batch file
        batch_file = self.repo_path / "start_scraper.bat"
        batch_content = f"""@echo off
cd /d "{self.repo_path}"
"{python_exe}" "{script_path}"
pause
"""
        batch_file.write_text(batch_content)
        print(f"✓ Created: {batch_file}")
        
        # Create Task Scheduler XML
        task_name = f"StructCrew-Scraper-{pc_name}"
        xml_file = self.repo_path / f"{task_name}.xml"
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2025-12-03T00:00:00</Date>
    <Author>StructCrew</Author>
    <Description>Local Instagram scraper for {pc_name}</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <StartBoundary>2025-12-03T00:00:00</StartBoundary>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-21-3623811015-3361044348-30300820-1013</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <Duration>PT10M</Duration>
      <WaitTimeout>PT1H</WaitTimeout>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"{batch_file}"</Command>
      <WorkingDirectory>{self.repo_path}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""
        xml_file.write_text(xml_content)
        print(f"✓ Created: {xml_file}")
        
        print("\n📋 MANUAL SETUP NEEDED (Windows Task Scheduler):")
        print(f"1. Open Task Scheduler (Win+R → taskschd.msc)")
        print(f"2. Right-click 'Task Scheduler Library'")
        print(f"3. Select 'Import Task'")
        print(f"4. Browse to: {xml_file}")
        print(f"5. Click OK")
        print(f"\nOr run manually:")
        print(f"  {batch_file}")
        
        print(f"\n✅ Scheduler files created. Import into Task Scheduler.")

    def setup_mac_scheduler(self, pc_name):
        """Setup Mac launchd scheduler"""
        print("\n📅 Setting up Mac launchd...")
        
        python_exe = sys.executable
        script_path = self.repo_path / "local_scraper_scheduler.py"
        
        plist_name = f"com.structcrew.scraper-{pc_name}.plist"
        plist_path = Path.home() / "Library" / "LaunchAgents" / plist_name
        plist_path.parent.mkdir(parents=True, exist_ok=True)
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.structcrew.scraper-{pc_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_exe}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{self.repo_path}/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>{self.repo_path}/logs/launchd_error.log</string>
</dict>
</plist>
"""
        plist_path.write_text(plist_content)
        print(f"✓ Created: {plist_path}")
        
        # Load the plist
        run_command(f'launchctl load "{plist_path}"', "Loading launchd service")
        
        print(f"\n✅ Mac scheduler configured for {pc_name}")
        print(f"Logs: {self.repo_path}/logs/launchd.log")

    def setup_linux_scheduler(self, pc_name):
        """Setup Linux cron scheduler"""
        print("\n📅 Setting up Linux cron...")
        
        python_exe = sys.executable
        script_path = self.repo_path / "local_scraper_scheduler.py"
        
        cron_entry = f"@reboot cd {self.repo_path} && {python_exe} {script_path} >> logs/cron.log 2>&1"
        
        print(f"Add this line to your crontab:")
        print(f"\n{cron_entry}\n")
        print(f"To add it:")
        print(f"1. Run: crontab -e")
        print(f"2. Paste the line above")
        print(f"3. Save and exit")
        
        print(f"\n✅ Linux scheduler instructions provided")

    def verify_setup(self):
        """Verify everything is set up correctly"""
        print("\n" + "="*70)
        print("✅ VERIFICATION")
        print("="*70)
        
        checks = [
            ("Python", lambda: run_command('python --version')),
            ("Git", lambda: run_command('git --version')),
            ("Requirements", lambda: Path('requirements.txt').exists()),
            (".env", lambda: Path('.env').exists()),
            ("Scraper", lambda: Path('1_scraper/instagram_scraper_pro.py').exists()),
            ("Scheduler", lambda: Path('local_scraper_scheduler.py').exists()),
        ]
        
        for name, check in checks:
            try:
                if check():
                    print(f"✅ {name}")
                else:
                    print(f"⚠️ {name}")
            except:
                print(f"⚠️ {name}")
        
        print("\n✅ Setup complete!")

    def run(self):
        """Run full setup"""
        print("\n" + "="*70)
        print("🚀 StructCrew Multi-PC Setup Installer")
        print("="*70)
        print(f"OS: {self.os_type}")
        print(f"Location: {self.repo_path}")
        
        # Step 1: Git config
        pc_name = self.setup_git_config()
        
        # Step 2: Dependencies
        self.setup_dependencies()
        
        # Step 3: Scheduler
        self.setup_scheduler(pc_name)
        
        # Step 4: Verify
        self.verify_setup()
        
        print("\n" + "="*70)
        print("📖 NEXT STEPS:")
        print("="*70)
        print("\n1. ⚙️ MANUALLY setup scheduler (if needed)")
        print("   Windows: Import .xml file to Task Scheduler")
        print("   Mac: Copy plist path from above")
        print("   Linux: Add cron entry from above")
        print("\n2. 🧪 Test the scraper:")
        print(f"   python local_scraper_scheduler.py")
        print("\n3. 📊 Monitor progress:")
        print(f"   tail -f logs/local_scraper.log")
        print("\n4. 🔄 Check database growth:")
        print(f"   git log --oneline | head -20")
        print("\n" + "="*70)


if __name__ == "__main__":
    setup = MultiPCSetup()
    setup.run()
