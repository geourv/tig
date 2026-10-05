"""Native QGIS GUI actor for this one Vila-seca lesson; execute with qgis --code.

The actor uses the application's menus, dialogs and Browser. It never draws a
replacement UI. Inputs and original classroom projects are mounted read-only.
Only the disposable teaching directory PR1_GUI_ROOT is writable.
"""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import traceback
import unicodedata

from qgis.PyQt.QtCore import QDir, QModelIndex, QPoint, QTimer, Qt
from qgis.PyQt import sip
from qgis.PyQt.QtGui import QColor, QContextMenuEvent, QFont
from qgis.PyQt.QtTest import QTest
from qgis.PyQt.QtWidgets import (
    QAction, QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox,
    QDockWidget, QFileDialog, QLineEdit, QMenu, QPushButton, QTreeView, QWidget,
)
from qgis.core import (
    Qgis, QgsCoordinateReferenceSystem, QgsDataSourceUri, QgsFillSymbol,
    QgsPalLayerSettings, QgsProject, QgsRasterLayer, QgsRectangle,
    QgsSingleSymbolRenderer, QgsTextBufferSettings, QgsTextFormat,
    QgsVectorLayer, QgsVectorLayerSimpleLabeling,
)
from qgis.gui import QgsCollapsibleGroupBox, QgsFileWidget, QgsProjectionSelectionWidget, QgsVectorLayerSaveAsDialog
from qgis.utils import iface

ROOT = Path(os.environ.get("PR1_GUI_ROOT", "/home/docent/tig"))
STEM = "pr1-project-setup-exemple"
GPKG = ROOT / "sandbox" / f"{STEM}.gpkg"
IMAGE = "qgis/qgis@sha256:e016b5296b99f0b07760b883888bc4ba615c0099feae9432374b4c83e8e073cc"


def normal(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.replace("&", "").lower())
                   if unicodedata.category(c) != "Mn").strip()


