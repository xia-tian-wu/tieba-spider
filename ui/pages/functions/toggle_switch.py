from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Signal, Qt, QRect, QPoint, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFontMetrics

class ToggleSwitch(QWidget):
    toggled = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 22)
        self._checked = False
        self._offset = 0  # 私有变量，存储offset的实际值
        
        # 直接使用注册后的"offset"属性，Qt可识别，无报错
        self._animation = QPropertyAnimation(self, b"offset", self)
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
    
    # 关键：使用@property装饰器（PySide6的Property）注册Qt属性
    @Property(float)  # 定义属性类型为float，支持动画的连续数值变化
    def offset(self):
        # 取值方法：返回私有变量_offset的值
        return self._offset
    
    @offset.setter
    def offset(self, value):
        # 赋值方法：接收动画传入的数值，更新并刷新界面
        self._offset = value
        self.update()  # 触发paintEvent，实时重绘滑块
    
    def isChecked(self):
        return self._checked
        
    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            end_value = 20 if checked else 2
            self._animation.stop()
            self._animation.setStartValue(self._offset)
            self._animation.setEndValue(end_value)
            self._animation.start()
            self.toggled.emit(checked)
            
    def mousePressEvent(self, event):
        self.setChecked(not self._checked)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # === 滑轨（Track）绘制 ===
        track_width = self.width()      # 40
        track_height = self.height()    # 22
        corner_radius = track_height // 2  # 11 → 完全圆角
        
        # 背景颜色（根据状态）
        bg_color = QColor(155, 205, 246) if self._checked else QColor(200, 200, 200)
   
        # 画内填充（覆盖边框内部）
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_color))
        # 缩小矩形以避开边框（内缩 1.5px，因为边框宽3px，每边占1.5px）
        inner_rect = QRectF(1.5, 1.5, track_width - 3, track_height - 3)
        painter.drawRoundedRect(inner_rect, corner_radius - 1.5, corner_radius - 1.5)
        
        # === 滑块（Thumb）绘制 ===
        thumb_size = 18  # 🔸 原14 → 现18，明显放大
        # 滑块位置：在 2px 到 (40 - 18 - 2) = 20px 之间滑动
        
        thumb_x = int(self._offset)
        thumb_y = (track_height - thumb_size) // 2  # 垂直居中：(22-18)/2 = 2
        
        # 白色滑块 + 可选轻微阴影边框
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(180, 180, 180), 1))  # 浅灰细边框，增强立体感
        painter.drawEllipse(thumb_x, thumb_y, thumb_size, thumb_size)