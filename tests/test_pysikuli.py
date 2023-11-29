import pytest

from ..src import pysikuli as sik


class TestPysikuli:
    def test_accessibleNames(self):
        # Check that all the functions are defined.

        # keyboard-related API
        sik.tap
        sik.keyUp
        sik.keyDown
        sik.hotkey
        sik.write
        sik.paste
        sik.copyToClip
        sik.pasteFromClip

        # mouse-related API
        sik.click
        sik.rightClick
        sik.mouseDown
        sik.mouseUp
        sik.mouseMove
        sik.mouseMoveRealive
        sik.dragDrop

        # The functions implemented in the platform-specific modules should also show up in the sik namespace:
        # sik.position
        # sik.scroll
        # sik.hscroll
        sik.activateWindow
        sik.getWindowRegion
        sik.minimizeWindow
        sik.unminimizeWindow

        # utils API
        sik.Key
        sik.Config
        sik.Region
        sik.MONITOR_REGION
        sik.MONITOR_RESOLUTION
        sik.saveScreenshot
        sik.saveNumpyImg
        sik.deleteFile

        # screenshot-related API
        sik.find
        sik.findAny
        sik.getPixel
        sik.wait
        sik.sleep
        sik.exist

        # tools-related API
        sik.getLocation
        sik.getRegion

    def test_getRegion(self):
        test_loc = (500, 500)
        test_interrupt_offset = 100
        sik.mouseMove(test_loc)
        sik._getRegion(sik._REGION_FORMAT, 0.5, test_interrupt_offset)
        captured_reg = sik.pasteFromClip()
        expected_reg = f"{test_loc[0]}, {test_loc[1]}, {test_loc[0] + test_interrupt_offset}, {test_loc[1] + test_interrupt_offset}"

        assert captured_reg == expected_reg
        assert sik.getRegion

    def test_exist_docstring(self):
        assert sik.exist.__doc__ == sik._main._exist.__doc__
