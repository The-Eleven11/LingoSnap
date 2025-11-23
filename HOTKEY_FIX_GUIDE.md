# LingoSnap 快捷键修复指南 / Hotkey Fix Guide

## 问题描述 / Problem Description

**中文**: 全局快捷键（Ctrl+C+C 和 Ctrl+F8）无法唤醒程序或触发功能。
**English**: Global hotkeys (Ctrl+C+C and Ctrl+F8) cannot wake up the program or trigger functions.

## 根本原因 / Root Cause

全局快捷键在 Linux 上依赖于底层系统权限和显示服务器配置。主要限制包括：
Global hotkeys on Linux depend on underlying system permissions and display server configuration. Main limitations include:

1. **Wayland 安全限制** / **Wayland Security Restrictions**
   - Wayland 默认禁止应用程序监听全局键盘事件（安全特性）
   - Wayland blocks apps from monitoring global keyboard events by default (security feature)

2. **权限不足** / **Insufficient Permissions**
   - 用户可能不在 `input` 组中，无法访问输入设备
   - User may not be in `input` group, cannot access input devices

3. **桌面环境限制** / **Desktop Environment Restrictions**
   - 某些桌面环境（GNOME、KDE等）对全局快捷键有额外限制
   - Some desktop environments (GNOME, KDE, etc.) have additional restrictions on global hotkeys

## 解决方案 / Solutions

### 方案 1: 使用 GUI 按钮（推荐，无需配置）/ Solution 1: Use GUI Button (Recommended, No Configuration)

✅ **最简单的解决方法 / Easiest Solution:**

1. 打开 LingoSnap 应用程序
2. Open LingoSnap application

3. 在"文本翻译"标签页，点击右下角的 "📷 OCR Screenshot" 按钮
4. In "Text Translate" tab, click "📷 OCR Screenshot" button at bottom right

5. 选择屏幕区域进行 OCR 识别
6. Select screen region for OCR recognition

**优点 / Advantages:**
- ✅ 无需任何系统配置 / No system configuration needed
- ✅ 在所有桌面环境和显示服务器上工作 / Works on all desktop environments and display servers
- ✅ 使用系统截图工具，完全兼容 / Uses system screenshot tools, fully compatible

### 方案 2: 切换到 X11 显示服务器 / Solution 2: Switch to X11 Display Server

如果您在使用 Wayland 并且想要使用快捷键：
If you're using Wayland and want to use hotkeys:

1. **注销当前会话** / **Logout current session**
   ```bash
   # 点击用户菜单 → 注销
   # Click user menu → Logout
   ```

2. **在登录屏幕选择 X11** / **Select X11 at login screen**
   - 点击您的用户名 / Click your username
   - 点击右下角齿轮图标 ⚙️ / Click gear icon ⚙️ in bottom right
   - 选择 "Ubuntu on Xorg" 或 "GNOME on Xorg" / Select "Ubuntu on Xorg" or "GNOME on Xorg"
   - 输入密码登录 / Enter password and login

3. **重新启动 LingoSnap** / **Restart LingoSnap**
   ```bash
   lingosnap
   ```

4. **测试快捷键** / **Test hotkeys**
   - Ctrl+C+C: 文本捕获 / Text capture
   - Ctrl+F8: OCR 截图 / OCR screenshot

### 方案 3: 添加用户到 input 组 / Solution 3: Add User to input Group

在 X11 下如果快捷键仍不工作，可能需要权限：
On X11, if hotkeys still don't work, you may need permissions:

```bash
# 添加用户到 input 组 / Add user to input group
sudo usermod -a -G input $USER

# 注销并重新登录使更改生效 / Logout and login for changes to take effect
```

**验证权限 / Verify permissions:**
```bash
# 检查用户组 / Check user groups
groups $USER

# 应该看到 'input' 在列表中 / Should see 'input' in the list
```

### 方案 4: 启用辅助功能（某些桌面环境）/ Solution 4: Enable Accessibility (Some Desktop Environments)

某些桌面环境需要启用辅助功能才能使用全局快捷键：
Some desktop environments require accessibility to be enabled for global hotkeys:

**GNOME:**
1. 打开设置 → 辅助功能 / Settings → Accessibility
2. 启用"辅助功能" / Enable "Accessibility"
3. 重启 LingoSnap / Restart LingoSnap

**KDE Plasma:**
1. 系统设置 → 辅助功能 / System Settings → Accessibility
2. 启用屏幕阅读器或其他辅助功能 / Enable screen reader or other accessibility features

## 诊断工具 / Diagnostic Tools

### 检查显示服务器 / Check Display Server
```bash
echo $XDG_SESSION_TYPE
# 输出 'wayland' 或 'x11' / Output: 'wayland' or 'x11'
```

### 检查 pynput 是否工作 / Check if pynput Works
```bash
python3 -c "
from pynput import keyboard
import time

def on_press(key):
    print(f'Key detected: {key}')

listener = keyboard.Listener(on_press=on_press)
listener.start()
print('Press any key (Ctrl+C to exit)...')
time.sleep(10)
listener.stop()
"
```

### 检查 LingoSnap 日志 / Check LingoSnap Logs
```bash
# 从终端运行以查看调试输出 / Run from terminal to see debug output
lingosnap
```

查找以下消息 / Look for these messages:
- ✅ "Hotkey listener started successfully" = 工作正常 / Working
- ❌ "Failed to start hotkey listener" = 需要修复 / Needs fix
- ⚠️ "pynput method failed" = 使用 GUI 按钮替代 / Use GUI button instead

## 常见问题 / FAQ