class VilaSecaLesson:
    def __init__(self):
        self.project = QgsProject.instance()
        self.window = iface.mainWindow()
        self.trace = {"complete": False, "transport": "native-qgis-gui",
                      "producer": "TIG case-specific PyQGIS/Qt actor", "image": IMAGE,
                      "qgis": Qgis.QGIS_VERSION, "locale": "ca_ES", "steps": [], "captures": {}}
        self.counter = 0
        self.pending_project = "pr1"
        self.result_notice_cleared = False
        self.menu = None
        self.submenu = None
        self.write_trace()
        QTimer.singleShot(1800, self.guard(self.start))

    def guard(self, function):
        def wrapped():
            try:
                function()
            except Exception:
                self.trace["error"] = traceback.format_exc()
                self.write_trace()
                self.close()
        return wrapped

    def later(self, function, milliseconds=700):
        QTimer.singleShot(milliseconds, self.guard(function))

    def require(self, condition, message):
        if not condition:
            raise RuntimeError(message)

    def write_trace(self):
        (ROOT / "gui-evidence.json").write_text(json.dumps(self.trace, ensure_ascii=False, indent=2) + "\n")

    def log(self, event, **values):
        self.trace["steps"].append({"event": event, **values})
        self.write_trace()

    def close(self):
        modal = QApplication.activeModalWidget()
        if isinstance(modal, QDialog):
            modal.close()
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMenu) and widget.isVisible():
                widget.hide()
        iface.mapCanvas().stopRendering()
        self.project.setDirty(False)
        QTimer.singleShot(700, self.window.close)

    def dump(self, widget, name):
        controls = []
        for child in widget.findChildren((QLineEdit, QComboBox, QCheckBox, QPushButton)):
            item = {"object": child.objectName(), "class": child.metaObject().className(), "visible": child.isVisible()}
            if isinstance(child, QComboBox):
                item.update(current=child.currentText(), count=child.count(), editable=child.isEditable(),
                            values=[child.itemText(i) for i in range(min(child.count(), 32))])
            else:
                item["text"] = child.text()
            controls.append(item)
        (ROOT / f"{name}.json").write_text(json.dumps({"title": widget.windowTitle(),
            "class": widget.metaObject().className(), "controls": controls,
            "qgis_widgets": [{"object": child.objectName(), "class": child.metaObject().className()}
                             for child in widget.findChildren(QWidget)
                             if child.metaObject().className().startswith("Qgs")]}, ensure_ascii=False, indent=2))

    def capture(self, key, widget=None, detail=None):
        self.window.repaint()
        screen = QApplication.primaryScreen()
        if key == "projects-in-browser":
            widget = self.browser_dock
        if widget is not None:
            pixmap = widget.grab()
            camera = {"kind": "native-widget", "class": widget.metaObject().className(),
                      "title": widget.windowTitle(), "object": widget.objectName()}
        else:
            rectangle = self.window.frameGeometry()
            menus = [top for top in QApplication.topLevelWidgets() if top.isVisible() and isinstance(top, QMenu)]
            if key in {"export-menu", "save-project-menu"} and menus:
                rectangle = menus[0].frameGeometry()
                for menu in menus[1:]:
                    rectangle = rectangle.united(menu.frameGeometry())
                if key == "save-project-menu":
                    bar = self.window.menuBar()
                    item = bar.actionGeometry(iface.projectMenu().menuAction())
                    item.moveTopLeft(bar.mapToGlobal(item.topLeft()))
                    rectangle = rectangle.united(item)
                rectangle.adjust(-6, -6, 6, 6)
            elif key == "refresh-connection":
                rectangle = self.browser_dock.rect()
                rectangle.moveTopLeft(self.browser_dock.mapToGlobal(QPoint(0, 0)))
                for menu in menus:
                    rectangle = rectangle.united(menu.frameGeometry())
                rectangle.adjust(-6, -6, 6, 6)
            else:
                for menu in menus:
                    rectangle = rectangle.united(menu.frameGeometry())
            rectangle = rectangle.intersected(screen.geometry())
            pixmap = screen.grabWindow(0, rectangle.x(), rectangle.y(), rectangle.width(), rectangle.height())
            camera = {"kind": "native-screen", "x": rectangle.x(), "y": rectangle.y()}
        path = ROOT / "captures" / f"qgis-pr1-{key}.png"
        self.require(pixmap.save(str(path), "PNG"), f"Cannot save {key}")
        camera.update(width=pixmap.width(), height=pixmap.height(), device_pixel_ratio=pixmap.devicePixelRatio())
        manifest = {"capture": key, "producer": self.trace["producer"], "transport": self.trace["transport"],
                    "image": IMAGE, "qgis": Qgis.QGIS_VERSION, "locale": "ca_ES", "camera": camera,
                    "png_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "evidence": detail or {},
                    "source": "context/practiques/capture_pr1_guided.py", "native_ui": True,
                    "source_geometry": "municipis_entorn.gpkg, fixed ICGC edition 20260120"}
        path.with_suffix(".manifest.yml").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        self.trace["captures"][key] = manifest
        self.write_trace()

    def action(self, menu, words):
        for action in menu.actions():
            if any(word in normal(action.text()) for word in words):
                return action
        raise RuntimeError(f"Menu action {words} not found: {[a.text() for a in menu.actions()]}")

    def modal(self):
        widget = QApplication.activeModalWidget()
        if widget is None:
            visible = [w for w in QApplication.topLevelWidgets() if w.isVisible() and isinstance(w, QDialog)]
            self.require(len(visible) == 1, f"Expected one native dialog, got {[w.windowTitle() for w in visible]}")
            widget = visible[0]
        return widget

    def accept(self, dialog):
        choices = []
        states = []
        for box in dialog.findChildren(QDialogButtonBox):
            for role in (QDialogButtonBox.Ok, QDialogButtonBox.Save, QDialogButtonBox.Open):
                button = box.button(role)
                if button is not None:
                    states.append({"box": box.objectName(), "text": button.text(),
                                   "visible": button.isVisible(), "enabled": button.isEnabled()})
                    if button.isVisible() and button.isEnabled():
                        choices.append(button)
        self.log("native-accept-buttons", buttons=states)
        self.require(len(choices) == 1, "Native accept button is missing, ambiguous or disabled")
        choices[0].click()

    def start(self):
        self.log("start")
        self.require(ROOT.is_dir() and not GPKG.exists(), "Use a freshly prepared teaching directory")
        QDir.setCurrent(str(ROOT / "sandbox"))
        QApplication.setFont(QFont("DejaVu Sans", 10))
        QApplication.instance().setStyleSheet("QMenu { font-size: 12pt; } QDialog, QDialog QWidget { font-size: 12pt; }")
        self.window.resize(1100, 730)
        self.window.move(0, 0)
        self.project.clear()
        self.project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        self.project.setFilePathStorage(Qgis.FilePathType.Relative)
        self.project.setPresetHomePath(".")
        uri = QgsDataSourceUri()
        for name, value in {"url": "https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms",
                            "layers": "ortofoto_25cm_color_2025", "styles": "", "format": "image/jpeg",
                            "crs": "EPSG:25831"}.items():
            uri.setParam(name, value)
        self.wms = QgsRasterLayer(bytes(uri.encodedUri()).decode(), "Ortofoto ICGC 2025 · WMS", "wms")
        self.require(self.wms.isValid(), "The real ICGC WMS could not be loaded")
        self.log("wms-ready", uri=self.wms.source())
        self.municipalities = QgsVectorLayer(str(ROOT / "data/raw/municipis_entorn.gpkg") + "|layername=municipis_entorn",
                                            "Municipis ICGC", "ogr")
        self.require(self.municipalities.isValid(), "Municipal source missing")
        self.municipalities.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({
            "color": "0,0,0,0", "outline_color": "255,255,255,255", "outline_width": "0.6"})))
        self.project.addMapLayer(self.wms)
        self.project.addMapLayer(self.municipalities)
        settings = QgsPalLayerSettings()
        settings.fieldName = "NOMMUNI"
        settings.placement = Qgis.LabelPlacement.Horizontal
        settings.setPolygonPlacementFlags(Qgis.LabelPolygonPlacementFlag.AllowPlacementInsideOfPolygon)
        settings.fitInPolygonOnly = True
        text = QgsTextFormat()
        text.setFont(QFont("DejaVu Sans", 14))
        text.setSize(14)
        text.setColor(QColor("white"))
        buffer = QgsTextBufferSettings()
        buffer.setEnabled(True)
        buffer.setSize(0.8)
        buffer.setColor(QColor("#262626"))
        text.setBuffer(buffer)
        settings.setFormat(text)
        self.municipalities.setLabeling(QgsVectorLayerSimpleLabeling(settings))
        self.municipalities.setLabelsEnabled(True)
        matches = [f for f in self.municipalities.getFeatures() if f["CODIMUNI"] == "431711"]
        self.require(len(matches) == 1, "Vila-seca is not unique")
        self.extent = QgsRectangle(matches[0].geometry().boundingBox())
        self.extent.scale(1.15)
        self.browser_dock = self.window.findChild(QDockWidget, "Browser")
        self.layers_dock = self.window.findChild(QDockWidget, "Layers")
        self.require(self.browser_dock and self.layers_dock, "Browser and Layers docks required")
        self.browser_dock.hide()
        self.layers_dock.show()
        self.window.resizeDocks([self.layers_dock], [265], Qt.Horizontal)
        iface.setActiveLayer(self.municipalities)
        iface.mapCanvas().setExtent(self.extent)
        iface.mapCanvas().refresh()
        self.counter = 0
        self.later(self.overview, 2000)

    def rendered(self, retry):
        self.counter += 1
        image = iface.mapCanvas().grab().toImage()
        colours = {image.pixel(x, y) for x in range(0, image.width(), 9) for y in range(0, image.height(), 9)}
        if iface.mapCanvas().isDrawing() or len(colours) < 700:
            self.require(self.counter < 75, f"WMS imagery did not render: {len(colours)} colours")
            self.later(retry, 1500)
            return False
        return True

    def overview(self):
        if iface.mapCanvas().extent().width() > 30000:
            self.counter += 1
            self.require(self.counter < 30, "The requested municipal zoom did not take effect")
            self.log("restore-municipal-extent", requested=self.extent.toString(), actual=iface.mapCanvas().extent().toString())
            iface.messageBar().clearWidgets()
            iface.mapCanvas().setExtent(self.extent)
            iface.mapCanvas().refresh()
            self.later(self.overview, 1500)
            return
        if not self.rendered(self.overview):
            return
        iface.messageBar().clearWidgets()
        self.capture("wms-overview", detail={"provider": self.wms.providerType(), "uri": self.wms.source(),
                    "municipality_count": self.municipalities.featureCount(), "crs": self.project.crs().authid(),
                    "canvas_extent": iface.mapCanvas().extent().toString()})
        self.municipalities.selectByExpression('"CODIMUNI" = \'431711\'')
        self.require(self.municipalities.selectedFeatureCount() == 1, "Selection failed")
        self.later(self.selected)

    def selected(self):
        self.capture("selected-municipality", detail={"expression": '"CODIMUNI" = \'431711\'', "selected": 1})
        view = iface.layerTreeView()
        index = view.currentIndex()
        position = view.visualRect(index).center()
        self.later(self.export_menu)
        event = QContextMenuEvent(QContextMenuEvent.Mouse, position, view.viewport().mapToGlobal(position))
        QApplication.sendEvent(view.viewport(), event)

    def export_menu(self):
        self.menu = QApplication.activePopupWidget()
        self.require(isinstance(self.menu, QMenu), "The native layer context menu did not open")
        export = self.action(self.menu, ["exporta", "export"])
        self.submenu = export.menu()
        self.require(self.submenu is not None, "Export submenu missing")
        self.menu.setActiveAction(export)
        self.submenu.popup(self.menu.mapToGlobal(self.menu.actionGeometry(export).topRight()))
        self.export_action = self.action(self.submenu, ["seleccion", "selected"])
        self.later(self.export_menu_shot)

    def export_menu_shot(self):
        self.capture("export-menu", detail={"action": self.export_action.text(), "selected": 1})
        self.later(self.configure_export)
        self.export_action.trigger()

    def configure_export(self):
        self.export_dialog = self.modal()
        self.dump(self.export_dialog, "export-controls")
        self.require(self.export_dialog.inherits("QgsVectorLayerSaveAsDialog"), "Not the native vector export dialog")
        self.export_dialog = sip.cast(self.export_dialog, QgsVectorLayerSaveAsDialog)
        if os.environ.get("PR1_GUI_PROBE") == "export":
            self.log("probe-export-dialog")
            self.close()
            return
        formats = [c for c in self.export_dialog.findChildren(QComboBox) if c.findText("GeoPackage") >= 0]
        self.require(len(formats) == 1, "GeoPackage format selector is ambiguous")
        formats[0].setCurrentIndex(formats[0].findText("GeoPackage"))
        self.later(self.export_parameters, 400)

    def export_parameters(self):
        dialog = self.export_dialog
        self.dump(dialog, "export-controls")
        file_widgets = dialog.findChildren(QgsFileWidget)
        self.require(len(file_widgets) == 1, "Expected one native export file widget")
        file_widgets[0].setFilePath(str(GPKG))
        layer_name = dialog.findChild(QLineEdit, "mLayerName") or dialog.findChild(QLineEdit, "leLayername")
        self.require(layer_name is not None, "Layer name control missing; inspect export-controls.json")
        layer_name.setText("municipi_vilaseca")
        crs = dialog.findChild(QgsProjectionSelectionWidget)
        if crs is None:
            matches = [w for w in dialog.findChildren(QWidget) if w.inherits("QgsProjectionSelectionWidget")]
            if matches:
                crs = sip.cast(matches[0], QgsProjectionSelectionWidget)
        self.require(crs is not None, "Native output CRS selector missing")
        crs.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        dialog.setOnlySelected(True)
        dialog.setAddToCanvas(True)
        for widget in dialog.findChildren(QWidget):
            if widget.inherits("QgsCollapsibleGroupBox"):
                sip.cast(widget, QgsCollapsibleGroupBox).setCollapsed(True)
        dialog.resize(850, 540)
        self.later(self.export_dialog_shot)

    def export_dialog_shot(self):
        dialog = self.export_dialog
        evidence = {"format": dialog.format(), "filename": dialog.fileName(), "layer": dialog.layerName(),
                    "only_selected": dialog.onlySelected(), "crs": dialog.crs().authid(), "add_to_canvas": dialog.addToCanvas()}
        self.require(evidence["format"] == "GPKG" and evidence["layer"] == "municipi_vilaseca"
                     and evidence["only_selected"] and evidence["crs"] == "EPSG:25831", str(evidence))
        self.capture("export-dialog", dialog, evidence)
        self.log("native-export-dialog-configured", **evidence)
        self.counter = 0
        self.later(self.exported, 1200)
        self.accept(dialog)

    def exported(self):
        self.counter += 1
        layers = [l for l in self.project.mapLayers().values() if str(GPKG) in l.source() and l.providerType() == "ogr"]
        if not layers:
            self.require(self.counter < 40, "The native export did not add the result")
            self.later(self.exported, 750)
            return
        self.local = layers[0]
        self.require(self.local.featureCount() == 1 and self.local.crs().authid() == "EPSG:25831", "Invalid export result")
        self.log("native-export-output-loaded", source=self.local.source(), count=self.local.featureCount())
        self.local.setName("Vila-seca · límit municipal")
        self.local.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({
            "color": "0,0,0,0", "outline_color": "255,70,190,255", "outline_width": "1.1"})))
        self.project.removeMapLayer(self.municipalities.id())
        iface.setActiveLayer(self.local)
        extent = QgsRectangle(self.local.extent())
        extent.scale(1.08)
        iface.mapCanvas().setExtent(extent)
        iface.mapCanvas().refresh()
        self.counter = 0
        self.later(self.result_map, 1200)

    def result_map(self):
        if not self.result_notice_cleared:
            iface.messageBar().clearWidgets()
            self.result_notice_cleared = True
            self.later(self.result_map, 600)
            return
        if not iface.mapCanvas().extent().contains(self.local.extent()):
            self.counter += 1
            self.require(self.counter < 30, "The exported municipality is not fully in view")
            iface.messageBar().clearWidgets()
            extent = QgsRectangle(self.local.extent())
            extent.scale(1.12)
            iface.mapCanvas().setExtent(extent)
            iface.mapCanvas().refresh()
            self.later(self.result_map, 1200)
            return
        if not self.rendered(self.result_map):
            return
        self.capture("wms-result", detail={"local_source": self.local.source(), "count": self.local.featureCount(),
                                         "wms": self.wms.source(), "crs": self.local.crs().authid(),
                                         "canvas_extent": iface.mapCanvas().extent().toString()})
        self.browser_dock.show()
        self.window.resizeDocks([self.browser_dock], [335], Qt.Horizontal)
        self.window.resizeDocks([self.browser_dock, self.layers_dock], [420, 230], Qt.Vertical)
        self.browser = self.browser_dock.findChild(QTreeView)
        self.require(self.browser is not None, "Browser tree missing")
        self.later(self.connect_menu)

    def find_index(self, text, parent=QModelIndex(), exact=False):
        model = self.browser.model()
        for row in range(model.rowCount(parent)):
            index = model.index(row, 0, parent)
            value = str(model.data(index, Qt.DisplayRole) or "")
            if (value == text) if exact else (text in value):
                return index
            child = self.find_index(text, index, exact)
            if child.isValid():
                return child
        return QModelIndex()

    def browser_context(self, index, callback):
        self.require(index.isValid(), "Browser entry not found")
        self.browser.setCurrentIndex(index)
        self.browser.scrollTo(index)
        point = self.browser.visualRect(index).center()
        self.later(callback)
        QApplication.sendEvent(self.browser.viewport(), QContextMenuEvent(
            QContextMenuEvent.Mouse, point, self.browser.viewport().mapToGlobal(point)))

    def connect_menu(self):
        self.browser_context(self.find_index("GeoPackage", exact=True), self.choose_connection)

    def choose_connection(self):
        menu = QApplication.activePopupWidget()
        self.require(isinstance(menu, QMenu), "GeoPackage Browser menu missing")
        action = self.action(menu, ["nova connexio", "new connection"])
        self.later(self.connection_dialog)
        action.trigger()

    def connection_dialog(self):
        dialog = self.modal()
        self.dump(dialog, "connection-controls")
        self.require(isinstance(dialog, QFileDialog), "Expected the native GeoPackage file chooser")
        dialog.setDirectory(str(GPKG.parent))
        dialog.resize(900, 540)
        self.later(lambda: self.fill_connection(dialog), 500)

    def fill_connection(self, dialog):
        edit = dialog.findChild(QLineEdit, "fileNameEdit")
        self.require(edit is not None, "Native file name control missing")
        edit.setFocus()
        edit.selectAll()
        QTest.keyClicks(edit, GPKG.name)
        files = dialog.findChild(QTreeView, "treeView")
        if files is not None:
            for column, width in enumerate((390, 90, 100, 170)):
                files.header().resizeSection(column, width)
        self.dump(dialog, "connection-controls")
        self.later(lambda: self.connection_shot(dialog))

    def connection_shot(self, dialog):
        self.require(str(GPKG) in dialog.selectedFiles(), f"Wrong connection file: {dialog.selectedFiles()}")
        self.capture("connect-dialog", dialog, {"selected_files": dialog.selectedFiles()})
        self.later(self.project_menu, 1000)
        self.accept(dialog)

    def project_menu(self):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMenu) and widget.isVisible():
                widget.hide()
        self.menu = iface.projectMenu()
        bar = self.window.menuBar()
        position = bar.mapToGlobal(bar.actionGeometry(self.menu.menuAction()).bottomLeft())
        self.menu.popup(position)
        self.later(self.save_submenu)

    def save_submenu(self):
        action = self.action(self.menu, ["desa a", "save to"])
        self.submenu = action.menu()
        self.require(self.submenu is not None, "Save To submenu missing")
        self.menu.setActiveAction(action)
        self.submenu.popup(self.menu.mapToGlobal(self.menu.actionGeometry(action).topRight()))
        self.save_action = self.action(self.submenu, ["geopackage"])
        self.later(self.save_menu_shot)

    def save_menu_shot(self):
        if self.pending_project == "pr1":
            self.capture("save-project-menu", detail={"action": self.save_action.text()})
        self.later(self.configure_project_save)
        self.save_action.trigger()

    def configure_project_save(self):
        dialog = self.modal()
        self.dump(dialog, "project-save-controls")
        combos = dialog.findChildren(QComboBox)
        connections = [(combo, index) for combo in combos for index in range(combo.count())
                       if STEM in combo.itemText(index)]
        self.require(connections, "The practice GeoPackage is absent from the save dialog")
        connections[0][0].setCurrentIndex(connections[0][1])
        self.save_dialog = dialog
        self.later(self.project_name, 400)

    def project_name(self):
        dialog = self.save_dialog
        self.dump(dialog, "project-save-controls")
        name = dialog.findChild(QComboBox, "mCboProject")
        if name is None:
            name = dialog.findChild(QComboBox, "mComboProject")
        if name is not None and name.isEditable():
            name.setEditText(self.pending_project)
        else:
            edit = dialog.findChild(QLineEdit, "mEditProjectName") or dialog.findChild(QLineEdit, "mProjectName")
            self.require(edit is not None, "Project name control missing; inspect project-save-controls.json")
            edit.setText(self.pending_project)
        self.later(self.save_dialog_shot)

    def save_dialog_shot(self):
        if self.pending_project == "pr1":
            self.capture("save-project-dialog", self.save_dialog, {"project_name": self.pending_project, "file": str(GPKG)})
        self.log("native-project-save-configured", project=self.pending_project)
        self.counter = 0
        self.later(self.project_saved, 1200)
        self.accept(self.save_dialog)

    def project_saved(self):
        self.counter += 1
        with sqlite3.connect(GPKG.resolve().as_uri() + "?mode=ro", uri=True) as db:
            tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            names = [r[0] for r in db.execute("SELECT name FROM qgis_projects")] if "qgis_projects" in tables else []
        if self.pending_project not in names:
            self.require(self.counter < 25, "The GUI did not save the project")
            self.later(self.project_saved)
            return
        self.log("project-exists-in-geopackage", names=names, active_project=self.project.fileName())
        self.later(self.refresh_menu)

    def expand(self, index):
        self.browser.expand(index)
        model = self.browser.model()
        if model.canFetchMore(index):
            model.fetchMore(index)

    def refresh_menu(self):
        root = self.find_index("GeoPackage", exact=True)
        self.expand(root)
        self.later(self.connection_context)

    def connection_context(self):
        connection = self.find_index(STEM)
        self.require(connection.isValid(), "The Browser connection did not appear")
        self.expand(connection)
        self.browser_context(connection, self.refresh_action)

    def refresh_action(self):
        menu = QApplication.activePopupWidget()
        self.require(isinstance(menu, QMenu), "Connection context menu missing")
        refresh = self.action(menu, ["actualitza", "refresca", "refresh"])
        if self.pending_project == "pr1":
            self.capture("refresh-connection", detail={"action": refresh.text(), "connection": STEM})
        self.later(self.refreshed, 1200)
        refresh.trigger()
        menu.hide()

    def tree_items(self, parent=QModelIndex(), depth=0):
        model = self.browser.model()
        items = []
        for row in range(model.rowCount(parent)):
            index = model.index(row, 0, parent)
            items.append({"text": str(model.data(index, Qt.DisplayRole)), "depth": depth})
            items.extend(self.tree_items(index, depth + 1))
        return items

    def refreshed(self):
        for popup in QApplication.topLevelWidgets():
            if isinstance(popup, QMenu) and popup.isVisible():
                popup.hide()
        connection = self.find_index(STEM)
        self.expand(connection)
        model = self.browser.model()
        for row in range(model.rowCount(connection)):
            self.expand(model.index(row, 0, connection))
        if self.pending_project == "pr1":
            self.pending_project = "comparacio"
            self.local.renderer().symbol().symbolLayer(0).setStrokeColor(QColor("#ffcc33"))
            self.local.triggerRepaint()
            extent = QgsRectangle(self.local.extent())
            extent.scale(0.55)
            iface.mapCanvas().setExtent(extent)
            self.project.setDirty(True)
            self.later(self.project_menu)
        else:
            self.counter = 0
            self.later(self.final_browser, 1500)

    def final_browser(self):
        self.counter += 1
        connection = self.find_index(STEM)
        self.expand(connection)
        model = self.browser.model()
        for row in range(model.rowCount(connection)):
            self.expand(model.index(row, 0, connection))
        items = self.tree_items(connection)
        names = [item["text"] for item in items]
        if not all(any(project in item for item in names) for project in ("pr1", "comparacio")):
            self.require(self.counter < 20, f"Browser does not expose both projects: {names}")
            self.later(self.final_browser)
            return
        self.browser.scrollTo(connection)
        self.capture("projects-in-browser", detail={"connection": STEM, "children": items})
        self.require(self.project.read(f"geopackage:{GPKG}?projectName=pr1"), "Cannot reopen pr1")
        self.project.setFilePathStorage(Qgis.FilePathType.Relative)
        self.require(self.project.write(str(GPKG.with_suffix(".qgz"))), "Cannot write the external project")
        self.trace["external_project_save"] = "PyQGIS write after reopening the native-GUI-saved pr1; not a claimed GUI click"
        self.trace["complete"] = True
        self.write_trace()
        self.close()


LESSON = VilaSecaLesson()
