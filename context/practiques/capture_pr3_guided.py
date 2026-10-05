"""Native QGIS actor for the chapter 05 filters, selections and expressions case."""
import hashlib
import copy
import json
import os
from pathlib import Path
import sys
import runpy
import sqlite3
import traceback
import unicodedata
import yaml

from qgis.PyQt import sip
from qgis.PyQt.Qsci import QsciScintilla
from qgis.PyQt.QtCore import QDir, QEvent, QItemSelectionModel, QPoint, QPointF, QRect, QTimer, Qt
from qgis.PyQt.QtGui import QColor, QContextMenuEvent, QFont, QMouseEvent
from qgis.PyQt.QtTest import QTest
from qgis.PyQt.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDockWidget,
    QGroupBox, QLineEdit, QListView, QMenu, QPushButton, QSpinBox, QTextBrowser, QToolButton, QTreeView, QWidget,
)
from qgis.core import (
    Qgis, QgsApplication, QgsAttributeTableConfig, QgsCoordinateReferenceSystem,
    QgsCoordinateTransform, QgsDataSourceUri, QgsExpression, QgsExpressionContext,
    QgsExpressionContextUtils, QgsFeatureRequest, QgsField, QgsFillSymbol, QgsGeometry,
    QgsLineSymbol, QgsMarkerSymbol, QgsPalLayerSettings, QgsProject, QgsRasterLayer, QgsRectangle, QgsRuleBasedLabeling, QgsSingleSymbolRenderer,
    QgsTextBufferSettings, QgsTextFormat, QgsVectorLayer, QgsVectorLayerSimpleLabeling,
)
from qgis.gui import (QgsAttributeTableView, QgsCollapsibleGroupBox, QgsDualView, QgsExpressionBuilderWidget,
                      QgsFileWidget, QgsProjectionSelectionWidget, QgsQueryBuilder, QgsVectorLayerSaveAsDialog)
from qgis.utils import iface

ROOT = Path(os.environ.get("PR3_GUI_ROOT", "/home/docent/tig"))
GPKG = ROOT / "sandbox/pr3-consultes-exemple.gpkg"
IMAGE = "qgis/qgis@sha256:e016b5296b99f0b07760b883888bc4ba615c0099feae9432374b4c83e8e073cc"
SOURCE_ROOT = Path("/workspace")


class FrameReady(Exception):
    """Hand the prepared native scene to the installed one-shot provider."""


def normal(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.replace("&", "").lower())
                   if unicodedata.category(c) != "Mn")


