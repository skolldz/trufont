from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import QSizePolicy, QWidget


class GlyphAlignmentWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self._alignment = None
        self._alignmentPaths = []
        self._glyph = None

        self._color = QColor(130, 130, 130)
        self._selectedColor = QColor(20, 146, 230)

    def alignment(self):
        return self._alignment

    def setAlignment(self, value):
        self._alignment = value

    def glyph(self):
        return self._glyph

    def setGlyph(self, glyph):
        self._glyph = glyph

    def origin(self):
        alignment = self._alignment
        glyph = self._glyph
        if None in (alignment, glyph, glyph.bounds):
            return (0, 0)
        left, bottom, right, top = glyph.bounds
        if not alignment % 3:
            x = left
        elif not (alignment - 2) % 3:
            x = right
        else:
            x = (left + right) / 2
        if alignment < 3:
            y = top
        elif alignment > 5:
            y = bottom
        else:
            y = (top + bottom) / 2
        return (x, y)

    def color(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.update()

    def selectedColor(self):
        return self._selectedColor

    def setSelectedColor(self, color):
        self._selectedColor = color
        self.update()

    # ----------
    # Qt methods
    # ----------

    def sizeHint(self):
        return QSize(30, 30)

    def mousePressEvent(self, event):
        if event.button() & Qt.LeftButton:
            pos = event.localPos()
            # TODO: press should be actuated on release...
            for index, path in enumerate(self._alignmentPaths):
                if path.contains(pos):
                    if self._alignment == index:
                        self._alignment = None
                    else:
                        self._alignment = index
                    self.update()
                    break
        else:
            super().mousePressEvent(event)

    def paintEvent(self, event):
        self._alignmentPaths = []
        painter = QPainter(self)
        painter.setPen(self._color)

        circleRadius = 2.5
        padding = 1
        rect = event.rect()
        size = min(rect.height(), rect.width())
        offset = round(.5 * (rect.width() - size))
        painter.translate(offset, 0)
        borderRect = rect.__class__(
            rect.left() + circleRadius + padding,
            rect.top() + circleRadius + padding,
            size - 2 * (circleRadius + padding),
            size - 2 * (circleRadius + padding))
        borderPath = QPainterPath()
        borderPath.addRect(*borderRect.getRect())

        columnCount = 3
        radioPath = QPainterPath()
        selectedPath = QPainterPath()
        for row in range(columnCount):
            for col in range(columnCount):
                index = row * columnCount + col
                x, y = padding + col * .5 * borderRect.width(
                    ), padding + row * .5 * borderRect.height()
                if self._alignment == index:
                    selectedRadius = 3
                    x -= selectedRadius - circleRadius
                    y -= selectedRadius - circleRadius
                    path = QPainterPath()
                    path.addEllipse(
                        x, y, 2 * selectedRadius, 2 * selectedRadius)
                    selectedPath = path
                else:
                    path = QPainterPath()
                    path.addEllipse(
                        x, y, 2 * circleRadius, 2 * circleRadius)
                    radioPath.addPath(path)
                self._alignmentPaths.append(path.translated(offset, 0))
        painter.drawPath(borderPath - radioPath)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(radioPath, self._color)
        painter.fillPath(selectedPath, self._selectedColor)
