# LingoSnap Hotkey and Package Installation Guide

## 快捷键和语言包安装指南 / Hotkey and Package Installation Guide

This guide addresses the features mentioned in the user feedback.

---

## 1. Argos Translate 语言包安装 / Argos Translate Package Installation

### 如何安装语言包 / How to Install Language Packages

**中文说明：**

1. 打开 LingoSnap 应用
2. 点击 **Settings（设置）** 标签
3. 在 "Translation Engine" 下拉框中选择 **"Argos Translate (Offline)"**
4. 在 "Argos Translate Settings" 区域，点击 **"Install Package"（安装语言包）** 按钮
5. 会弹出一个对话框，显示所有可用的语言包
6. 从列表中选择您需要的语言包，例如：
   - English → Chinese (英语到中文)
   - Chinese → English (中文到英语)
   - English → Spanish (英语到西班牙语)
   等等
7. 点击 **"OK"** 开始安装
8. 等待下载和安装完成（可能需要几分钟，取决于网络速度）
9. 安装完成后，该语言包将出现在 "Installed Language Packages" 列表中
10. 现在您可以使用该语言对进行离线翻译了！

**English Instructions:**

1. Open LingoSnap application
2. Click the **Settings** tab
3. In "Translation Engine" dropdown, select **"Argos Translate (Offline)"**
4. In "Argos Translate Settings" section, click **"Install Package"** button
5. A dialog will appear showing all available language packages
6. Select the language package you need from the list, such as:
   - English → Chinese
   - Chinese → English
   - English → Spanish
   etc.
7. Click **"OK"** to start installation
8. Wait for download and installation to complete (may take a few minutes depending on network speed)
9. After installation completes, the package will appear in "Installed Language Packages" list
10. You can now use that language pair for offline translation!

### 常见语言包 / Common Packages

- **英语 ↔ 中文 / English ↔ Chinese**
  - English → Chinese (Simplified)
  - Chinese → English

- **英语 ↔ 其他语言 / English ↔ Other Languages**
  - English → Spanish / Spanish → English
  - English → French / French → English
  - English → German / German → English
  - English → Japanese / Japanese → English
  - English → Korean / Korean → English
  - English → Russian / Russian → English

### 注意事项 / Notes

- 安装语言包需要互联网连接 / Internet connection required for installation
- 每个语言包大小约 20-100 MB / Each package is approximately 20-100 MB
- 安装后可离线使用 / Can be used offline after installation
- 语言包存储在 `~/.local/share/argos-translate/packages/` / Packages stored in `~/.local/share/argos-translate/packages/`

---

## 2. 快捷键功能 / Hotkey Functionality

### ⚠️ 重要更新 / Important Update (2025-11-20)

**中文：**
最新版本(commit 845b860)修复了快捷键监听器立即停止的问题。如果您看到：
```
Starting hotkey listener...
Hotkey listener stopped.
```

这个问题已经被修复。更新后，应用程序会：
- 自动检查快捷键监听器是否成功启动
- 如果启动失败，显示警告对话框并提供帮助信息
- 提供更详细的错误日志用于排查问题

如果快捷键仍然不工作，可能是权限问题（见下面的故障排除）。

**English:**
The latest version (commit 845b860) fixes the issue where hotkey listener stops immediately. If you see:
```
Starting hotkey listener...
Hotkey listener stopped.
```

This issue has been fixed. After updating, the application will:
- Automatically check if hotkey listener started successfully
- Show a warning dialog if startup fails with helpful information
- Provide more detailed error logs for troubleshooting

If hotkeys still don't work, it may be a permission issue (see troubleshooting below).

---

### 快捷键说明 / Hotkey Instructions

LingoSnap 提供两个全局快捷键 / LingoSnap provides two global hotkeys:

#### 2.1 文本捕获快捷键 / Text Capture Hotkey

**快捷键 / Shortcut:** `Ctrl + C + C`

**使用方法 / How to Use:**

中文：
1. 在任何应用程序中选中您想翻译的文本
2. **按住 Ctrl 键**
3. **快速按两次 C 键**（在 0.5 秒内）
4. LingoSnap 窗口会自动弹出，并显示选中的文本
5. 翻译会自动开始

English:
1. Select the text you want to translate in any application
2. **Hold down Ctrl key**
3. **Quickly press C key twice** (within 0.5 seconds)
4. LingoSnap window will automatically appear with the selected text
5. Translation will start automatically

