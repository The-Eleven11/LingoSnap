# LingoSnap 兼容性指南 / Compatibility Guide

## 为什么程序只能在 Xorg 上运行？/ Why Does the Program Only Run on Xorg?

### 问题根源 / Root Cause

LingoSnap 依赖 PyQt6 和相关的 Qt 库。Qt 需要特定的平台插件才能在不同的显示服务器上运行：

LingoSnap relies on PyQt6 and related Qt libraries. Qt requires specific platform plugins to run on different display servers:

- **Xorg (X11)**: 使用 `xcb` 插件 / Uses `xcb` plugin
- **Wayland**: 使用 `wayland` 插件 / Uses `wayland` plugin

### 常见错误 / Common Errors

#### 1. Missing xcb-cursor Library

```
qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed
qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
```

**解决方案 / Solution:**

```bash
# Ubuntu/Debian
sudo apt install libxcb-cursor0

# 或安装完整的 XCB 依赖 / Or install full XCB dependencies
sudo apt install libxcb-cursor0 libxcb-xinerama0 libxcb-icccm4 \
                 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
                 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0
```

#### 2. Platform Plugin Not Available

```
This application failed to start because no Qt platform plugin could be initialized
```

**解决方案 / Solutions:**

**方案 1: 安装缺失的依赖 / Install Missing Dependencies**

```bash
# 安装 PyQt6 和所有依赖 / Install PyQt6 and all dependencies
sudo apt install python3-pyqt6 python3-pyqt6.qtwidgets

# 或使用 pip 重新安装 / Or reinstall with pip
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6
```

**方案 2: 切换到 Xorg / Switch to Xorg**

1. 注销当前会话 / Logout from current session
2. 在登录屏幕，点击用户名 / At login screen, click your username
3. 点击右下角的齿轮图标 ⚙️ / Click gear icon ⚙️ in bottom right
4. 选择 "Ubuntu on Xorg" / Select "Ubuntu on Xorg"
5. 输入密码登录 / Enter password and login

**方案 3: 设置环境变量 / Set Environment Variables**

```bash
# 如果在 Wayland 上运行 / If running on Wayland
export QT_QPA_PLATFORM=wayland

# 如果在 Xorg 上运行 / If running on Xorg
export QT_QPA_PLATFORM=xcb

# 然后运行 LingoSnap / Then run LingoSnap
lingosnap
```

## OCR 识别超时问题 / OCR Recognition Timeout Issues

### 问题描述 / Problem Description

OCR 有时候会超时或花费很长时间识别文本。
OCR sometimes times out or takes a very long time to recognize text.

### 原因分析 / Cause Analysis

1. **图像质量问题 / Image Quality**: 模糊、低分辨率或复杂的图像需要更长时间处理
2. **语言数据包 / Language Data**: 某些语言的数据包可能需要更多处理时间
3. **系统资源 / System Resources**: CPU 负载高或内存不足会影响性能
4. **Tesseract 配置 / Tesseract Config**: 默认配置可能不是最优的

### 解决方案 / Solutions

#### 1. 优化的 OCR 配置（已实现）/ Optimized OCR Config (Implemented)

LingoSnap 现在使用优化的 Tesseract 配置：
LingoSnap now uses optimized Tesseract configuration:

- **PSM 3**: 全自动页面分割（适合大多数情况）
- **PSM 3**: Fully automatic page segmentation (good for most cases)
- **OEM 3**: 默认 OCR 引擎模式（使用最佳可用引擎）
- **OEM 3**: Default OCR Engine Mode (uses best available)
- **30 秒超时**: 防止无限期挂起
- **30 second timeout**: Prevents indefinite hanging

#### 2. 提高截图质量 / Improve Screenshot Quality

**建议 / Recommendations:**

- 选择清晰、高对比度的文本区域
- Select clear, high-contrast text areas
- 避免选择过大的区域（减少处理时间）
- Avoid selecting very large areas (reduces processing time)
- 确保文本大小合适（不要太小）
- Ensure text size is reasonable (not too small)

#### 3. 使用正确的语言包 / Use Correct Language Pack

```bash
# 查看已安装的语言包 / Check installed language packs
tesseract --list-langs

# 安装额外的语言包 / Install additional language packs
# 中文简体 / Simplified Chinese
sudo apt install tesseract-ocr-chi-sim

# 中文繁体 / Traditional Chinese
sudo apt install tesseract-ocr-chi-tra

# 英语（通常已安装）/ English (usually pre-installed)
sudo apt install tesseract-ocr-eng
```