class FiltersLesson:
    def __init__(self):
        self.control = json.loads((ROOT / "controls.json").read_text())
        self.provenance = json.loads((ROOT / "provenance.json").read_text())
        self.plan = yaml.safe_load((SOURCE_ROOT / "context/practiques/pr3-captures.yml").read_text())
        self.render_shot = os.environ.get("PR3_RENDER_SHOT", "")
        self.dynamic_targets = {}
        self.project = QgsProject.instance()
        self.window = iface.mainWindow()
        self.trace = {"complete": False, "transport": "native-qgis-gui", "qgis": Qgis.QGIS_VERSION,
                      "image": IMAGE, "captures": {}, "steps": [], "selection_tests": []}
        self.write_trace()
        self.later(self.start, 1500)

    def require(self, condition, message):
        if not condition:
            raise RuntimeError(message)

    def write_trace(self):
        (ROOT / "gui-evidence.json").write_text(json.dumps(self.trace, ensure_ascii=False, indent=2) + "\n")

    def close(self):
        dialog = QApplication.activeModalWidget()
        if dialog is not None:
            dialog.close()
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMenu) and widget.isVisible():
                widget.hide()
        iface.mapCanvas().stopRendering()
        self.project.setDirty(False)
        QTimer.singleShot(700, self.window.close)

    def later(self, callback, ms=700):
        def guarded():
            try:
                callback()
            except FrameReady:
                pass
            except Exception:
                self.trace["error"] = traceback.format_exc()
                self.window.grab().save(str(ROOT / "failure.png"), "PNG")
                self.write_trace()
                self.close()
        QTimer.singleShot(ms, guarded)

    def dump(self, dialog, name):
        items = []
        for widget in dialog.findChildren(QWidget):
            if isinstance(widget, (QLineEdit, QComboBox, QCheckBox, QGroupBox, QPushButton, QSpinBox, QToolButton, QTextBrowser, QTreeView)) or widget.metaObject().className().startswith("QgsExpression"):
                item = {"object": widget.objectName(), "class": widget.metaObject().className(), "visible": widget.isVisible()}
                if isinstance(widget, QComboBox):
                    item.update(text=widget.currentText(), editable=widget.isEditable(),
                                values=[widget.itemText(i) for i in range(min(24, widget.count()))])
                elif hasattr(widget, "text"):
                    item["text"] = widget.text()
                items.append(item)
        (ROOT / (name + ".json")).write_text(json.dumps({"title": dialog.windowTitle(), "class": dialog.metaObject().className(), "controls": items}, ensure_ascii=False, indent=2))

    def capture(self, key, widget=None, evidence=None, popups=False):
        if self.render_shot:
            if key != self.render_shot:
                return
            wheel = Path(os.environ["PR3_ANNOTATION_WHEEL"])
            provider = self.provenance["annotation_provider"]
            self.require(hashlib.sha256(wheel.read_bytes()).hexdigest() == provider["sha256"], "Annotation provider changed")
            target = widget if widget is not None else self.window
            target.setObjectName("tigCaptureTarget")
            spec = copy.deepcopy(next(item for item in self.plan["captures"] if item["id"] == key))
            # Scope exact widget targets to this live frame. Earlier closed
            # native dialogs may retain controls with identical object names.
            for drawing in spec.get("drawings", []):
                name = drawing.get("target", {}).get("object_name")
                if not name or name in self.dynamic_targets:
                    continue
                matches = [w for w in target.findChildren(QWidget) if w.isVisible() and w.objectName() == name]
                self.require(len(matches) == 1, f"Frame target is missing or ambiguous: {key}/{name}")
                actual = matches[0]
                rect = actual.rect()
                rect.moveTopLeft(actual.mapToGlobal(QPoint(0, 0)))
                self.dynamic_targets[name] = rect
            spec["mode"] = "screen" if popups or spec.get("mode") == "screen" else "widget"
            if spec["mode"] == "screen":
                spec["camera"] = {"mode": "crop", "target": {"object_name": "tigCaptureTarget"}, "padding": 24}
                # Table dropdowns and adjacent layer context menus need their
                # real combined Qt bounds, rather than a menu-only crop.
                rect = target.rect()
                rect.moveTopLeft(target.mapToGlobal(QPoint(0, 0)))
                for menu in QApplication.topLevelWidgets():
                    if isinstance(menu, QMenu) and menu.isVisible():
                        rect = rect.united(menu.frameGeometry())
                self.dynamic_targets["tigFrameBounds"] = rect
                spec["camera"]["target"] = {"object_name": "tigFrameBounds"}
            path = ROOT / "captures" / f"qgis-c05-{key}.png"
            spec["output"] = {"path": str(path), "manifest": str(path.with_suffix(".manifest.yml")),
                              "annotations_svg": str(path.with_suffix(".annotations.svg"))}
            job = {"image": IMAGE, "image_digest": IMAGE, "locale": "ca_ES", "display_backend": "x11",
                   "probe": {"qgis_version": Qgis.QGIS_VERSION, "annotation_provider": provider},
                   "recipe_path": "context/practiques/pr3-captures.yml", "recipe": {**self.plan, "setup": []},
                   "captures": [spec], "project": {"runtime": {"display_backend": "x11"}}}
            job_path = ROOT / "annotation-job.json"
            job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2))
            self.trace["frame_ready"] = {"id": key, "evidence": evidence or {},
                                         "sources": self.provenance["authoritative_sources"]}
            self.write_trace()
            os.environ["UNALTRACAPTURA_QGIS_BRIDGE_JOB"] = str(job_path)
            os.environ["UNALTRACAPTURA_QGIS_BRIDGE_RESULT"] = str(ROOT / "annotation-result.json")
            size = self.window.size()
            QTimer.singleShot(100, lambda: self.window.resize(size))
            sys.path.insert(0, str(wheel))
            bridge = runpy.run_module("veure_qgis_mcp.bridge.qgis_bridge")
            bridge["SYNTHETIC_RECTS"].update(self.dynamic_targets)
            raise FrameReady()
        if widget is not None and not popups:
            pixmap = widget.grab()
            camera = {"kind": "native-widget", "class": widget.metaObject().className(), "title": widget.windowTitle()}
        else:
            target = widget or self.window
            rect = target.rect()
            rect.moveTopLeft(target.mapToGlobal(QPoint(0, 0)))
            menus = [w for w in QApplication.topLevelWidgets() if isinstance(w, QMenu) and w.isVisible()]
            if widget is None and menus:
                rect = menus[0].frameGeometry()
                for menu in menus[1:]:
                    rect = rect.united(menu.frameGeometry())
            elif popups:
                for menu in menus:
                    rect = rect.united(menu.frameGeometry())
            rect = rect.intersected(QApplication.primaryScreen().geometry())
            pixmap = QApplication.primaryScreen().grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
            camera = {"kind": "native-screen", "x": rect.x(), "y": rect.y()}
        path = ROOT / "captures" / f"qgis-c05-{key}.png"
        self.require(pixmap.save(str(path), "PNG"), "Cannot save screenshot")
        camera.update(width=pixmap.width(), height=pixmap.height(), device_pixel_ratio=pixmap.devicePixelRatio())
        manifest = {"producer": "TIG chapter 05 PyQGIS/Qt actor", "transport": "native-qgis-gui",
                     "source": "context/practiques/capture_pr3_guided.py", "qgis": Qgis.QGIS_VERSION,
                     "source_sha256": self.provenance["authoritative_sources"]["context/practiques/capture_pr3_guided.py"],
                    "image": IMAGE, "capture": key, "camera": camera, "native_ui": True,
                    "png_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "evidence": evidence or {}}
        path.with_suffix(".manifest.yml").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        self.trace["captures"][key] = manifest
        self.write_trace()

    def modal(self):
        dialog = QApplication.activeModalWidget()
        self.require(dialog is not None, "Expected a native modal dialog")
        return dialog

    def accept(self, dialog):
        for role in (QDialogButtonBox.Ok, QDialogButtonBox.Save):
            choices = []
            for box in dialog.findChildren(QDialogButtonBox):
                button = box.button(role)
                if button is not None and button.isVisible() and button.isEnabled():
                    choices.append(button)
            if choices:
                self.require(len(choices) == 1, "Native accept button is ambiguous")
                choices[0].click()
                return
        self.require(False, "Native accept button missing")

    def readable_editor(self, dialog):
        for widget in dialog.findChildren(QWidget):
            if widget.inherits("QsciScintilla"):
                editor = sip.cast(widget, QsciScintilla)
                editor.setObjectName("tigExpression")
                font = QFont("DejaVu Sans Mono", 12)
                editor.setFont(font)
                if editor.lexer() is not None:
                    editor.lexer().setFont(font)
                editor.setWrapMode(QsciScintilla.WrapWord)

    def load(self, path, title, table=None, group=None):
        layer = QgsVectorLayer(str(path) + (f"|layername={table}" if table else ""), title, "ogr")
        self.require(layer.isValid(), f"Cannot load {title}")
        self.project.addMapLayer(layer, group is None)
        if group is not None:
            group.addLayer(layer)
        return layer

    def start(self):
        QDir.setCurrent(str(GPKG.parent))
        QApplication.setFont(QFont("DejaVu Sans", 10))
        QApplication.instance().setStyleSheet("QMenu { font-size: 12pt; } QDialog, QDialog QWidget { font-size: 12pt; }")
        self.window.resize(1188, 900)
        self.window.move(0, 0)
        self.project.clear()
        self.project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        self.project.setEllipsoid("GRS80")
        self.project.setAreaUnits(Qgis.AreaUnit.SquareMeters)
        self.project.setDistanceUnits(Qgis.DistanceUnit.Meters)
        self.project.setFilePathStorage(Qgis.FilePathType.Relative)
        self.project.setPresetHomePath(".")
        uri = QgsDataSourceUri()
        for key, value in {"url": "https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms", "layers": "ortofoto_25cm_color_2025",
                           "styles": "", "format": "image/jpeg", "crs": "EPSG:25831"}.items():
            uri.setParam(key, value)
        self.wms = QgsRasterLayer(bytes(uri.encodedUri()).decode(), "Ortofoto ICGC 2025 · WMS", "wms")
        self.require(self.wms.isValid(), "WMS unavailable")
        self.project.addMapLayer(self.wms)
        self.boundary = QgsVectorLayer(f"{GPKG}|layername=municipi_consulta", "Vila-seca · municipi CNIG", "ogr")
        self.require(self.boundary.isValid(), "Missing CNIG query municipality")
        self.boundary.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({"color":"0,0,0,0", "outline_color":"#d62a93", "outline_width":"1.1"})))
        self.municipalities = self.load(self.control["input_paths"]["municipales"], "Municipis CNIG")
        self.municipalities.setDisplayExpression('"NAMEUNIT"')
        self.municipalities.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({"color":"0,0,0,0", "outline_color":"white", "outline_width":"0.5"})))
        names = QgsPalLayerSettings()
        names.fieldName = "NAMEUNIT"
        names.placement = Qgis.LabelPlacement.Horizontal
        names.setPolygonPlacementFlags(Qgis.LabelPolygonPlacementFlag.AllowPlacementInsideOfPolygon)
        names.fitInPolygonOnly = True
        label_format = QgsTextFormat()
        label_format.setSize(13)
        label_format.setColor(QColor("#16334a"))
        halo = QgsTextBufferSettings()
        halo.setEnabled(True)
        halo.setSize(0.8)
        halo.setColor(QColor("white"))
        label_format.setBuffer(halo)
        names.setFormat(label_format)
        self.municipalities.setLabeling(QgsVectorLayerSimpleLabeling(names))
        self.municipalities.setLabelsEnabled(True)
        iface.setActiveLayer(self.municipalities)
        dock = self.window.findChild(QDockWidget, "Browser")
        if dock is not None:
            dock.hide()
        self.extent = QgsRectangle(self.boundary.extent())
        self.extent.scale(1.25)
        self.later(self.begin_manual, 2500)

    def begin_manual(self):
        # QGIS's first-layer policy can reset the CRS while the layers are added.
        self.project.setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        self.project.setEllipsoid("GRS80")
        iface.mapCanvas().setDestinationCrs(self.project.crs())
        iface.messageBar().clearWidgets()
        iface.mapCanvas().setExtent(self.extent)
        iface.mapCanvas().refresh()
        self.later(self.manual_selection, 2200)

    def manual_selection(self):
        feature = next(self.municipalities.getFeatures(QgsFeatureRequest().setFilterExpression('"NATCODE"=\'34094343171\'')))
        point = self.pixel(feature)
        viewport = iface.mapCanvas().viewport()
        # Click another verified interior point so the input cue does not
        # obscure the municipality's native name label near the polygon centre.
        shape = next(self.boundary.getFeatures()).geometry()
        transform = iface.mapCanvas().mapSettings().mapToPixel()
        candidates = [point + delta for delta in (QPoint(0, 130), QPoint(-100, 130), QPoint(100, 130))]
        candidates = [p for p in candidates if viewport.rect().contains(p) and
                      shape.contains(QgsGeometry.fromPointXY(transform.toMapCoordinates(p.x(), p.y())))]
        self.require(candidates, "No clear interior point for the manual click")
        point = candidates[0]
        iface.actionSelectRectangle().trigger()
        QTest.mouseClick(viewport, Qt.LeftButton, Qt.NoModifier, point)
        self.manual_id = feature.id()
        self.dynamic_targets["tigManualClick"] = QRect(viewport.mapToGlobal(point), viewport.size()).adjusted(0, 0, 1-viewport.width(), 1-viewport.height())
        self.later(self.manual_shot)

    def manual_shot(self):
        self.require(self.municipalities.selectedFeatureIds() == [self.manual_id], "Manual click did not select Vila-seca")
        self.trace["steps"].append({"operation": "manual click before any layer filter", "source_count": 8132, "selected": 1})
        self.capture("manual-selection", evidence={"source_count": 8132, "selected": 1, "NATCODE": "34094343171"})
        self.municipalities.removeSelection()
        self.later(lambda: self.layer_menu(self.municipalities, "layer-filter-menu", '"CODNUT3"=\'ES514\'',
                                          "layer-filter-dialog", self.filtered))

    def layer_menu(self, layer, menu_shot, sql, dialog_shot, afterwards):
        iface.setActiveLayer(layer)
        self.filter_layer = layer
        self.filter_sql = sql
        self.filter_dialog_shot = dialog_shot
        self.filter_afterwards = afterwards
        self.filter_menu_shot = menu_shot
        view = iface.layerTreeView()
        view.selectionModel().select(view.currentIndex(), QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        point = view.visualRect(view.currentIndex()).center()
        self.later(self.filter_menu)
        QApplication.sendEvent(view.viewport(), QContextMenuEvent(QContextMenuEvent.Mouse, point, view.viewport().mapToGlobal(point)))

    def filter_menu(self):
        menu = QApplication.activePopupWidget()
        self.require(isinstance(menu, QMenu), "Layer context menu missing")
        actions = [a for a in menu.actions() if normal(a.text()).startswith(("filtre", "filter"))]
        self.require(len(actions) == 1, f"Filter action missing on {self.filter_layer.name()}: {[a.text() for a in menu.actions()]}")
        menu.setActiveAction(actions[0])
        row = iface.layerTreeView().visualRect(iface.layerTreeView().currentIndex())
        menu.move(iface.layerTreeView().mapToGlobal(QPoint(iface.layerTreeView().width() + 16, row.top())))
        QTest.qWait(250)
        if self.filter_menu_shot:
            self.capture(self.filter_menu_shot, evidence={"action": actions[0].text(), "layer": self.filter_layer.name()})
        self.later(self.filter_dialog)
        actions[0].trigger()

    def filter_dialog(self):
        dialog = self.modal()
        self.dump(dialog, "query-builder-controls")
        self.require(dialog.inherits("QgsQueryBuilder"), "Not the native query builder")
        self.query = sip.cast(dialog, QgsQueryBuilder)
        self.query.setSql(self.filter_sql)
        self.query.resize(900, 620)
        self.readable_editor(self.query)
        field = "clased" if "clased" in self.filter_sql else "tipo" if "tipo" in self.filter_sql else "CODNUT3"
        for view in self.query.findChildren(QListView):
            model = view.model()
            if model is None:
                continue
            for row in range(model.rowCount()):
                index = model.index(row, 0)
                if index.data() == field:
                    view.setCurrentIndex(index)
                    view.scrollTo(index)
                    for button in self.query.findChildren(QPushButton):
                        if normal(button.text()) in {"mostra", "sample"}:
                            button.click()
                    break
        self.later(self.query_shot)

    def query_shot(self):
        self.capture(self.filter_dialog_shot, self.query, {"sql": self.query.sql(), "layer": self.filter_layer.name()})
        self.later(self.filter_afterwards)
        self.accept(self.query)

    def filtered(self):
        self.require(self.municipalities.featureCount() == 184, "Municipal filter did not apply")
        iface.mapCanvas().setExtent(self.extent)
        iface.mapCanvas().refresh()
        self.later(self.table_filter, 1200)

    def selection_menu(self):
        for button in self.window.findChildren(QToolButton):
            menu = button.menu()
            if menu is not None and any(
                action.objectName() == iface.actionSelectPolygon().objectName()
                for action in menu.actions() if action.objectName()
            ):
                self.tools_menu = menu
                menu.popup(button.mapToGlobal(button.rect().bottomLeft()))
                self.later(self.selection_menu_shot)
                return
        bar = self.window.menuBar()
        edits = [a for a in bar.actions() if normal(a.text()) in {"edita", "edit"}]
        self.require(edits, "Edit menu missing")
        self.tools_parent = edits[0].menu()
        choices = [a for a in self.tools_parent.actions() if a.menu() is not None and
                   ("seleccio" in normal(a.text()) or "select" in normal(a.text()))]
        self.require(choices, f"Selection submenu missing: {[a.text() for a in self.tools_parent.actions()]}")
        self.tools_parent.popup(bar.mapToGlobal(bar.actionGeometry(edits[0]).bottomLeft()))
        self.tools_parent.setActiveAction(choices[0])
        self.tools_menu = choices[0].menu()
        self.tools_menu.popup(self.tools_parent.mapToGlobal(self.tools_parent.actionGeometry(choices[0]).topRight()))
        self.later(self.selection_menu_shot)

    def selection_menu_shot(self):
        action = next(a for a in self.tools_menu.actions() if a == iface.actionSelectRectangle())
        rect = self.tools_menu.actionGeometry(action)
        rect.moveTopLeft(self.tools_menu.mapToGlobal(rect.topLeft()))
        self.dynamic_targets["tigSelectionRectangle"] = rect
        self.capture("selection-tools", self.tools_menu, {"tools": [a.text() for a in self.tools_menu.actions()]})
        self.tools_menu.hide()
        if hasattr(self, "tools_parent"):
            self.tools_parent.hide()
        self.later(self.selection_tests)

    def map_point(self, feature):
        geometry = QgsGeometry(feature.geometry())
        geometry.transform(QgsCoordinateTransform(self.municipalities.crs(), self.project.crs(), self.project))
        return geometry.poleOfInaccessibility(5)[0].asPoint()

    def pixel(self, feature):
        point = self.map_point(feature)
        position = iface.mapCanvas().mapSettings().mapToPixel().transform(point)
        pixel = QPoint(round(position.x()), round(position.y()))
        self.require(iface.mapCanvas().viewport().rect().contains(pixel),
                     f"Selection point outside canvas: {feature['NAMEUNIT']}, {point}, {pixel}, {iface.mapCanvas().extent().toString()}")
        return pixel

    def selection_tests(self):
        layer = self.municipalities
        iface.setActiveLayer(layer)
        features = {f["NAMEUNIT"]: f for f in layer.getFeatures(QgsFeatureRequest().setFilterExpression('"NAMEUNIT" IN (\'Vila-seca\',\'Salou\')'))}
        self.require(set(features) == {"Vila-seca", "Salou"}, "Selection controls missing")
        points = [self.map_point(feature) for feature in features.values()]
        area = QgsRectangle(min(p.x() for p in points)-2500, min(p.y() for p in points)-2500,
                            max(p.x() for p in points)+2500, max(p.y() for p in points)+2500)
        iface.mapCanvas().setExtent(area)
        iface.mapCanvas().refresh()
        QTest.qWait(1200)
        villa, salou = features["Vila-seca"].id(), features["Salou"].id()
        a, b = self.pixel(features["Vila-seca"]), self.pixel(features["Salou"])
        viewport = iface.mapCanvas().viewport()
        self.trace["selection_points"] = {
            "project_crs": self.project.crs().authid(),
            "canvas_crs": iface.mapCanvas().mapSettings().destinationCrs().authid(),
            "extent": iface.mapCanvas().extent().toString(),
            "points": {name: {"fid": f.id(), "map": self.map_point(f).toString(),
                              "pixel": [self.pixel(f).x(), self.pixel(f).y()]}
                       for name, f in features.items()},
        }

        def record(name, wanted):
            QTest.qWait(180)
            actual = set(layer.selectedFeatureIds())
            self.trace["selection_tests"].append({"test": name, "count": len(actual), "ids": sorted(actual),
                "names": [f["NAMEUNIT"] for f in layer.getSelectedFeatures()], "expected_ids": sorted(wanted)})
            self.write_trace()
            self.require(actual == wanted, f"Selection control failed: {name}, {actual}, {wanted}")

        def rectangle(point, modifiers=Qt.NoModifier):
            QTest.mousePress(viewport, Qt.LeftButton, modifiers, point - QPoint(7, 7))
            move(point, modifiers, Qt.LeftButton)
            move(point + QPoint(7, 7), modifiers, Qt.LeftButton)
            QTest.mouseRelease(viewport, Qt.LeftButton, modifiers, point + QPoint(7, 7))

        def move(point, modifiers=Qt.NoModifier, buttons=Qt.NoButton):
            # QWidget QTest.mouseMove does not carry the held button under Xvfb.
            # Deliver the move to the real canvas, with the actual drag state.
            event = QMouseEvent(QEvent.MouseMove, QPointF(point), Qt.NoButton, buttons, modifiers)
            QApplication.sendEvent(viewport, event)
            QTest.qWait(80)

        layer.removeSelection()
        iface.actionSelectRectangle().trigger()
        QTest.mouseClick(viewport, Qt.LeftButton, Qt.NoModifier, a)
        record("single-click-new", {villa})
        QTest.mouseClick(viewport, Qt.LeftButton, Qt.ShiftModifier, b)
        record("single-click-shift-toggle-add", {villa, salou})
        QTest.mouseClick(viewport, Qt.LeftButton, Qt.ControlModifier, a)
        record("single-click-control-toggle-remove", {salou})
        rectangle(a)
        record("rectangle-new", {villa})
        rectangle(b, Qt.ShiftModifier)
        record("rectangle-shift-add", {villa, salou})
        rectangle(a, Qt.ControlModifier)
        record("rectangle-control-subtract", {salou})
        layer.selectByIds([villa, salou])
        rectangle(a, Qt.ControlModifier | Qt.ShiftModifier)
        record("rectangle-control-shift-intersect", {villa})
        rectangle(a, Qt.AltModifier)
        record("rectangle-alt-wholly-contained", set())
        layer.removeSelection()
        iface.actionSelectPolygon().trigger()
        for delta in (QPoint(-7, -7), QPoint(7, -7), QPoint(7, 7), QPoint(-7, 7)):
            QTest.mouseClick(viewport, Qt.LeftButton, Qt.NoModifier, a + delta)
        QTest.mouseClick(viewport, Qt.RightButton, Qt.NoModifier, a)
        record("polygon", {villa})
        layer.removeSelection()
        iface.actionSelectFreehand().trigger()
        QTest.mouseClick(viewport, Qt.LeftButton, Qt.NoModifier, a - QPoint(7, 7))
        for delta in (QPoint(7, -7), QPoint(7, 7), QPoint(-7, 7), QPoint(-7, -7)):
            move(a + delta)
        QTest.mouseClick(viewport, Qt.LeftButton, Qt.NoModifier, a - QPoint(7, 7))
        record("freehand", {villa})
        layer.removeSelection()
        iface.actionSelectRadius().trigger()
        QTest.mouseClick(viewport, Qt.LeftButton, Qt.NoModifier, a)
        move(a + QPoint(10, 0))
        QTest.mouseClick(viewport, Qt.LeftButton, Qt.NoModifier, a + QPoint(10, 0))
        record("radius", {villa})
        next(a for a in self.tools_menu.actions() if normal(a.text()).startswith(("inverteix", "invert"))).trigger()
        self.require(layer.selectedFeatureCount() == 183, "Inversion did not act on the filtered layer")
        self.trace["steps"].append({"operation": "native invert selection", "count": 183, "layer_count": 184})
        next(a for a in self.tools_menu.actions() if "capa actual" in normal(a.text()) or "current active layer" in normal(a.text())).trigger()
        self.require(layer.selectedFeatureCount() == 0, "Native deselection failed")
        self.later(self.expression_menu)

    def table_filter(self):
        layer = self.municipalities
        config = layer.attributeTableConfig()
        columns = config.columns()
        for column in columns:
            column.hidden = column.name not in {"NAMEUNIT", "NATCODE", "CODNUT3"}
            column.width = 260 if column.name == "NAMEUNIT" else 165
        config.setColumns(columns)
        layer.setAttributeTableConfig(config)
        self.table = iface.showAttributeTable(layer)
        self.table.resize(850, 390)
        self.table.move(80, 130)
        self.table.show()
        self.later(self.table_selection_tests)

    def table_selection_tests(self):
        views = [w for w in self.table.findChildren(QWidget) if w.inherits("QgsAttributeTableView")]
        self.require(views, "Native attribute-table view missing")
        view = sip.cast(views[0], QgsAttributeTableView)
        header = view.verticalHeader()
        model = view.model()
        codes = [model.index(row, 0).data() for row in range(3)]

        def click(row, modifiers, wanted, name):
            point = QPoint(header.width() // 2, header.sectionViewportPosition(row) + header.sectionSize(row) // 2)
            QTest.mouseClick(header.viewport(), Qt.LeftButton, modifiers, point)
            QTest.qWait(150)
            actual = sorted(f["NATCODE"] for f in self.municipalities.getSelectedFeatures())
            self.trace.setdefault("table_selection_tests", []).append({"test": name, "actual": actual, "expected": sorted(wanted)})
            self.write_trace()
            self.require(actual == sorted(wanted), f"Table row selection failed: {name}, {actual}, {wanted}")

        click(0, Qt.NoModifier, [codes[0]], "header-click-new")
        click(2, Qt.ControlModifier, [codes[0], codes[2]], "header-control-add")
        click(0, Qt.ControlModifier, [codes[2]], "header-control-remove")
        click(0, Qt.NoModifier, [codes[0]], "header-click-replace")
        click(2, Qt.ShiftModifier, codes, "header-shift-range")
        self.municipalities.selectByExpression('"NAMEUNIT" IN (\'Vila-seca\',\'Salou\',\'Reus\')')
        self.later(self.table_filter_menu)

    def table_filter_menu(self):
        self.dump(self.table, "table-controls")
        button = self.table.findChild(QToolButton, "mFilterButton")
        self.require(button is not None and button.actions(), "Attribute-table filter actions missing")
        self.table_button = button
        candidates = [a for a in button.actions() if a.objectName() == "mActionSelectedFilter"]
        self.require(candidates, "Show selected features action missing")
        self.table_filter_action = candidates[0]
        self.table_filter_action.trigger()
        self.later(self.table_filtered)

    def table_filtered(self):
        views = [w for w in self.table.findChildren(QWidget) if w.inherits("QgsDualView")]
        self.require(views, "Dual view missing")
        view = sip.cast(views[0], QgsDualView)
        self.require(view.filteredFeatureCount() == 3 and self.municipalities.featureCount() == 184, "Table filtering changed the wrong state")
        self.later(self.table_shot)
        self.table_button.showMenu()

    def table_shot(self):
        self.table_menu = QApplication.activePopupWidget()
        self.require(isinstance(self.table_menu, QMenu), "Native table filter menu missing")
        rect = self.table_menu.actionGeometry(self.table_filter_action)
        rect.moveTopLeft(self.table_menu.mapToGlobal(rect.topLeft()))
        self.dynamic_targets["tigTableSelectedFilter"] = rect
        self.capture("table-filter", self.table, {"layer_features": 184, "selected": 3, "table_features": 3}, popups=True)
        self.table_menu.hide()
        self.later(self.table_visible)

    def table_view(self):
        return sip.cast(next(w for w in self.table.findChildren(QWidget) if w.inherits("QgsDualView")), QgsDualView)

    def table_visible(self):
        self.table.setMinimumHeight(410)
        next(a for a in self.table_button.actions() if a.objectName() == "mActionVisibleFilter").trigger()
        self.later(self.table_visible_shot)

    def table_visible_shot(self):
        count = self.table_view().filteredFeatureCount()
        self.require(0 < count < 184, "Visible filter does not reflect the local extent")
        self.trace["steps"].append({"operation": "table visible filter", "rows": count, "layer_count": 184})
        self.capture("table-visible-filter", self.table, {"rows": count, "layer_count": 184})
        self.municipalities.removeSelection()
        self.later(self.table_expression_dialog)
        next(a for a in self.table_button.actions() if a.objectName() == "mActionAdvancedFilter").trigger()

    def expression_builder(self, dialog, text):
        candidates = [w for w in dialog.findChildren(QWidget) if w.inherits("QgsExpressionBuilderWidget")]
        self.require(candidates, "Expression builder missing")
        builder = sip.cast(candidates[0], QgsExpressionBuilderWidget)
        builder.setExpressionText(text)
        self.readable_editor(dialog)
        return builder

    def table_expression_dialog(self):
        dialog = self.modal()
        self.expression_builder(dialog, '\"NAMEUNIT\" IN (\'Vila-seca\',\'Salou\',\'Reus\')')
        self.later(lambda: self.finish_table_expression(dialog))

    def finish_table_expression(self, dialog):
        self.later(self.table_expression_shot)
        self.accept(dialog)

    def table_expression_shot(self):
        self.require(self.table_view().filteredFeatureCount() == 3 and self.municipalities.selectedFeatureCount() == 0, "Table expression selected features")
        query = self.table.findChild(QLineEdit, "mFilterQuery")
        query.setMinimumWidth(query.fontMetrics().horizontalAdvance(query.text()) + 40)
        query.setCursorPosition(0)
        self.table.adjustSize()
        self.later(self.table_expression_final_shot)

    def table_expression_final_shot(self):
        self.capture("table-expression-filter", self.table, {"rows": 3, "selected": 0, "layer_count": 184})
        self.table.close()
        self.later(self.selection_menu)

    def expression_menu(self):
        bar = self.window.menuBar()
        edit = next(a for a in bar.actions() if normal(a.text()) in {"edita", "edit"})
        parent = edit.menu()
        selection = next(a for a in parent.actions() if a.menu() is not None and ("seleccio" in normal(a.text()) or "select" in normal(a.text())))
        parent.popup(bar.mapToGlobal(bar.actionGeometry(edit).bottomLeft()))
        parent.setActiveAction(selection)
        self.expression_selection_menu = selection.menu()
        self.expression_selection_menu.popup(parent.mapToGlobal(parent.actionGeometry(selection).topRight()))
        self.expression_action = next(a for a in self.expression_selection_menu.actions() if "expressi" in normal(a.text()))
        self.expression_selection_menu.setActiveAction(self.expression_action)
        self.later(self.expression_menu_shot)

    def expression_menu_shot(self):
        rect = self.expression_selection_menu.actionGeometry(self.expression_action)
        rect.moveTopLeft(self.expression_selection_menu.mapToGlobal(rect.topLeft()))
        self.dynamic_targets["tigExpressionMenuAction"] = rect
        self.capture("selection-expression-menu", self.expression_selection_menu, {"action": self.expression_action.text()}, popups=True)
        for menu in QApplication.topLevelWidgets():
            if isinstance(menu, QMenu):
                menu.hide()
        self.later(self.expression_selection_dialog)
        self.expression_action.trigger()

    def expression_selection_dialog(self):
        dialogs = [w for w in QApplication.topLevelWidgets() if w.isVisible() and w.inherits("QgsExpressionSelectionDialog")]
        self.require(dialogs, "Native selection-by-expression dialog missing")
        self.selection_dialog = dialogs[0]
        self.selection_builder = self.expression_builder(self.selection_dialog, '\"NATCODE\"=\'34094343171\'')
        self.selection_dialog.resize(950, 620)
        self.dump(self.selection_dialog, "selection-expression-controls")
        self.selection_button = self.selection_dialog.findChild(QToolButton, "mButtonSelect")
        self.require(self.selection_button is not None, "Native Select button missing")
        self.selection_button.setObjectName("tigSelectExpressionButton")
        self.later(self.expression_selection_shot)

    def expression_selection_shot(self):
        self.require(self.selection_builder.isExpressionValid(), "Invalid selection expression")
        self.capture("selection-expression-dialog", self.selection_dialog, {"expression": '\"NATCODE\"=\'34094343171\'', "layer_count": 184})
        self.selection_button.click()
        self.later(self.expression_selected)

    def expression_selected(self):
        self.require(self.municipalities.selectedFeatureIds() == [self.manual_id], "Expression and manual click disagree")
        self.trace["steps"].append({"operation": "native selection by expression", "selected": 1, "NATCODE": "34094343171"})
        self.selection_dialog.close()
        self.municipalities.removeSelection()
        self.project.addMapLayer(self.boundary)
        self.portals = self.load(self.control["input_paths"]["cartociudad"], "Portals CartoCiudad", "portalpk_publi")
        self.later(lambda: self.layer_menu(self.portals, None, '"tipo"=\'Portal\'', "portals-filter", self.spatial_dialog))

    def spatial_dialog(self, kind="portals"):
        self.spatial_kind = kind
        self.spatial_layer = {"portals": self.portals, "blocks": getattr(self, "blocks", None),
                              "roads": getattr(self, "roads", None)}[kind]
        self.spatial_table = {"portals": "portals_vilaseca", "blocks": "illes_vilaseca", "roads": "transport_candidats_c06"}[kind]
        self.spatial_shot_id = {"portals": "spatial-selection", "blocks": "blocks-spatial-selection", "roads": "roads-spatial-selection"}[kind]
        self.spatial_predicate = 6 if kind == "blocks" else 0
        self.spatial_expected = self.control["exports"][self.spatial_table]["count"]
        if kind == "portals":
            self.require(self.portals.subsetString() == '"tipo"=\'Portal\'', "Portal filter missing")
        iface.setActiveLayer(self.spatial_layer)
        sys.path.insert(0, str(Path(QgsApplication.pkgDataPath()) / "python/plugins"))
        import qgis.utils
        if "processing" not in qgis.utils.plugins:
            qgis.utils.loadPlugin("processing")
            qgis.utils.startPlugin("processing")
        import processing
        self.algorithm_dialog = processing.createAlgorithmDialog("native:selectbylocation", {
            "INPUT": self.spatial_layer, "PREDICATE": [self.spatial_predicate], "INTERSECT": self.boundary, "METHOD": 0})
        self.algorithm_dialog.show()
        self.algorithm_dialog.resize(900, 650)
        for combo in self.algorithm_dialog.findChildren(QComboBox):
            if self.boundary.name() in combo.currentText():
                combo.setObjectName("tigSpatialReference")
        self.later(self.spatial_shot)

    def spatial_shot(self):
        buttons = [button for button in self.algorithm_dialog.findChildren(QPushButton)
                   if button.isVisible() and normal(button.text()) in {"executa", "run"}]
        self.require(len(buttons) == 1, "Native Processing Run button missing")
        buttons[0].setObjectName("tigSpatialRun")
        predicate_text = "estan dins" if self.spatial_kind == "blocks" else "intersecta"
        predicate = next(w for w in self.algorithm_dialog.findChildren(QCheckBox) if normal(w.text()) == predicate_text)
        predicate.setObjectName("tigSpatialPredicate")
        self.capture(self.spatial_shot_id, self.algorithm_dialog, {"algorithm": "native:selectbylocation",
            "input": self.spatial_layer.name(), "reference": self.boundary.name(), "predicate": predicate_text, "method": "new selection"})
        self.spatial_layer.removeSelection()
        self.spatial_attempts = 0
        self.later(self.spatial_completed, 1000)
        buttons[0].click()

    def spatial_completed(self):
        self.spatial_attempts += 1
        if self.spatial_layer.selectedFeatureCount() != self.spatial_expected:
            self.require(self.spatial_attempts < 30, "Spatial GUI result did not match the computed control")
            self.later(self.spatial_completed, 1000)
            return
        self.trace["steps"].append({"operation": "native:selectbylocation GUI", "kind": self.spatial_kind,
                                    "selected": self.spatial_layer.selectedFeatureCount(), "predicate": self.spatial_predicate})
        self.algorithm_dialog.close()
        if self.spatial_kind == "portals":
            self.project.removeMapLayer(self.municipalities.id())
            self.portals.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
                {"color": "#777777", "outline_color": "#333333", "size": "1.2", "outline_width": "0.12"})))
        elif self.spatial_kind == "blocks":
            self.blocks.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
                {"color": "180,180,180,115", "outline_color": "#59636a", "outline_width": "0.25"})))
        else:
            self.roads.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
                {"line_color": "#6b7178", "line_width": "1.0"})))
        self.show_map([self.spatial_layer])
        self.later(self.selected_map_shot, 1600)

    def show_map(self, layers):
        visible = {layer.id() for layer in [self.wms, self.boundary, *layers]}
        for layer in self.project.mapLayers().values():
            node = self.project.layerTreeRoot().findLayer(layer.id())
            if node is not None:
                node.setItemVisibilityChecked(layer.id() in visible)
        iface.messageBar().clearWidgets()
        iface.setActiveLayer(layers[0])
        for layer in [self.boundary, *layers]:
            layer.triggerRepaint()
        iface.mapCanvas().setExtent(self.extent)
        iface.mapCanvas().refresh()

    def selected_map_shot(self):
        key = self.spatial_kind + "-selected"
        self.capture(key, evidence={"selected": self.spatial_layer.selectedFeatureCount(),
                                   "layer": self.spatial_layer.name(), "temporary_selection": True})
        self.begin_selected_export()

    def begin_selected_export(self):
        self.export_table = self.spatial_table
        self.export_source = self.spatial_layer
        self.export_kind = self.spatial_kind
        with sqlite3.connect(f"file:{GPKG}?mode=ro", uri=True) as db:
            self.require(db.execute("SELECT count(*) FROM sqlite_master WHERE name=?", (self.export_table,)).fetchone()[0] == 0,
                         "Destination must not exist before its native export")
        iface.setActiveLayer(self.export_source)
        view = iface.layerTreeView()
        view.selectionModel().select(view.currentIndex(), QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        position = view.visualRect(view.currentIndex()).center()
        self.later(self.selected_export_menu)
        QApplication.sendEvent(view.viewport(), QContextMenuEvent(QContextMenuEvent.Mouse, position, view.viewport().mapToGlobal(position)))

    def selected_export_menu(self):
        self.export_menu = QApplication.activePopupWidget()
        self.require(isinstance(self.export_menu, QMenu), "Native layer context menu missing")
        view = iface.layerTreeView()
        row = view.visualRect(view.currentIndex())
        self.export_menu.move(view.mapToGlobal(QPoint(view.width() + 16, row.top())))
        action = next(a for a in self.export_menu.actions() if normal(a.text()) in {"exporta", "export"})
        self.export_submenu = action.menu()
        self.require(self.export_submenu is not None, "Native Export submenu missing")
        self.export_menu.setActiveAction(action)
        self.export_submenu.popup(self.export_menu.mapToGlobal(self.export_menu.actionGeometry(action).topRight()))
        self.export_action = next(a for a in self.export_submenu.actions() if "seleccion" in normal(a.text()) or "selected" in normal(a.text()))
        self.export_submenu.setActiveAction(self.export_action)
        self.later(self.selected_export_menu_shot)

    def selected_export_menu_shot(self):
        rect = self.export_submenu.actionGeometry(self.export_action)
        rect.moveTopLeft(self.export_submenu.mapToGlobal(rect.topLeft()))
        self.dynamic_targets["tigSelectedExportAction"] = rect
        if self.export_kind == "portals":
            self.capture("selected-export-menu", evidence=
                         {"action": self.export_action.text(), "selected": self.export_source.selectedFeatureCount()}, popups=True)
        self.later(self.configure_selected_export)
        self.export_action.trigger()

    def configure_selected_export(self):
        dialog = self.modal()
        self.require(dialog.inherits("QgsVectorLayerSaveAsDialog"), "Not the native vector export dialog")
        self.export_dialog = sip.cast(dialog, QgsVectorLayerSaveAsDialog)
        formats = [c for c in dialog.findChildren(QComboBox) if c.findText("GeoPackage") >= 0]
        self.require(len(formats) == 1, "GeoPackage format selector missing")
        formats[0].setCurrentIndex(formats[0].findText("GeoPackage"))
        self.later(self.selected_export_parameters, 400)

    def selected_export_parameters(self):
        dialog = self.export_dialog
        self.dump(dialog, f"{self.export_kind}-export-controls")
        files = dialog.findChildren(QgsFileWidget)
        self.require(len(files) == 1, "Export file widget missing")
        files[0].setFilePath(str(GPKG))
        files[0].setObjectName("tigExportFile")
        name = dialog.findChild(QLineEdit, "mLayerName")
        if name is None:
            name = dialog.findChild(QLineEdit, "leLayername")
        self.require(name is not None, "Export layer-name control missing")
        name.setText(self.export_table)
        name.setObjectName("tigExportLayer")
        crs = next(w for w in dialog.findChildren(QWidget) if w.inherits("QgsProjectionSelectionWidget"))
        sip.cast(crs, QgsProjectionSelectionWidget).setCrs(QgsCoordinateReferenceSystem("EPSG:25831"))
        crs.setObjectName("tigExportCrs")
        dialog.setOnlySelected(True)
        dialog.setAddToCanvas(True)
        selected = next(w for w in dialog.findChildren(QCheckBox) if "seleccion" in normal(w.text()) or "selected" in normal(w.text()))
        selected.setObjectName("tigExportSelected")
        for widget in dialog.findChildren(QWidget):
            if widget.inherits("QgsCollapsibleGroupBox"):
                sip.cast(widget, QgsCollapsibleGroupBox).setCollapsed(True)
        dialog.resize(900, 540)
        self.later(self.selected_export_dialog_shot)

    def selected_export_dialog_shot(self):
        dialog = self.export_dialog
        self.export_evidence = {"format": dialog.format(), "filename": dialog.fileName(), "table": dialog.layerName(),
            "only_selected": dialog.onlySelected(), "crs": dialog.crs().authid(), "add_to_canvas": dialog.addToCanvas(),
            "initially_absent": True, "count": self.export_source.selectedFeatureCount()}
        self.require(dialog.format() == "GPKG" and dialog.onlySelected() and dialog.layerName() == self.export_table,
                     "Wrong native export configuration")
        self.capture(self.export_kind + "-export-dialog", dialog, self.export_evidence)
        self.export_attempts = 0
        self.later(self.selected_export_completed, 1000)
        self.accept(dialog)

    def selected_export_completed(self):
        self.export_attempts += 1
        candidates = [layer for layer in self.project.mapLayers().values() if layer.providerType() == "ogr"
                      and str(GPKG) in layer.source() and f"layername={self.export_table}" in layer.source()]
        if not candidates:
            dialog = QApplication.activeModalWidget()
            if dialog is not None:
                self.dump(dialog, "export-confirmation")
            self.require(self.export_attempts < 30, "The native export did not load a result")
            self.later(self.selected_export_completed, 750)
            return
        self.require(len(candidates) == 1, "Ambiguous native export result")
        result = candidates[0]
        proof = self.control["exports"][self.export_table]
        self.require(result.isValid() and result.featureCount() == proof["count"] and result.crs().authid() == "EPSG:25831", "Wrong native export result")
        sys.path.insert(0, str(SOURCE_ROOT / "context/practiques"))
        from prepare_pr3_guided import content_signature, store_measures
        self.require(content_signature(result, proof["fields"]) == proof["sha256"], "Native export changed the selected attributes or geometry")
        self.export_evidence.update(source=result.source(), verified_signature=proof["sha256"])
        self.trace.setdefault("native_exports", []).append(self.export_evidence)
        self.trace["steps"].append({"operation": "native selected export and reload", "table": self.export_table, "count": result.featureCount()})
        self.export_source.removeSelection()
        self.project.removeMapLayer(self.export_source.id())
        result.removeSelection()
        if self.export_kind == "portals":
            self.output_portals = result
            result.setName("Portals seleccionats · desats")
            result.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
                {"color": "#b84200", "outline_color": "white", "outline_width": "0.12", "size": "1.4"})))
            self.blocks = self.load(self.control["input_paths"]["cartociudad"], "Illes CartoCiudad", "manzana")
            self.later(lambda: self.spatial_dialog("blocks"))
        elif self.export_kind == "blocks":
            self.output_blocks = result
            result.setName("Illes seleccionades · desades")
            result.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
                {"color": "125,185,215,170", "outline_color": "#126090", "outline_width": "0.28"})))
            self.show_map([self.output_portals, self.output_blocks])
            self.later(self.results_shot, 1600)
        else:
            self.output_roads = result
            store_measures(result, self.control["road_measurements"], "fid")
            result.setName("Autovies i autopistes · desades")
            result.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
                {"line_color": "#0072b2", "line_width": "0.8"})))
            text = QgsTextFormat()
            text.setSize(13)
            halo = QgsTextBufferSettings()
            halo.setEnabled(True)
            halo.setSize(1)
            halo.setColor(QColor("white"))
            text.setBuffer(halo)
            root = QgsRuleBasedLabeling.Rule(None)
            reference = next(self.boundary.getFeatures()).geometry()
            for road_name in ("A-7", "AP-7"):
                candidates = [f for f in result.getFeatures() if f["nombre"] == road_name and f.geometry().within(reference)]
                self.require(candidates, f"No interior segment available for the {road_name} label")
                labelled = max(candidates, key=lambda f: f.geometry().length())
                settings = QgsPalLayerSettings()
                settings.fieldName = "nombre"
                settings.placement = Qgis.LabelPlacement.Line
                settings.setFormat(text)
                rule = QgsRuleBasedLabeling.Rule(settings)
                rule.setFilterExpression(f"$id={labelled.id()}")
                root.appendChild(rule)
                self.trace.setdefault("road_label_ids", {})[road_name] = {"fid": labelled.id(), "id_tramo": labelled["id_tramo"]}
            result.setLabeling(QgsRuleBasedLabeling(root))
            result.setLabelsEnabled(True)
            self.show_map([result])
            self.later(self.roads_result_shot, 1600)

    def results_shot(self):
        self.capture("exported-selections", evidence={"portals": self.output_portals.featureCount(),
            "blocks": self.output_blocks.featureCount(), "sources": [self.output_portals.source(), self.output_blocks.source()]})
        self.roads = self.load(self.control["input_paths"]["transport"], "Vials RT · rt_tramo_vial", "rt_tramo_vial")
        self.later(lambda: self.layer_menu(self.roads, None, self.control["criteria"]["vies_principals"], "roads-filter", lambda: self.spatial_dialog("roads")))

    def roads_result_shot(self):
        self.capture("roads-result", evidence={"count": self.output_roads.featureCount(), "source": self.output_roads.source(),
                                               "names": self.control["motorways"]["names"], "selected": 0})
        self.later(self.calculator)

    def calculator(self):
        self.measure_layer = self.load(GPKG, "Municipis · mesures", "municipis_tarragona")
        self.measure_layer.setDisplayExpression('"NAMEUNIT"')
        iface.setActiveLayer(self.measure_layer)
        self.measure_layer.removeSelection()
        self.later(self.configure_calculator)
        iface.actionOpenFieldCalculator().trigger()

    def configure_calculator(self):
        self.calc = self.modal()
        self.dump(self.calc, "calculator-controls")
        name = self.calc.findChild(QLineEdit, "mOutputFieldNameLineEdit")
        self.require(name is not None, "Output field name control missing")
        name.setText("area_km2")
        types = self.calc.findChild(QComboBox, "mOutputFieldTypeComboBox")
        self.require(types is not None, "Output type control missing")
        matches = [i for i in range(types.count()) if any(word in normal(types.itemText(i)) for word in ("decimal", "real", "double"))]
        self.require(matches, "Decimal field type missing")
        types.setCurrentIndex(matches[0])
        for spin in self.calc.findChildren(QSpinBox):
            if "precision" in spin.objectName().lower():
                spin.setValue(8)
            elif "length" in spin.objectName().lower() or "width" in spin.objectName().lower():
                spin.setValue(20)
        widgets = [w for w in self.calc.findChildren(QWidget) if w.inherits("QgsExpressionBuilderWidget")]
        self.require(widgets, "Native expression builder missing")
        self.expression_widget = sip.cast(widgets[0], QgsExpressionBuilderWidget)
        self.expression_widget.setExpressionText("$area / 1000000")
        self.readable_editor(self.calc)
        self.calc.resize(1000, 680)
        self.later(self.calculator_shot)

    def calculator_shot(self):
        self.require(self.expression_widget.isExpressionValid(), "Invalid calculator expression")
        self.capture("field-calculator", self.calc, {"expression": "$area / 1000000", "field": "area_km2", "ellipsoid": self.project.ellipsoid(), "area_unit": "m2"})
        self.later(self.calculated, 1200)
        self.accept(self.calc)

    def calculated(self):
        layer = self.measure_layer
        index = layer.fields().indexFromName("area_km2")
        self.require(index >= 0, "The calculator did not create area_km2")
        expected = {row["NATCODE"]: row for row in self.control["measurements"]["rows"]}
        for feature in layer.getFeatures():
            self.require(abs(feature["area_km2"] - expected[feature["NATCODE"]]["area_km2"]) < 0.00001,
                         "GUI field calculation differs from the QGIS control")
        if layer.isEditable():
            self.require(layer.commitChanges(), str(layer.commitErrors()))
        layer.setFieldAlias(index, "Àrea (km²)")
        self.trace["steps"].append({"operation": "native field calculator", "field": "area_km2", "verified_rows": len(expected)})
        self.later(self.configure_update)
        iface.actionOpenFieldCalculator().trigger()

    def configure_update(self):
        self.update_calc = self.modal()
        self.dump(self.update_calc, "update-calculator-controls")
        groups = [w for w in self.update_calc.findChildren(QGroupBox) if "actualitza" in normal(w.title()) or "update" in normal(w.title())]
        self.require(groups, "Update-existing-field group missing")
        group = groups[0]
        group.setChecked(True)
        group.setObjectName("tigUpdateGroup")
        combo = next(c for c in group.findChildren(QComboBox) if any(c.itemText(i) in {"area_km2", "Àrea (km²)"} for i in range(c.count())))
        combo.setCurrentIndex(next(i for i in range(combo.count()) if combo.itemText(i) in {"area_km2", "Àrea (km²)"}))
        self.expression_builder(self.update_calc, self.control["aggregates"]["updated_expression"])
        self.update_calc.resize(1000, 680)
        self.later(self.update_shot)

    def update_shot(self):
        self.capture("field-update", self.update_calc, {"field": "area_km2", "expression": self.control["aggregates"]["updated_expression"], "rows": 184})
        self.later(self.updated)
        self.accept(self.update_calc)

    def updated(self):
        expected = {row["NATCODE"]: round(row["area_km2"], 6) for row in self.control["measurements"]["rows"]}
        for feature in self.measure_layer.getFeatures():
            self.require(abs(feature["area_km2"] - expected[feature["NATCODE"]]) < 1e-10, "Native update did not cover every row")
        self.require(self.measure_layer.commitChanges(), str(self.measure_layer.commitErrors()))
        self.trace["steps"].append({"operation": "native field update", "rows": 184, "expression": self.control["aggregates"]["updated_expression"]})
        self.later(self.configure_aggregate)
        iface.actionOpenFieldCalculator().trigger()

    def configure_aggregate(self):
        self.aggregate_calc = self.modal()
        self.aggregate_calc.findChild(QLineEdit, "mOutputFieldNameLineEdit").setText("quota_area_pct")
        types = self.aggregate_calc.findChild(QComboBox, "mOutputFieldTypeComboBox")
        types.setCurrentIndex(next(i for i in range(types.count()) if any(word in normal(types.itemText(i)) for word in ("decimal", "real", "double"))))
        self.aggregate_builder = self.expression_builder(self.aggregate_calc, self.control["aggregates"]["expression"])
        self.aggregate_calc.resize(1120, 720)
        self.later(self.aggregate_function_help)

    def aggregate_function_help(self):
        def indexes(model, parent=None):
            from qgis.PyQt.QtCore import QModelIndex
            parent = parent if parent is not None else QModelIndex()
            for row in range(model.rowCount(parent)):
                index = model.index(row, 0, parent)
                yield index
                yield from indexes(model, index)
        for tree in self.aggregate_calc.findChildren(QTreeView):
            for index in indexes(tree.model()):
                if str(index.data()).strip() == "aggregate":
                    tree.expand(index.parent())
                    tree.scrollTo(index)
                    tree.setCurrentIndex(index)
                    QTest.mouseClick(tree.viewport(), Qt.LeftButton, Qt.NoModifier, tree.visualRect(index).center())
                    self.later(self.aggregate_shot)
                    return
        self.dump(self.aggregate_calc, "aggregate-calculator-controls")
        raise RuntimeError("aggregate function not found in the native function tree")

    def aggregate_shot(self):
        helps = [w for w in self.aggregate_calc.findChildren(QTextBrowser) if w.isVisible() and "aggregate" in w.toPlainText().lower()]
        self.require(helps, "Native aggregate help is not visible")
        helps[0].setObjectName("tigFunctionHelp")
        self.require(self.aggregate_builder.isExpressionValid(), "Invalid aggregate expression")
        self.capture("aggregate-help", self.aggregate_calc, {"expression": self.control["aggregates"]["expression"], "help": helps[0].toPlainText()})
        self.later(self.aggregated)
        self.accept(self.aggregate_calc)

    def aggregated(self):
        layer = self.measure_layer
        for feature in layer.getFeatures():
            self.require(abs(feature["quota_area_pct"] - self.control["aggregates"]["quota_area_pct"][feature["NATCODE"]]) < 1e-7, "Aggregate percentage differs from independent arithmetic")
        self.require(abs(sum(f["quota_area_pct"] for f in layer.getFeatures()) - 100) < 1e-7, "Area shares do not sum to 100")
        self.require(layer.commitChanges(), str(layer.commitErrors()))
        self.trace["steps"].append({"operation": "native aggregate field", "rows": 184, "sum_pct": 100})
        expression = '"nom_etiqueta" || \'\\n\' || format_number("area_km2", 2, \'ca_ES\') || \' km²\''
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
        context.setFeature(next(layer.getFeatures(QgsFeatureRequest().setFilterExpression('"NATCODE"=\'34094343171\''))))
        label = QgsExpression(expression)
        self.require(label.evaluate(context) == "Vila-seca\n21,71 km²", "Label expression differs from the checked Catalan display")
        labels = QgsPalLayerSettings()
        labels.fieldName = expression
        labels.isExpression = True
        labels.placement = Qgis.LabelPlacement.Horizontal
        labels.setPolygonPlacementFlags(Qgis.LabelPolygonPlacementFlag.AllowPlacementInsideOfPolygon)
        labels.fitInPolygonOnly = True
        text = QgsTextFormat()
        text.setSize(13)
        text.setColor(QColor("#16334a"))
        buffer = QgsTextBufferSettings()
        buffer.setEnabled(True)
        buffer.setSize(0.8)
        buffer.setColor(QColor("white"))
        text.setBuffer(buffer)
        labels.setFormat(text)
        layer.setLabeling(QgsVectorLayerSimpleLabeling(labels))
        layer.setLabelsEnabled(True)
        layer.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({"color":"245,243,232,220", "outline_color":"#3d7287", "outline_width":"0.5"})))
        layer.triggerRepaint()
        for other in (self.output_portals, self.output_blocks, self.output_roads, self.boundary):
            self.project.layerTreeRoot().findLayer(other.id()).setItemVisibilityChecked(False)
        iface.mapCanvas().setExtent(self.extent)
        iface.mapCanvas().refresh()
        self.label_expression = expression
        self.later(self.labels_shot, 1800)

    def labels_shot(self):
        self.capture("label-expression", evidence={"expression": self.label_expression, "numeric_field": "area_km2", "alias": "Àrea (km²)"})
        group = self.project.layerTreeRoot().addGroup("Context i continuïtat")
        for table, title in (("municipi_vilaseca", "Límit ICGC · font heretada"),
                             ("municipi_treball", "Límit de treball · fase anterior"),
                             ("provincies_catalunya", "Províncies de Catalunya"),
                             ("ccaa_context", "Catalunya, Aragó i C. Valenciana")):
            layer = self.load(GPKG, title, table, group)
            group.findLayer(layer.id()).setItemVisibilityChecked(False)
        group.setExpanded(False)
        self.project.setFilePathStorage(Qgis.FilePathType.Relative)
        self.project.setPresetHomePath(".")
        self.require(self.project.write(f"geopackage:{GPKG}?projectName=pr3"), "Cannot retain the project")
        self.require(self.project.write(str(GPKG.with_suffix(".qgz"))), "Cannot write the external project")
        self.trace["complete"] = True
        self.trace["project_save_transport"] = "PyQGIS after the native GUI calculations"
        self.write_trace()
        self.close()


LESSON = FiltersLesson()
