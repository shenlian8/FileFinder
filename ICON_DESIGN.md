# 3S Lab FileFinder 图标设计说明

## 设计概念
为"3S Lab"的FileFinder应用创建一个现代、专业的图标。

## 视觉元素
1. **主要图形**：放大镜（代表搜索功能）
2. **品牌元素**："3S"文字融入设计中
3. **颜色方案**：
   - 主色：渐变蓝色到紫色 (#4287f5 → #8a2be2)
   - 强调色：白色（用于放大镜和文字）
   - 背景：透明或圆角方形背景

## 具体设计
```
- 圆角方形背景（蓝紫渐变）
- 中心：白色放大镜图标
- 放大镜镜片内：白色"3S"文字（粗体）
- 放大镜手柄：斜向右下方
- 整体风格：扁平化、现代、科技感
```

## 推荐尺寸
- 256x256 像素（主图标）
- 支持多尺寸：16x16, 32x32, 48x48, 64x64, 128x128, 256x256

## 在线工具推荐
1. **Canva** (canva.com) - 免费，易用
2. **Favicon.io** - 快速生成图标
3. **IconArchive** - 图标资源库
4. **Figma** - 专业设计工具（免费版）

## 使用方法
创建好图标后：
1. 保存为 `icon.ico` 格式
2. 放在 FileFinder 目录下
3. 在 main.py 中添加以下代码（在 MainWindow.__init__ 中）：
   ```python
   import os
   icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
   if os.path.exists(icon_path):
       self.setWindowIcon(QIcon(icon_path))
   ```

## 临时方案
如果暂时没有图标文件，应用程序将使用系统默认图标，但窗口标题已更新为"FileFinder - 3S Lab"以体现品牌。