#### 4. 监控 OCR 性能 / Monitor OCR Performance

如果 OCR 经常超时：
If OCR frequently times out:

```bash
# 检查 Tesseract 版本 / Check Tesseract version
tesseract --version

# 测试 Tesseract 性能 / Test Tesseract performance
tesseract test.png stdout

# 检查系统资源 / Check system resources
top
htop
```

## 提高整体兼容性的建议 / Recommendations for Better Compatibility

### 1. 系统要求 / System Requirements

**推荐配置 / Recommended:**
- Ubuntu 22.04 LTS 或更新版本 / or newer
- Xorg 显示服务器（不是 Wayland）/ display server (not Wayland)
- Python 3.10+ 
- 2GB+ RAM
- 现代 CPU（支持 SSE4.2）/ Modern CPU (SSE4.2 support)

**最小配置 / Minimum:**
- Ubuntu 20.04 LTS
- Python 3.8+
- 1GB RAM
- 任何 x86_64 CPU / Any x86_64 CPU

### 2. 依赖检查清单 / Dependency Checklist

安装前检查：
Before installation, check:

```bash
# Python 版本 / Python version
python3 --version  # Should be 3.8+

# Tesseract OCR
tesseract --version  # Should be 4.0+

# Qt 库 / Qt libraries
dpkg -l | grep libxcb  # Should show xcb libraries

# 截图工具（至少一个）/ Screenshot tool (at least one)
which flameshot gnome-screenshot spectacle import scrot
```

### 3. 完整安装脚本 / Complete Installation Script

```bash
#!/bin/bash

# 更新包列表 / Update package list
sudo apt update

# 安装系统依赖 / Install system dependencies
sudo apt install -y \
    python3 python3-pip python3-venv \
    tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim \
    libxcb-cursor0 libxcb-xinerama0 libxcb-icccm4 \
    libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
    libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 \
    flameshot

# 克隆仓库 / Clone repository
cd ~/Documents
git clone https://github.com/The-Eleven11/LingoSnap.git
cd LingoSnap

# 创建虚拟环境 / Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 安装 Python 依赖 / Install Python dependencies
pip install -r requirements.txt
pip install -e .

# 测试安装 / Test installation
lingosnap --version || echo "Installation complete! Run 'lingosnap' to start."
```

### 4. 桌面环境特定注意事项 / Desktop Environment Specific Notes

#### GNOME (Ubuntu 默认 / Default)

- ✅ 完全支持 Xorg / Full support on Xorg
- ⚠️ Wayland 上有限支持（截图和快捷键受限）/ Limited on Wayland (screenshot and hotkeys restricted)
- 推荐：切换到 Xorg / Recommended: Switch to Xorg

#### KDE Plasma

- ✅ 完全支持 Xorg 和 Wayland / Full support on both Xorg and Wayland
- ✅ 内置 Spectacle 截图工具 / Built-in Spectacle screenshot tool
- 建议：安装 flameshot 以获得更好的体验 / Suggestion: Install flameshot for better experience

#### XFCE

- ✅ 完全支持（只用 Xorg）/ Full support (Xorg only)
- ✅ 轻量级，性能好 / Lightweight, good performance
- 建议：安装 flameshot 或 scrot / Suggestion: Install flameshot or scrot

#### LXDE/LXQt

- ✅ 完全支持 / Full support
- ✅ 资源占用少 / Low resource usage
- 建议：安装 scrot（最轻量）/ Suggestion: Install scrot (lightest)

## 故障排除 / Troubleshooting

### 诊断工具 / Diagnostic Tools

```bash
# 检查当前显示服务器 / Check current display server
echo $XDG_SESSION_TYPE

# 检查 Qt 平台插件 / Check Qt platform plugins
ls /usr/lib/x86_64-linux-gnu/qt6/plugins/platforms/

# 列出可用的 Qt 平台 / List available Qt platforms
QT_DEBUG_PLUGINS=1 python3 -c "from PyQt6.QtWidgets import QApplication; import sys; app = QApplication(sys.argv)"

# 测试 OCR / Test OCR
python3 -c "import pytesseract; print(pytesseract.get_tesseract_version())"

# 检查依赖 / Check dependencies
pip list | grep -E "PyQt6|pytesseract|Pillow"
```