**提示 / Tips:**
- 确保两次按 C 的间隔不超过 0.5 秒 / Ensure both C presses are within 0.5 seconds
- 第二次按 C 时不要松开 Ctrl / Keep holding Ctrl when pressing C the second time
- 如果没有反应，请使用下面的测试方法 / If not working, use the test method below

#### 2.2 OCR 截图快捷键 / OCR Screenshot Hotkey

**快捷键 / Shortcut:** `Ctrl + F8`

**使用方法 / How to Use:**

中文：
1. 按下 **Ctrl + F8**
2. 屏幕会变暗，出现一个十字光标
3. 点击并拖动鼠标，选择包含文本的区域
4. 松开鼠标，自动进行 OCR 识别
5. 识别出的文本会在 LingoSnap 窗口中显示并翻译
6. 按 **ESC** 可以取消截图

English:
1. Press **Ctrl + F8**
2. Screen will darken with a crosshair cursor
3. Click and drag to select the area containing text
4. Release mouse to automatically perform OCR
5. Recognized text will appear in LingoSnap window and be translated
6. Press **ESC** to cancel screenshot

### 测试快捷键 / Testing Hotkeys

**中文：**

如果快捷键不工作，请按照以下步骤测试：

1. 打开 LingoSnap
2. 进入 **Settings（设置）** 标签
3. 找到 "Hotkey Settings" 区域
4. 点击 **"Test Hotkeys"（测试快捷键）** 按钮
5. 按照弹出对话框中的说明测试快捷键
6. 查看状态信息，确认快捷键监听器是否正在运行

**English:**

If hotkeys are not working, follow these steps to test:

1. Open LingoSnap
2. Go to **Settings** tab
3. Find "Hotkey Settings" section
4. Click **"Test Hotkeys"** button
5. Follow the instructions in the dialog to test hotkeys
6. Check status information to confirm hotkey listener is running

### 快捷键故障排除 / Hotkey Troubleshooting

**问题 / Issue:** 快捷键监听器立即停止 / Hotkey listener stops immediately

**症状 / Symptoms:**
```
Hotkey manager started successfully
Starting hotkey listener...
Hotkey listener stopped.
```

**解决方法 / Solution:**

**中文：**
这个问题在最新版本（commit 845b860）中已经修复。如果您遇到此问题：

1. **更新代码**：
   ```bash
   git pull origin copilot/complete-project-requirements
   pip install -e .
   ```

2. **Linux 权限问题**：
   如果更新后仍有问题，可能需要输入设备权限：
   ```bash
   # 将用户添加到 input 组
   sudo usermod -a -G input $USER
   # 注销并重新登录以使更改生效
   ```

3. **检查显示服务器**：
   ```bash
   # 检查是否使用 Wayland
   echo $XDG_SESSION_TYPE
   
   # 如果是 Wayland，尝试切换到 X11
   # 在登录屏幕选择 "Ubuntu on Xorg"
   ```

4. **启用辅助功能**（某些桌面环境需要）：
   - GNOME: 设置 → 辅助功能 → 启用辅助功能
   - KDE: 系统设置 → 辅助功能

**English:**
This issue has been fixed in the latest version (commit 845b860). If you encounter this:

1. **Update the code**:
   ```bash
   git pull origin copilot/complete-project-requirements
   pip install -e .
   ```

2. **Linux permission issues**:
   If still having issues after update, you may need input device permissions:
   ```bash
   # Add user to input group
   sudo usermod -a -G input $USER
   # Logout and login again for changes to take effect
   ```

3. **Check display server**:
   ```bash
   # Check if using Wayland
   echo $XDG_SESSION_TYPE
   
   # If Wayland, try switching to X11
   # Select "Ubuntu on Xorg" at login screen
   ```

4. **Enable accessibility** (required on some desktop environments):
   - GNOME: Settings → Universal Access → Enable accessibility
   - KDE: System Settings → Accessibility

---

**问题 / Issue:** 快捷键无响应 / Hotkeys not responding

**解决方法 / Solutions:**

中文：
1. **检查权限**：在 Linux 上，快捷键可能需要适当的权限
   - 尝试从终端运行：`lingosnap`
   - 查看终端输出的调试信息

2. **检查监听器状态**：
   - 在 Settings 中点击 "Test Hotkeys"
   - 确认监听器状态显示为 "✓ Hotkey listener is running"

3. **检查快捷键冲突**：
   - 确保其他应用程序没有使用相同的快捷键
   - Ubuntu 系统设置中检查全局快捷键

4. **重启应用**：
   - 完全退出 LingoSnap（右键系统托盘图标 → Quit）
   - 重新启动应用