### Q: 为什么 Ubuntu 22.04+ 默认不支持全局快捷键？
### Q: Why doesn't Ubuntu 22.04+ support global hotkeys by default?

**A**: Ubuntu 22.04+ 默认使用 Wayland 显示服务器。Wayland 出于安全考虑禁止应用程序监听全局键盘事件，防止键盘记录器。这是设计决定，不是 LingoSnap 的错误。

**A**: Ubuntu 22.04+ uses Wayland display server by default. Wayland blocks apps from monitoring global keyboard events for security (prevents keyloggers). This is a design decision, not a LingoSnap bug.

### Q: GUI 按钮和快捷键有什么区别？
### Q: What's the difference between GUI button and hotkeys?

**A**: 
- **GUI 按钮**: 需要手动点击，但始终有效，无配置要求
- **快捷键**: 可以在任何时候触发，但需要系统配置和权限

**A**:
- **GUI Button**: Requires manual click, but always works, no configuration needed
- **Hotkeys**: Can be triggered anytime, but requires system configuration and permissions

### Q: 我可以自定义快捷键吗？
### Q: Can I customize the hotkeys?

**A**: 当前版本使用固定快捷键（Ctrl+C+C 和 Ctrl+F8）。未来版本可能会添加自定义选项。同时，您可以修改 `hotkey_manager.py` 中的代码来更改快捷键。

**A**: Current version uses fixed hotkeys (Ctrl+C+C and Ctrl+F8). Future versions may add customization. Meanwhile, you can modify the code in `hotkey_manager.py` to change hotkeys.

### Q: 为什么 Ctrl+C+C 不工作但 Ctrl+F8 工作？
### Q: Why does Ctrl+C+C not work but Ctrl+F8 works?

**A**: Ctrl+C+C 需要检测双击 C 键，时序更复杂。确保：
1. 按住 Ctrl 键
2. 快速按 C 两次（500ms 内）
3. 不要同时按其他键

**A**: Ctrl+C+C needs to detect double-tap of C key, timing is more complex. Ensure:
1. Hold Ctrl key
2. Quickly press C twice (within 500ms)
3. Don't press other keys simultaneously

## 推荐工作流程 / Recommended Workflow

✅ **最佳实践 / Best Practice:**

1. **主要使用 GUI 按钮进行 OCR** / **Primarily use GUI button for OCR**
   - 点击 "📷 OCR Screenshot" 按钮
   - Click "📷 OCR Screenshot" button
   - 选择区域
   - Select region
   - 自动识别和翻译
   - Auto-recognize and translate

2. **文本翻译直接使用剪贴板** / **Use clipboard directly for text translation**
   - 选择文本并复制（Ctrl+C）
   - Select text and copy (Ctrl+C)
   - 切换到 LingoSnap 窗口
   - Switch to LingoSnap window
   - 粘贴到输入框（Ctrl+V）
   - Paste to input box (Ctrl+V)

3. **只在 X11 环境使用快捷键** / **Use hotkeys only on X11**
   - 如果您经常使用快捷键，切换到 X11
   - If you use hotkeys frequently, switch to X11
   - 按照上面的方案 2 操作
   - Follow Solution 2 above

## 技术细节 / Technical Details

### pynput 库的限制 / pynput Library Limitations

`pynput` 是用于全局键盘/鼠标监听的 Python 库。其限制：
`pynput` is a Python library for global keyboard/mouse listening. Its limitations:

1. **在 Wayland 上不工作** / **Doesn't work on Wayland**
   - Wayland 协议不允许应用程序访问全局输入事件
   - Wayland protocol doesn't allow apps to access global input events

2. **需要 X11 权限** / **Requires X11 permissions**
   - 在 X11 上，需要 `input` 组成员资格或 root 权限
   - On X11, requires `input` group membership or root privileges

3. **桌面环境兼容性** / **Desktop Environment Compatibility**
   - 某些桌面环境（如启用了安全功能的 GNOME）可能阻止或限制
   - Some desktop environments (like GNOME with security features) may block or restrict

### 替代方案（未来）/ Alternative Solutions (Future)

未来版本可能考虑的替代实现：
Alternative implementations that may be considered in future versions:

1. **D-Bus 全局快捷键** / **D-Bus Global Shortcuts**
   - 使用桌面环境的快捷键 API
   - Use desktop environment's shortcut API
   - 更好的兼容性，但实现复杂
   - Better compatibility but complex implementation

2. **XGrabKey (X11)** / **XGrabKey (X11)**
   - 直接使用 X11 API
   - Use X11 API directly
   - 仅适用于 X11
   - Only for X11

3. **系统快捷键注册** / **System Shortcut Registration**
   - 注册到桌面环境
   - Register with desktop environment
   - 需要用户手动配置
   - Requires manual user configuration

## 总结 / Summary

**简单使用（推荐）** / **Simple Usage (Recommended):**
- ✅ 使用 GUI 中的 "📷 OCR Screenshot" 按钮
- ✅ Use "📷 OCR Screenshot" button in GUI
- 无需任何配置，在所有环境下工作
- No configuration needed, works in all environments

**高级用户（需要快捷键）** / **Advanced Users (Need Hotkeys):**
1. 切换到 X11 显示服务器
2. Switch to X11 display server
3. 添加用户到 input 组
4. Add user to input group
5. 重启 LingoSnap
6. Restart LingoSnap

**遇到问题？** / **Having Issues?**
- 查看终端输出诊断消息
- Check terminal output for diagnostic messages
- 使用 GUI 按钮作为可靠的替代方案
- Use GUI button as reliable alternative
- 查阅 HOTKEY_TROUBLESHOOTING.md 获取更多详情
- Refer to HOTKEY_TROUBLESHOOTING.md for more details