### 常见问题解答 / FAQ

**Q: 为什么 Wayland 上功能受限？**
**Q: Why is functionality limited on Wayland?**

A: Wayland 出于安全考虑限制应用的屏幕捕获和全局键盘监听权限。LingoSnap 使用系统截图工具作为替代方案，但全局快捷键在 Wayland 上无法工作。
A: Wayland restricts screen capture and global keyboard monitoring for security. LingoSnap uses system screenshot tools as a workaround, but global hotkeys don't work on Wayland.

**Q: 如何判断我在用 Xorg 还是 Wayland？**
**Q: How do I tell if I'm using Xorg or Wayland?**

A: 运行 `echo $XDG_SESSION_TYPE`。输出 `x11` 表示 Xorg，`wayland` 表示 Wayland。
A: Run `echo $XDG_SESSION_TYPE`. Output `x11` means Xorg, `wayland` means Wayland.

**Q: OCR 识别速度慢怎么办？**
**Q: What to do about slow OCR recognition?**

A: 
1. 选择较小的截图区域 / Select smaller screenshot areas
2. 确保文本清晰可读 / Ensure text is clear and readable
3. 关闭其他占用 CPU 的程序 / Close other CPU-intensive programs
4. 考虑升级硬件（更快的 CPU）/ Consider hardware upgrade (faster CPU)

**Q: 能否支持其他显示服务器（如 Mir）？**
**Q: Can other display servers (like Mir) be supported?**

A: LingoSnap 依赖 Qt6 的平台支持。目前主要支持 Xorg 和 Wayland。其他显示服务器的支持取决于 Qt6 是否提供相应的插件。
A: LingoSnap depends on Qt6 platform support. Currently mainly supports Xorg and Wayland. Support for other display servers depends on whether Qt6 provides corresponding plugins.

## 获取帮助 / Getting Help

如果以上方法都无法解决问题，请：
If the above methods don't solve the problem, please:

1. 收集诊断信息 / Collect diagnostic information:
```bash
# 创建诊断报告 / Create diagnostic report
cat > lingosnap-diagnostic.txt << EOF
System Info:
$(uname -a)

Display Server:
$(echo $XDG_SESSION_TYPE)

Desktop Environment:
$(echo $XDG_CURRENT_DESKTOP)

Python Version:
$(python3 --version)

PyQt6 Version:
$(pip show PyQt6 | grep Version)

Tesseract Version:
$(tesseract --version 2>&1 | head -1)

Qt Platform Plugins:
$(ls /usr/lib/x86_64-linux-gnu/qt6/plugins/platforms/ 2>/dev/null || echo "Not found")

XCB Libraries:
$(dpkg -l | grep libxcb)

Screenshot Tools:
$(which flameshot gnome-screenshot spectacle import scrot 2>/dev/null || echo "None found")

Environment:
QT_QPA_PLATFORM=$QT_QPA_PLATFORM
XDG_SESSION_TYPE=$XDG_SESSION_TYPE
XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP
EOF

cat lingosnap-diagnostic.txt
```

2. 在 GitHub 上创建 Issue / Create an Issue on GitHub:
   - 附上诊断报告 / Attach diagnostic report
   - 描述具体问题 / Describe the specific problem
   - 包含错误消息 / Include error messages

3. 查阅文档 / Check documentation:
   - INSTALLATION.md
   - USAGE.md
   - HOTKEY_FIX_GUIDE.md

## 如何正确使用 Flameshot / How to Use Flameshot Correctly

### 问题：Timeout waiting for screenshot

如果您看到 "Timeout waiting for screenshot" 错误，这通常意味着 flameshot 正在等待您完成截图操作。

If you see "Timeout waiting for screenshot" error, it usually means flameshot is waiting for you to complete the screenshot operation.

### Flameshot 使用步骤 / Flameshot Usage Steps

1. **点击 OCR 按钮 / Click OCR Button**
   - 在 LingoSnap 文本翻译标签中点击 "📷 OCR Screenshot" 按钮
   - Click "📷 OCR Screenshot" button in LingoSnap Text Translate tab

2. **Flameshot 界面出现 / Flameshot Interface Appears**
   - 屏幕会显示 flameshot 的截图界面
   - Screen will show flameshot screenshot interface
   - 鼠标指针变成十字光标
   - Mouse cursor becomes crosshair

