# Lab 1: Mobile Application Security Analysis with APKTool and Jadx

## Objective
Learn to perform static analysis on Android applications to identify security vulnerabilities, hardcoded credentials, and insecure configurations.

## Prerequisites
- Kali Linux system
- Android smartphone (for testing)
- Internet connection
- Basic understanding of Android applications

## Lab Duration
Approximately 60-90 minutes

## Learning Outcomes
After completing this lab, you will be able to:
1. Decompile Android APK files
2. Analyze application manifests for security issues
3. Identify hardcoded credentials and API keys
4. Examine network security configurations
5. Understand common mobile application vulnerabilities

## Required Tools
All tools are available in Kali Linux:
- `apktool` - APK decompilation tool
- `jadx` or `jadx-gui` - Java decompiler
- `zipalign` - APK optimization tool (optional)
- `adb` - Android Debug Bridge

## Part 1: Environment Setup (15 minutes)

### Step 1: Install Required Tools

```bash
# Update system
sudo apt update

# Install apktool
sudo apt install -y apktool

# Install jadx (GUI version recommended)
sudo apt install -y jadx

# Install Android tools
sudo apt install -y android-tools-adb android-tools-fastboot

# Verify installations
apktool --version
jadx --version
adb version
```

### Step 2: Download Sample APK

For this lab, we'll use intentionally vulnerable applications:

```bash
# Create working directory
mkdir -p ~/mobile-security-lab
cd ~/mobile-security-lab

# Download DIVA (Damn Insecure and Vulnerable App)
wget https://github.com/payatu/diva-android/raw/master/app/release/diva-beta.apk

# Alternative: InsecureBankv2
# wget https://github.com/dineshshetty/Android-InsecureBankv2/raw/master/AndroLabServer/InsecureBankv2.apk
```

**Note:** If download fails, you can also download APKs from:
- APKPure.com
- APKMirror.com
- Or use any APK from your phone (non-system apps)

## Part 2: APK Decompilation (20 minutes)

### Step 3: Decompile APK with APKTool

```bash
# Decompile the APK
apktool d diva-beta.apk -o diva-decompiled

# List the contents
ls -la diva-decompiled/
```

**Expected Output:**
```
AndroidManifest.xml
apktool.yml
original/
res/
smali/
```

### Step 4: Analyze AndroidManifest.xml

```bash
# View the manifest file
cat diva-decompiled/AndroidManifest.xml
```

**Tasks:**
1. Identify all declared permissions
2. Check for exported activities/services/receivers
3. Look for debuggable flag
4. Check minimum SDK version
5. Identify any custom permissions

**Security Checklist:**
- [ ] Is `android:debuggable="true"` present? (CRITICAL vulnerability)
- [ ] Are there unnecessary permissions?
- [ ] Are there exported components without proper protection?
- [ ] Is backup enabled (`android:allowBackup="true"`)?
- [ ] Are there any cleartext traffic settings?

### Step 5: Examine Network Security Configuration

```bash
# Check for network security config
cat diva-decompiled/res/xml/network_security_config.xml 2>/dev/null || echo "No network security config found"

# Check if cleartext traffic is allowed in manifest
grep -i "cleartextTraffic" diva-decompiled/AndroidManifest.xml
```

**Questions to Answer:**
1. Does the app allow cleartext HTTP traffic?
2. Are there any certificate pinning configurations?
3. Are there custom trust anchors defined?

## Part 3: Source Code Analysis (30 minutes)

### Step 6: Decompile to Java Source Code

```bash
# Use jadx to decompile to Java
jadx -d diva-java-source diva-beta.apk

# Or use GUI version
jadx-gui diva-beta.apk &
```

### Step 7: Search for Common Vulnerabilities

**Search for Hardcoded Credentials:**
```bash
cd diva-java-source
grep -r -i "password" --include="*.java" .
grep -r -i "api_key\|apikey" --include="*.java" .
grep -r -i "secret" --include="*.java" .
grep -r -i "token" --include="*.java" .
```

**Search for Insecure Storage:**
```bash
# Look for SharedPreferences usage
grep -r "SharedPreferences" --include="*.java" .

# Look for file operations
grep -r "FileOutputStream\|FileInputStream" --include="*.java" .

# Look for SQLite databases
grep -r "SQLiteDatabase" --include="*.java" .
```

**Search for Insecure Communications:**
```bash
# HTTP connections
grep -r "http://" --include="*.java" .

# SSL/TLS issues
grep -r "TrustManager\|HostnameVerifier" --include="*.java" .

# WebView security
grep -r "WebView\|addJavascriptInterface" --include="*.java" .
```

### Step 8: Analyze Specific Vulnerabilities in DIVA

**Insecure Logging:**
```bash
# Search for Log statements
grep -r "Log\." --include="*.java" . | head -20
```

**SQL Injection:**
```bash
# Look for raw SQL queries
grep -r "rawQuery\|execSQL" --include="*.java" .
```

**Insecure Data Storage:**
```bash
# Check how sensitive data is stored
grep -r -A 5 "MODE_WORLD_READABLE\|MODE_WORLD_WRITABLE" --include="*.java" .
```

