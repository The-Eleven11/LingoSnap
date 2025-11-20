# LingoSnap 快捷键故障排除指南 / Hotkey Troubleshooting Guide

## 问题：快捷键无法激活 / Issue: Hotkeys Not Activating

如果您看到这样的消息但快捷键不工作：
If you see this message but hotkeys don't work:

```
Hotkey monitoring is active.
```

这意味着监听器正在运行，但由于系统限制无法捕获按键。
This means the listener is running but cannot capture keys due to system restrictions.

---

## 🔍 诊断步骤 / Diagnostic Steps

### 1. 检查显示服务器 / Check Display Server

**Wayland 通常有限制 / Wayland has restrictions:**

```bash
# 检查您使用的是什么 / Check what you're using
echo $XDG_SESSION_TYPE

# 如果输出是 "wayland"，这可能是问题所在
# If output is "wayland", this is likely the issue
```

**解决方案 / Solution:**
在登录屏幕，选择 "Ubuntu on Xorg" 而不是 "Ubuntu"
At login screen, select "Ubuntu on Xorg" instead of "Ubuntu"

---

### 2. 检查权限 / Check Permissions

**需要输入设备访问权限 / Need input device access:**

```bash
# 检查您所在的组 / Check your groups
groups

# 如果没有 'input' 组，添加它 / If no 'input' group, add it
sudo usermod -a -G input $USER

# 注销并重新登录以使更改生效 / Logout and login for changes to take effect
```

---

### 3. 检查 Python 和 pynput 权限 / Check Python and pynput Permissions

**验证 pynput 可以访问键盘 / Verify pynput can access keyboard:**

```bash
# 测试 pynput 是否工作 / Test if pynput works
python3 << 'EOF'
from pynput import keyboard
import time

def on_press(key):
    print(f"Key pressed: {key}")
    return False  # Stop listener after first key

print("Press any key...")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
EOF
```

如果这个测试失败，说明是系统级别的权限问题。
If this test fails, it's a system-level permission issue.

---

### 4. 检查安全策略 / Check Security Policies

**某些系统有额外的安全限制 / Some systems have additional security:**

```bash
# 检查 AppArmor 状态 / Check AppArmor status
sudo aa-status

# 检查 SELinux 状态 / Check SELinux status (if applicable)
getenforce
```

如果启用了 AppArmor 或 SELinux，可能需要配置策略。
If AppArmor or SELinux is enabled, you may need to configure policies.

---

### 5. 使用辅助功能 / Use Accessibility Features

**某些桌面环境需要启用辅助功能 / Some desktop environments require accessibility:**

#### GNOME:
```
设置 → 辅助功能 → 启用辅助功能
Settings → Universal Access → Enable accessibility features
```

#### KDE:
```
系统设置 → 辅助功能 → 启用屏幕阅读器
System Settings → Accessibility → Enable screen reader
```

---

## 🛠️ 解决方案 / Solutions

### 解决方案 1：使用 X11（推荐）/ Solution 1: Use X11 (Recommended)

**最可靠的解决方案 / Most reliable solution:**

1. 注销当前会话 / Logout from current session
2. 在登录屏幕，点击用户名 / At login screen, click your username
3. 点击右下角的齿轮图标 ⚙️ / Click gear icon in bottom right ⚙️
4. 选择 "Ubuntu on Xorg" / Select "Ubuntu on Xorg"
5. 输入密码并登录 / Enter password and login
6. 再次运行 LingoSnap / Run LingoSnap again

---

### 解决方案 2：配置 Wayland 权限 / Solution 2: Configure Wayland Permissions

**如果必须使用 Wayland / If you must use Wayland:**

某些 Wayland 合成器支持通过特殊权限实现全局快捷键：
Some Wayland compositors support global hotkeys with special permissions:

```bash
# For GNOME Wayland
# 安装 gnome-shell 扩展支持
sudo apt install gnome-shell-extensions

# 可能需要手动配置快捷键
# May need to manually configure shortcuts
```

**注意：** Wayland 设计上限制了全局键盘监听以提高安全性。
**Note:** Wayland is designed to restrict global keyboard listening for security.

---