5. **查看日志**：
   - 从终端运行 `lingosnap` 查看调试信息
   - 日志会显示 "DEBUG: Ctrl+C+C detected" 等信息

English:
1. **Check Permissions**: On Linux, hotkeys may require appropriate permissions
   - Try running from terminal: `lingosnap`
   - Check debug output in terminal

2. **Check Listener Status**:
   - Click "Test Hotkeys" in Settings
   - Confirm listener status shows "✓ Hotkey listener is running"

3. **Check Hotkey Conflicts**:
   - Ensure no other applications use the same hotkeys
   - Check global hotkeys in Ubuntu system settings

4. **Restart Application**:
   - Completely quit LingoSnap (right-click tray icon → Quit)
   - Restart the application

5. **View Logs**:
   - Run `lingosnap` from terminal to see debug info
   - Logs will show "DEBUG: Ctrl+C+C detected" messages

### 调试模式 / Debug Mode

**中文：**

从终端运行可以看到详细的调试信息：

```bash
lingosnap 2>&1 | grep -E "(DEBUG|ERROR|Starting|Hotkey)"
```

您应该看到类似这样的输出：
- `Starting hotkey listener...`
- `Hotkey manager started successfully`
- `DEBUG: Ctrl+C+C detected, triggering text capture`
- `DEBUG: Ctrl+F8 detected, triggering OCR capture`

**English:**

Run from terminal to see detailed debug information:

```bash
lingosnap 2>&1 | grep -E "(DEBUG|ERROR|Starting|Hotkey)"
```

You should see output like:
- `Starting hotkey listener...`
- `Hotkey manager started successfully`
- `DEBUG: Ctrl+C+C detected, triggering text capture`
- `DEBUG: Ctrl+F8 detected, triggering OCR capture`

---

## 3. 系统要求 / System Requirements

### Linux 权限 / Linux Permissions

**中文：**
- 快捷键监听需要 X11 输入权限
- 某些系统可能需要将用户添加到 `input` 组
- 如果遇到权限问题，请参考系统文档

**English:**
- Hotkey listening requires X11 input permissions
- Some systems may require adding user to `input` group
- Refer to system documentation if permission issues occur

### 依赖项 / Dependencies

确保已安装以下依赖项 / Ensure these dependencies are installed:

```bash
# Python 依赖 / Python dependencies
pip install -r requirements.txt

# 系统依赖 / System dependencies  
sudo apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim
```

---

## 4. 常见问题 / FAQ

**Q1: 为什么我看不到 "Install Package" 按钮？**
**A1:** 确保您已选择 "Argos Translate (Offline)" 作为翻译引擎。该按钮只在 Argos 设置区域显示。

**Q2: Why can't I see the "Install Package" button?**
**A2:** Make sure you've selected "Argos Translate (Offline)" as the translation engine. The button only appears in the Argos settings section.

---

**Q3: 快捷键完全不工作怎么办？**
**A3:** 
1. 从终端运行 `lingosnap` 查看错误信息
2. 检查是否有其他程序占用了相同的快捷键
3. 尝试重启应用程序
4. 如果问题持续，请在 GitHub 上报告问题，并附上终端输出

**Q3: What if hotkeys don't work at all?**
**A3:**
1. Run `lingosnap` from terminal to see error messages
2. Check if other programs are using the same hotkeys
3. Try restarting the application
4. If problem persists, report on GitHub with terminal output

---

**Q4: 语言包安装失败怎么办？**
**A4:** 
1. 检查网络连接
2. 确保有足够的磁盘空间（每个包约 20-100 MB）
3. 尝试刷新包列表后重试
4. 检查 `~/.local/share/argos-translate/` 目录的写权限

**Q4: What if package installation fails?**
**A4:**
1. Check internet connection
2. Ensure sufficient disk space (each package ~20-100 MB)
3. Try refreshing package list and retry
4. Check write permissions for `~/.local/share/argos-translate/`

---

## 5. 获取帮助 / Getting Help

**中文：**
- GitHub Issues: https://github.com/The-Eleven11/LingoSnap/issues
- 提交问题时请包含：
  - 操作系统版本
  - LingoSnap 版本
  - 终端输出的错误信息
  - 重现问题的步骤

**English:**
- GitHub Issues: https://github.com/The-Eleven11/LingoSnap/issues
- When submitting issues, please include:
  - Operating system version
  - LingoSnap version
  - Error messages from terminal
  - Steps to reproduce the problem

---

**更新日期 / Last Updated:** 2025-11-20
**版本 / Version:** 0.1.0