## Part 4: Dynamic Analysis Setup (15 minutes)

### Step 9: Enable USB Debugging on Your Android Phone

**On your Android device:**
1. Go to Settings > About Phone
2. Tap "Build Number" 7 times to enable Developer Options
3. Go to Settings > Developer Options
4. Enable "USB Debugging"
5. Connect phone to Kali via USB

### Step 10: Verify ADB Connection

```bash
# List connected devices
adb devices

# If device shows as unauthorized, check phone for authorization prompt

# Once authorized
adb shell getprop ro.build.version.release  # Android version
adb shell getprop ro.product.model  # Device model
```

### Step 11: Install the APK

```bash
# Install the decompiled app
adb install diva-beta.apk

# Verify installation
adb shell pm list packages | grep -i diva
```

### Step 12: Pull Application Data (Root Required for full access)

```bash
# Without root, you can only access your app's data if debuggable
adb shell run-as jakhar.aseem.diva ls /data/data/jakhar.aseem.diva/

# If device is rooted
adb shell su -c "ls -la /data/data/jakhar.aseem.diva/"

# Pull databases
adb pull /data/data/jakhar.aseem.diva/databases/
```

## Part 5: Vulnerability Report (10 minutes)

### Step 13: Document Your Findings

Create a simple vulnerability report with the following sections:

**Template:**
```markdown
# Mobile Application Security Assessment Report

**Application:** [App Name]
**Package Name:** [com.example.app]
**Version:** [1.0]
**Tested By:** [Your Name]
**Date:** [Current Date]

## Executive Summary
[Brief overview of findings]

## Vulnerabilities Identified

### 1. [Vulnerability Name]
- **Severity:** Critical/High/Medium/Low
- **Description:** [What is the issue]
- **Evidence:** [Code snippet or screenshot]
- **Impact:** [What can an attacker do]
- **Recommendation:** [How to fix]

### 2. [Next vulnerability]
...

## Conclusion
[Overall security posture]
```

## Expected Findings in DIVA App

If using DIVA, you should find:
1. ✅ Insecure Logging - Credentials logged in LogCat
2. ✅ Hardcoded Encryption Keys
3. ✅ Insecure Data Storage - SharedPreferences in MODE_PRIVATE
4. ✅ SQL Injection vulnerabilities
5. ✅ Insecure File Permissions
6. ✅ Weak Encryption Implementation
7. ✅ Insecure Communication (HTTP)
8. ✅ Input Validation Issues
9. ✅ Access Control Problems

## Challenge Questions

1. **What is the package name of the application?**
2. **Is the application debuggable? How did you determine this?**
3. **List 5 permissions requested by the application.**
4. **Did you find any hardcoded API keys or passwords?**
5. **What encryption algorithm is used in the application (if any)?**
6. **Are there any exported components? List them.**
7. **Does the app use HTTPS or HTTP for network communication?**
8. **What is the minimum Android SDK version supported?**
9. **Did you find any SQL queries that might be vulnerable to injection?**
10. **How is sensitive data stored in the application?**

## Additional Resources

- OWASP Mobile Security Testing Guide: https://owasp.org/www-project-mobile-security-testing-guide/
- OWASP Mobile Top 10: https://owasp.org/www-project-mobile-top-10/
- Android Security Documentation: https://developer.android.com/topic/security
- MobSF (Mobile Security Framework): Alternative automated analysis tool

## Bonus Tasks

1. **Recompile the APK:**
   ```bash
   apktool b diva-decompiled -o diva-modified.apk
   ```

2. **Sign the modified APK:**
   ```bash
   # Generate keystore
   keytool -genkey -v -keystore my-key.keystore -alias my-alias -keyalg RSA -keysize 2048 -validity 10000
   
   # Sign APK
   jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-key.keystore diva-modified.apk my-alias
   ```

3. **Install and test modified APK:**
   ```bash
   adb install diva-modified.apk
   ```

## Troubleshooting

**Issue: APKTool fails to decompile**
- Solution: Update apktool to latest version or try different framework files

**Issue: ADB doesn't detect device**
- Solution: Install proper USB drivers, check USB cable, verify USB debugging is enabled

**Issue: Cannot install APK**
- Solution: Uninstall existing version first with `adb uninstall [package-name]`

**Issue: Permission denied when accessing /data/data**
- Solution: This requires root access or debuggable app with run-as

## Lab Submission

Submit the following:
1. Your vulnerability assessment report (PDF or Markdown)
2. Screenshots showing:
   - Decompiled AndroidManifest.xml
   - At least one vulnerability you discovered
   - ADB connection to your device
3. Answers to all 10 challenge questions

## Grading Rubric

- Environment setup and tool usage: 20%
- Proper decompilation and analysis: 30%
- Vulnerability identification: 30%
- Documentation quality: 15%
- Challenge questions: 5%

---
**Lab Created for:** Cybersecurity Architecture Course - CEH Chapter 8
**Difficulty Level:** Intermediate
**Last Updated:** December 2025