3. **选择区域 / Select Region**
   - 点击并拖动鼠标选择要识别的文本区域
   - Click and drag to select the text region you want to recognize
   - 选择清晰、对比度高的文本
   - Select clear, high-contrast text

4. **⭐ 重要：确认选择 / Important: Confirm Selection ⭐**
   
   **这是最关键的步骤！/ This is the most critical step!**
   
   选择区域后，您必须确认：
   After selecting the region, you MUST confirm:
   
   - **点击绿色的勾号 ✓ / Click the green checkmark ✓**
   - **或按 Enter 键 / Or press Enter key**
   - **或双击选择区域 / Or double-click the selected region**
   
   如果您：
   If you:
   - 按 ESC = 取消截图 / Press ESC = Cancel screenshot
   - 关闭 flameshot = 取消截图 / Close flameshot = Cancel screenshot
   - 什么都不做 = 超时（2分钟）/ Do nothing = Timeout (2 minutes)

5. **LingoSnap 自动处理 / LingoSnap Auto-processes**
   - 确认后，LingoSnap 自动加载截图
   - After confirmation, LingoSnap automatically loads the screenshot
   - OCR 识别文本
   - OCR recognizes text
   - 自动翻译
   - Automatic translation

### 常见问题 / Common Issues

**Q: 为什么一直显示 "Timeout waiting for screenshot"？**

A: 您可能忘记点击确认按钮（✓）或按 Enter。选择区域后必须确认！

**Q: Why does it keep showing "Timeout waiting for screenshot"?**

A: You may have forgotten to click the confirmation button (✓) or press Enter. You MUST confirm after selecting the region!

---

**Q: 我按了 ESC，现在什么都没发生？**

A: 按 ESC 会取消截图。重新点击 OCR 按钮再试一次。

**Q: I pressed ESC, now nothing happens?**

A: Pressing ESC cancels the screenshot. Click the OCR button again to retry.

---

**Q: Flameshot 太慢了，有更快的方法吗？**

A: 试试其他截图工具：
- gnome-screenshot (Ubuntu 自带)
- import (ImageMagick)
- scrot (轻量级)

**Q: Flameshot is too slow, is there a faster way?**

A: Try other screenshot tools:
- gnome-screenshot (pre-installed on Ubuntu)
- import (ImageMagick)
- scrot (lightweight)

安装替代工具：
Install alternative tools:
```bash
sudo apt install gnome-screenshot imagemagick scrot
```

### 提示 / Tips

1. **选择合适大小的区域 / Select Appropriately Sized Regions**
   - 不要选择整个屏幕 / Don't select entire screen
   - 只选择需要翻译的文本 / Only select text you need to translate
   - 清晰的文本识别更快 / Clear text recognizes faster

2. **确保文本清晰 / Ensure Text is Clear**
   - 文本大小适中 / Moderate text size
   - 高对比度（黑字白底最佳）/ High contrast (black on white is best)
   - 避免模糊或扭曲的文本 / Avoid blurry or distorted text

3. **使用快捷键 / Use Shortcuts**
   - Enter = 确认 / Confirm
   - ESC = 取消 / Cancel
   - 双击 = 快速确认 / Double-click = Quick confirm

4. **耐心等待 / Be Patient**
   - LingoSnap 会等待最多 2 分钟 / LingoSnap waits up to 2 minutes
   - 每 10 秒显示一次进度 / Progress shown every 10 seconds
   - 看到 "Still waiting..." 是正常的 / Seeing "Still waiting..." is normal

## 总结 / Summary

**最佳实践 / Best Practices:**

1. ✅ 使用 Xorg 而不是 Wayland / Use Xorg instead of Wayland
2. ✅ 安装完整的 XCB 依赖 / Install complete XCB dependencies
3. ✅ 安装推荐的截图工具（flameshot）/ Install recommended screenshot tool (flameshot)
4. ✅ 使用 GUI OCR 按钮而不是快捷键 / Use GUI OCR button instead of hotkeys
5. ✅ 选择清晰、适中大小的截图区域 / Select clear, moderately-sized screenshot areas
6. ✅ 保持系统和依赖更新 / Keep system and dependencies updated

遵循这些建议可以确保 LingoSnap 在您的系统上获得最佳性能和兼容性。
Following these recommendations ensures LingoSnap achieves optimal performance and compatibility on your system.