### 解决方案 3：使用 sudo（临时测试）/ Solution 3: Use sudo (Temporary Test)

**仅用于测试，不推荐日常使用 / Only for testing, not recommended for daily use:**

```bash
# 测试是否是权限问题 / Test if it's a permission issue
sudo lingosnap

# 如果这样可以工作，说明是权限问题
# If this works, it's definitely a permission issue
```

**警告：** 不要长期以 root 运行应用程序！
**Warning:** Don't run applications as root long-term!

---

### 解决方案 4：替代方法 - 手动触发 / Solution 4: Alternative - Manual Trigger

**如果快捷键无法工作，使用 GUI 按钮 / If hotkeys can't work, use GUI buttons:**

1. **OCR 截图 / OCR Screenshot:**
   - 在文本翻译标签中，点击 "📷 OCR Screenshot" 按钮
   - In Text Translate tab, click "📷 OCR Screenshot" button
   
2. **文本翻译 / Text Translation:**
   - 直接在文本框中粘贴文本
   - Directly paste text in the text box

---

## 📋 系统兼容性 / System Compatibility

### ✅ 已知可用 / Known to Work:

- Ubuntu 20.04+ with X11
- Ubuntu 22.04+ with X11
- Pop!_OS with X11
- Linux Mint with X11

### ⚠️ 已知问题 / Known Issues:

- Ubuntu with Wayland (默认) - 需要切换到 X11
- Ubuntu with Wayland (default) - Need to switch to X11
- Fedora with Wayland - 相同限制
- Fedora with Wayland - Same restrictions

### ❓ 未测试 / Untested:

- Other Linux distributions
- BSD systems

---

## 🔧 高级调试 / Advanced Debugging

### 启用详细日志 / Enable Verbose Logging

```bash
# 运行并查看详细输出 / Run with verbose output
PYTHONUNBUFFERED=1 lingosnap 2>&1 | tee lingosnap.log

# 按快捷键，然后检查日志 / Press hotkeys, then check log
grep -i "key\|hotkey\|press" lingosnap.log
```

### 检查进程权限 / Check Process Permissions

```bash
# 找到 LingoSnap 进程 / Find LingoSnap process
ps aux | grep lingosnap

# 检查进程的能力 / Check process capabilities
cat /proc/$(pgrep -f lingosnap)/status | grep Cap
```

### 测试键盘访问 / Test Keyboard Access

```bash
# 使用 evtest 检查原始键盘事件 / Use evtest for raw keyboard events
sudo apt install evtest
sudo evtest
# 选择键盘设备并按键测试 / Select keyboard device and test keys
```

---

## 📞 获取帮助 / Getting Help

如果以上解决方案都不起作用，请在 GitHub Issues 中报告：
If none of the above works, please report on GitHub Issues:

**包含以下信息 / Include this information:**

1. **系统信息 / System info:**
   ```bash
   uname -a
   echo $XDG_SESSION_TYPE
   lsb_release -a
   ```

2. **Python 和包版本 / Python and package versions:**
   ```bash
   python3 --version
   pip3 show pynput PyQt6
   ```

3. **权限信息 / Permission info:**
   ```bash
   groups
   ls -la ~/.lingosnap/
   ```

4. **日志输出 / Log output:**
   ```bash
   lingosnap 2>&1 | head -50
   ```

---

## ✨ 临时解决方案 / Workaround

在快捷键问题解决之前，您可以：
Until hotkey issues are resolved, you can:

1. **使用 OCR 按钮** / **Use OCR button** 
   - 在文本翻译界面右下角 / Bottom right of Text Translate interface

2. **直接粘贴文本** / **Paste text directly**
   - 复制文本，粘贴到输入框 / Copy text, paste into input box

3. **使用终端命令** / **Use terminal command**
   - `lingo -t 1` 翻译终端输出 / Translate terminal output

---

**更新日期 / Last Updated:** 2025-11-20
**版本 / Version:** 0.1.0

这些是最全面的故障排除步骤。如果问题仍然存在，可能是您特定系统配置的独特问题。
These are the most comprehensive troubleshooting steps. If issues persist, it may be a unique issue with your specific system configuration.
