
import sys
from PySide6.QtWidgets import QApplication
from QtGraphVisuals import QGraphViewer
from qt_material import apply_stylesheet
import networkx as nx

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("QtGraphVisuals Demo")

    extra={ "secondaryDarkColor":"#232629", "font_size": '15px',}
    apply_stylesheet(app, theme='dark_blue.xml', extra=extra)

    from tensorflow import keras
    model = keras.models.load_model("hardnet_block.h5")
    viewer = QGraphViewer({'hardnet_block':model, 'resnet50':keras.applications.ResNet50()})
    viewer.show()

    sys.exit(app.exec())
